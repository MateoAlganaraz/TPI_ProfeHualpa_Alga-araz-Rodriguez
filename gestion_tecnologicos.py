import os 
import csv
from typing import List, Dict, Optional

DATOS_DIR = "datos"

CAMPOS_PRODUCTOS = ["nombre", "precio", "stock", "modelo"]

def crear_estructura_directorios(categoria: str, marca: str, tipo: str) -> str:
    """Crea la ruta de directorios jerárquicos y devuelve la ruta del archivo CSV."""
    ruta_categoria = os.path.join(DATOS_DIR, categoria)
    ruta_marca = os.path.join(ruta_categoria, marca)
    os.makedirs(ruta_marca, exist_ok=True)
    return os.path.join(ruta_marca, f"{tipo}.csv")

def leer_csv_producto(ruta_archivo:str, categoria:str, marca:str, tipo:str) -> List[Dict]:
    """Lee un archivo CSV y devuelve una lista de productos con metadatos jerárquicos."""
    productos = []
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            lector = csv.DictReader(f)
            if set(CAMPOS_PRODUCTOS).issubset(lector.fieldnames or []):
                for fila in lector:
                    try:
                        producto = {
                            "nombre": fila["nombre"].strip(),
                            "precio": float(fila["precio"]),
                            "stock": int(fila["stock"]),
                            "modelo": fila["modelo"].strip(),
                            "categoria": categoria,
                            "marca": marca,
                            "tipo": tipo
                        }
                        if producto["precio"] > 0 and producto["stock"] >= 0:
                            productos.append(producto)
                    except (ValueError, KeyError):
                        continue #Saltar filas inválidas
    except (FileNotFoundError, OSError):
        pass
    return productos

def leer_recursivo(ruta: str = DATOS_DIR) -> list[Dict]:
    """Función recursiva que recorre toda la jerarquía y devuelve todos los productos."""
    todos_productos = []

    if not os.path.exists(ruta):
        return todos_productos
    
    for item in os.listdir(ruta):
        ruta_completa = os.path.join(ruta,item)

        if os.path.isdir(ruta_completa):
            #Paso recursivo: Explorar subdirectorio
            todos_productos.extend(leer_recursivo(ruta_completa))
        elif item.endswith(".csv") and os.path.isfile(ruta_completa):
            #Caso base: es un archivo CSV
            #Extraer jerarquía de la ruta
            partes = os.path.normpath(ruta).split(os.sep)
            if len(partes) >= 2:
                tipo = os.path.splitext(item)[0]
                marca = partes[-1]
                categoria = partes[-2] if len(partes) >= 3 else "Desconocida"
                productos = leer_csv_producto(ruta_completa, categoria, marca, tipo)
                todos_productos.extend(productos)

    return todos_productos

def guardar_producto_csv(ruta_archivo: str, productos: List[Dict]):
    """Sobrescribe un archivo CSV con la lista de productos (sin metadatos jerárquicos)"""
    try:
        with open(ruta_archivo, 'w', newline='',encoding='utf-8') as f:
            escritor = csv.DictWriter(f, fieldnames=CAMPOS_PRODUCTOS)
            escritor.writeheader()
            for p in productos:
                escritor.writerow({k: p[k] for k in CAMPOS_PRODUCTOS})
    except Exception as e:
        print(f"Error al guardar {ruta_archivo}: {e}")

def alta_producto():
    """Registra un nuevo producto, creando la estructura de directorios si es necesario."""
    print("\n=== ALTA DE PRODUCTO ===")
    categoria = input("Categoría (ej: Computadoras, Teléfonos, Accesorios): ").strip()
    marca = input("Marca (ej: Apple, Samsung): ").strip()
    tipo = input("Tipo de producto (ej: Laptop, Smartphone): ").strip()

    if not all([categoria,marca,tipo]):
        print("Todos los niveles jerárquicos son obligatorios.")
        return
    
    nombre = input("Nombre del producto: ").strip()
    modelo = input("Modelo: ").strip()
    if not nombre or not modelo:
        print("Nombre y modelo son obligatorios.")
        return
    
    try:
        precio = float(input("Precio (número positivo): "))
        stock = int(input("Stock (entero >= 0): "))
        if precio <= 0 or stock < 0:
            print("El precio debe ser mayor a 0 y el stock no puede ser negativo")
            return
    except ValueError:
        print("Valores numéricos inválidos.")
        return
    
    #Crear ruta y cargar productos existentes en ese archivo
    ruta_csv = crear_estructura_directorios(categoria, marca, tipo)
    productos_existentes = []
    if os.path.exists(ruta_csv):
        productos_existentes = leer_csv_producto(ruta_csv, categoria, marca, tipo)

    #Agregar nuevo producto
    nuevo_producto = {
        "nombre": nombre, "precio": precio, "stock": stock, "modelo": modelo,
        "categoria": categoria, "marca": marca, "tipo": tipo
    }
    productos_existentes.append(nuevo_producto)

    #Guardar (solo los campos del CSV)
    guardar_producto_csv(ruta_csv, productos_existentes)
    print("Producto registrado correctamente.")

def mostrar_productos(productos: List[Dict]):
    """Muestra una lista de productos con su jerarquía."""
    if not productos:
        print("No hay productos que mostrar.")
        return
    print(f"\n{'NOMBRE':<20} {'PRECIO':<10} {'STOCK':<6} {'MODELO':<15} {'UBICACIÓN'}")
    print("-"*75)
    for p in productos:
        ubicacion = f"{p['categoria']} / {p['marca']} / {p['tipo']}"
        print(f"{p['nombre']:<20} ${p['precio']:<9.2f} {p['stock']:<6} {p['modelo']:<15} {ubicacion}")

def filtrar_productos(productos: List[Dict]) -> List[Dict]:
    """Permite filtrar por categoría o rango de precio."""
    print("\nFiltrar por:")
    print("1. Categoría")
    print("2. Rango de precio")
    opcion = input("Seleccione una opción: ").strip()

    match opcion:
        case '1':
            categoria = input("Ingrese categoría: ").strip()
            return [p for p in productos if p["categoria"].lower() == categoria.lower()]
        case '2':
            try:
                min_p = float(input("Precio mínimo: "))
                max_p = float(input("Precio máximo: "))
                return [p for p in productos if min_p <= p["precio"] <= max_p]
            except ValueError:
                print("Valores inválidos.")
                return productos
        case _:
            print("Opción inválida.")
            return productos
        
def modificar_producto():
    """Modifica un producto existente."""
    todos = leer_recursivo()
    if not todos:
        print("No hay productos registrados.")
        return
    
    nombre = input("Nombre exacto del producto a modificar: ").strip()
    coincidencias = [p for p in todos if p["nombre"].lower() == nombre.lower()]

    if not coincidencias:
        print("Porducto no encontrado.")
        return
    if len(coincidencias) > 1:
        print("Hay varios productos con ese nombre. Se modificará el primero.")

    producto = coincidencias[0]
    print(f"\nProducto encontrado: {producto['nombre']} (en {producto['categoria']}/{producto['marca']}/{producto['tipo']})")

    #Pedir nuevo valor
    campo = input("Campo a modificar (precio/stock): ").strip().lower()
    if campo not in ["precio", "stock"]:
        print("Solo se puede modificar 'precio' o 'stock'.")
        return
    
    try:
        nuevo_valor = float(input(f"Nuevo valor para {campo}: "))
        if campo == "stock":
            nuevo_valor = int(nuevo_valor)
        if (campo == "precio" and nuevo_valor <= 0) or (campo == "stock" and nuevo_valor < 0):
            print("Valor no válido según reglas de negocio.")
            return
    except ValueError:
        print("Valor numérico inválido.")
        return
    
    #Actualizar en memoria
    producto[campo] = nuevo_valor

    #Guardar en su archivo CSV específico
    ruta_csv = crear_estructura_directorios(producto["categoria"], producto["marca"], producto["tipo"])
    productos_en_archivo = leer_csv_producto(ruta_csv, producto["categoria"], producto["marca"], producto["tipo"])

    #Reemplazar el producto modificado 
    for i, p in enumerate(productos_en_archivo):
        if p["nombre"] == producto["nombre"] and p["modelo"] == producto["modelo"]:
            productos_en_archivo[i] = producto
            break

    guardar_producto_csv(ruta_csv, productos_en_archivo)
    print("Producto actualizado.")

def eliminar_producto():
    """Eliminar un producto."""
    todos = leer_recursivo()
    if not todos:
        print("No hay prodcutos registrados.")
        return
    
    nombre = input("Nombre exacto del producto a eliminar: ").strip()
    coincidencias = [p for p in todos if p["nombre"].lower() == nombre.lower()]

    if not coincidencias:
        print("Producto no encontrado.")
        return
    if len(coincidencias) > 1:
        print("Hay varios productos con ese nombre. Se eliminará el primero.")

    producto = coincidencias[0]
    ruta_csv = crear_estructura_directorios(producto["categoria"], producto["marca"], producto["tipo"])
    productos_en_archivo = leer_csv_producto(ruta_csv, producto["categoria"], producto["marca"], producto["tipo"])

    #Eliminar del archivo
    productos_filtrados = [
        p for p in productos_en_archivo
        if not (p["nombre"] == producto["nombre"] and p["modelo"] == producto["modelo"])
    ]

    guardar_producto_csv(ruta_csv, productos_filtrados)
    print("Producto eliminado.")

def estadisticas(productos: List[Dict]):
    """Muestra estadísticas básicas."""
    if not productos:
        print("No hay datos para estadísticas.")
        return
    
    total = len(productos)
    promedio_precio = sum(p["precio"] for p in productos) / total
    por_categoria = {}
    for p in productos:
        por_categoria[p["categoria"]] = por_categoria.get(p["categoria"], 0) + 1

    print(f"\nESTADÍSTICAS")
    print(f"Total de productos: {total}")
    print(f"Promedio de precios: ${promedio_precio:.2f}")
    print("Porductos por categoría:")
    for cat,cant in por_categoria.items():
        print(f"-{cat}: {cant}")

def ordenar_productos(productos: List[Dict]) -> List[Dict]:
    """Ordena productos por nombre, precio o stock."""
    print("\nOrdenar por:")
    print("1. Nombre (A-Z)")
    print("2. Precio (menor a mayor)")
    print("3. Stock (mayor a menor)")
    opcion = input("Seleccione una opción: ").strip()

    match opcion:
        case '1':
            return sorted(productos, key=lambda x: x["nombre"].lower())
        case '2':
            return sorted(productos, key=lambda x: x["precio"])
        case'3':
            return sorted(productos, key=lambda x: -x["stock"])
        case _:
            print("Opción inválida.")
            return productos
        
def menu_principal():
    """Menú interactivo principal."""
    while True:
        print("\n" + "="*50)
        print("SISTEMA DE GESTIÓN TECNOLÓGICA")
        print("="*50)
        print("1. Alta de nuevo producto")
        print("2. Mostrar todos los productos")
        print("3. Filtrar productos")
        print("4. Modificar producto")
        print("5. Eliminar producto")
        print("6. Estadísticas")
        print("7. Ordenar productos")
        print("8. Salir")
        print("="*50)     
        opcion = input("Seleccione una opción: ").strip()

        match opcion:
            case '1':
                alta_producto()
            case '2':
                todos = leer_recursivo()
                mostrar_productos(todos)
            case '3':
                todos = leer_recursivo()
                filtrados = filtrar_productos(todos)
                mostrar_productos(filtrados)
            case '4':
                modificar_producto()
            case '5':
                eliminar_producto()
            case '6':
                todos = leer_recursivo()
                estadisticas(todos)
            case '7':
                todos = leer_recursivo()
                ordenados = ordenar_productos(todos)
                mostrar_productos(ordenados)
            case '8':
                print("¡Gracias por usar el sistema!")
                break
            case _:
                print("Opción inválida.")

if __name__ == "__main__":
    #Crear carpeta raíz si no existe
    os.makedirs(DATOS_DIR, exist_ok=True)
    menu_principal()