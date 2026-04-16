import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Cotizador Transporte", layout="centered")

st.title("🚛 Cotizador de Transporte Terrestre")

# -------------------------
# Catálogo de unidades
# -------------------------
unidades = {
    "Camioneta 3.5 ton": {"capacidad": 3.5, "precio_min": 3500, "precio_max": 4800},
    "Camioneta 5.5 ton": {"capacidad": 5.5, "precio_min": 5000, "precio_max": 6500},
    "Camión 8 ton": {"capacidad": 8, "precio_min": 7000, "precio_max": 9500},
    "Camión 16 ton": {"capacidad": 16, "precio_min": 11000, "precio_max": 14500},
    "Tractocamión": {"capacidad": 30, "precio_min": 18000, "precio_max": 24000},
    "Doble remolque": {"capacidad": 60, "precio_min": 28000, "precio_max": 38000},
}

# -------------------------
# Selección de unidad
# -------------------------
tipo = st.selectbox("Tipo de unidad", list(unidades.keys()))
data = unidades[tipo]

st.write(f"Capacidad máxima: {data['capacidad']} ton")

# -------------------------
# Tipo de carga
# -------------------------
tipo_carga = st.radio("Tipo de carga", ["FCL (carga completa)", "LTL (carga parcial)"])

# -------------------------
# Entrada de carga
# -------------------------
modo_calculo = st.radio("¿Cómo deseas cotizar?", ["Por peso (toneladas)", "Por volumen (m3)"])

if modo_calculo == "Por peso (toneladas)":
    carga = st.number_input("Carga en toneladas", min_value=0.1, value=1.0)
else:
    volumen = st.number_input("Volumen (m3)", min_value=0.1, value=1.0)
    factor_conversion = st.number_input("Factor ton/m3", value=0.25)
    carga = volumen * factor_conversion

# Validación de capacidad
if carga > data["capacidad"]:
    st.warning("⚠️ La carga excede la capacidad del vehículo")

# -------------------------
# Variables de operación
# -------------------------
distancia = st.number_input("Distancia (km)", min_value=1, value=100)

precio_diesel = st.number_input("Precio diésel", value=24.0)
rendimiento = st.number_input("Rendimiento km/l", value=4.0)

sueldo_operador = st.number_input("Sueldo operador", value=1500)
casetas = st.number_input("Casetas", value=1000)
mantenimiento = st.number_input("Mantenimiento", value=800)
otros = st.number_input("Otros costos", value=500)

utilidad = st.slider("Utilidad (%)", 0, 100, 30)
costos_fijos = st.number_input("Costos fijos", value=20000)

# -------------------------
# Cálculos
# -------------------------
combustible = (distancia / rendimiento) * precio_diesel

costo_operacion = combustible + sueldo_operador + casetas + mantenimiento + otros

# Ajuste por tipo de carga
if tipo_carga == "LTL (carga parcial)":
    factor_ocupacion = carga / data["capacidad"]
    costo_operacion = costo_operacion * factor_ocupacion

precio_venta = costo_operacion * (1 + utilidad / 100)
margen = precio_venta - costo_operacion

# Punto de equilibrio
if margen > 0:
    punto_equilibrio = costos_fijos / margen
else:
    punto_equilibrio = 0

# -------------------------
# Resultados
# -------------------------
st.subheader("📊 Resultados")

st.write(f"⛽ Combustible: ${combustible:,.2f}")
st.write(f"💰 Costo de operación: ${costo_operacion:,.2f}")
st.write(f"📦 Precio de venta: ${precio_venta:,.2f}")
st.write(f"📈 Margen: ${margen:,.2f}")
st.write(f"⚖️ Punto de equilibrio: {punto_equilibrio:.2f} viajes")

# -------------------------
# Gráfica de punto de equilibrio
# -------------------------
st.subheader("📉 Gráfica de Punto de Equilibrio")

viajes = np.arange(0, int(punto_equilibrio * 2) + 1)

ingresos = viajes * precio_venta
costos_totales = costos_fijos + (viajes * costo_operacion)

fig, ax = plt.subplots()
ax.plot(viajes, ingresos, label="Ingresos")
ax.plot(viajes, costos_totales, label="Costos totales")

ax.axvline(punto_equilibrio, linestyle="--")
ax.set_xlabel("Número de viajes")
ax.set_ylabel("Dinero")

ax.legend()

st.pyplot(fig)