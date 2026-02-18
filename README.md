# prueba_tecnica

Sistema de control de inventarios construido con Django + Django REST Framework.

Incluye:
- Gestión de clientes (alta, edición, listado)
- Gestión de sucursales y almacenes ligados a clientes
- Catálogo de productos
- Movimientos de inventario (IN/OUT) con actualización automática de stock
- Generación de comprobante PDF por movimiento (stock antes/después)

## Stack tecnológico

- Python 3.13+
- Django 5.x
- Django REST Framework
- SQLite (por defecto para la prueba técnica)
- ReportLab (generación de PDF)
- Pytest + pytest-django (tests)

## Estructura del proyecto

- `config/`  
  Settings del proyecto y ruteo de URLs.
  - `config/settings/` settings divididos (`base.py`, `local.py`)
  - `config/api_urls.py` router central de DRF
  - `config/urls.py` redirect raíz (`/` -> `/api/`) y serving de media (DEBUG)

- `apps/` (apps por dominio)
  - `apps/customers/` clientes
  - `apps/locations/` sucursales + almacenes
  - `apps/catalog/` productos
  - `apps/inventory/` stock + movimientos + generación de PDF

- `apps/*/models/` modelos del dominio
- `apps/*/api/` serializers + viewsets
- `apps/inventory/services/` lógica de negocio
  - `movements.py` registro atómico de movimientos + actualización de stock + guardado de PDF
  - `pdfs.py` generador de bytes del PDF
  - `errors.py` errores propios del dominio

- `third_party/provided/`  
  Material proporcionado por la empresa (se conserva como referencia).

## Instalación (Windows / PowerShell)

Desde la raíz del repo:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements/base.txt
pip install -r requirements/dev.txt

## PDF (comprobante por movimiento)

- Descarga directa: `GET /api/movements/{uuid}/pdf/`
- Alternativa: el campo `pdf_url` del movimiento apunta al archivo en `/media/...`

El PDF incluye: tipo de movimiento, fecha, producto, cantidad, almacén y stock antes/después.
