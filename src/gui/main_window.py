import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import ctypes
from ..logic.converter import FFmpegConverter
from ..utils.helpers import format_time
from .styles import setup_app_styles

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.converter = FFmpegConverter()
        
        self.setup_window()
        self.setup_styles()
        self.init_variables()
        self.create_widgets()
        
    def setup_window(self):
        self.root.title("PureMP4 | Simplicidad y formato sin complicaciones")
        self.root.geometry("650x500")
        self.root.configure(bg="#0F172A")
        
        # Centrar ventana
        self.center_window()
    
    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def setup_styles(self):
        self.style = ttk.Style()
        setup_app_styles(self.style)

    def init_variables(self):
        self.input_file_path = tk.StringVar()
        self.status_var = tk.StringVar(value="Esperando para iniciar...")
        self.percentage_var = tk.StringVar(value="0%")
        self.timer_var = tk.StringVar(value="00:00")

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="30")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Header
        ttk.Label(main_frame, text="PureMP4", style="Header.TLabel").pack(pady=(0, 15))

        # Description
        ttk.Label(main_frame, 
                  text="Convierte tus archivos MP4 a un formato totalmente compatible con WhatsApp (H.264/AAC).", 
                  wraplength=550, justify="center", foreground="#CBD5E1", font=("Segoe UI", 11)).pack(pady=(0, 35))

        # File Selection Block
        file_frame = ttk.LabelFrame(main_frame, text=" Archivo de Origen ", padding="20", style="TLabelframe")
        file_frame.pack(fill=tk.X, pady=(0, 20))

        entry_container = ttk.Frame(file_frame)
        entry_container.pack(fill=tk.X)

        self.file_entry = ttk.Entry(entry_container, textvariable=self.input_file_path, font=("Segoe UI", 12))
        self.file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 15), ipady=4)

        ttk.Button(entry_container, text="Buscar Archivo", style="Secondary.TButton", 
                   command=self.select_file, cursor="hand2").pack(side=tk.RIGHT, ipady=2)

        # Progress Section
        progress_frame = ttk.Frame(main_frame)
        progress_frame.pack(fill=tk.X, pady=10)

        stats_frame = ttk.Frame(progress_frame)
        stats_frame.pack(fill=tk.X, pady=(0, 8))
        
        ttk.Label(stats_frame, textvariable=self.percentage_var, style="Timer.TLabel").pack(side=tk.LEFT)
        ttk.Label(stats_frame, textvariable=self.timer_var, font=("Segoe UI", 12), foreground="#CBD5E1").pack(side=tk.RIGHT)
        
        self.progress_bar = ttk.Progressbar(progress_frame, mode='determinate', length=400, style="Horizontal.TProgressbar")
        self.progress_bar.pack(fill=tk.X, pady=0)
        
        ttk.Label(progress_frame, textvariable=self.status_var, style="Status.TLabel").pack(anchor="w", pady=(8,0))

        # Convert Button
        ttk.Frame(main_frame).pack(fill=tk.Y, expand=True) # Spacer

        self.convert_btn = ttk.Button(main_frame, text="INICIAR CONVERSIÓN", style="Accent.TButton", 
                                      command=self.start_conversion, cursor="hand2")
        self.convert_btn.pack(fill=tk.X, pady=10, ipady=12)

    def select_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("MP4 files", "*.mp4"), ("All files", "*.*")]
        )
        if file_path:
            self.input_file_path.set(file_path)
            self.reset_ui()

    def reset_ui(self):
        self.status_var.set("Listo para convertir.")
        self.percentage_var.set("0%")
        self.timer_var.set("00:00")
        self.progress_bar['value'] = 0

    def start_conversion(self):
        input_path = self.input_file_path.get()
        if not input_path:
            messagebox.showwarning("Advertencia", "Por favor selecciona un archivo primero.")
            return
        
        if not os.path.exists(input_path):
            messagebox.showerror("Error", "Archivo de entrada no encontrado.")
            return

        directory = os.path.dirname(input_path)
        filename = os.path.basename(input_path)
        output_path = os.path.join(directory, f"converted_{filename}")

        self.lock_ui(True)
        self.status_var.set("Inicializando...")
        
        # Start conversion using logic class
        self.converter.start_conversion(
            input_path, 
            output_path, 
            self.on_progress_update, 
            self.on_conversion_complete
        )

    def on_progress_update(self, percentage, remaining_time):
        # Update UI in main thread
        self.root.after(0, lambda: self._update_ui_progress(percentage, remaining_time))

    def _update_ui_progress(self, percentage, remaining_time):
        self.progress_bar['value'] = percentage
        self.percentage_var.set(f"{int(percentage)}%")
        self.timer_var.set(f"Restante: {format_time(remaining_time)}")
        self.status_var.set("Procesando datos del video...")

    def on_conversion_complete(self, success, message):
        # Handle completion in main thread
        self.root.after(0, lambda: self._handle_complete(success, message))

    def _handle_complete(self, success, message):
        self.lock_ui(False)
        if success:
            self.progress_bar['value'] = 100
            self.percentage_var.set("100%")
            self.timer_var.set("Completado")
            self.status_var.set("Conversión completada exitosamente.")
            messagebox.showinfo("Éxito", f"Archivo guardado:\n{message}")
        else:
            self.reset_ui()
            self.status_var.set("Ocurrió un error.")
            messagebox.showerror("Error", message)

    def lock_ui(self, lock):
        state = tk.DISABLED if lock else tk.NORMAL
        self.convert_btn.config(state=state)
