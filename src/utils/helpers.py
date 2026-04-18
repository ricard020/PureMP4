def get_seconds(time_str):
    """Convierte HH:MM:SS.ms a segundos"""
    try:
        parts = time_str.split(':')
        if len(parts) == 3:
            h, m, s = map(float, parts)
            return h * 3600 + m * 60 + s
        return 0
    except:
        return 0

def format_time(seconds):
    """Formatea segundos a MM:SS"""
    if seconds < 0: seconds = 0
    m = int(seconds // 60)
    s = int(seconds % 60)
    return f"{m:02d}:{s:02d}"
