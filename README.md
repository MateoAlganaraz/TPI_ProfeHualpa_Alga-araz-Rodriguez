# 🛠️ Sistema de Gestión Jerárquica de Productos Tecnológicos

Este proyecto implementa un sistema de persistencia y consulta de **productos tecnológicos** utilizando una **estructura de directorios jerárquica** de 3 niveles, con almacenamiento en archivos CSV y procesamiento mediante **recursividad**.

## 🌐 Modelo de Datos

### Jerarquía de Clasificación
1. **Categoría**: `Computadoras`, `Teléfonos`, `Accesorios`
2. **Marca**: `Apple`, `Samsung`, `Dell`, `Genérico`, etc.
3. **Tipo de Producto**: `Laptop`, `Smartphone`, `Cargador`, `Cable`, etc.

### Estructura de Directorios
datos/
|---{categoria}/
|---{marca}/
|---{tipo}.csv

### Formato de Datos (CSV)
Cada archivo `.csv` contiene productos con los siguientes campos:
- `nombre` (texto)
- `precio` (float > 0)
- `stock` (entero ≥ 0)
- `modelo` (texto)

Cada producto en memoria es un diccionario que **incluye también los 3 niveles jerárquicos** para facilitar consultas.

## 🚀 Funcionalidades

- ✅ **Alta de producto**: Crea automáticamente la estructura de carpetas si no existe.
- 🔍 **Lectura global**: Usa recursividad para consolidar todos los productos en una lista.
- 🔧 **Modificación**: Actualiza un producto y sobrescribe solo su archivo CSV.
- 🗑️ **Eliminación**: Borra un producto y actualiza su archivo correspondiente.
- 📊 **Estadísticas**: Total de productos, promedio de precios, recuento por categoría.
- 📈 **Ordenamiento**: Por nombre, precio o stock.
- 🔎 **Filtrado**: Por categoría, marca o rango de precio.

## 📦 Requisitos

- Python 3.10 o superior
- No requiere librerías externas (solo módulos estándar: `os`, `csv`)

## ▶️ Instrucciones de Uso

1. Clona o descarga este repositorio.
2. Ejecuta el programa:
   ```bash
   python gestion_tecnologicos.py
3. Sigue las opciones del menú interactivo
4. Los datos se guardarán automáticamente en la carpeta datos/

## Estructura del Proyecto
|--- gestion_tecnologicos.py  # Código principal
|--- datos/                   # Carpeta de persistencia
|--- README.md

## Video explicativo