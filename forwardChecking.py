def forwardChecking(variables, usadas):
    if len(variables[0]) == 0 and len(variables[1]) == 0:
            return True
    if len(variables[0]) != 0:
        actual = variables[0][0]
        siguientes = (variables[0][1:], variables[1])
    elif len(variables[1]) != 0:
        actual = variables[1][0]
        siguientes = (variables[0], variables[1][1:])

    for palabra in actual.getDominio():
        if palabra in usadas:
            continue
        listaVecinos = []
        actual.setPalabraActual(palabra)
        usadas.add(palabra)
        valida = True
        for restriccion in actual.Ractuales:
            vecino = restriccion[0]
            if vecino.palabra_actual is not None:
                continue
            vecino = restriccion[0]
            aux = vecino.getDominio().copy()
            listaVecinos.append((vecino, aux))
            vecino.actualizarDominio()
            if vecino.getDominio() == set():
                valida = False
                actual.setPalabraActual(None)
                usadas.remove(palabra)
                for vecino, dominio in listaVecinos:
                    vecino.setDominio(dominio)
                break
        if valida:
            if forwardChecking(siguientes, usadas):
                return True
            else:
                actual.setPalabraActual(None)
                usadas.remove(palabra)
                for vecino, dominio in listaVecinos:
                    vecino.setDominio(dominio)

    return False