import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path


class MainView(ttk.Frame):
    def __init__(self, master, servicio, usuario_actual, al_cerrar_sesion):
        super().__init__(master)
        self.servicio = servicio
        self.usuario_actual = usuario_actual
        self.al_cerrar_sesion = al_cerrar_sesion

        self.prod_id = tk.StringVar()
        self.prod_nombre = tk.StringVar()
        self.prod_categoria = tk.StringVar()
        self.prod_precio = tk.StringVar()
        self.prod_cantidad = tk.StringVar()

        self.venta_usuario = tk.StringVar()
        self.venta_producto = tk.StringVar()

        self._crear_interfaz()
        self._actualizar_todo()

    def _crear_interfaz(self):
        self.pack(fill="both", expand=True)

        encabezado = ttk.Frame(self, padding=(16, 10))
        encabezado.pack(fill="x")

        ruta_logo = Path(__file__).resolve().parents[1] / "assets" / "icon.png"
        self.icono = tk.PhotoImage(file=str(ruta_logo))
        ttk.Label(encabezado, image=self.icono).pack(side="left", padx=(0, 8))
        ttk.Label(encabezado, text="Restaurante App", style="Title.TLabel").pack(side="left")
        ttk.Label(
            encabezado,
            text=f"Sesión: {self.usuario_actual.nombre}",
        ).pack(side="right", padx=12)
        ttk.Button(encabezado, text="Cerrar sesión", command=self.al_cerrar_sesion).pack(side="right")

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=14, pady=(0, 14))

        self.tab_usuarios = ttk.Frame(self.notebook, padding=12)
        self.tab_productos = ttk.Frame(self.notebook, padding=12)
        self.tab_ventas = ttk.Frame(self.notebook, padding=12)

        self.notebook.add(self.tab_usuarios, text="Usuarios")
        self.notebook.add(self.tab_productos, text="Productos")
        self.notebook.add(self.tab_ventas, text="Ventas")

        self._crear_usuarios()
        self._crear_productos()
        self._crear_ventas()

    def _crear_usuarios(self):
        columnas = ("id", "nombre", "usuario", "rol")
        self.tabla_usuarios = ttk.Treeview(self.tab_usuarios, columns=columnas, show="headings", height=15)
        for col, titulo, ancho in [
            ("id", "ID", 90), ("nombre", "Nombre", 220), ("usuario", "Usuario", 150), ("rol", "Rol", 150)
        ]:
            self.tabla_usuarios.heading(col, text=titulo)
            self.tabla_usuarios.column(col, width=ancho, anchor="center")
        self.tabla_usuarios.pack(fill="both", expand=True)

    def _crear_productos(self):
        formulario = ttk.LabelFrame(self.tab_productos, text="Gestión de productos", padding=12)
        formulario.pack(fill="x", pady=(0, 10))

        campos = [
            ("ID", self.prod_id),
            ("Nombre", self.prod_nombre),
            ("Categoría", self.prod_categoria),
            ("Precio", self.prod_precio),
            ("Cantidad", self.prod_cantidad),
        ]
        for i, (texto, variable) in enumerate(campos):
            ttk.Label(formulario, text=texto).grid(row=0, column=i, padx=4, sticky="w")
            ttk.Entry(formulario, textvariable=variable, width=17).grid(row=1, column=i, padx=4, pady=4)

        acciones = ttk.Frame(formulario)
        acciones.grid(row=2, column=0, columnspan=5, sticky="w", pady=(8, 0))
        ttk.Button(acciones, text="Registrar", command=self._callback_registrar_producto).pack(side="left", padx=3)
        ttk.Button(acciones, text="Cargar/Consultar", command=self._callback_cargar_producto).pack(side="left", padx=3)
        ttk.Button(acciones, text="Actualizar", command=self._callback_actualizar_producto).pack(side="left", padx=3)
        ttk.Button(acciones, text="Eliminar", command=self._callback_eliminar_producto).pack(side="left", padx=3)
        ttk.Button(acciones, text="Limpiar", command=self._limpiar_producto).pack(side="left", padx=3)

        columnas = ("id", "nombre", "categoria", "precio", "cantidad")
        self.tabla_productos = ttk.Treeview(self.tab_productos, columns=columnas, show="headings", height=12)
        titulos = [("id","ID",80),("nombre","Nombre",220),("categoria","Categoría",160),
                   ("precio","Precio",100),("cantidad","Cantidad",100)]
        for col, titulo, ancho in titulos:
            self.tabla_productos.heading(col, text=titulo)
            self.tabla_productos.column(col, width=ancho, anchor="center")
        self.tabla_productos.pack(fill="both", expand=True)

    def _crear_ventas(self):
        panel = ttk.LabelFrame(self.tab_ventas, text="Registrar venta", padding=14)
        panel.pack(fill="x", pady=(0, 10))

        ttk.Label(panel, text="Usuario").grid(row=0, column=0, sticky="w", padx=5)
        ttk.Label(panel, text="Producto").grid(row=0, column=1, sticky="w", padx=5)

        self.combo_usuario = ttk.Combobox(panel, textvariable=self.venta_usuario, state="readonly", width=35)
        self.combo_producto = ttk.Combobox(panel, textvariable=self.venta_producto, state="readonly", width=40)
        self.combo_usuario.grid(row=1, column=0, padx=5, pady=5)
        self.combo_producto.grid(row=1, column=1, padx=5, pady=5)

        # Semana 15: command= -> callback -> servicio -> persistencia -> respuesta visual.
        ttk.Button(panel, text="Registrar venta", command=self._callback_registrar_venta).grid(
            row=1, column=2, padx=10, pady=5
        )

        columnas = ("id", "usuario", "producto", "fecha")
        self.tabla_ventas = ttk.Treeview(self.tab_ventas, columns=columnas, show="headings", height=15)
        for col, titulo, ancho in [
            ("id","ID",80), ("usuario","Usuario",210), ("producto","Producto",240), ("fecha","Fecha",170)
        ]:
            self.tabla_ventas.heading(col, text=titulo)
            self.tabla_ventas.column(col, width=ancho, anchor="center")
        self.tabla_ventas.pack(fill="both", expand=True)

    # ---------- Callbacks de productos ----------
    def _callback_registrar_producto(self):
        try:
            self.servicio.registrar_producto(
                self.prod_id.get(), self.prod_nombre.get(), self.prod_categoria.get(),
                self.prod_precio.get(), self.prod_cantidad.get()
            )
            self._actualizar_productos()
            self._actualizar_selectores_venta()
            self._limpiar_producto()
            messagebox.showinfo("Productos", "Producto registrado correctamente.")
        except ValueError as error:
            messagebox.showwarning("Productos", str(error))

    def _callback_cargar_producto(self):
        producto = self.servicio.buscar_producto(self.prod_id.get())
        if not producto:
            messagebox.showwarning("Productos", "No se encontró el producto indicado.")
            return
        self.prod_nombre.set(producto.nombre)
        self.prod_categoria.set(producto.categoria)
        self.prod_precio.set(str(producto.precio))
        self.prod_cantidad.set(str(producto.cantidad))

    def _callback_actualizar_producto(self):
        try:
            self.servicio.actualizar_producto(
                self.prod_id.get(), self.prod_nombre.get(), self.prod_categoria.get(),
                self.prod_precio.get(), self.prod_cantidad.get()
            )
            self._actualizar_productos()
            self._actualizar_selectores_venta()
            messagebox.showinfo("Productos", "Producto actualizado correctamente.")
        except ValueError as error:
            messagebox.showwarning("Productos", str(error))

    def _callback_eliminar_producto(self):
        try:
            self.servicio.eliminar_producto(self.prod_id.get())
            self._actualizar_productos()
            self._actualizar_selectores_venta()
            self._limpiar_producto()
            messagebox.showinfo("Productos", "Producto eliminado correctamente.")
        except ValueError as error:
            messagebox.showwarning("Productos", str(error))

    # ---------- Callback principal de Semana 15 ----------
    def _callback_registrar_venta(self):
        try:
            usuario_id = self._extraer_id(self.venta_usuario.get())
            producto_id = self._extraer_id(self.venta_producto.get())

            # La UI coordina; RestauranteServicio valida y persiste.
            venta = self.servicio.registrar_venta(usuario_id, producto_id)

            self._actualizar_ventas()
            self.venta_usuario.set("")
            self.venta_producto.set("")
            messagebox.showinfo("Ventas", f"Venta {venta.id} registrada correctamente.")
        except ValueError as error:
            messagebox.showwarning("Ventas", str(error))

    @staticmethod
    def _extraer_id(texto):
        if not texto or " - " not in texto:
            return ""
        return texto.split(" - ", 1)[0].strip()

    # ---------- Actualización visual ----------
    def _actualizar_todo(self):
        self._actualizar_usuarios()
        self._actualizar_productos()
        self._actualizar_selectores_venta()
        self._actualizar_ventas()

    def _actualizar_usuarios(self):
        self._vaciar(self.tabla_usuarios)
        for u in self.servicio.listar_usuarios():
            self.tabla_usuarios.insert("", "end", values=(u.id, u.nombre, u.usuario, u.rol))

    def _actualizar_productos(self):
        self._vaciar(self.tabla_productos)
        for p in self.servicio.listar_productos():
            self.tabla_productos.insert(
                "", "end", values=(p.id, p.nombre, p.categoria, f"${p.precio:.2f}", p.cantidad)
            )

    def _actualizar_selectores_venta(self):
        self.combo_usuario["values"] = [f"{u.id} - {u.nombre}" for u in self.servicio.listar_usuarios()]
        self.combo_producto["values"] = [f"{p.id} - {p.nombre}" for p in self.servicio.listar_productos()]

    def _actualizar_ventas(self):
        self._vaciar(self.tabla_ventas)
        for v in self.servicio.listar_ventas():
            self.tabla_ventas.insert("", "end", values=(v.id, v.usuario_nombre, v.producto_nombre, v.fecha))

    @staticmethod
    def _vaciar(tabla):
        for item in tabla.get_children():
            tabla.delete(item)

    def _limpiar_producto(self):
        for variable in [self.prod_id, self.prod_nombre, self.prod_categoria, self.prod_precio, self.prod_cantidad]:
            variable.set("")
