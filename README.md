# Inventory Control (Django)

Sistema de control de inventarios con:
- Clientes, sucursales, almacenes
- Productos y control de stock por almacén
- Movimientos de ingreso/egreso con validación de stock
- Generación de comprobante PDF por movimiento

## Stack
- Django
- Django REST Framework
- ReportLab (PDF)

## Setup (local)
```bash
python -m venv .venv
# activar entorno
python -m pip install -r requirements/dev.txt
python manage.py migrate
python manage.py runserver


---

### 3) Instalar dependencias
```bash
python -m pip install -r requirements/dev.txt
