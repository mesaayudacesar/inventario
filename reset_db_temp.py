# Script temporal para recrear la base de datos
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventario_pda.settings')
django.setup()

from django.db import connections
from django.db.utils import OperationalError

# Cerrar todas las conexiones
for conn in connections.all():
    try:
        conn.close()
    except:
        pass

# Eliminar el archivo
import time
time.sleep(1)

db_path = 'db.sqlite3'
if os.path.exists(db_path):
    try:
        os.remove(db_path)
        print(f"✓ Base de datos eliminada: {db_path}")
    except Exception as e:
        print(f"✗ Error al eliminar: {e}")
        sys.exit(1)
else:
    print("✓ La base de datos no existe")

print("✓ Listo para ejecutar migraciones")
