import pygame
from pygame.locals import *
import tkinter
from tkinter import *
from tkinter.simpledialog import *
from tkinter import messagebox as MessageBox
import sys
import time
import copy
from tablero import *
from variable import *
from backtracking import *
from forwardChecking import *
from AC3 import *

GREY=(190, 190, 190)
NEGRO=(100,100, 100)
BLANCO=(255, 255, 255)
GRIS_ACTIVO=(245,245,245)
GRIS_NORMAL=(169,169,169)

MARGEN=5 #ancho del borde entre celdas
MARGEN_DERECHO=125 #ancho del margen derecho entre la cuadrícula y la ventana
TAM=60  #tamaño de la celda

LLENA='*' 
VACIA='-'

#########################################################################
# Detecta si se pulsa un botón
#########################################################################   
def pulsaBoton(pos, boton):
    if boton.collidepoint(pos[0], pos[1]):    
        return True
    else:
        return False
    
#########################################################################
# Pintar un boton
#########################################################################   
def pintarBoton(screen, fuenteBot, boton, mensaje):
    if boton.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, GRIS_ACTIVO, boton, 0)        
    else:
        pygame.draw.rect(screen, GRIS_NORMAL, boton, 0)
        
    texto=fuenteBot.render(mensaje, True, NEGRO)
    screen.blit(texto, (boton.x+(boton.width-texto.get_width())/2, boton.y+(boton.height-texto.get_height())/2))         

#########################################################################
# Pintar el crucigrama
#########################################################################         
def pintarTablero(screen, fuenteCelda,tablero, filas, cols):
    pygame.draw.rect(screen, GREY, [0, 0, filas*(TAM+MARGEN)+MARGEN, cols*(TAM+MARGEN)+MARGEN],0)
    for fil in range(tablero.getAlto()):
        for col in range(tablero.getAncho()):
            if tablero.getCelda(fil, col)==VACIA: 
                pygame.draw.rect(screen, BLANCO, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)
            elif tablero.getCelda(fil, col)==LLENA: 
                pygame.draw.rect(screen, NEGRO, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)
            else: #dibujar letra                    
                pygame.draw.rect(screen, BLANCO, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)                
                texto= fuenteCelda.render(tablero.getCelda(fil, col), True, NEGRO)            
                screen.blit(texto, [(TAM+MARGEN)*col+MARGEN+15, (TAM+MARGEN)*fil+MARGEN+5])    
    
######################################################################### 
# Detecta si el ratón se pulsa en la cuadrícula
######################################################################### 
def inTablero(pos, filas, cols):
    if pos[0]>=MARGEN and pos[0]<=(TAM+MARGEN)*cols+MARGEN and pos[1]>=MARGEN and pos[1]<=(TAM+MARGEN)*filas+MARGEN:        
        return True
    else:
        return False
    
######################################################################### 
# Crea el almacen de palabras
######################################################################### 
def creaAlmacen(file):   
    f= open(file, 'r', encoding="utf-8")
    lista=f.read()
    f.close()
    listaPal=lista.split()
    almacen={}
    for pal in listaPal:        
        if len(pal) not in almacen:
            almacen[len(pal)]=set()
            almacen[len(pal)].add(pal.upper())
        else:
            almacen[len(pal)].add(pal.upper())   
    
    return almacen

######################################################################### 
# Imprime el contenido del almacen
######################################################################### 
def imprimeAlmacen(almacen):
    for tam, palabras in almacen.items():
        print (f'tam: {tam}: {palabras}')
        
######################################################################### 
# Inicializa las variables del tablero
#########################################################################

def construir_variables(tablero, almacen):
    variablesHorizontales = []
    variablesVerticales = []
    otrasVariables = []
    fils = tablero.getAlto()
    cols = tablero.getAncho()

## Extraer variables horizontales
    for f in range(fils):
        inicio = -1
        longitud = 0
        restricciones = []
        for c in range(cols):
            celda = tablero.getCelda(f, c)
            if celda == LLENA:
                if longitud >= 2:
                    variable = Variable('h', (f, inicio), longitud, restricciones, almacen.get(longitud, set())) ## Para que no de error a la hora de crear el almacen si no hay palabras de esa longitud
                    variablesHorizontales.append(variable)
                inicio = -1
                longitud = 0
                restricciones = []
            else:
                if inicio == -1:
                    inicio = c
                longitud += 1
                if celda != VACIA:
                    restricciones.append(((f, c), celda)) ## Celda es la letra
        if longitud >= 2:
            variable = Variable('h', (f, inicio), longitud, restricciones, almacen.get(longitud, set()))
            variablesHorizontales.append(variable)

### Extraer variables verticales
    for c in range(cols):
        inicio = -1
        longitud = 0
        restricciones = []
        for f in range(fils):
            celda = tablero.getCelda(f, c)
            if celda == LLENA:
                if longitud >= 2:
                    variable = Variable('v', (inicio, c), longitud, restricciones, almacen.get(longitud, set()))
                    variablesVerticales.append(variable)
                inicio = -1
                longitud = 0
                restricciones = []
            else:
                if inicio == -1:
                    inicio = f
                longitud += 1
                if celda != VACIA:
                    restricciones.append(((f, c), celda))
        if longitud >= 2:
            variable = Variable('v', (inicio, c), longitud, restricciones, almacen.get(longitud, set()))
            variablesVerticales.append(variable)

    for f in range(fils):
        for c in range(cols):
            celda = tablero.getCelda(f, c)
            if celda != LLENA:
                aislada = True
                if f > 0 and tablero.getCelda(f-1, c) != LLENA:
                    aislada = False
                if f < fils - 1 and tablero.getCelda(f+1, c) != LLENA:
                    aislada = False
                if c > 0 and tablero.getCelda(f, c-1) != LLENA:
                    aislada = False
                if c < cols - 1 and tablero.getCelda(f, c+1) != LLENA:
                    aislada = False
                if aislada:
                    restricciones = []
                    if celda != VACIA:
                        restricciones.append(((f, c), celda))
                    var = Variable('u', (f,c), 1, restricciones, almacen.get(1, set()))
                    otrasVariables.append(var)

    construir_restricciones(variablesHorizontales, variablesVerticales)

    return variablesHorizontales, variablesVerticales, otrasVariables

#########################################################################  
# Funcion que se encarga de examinar las restricciones entre variables
#########################################################################

def construir_restricciones(variablesHorizontales, variablesVerticales):
    for h in variablesHorizontales:
        for v in variablesVerticales:
            h_pos = h.getPosInicial()
            for i in range(h.getLongitud()):
                casilla_h = (h_pos[0], h_pos[1] + i)
                v_pos = v.getPosInicial()
                for j in range(v.getLongitud()):
                    casilla_v = (v_pos[0] + j, v_pos[1])
                    if casilla_h == casilla_v:
                        h.Ractuales.append((v, i, j))
                        v.Ractuales.append((h, j, i)) ## Él, desplazamiento mio, desplazamiento suyo
                        break

#########################################################################  
# Funcion que actualiza el tablero con las palabras encontradas
#########################################################################
def actualizarTablero(tablero, variables):
    for h in variables[0]:
        if h.getPalabraActual() is not None:
            pos = h.getPosInicial()
            for i in range(h.getLongitud()):
                tablero.setCelda(pos[0], pos[1] + i, h.getPalabraActual()[i])
    for v in variables[1]:
        if v.getPalabraActual() is not None:
            pos = v.getPosInicial()
            for i in range(v.getLongitud()):
                if tablero.getCelda(pos[0] + i, pos[1]) == VACIA:
                    tablero.setCelda(pos[0] + i, pos[1], v.getPalabraActual()[i])
    for o in variables[2]:
        if o.getPalabraActual() is not None:
            pos = o.getPosInicial()
            tablero.setCelda(pos[0], pos[1], o.getPalabraActual())


#########################################################################  
# Función que se encarga de analizar las variables de longitud 1
#########################################################################
def gestionarCortas(v, usadas):
    valido = True
    for variable in v:
        for palabra in variable.getDominio():
            if palabra in usadas:
                continue
            else:
                variable.setPalabraActual(palabra)
                usadas.add(palabra)
                break
        if variable.getPalabraActual() == None:
            valido = False
    return valido

#########################################################################  
# Principal
#########################################################################
def main():
    root= tkinter.Tk() #para eliminar la ventana de Tkinter
    root.withdraw() #se cierra
    pygame.init()
    
    reloj=pygame.time.Clock()
    
    print("Uso: python main.py --filas M --columnas N --dic archivo.txt")
    if '--filas' in sys.argv:
        filas = int(sys.argv[sys.argv.index("--filas") + 1])
    else:
        filas=5
    if '--columnas' in sys.argv:
        cols = int(sys.argv[sys.argv.index("--columnas") + 1])
    else:
        cols=6
    if '--dic' in sys.argv:
        file = sys.argv[sys.argv.index("--dic") + 1]
    else:
        file='d0.txt'    
        
    anchoVentana=cols*(TAM+MARGEN)+MARGEN_DERECHO
    altoVentana= filas*(TAM+MARGEN)+2*MARGEN 
    dimension=[anchoVentana,altoVentana]
    screen=pygame.display.set_mode(dimension) 
    pygame.display.set_caption("Practica 1: Crucigrama")    

    #La altura del botón depende del tamaño de la ventana pero hay una altura máxima
    altoBoton=altoVentana//5    
    if altoBoton>=65:
        altoBoton=65    
    
    posBotBK=altoVentana//4-altoBoton//2
    posBotFC=altoVentana//2-altoBoton//2
    posBotAC3=(altoVentana//2+altoVentana)//2-altoBoton//2      
    botBK=pygame.Rect(anchoVentana-95, posBotBK, 70, altoBoton)    
    botFC=pygame.Rect(anchoVentana-95,posBotFC , 70, altoBoton)
    botAC3=pygame.Rect(anchoVentana-95, posBotAC3, 70, altoBoton)

    tamFuenteBot=int(altoBoton//1.5)    
    fuenteBot=pygame.font.Font(None, tamFuenteBot)
    fuenteCelda= pygame.font.Font(None, 70)
    
    almacen=creaAlmacen(file)
    #imprimeAlmacen(almacen)
    game_over=False
    tablero=Tablero(filas, cols)    

    variables = None
    ac3_ok = False

    while not game_over:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:               
                game_over=True
            if event.type==pygame.MOUSEBUTTONUP:                
                #obtener posición y calcular coordenadas matriciales                               
                pos=pygame.mouse.get_pos()                
                if pulsaBoton(pos, botBK):
                    print('BK')
                    if not ac3_ok:
                        variables = construir_variables(tablero, almacen)
                    usadas = set()
                    sol = gestionarCortas(variables[2], usadas)
                    if sol == False:
                        MessageBox.showwarning("Alerta", "No hay solución")
                    else:
                        res = backtracking(variables, usadas) 
                        if res==False:
                                MessageBox.showwarning("Alerta", "No hay solución")   
                        else:
                            actualizarTablero(tablero, variables)
                    ac3_ok = False
                elif pulsaBoton(pos, botFC):
                    print('FC')
                    if not ac3_ok:
                        variables = construir_variables(tablero, almacen)
                    usadas = set()
                    sol = gestionarCortas(variables[2], usadas)
                    if sol == False:
                        MessageBox.showwarning("Alerta", "No hay solución")
                    else:
                        res = forwardChecking(variables, usadas)
                        if res==False:
                            MessageBox.showwarning("Alerta", "No hay solución")
                        else:
                            actualizarTablero(tablero, variables)
                    ac3_ok = False
                elif pulsaBoton(pos, botAC3):
                    print('AC3')
                    variables = construir_variables(tablero, almacen)
                    ac3_ok = ac3(variables)
                    if not ac3_ok:
                        variables = None
                        MessageBox.showwarning("Alerta", "No hay solución")
                elif inTablero(pos, filas, cols):
                    ac3_ok = False
                    colDestino=pos[0]//(TAM+MARGEN)
                    filDestino=pos[1]//(TAM+MARGEN)                    
                    if event.button==1: #botón izquierdo
                        if tablero.getCelda(filDestino, colDestino)==VACIA:
                            tablero.setCelda(filDestino, colDestino, LLENA)
                        else:
                            tablero.setCelda(filDestino, colDestino, VACIA)
                    elif event.button==3: #botón derecho
                        c=askstring('Entrada', 'Introduce carácter')
                        if not c is None:
                            tablero.setCelda(filDestino, colDestino, c.upper())             
        #limpiar pantalla
        screen.fill(GREY)
        #pintar crucigrama 
        pintarTablero(screen, fuenteCelda, tablero, filas, cols)                   
        #pintar botones           
        pintarBoton(screen, fuenteBot, botBK, "BK")
        pintarBoton(screen, fuenteBot, botFC, "FC")
        pintarBoton(screen, fuenteBot, botAC3, "AC3")   
        #actualizar pantalla
        pygame.display.flip()
        reloj.tick(40)
        if game_over==True: #retardo cuando se cierra la ventana
            pygame.time.delay(500)
    
    pygame.quit()

if __name__=="__main__":
    main()

