from .filesystem import leer_recursivo
from .producto import alta_producto, modificar_producto, eliminar_producto
from .consultas import mostrar_productos, filtrar_productos, estadisticas, ordenar_productos

def menu_principal():
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