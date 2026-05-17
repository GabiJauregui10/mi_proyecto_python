import tkinter as tk
from tkinter import ttk
import json

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

def guardar_insumo():

    datos = cargar_datos()

    insumo = {
        "nombre": entrada_nombre.get(),
        "lote": entrada_lote.get(),
        "ingreso": entrada_ingreso.get(),
        "vencimiento": entrada_vencimiento.get(),
        "cantidad": int(entrada_cantidad.get())
    }

    datos.append(insumo)

    guardar_datos(datos)

    print("✅ Insumo guardado")


def ver_insumos():

    datos = cargar_datos()

    # Limpiar tabla
    for fila in tabla.get_children():
        tabla.delete(fila)

    # Insertar datos
    for i in datos:

        tabla.insert(
            "",
            tk.END,
            values=(
                i["nombre"],
                i.get("lote", "Sin lote"),
                i["ingreso"],
                i["vencimiento"],
                i["cantidad"]
            )
        )

def eliminar_insumo():

    seleccion = tabla.selection()

    if not seleccion:
        print("❌ No seleccionaste ningún insumo")
        return

    item = tabla.item(seleccion)

    valores = item["values"]

    nombre = valores[0]
    lote = valores[1]

    datos = cargar_datos()

    nuevos_datos = []

    for i in datos:

        if not (
            i["nombre"] == nombre and
            i.get("lote", "Sin lote") == lote
        ):
            nuevos_datos.append(i)

    guardar_datos(nuevos_datos)

    print("✅ Insumo eliminado")

    ver_insumos()

# ---------------- VENTANA ----------------

ventana = tk.Tk()
ventana.title("Control de Insumos Químicos")
ventana.geometry("500x500")

# ---------------- TÍTULO ----------------

titulo = tk.Label(
    ventana,
    text="Sistema de Control de Insumos",
    font=("Arial", 18)
)

titulo.pack(pady=20)

# ---------------- NOMBRE ----------------

label_nombre = tk.Label(ventana, text="Nombre del insumo")
label_nombre.pack()

entrada_nombre = tk.Entry(ventana, width=40)
entrada_nombre.pack(pady=5)

# ---------------- LOTE ----------------

label_lote = tk.Label(ventana, text="Número de lote")
label_lote.pack()

entrada_lote = tk.Entry(ventana, width=40)
entrada_lote.pack(pady=5)

# ---------------- INGRESO ----------------

label_ingreso = tk.Label(ventana, text="Fecha ingreso (YYYY-MM-DD)")
label_ingreso.pack()

entrada_ingreso = tk.Entry(ventana, width=40)
entrada_ingreso.pack(pady=5)

# ---------------- VENCIMIENTO ----------------

label_vencimiento = tk.Label(ventana, text="Fecha vencimiento (YYYY-MM-DD)")
label_vencimiento.pack()

entrada_vencimiento = tk.Entry(ventana, width=40)
entrada_vencimiento.pack(pady=5)

# ---------------- CANTIDAD ----------------

label_cantidad = tk.Label(ventana, text="Cantidad")
label_cantidad.pack()

entrada_cantidad = tk.Entry(ventana, width=40)
entrada_cantidad.pack(pady=5)

# ---------------- BOTÓN ----------------

boton_guardar = tk.Button(
    ventana,
    text="Guardar insumo",
    bg="green",
    fg="white",
    command=guardar_insumo
)

boton_guardar.pack(pady=20)

boton_ver = tk.Button(
    ventana,
    text="Ver insumos",
    bg="blue",
    fg="white",
    command=ver_insumos
)

boton_ver.pack(pady=10)

boton_eliminar = tk.Button(
    ventana,
    text="Eliminar insumo",
    bg="red",
    fg="white",
    command=eliminar_insumo
)

boton_eliminar.pack(pady=10)

# ---------------- TABLA ----------------

tabla = ttk.Treeview(ventana)

tabla["columns"] = (
    "Nombre",
    "Lote",
    "Ingreso",
    "Vencimiento",
    "Cantidad"
)

tabla.column("#0", width=0, stretch=tk.NO)

tabla.column("Nombre", width=120)
tabla.column("Lote", width=100)
tabla.column("Ingreso", width=100)
tabla.column("Vencimiento", width=100)
tabla.column("Cantidad", width=80)

tabla.heading("#0", text="")

tabla.heading("Nombre", text="Nombre")
tabla.heading("Lote", text="Lote")
tabla.heading("Ingreso", text="Ingreso")
tabla.heading("Vencimiento", text="Vencimiento")
tabla.heading("Cantidad", text="Cantidad")

tabla.pack(pady=20)

# ---------------- EJECUTAR ----------------

ventana.mainloop()
