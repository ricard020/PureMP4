import subprocess
import threading
import sys
import os
import re
import time
from ..utils.helpers import get_seconds

class FFmpegConverter:
    def __init__(self):
        self.process = None
        self.duration = 0

    def start_conversion(self, input_path, output_path, on_progress, on_complete):
        """
        Inicia la conversión en un hilo separado.
        
        Args:
            input_path (str): Ruta del archivo de entrada using absolute path.
            output_path (str): Ruta del archivo de salida using absolute path.
            on_progress (callable): Callback(percentage, remaining_time).
            on_complete (callable): Callback(success, message).
        """
        thread = threading.Thread(target=self._run_ffmpeg, args=(input_path, output_path, on_progress, on_complete))
        thread.daemon = True
        thread.start()

    def _run_ffmpeg(self, input_path, output_path, on_progress, on_complete):
        command = [
            'ffmpeg', '-y',
            '-i', input_path,
            '-c:v', 'libx264',
            '-preset', 'medium',
            '-crf', '23',
            '-c:a', 'aac',
            '-b:a', '128k',
            '-pix_fmt', 'yuv420p',
            '-movflags', '+faststart',
            output_path
        ]

        try:
            creation_flags = 0
            if sys.platform == "win32":
                creation_flags = subprocess.CREATE_NO_WINDOW

            self.process = subprocess.Popen(
                command, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                universal_newlines=True,
                creationflags=creation_flags
            )

            start_time = time.time()
            self.duration = 0

            # FFmpeg usa stderr para mostrar el progreso
            # Leemos línea por línea
            while True:
                line = self.process.stderr.readline()
                if not line and self.process.poll() is not None:
                    break
                
                if line:
                    # Extraer Duración total
                    if 'Duration' in line and self.duration == 0:
                        match = re.search(r"Duration: (\d{2}):(\d{2}):(\d{2}\.\d{2})", line)
                        if match:
                            self.duration = get_seconds(f"{match.group(1)}:{match.group(2)}:{match.group(3)}")
                    
                    # Extraer Tiempo actual
                    if 'time=' in line and self.duration > 0:
                        match = re.search(r"time=(\d{2}):(\d{2}):(\d{2}\.\d{2})", line)
                        if match:
                            current_time = get_seconds(f"{match.group(1)}:{match.group(2)}:{match.group(3)}")
                            
                            if self.duration > 0:
                                percentage = (current_time / self.duration) * 100
                            else:
                                percentage = 0
                            
                            elapsed = time.time() - start_time
                            remaining_time = 0
                            
                            if percentage > 0:
                                estimated_total_time = elapsed * (100 / percentage)
                                remaining_time = estimated_total_time - elapsed
                            
                            on_progress(percentage, remaining_time)

            return_code = self.process.wait()

            if return_code == 0:
                on_complete(True, output_path)
            else:
                on_complete(False, "FFmpeg finalizó con error.")

        except FileNotFoundError:
            on_complete(False, "FFmpeg no encontrado. Por favor instala FFmpeg y agrégalo al PATH.")
        except Exception as e:
            on_complete(False, str(e))
