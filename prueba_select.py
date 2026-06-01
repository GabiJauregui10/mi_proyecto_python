from database import obtener_insumos

datos = obtener_insumos()

for fila in datos:
    print(fila)

    