from openpyxl import Workbook
import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime
from tkcalendar import DateEntry

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

    # -------- VALIDACIONES --------

    if (
        entrada_nombre.get().strip() == "" or
        entrada_lote.get().strip() == "" or
        entrada_ingreso.get().strip() == "" or
        entrada_vencimiento.get().strip() == "" or
        entrada_cantidad.get().strip() == ""
    ):

        messagebox.showerror(
            "Error",
            "Todos los campos son obligatorios"
        )

        return

    # Cantidad numérica
    try:

        cantidad = int(
            entrada_cantidad.get()
        )

    except ValueError:

        messagebox.showerror(
            "Error",
            "La cantidad debe ser un número"
        )

        return

    # Cantidad positiva
    if cantidad < 0:

        messagebox.showerror(
            "Error",
            "La cantidad no puede ser negativa"
        )

        return

    # Validar fechas
    try:

        fecha_ingreso = datetime.strptime(
            entrada_ingreso.get(),
            "%Y-%m-%d"
        )

        fecha_vencimiento = datetime.strptime(
            entrada_vencimiento.get(),
            "%Y-%m-%d"
        )

    except ValueError:

        messagebox.showerror(
            "Error",
            "Las fechas deben tener formato YYYY-MM-DD"
        )

        return

    # Vencimiento posterior al ingreso
    if fecha_vencimiento < fecha_ingreso:

        messagebox.showerror(
            "Error",
            "La fecha de vencimiento no puede ser anterior a la fecha de ingreso"
        )

        return

    # -------- GUARDAR DATOS --------

    datos = cargar_datos()

    insumo = {
        "nombre": entrada_nombre.get(),
        "lote": entrada_lote.get(),
        "ingreso": entrada_ingreso.get(),
        "vencimiento": entrada_vencimiento.get(),
        "cantidad": cantidad
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

    actualizar_estadisticas()

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

def actualizar_estadisticas():

    datos = cargar_datos()

    hoy = datetime.now()

    total = len(datos)

    vencidos = 0
    proximos = 0
    stock_bajo = 0

    for i in datos:

        fecha_venc = datetime.strptime(
            i["vencimiento"],
            "%Y-%m-%d"
        )

        dias = (fecha_venc - hoy).days

        if dias < 0:
            vencidos += 1

        elif dias <= 30:
            proximos += 1

        if i["cantidad"] < 5:
            stock_bajo += 1

    label_total.config(
        text=f"📦 Total: {total}"
    )

    label_vencidos.config(
        text=f"🔴 Vencidos: {vencidos}"
    )

    label_proximos.config(
        text=f"🟡 Próximos a vencer: {proximos}"
    )

    label_stock.config(
        text=f"🚨 Stock bajo: {stock_bajo}"
    )
def mostrar_filtrados(tipo):

    datos = cargar_datos()

    tabla.delete(*tabla.get_children())

    hoy = datetime.now()

    for i in datos:

        fecha_venc = datetime.strptime(
            i["vencimiento"],
            "%Y-%m-%d"
        )

        dias = (fecha_venc - hoy).days

        # Color
        if dias < 0:
            color = "vencido"

        elif dias <= 30:
            color = "proximo"

        else:
            color = "normal"

        mostrar = False

        # FILTROS
        if tipo == "todos":
            mostrar = True

        elif tipo == "vencidos" and dias < 0:
            mostrar = True

        elif tipo == "proximos" and dias <= 30 and dias >= 0:
            mostrar = True

        elif tipo == "stock" and i["cantidad"] < 5:
            mostrar = True

        if mostrar:

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
ventana.geometry("1400x800")

# -------- FRAMES PRINCIPALES --------

frame_izquierdo = tk.Frame(
    ventana,
    padx=20,
    pady=20
)

frame_izquierdo.pack(
    side="left",
    fill="y"
)

frame_derecho = tk.Frame(
    ventana,
    padx=20,
    pady=20
)

frame_derecho.pack(
    side="right",
    fill="both",
    expand=True
)

# ---------------- TÍTULO ----------------

titulo = tk.Label(
    frame_derecho,
    text="Sistema de Control de Insumos",
    font=("Arial", 18)
)

titulo.pack(pady=20)

# -------- BUSCADOR --------

label_buscar = tk.Label(
    frame_derecho,
    text="Buscar por nombre o lote"
)

label_buscar.pack()

entrada_buscar = tk.Entry(frame_derecho, width=40)
entrada_buscar.pack(pady=5)
entrada_buscar.bind(
    "<KeyRelease>",
    lambda event: buscar_insumos()
)

# -------- ESTADÍSTICAS --------

label_total = tk.Label(
    frame_derecho,
    text="📦 Total: 0",
    font=("Arial", 10, "bold")
)

label_total.pack()

label_vencidos = tk.Label(
    frame_derecho,
    text="🔴 Vencidos: 0",
    font=("Arial", 10, "bold")
)

label_vencidos.pack()

label_proximos = tk.Label(
    frame_derecho,
    text="🟡 Próximos a vencer: 0",
    font=("Arial", 10, "bold")
)

label_proximos.pack()

label_stock = tk.Label(
    frame_derecho,
    text="🚨 Stock bajo: 0",
    font=("Arial", 10, "bold")
)

label_stock.pack(pady=10)

# -------- FORMULARIO --------

label_formulario = tk.Label(
    frame_izquierdo,
    text="Registrar / Editar Insumo",
    font=("Arial", 16, "bold")
)

label_formulario.pack(pady=10)

# Nombre
label_nombre = tk.Label(
    frame_izquierdo,
    text="Nombre del insumo"
)

label_nombre.pack(anchor="w")

entrada_nombre = tk.Entry(
    frame_izquierdo,
    width=30
)

entrada_nombre.pack(pady=5)

# Lote
label_lote = tk.Label(
    frame_izquierdo,
    text="Número de lote"
)

label_lote.pack(anchor="w")

entrada_lote = tk.Entry(
    frame_izquierdo,
    width=30
)

entrada_lote.pack(pady=5)

# Ingreso
label_ingreso = tk.Label(
    frame_izquierdo,
    text="Fecha ingreso (YYYY-MM-DD)"
)

label_ingreso.pack(anchor="w")

entrada_ingreso = DateEntry(
    frame_izquierdo,
    width=27,
    date_pattern="yyyy-mm-dd"
)

entrada_ingreso.pack(pady=5)

# Vencimiento
label_vencimiento = tk.Label(
    frame_izquierdo,
    text="Fecha vencimiento (YYYY-MM-DD)"
)

label_vencimiento.pack(anchor="w")

entrada_vencimiento = DateEntry(
    frame_izquierdo,
    width=27,
    date_pattern="yyyy-mm-dd"
)

entrada_vencimiento.pack(pady=5)

# Cantidad
label_cantidad = tk.Label(
    frame_izquierdo,
    text="Cantidad"
)

label_cantidad.pack(anchor="w")

entrada_cantidad = tk.Entry(
    frame_izquierdo,
    width=30
)

entrada_cantidad.pack(pady=5)

# ---------------- BOTÓN ----------------
boton_buscar = tk.Button(
    frame_izquierdo,
    text="Buscar",
    bg="purple",
    fg="white",
    command=buscar_insumos
)

boton_buscar.pack(pady=10)

boton_guardar = tk.Button(
    frame_izquierdo,
    text="Guardar insumo",
    bg="green",
    fg="white",
    command=guardar_insumo
)

boton_guardar.pack(pady=20)

boton_ver = tk.Button(
    frame_izquierdo,
    text="Ver insumos",
    bg="blue",
    fg="white",
    command=ver_insumos
)

boton_ver.pack(pady=10)

boton_eliminar = tk.Button(
    frame_izquierdo,
    text="Eliminar insumo",
    bg="red",
    fg="white",
    command=eliminar_insumo
)

boton_eliminar.pack(pady=10)

boton_editar = tk.Button(
    frame_izquierdo,
    text="Cargar para editar",
    bg="orange",
    fg="white",
    command=cargar_para_editar
)

boton_editar.pack(pady=10)

boton_excel = tk.Button(
    frame_izquierdo,
    text="Exportar a Excel",
    bg="darkgreen",
    fg="white",
    command=exportar_excel
)

boton_excel.pack(pady=10)

# -------- FILTROS --------

boton_todos = tk.Button(
    frame_izquierdo,
    text="Todos",
    command=lambda: mostrar_filtrados("todos")
)

boton_todos.pack(pady=2)

boton_vencidos = tk.Button(
    frame_izquierdo,
    text="Vencidos",
    bg="red",
    fg="white",
    command=lambda: mostrar_filtrados("vencidos")
)

boton_vencidos.pack(pady=2)

boton_proximos = tk.Button(
    frame_izquierdo,
    text="Próximos",
    bg="orange",
    fg="white",
    command=lambda: mostrar_filtrados("proximos")
)

boton_proximos.pack(pady=2)

boton_stock = tk.Button(
    frame_izquierdo,
    text="Stock bajo",
    bg="purple",
    fg="white",
    command=lambda: mostrar_filtrados("stock")
)

boton_stock.pack(pady=2)

# ---------------- TABLA ----------------

tabla = ttk.Treeview(frame_derecho)

tabla["columns"] = (
    "Nombre",
    "Lote",
    "Ingreso",
    "Vencimiento",
    "Cantidad"
)

tabla.column("#0", width=0, stretch=tk.NO)

tabla.column("Nombre", width=250)
tabla.column("Lote", width=150)
tabla.column("Ingreso", width=150)
tabla.column("Vencimiento", width=150)
tabla.column("Cantidad", width=100)

tabla.heading("#0", text="")

tabla.heading("Nombre", text="Nombre")
tabla.heading("Lote", text="Lote")
tabla.heading("Ingreso", text="Ingreso")
tabla.heading("Vencimiento", text="Vencimiento")
tabla.heading("Cantidad", text="Cantidad")

tabla.pack(
    pady=20,
    fill="both",
    expand=True
)

# -------- COLORES --------

tabla.tag_configure("vencido", background="red")
tabla.tag_configure("proximo", background="yellow")
tabla.tag_configure("normal", background="lightgreen")

# ---------------- EJECUTAR ----------------
ver_insumos()
ventana.mainloop()

