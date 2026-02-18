# prueba_tecnica

Sistema de control de inventarios construido con **Django + Django REST Framework**, con una **UI web (HTML + Bootstrap)** para operar como usuario.

Incluye:
- **Clientes** (CRUD)
- **Sucursales** (CRUD) vinculadas a cliente
- **Almacenes** (CRUD) vinculados a sucursal (y por lo tanto a cliente)
- **Productos** (CRUD) vinculados a cliente (**SKU único por cliente**)
- **Movimientos de inventario** (IN/OUT) con actualización automática de stock
- **Comprobante PDF** por movimiento

---

## Reglas de negocio clave

### Productos por cliente
- Cada **Producto pertenece a un Cliente**.
- El **SKU es único por cliente** (puedes repetir SKU entre clientes diferentes, pero no dentro del mismo).

### Stock inicial automático (quantity = 0)
Se crean registros de stock en 0 de forma automática mediante **signals**:

- Al crear un **Producto**, se crea `Stock(quantity=0)` para **todos los almacenes** de ese cliente.
- Al crear un **Almacén**, se crea `Stock(quantity=0)` para **todos los productos** del cliente dueño de la sucursal.

Esto garantiza que siempre exista un Stock para la combinación `almacén + producto`.

---

## Stack tecnológico

- Python 3.13+
- Django 5.x
- Django REST Framework
- SQLite (por defecto)
- ReportLab (generación de PDF)
- Pytest + pytest-django (tests)

---

## Estructura del proyecto

- `config/`
  - settings del proyecto (`config/settings/`)
  - ruteo principal (`config/urls.py`)
  - ruteo API central (`config/api_urls.py`)

- `apps/` (apps por dominio)
  - `apps/customers/` clientes
  - `apps/locations/` sucursales + almacenes
  - `apps/catalog/` productos
  - `apps/inventory/` stock + movimientos + PDF + signals
  - `apps/ui/` UI web (templates Bootstrap)

- `apps/inventory/services/`
  - `movements.py`: registro atómico de movimientos + actualización de stock + guardado de PDF
  - `pdfs.py`: generador de bytes del PDF
  - `errors.py`: errores del dominio

- `scripts/`
  - scripts utilitarios (ej. `seed_data.py` para datos de prueba)

---

## Instalación (Windows / PowerShell)

Desde la raíz del repo:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements/base.txt
pip install -r requirements/dev.txt
