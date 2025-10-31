import os
import csv
from typing import List, Dict
from .config import CAMPOS_PRODUCTO

def crear_estructura_directorios(categoria: str, marca: str, tipo: str) -> str:
    """Crea la ruta de directorios jerárquicos y devuelve la ruta del archivo CSV."""
    ruta_categoria = os.path.join("datos", categoria)
    ruta_marca = os.path.join(ruta_categoria, marca)
    os.makedirs(ruta_marca, exist_ok=True)
    return os.path.join(ruta_marca, f"{tipo}.csv")

def leer_csv_producto(ruta_archivo: str, categoria: str, marca: str, tipo: str) -> List[Dict]:
    """Lee un archivo CSV y devuelve una lista de productos con metadatos jerárquicos."""
    productos = []
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            lector = csv.DictReader(f)
            if set(CAMPOS_PRODUCTO).issubset(lector.fieldnames or []):
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
                        continue
    except (FileNotFoundError, OSError):
        pass
    return productos

def leer_recursivo(ruta: str = "datos") -> List[Dict]:
    """Función recursiva que recorre toda la jerarquía y devuelve todos los productos."""
    todos_productos = []
    if not os.path.exists(ruta):
        return todos_productos

    for item in os.listdir(ruta):
        ruta_completa = os.path.join(ruta, item)
        if os.path.isdir(ruta_completa):
            todos_productos.extend(leer_recursivo(ruta_completa))
        elif item.endswith(".csv") and os.path.isfile(ruta_completa):
            partes = os.path.normpath(ruta).split(os.sep)
            if len(partes) >= 2:
                tipo = os.path.splitext(item)[0]
                marca = partes[-1]
                categoria = partes[-2] if len(partes) >= 3 else "Desconocida"
                productos = leer_csv_producto(ruta_completa, categoria, marca, tipo)
                todos_productos.extend(productos)
    return todos_productos

def guardar_producto_csv(ruta_archivo: str, productos: List[Dict]):
    """Sobrescribe un archivo CSV con solo los campos del producto."""
    try:
        with open(ruta_archivo, 'w', newline='', encoding='utf-8') as f:
            escritor = csv.DictWriter(f, fieldnames=CAMPOS_PRODUCTO)
            escritor.writeheader()
            for p in productos:
                escritor.writerow({k: p[k] for k in CAMPOS_PRODUCTO})
    except Exception as e:
        print(f"Error al guardar {ruta_archivo}: {e}")