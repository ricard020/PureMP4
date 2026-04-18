from tkinter import ttk

def setup_app_styles(style: ttk.Style):
    """Configuration centralizada de estilos de la aplicación"""
    style.theme_use('clam')
    
    # Paleta de colores Modern: #0F172A (bg) + #3B82F6 (primary)
    style.configure("TFrame", background="#0F172A")
    style.configure("TLabel", background="#0F172A", foreground="#E2E8F0", font=("Segoe UI", 11))
    
    style.configure("TEntry", 
                    fieldbackground="#1E293B",  # Lighter slate for input fields
                    foreground="#F1F5F9", 
                    insertcolor="#3B82F6",  # Blue cursor
                    borderwidth=1,
                    relief="flat")
                            
    style.configure("Accent.TButton", 
                    font=("Segoe UI", 11, "bold"), 
                    background="#3B82F6",  # Primary blue
                    foreground="white", 
                    borderwidth=0, 
                    focuscolor="none")
    style.map("Accent.TButton", 
                background=[('active', '#2563EB')],  # Darker blue on hover
                foreground=[('active', 'white')])

    style.configure("Secondary.TButton", 
                    font=("Segoe UI", 10), 
                    background="#3B82F6",  # Same blue for consistency
                    foreground="white", 
                    borderwidth=0, 
                    focuscolor="none")
    style.map("Secondary.TButton", 
                background=[('active', '#2563EB')])
    
    style.configure("Header.TLabel", font=("Segoe UI", 24, "bold"), foreground="#60A5FA")  # Light blue
    style.configure("Status.TLabel", font=("Segoe UI", 10, "italic"), foreground="#94A3B8")  # Slate gray
    style.configure("Timer.TLabel", font=("Segoe UI", 13, "bold"), foreground="#06B6D4")  # Cyan accent

    # File Selection Block
    style.configure("TLabelframe", background="#0F172A", foreground="#3B82F6")
    style.configure("TLabelframe.Label", background="#0F172A", foreground="#3B82F6", font=("Segoe UI", 10, "bold"))
    
    # Progress bar styling
    style.configure("Horizontal.TProgressbar", troughcolor="#1E293B", background="#3B82F6", borderwidth=0, lightcolor="#3B82F6", darkcolor="#3B82F6")
