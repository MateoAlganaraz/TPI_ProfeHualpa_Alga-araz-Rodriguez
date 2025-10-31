import os
from typing import List, Dict
from .filesystem import crear_estructura_directorios, leer_csv_producto, guardar_producto_csv, leer_recursivo

def alta_producto():
    print("\n=== ALTA DE PRODUCTO ===")
    categoria = input("Categoría (ej: Computadoras, Teléfonos, Accesorios): ").strip()
    marca = input("Marca (ej: Apple, Samsung): ").strip()
    tipo = input("Tipo de producto (ej: Laptop, Smartphone): ").strip()

    if not all([categoria, marca, tipo]):
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

    ruta_csv = crear_estructura_directorios(categoria, marca, tipo)
    productos_existentes = leer_csv_producto(ruta_csv, categoria, marca, tipo) if os.path.exists(ruta_csv) else []

    nuevo_producto = {
        "nombre": nombre, "precio": precio, "stock": stock, "modelo": modelo,
        "categoria": categoria, "marca": marca, "tipo": tipo
    }
    productos_existentes.append(nuevo_producto)
    guardar_producto_csv(ruta_csv, productos_existentes)
    print("Producto registrado correctamente.")

def modificar_producto():
    todos = leer_recursivo()
    if not todos:
        print("No hay productos registrados.")
        return

    nombre = input("Nombre exacto del producto a modificar: ").strip()
    coincidencias = [p for p in todos if p["nombre"].lower() == nombre.lower()]
    if not coincidencias:
        print("Producto no encontrado.")
        return
    if len(coincidencias) > 1:
        print("Hay varios productos con ese nombre. Se modificará el primero.")
    producto = coincidencias[0]

    print(f"\nProducto encontrado: {producto['nombre']} (en {producto['categoria']}/{producto['marca']}/{producto['tipo']})")
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

    producto[campo] = nuevo_valor
    ruta_csv = crear_estructura_directorios(producto["categoria"], producto["marca"], producto["tipo"])
    productos_en_archivo = leer_csv_producto(ruta_csv, producto["categoria"], producto["marca"], producto["tipo"])

    for i, p in enumerate(productos_en_archivo):
        if p["nombre"] == producto["nombre"] and p["modelo"] == producto["modelo"]:
            productos_en_archivo[i] = producto
            break

    guardar_producto_csv(ruta_csv, productos_en_archivo)
    print("Producto actualizado.")

def eliminar_producto():
    todos = leer_recursivo()
    if not todos:
        print("No hay productos registrados.")
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
    productos_filtrados = [
        p for p in productos_en_archivo
        if not (p["nombre"] == producto["nombre"] and p["modelo"] == producto["modelo"])
    ]
    guardar_producto_csv(ruta_csv, productos_filtrados)
    print("Producto eliminado.")