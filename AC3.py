from collections import deque

def ac3(variables):
    # R.ACTUALES => (VECINO, POS-MIA, POS-VECINO)
    # USAMOS DEQUE PARA AHORRO DE MEMORIA
    cola_restricciones = deque()
    if(len(variables[0]) != 0):
        for variable in variables[0]:
            for restriccion in variable.Ractuales:
                cola_restricciones.append((variable, restriccion))
    if(len(variables[1]) != 0):
        for variable in variables[1]:
            for restriccion in variable.Ractuales:
                cola_restricciones.append((variable, restriccion))

    print("DOMINIOS ANTES DEL AC3 \n")
    mostrarDominios(variables)
    res = True

    for horizontal in variables[0]:
        if(len(horizontal.getDominio()) == 0):
            res = False

    for vertical in variables[1]:
        if(len(vertical.getDominio()) == 0):
            res = False
            
    for otras in variables[2]:
        if(len(otras.getDominio()) == 0):
            res = False

    while res and cola_restricciones:
        modificado = False
        tupla = cola_restricciones.popleft()
        nuevoDominio = set()
        actual = tupla[0]
        vecino = tupla[1][0]
        pos_mio = tupla[1][1]
        pos_vecino = tupla[1][2]

        for palabra in actual.getDominio():
            pareja = False
            for restringida in vecino.getDominio():
                if palabra[pos_mio] == restringida[pos_vecino]:
                    nuevoDominio.add(palabra)
                    pareja = True
                    break # PARA NO SEGUIR RECORRIENDO, YA HEMOS VISTO QUE VALE LA PALABRA
            if not pareja:
                modificado = True
        actual.setDominio(nuevoDominio)
        if modificado:
            for v in actual.Ractuales:
                if v[0] != vecino:
                    restriccion = (actual, v[2], v[1])
                    tupla_nueva = (v[0], restriccion)
                    if tupla_nueva not in cola_restricciones:
                        cola_restricciones.append(tupla_nueva)
        if len(nuevoDominio) == 0:
            res = False
            break

        
    print("DOMINIOS DESPUÉS DEL AC3 \n")
    mostrarDominios(variables)

    
    return res



def mostrarDominios(variables):
    for h in variables[0]:
        print(h)
    for v in variables[1]:
        print(v)
    for o in variables[2]:
        print(o)
