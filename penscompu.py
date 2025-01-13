import pygame
import random

# --- Funciones del Sudoku ---

def crear_sudoku_vacio():
    """Crea una cuadrícula de Sudoku vacía."""
    return [[0 for _ in range(9)] for _ in range(9)]

def es_valido(sudoku, fila, columna, caracter):
    """Verifica si es válido colocar un caracter en una celda específica."""
    # Comprobar si el caracter ya existe en la fila
    if caracter in sudoku[fila]:
        return False
    # Comprobar si el caracter ya existe en la columna
    if caracter in [sudoku[i][columna] for i in range(9)]:
        return False
    # Comprobar si el caracter ya existe en la región 3x3
    fila_region = (fila // 3) * 3
    columna_region = (columna // 3) * 3
    for i in range(fila_region, fila_region + 3):
        for j in range(columna_region, columna_region + 3):
            if sudoku[i][j] == caracter:
                return False
    return True

def rellenar_sudoku(sudoku, caracteres):
    """Rellena el Sudoku usando un algoritmo de backtracking."""
    for fila in range(9):
        for columna in range(9):
            if sudoku[fila][columna] == 0:
                caracteres_posibles = caracteres.copy()
                random.shuffle(caracteres_posibles)
                for caracter in caracteres_posibles:
                    if es_valido(sudoku, fila, columna, caracter):
                        sudoku[fila][columna] = caracter
                        if rellenar_sudoku(sudoku, caracteres):
                            return True
                        sudoku[fila][columna] = 0
                return False
    return True

def generar_sudoku(tipo_sudoku):
    """Genera un Sudoku completo."""
    if tipo_sudoku == "numeros":
        caracteres = list(range(1, 10))
    elif tipo_sudoku == "letras":
        caracteres = list("ABCDEFGHI")
    else:
        return sudoku

    sudoku = crear_sudoku_vacio()
    rellenar_sudoku(sudoku, caracteres)
    return sudoku

def eliminar_valores(sudoku, dificultad):
    """Elimina valores del Sudoku para crear el juego."""
    if dificultad == 1:
        casillas_a_eliminar = 20  # Fácil
    elif dificultad == 2:
        casillas_a_eliminar = 35  # Medio
    elif dificultad == 3:
        casillas_a_eliminar = 50  # Difícil
    else:
        return sudoku

    casillas_eliminadas = 0
    while casillas_eliminadas < casillas_a_eliminar:
        fila = random.randint(0, 8)
        columna = random.randint(0, 8)
        if sudoku[fila][columna] != 0:
            sudoku[fila][columna] = 0
            casillas_eliminadas += 1

def validar_sudoku(sudoku_original, sudoku_usuario):
    """Valida si el Sudoku completado por el usuario es correcto."""
    for fila in range(9):
        for columna in range(9):
            if sudoku_usuario[fila][columna] != sudoku_original[fila][columna]:
                return False
    return True

# --- Funciones de la interfaz gráfica ---

def dibujar_tablero(pantalla, sudoku, tipo_sudoku, celda_seleccionada=None, casillas_iniciales=None):
    """Dibuja el tablero de Sudoku en la pantalla."""
    pantalla.fill((255, 255, 255))  # Fondo blanco
    for i in range(10):
        grosor = 4 if i % 3 == 0 else 1
        pygame.draw.line(pantalla, (0, 0, 0), (50 + i * 50, 50), (50 + i * 50, 500), grosor)
        pygame.draw.line(pantalla, (0, 0, 0), (50, 50 + i * 50), (500, 50 + i * 50), grosor)

    fuente = pygame.font.Font(None, 40)
    for fila in range(9):
        for columna in range(9):
            valor = sudoku[fila][columna]
            if valor != 0:  # Solo dibujar valores no vacíos
                if tipo_sudoku == "numeros":
                    texto = fuente.render(str(valor), True, (0, 0, 0))
                else:
                    texto = fuente.render(valor, True, (0, 0, 0))
                x = 50 + columna * 50 + 15
                y = 50 + fila * 50 + 10
                if casillas_iniciales and (fila, columna) in casillas_iniciales:  # Cambiar color de las casillas iniciales
                    texto = fuente.render(str(valor), True, (0, 0, 255))  # Azul
                pantalla.blit(texto, (x, y))

    if celda_seleccionada:
        fila, columna = celda_seleccionada
        pygame.draw.rect(pantalla, (255, 0, 0), (50 + columna * 50, 50 + fila * 50, 50, 50), 3)

def obtener_celda_click(pos):
    """Obtiene la fila y columna de la celda clickeada."""
    x, y = pos
    if 50 <= x <= 500 and 50 <= y <= 500:
        fila = (y - 50) // 50
        columna = (x - 50) // 50
        return fila, columna
    return None

def mostrar_mensaje(pantalla, mensaje):
    """Muestra un mensaje en la pantalla, manejando saltos de línea."""
    fuente = pygame.font.Font(None, 40)
    lineas = mensaje.splitlines()  # Dividir el mensaje en líneas
    altura_linea = fuente.get_linesize()
    y = 550 - (len(lineas) * altura_linea) / 2  # Centrar verticalmente

    for linea in lineas:
        texto = fuente.render(linea, True, (0, 0, 0))
        rect_texto = texto.get_rect(center=(275, y))
        pantalla.blit(texto, rect_texto)
        y += altura_linea  # Mover a la siguiente línea

def obtener_tipo_sudoku(pantalla):
    """Pregunta al usuario el tipo de Sudoku y lo devuelve."""
    fuente = pygame.font.Font(None, 30)
    opciones = ["numeros", "letras"]
    seleccion = 0
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    seleccion = (seleccion - 1) % 2
                elif evento.key == pygame.K_DOWN:
                    seleccion = (seleccion + 1) % 2
                elif evento.key == pygame.K_RETURN:
                    return opciones[seleccion]

        pantalla.fill((255, 255, 255))
        texto_pregunta = fuente.render("¿Qué tipo de Sudoku quieres?", True, (0, 0, 0))
        rect_pregunta = texto_pregunta.get_rect(center=(275, 200))
        pantalla.blit(texto_pregunta, rect_pregunta)

        for i, opcion in enumerate(opciones):
            color = (255, 0, 0) if i == seleccion else (0, 0, 0)
            texto_opcion = fuente.render(opcion, True, color)
            rect_opcion = texto_opcion.get_rect(center=(275, 300 + i * 50))
            pantalla.blit(texto_opcion, rect_opcion)

        pygame.display.flip()

def obtener_dificultad(pantalla):
    """Pregunta al usuario la dificultad del Sudoku y la devuelve."""
    fuente = pygame.font.Font(None, 30)
    opciones = ["Fácil", "Medio", "Difícil"]
    seleccion = 0
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    seleccion = (seleccion - 1) % 3
                elif evento.key == pygame.K_DOWN:
                    seleccion = (seleccion + 1) % 3
                elif evento.key == pygame.K_RETURN:
                    return seleccion + 1

        pantalla.fill((255, 255, 255))
        texto_pregunta = fuente.render("Selecciona la dificultad:", True, (0, 0, 0))
        rect_pregunta = texto_pregunta.get_rect(center=(275, 200))
        pantalla.blit(texto_pregunta, rect_pregunta)

        for i, opcion in enumerate(opciones):
            color = (255, 0, 0) if i == seleccion else (0, 0, 0)
            texto_opcion = fuente.render(opcion, True, color)
            rect_opcion = texto_opcion.get_rect(center=(275, 300 + i * 50))
            pantalla.blit(texto_opcion, rect_opcion)

        pygame.display.flip()

# --- Bloque principal ---

if __name__ == "__main__":
    pygame.init()
    pantalla = pygame.display.set_mode((550, 600))
    pygame.display.set_caption("Sudoku")

    tipo_sudoku = obtener_tipo_sudoku(pantalla)
    dificultad = obtener_dificultad(pantalla)

    sudoku_original = generar_sudoku(tipo_sudoku)
    sudoku_usuario = [fila[:] for fila in sudoku_original]  # Copiar el Sudoku original
    eliminar_valores(sudoku_usuario, dificultad)

    casillas_iniciales = set()  # Conjunto para almacenar las casillas iniciales
    for fila in range(9):
        for columna in range(9):
            if sudoku_usuario[fila][columna] != 0:
                casillas_iniciales.add((fila, columna))

    celda_seleccionada = None
    juego_terminado = False

    # --- Botón Terminado ---
    color_boton = (0, 255, 0)  # Verde
    boton_terminado = pygame.Rect(200, 520, 150, 40)

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:

                celda_seleccionada = obtener_celda_click(evento.pos)
                if boton_terminado.collidepoint(evento.pos):
                    juego_terminado = True
                    
            if evento.type == pygame.KEYDOWN and celda_seleccionada:
                fila, columna = celda_seleccionada
                if evento.key == pygame.K_BACKSPACE:
                    if (fila, columna) not in casillas_iniciales:  # Solo permitir borrar si no es casilla inicial
                        sudoku_usuario[fila][columna] = 0
                elif evento.unicode.isdigit() or evento.unicode.isalpha():
                    caracter = int(evento.unicode) if tipo_sudoku == "numeros" else evento.unicode.upper()
                    if 1 <= caracter <= 9 and (fila, columna) not in casillas_iniciales:  # Validar entrada y permitir solo en casillas no iniciales
                        sudoku_usuario[fila][columna] = caracter
                        if validar_sudoku(sudoku_original, sudoku_usuario):
                            juego_terminado = True

        dibujar_tablero(pantalla, sudoku_usuario , tipo_sudoku, celda_seleccionada, casillas_iniciales) # Pasar casillas_iniciales a dibujar_tablero

        # Dibujar el botón
        pygame.draw.rect(pantalla, color_boton, boton_terminado)
        fuente_boton = pygame.font.Font(None, 30)
        texto_boton = fuente_boton.render("Terminado", True, (0, 0, 0))
        rect_texto_boton = texto_boton.get_rect(center=boton_terminado.center)
        pantalla.blit(texto_boton, rect_texto_boton)

        if juego_terminado:
            if validar_sudoku(sudoku_original, sudoku_usuario):
                mostrar_mensaje(pantalla, "\n\n\n¡Ganaste!")
            else:
                mostrar_mensaje(pantalla, "\n\n\nSudoku incorrecto")
        pygame.display.flip()