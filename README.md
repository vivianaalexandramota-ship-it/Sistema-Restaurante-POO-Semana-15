# Sistema Restaurante POO - Semana 15

## Propósito
Esta versión corresponde a la Semana 15 de Programación Orientada a Objetos. Continúa la aplicación gráfica desarrollada en semanas anteriores y conserva la arquitectura modular, el inicio de sesión, la consulta de usuarios y la gestión de productos. La evolución principal es la incorporación de la sección **Ventas** para evidenciar los fundamentos básicos del manejo de eventos en Tkinter.

## Evolución de la Semana 15
Se añadió el modelo `Venta`, el archivo `ventas.json` y una sección de ventas dentro de la interfaz principal. Una venta relaciona un usuario registrado con un producto existente y guarda la fecha de la operación.

El flujo implementado es:

`acción del usuario → botón con command= → callback → RestauranteServicio → ventas.json → actualización visual`

La interfaz obtiene las selecciones y coordina la operación, mientras que las validaciones y la persistencia permanecen dentro de `RestauranteServicio`.

## Estructura

```text
restaurante_app/
├── datos/
│   ├── productos.json
│   ├── usuarios.json
│   └── ventas.json
├── modelos/
│   ├── __init__.py
│   ├── producto.py
│   ├── usuario.py
│   └── venta.py
├── servicios/
│   ├── __init__.py
│   ├── archivo_servicio.py
│   └── restaurante_servicio.py
├── ui/
│   ├── __init__.py
│   ├── login_view.py
│   └── main_view.py
├── assets/
│   ├── icon.png
│   └── logo.png
└── main.py
```

## Funciones disponibles
- Inicio de sesión mediante usuarios almacenados en `usuarios.json`.
- Consulta de usuarios en una tabla `Treeview`.
- Gestión de productos: registrar, consultar/cargar, actualizar y eliminar.
- Persistencia de productos mediante `productos.json`.
- Selección de usuario y producto mediante `ttk.Combobox`.
- Registro de una venta mediante el botón **Registrar venta** asociado con `command=`.
- Callback de venta que delega la operación a `RestauranteServicio`.
- Persistencia de ventas en `ventas.json`.
- Presentación y actualización inmediata de ventas en una tabla `Treeview`.
- Recursos visuales cargados desde la carpeta obligatoria `assets/`.

## Ejecución
1. Tener instalado Python 3.
2. Abrir una terminal en la carpeta `restaurante_app`.
3. Ejecutar:

```bash
python main.py
```

Credenciales de prueba:
- Usuario: `admin`
- Contraseña: `1234`

También está disponible:
- Usuario: `viviana`
- Contraseña: `2026`

No se utilizan librerías externas para la aplicación; Tkinter forma parte de la instalación estándar de Python.
