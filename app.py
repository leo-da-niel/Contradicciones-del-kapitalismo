import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("Simulador extendido de tensiones distributivas")

# Número de sectores
n = st.slider("Número de sectores", min_value=2, max_value=6, value=3)

st.subheader("Matriz de producción A")
A = np.zeros((n, n))
for i in range(n):
    for j in range(n):
        A[i][j] = st.number_input(f"A[{i}][{j}]", value=0.1, key=f"A_{i}_{j}")

st.subheader("Trabajo directo por unidad (l)")
l = np.zeros(n)
for i in range(n):
    l[i] = st.number_input(f"l[{i}]", value=1.0, key=f"l_{i}")

# Política: salario mínimo
st.subheader("Política de salario mínimo")
w_min = st.slider("Salario mínimo", 0.0, 1.0, 0.2)

# Simulación
r_values = np.linspace(0, 1, 100)
w_values = []
validity = []

for r in r_values:
    p = np.ones(n)
    cost = p @ A * (1 + r)
    w = (p - cost).mean()
    w_values.append(w)
    if w >= w_min and all(p - cost > 0):
        validity.append(1)
    else:
        validity.append(0)

# Visualización
fig, ax = plt.subplots()
ax.plot(r_values, w_values, label='Salario promedio w(r)')
ax.fill_between(r_values, 0, 1, where=np.array(validity)==0, color='red', alpha=0.3, label='Obstrucción')
ax.axhline(w_min, color='gray', linestyle='--', label='Salario mínimo')
ax.set_xlabel('Tasa de beneficio r')
ax.set_ylabel('Salario promedio w')
ax.set_title('Tensiones distributivas en economía multissectorial')
ax.legend()
st.pyplot(fig)

# Diagnóstico
if any(np.array(validity) == 0):
    st.warning("⚠️ Se detectan obstrucciones distributivas: no se puede ensamblar una estructura económica global coherente en todo el intervalo.")
else:
    st.success("✅ No se detectan obstrucciones: la estructura económica es globalmente viable.")
