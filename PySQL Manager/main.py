import sqlite3
import os
from contextlib import contextmanager
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, IntPrompt, Confirm

console = Console()

@contextmanager
def get_db_connection(): # conectar a la base de datos
    conn = None
    try:
        conn = sqlite3.connect('ejemplo_bd.db')
        conn.row_factory = sqlite3.Row  
        yield conn
    except sqlite3.Error as e:
        console.print(f"[red]Error de base de datos: {e}[/red]")
    finally:
        if conn:
            conn.close()

# Menús y opciones actualizados
ui = ['Crear tabla', 'Ver todas las tablas', 'Seleccionar tabla', 'Cerrar sesion']  # Nueva opción añadida
opt_tabla = [
    'Mostrar todos los registros',
    'Ingresar nuevos datos', 
    'Buscar datos', 
    'Actualizar registro',
    'Eliminar fila', 
    'Borrar Tabla', 
    'Volver'
]

def crear_db(name_db, dt_db):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{name_db}'")
            if cursor.fetchone():
                console.print(f"[yellow]La tabla '{name_db}' ya existe.[/yellow]")
                return False
            
            columnas = ", ".join([f"{col_name} {col_type} {nulo}" for col_name, col_type, nulo in dt_db])
            query = f'''
                CREATE TABLE {name_db} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    {columnas}
                )
            '''
            cursor.execute(query)
            conn.commit()
            console.print(f"[green]Tabla '{name_db}' creada exitosamente.[/green]")
            return True
        except sqlite3.Error as e:
            console.print(f"[red]Error al crear la tabla: {e}[/red]")
            return False

def list_tablas():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name != 'sqlite_sequence'")
        return [tabla[0] for tabla in cursor.fetchall()]

def mostrar_todas_tablas():
    tablas = list_tablas()
    if not tablas:
        console.print("[yellow]No hay tablas en la base de datos.[/yellow]")
        return False
    
    table = Table(title="Tablas Disponibles en la Base de Datos")
    table.add_column("N°", style="cyan")
    table.add_column("Nombre de la Tabla", style="magenta")
    
    for i, tabla in enumerate(tablas, 1):
        table.add_row(str(i), tabla)
    
    console.print(table)
    return True

def get_columnas(name):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(f"PRAGMA table_info({name})")
            columnas = cursor.fetchall()
            return [columna[1] for columna in columnas] if columnas else []
        except sqlite3.Error:
            return []

def mostrar_tabla_completa(name):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(f"SELECT * FROM {name}")
            registros = cursor.fetchall()
            
            if not registros:
                console.print(f"[yellow]La tabla '{name}' está vacía.[/yellow]")
                return
            
            table = Table(title=f"Contenido de la tabla '{name}'")
            columnas = get_columnas(name)
            
            for col in columnas:
                table.add_column(col)
                
            for registro in registros:
                table.add_row(*[str(registro[col]) for col in columnas])
                
            console.print(table)
            return True
        except sqlite3.Error as e:
            console.print(f"[red]Error al mostrar la tabla: {e}[/red]")
            return False

def ingresar_datos(name, datos, columnas):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            columnas_sin_id = [col for col in columnas if col != 'id']
            query = f"INSERT INTO {name} ({', '.join(columnas_sin_id)}) VALUES ({', '.join(['?']*len(columnas_sin_id))})"
            cursor.execute(query, datos)
            conn.commit()
            console.print(f"[green]Datos insertados correctamente en '{name}'.[/green]")
            return True
        except sqlite3.Error as e:
            console.print(f"[red]Error al insertar datos: {e}[/red]")
            return False

def buscar_datos(name, columna, valor):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            query = f"SELECT * FROM {name} WHERE {columna} LIKE ?"
            cursor.execute(query, (f"%{valor}%",))
            registros = cursor.fetchall()
            
            if not registros:
                console.print("[yellow]No se encontraron registros.[/yellow]")
                return False
            
            table = Table(title=f"Resultados de búsqueda en '{name}'")
            columnas = get_columnas(name)
            
            for col in columnas:
                table.add_column(col)
                
            for registro in registros:
                table.add_row(*[str(registro[col]) for col in columnas])
                
            console.print(table)
            return True
        except sqlite3.Error as e:
            console.print(f"[red]Error en la búsqueda: {e}[/red]")
            return False

def actualizar_registro(name, id_registro, nuevos_datos):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            columnas = get_columnas(name)
            columnas_sin_id = [col for col in columnas if col != 'id']
            
            if len(nuevos_datos) != len(columnas_sin_id):
                console.print("[red]Número de datos incorrecto[/red]")
                return False
                
            set_clause = ", ".join([f"{col} = ?" for col in columnas_sin_id])
            query = f"UPDATE {name} SET {set_clause} WHERE id = ?"
            
            cursor.execute(query, (*nuevos_datos, id_registro))
            conn.commit()
            
            if cursor.rowcount == 0:
                console.print("[yellow]No se actualizó ningún registro.[/yellow]")
                return False
                
            console.print(f"[green]Registro {id_registro} actualizado correctamente.[/green]")
            return True
        except sqlite3.Error as e:
            console.print(f"[red]Error al actualizar: {e}[/red]")
            return False

def eliminar_fila(name, columna, valor):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            query = f"DELETE FROM {name} WHERE {columna} = ?"
            cursor.execute(query, (valor,))
            conn.commit()
            
            if cursor.rowcount == 0:
                console.print("[yellow]No se eliminó ningún registro.[/yellow]")
                return False
                
            console.print(f"[green]Registro(s) eliminado(s) correctamente.[/green]")
            return True
        except sqlite3.Error as e:
            console.print(f"[red]Error al eliminar: {e}[/red]")
            return False

def eliminar_tabla(name):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(f"DROP TABLE IF EXISTS {name}")
            conn.commit()
            console.print(f"[green]Tabla '{name}' eliminada correctamente.[/green]")
            return True
        except sqlite3.Error as e:
            console.print(f"[red]Error al eliminar tabla: {e}[/red]")
            return False

def mostrar_menu(titulo, opciones):
    console.print(f"\n[bold cyan]{titulo:^50}[/bold cyan]")
    for i, opcion in enumerate(opciones, 1):
        console.print(f"[bold][{i}][/bold] {opcion}")
    console.print()

def main():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        mostrar_menu("Gestor de base de datos", ui)
        
        try:
            opcion = IntPrompt.ask("Seleccione una opción", choices=[str(i) for i in range(1, len(ui)+1)])
            
            if opcion == 1:  # Crear tabla
                os.system('cls' if os.name == 'nt' else 'clear')
                console.print("[bold]Crear nueva tabla[/bold]\n")
                console.print("La tabla tendrá un ID como PRIMARY KEY AUTOINCREMENT\n")
                
                nombre_tabla = Prompt.ask("Nombre de la tabla").strip()
                if not nombre_tabla:
                    console.print("[red]El nombre no puede estar vacío[/red]")
                    input("Presione Enter para continuar...")
                    continue
                    
                num_columnas = IntPrompt.ask("Número de columnas (sin contar ID)", default=1, show_default=True)
                if num_columnas < 1:
                    console.print("[red]Debe tener al menos una columna[/red]")
                    input("Presione Enter para continuar...")
                    continue
                    
                tipos_validos = ["TEXT", "INTEGER", "REAL", "BLOB", "TEXT UNIQUE"]
                datos_tabla = []
                
                for i in range(num_columnas):
                    console.print(f"\n[bold]Columna {i+1}[/bold]")
                    nombre_col = Prompt.ask("Nombre de la columna").strip().lower()
                    if not nombre_col:
                        console.print("[red]El nombre no puede estar vacío[/red]")
                        break
                        
                    tipo_col = Prompt.ask(
                        "Tipo de dato", 
                        choices=tipos_validos,
                        default="TEXT"
                    ).upper()
                    
                    not_null = Confirm.ask("¿Es NOT NULL?")
                    
                    datos_tabla.append((nombre_col, tipo_col, "NOT NULL" if not_null else ""))
                else:
                    crear_db(nombre_tabla, datos_tabla)
                    
                input("\nPresione Enter para continuar...")
                
            elif opcion == 2:  # Ver todas las tablas (nueva opción)
                os.system('cls' if os.name == 'nt' else 'clear')
                console.print("[bold]Listado de todas las tablas[/bold]\n")
                mostrar_todas_tablas()
                input("\nPresione Enter para continuar...")
                
            elif opcion == 3:  # Seleccionar tabla (ahora es opción 3)
                while True:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    tablas_disponibles = list_tablas()
                    
                    if not tablas_disponibles:
                        console.print("[yellow]No hay tablas disponibles[/yellow]")
                        input("\nPresione Enter para continuar...")
                        break
                        
                    mostrar_menu("Tablas disponibles", tablas_disponibles)
                    console.print(f"[bold][{len(tablas_disponibles)+1}][/bold] Volver")
                    
                    try:
                        opcion_tabla = IntPrompt.ask(
                            "Seleccione una tabla", 
                            choices=[str(i) for i in range(1, len(tablas_disponibles)+2)]
                        )
                        
                        if opcion_tabla == len(tablas_disponibles)+1:
                            break
                            
                        tabla_seleccionada = tablas_disponibles[opcion_tabla-1]
                        
                        while True:
                            os.system('cls' if os.name == 'nt' else 'clear')
                            mostrar_menu(f"Tabla: {tabla_seleccionada}", opt_tabla)
                            
                            opcion_operacion = IntPrompt.ask(
                                "Seleccione una operación", 
                                choices=[str(i) for i in range(1, len(opt_tabla)+1)]
                            )
                            
                            if opcion_operacion == 1:  # Mostrar todos
                                mostrar_tabla_completa(tabla_seleccionada)
                                input("\nPresione Enter para continuar...")
                                
                            elif opcion_operacion == 2:  # Ingresar datos
                                columnas = get_columnas(tabla_seleccionada)
                                columnas_sin_id = [col for col in columnas if col != 'id']
                                
                                if not columnas_sin_id:
                                    console.print("[red]No hay columnas para insertar datos[/red]")
                                    input("\nPresione Enter para continuar...")
                                    continue
                                    
                                datos = []
                                for col in columnas_sin_id:
                                    valor = Prompt.ask(f"Ingrese valor para '{col}'")
                                    datos.append(valor)
                                
                                if ingresar_datos(tabla_seleccionada, datos, columnas):
                                    mostrar_tabla_completa(tabla_seleccionada)
                                input("\nPresione Enter para continuar...")
                                
                            elif opcion_operacion == 3:  # Buscar datos
                                columnas = get_columnas(tabla_seleccionada)
                                columnas_sin_id = [col for col in columnas if col != 'id']
                                
                                if not columnas_sin_id:
                                    console.print("[red]No hay columnas para buscar[/red]")
                                    input("\nPresione Enter para continuar...")
                                    continue
                                    
                                console.print("\nColumnas disponibles:")
                                for i, col in enumerate(columnas_sin_id, 1):
                                    console.print(f"[bold][{i}][/bold] {col}")
                                    
                                opcion_col = IntPrompt.ask(
                                    "Seleccione columna para buscar", 
                                    choices=[str(i) for i in range(1, len(columnas_sin_id)+1)]
                                )
                                
                                valor_busqueda = Prompt.ask("Ingrese valor a buscar")
                                buscar_datos(tabla_seleccionada, columnas_sin_id[opcion_col-1], valor_busqueda)
                                input("\nPresione Enter para continuar...")
                                
                            elif opcion_operacion == 4:  # Actualizar registro
                                if not mostrar_tabla_completa(tabla_seleccionada):
                                    input("\nPresione Enter para continuar...")
                                    continue
                                    
                                id_actualizar = IntPrompt.ask("Ingrese ID del registro a actualizar")
                                columnas = get_columnas(tabla_seleccionada)
                                columnas_sin_id = [col for col in columnas if col != 'id']
                                
                                nuevos_datos = []
                                for col in columnas_sin_id:
                                    nuevo_valor = Prompt.ask(f"Nuevo valor para '{col}'")
                                    nuevos_datos.append(nuevo_valor)
                                
                                if actualizar_registro(tabla_seleccionada, id_actualizar, nuevos_datos):
                                    mostrar_tabla_completa(tabla_seleccionada)
                                input("\nPresione Enter para continuar...")
                                
                            elif opcion_operacion == 5:  # Eliminar fila
                                if not mostrar_tabla_completa(tabla_seleccionada):
                                    input("\nPresione Enter para continuar...")
                                    continue
                                    
                                columnas = get_columnas(tabla_seleccionada)
                                console.print("\nColumnas disponibles:")
                                for i, col in enumerate(columnas, 1):
                                    console.print(f"[bold][{i}][/bold] {col}")
                                    
                                opcion_col = IntPrompt.ask(
                                    "Seleccione columna para eliminar", 
                                    choices=[str(i) for i in range(1, len(columnas)+1)]
                                )
                                
                                valor_eliminar = Prompt.ask(f"Ingrese valor de '{columnas[opcion_col-1]}' a eliminar")
                                
                                if eliminar_fila(tabla_seleccionada, columnas[opcion_col-1], valor_eliminar):
                                    mostrar_tabla_completa(tabla_seleccionada)
                                input("\nPresione Enter para continuar...")
                                
                            elif opcion_operacion == 6:  # Eliminar tabla
                                confirmar = Confirm.ask(
                                    f"[red]¿Está seguro que desea eliminar la tabla '{tabla_seleccionada}'?[/red]", 
                                    default=False
                                )
                                
                                if confirmar:
                                    if eliminar_tabla(tabla_seleccionada):
                                        break
                                input("\nPresione Enter para continuar...")
                                
                            elif opcion_operacion == 7:  # Volver
                                break
                                
                    except Exception as e:
                        console.print(f"[red]Error: {e}[/red]")
                        input("\nPresione Enter para continuar...")
                        
            elif opcion == 4:  # Cerrar sesión (ahora es opción 4)
                console.print("\n[bold green]Sesión finalizada[/bold green]")
                break
                
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            input("\nPresione Enter para continuar...")

if __name__ == "__main__":
    main()