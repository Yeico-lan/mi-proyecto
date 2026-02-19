import mysql.connector
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox

## ---------------- CONEXIÓN A MYSQL ----------------
def conectar_db():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="db_movimientos"
        )
    except mysql.connector.Error as err:
        messagebox.showerror("Error de conexión", f"No se pudo conectar a MySQL:\n{err}")
        return None


# Crear conexión global inicial.
conn = conectar_db()
if conn:
    cursor = conn.cursor()
else:
    exit()

# ---------------- FUNCIONES ----------------

def agregar_movimiento():
    tipo = tipo_var.get()
    descripcion = descripcion_entry.get().strip()

    if descripcion == "":
        messagebox.showerror("Error", "La descripción no puede estar vacía")
        return

    try:
        monto = float(monto_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Monto inválido")
        return

    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    sql = "INSERT INTO movimientos (tipo, descripcion, monto, fecha_hora) VALUES (%s, %s, %s, %s)"
    valores = (tipo, descripcion, monto, fecha_hora)

    cursor.execute(sql, valores)
    conn.commit()

    descripcion_entry.delete(0, tk.END)
    monto_entry.delete(0, tk.END)

    listar_movimientos()


def listar_movimientos(filtro="todos"):
    for item in tree.get_children():
        tree.delete(item)

    if filtro == "todos":
        cursor.execute("SELECT * FROM movimientos ORDER BY fecha_hora DESC")
    else:
        cursor.execute("SELECT * FROM movimientos WHERE tipo=%s ORDER BY fecha_hora DESC", (filtro,))

    ingresos_total = 0
    gastos_total = 0

    for mov in cursor.fetchall():
        tree.insert("", tk.END, values=mov)

        if mov[1] == "ingreso":
            ingresos_total += float(mov[3])
        else:
            gastos_total += float(mov[3])

    saldo = ingresos_total - gastos_total

    label_total.config(
        text=f"Ingresos: ${ingresos_total:.2f}   |   Gastos: ${gastos_total:.2f}   |   Saldo: ${saldo:.2f}"
    )


def cerrar_programa():
    try:
        conn.close()
    except:
        pass
    root.destroy()


# ---------------- INTERFAZ ----------------

root = tk.Tk()
root.title("YeiSys FMS - Yeico Financial Management System")
root.geometry("900x700")
root.config(bg="#0A0A5F")

style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview",
                background="#000000",
                foreground="white",
                fieldbackground="#4E4D4D",
                rowheight=25)
style.configure("Treeview.Heading", font=("Arial", 10, "bold"))

# Frame principal
main_frame = tk.Frame(root, bg="#A3A3A3")
main_frame.pack(pady=15)

tipo_var = tk.StringVar(value="ingreso")

tk.Label(main_frame, text="Tipo:", bg="#1e1e2f", fg="white").grid(row=0, column=0, padx=5)
tk.OptionMenu(main_frame, tipo_var, "ingreso", "gasto").grid(row=0, column=1, padx=5)

tk.Label(main_frame, text="Descripción:", bg="#1e1e2f", fg="white").grid(row=1, column=0, padx=5)
descripcion_entry = tk.Entry(main_frame, width=30)
descripcion_entry.grid(row=1, column=1, padx=5)

tk.Label(main_frame, text="Monto:", bg="#1e1e2f", fg="white").grid(row=2, column=0, padx=5)
monto_entry = tk.Entry(main_frame, width=30)
monto_entry.grid(row=2, column=1, padx=5)

tk.Button(main_frame, text="Agregar Movimiento",
          bg="#317734", fg="white",
          command=agregar_movimiento).grid(row=3, column=0, columnspan=2, pady=10)

# Botones de filtro
filter_frame = tk.Frame(root, bg="#0c0c0c")
filter_frame.pack()

tk.Button(filter_frame, text="Todos", command=lambda: listar_movimientos("todos")).pack(side=tk.LEFT, padx=5)
tk.Button(filter_frame, text="Ingresos", command=lambda: listar_movimientos("ingreso")).pack(side=tk.LEFT, padx=5)
tk.Button(filter_frame, text="Gastos", command=lambda: listar_movimientos("gasto")).pack(side=tk.LEFT, padx=5)

# Tabla
columnas = ("ID", "Tipo", "Descripción", "Monto", "Fecha y Hora")

tree = ttk.Treeview(root, columns=columnas, show="headings")

for col in columnas:
    tree.heading(col, text=col)
    tree.column(col, anchor="center")

tree.pack(fill=tk.BOTH, expand=True, pady=10)


# Label de saldo total
label_total = tk.Label(root, text="Saldo Total: $0", bg="#1e1e2f", fg="white", font=("Arial", 12, "bold"))
label_total.pack(pady=10)


# Cargar datos al iniciar
def cargar_datos(filtro="Todos"):
    for fila in tree.get_children():
        tree.delete(fila)

    conexion = conectar_db()
    cursor = conexion.cursor()

    if filtro == "Ingresos":
        cursor.execute("SELECT * FROM movimientos WHERE tipo='ingreso'")
    elif filtro == "Gastos":
        cursor.execute("SELECT * FROM movimientos WHERE tipo='gasto'")
    else:
        cursor.execute("SELECT * FROM movimientos")

    resultados = cursor.fetchall()

    saldo = 0

    for fila in resultados:
        tree.insert("", tk.END, values=fila)

        if fila[1] == "ingreso":
            saldo += float(fila[3])
        else:
            saldo -= float(fila[3])

    label_total.config(text=f"Saldo Total: ${saldo:.2f}")

    conexion.close()

listar_movimientos()

root.mainloop()