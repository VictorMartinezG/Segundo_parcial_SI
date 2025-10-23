import tkinter as tk
from tkinter import messagebox, simpledialog
import os
import json

ARCHIVO = "arbol.json"

# ======================
# FUNCIONES BASE (MISMO CÓDIGO DE TU AKINATOR)
# ======================

def arbol_inicial():
    return {
        "¿Tu carta es terrestre?": {
            "sí": {
                "¿Tu carta ataca estructuras?": {
                    "sí": {
                        "¿Tu carta es un tanque?": {
                            "sí": "Gigante",
                            "no": "Montapuercos"
                        }
                    },
                    "no": {
                        "¿Es tropa cuerpo a cuerpo?": {
                            "sí": {
                                "¿Tiene escudo?": {
                                    "sí": "Guardias",
                                    "no": "Mini P.E.K.K.A"
                                }
                            },
                            "no": {
                                "¿Lanza proyectiles?": {
                                    "sí": "Mosquetera",
                                    "no": "Mago"
                                }
                            }
                        }
                    }
                }
            },
            "no": {
                "¿Tu carta vuela?": {
                    "sí": {
                        "¿Dispara desde lejos?": {
                            "sí": {
                                "¿Hace daño en área?": {
                                    "sí": "Bebé Dragón",
                                    "no": "Arqueras"
                                }
                            },
                            "no": {
                                "¿Es tropa individual?": {
                                    "sí": "Megaesbirro",
                                    "no": "Horda de Esbirros"
                                }
                            }
                        }
                    },
                    "no": {
                        "¿Tu carta es un hechizo?": {
                            "sí": {
                                "¿Hace daño directo?": {
                                    "sí": {
                                        "¿Afecta en área?": {
                                            "sí": "Bola de Fuego",
                                            "no": "Rayo"
                                        }
                                    },
                                    "no": "Descarga"
                                }
                            },
                            "no": {
                                "¿Es una estructura defensiva?": {
                                    "sí": {
                                        "¿Ataca aire y tierra?": {
                                            "sí": "Torre Infernal",
                                            "no": "Cañón"
                                        }
                                    },
                                    "no": {
                                        "¿Tu carta congela enemigos?": {
                                            "sí": "Mago de Hielo",
                                            "no": {
                                                "¿Tu carta hace daño eléctrico a varios enemigos?": {
                                                    "sí": "Dragón Eléctrico",
                                                    "no": {
                                                        "¿Tu carta hace carga?": {
                                                            "sí": "Príncipe",
                                                            "no": {
                                                                "¿Tu carta embiste rápidamente?": {
                                                                    "sí": "Bandida",
                                                                    "no": {
                                                                        "¿Tu carta puede moverse rápido mientras ataca?": {
                                                                            "sí": "Caballero Dorado",
                                                                            "no": {
                                                                                "¿Tu carta electrocuta enemigos cercanos?": {
                                                                                    "sí": "Mago Eléctrico",
                                                                                    "no": {
                                                                                        "¿Tu carta cura a otras tropas?": {
                                                                                            "sí": "Sanadora",
                                                                                            "no": {
                                                                                                "¿Tu carta genera esqueletos?": {
                                                                                                    "sí": "Bruja",
                                                                                                    "no": "Recolector de Elixir"
                                                                                                }
                                                                                            }
                                                                                        }
                                                                                    }
                                                                                }
                                                                            }
                                                                        }
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }

def cargar_arbol():
    if os.path.exists(ARCHIVO):
        try:
            with open(ARCHIVO, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return arbol_inicial()

def guardar_arbol(arbol):
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        json.dump(arbol, f, ensure_ascii=False, indent=4)

# ======================
# INTERFAZ GRÁFICA
# ======================

class AkinatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Akinator Clash Royale")
        self.root.geometry("800x800")
        self.root.configure(bg="#242424")

        self.arbol = cargar_arbol()
        self.pila = []  # para regresar al nodo anterior
        self.nodo_actual = self.arbol

        # Pantalla de inicio
        self.frame_inicio = tk.Frame(self.root, bg="#242424")
        self.frame_inicio.pack(expand=True, fill="both")

        self.titulo = tk.Label(self.frame_inicio, text="Akinator Clash Royale",
                               font=("Arial", 26, "bold"), fg="gold", bg="#242424")
        self.titulo.pack(pady=20)

        try:
            # Asegúrate de tener una imagen llamada carta.png en la misma carpeta
            self.img = tk.PhotoImage(file="carta.png")
            self.img_label = tk.Label(self.frame_inicio, image=self.img, bg="#242424")
            self.img_label.pack(pady=10)
        except:
            tk.Label(self.frame_inicio, text="[Imagen no encontrada]", fg="white", bg="#242424").pack(pady=20)

        self.boton_jugar = tk.Button(self.frame_inicio, text="Jugar", font=("Arial", 18, "bold"),
                                     bg="gold", command=self.iniciar_juego)
        self.boton_jugar.pack(pady=40)

        # Frame del juego (oculto al inicio)
        self.frame_juego = tk.Frame(self.root, bg="#242424")

        self.pregunta_label = tk.Label(self.frame_juego, text="", font=("Arial", 18), fg="white", bg="#242424", wraplength=500)
        self.pregunta_label.pack(pady=40)

        botones_frame = tk.Frame(self.frame_juego, bg="#242424")
        botones_frame.pack(pady=30)

        self.boton_si = tk.Button(botones_frame, text="Sí", font=("Arial", 16, "bold"),
                                  bg="green", fg="white", width=10, command=lambda: self.responder("sí"))
        self.boton_si.grid(row=0, column=0, padx=15)

        self.boton_no = tk.Button(botones_frame, text="No", font=("Arial", 16, "bold"),
                                  bg="red", fg="white", width=10, command=lambda: self.responder("no"))
        self.boton_no.grid(row=0, column=1, padx=15)

    def iniciar_juego(self):
        """Cambia a la pantalla de juego y muestra la primera pregunta"""
        self.frame_inicio.pack_forget()
        self.frame_juego.pack(expand=True, fill="both")
        self.mostrar_pregunta(self.nodo_actual)

    def mostrar_pregunta(self, nodo):
        """Muestra la pregunta o el intento de carta"""
        if isinstance(nodo, str):
            self.pregunta_label.config(text=f"¿Tu carta es {nodo}?")
        elif isinstance(nodo, dict):
            pregunta = next(iter(nodo))
            self.pregunta_label.config(text=pregunta)

    def responder(self, respuesta):
        """Gestiona las respuestas 'sí' o 'no'"""
        if isinstance(self.nodo_actual, str):
            if respuesta == "sí":
                messagebox.showinfo("Akinator", "¡Lo adiviné!")
                guardar_arbol(self.arbol)
                self.root.destroy()
            else:
                self.aprender()
            return

        # Si es pregunta
        pregunta = next(iter(self.nodo_actual))
        siguiente = self.nodo_actual[pregunta].get(respuesta)

        if siguiente is None:
            messagebox.showinfo("Error", "Esta rama no está definida.")
            return

        self.pila.append(self.nodo_actual)
        self.nodo_actual = siguiente
        self.mostrar_pregunta(self.nodo_actual)

    def aprender(self):
        """Cuando no adivina, aprende una nueva carta"""
        carta_nueva = tk.simpledialog.askstring("Aprender", "¿Cuál era tu carta?")
        if not carta_nueva:
            return
        pregunta_nueva = tk.simpledialog.askstring("Aprender", f"Escribe una pregunta que distinga a {carta_nueva}:")
        if not pregunta_nueva:
            return
        respuesta_correcta = messagebox.askyesno("Aprender", f"Si la carta fuera {carta_nueva}, ¿la respuesta sería 'sí'?")

        if respuesta_correcta:
            nuevo = {pregunta_nueva: {"sí": carta_nueva, "no": self.nodo_actual}}
        else:
            nuevo = {pregunta_nueva: {"sí": self.nodo_actual, "no": carta_nueva}}

        if self.pila:
            padre = self.pila.pop()
            clave = next(iter(padre))
            for r in ("sí", "no"):
                if padre[clave][r] == self.nodo_actual:
                    padre[clave][r] = nuevo
                    break
        else:
            self.arbol = nuevo

        guardar_arbol(self.arbol)
        messagebox.showinfo("Akinator", "¡He aprendido una nueva carta!")
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = AkinatorGUI(root)
    root.mainloop()
