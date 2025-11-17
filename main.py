import os
import tkinter as tk
from tkinter import scrolledtext
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
clave = os.getenv("API_KEY")

genai.configure(api_key=clave)

modelo = genai.GenerativeModel('gemini-2.0-flash')

try:
    archivo = open("datos.txt", "r", encoding="utf-8")
    datos_panaderia = archivo.read()
    archivo.close()
except:
    datos_panaderia = "No se encontró el archivo datos.txt. Crea el archivo con los precios."

# --- FUNCIÓN PREGUNTAR ---
def preguntar():
    pregunta = entrada.get()
    if pregunta == "":
        return

    # Mostrar pregunta del usuario
    chat.config(state=tk.NORMAL)
    chat.insert(tk.END, "Tú: " + pregunta + "\n", "usuario")
    entrada.delete(0, tk.END)

    # Crear prompt y enviar a Google
    prompt = datos_panaderia + "\n\nCliente: " + pregunta

    try:
        respuesta = modelo.generate_content(prompt)
        texto = respuesta.text
    except Exception as e:
        texto = f"Error de conexión: {str(e)}"
        print(texto) # Imprime el error en la consola por si acaso

    # Mostrar respuesta de la IA
    chat.insert(tk.END, "Panadero: " + texto + "\n\n", "bot")
    chat.config(state=tk.DISABLED)
    chat.yview(tk.END) # Auto-scroll hacia abajo

# --- VENTANA GRAFICA ---
ventana = tk.Tk()
ventana.title("Panadería IA")
ventana.geometry("450x550")

# Chat con colores
chat = scrolledtext.ScrolledText(ventana, width=50, height=20, font=("Arial", 10))
chat.tag_config("usuario", foreground="blue")
chat.tag_config("bot", foreground="green")
chat.pack(padx=10, pady=10)
chat.config(state=tk.DISABLED)

entrada = tk.Entry(ventana, width=35, font=("Arial", 11))
entrada.pack(padx=10, pady=5)

# Permitir enviar con la tecla ENTER
entrada.bind("<Return>", lambda event: preguntar())

boton = tk.Button(ventana, text="Enviar Pregunta", command=preguntar, bg="#dddddd")
boton.pack(padx=10, pady=10)

ventana.mainloop()