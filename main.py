import sys
import os
import tkinter as tk

# Asegurar que el directorio src está en el path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from src.gui.main_window import MainWindow

def main():
    # Establecer AppID para que Windows muestre el icono correcto en la barra de tareas
    try:
        from ctypes import windll
        myappid = 'puremp4.converter.v1'
        windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except Exception:
        pass

    root = tk.Tk()
    
    # Establecer el icono de la ventana principal
    icon_path = os.path.join(current_dir, "assets", "logo", "logo-ico.ico")
    if os.path.exists(icon_path):
        root.iconbitmap(icon_path)
    
    app = MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()
