## 👨‍💻 Autores

Mateo Algañaraz 
Ignacio Rodríguez
COMISIÓN 3 

# 📦 Sistema de Gestión Tecnológica

Sistema de gestión de inventario para productos tecnológicos con almacenamiento jerárquico basado en directorios y archivos CSV.

## 📋 Descripción

Este sistema permite administrar un inventario de productos tecnológicos organizados de forma jerárquica mediante una estructura de directorios que refleja la taxonomía: **Categoría → Marca → Tipo**. Cada tipo de producto se almacena en su propio archivo CSV, facilitando la escalabilidad y organización de grandes catálogos.

## 🏗️ Estructura de Datos

### Jerarquía de Directorios

El sistema organiza los productos en una estructura de tres niveles:

```
datos/
├── Computadoras/
│   ├── Apple/
│   │   ├── Laptop.csv
│   │   └── Desktop.csv
│   └── Dell/
│       └── Laptop.csv
├── Teléfonos/
│   ├── Samsung/
│   │   └── Smartphone.csv
│   └── Apple/
│       └── Smartphone.csv
└── Accesorios/
    └── Logitech/
        ├── Mouse.csv
        └── Teclado.csv
```

**Niveles jerárquicos:**
1. **Categoría**: Tipo general del producto (ej: Computadoras, Teléfonos, Accesorios)
2. **Marca**: Fabricante del producto (ej: Apple, Samsung, Dell)
3. **Tipo**: Clasificación específica (ej: Laptop, Smartphone, Mouse)

### Formato de Archivos CSV

Cada archivo CSV contiene los siguientes campos:

| Campo   | Tipo    | Descripción                    | Validación          |
|---------|---------|--------------------------------|---------------------|
| nombre  | string  | Nombre del producto            | Obligatorio         |
| precio  | float   | Precio en unidad monetaria     | > 0                 |
| stock   | int     | Cantidad disponible            | ≥ 0                 |
| modelo  | string  | Modelo o código del producto   | Obligatorio         |

**Ejemplo de contenido CSV:**
```csv
nombre,precio,stock,modelo
MacBook Pro 14,2499.99,15,MBP14-2023
MacBook Air M2,1299.99,25,MBA-M2-2023
iMac 24,1499.99,8,iMac24-2023
```

## 🔍 Lógica de Almacenamiento y Filtrado

### Almacenamiento

1. **Creación Automática de Estructura**: Al dar de alta un producto, el sistema crea automáticamente los directorios necesarios si no existen.

2. **Archivos por Tipo**: Cada combinación de Categoría/Marca/Tipo genera un archivo CSV único, evitando archivos masivos y permitiendo acceso granular.

3. **Persistencia Atómica**: Las operaciones de escritura sobrescriben el archivo completo, garantizando consistencia de datos.

### Lectura Recursiva

La función `leer_recursivo()` implementa un algoritmo recursivo que:

1. **Explora la jerarquía**: Navega recursivamente desde el directorio raíz `datos/`
2. **Identifica archivos CSV**: Detecta archivos `.csv` en cualquier nivel
3. **Extrae metadatos**: Infiere la jerarquía (categoría, marca, tipo) desde la ruta del archivo
4. **Enriquece los datos**: Añade metadatos jerárquicos a cada producto leído
5. **Consolida resultados**: Retorna una lista unificada de todos los productos

**Ventaja**: Permite consultar todo el inventario sin conocer previamente la estructura de directorios.

### Filtrado

El sistema ofrece dos métodos de filtrado:

1. **Por Categoría**: Búsqueda case-insensitive sobre el campo `categoria`
2. **Por Rango de Precio**: Filtro numérico entre precio mínimo y máximo

Los filtros operan sobre la lista en memoria resultante de `leer_recursivo()`.

## 🚀 Instalación y Uso

### Requisitos

- Python 3.10 o superior (utiliza pattern matching con `match-case`)
- No requiere dependencias externas (solo biblioteca estándar)

### Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/tu-usuario/sistema-gestion-tecnologica.git
cd sistema-gestion-tecnologica
```

2. Ejecutar el sistema:
```bash
python main.py
```

El directorio `datos/` se creará automáticamente en la primera ejecución.

## 📖 Guía de Uso

### Menú Principal

```
==================================================
SISTEMA DE GESTIÓN TECNOLÓGICA
==================================================
1. Alta de nuevo producto
2. Mostrar todos los productos
3. Filtrar productos
4. Modificar producto
5. Eliminar producto
6. Estadísticas
7. Ordenar productos
8. Salir
==================================================
```

### 1. Alta de Producto

Registra un nuevo producto en el sistema:

```
Categoría: Computadoras
Marca: Apple
Tipo: Laptop
Nombre: MacBook Pro 16
Modelo: MBP16-2023
Precio: 2899.99
Stock: 10
```

El sistema creará automáticamente `datos/Computadoras/Apple/Laptop.csv` si no existe.

### 2. Mostrar Productos

Lista todos los productos del inventario con su ubicación jerárquica:

```
NOMBRE               PRECIO     STOCK  MODELO          UBICACIÓN
---------------------------------------------------------------------------
MacBook Pro 16       $2899.99   10     MBP16-2023      Computadoras / Apple / Laptop
```

### 3. Filtrar Productos

Permite filtrar por:
- **Categoría**: Filtra por categoría específica (ej: "Teléfonos")
- **Rango de precio**: Define precio mínimo y máximo

### 4. Modificar Producto

Actualiza el precio o stock de un producto existente:

```
Nombre exacto: MacBook Pro 16
Campo a modificar: stock
Nuevo valor: 15
```

### 5. Eliminar Producto

Elimina un producto del sistema por su nombre exacto.

### 6. Estadísticas

Muestra:
- Total de productos
- Precio promedio
- Cantidad de productos por categoría

### 7. Ordenar Productos

Ordena la visualización por:
- Nombre (alfabéticamente A-Z)
- Precio (menor a mayor)
- Stock (mayor a menor)

## 🔧 Funciones Principales

### `crear_estructura_directorios(categoria, marca, tipo)`
Crea la jerarquía de directorios y retorna la ruta del archivo CSV.

### `leer_csv_producto(ruta_archivo, categoria, marca, tipo)`
Lee un archivo CSV específico y retorna productos con metadatos jerárquicos.

### `leer_recursivo(ruta)`
**Función clave**: Recorre recursivamente toda la estructura de directorios y consolida todos los productos en una única lista.

### `guardar_producto_csv(ruta_archivo, productos)`
Persiste productos en un archivo CSV (solo campos base, sin metadatos).

### Operaciones CRUD
- `alta_producto()`: Crear
- `mostrar_productos()`: Leer
- `modificar_producto()`: Actualizar
- `eliminar_producto()`: Eliminar

## 📊 Validaciones

El sistema implementa las siguientes validaciones:

- ✅ Campos obligatorios: nombre, modelo, categoría, marca, tipo
- ✅ Precio debe ser mayor a 0
- ✅ Stock debe ser mayor o igual a 0
- ✅ Validación de tipos de datos (float para precio, int para stock)
- ✅ Manejo de errores en lectura/escritura de archivos
- ✅ Omisión de filas con datos inválidos en CSVs

## 🎯 Características Técnicas

- **Python 3.10+**: Utiliza pattern matching (`match-case`)
- **Type Hints**: Tipado estático para mejor legibilidad
- **Manejo de errores**: Try-except en operaciones de I/O
- **Codificación UTF-8**: Soporte completo para caracteres especiales
- **Búsqueda case-insensitive**: Filtros no sensibles a mayúsculas
- **Arquitectura modular**: Funciones separadas por responsabilidad

## 📁 Estructura del Proyecto

```
sistema-gestion-tecnologica/
├── main.py              # Archivo principal del sistema
├── README.md            # Este archivo
└── datos/               # Directorio de datos (generado automáticamente)
    └── [jerarquía de categorías/marcas/tipos]
```

## Video explicativo


**Nota**: El sistema utiliza archivos CSV para persistencia de datos. Para entornos de producción con alta concurrencia, considera migrar a una base de datos relacional.