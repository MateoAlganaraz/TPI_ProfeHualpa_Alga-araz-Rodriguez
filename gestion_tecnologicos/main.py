import os
import sys

if __name__ == "__main__":
    # Obtiene la ruta del directorio padre (la carpeta que contiene 'gestion_tecnologicos')
    proyecto_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if proyecto_dir not in sys.path:
        sys.path.insert(0, proyecto_dir)

from gestion_tecnologicos.menu import menu_principal

if __name__ == "__main__":
    os.makedirs("datos", exist_ok=True)
    menu_principal()