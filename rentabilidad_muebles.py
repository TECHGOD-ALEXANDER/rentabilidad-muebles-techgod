import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
import io

# =================================================
# CONFIGURACIÓN
# =================================================
st.set_page_config(
    page_title="TECHGOD | Rentabilidad de Muebles",
    layout="centered"
)

st.markdown(
    "<style>body{background-color:#0b0f14;color:white;}</style>",
    unsafe_allow_html=True
)

# =================================================
# CONSTANTES
# =================================================
DESGASTE_PORC = 0.05
MARGEN_VENTA_RECOMENDADO = 0.50
MARGEN_VENTA_MAYOR = 0.45
GANANCIA_DIARIA_MIN = 80

# =================================================
# HEADER
# =================================================
st.title("Calculadora de Rentabilidad de Muebles")
st.write("Define precios y verifica si un trabajo conviene")

st.markdown("---")

# =================================================
# PRODUCCIÓN
# =================================================
st.subheader("Producción")

cantidad = st.number_input("Cantidad de muebles", min_value=1, value=1)
dias = st.number_input("Días totales de trabajo", min_value=1, value=1)

st.markdown("---")

# =================================================
# COSTOS
# =================================================
st.subheader("Costos de materiales")

melamina = st.number_input("Costo total de melamina (S/)", min_value=0.0)
accesorios = st.number_input("Costo total de accesorios (S/)", min_value=0.0)

st.markdown("---")

st.subheader("Mano de obra")

sueldo_diario = st.number_input(
    "Sueldo diario (S/) – usa 0 si no separas sueldo",
    min_value=0.0
)
mano_obra = sueldo_diario * dias

st.markdown("---")

st.subheader("Otros costos")

transporte = st.number_input("Transporte (S/)", min_value=0.0)
instalacion = st.number_input("Instalación (S/)", min_value=0.0)
extra = st.number_input("Otros gastos (S/)", min_value=0.0)

st.markdown("---")

# =================================================
# CÁLCULOS
# =================================================
desgaste = (melamina + accesorios) * DESGASTE_PORC

inversion_total = (
    melamina + accesorios + desgaste +
    transporte + instalacion + extra +
    mano_obra
)

inversion_por_mueble = inversion_total / cantidad

precio_recomendado = inversion_por_mueble * (1 + MARGEN_VENTA_RECOMENDADO)
precio_mayor = inversion_por_mueble * (1 + MARGEN_VENTA_MAYOR)

# =================================================
# PRECIO USADO
# =================================================
st.subheader("Precio de venta a usar")

modo_precio = st.radio(
    "",
    (
        "Usar precio de venta recomendado",
        "Definir precio por porcentaje",
        "Definir ganancia fija por mueble",
        "Ya tengo el precio de venta"
    )
)

if modo_precio == "Definir precio por porcentaje":
    porcentaje = st.number_input("Porcentaje de ganancia (%)", min_value=0.0, value=50.0)
    precio_usado = inversion_por_mueble * (1 + porcentaje / 100)

elif modo_precio == "Definir ganancia fija por mueble":
    ganancia_fija = st.number_input("Ganancia por mueble (S/)", min_value=0.0)
    precio_usado = inversion_por_mueble + ganancia_fija

elif modo_precio == "Ya tengo el precio de venta":
    precio_usado = st.number_input("Precio de venta por mueble (S/)", min_value=0.0)

else:
    precio_usado = precio_recomendado

st.markdown("---")

# =================================================
# RESULTADOS
# =================================================
ganancia_por_mueble = precio_usado - inversion_por_mueble
ganancia_total = ganancia_por_mueble * cantidad
ganancia_diaria = ganancia_total / dias

st.subheader("Resultados")

st.write(f"Inversión total: S/ {inversion_total:,.2f}")
st.write(f"Inversión por mueble: S/ {inversion_por_mueble:,.2f}")
st.write(f"Precio de venta recomendado: S/ {precio_recomendado:,.2f}")
st.write(f"Precio por mayor mínimo recomendado: S/ {precio_mayor:,.2f}")
st.write(f"Precio usado: S/ {precio_usado:,.2f}")
st.write(f"Ganancia por mueble: S/ {ganancia_por_mueble:,.2f}")
st.write(f"Ganancia total: S/ {ganancia_total:,.2f}")
st.write(f"Ganancia diaria: S/ {ganancia_diaria:,.2f}")

# =================================================
# EXPORTAR PDF
# =================================================
def generar_pdf():
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    content = []

    content.append(Paragraph("<b>REPORTE DE RENTABILIDAD - TECHGOD</b>", styles["Title"]))
    content.append(Paragraph(f"Inversión total: S/ {inversion_total:,.2f}", styles["Normal"]))
    content.append(Paragraph(f"Inversión por mueble: S/ {inversion_por_mueble:,.2f}", styles["Normal"]))
    content.append(Paragraph(f"Precio recomendado: S/ {precio_recomendado:,.2f}", styles["Normal"]))
    content.append(Paragraph(f"Precio por mayor recomendado: S/ {precio_mayor:,.2f}", styles["Normal"]))
    content.append(Paragraph(f"Precio usado: S/ {precio_usado:,.2f}", styles["Normal"]))
    content.append(Paragraph(f"Ganancia total: S/ {ganancia_total:,.2f}", styles["Normal"]))
    content.append(Paragraph(f"Ganancia diaria: S/ {ganancia_diaria:,.2f}", styles["Normal"]))
    content.append(Paragraph("<br/>Powered by TECHGOD", styles["Italic"]))

    doc.build(content)
    buffer.seek(0)
    return buffer

st.markdown("---")

st.subheader("Exportar")

pdf = generar_pdf()
st.download_button(
    label="📄 Exportar resultados en PDF",
    data=pdf,
    file_name="rentabilidad_muebles_techgod.pdf",
    mime="application/pdf"
)

st.markdown("---")
st.write("Powered by TECHGOD")
st.write("Built by TECHGOD")
