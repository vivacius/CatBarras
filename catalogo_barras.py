import streamlit as st
import pandas as pd
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from PIL import Image

# Configuración del estilo del código de barras
writer_options = {
    'write_text': True,
    'font_size': 8,
    'text_distance': 6,
    'module_height': 20.0,
    'dpi': 300
}

# Función para cargar datos según el tipo
@st.cache_data
def cargar_datos(tipo):
    if tipo == "Producto Terminado":
        return pd.read_excel("Productos_barras.xlsx")
    else:
        return pd.read_excel("productos_sin_terminar_resumidos.xlsx")

# Selector para tipo de producto
tipo_producto = st.radio(
    "Seleccione el tipo de producto:",
    ("Producto Terminado", "Producto Sin Terminar")
)

# Cargar datos según selección
df = cargar_datos(tipo_producto)

# Título
st.title("📦 Buscador de Códigos de Barras")

# Campo de búsqueda
consulta = st.text_input("🔍 Escribe parte del nombre del producto...").upper()

# Filtrar coincidencias
resultados = df[df["Referencia_general"].str.contains(consulta, na=False)]

if not resultados.empty:
    producto = st.selectbox("Selecciona un producto", resultados["Referencia_general"])

    # Extraer la fila correspondiente
    fila = resultados[resultados["Referencia_general"] == producto].iloc[0]
    codigo = str(fila["Codigo_Barras"])
    detalle = fila["Detalle_Original"]

    # Mostrar detalles
    st.subheader("📝 Detalle del producto")
    st.write(f"**Código de barras:** {codigo}")
    st.write(f"**Detalle original:** {detalle}")

    # Generar imagen del código de barras (Code128)
    try:
        buffer = BytesIO()
        code128 = barcode.get_barcode_class('code128')
        barcode_obj = code128(codigo, writer=ImageWriter())
        barcode_obj.write(buffer, options=writer_options)
        buffer.seek(0)

        st.image(
            Image.open(buffer),
            caption="📸 Código de barras generado",
            use_container_width=False,
            width=300
        )
    except Exception as e:
        st.error(f"❌ Error al generar el código de barras: {e}")

else:
    st.info("Escribe al menos una palabra del nombre del producto.")
