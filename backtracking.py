def backtracking(variables, usadas): 
    if len(variables[0]) == 0 and len(variables[1]) == 0:
        return True
    valida = False
    if len(variables[0]) != 0:
        actual = variables[0][0]
        actual.actualizarDominio()
        
        if actual.getDominio() == set():
            return False
        else:
            for palabra in actual.getDominio():
                if palabra in usadas:
                    continue

                actual.setPalabraActual(palabra)
                usadas.add(palabra)
                valida = backtracking((variables[0][1:], variables[1]), usadas)
                if valida:
                    return True
                actual.setPalabraActual(None)
                usadas.remove(palabra)
            return False

    if len(variables[1]) != 0:
        actual = variables[1][0]
        actual.actualizarDominio()
        if actual.getDominio() == set():
            return False
        else:
            for palabra in actual.getDominio():
                if palabra in usadas:
                    continue

                actual.setPalabraActual(palabra)
                usadas.add(palabra)
                valida = backtracking((variables[0], variables[1][1:]), usadas)
                if valida:
                    return True
                actual.setPalabraActual(None)
                usadas.remove(palabra)
            return False