# akinator_clash.py
import json                     # para leer/escribir el JSON
import os                       # para comprobar existencia de archivos

ARCHIVO = "arbol.json"          # nombre del archivo que guardará el árbol

# -----------------------------------------------------------
# ÁRBOL INICIAL (formato consistente):
# - Un nodo pregunta es: { "Pregunta?": { "sí": <subnodo>, "no": <subnodo> } }
# - Una hoja/carta es una cadena: "Nombre Carta"
# -----------------------------------------------------------

def arbol_inicial():
    """Devuelve el árbol base (24 cartas) como estructura de Python."""
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
                                    # Nodo para preguntas especiales que distinguen las legendarias restantes
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

# -----------------------------------------------------------
# Cargar / Guardar
# -----------------------------------------------------------

def cargar_arbol():
    """Carga el árbol desde ARCHIVO. Si no existe o está dañado, devuelve el árbol inicial."""
    if os.path.exists(ARCHIVO):                               # si el archivo existe
        try:
            with open(ARCHIVO, "r", encoding="utf-8") as f:   # abrir en modo lectura
                return json.load(f)                          # y cargar JSON a estructura Python
        except (json.JSONDecodeError, OSError):
            print(" Archivo JSON dañado o ilegible. Se cargará el árbol inicial.")
    # si no existe o está dañado, devolvemos el árbol base
    return arbol_inicial()

def guardar_arbol(arbol):
    """Guarda la estructura del árbol en ARCHIVO (JSON, legible)."""
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        json.dump(arbol, f, ensure_ascii=False, indent=4)

# -----------------------------------------------------------
# Utilidad para leer respuestas válidas
# -----------------------------------------------------------

def leer_respuesta(prompt):
    """Pide repetidamente una respuesta hasta obtener 'sí' o 'no'. Devuelve 'sí' o 'no'."""
    while True:
        r = input(prompt + " (sí/no): ").strip().lower()   # leer entrada del usuario
        if r in ("sí", "si"):                              # aceptar 'sí' o 'si'
            return "sí"
        if r == "no":
            return "no"
        print("Respuesta no válida. Escribe 'sí' o 'no'.")

# -----------------------------------------------------------
# Lógica recursiva principal
# -----------------------------------------------------------

def recorrer_nodo(nodo):
    """
    Recorre un nodo (que puede ser cadena = carta, o dict = pregunta).
    Devuelve el nodo actualizado (importante para que el aprendizaje se propague).
    """
    # caso hoja: nodo es una carta (string)
    if isinstance(nodo, str):
        # preguntar por la carta
        respuesta = leer_respuesta(f"¿Tu carta es {nodo}?")
        if respuesta == "sí":
            print("¡Lo adiviné!")
            return nodo                                  # la hoja queda igual
        # si no acierta, aprendemos: pedimos la carta correcta y una pregunta
        nueva_carta = input("No lo acerté. ¿Cuál era tu carta? ").strip()
        # pedimos la pregunta que diferencia la nueva carta de la suposición 'nodo'
        nueva_pregunta = input(f"Escribe una pregunta que distinga a {nueva_carta} de {nodo}: ").strip()
        # pedimos cuál sería la respuesta correcta para la nueva carta
        respuesta_correcta = leer_respuesta(f"Si la carta fuera {nueva_carta}, ¿la respuesta a tu pregunta sería?")
        # construir el nuevo subárbol según la respuesta correcta
        if respuesta_correcta == "sí":
            return { nueva_pregunta: {"sí": nueva_carta, "no": nodo} }
        else:
            return { nueva_pregunta: {"sí": nodo, "no": nueva_carta} }

    # caso pregunta: nodo es un diccionario con una sola clave: la pregunta
    if isinstance(nodo, dict):
        # extraer la pregunta (primera clave)
        pregunta = next(iter(nodo))
        # obtener el mapa de respuestas del nodo actual
        mapa = nodo[pregunta]
        # leer respuesta del usuario
        respuesta = leer_respuesta(pregunta)
        # si la clave de respuesta existe, continuar, si no, tratar como desconocido
        siguiente = mapa.get(respuesta)
        if siguiente is None:
            # Si para alguna razón la rama faltara, preguntar al usuario qué poner ahí:
            print("No hay una rama definida para esa respuesta. Vamos a crearla.")
            # pedimos si la rama debe ser una carta o pregunta: simplificamos pidiendo carta
            nueva_carta = input("¿Qué carta debería ir en esta rama? Escribe el nombre: ").strip()
            nodo[pregunta][respuesta] = nueva_carta
            return nodo
        # recorrer recursivamente la rama seleccionada
        nodo[pregunta][respuesta] = recorrer_nodo(siguiente)
        return nodo

    # en caso improbable de estructura diferente, devolvemos sin cambios
    return nodo

# -----------------------------------------------------------
# Función principal del juego
# -----------------------------------------------------------

def jugar():
    """Ejecuta una partida completa: recorre el árbol, aprende si falla y guarda al final."""
    print("Akinator Clash Royale - piensa en una carta y responde con 'sí' o 'no'.")
    arbol = cargar_arbol()                 # cargar (o crear) árbol
    arbol = recorrer_nodo(arbol)          # jugar y obtener árbol actualizado
    guardar_arbol(arbol)                  # guardar aprendizaje
    print("Progreso guardado en", ARCHIVO)

# -----------------------------------------------------------
# Ejecutable
# -----------------------------------------------------------

if __name__ == "__main__":
    jugar()
