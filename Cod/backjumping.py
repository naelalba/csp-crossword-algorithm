def backjumping(variables, usadas):
    pendientes = variables[0] + variables[1]
    orden = {}
    for i in range(len(pendientes)):
        orden[pendientes[i]] = i
    usadas_dic = {}
    for palabra in usadas:
        usadas_dic[palabra] = None

    conflictos = {}
    valida, salto = bj(pendientes, 0, orden, usadas_dic, conflictos)
    return valida

def bj(pendientes, nivel, orden, usadas, conflictos):
    if nivel == len(pendientes):
        return True, None

    actual = pendientes[nivel]
    conflictos[actual] = set() 
    for palabra in sorted(actual.getDominio()):
        
        if palabra in usadas:
            culpable = usadas[palabra]
            if culpable is not None:
                conflictos[actual].add(culpable)
            continue

        valida = True
        for restriccion in actual.Ractuales:
            vecino = restriccion[0]
            pos_mia = restriccion[1]
            pos_vecino = restriccion[2]
            if vecino.palabra_actual is None:
                continue
            if palabra[pos_mia] != vecino.palabra_actual[pos_vecino]:
                conflictos[actual].add(vecino)
                valida = False
                break
        if not valida:
            continue

        actual.setPalabraActual(palabra)
        usadas[palabra] = actual
        resultado, salto = bj(pendientes, nivel + 1, orden, usadas, conflictos)
        if resultado:
            return True, None

        actual.setPalabraActual(None)
        del usadas[palabra]

        if salto is None:
            return False, None   
        if salto is not actual:
            return False, salto

    if len(conflictos[actual]) == 0:
        return False, None
    
    destino = actual
    for culpable in conflictos[actual]:
        if destino is actual or orden[culpable] > orden[destino]:
            destino = culpable

    for culpable in conflictos[actual]:
        if culpable is not destino:
            conflictos[destino].add(culpable)

    return False, destino