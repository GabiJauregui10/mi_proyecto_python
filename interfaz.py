from openpyxl import Workbook
import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

ARCHIVO = "insumos.json"
indice_seleccionado = None

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

    global indice_seleccionado

    # Validar cantidad
    if entrada_cantidad.get() == "":
        messagebox.showerror("Error", "Ingresá una cantidad")
        return

    datos = cargar_datos()

    insumo = {
        "nombre": entrada_nombre.get(),
        "lote": entrada_lote.get(),
        "ingreso": entrada_ingreso.get(),
        "vencimiento": entrada_vencimiento.get(),
        "cantidad": int(entrada_cantidad.get())
    }

    # EDITAR
    if indice_seleccionado is not None:

        datos[indice_seleccionado] = insumo

        indice_seleccionado = None

        messagebox.showinfo(
    "Éxito",
    "Insumo actualizado correctamente"
)

    # NUEVO
    else:

        datos.append(insumo)

        messagebox.showinfo(
            "Éxito",
            "Insumo agregado correctamente"
        )

    guardar_datos(datos)

    ver_insumos()

    # Limpiar campos
    entrada_nombre.delete(0, tk.END)
    entrada_lote.delete(0, tk.END)
    entrada_ingreso.delete(0, tk.END)
    entrada_vencimiento.delete(0, tk.END)
    entrada_cantidad.delete(0, tk.END)

def ver_insumos():

    datos = cargar_datos()

    tabla.delete(*tabla.get_children())

    hoy = datetime.now()

    for i in datos:

        fecha_venc = datetime.strptime(
            i["vencimiento"],
            "%Y-%m-%d"
        )

        dias = (fecha_venc - hoy).days

        # Determinar color
        if dias < 0:
            color = "vencido"

        elif dias <= 30:
            color = "proximo"

        else:
            color = "normal"

        tabla.insert(
            "",
            tk.END,
            values=(
                i["nombre"],
                i.get("lote", "Sin lote"),
                i["ingreso"],
                i["vencimiento"],
                i["cantidad"]
            ),
            tags=(color,)
        )

def buscar_insumos():

    busqueda = entrada_buscar.get().lower()

    datos = cargar_datos()

    tabla.delete(*tabla.get_children())

    hoy = datetime.now()

    for i in datos:

        nombre = i["nombre"].lower()
        lote = i.get("lote", "").lower()

        if busqueda in nombre or busqueda in lote:

            fecha_venc = datetime.strptime(
                i["vencimiento"],
                "%Y-%m-%d"
            )

            dias = (fecha_venc - hoy).days

            if dias < 0:
                color = "vencido"

            elif dias <= 30:
                color = "proximo"

            else:
                color = "normal"

            tabla.insert(
                "",
                tk.END,
                values=(
                    i["nombre"],
                    i.get("lote", "Sin lote"),
                    i["ingreso"],
                    i["vencimiento"],
                    i["cantidad"]
                ),
                tags=(color,)
            )   

def exportar_excel():

    datos = cargar_datos()

    libro = Workbook()

    hoja = libro.active

    hoja.title = "Insumos"

    # Encabezados
    hoja.append([
        "Nombre",
        "Lote",
        "Ingreso",
        "Vencimiento",
        "Cantidad"
    ])

    # Datos
    for i in datos:

        hoja.append([
            i["nombre"],
            i.get("lote", "Sin lote"),
            i["ingreso"],
            i["vencimiento"],
            i["cantidad"]
        ])

    libro.save("insumos.xlsx")

    messagebox.showinfo(
        "Éxito",
        "Archivo Excel generado correctamente"
    )

def eliminar_insumo():

    seleccion = tabla.selection()

    if not seleccion:
        messagebox.showerror("Error", "Seleccioná un insumo")
        return

    item_id = seleccion[0]

    indice = tabla.index(item_id)

    datos = cargar_datos()

    datos.pop(indice)

    guardar_datos(datos)

    ver_insumos()

    messagebox.showinfo("Éxito", "Insumo eliminado correctamente")

def cargar_para_editar():

    global indice_seleccionado

    seleccion = tabla.selection()

    if not seleccion:
        messagebox.showwarning(
    "Advertencia",
    "Seleccioná un insumo"
)
        return

    item_id = seleccion[0]

    indice_seleccionado = tabla.index(item_id)

    datos = cargar_datos()

    insumo = datos[indice_seleccionado]

    entrada_nombre.delete(0, tk.END)
    entrada_nombre.insert(0, insumo["nombre"])

    entrada_lote.delete(0, tk.END)
    entrada_lote.insert(0, insumo.get("lote", ""))

    entrada_ingreso.delete(0, tk.END)
    entrada_ingreso.insert(0, insumo["ingreso"])

    entrada_vencimiento.delete(0, tk.END)
    entrada_vencimiento.insert(0, insumo["vencimiento"])

    entrada_cantidad.delete(0, tk.END)
    entrada_cantidad.insert(0, insumo["cantidad"])

    messagebox.showinfo("Editar",
    "Insumo cargado para edición")

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

# -------- BUSCADOR --------

label_buscar = tk.Label(
    ventana,
    text="Buscar por nombre o lote"
)

label_buscar.pack()

entrada_buscar = tk.Entry(ventana, width=40)
entrada_buscar.pack(pady=5)

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
boton_buscar = tk.Button(
    ventana,
    text="Buscar",
    bg="purple",
    fg="white",
    command=buscar_insumos
)

boton_buscar.pack(pady=10)

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

boton_editar = tk.Button(
    ventana,
    text="Cargar para editar",
    bg="orange",
    fg="white",
    command=cargar_para_editar
)

boton_editar.pack(pady=10)

boton_excel = tk.Button(
    ventana,
    text="Exportar a Excel",
    bg="darkgreen",
    fg="white",
    command=exportar_excel
)

boton_excel.pack(pady=10)

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

# -------- COLORES --------

tabla.tag_configure("vencido", background="red")
tabla.tag_configure("proximo", background="yellow")
tabla.tag_configure("normal", background="lightgreen")

# ---------------- EJECUTAR ----------------

ventana.mainloop()
