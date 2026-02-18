# prueba_tecnica

Sistema de control de inventarios construido con Django + Django REST Framework.

Incluye:
- GestiÃ³n de clientes (alta, ediciÃ³n, listado)
- GestiÃ³n de sucursales y almacenes ligados a clientes
- CatÃ¡logo de productos
- Movimientos de inventario (IN/OUT) con actualizaciÃ³n automÃ¡tica de stock
- GeneraciÃ³n de comprobante PDF por movimiento (stock antes/despuÃ©s)

## Stack tecnolÃ³gico

- Python 3.13+
- Django 5.x
- Django REST Framework
- SQLite (por defecto para la prueba tÃ©cnica)
- ReportLab (generaciÃ³n de PDF)
- Pytest + pytest-django (tests)

## Estructura del proyecto

- `config/`  
  Settings del proyecto y ruteo de URLs.
  - `config/settings/` settings divididos (`base.py`, `local.py`)
  - `config/api_urls.py` router central de DRF
  - `config/urls.py` redirect raÃ­z (`/` -> `/api/`) y serving de media (DEBUG)

- `apps/` (apps por dominio)
  - `apps/customers/` clientes
  - `apps/locations/` sucursales + almacenes
  - `apps/catalog/` productos
  - `apps/inventory/` stock + movimientos + generaciÃ³n de PDF

- `apps/*/models/` modelos del dominio
- `apps/*/api/` serializers + viewsets
- `apps/inventory/services/` lÃ³gica de negocio
  - `movements.py` registro atÃ³mico de movimientos + actualizaciÃ³n de stock + guardado de PDF
  - `pdfs.py` generador de bytes del PDF
  - `errors.py` errores propios del dominio

- `third_party/provided/`  
  Material proporcionado por la empresa (se conserva como referencia).

## InstalaciÃ³n (Windows / PowerShell)

Desde la raÃ­z del repo:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements/base.txt
pip install -r requirements/dev.txt

