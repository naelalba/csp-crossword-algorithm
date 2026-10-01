from main import *

class Variable:
        def __init__(self, orientacion, posicion_inicial, longitud, restricciones_obligatorias, almacen):
                self.nombre = f"{self.tipo}_{self.pos[0]},{self.pos[1]}"
                self.tipo = orientacion
                self.pos = posicion_inicial
                self.long = longitud
                self.Robligatorias = restricciones_obligatorias
                self.dominio = self.calcularDominio(almacen)
                self.Ractuales = []
                self.palabra_actual = None

        def calcularDominio(self, almacen):
            dominio = set()
            
            for palabra in almacen:
                valida = True
                for restriccion in self.Robligatorias:
                    pos_restriccion = restriccion[0]
                    letra = restriccion[1]
                    
                    if self.tipo == 'h':
                        i = pos_restriccion[1] - self.pos[1]
                    else:
                        i = pos_restriccion[0] - self.pos[0]
                    
                    if palabra[i] != letra:
                        valida = False
                        break
                if valida:
                    dominio.add(palabra)
            return dominio

        def actualizarDominio(self):
            res = set()
            for palabra in self.dominio:
                valida = True
                for restriccion in self.Ractuales:
                    vecino = restriccion[0]
                    pos_mia = restriccion[1]
                    pos_vecino = restriccion[2]

                    if vecino.palabra_actual is None:
                        continue
                    else:
                        letra = vecino.palabra_actual[pos_vecino]
                        if palabra[pos_mia] != letra:
                            valida = False
                            break

                if valida:
                    res.add(palabra)
            self.dominio = res







        def setPalabraActual(self, palabra):
            self.palabra_actual = palabra

        def getLongitud(self):
            return self.long

        def getPosInicial(self):
            return self.pos

        def getDominio(self):
            return self.dominio

        def getTipo(self):
            return self.tipo

        def getNombre(self):
            return self.nombre
