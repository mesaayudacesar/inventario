# Sistema de Inventario de Activos (Django + SQLite + Render)

## Descripción del Proyecto

Este proyecto es un sistema web responsive de inventario de máquinas PDA, diseñado para operar en línea con usuarios autenticados, roles y trazabilidad completa mediante historial de cambios.

El objetivo es permitir:
- Registrar activos que entran a bodega.
- Asignarlos a un usuario final.
- Consultarlos según permisos.
- Mantener un historial de movimientos.
- Exportar los datos en Excel.
- Administrar usuarios y roles.

Está construido con Django, usando SQLite como base de datos (ideal para Render Free) y Bootstrap para la interfaz.

## Características Principales

### 1. Sistema de Roles

El sistema tiene 4 roles principales:

| Rol          | Descripción |
|--------------|-------------|
| Administrador | Control total del sistema. CRUD completo, crea usuarios, modifica roles, exporta datos. |
| Consulta     | Solo puede leer información. No crea ni edita nada. |
| Bodega       | Registra activos nuevos y edita datos relacionados con ingreso a bodega. |
| Asignador    | Asigna los activos a usuarios, llena campos de asignación. |

Cada rol tiene permisos basados en los campos que debe manipular.

### 2. Gestión de Activos

Los activos tienen la siguiente información:

- ITEM (consecutivo)
- DOCUMENTO
- NOMBRES Y APELLIDOS
- IMEI 1
- IMEI 2 (opcional)
- S/N
- MAC SUPERFLEX
- ARTÍCULO (defecto: MAQUINA)
- MARCA (opciones: SUNMI V1 / SUNMI V2 / SUNMI V2 PRO / N910 / NEWLAND GRIS)
- ACTIVO
- CARGO (defecto: vendedor ambulante)
- ESTADO (defecto: activo confirmado)
- FECHA DE CONFIRMACIÓN (defecto: hoy)
- RESPONSABLE
- IDENTIFICACIÓN
- ZONA (defecto: Valledupar)
- OBSERVACIÓN (defecto: VERIFICADO)
- PUNTO DE VENTA
- CÓDIGO CENTRO DE COSTO
- CENTRO DE COSTO PUNTO
- FECHA DE SALIDA DE BODEGA

### 3. Historial de Cambios

El sistema registra cada cambio realizado sobre un activo:
- Qué usuario realizó la acción
- Antes y después del cambio
- Fecha y hora
- Tipo de acción (creación, edición, asignación, cambio de estado, etc.)

### 4. Exportación a Excel

El sistema permite exportar el inventario completo o filtrado usando:
- django-import-export, o
- Exportación personalizada en openpyxl.

### 5. Panel Admin

Django Admin está habilitado para el rol Administrador, con:
- CRUD de activos
- CRUD de usuarios
- Gestión de roles (grupos)
- Exportación

## Estructura del Proyecto

```
inventario_pda/
│
├── activos/                # App principal
│   ├── models.py           # Modelos: Activo, Historial
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   ├── admin.py
│   └── templates/
│
├── usuarios/               # App para roles y permisos
│   ├── models.py
│   ├── signals.py
│
├── settings.py
├── urls.py
├── requirements.txt
└── Procfile                # Para Render
```

## Modelos

### Tabla: Activo

| Campo               | Tipo             | Quién lo llena         | Default              |
|---------------------|------------------|------------------------|----------------------|
| item                | Integer (auto)   | Automático             | consecutivo          |
| documento           | CharField        | Asignador              | —                    |
| nombres_apellidos   | CharField        | Asignador              | —                    |
| imei1               | CharField        | Bodega / Admin         | —                    |
| imei2               | CharField (null) | Bodega / Admin         | opcional             |
| sn                  | CharField        | Bodega                 | —                    |
| mac_superflex       | CharField        | Asignador/Admin        | —                    |
| articulo            | CharField        | Sistema                | "MAQUINA"            |
| marca               | ChoiceField      | Bodega/Asignador/Admin | (5 opciones)         |
| activo              | CharField        | Bodega                 | —                    |
| cargo               | CharField        | Asignador              | "vendedor ambulante" |
| estado              | CharField        | Bodega/Admin           | "activo confirmado"  |
| fecha_confirmacion  | DateField        | Sistema                | hoy                  |
| responsable         | CharField        | Bodega                 | —                    |
| identificacion      | CharField        | Bodega                 | —                    |
| zona                | CharField        | Sistema                | "Valledupar"         |
| observacion         | TextField        | Sistema                | "VERIFICADO"         |
| punto_venta         | CharField        | Asignador              | —                    |
| codigo_centro_costo | CharField        | Asignador              | —                    |
| centro_costo_punto  | CharField        | Asignador              | —                    |
| fecha_salida_bodega | DateField        | Bodega                 | —                    |
| fecha_creacion      | DateTime         | Sistema                | auto                 |
| fecha_modificacion  | DateTime         | Sistema                | auto                 |

### Tabla: Historial

Registra todos los cambios a activos.

| Campo          | Tipo      |
|----------------|-----------|
| activo (FK)    | Activo    |
| usuario        | Usuario   |
| campo_cambiado | CharField |
| valor_anterior | Text      |
| valor_nuevo    | Text      |
| fecha          | DateTime  |

### Tabla: Usuario / Roles

Usa grupos de Django:

Grupos:
- Administrador
- Consulta
- Bodega
- Asignador

Cada grupo tendrá permisos específicos sobre:
- Crear
- Editar
- Asignar
- Consultar
- Exportar

## Instalación y Ejecución Local

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Despliegue en Render

1. Subir el proyecto a GitHub
2. Crear servicio Web Service → "Deploy from repo"
3. En Build Command:
   ```
   pip install -r requirements.txt
   ```
4. En Start Command:
   ```
   gunicorn inventario_pda.wsgi
   ```
5. Añadir variable:
   ```
   PYTHON_VERSION = 3.10
   ```

## Soporte y Mejoras Futuras

- API REST para apps móviles.
- Dashboard con gráficas.
- Módulo de generación de reportes Excel.
- Control de inventario de consumibles u otros equipos.
