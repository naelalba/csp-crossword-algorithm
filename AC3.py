from collections import deque

def ac3(variables):
    # R.ACTUALES => (VECINO, POS-MIA, POS-VECINO)
    # USAMOS DEQUE PARA AHORRO DE MEMORIA
    cola_restricciones = deque()
    if(len(variables[0]) != 0):
        for variable in variables[0]:
            for restriccion in variable.Ractuales:
                cola_restricciones.append((variable, restriccion[0]))
    if(len(variables[1]) != 0):
        for variable in variables[1]:
            for restriccion in variable.Ractuales:
                cola_restricciones.append((variable, restriccion[0]))

    print("DOMINIOS ANTES DEL AC3 \n")
    mostrarDominios(variables)





    print("DOMINIOS DESPUÉS DEL AC3 \n")



def mostrarDominios(variables):
    for h in variables[0]:
        print(h)
    for v in variables[1]:
        print(v)
