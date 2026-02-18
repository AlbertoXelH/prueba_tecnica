from io import BytesIO
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas

def build_movement_pdf(payload: dict) -> bytes:
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=LETTER)

    x = 72
    y = 720
    line = 18

    c.setFont("Helvetica-Bold", 14)
    c.drawString(x, y, "Comprobante de Movimiento")
    y -= line * 2

    c.setFont("Helvetica", 11)
    rows = [
        ("Tipo", payload["movement_type"]),
        ("Fecha", payload["date"]),
        ("Producto", payload["product"]),
        ("Cantidad", str(payload["quantity"])),
        ("Almacén", payload["warehouse"]),
        ("Stock antes", str(payload["stock_before"])),
        ("Stock después", str(payload["stock_after"])),
    ]

    for label, value in rows:
        c.setFont("Helvetica-Bold", 11)
        c.drawString(x, y, f"{label}:")
        c.setFont("Helvetica", 11)
        c.drawString(x + 120, y, value)
        y -= line

    c.showPage()
    c.save()

    buffer.seek(0)
    return buffer.read()
