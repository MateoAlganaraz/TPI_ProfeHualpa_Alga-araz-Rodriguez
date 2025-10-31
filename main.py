import os
from menu import menu_principal

if __name__ == "__main__":
    os.makedirs("datos", exist_ok=True)
    menu_principal()