import tkinter as tk
from tkinter import scrolledtext, messagebox
import subprocess
import threading

def start_program():
    global process
    if process is None or process.poll() is not None:
        process = subprocess.Popen(
            ['python', 'bot.py'],  # Замените на путь к вашей второй программе
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1
        )
        threading.Thread(target=read_output, daemon=True).start()
        messagebox.showinfo("Статус", "Программа успешно запущена!")
        start_button.pack_forget()
        stop_button.pack(side=tk.LEFT, padx=5)

def stop_program():
    global process
    if process and process.poll() is None:
        process.terminate()
        process.wait()
        log_output.insert(tk.END, "\nПрограмма остановлена.\n")
        log_output.see(tk.END)
        stop_button.pack_forget()
        start_button.pack(side=tk.LEFT, padx=5)

def read_output():
    global process
    for line in iter(process.stdout.readline, ''):
        log_output.insert(tk.END, line)
        log_output.see(tk.END)
    process.stdout.close()

# Глобальная переменная для процесса
process = None

# Создание графического интерфейса
root = tk.Tk()
root.title("Запуск Python-программы")

frame = tk.Frame(root)
frame.pack(pady=10)

start_button = tk.Button(frame, text="Запустить", command=start_program)
start_button.pack(side=tk.LEFT, padx=5)

stop_button = tk.Button(frame, text="Остановить", command=stop_program)
stop_button.pack_forget()

log_output = scrolledtext.ScrolledText(root, width=80, height=20)
log_output.pack(pady=10)

root.mainloop()