from datetime import datetime
from pathlib import Path

from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta
from servicios.archivo_servicio import ArchivoServicio


class RestauranteServicio:
    def __init__(self, carpeta_datos=None):
        base = Path(carpeta_datos) if carpeta_datos else Path(__file__).resolve().parents[1] / "datos"
        self.ruta_productos = base / "productos.json"
        self.ruta_usuarios = base / "usuarios.json"
        self.ruta_ventas = base / "ventas.json"

    # ---------- Usuarios ----------
    def listar_usuarios(self):
        return [Usuario(**dato) for dato in ArchivoServicio.leer_json(self.ruta_usuarios)]

    def validar_acceso(self, usuario, contrasena):
        usuario = usuario.strip()
        for item in self.listar_usuarios():
            if item.usuario == usuario and item.contrasena == contrasena:
                return item
        return None

    # ---------- Productos ----------
    def listar_productos(self):
        return [Producto(**dato) for dato in ArchivoServicio.leer_json(self.ruta_productos)]

    def buscar_producto(self, producto_id):
        producto_id = str(producto_id).strip()
        return next((p for p in self.listar_productos() if p.id == producto_id), None)

    def registrar_producto(self, producto_id, nombre, categoria, precio, cantidad):
        self._validar_producto(producto_id, nombre, categoria, precio, cantidad)
        if self.buscar_producto(producto_id):
            raise ValueError("Ya existe un producto con ese ID.")

        producto = Producto(producto_id, nombre, categoria, precio, cantidad)
        datos = [p.a_diccionario() for p in self.listar_productos()]
        datos.append(producto.a_diccionario())
        ArchivoServicio.guardar_json(self.ruta_productos, datos)
        return producto

    def actualizar_producto(self, producto_id, nombre, categoria, precio, cantidad):
        self._validar_producto(producto_id, nombre, categoria, precio, cantidad)
        productos = self.listar_productos()
        encontrado = False
        for i, producto in enumerate(productos):
            if producto.id == str(producto_id).strip():
                productos[i] = Producto(producto_id, nombre, categoria, precio, cantidad)
                encontrado = True
                break
        if not encontrado:
            raise ValueError("No se encontró el producto indicado.")
        ArchivoServicio.guardar_json(self.ruta_productos, [p.a_diccionario() for p in productos])
        return productos[i]

    def eliminar_producto(self, producto_id):
        producto_id = str(producto_id).strip()
        productos = self.listar_productos()
        nuevos = [p for p in productos if p.id != producto_id]
        if len(nuevos) == len(productos):
            raise ValueError("No se encontró el producto indicado.")
        ArchivoServicio.guardar_json(self.ruta_productos, [p.a_diccionario() for p in nuevos])

    @staticmethod
    def _validar_producto(producto_id, nombre, categoria, precio, cantidad):
        if not str(producto_id).strip() or not str(nombre).strip() or not str(categoria).strip():
            raise ValueError("Complete todos los datos del producto.")
        try:
            precio = float(precio)
            cantidad = int(cantidad)
        except (TypeError, ValueError):
            raise ValueError("Precio y cantidad deben ser valores numéricos.")
        if precio < 0 or cantidad < 0:
            raise ValueError("Precio y cantidad no pueden ser negativos.")

    # ---------- Ventas ----------
    def listar_ventas(self):
        return [Venta(**dato) for dato in ArchivoServicio.leer_json(self.ruta_ventas)]

    def registrar_venta(self, usuario_id, producto_id):
        usuario_id = str(usuario_id).strip()
        producto_id = str(producto_id).strip()

        usuario = next((u for u in self.listar_usuarios() if u.id == usuario_id), None)
        if not usuario:
            raise ValueError("Seleccione un usuario registrado.")

        producto = self.buscar_producto(producto_id)
        if not producto:
            raise ValueError("Seleccione un producto registrado.")

        ventas = self.listar_ventas()
        nuevo_id = f"V{len(ventas) + 1:03d}"
        venta = Venta(
            nuevo_id,
            usuario.id,
            usuario.nombre,
            producto.id,
            producto.nombre,
            datetime.now().strftime("%d/%m/%Y %H:%M"),
        )
        ventas.append(venta)
        ArchivoServicio.guardar_json(self.ruta_ventas, [v.a_diccionario() for v in ventas])
        return venta
