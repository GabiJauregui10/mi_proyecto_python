import json
from datetime import datetime

ARCHIVO = "insumos.json"

def cargar_datos():
    try:
        with open(ARCHIVO, "r") as f:
            return json.load(f)
    except:
        return []

def guardar_datos(datos):
    with open(ARCHIVO, "w") as f:
        json.dump(datos, f, indent=4)

def agregar_insumo():
    datos = cargar_datos()

    nombre = input("Nombre del insumo: ")
    lote = input("Número de lote: ")
    fecha_ingreso = input("Fecha ingreso (YYYY-MM-DD): ")
    fecha_vencimiento = input("Fecha vencimiento (YYYY-MM-DD): ")
    cantidad = int(input("Cantidad: "))

    insumo = {
    "nombre": nombre,
    "lote": lote,
    "ingreso": fecha_ingreso,
    "vencimiento": fecha_vencimiento,
    "cantidad": cantidad
}

    datos.append(insumo)
    guardar_datos(datos)
    print("✅ Insumo agregado correctamente")

def ver_insumos():
    datos = cargar_datos()
    print("\n📋 LISTA DE INSUMOS")

    for i in datos:
        print("----------------------------")
        print("Nombre:", i["nombre"])
        print("Lote:", i.get("lote", "Sin lote"))
        print("Ingreso:", i["ingreso"])
        print("Vencimiento:", i["vencimiento"])
        print("Cantidad:", i["cantidad"])

def insumos_por_vencer():
    datos = cargar_datos()
    hoy = datetime.now()
    encontrados = False

    print("\n⚠️ INSUMOS POR VENCER (30 días)")

    for i in datos:
        try:
            fecha_venc = datetime.strptime(i["vencimiento"], "%Y-%m-%d")
            dias = (fecha_venc - hoy).days

            if dias <= 30:
                print(i["nombre"], "- vence en", dias, "días")
                encontrados = True

        except:
            print(f"❌ Fecha incorrecta en el insumo: {i['nombre']}")

    if not encontrados:
        print("✔️ No hay insumos por vencer")

def insumos_poca_cantidad():
    datos = cargar_datos()
    print("\n🚨 INSUMOS CON POCA CANTIDAD (<5)")
    for i in datos:
        if i["cantidad"] < 5:
            print(i["nombre"], "- quedan", i["cantidad"])

def buscar_insumo():
    datos = cargar_datos()

    busqueda = input("Ingrese nombre o lote a buscar: ").lower()

    encontrados = False

    print("\n🔎 RESULTADOS DE BÚSQUEDA")

    for i in datos:
        nombre = i["nombre"].lower()
        lote = i.get("lote", "").lower()

        if busqueda in nombre or busqueda in lote:
            print("----------------------------")
            print("Nombre:", i["nombre"])
            print("Lote:", i.get("lote", "Sin lote"))
            print("Ingreso:", i["ingreso"])
            print("Vencimiento:", i["vencimiento"])
            print("Cantidad:", i["cantidad"])

            encontrados = True

    if not encontrados:
        print("❌ No se encontraron insumos")

def editar_cantidad():
    datos = cargar_datos()

    busqueda = input("Ingrese nombre o lote del insumo: ").lower()

    encontrado = False

    for i in datos:
        nombre = i["nombre"].lower()
        lote = i.get("lote", "").lower()

        if busqueda == nombre or busqueda == lote:

            print("\n📦 INSUMO ENCONTRADO")
            print("Nombre:", i["nombre"])
            print("Lote:", i.get("lote", "Sin lote"))
            print("Cantidad actual:", i["cantidad"])

            nueva_cantidad = int(input("Nueva cantidad: "))

            i["cantidad"] = nueva_cantidad

            guardar_datos(datos)

            print("✅ Cantidad actualizada correctamente")

            encontrado = True
            break

    if not encontrado:
        print("❌ No se encontró el insumo")

def eliminar_insumo():
    datos = cargar_datos()

    busqueda = input("Ingrese nombre o lote del insumo a eliminar: ").lower()

    encontrado = False

    for i in datos:
        nombre = i["nombre"].lower()
        lote = i.get("lote", "").lower()

        if busqueda == nombre or busqueda == lote:

            print("\n🗑️ INSUMO ENCONTRADO")
            print("Nombre:", i["nombre"])
            print("Lote:", i.get("lote", "Sin lote"))
            print("Cantidad:", i["cantidad"])

            confirmar = input("¿Seguro que desea eliminarlo? (s/n): ").lower()

            if confirmar == "s":
                datos.remove(i)
                guardar_datos(datos)

                print("✅ Insumo eliminado correctamente")

            else:
                print("❌ Eliminación cancelada")

            encontrado = True
            break

    if not encontrado:
        print("❌ No se encontró el insumo")                

def menu():
    while True:
        print("\n--- CONTROL DE INSUMOS QUÍMICOS ---")
        print("1. Agregar insumo (con lote)")
        print("2. Ver insumos")
        print("3. Insumos por vencer")
        print("4. Insumos con poca cantidad")
        print("5. Buscar insumo")
        print("6. Editar cantidad")
        print("7. Eliminar insumo")
        print("8. Salir")

        opcion = input("Elegir opción: ")

        if opcion == "1":
            agregar_insumo()
        elif opcion == "2":
            ver_insumos()
        elif opcion == "3":
            insumos_por_vencer()
        elif opcion == "4":
            insumos_poca_cantidad()
        elif opcion == "5":
            buscar_insumo()
        elif opcion == "6":
            editar_cantidad()
        elif opcion == "7":
            eliminar_insumo()
        elif opcion == "8":
            break

menu()
