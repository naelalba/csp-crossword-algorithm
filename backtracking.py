def backtracking(variables): 
    if len(variables[0]) == 0 and len(variables[1]) == 0:
        return True
    if len(variables[0]) != 0:
        actual = variables[0][0]
        actual.actualizarDominio()
        if actual.getDominio() == set():
            return False
        else:
            for palabra in actual.getDominio():
                actual.setPalabraActual(palabra)
                valida = backtracking((variables[0][1:], variables[1]))
                if valida:
                    return True
                actual.setPalabraActual(None)
            return False

    if len(variables[1]) != 0:
        actual = variables[1][0]
        actual.actualizarDominio()
        if actual.getDominio() == set():
            return False
        else:
            for palabra in actual.getDominio():
                actual.setPalabraActual(palabra)
                valida = backtracking((variables[0], variables[1][1:]))
                if valida:
                    return True
                actual.setPalabraActual(None)
            return False