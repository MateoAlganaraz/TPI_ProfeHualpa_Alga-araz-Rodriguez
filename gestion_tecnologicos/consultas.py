from typing import List, Dict
from .filesystem import leer_recursivo

def mostrar_productos(productos: List[Dict]):
    if not productos:
        print("No hay productos que mostrar.")
        return
    print(f"\n{'NOMBRE':<20} {'PRECIO':<10} {'STOCK':<6} {'MODELO':<15} {'UBICACIÓN'}")
    print("-" * 75)
    for p in productos:
        ubicacion = f"{p['categoria']} / {p['marca']} / {p['tipo']}"
        print(f"{p['nombre']:<20} ${p['precio']:<9.2f} {p['stock']:<6} {p['modelo']:<15} {ubicacion}")

def filtrar_productos(productos: List[Dict]) -> List[Dict]:
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

def estadisticas(productos: List[Dict]):
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
    print("Productos por categoría:")
    for cat, cant in por_categoria.items():
        print(f"- {cat}: {cant}")

def ordenar_productos(productos: List[Dict]) -> List[Dict]:
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
        case '3':
            return sorted(productos, key=lambda x: -x["stock"])
        case _:
            print("Opción inválida.")
            return productos