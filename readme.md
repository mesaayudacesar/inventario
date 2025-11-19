# Sistema de Inventario de Activos PDA (Django + SQLite + Bootstrap)

## Descripción del Proyecto

Este proyecto es un sistema web responsive de inventario de máquinas PDA, diseñado para operar en línea con usuarios autenticados, roles y trazabilidad completa mediante historial de cambios.

El objetivo es permitir:
- Registrar activos que entran a bodega.
- Asignarlos a un usuario final.
- Consultarlos según permisos.
- Mantener un historial de movimientos.
- Exportar los datos en Excel.
- Administrar usuarios, categorías y ubicaciones.
SQLite
Está construido con Django 5.2, usando  como base de datos, Bootstrap 5 para la interfaz y FontAwesome para iconos.

## Flujo del Aplicativo

### 1. Autenticación y Roles
- **Login**: Los usuarios inician sesión en `/` (usuarios/login.html).
- **Redirección Automática**: Después del login, el sistema redirige según el grupo del usuario:
  - **Admin**: `/activos/admin-dashboard/` (Panel administrativo completo).
  - **Logística**: `/activos/logistica-dashboard/` (Dashboard de logística).
  - **Lectura**: `/activos/lectura-dashboard/` (Dashboard de solo lectura).
  - **Sin grupo**: `/activos/` (Lista de activos).
- **Logout**: Cierra sesión y redirige a login.

### 2. Paneles por Rol
- **Admin Dashboard**: Muestra estadísticas (total activos, asignados, en bodega, dados de baja) y enlaces a todas las funcionalidades: gestión de activos, usuarios, categorías, ubicaciones, movimientos y reportes.
- **Logística Dashboard**: Estadísticas de activos por estado y movimientos recientes.
- **Lectura Dashboard**: Solo muestra el total de activos.

### 3. Gestión de Activos
- **Lista de Activos**: Vista principal en `/activos/` (home.html).
- **CRUD Activos**: Crear, ver detalle, editar, eliminar activos (solo Admin para crear/eliminar).
- **Movimientos**: Registrar movimientos de activos (ingreso, salida, transferencia, cambio de estado).
- **Historial**: Ver historial de cambios por activo.

### 4. Gestión Administrativa (Solo Admin)
- **Usuarios**: Listar, crear, editar, resetear contraseña de usuarios.
- **Categorías**: CRUD de categorías de activos.
- **Ubicaciones**: CRUD de ubicaciones (sedes, bodegas, etc.).
- **Reportes**: Inventario por sede, exportar a Excel.

### 5. Navegación
- **Sidebar**: Barra lateral con enlaces según permisos del usuario.
- **Base Template**: Plantilla base con navegación, mensajes de Django y estilos Bootstrap.

## Características Principales

### 1. Sistema de Roles

El sistema tiene 3 roles principales (grupos de Django):

| Rol          | Descripción | Dashboard |
|--------------|-------------|-----------|
| Admin        | Control total: CRUD activos, usuarios, categorías, ubicaciones, movimientos, reportes. | admin_dashboard.html |
| Logística    | Gestiona movimientos y estados de activos. | logistica_dashboard.html |
| Lectura      | Solo lectura de activos. | lectura_dashboard.html |

Permisos basados en grupos, con decoradores `@login_required` y checks de grupo en vistas.

### 2. Modelos de Datos

#### Activo
Campos principales: item (auto), documento, nombres_apellidos, imei1, imei2, sn, mac_superflex, articulo, marca (choices), activo, cargo, estado, fecha_confirmacion, responsable, identificacion, zona, ubicacion (FK), articulo_fk (FK), observacion, punto_venta, codigo_centro_costo, centro_costo_punto, fecha_salida_bodega.

#### Movimiento
Registra movimientos: tipo (ingreso/salida/transferencia/cambio_estado), activo, usuario, ubicaciones origen/destino, estados anterior/nuevo, descripcion, fecha.

#### Historial
Auditoría: activo, usuario, campo_cambiado, valor_anterior, valor_nuevo, fecha.

#### Ubicacion, Categoria, Articulo
Modelos auxiliares para clasificar activos.

### 3. Exportación y Reportes
- **Exportar Excel**: Descarga completa del inventario en XLSX usando openpyxl.
- **Reporte por Sede**: Filtrar activos por ubicación.
- **CSV**: Opción adicional para exportar.

### 4. Interfaz de Usuario
- **Responsive**: Bootstrap 5 con sidebar fija y contenido desplazable.
- **Iconos**: FontAwesome para navegación.
- **Mensajes**: Alertas de Django para feedback.
- **Context Processor**: Variables globales para grupos de usuario en templates.

## Estructura del Proyecto

```
inventario_pda/
│
├── activos/                # App principal
│   ├── models.py           # Modelos: Activo, Movimiento, Historial, Ubicacion, Categoria, Articulo
│   ├── views.py            # Vistas: CRUD Activos, Dashboards, Movimientos, etc.
│   ├── urls.py             # URLs: home, admin_dashboard, CRUDs, etc.
│   ├── admin.py            # Django Admin
│   └── templates/activos/  # Templates: home.html, admin_dashboard.html, etc.
│
├── usuarios/               # App de usuarios
│   ├── models.py           # Sin modelos adicionales (usa User de Django)
│   ├── views.py            # CustomLoginView, user_list, user_create, etc.
│   ├── urls.py             # login, logout, user management
│   └── templates/usuarios/ # login.html, user_list.html, etc.
│
├── inventario_pda/         # Configuración principal
│   ├── settings.py         # Config: INSTALLED_APPS, TEMPLATES, LOGIN_REDIRECT_URL, etc.
│   ├── urls.py             # Include activos.urls, usuarios.urls
│   ├── context_processors.py # user_groups para templates
│   ├── wsgi.py
│   └── asgi.py
│
├── templates/              # Templates globales
│   └── base.html           # Template base con sidebar
│
├── static/                 # Archivos estáticos (CSS, JS, imágenes)
├── requirements.txt        # Dependencias: Django, openpyxl, gunicorn
├── manage.py
├── db.sqlite3              # Base de datos
└── README.md
```

## Instalación y Ejecución Local

```bash
# Clonar repositorio
git clone <repo-url>
cd inventario_pda

# Instalar dependencias
pip install -r requirements.txt

# Migrar base de datos
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Ejecutar servidor
python manage.py runserver
```

Acceder a http://127.0.0.1:8000/

## Despliegue en Render

1. Subir el proyecto a GitHub.
2. Crear servicio Web Service en Render → "Deploy from repo".
3. **Build Command**:
   ```
   pip install -r requirements.txt
   ```
4. **Start Command**:
   ```
   gunicorn inventario_pda.wsgi
   ```
5. Variables de entorno:
   ```
   PYTHON_VERSION = 3.10
   DJANGO_SETTINGS_MODULE = inventario_pda.settings
   SECRET_KEY = <tu-secret-key>
   DEBUG = False
   ```

## Tecnologías Utilizadas

- **Backend**: Django 5.2 (Python 3.10)
- **Base de Datos**: SQLite
- **Frontend**: Bootstrap 5, FontAwesome, HTML5
- **Exportación**: openpyxl
- **Despliegue**: Render (gratuito)

## Mejoras Futuras

- API REST para integración móvil.
- Dashboards con gráficas (Chart.js).
- Más tipos de reportes.
- Notificaciones por email.
- Control de inventario de consumibles.
