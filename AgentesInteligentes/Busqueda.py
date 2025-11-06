import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

# --- CREAR EL GRAFO DEL MAPA DE ECUADOR ---
G = nx.Graph()

# Ciudades principales
ciudades = [
    "Quito", "Guayaquil", "Cuenca", "Ambato", "Loja", "Manta",
    "Esmeraldas", "Santo Domingo", "Portoviejo", "Machala",
    "Ibarra", "Tulcán", "Riobamba", "Babahoyo", "Latacunga",
    "Quevedo", "Tena", "Puyo"
]

conexiones = [
    ("Quito", "Ibarra", 115),
    ("Ibarra", "Tulcán", 125),
    ("Quito", "Latacunga", 90),
    ("Latacunga", "Ambato", 45),
    ("Ambato", "Riobamba", 55),
    ("Riobamba", "Cuenca", 250),
    ("Cuenca", "Loja", 215),
    ("Guayaquil", "Cuenca", 197),
    ("Guayaquil", "Machala", 180),
    ("Guayaquil", "Babahoyo", 70),
    ("Babahoyo", "Quevedo", 90),
    ("Quevedo", "Santo Domingo", 120),
    ("Santo Domingo", "Quito", 150),
    ("Santo Domingo", "Manta", 180),
    ("Manta", "Portoviejo", 40),
    ("Portoviejo", "Quevedo", 150),
    ("Quito", "Tena", 190),
    ("Tena", "Puyo", 120)
]

G.add_weighted_edges_from(conexiones)

# --- FUNCIONES DE BÚSQUEDA ---
def bfs(start, goal):
    queue = [[start]]
    visited = set()
    while queue:
        path = queue.pop(0)
        node = path[-1]
        if node == goal:
            return path, len(visited)
        if node not in visited:
            visited.add(node)
            for neighbor in G.neighbors(node):
                new_path = list(path)
                new_path.append(neighbor)
                queue.append(new_path)
    return None, len(visited)

def dfs(start, goal):
    stack = [[start]]
    visited = set()
    while stack:
        path = stack.pop()
        node = path[-1]
        if node == goal:
            return path, len(visited)
        if node not in visited:
            visited.add(node)
            for neighbor in G.neighbors(node):
                new_path = list(path)
                new_path.append(neighbor)
                stack.append(new_path)
    return None, len(visited)

def ucs(start, goal):
    queue = [(0, [start])]
    visited = set()
    while queue:
        queue.sort(key=lambda x: x[0])
        cost, path = queue.pop(0)
        node = path[-1]
        if node == goal:
            return path, cost, len(visited)
        if node not in visited:
            visited.add(node)
            for neighbor in G.neighbors(node):
                new_cost = cost + G[node][neighbor]['weight']
                new_path = list(path)
                new_path.append(neighbor)
                queue.append((new_cost, new_path))
    return None, 0, len(visited)

def iddfs(start, goal, max_depth=5):
    def dls(node, goal, depth, visited):
        if depth == 0 and node == goal:
            return [node]
        if depth > 0:
            for neighbor in G.neighbors(node):
                if neighbor not in visited:
                    path = dls(neighbor, goal, depth-1, visited | {neighbor})
                    if path:
                        return [node] + path
        return None

    for depth in range(max_depth + 1):
        path = dls(start, goal, depth, {start})
        if path:
            return path, depth
    return None, max_depth

# --- DISEÑO DE LA APP STREAMLIT ---
st.set_page_config(page_title="Algoritmos de Búsqueda - Ecuador", layout="wide")

# --- ESTILOS ---
st.markdown("""
<style>
.title {
    text-align: center;
    color: #0E6655;
    font-size: 38px;
    font-weight: bold;
    margin-bottom: 10px;
}
.subtitle {
    text-align: center;
    color: #1B4F72;
    font-size: 18px;
    margin-bottom: 25px;
}
.info-box {
    background-color: #E8F8F5;
    border-left: 6px solid #117864;
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 20px;
    box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
}
.algorithm-card {
    background-color: #F4F6F7;
    border: 1px solid #D5DBDB;
    border-radius: 10px;
    padding: 15px;
    margin: 10px 0;
}
.algorithm-card:hover {
    background-color: #EAF2F8;
    transform: scale(1.01);
    transition: all 0.3s ease-in-out;
}
.result-box {
    background-color: #E8F6F3;
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 10px;
}
.footer {
    text-align: center;
    color: gray;
    margin-top: 40px;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

# --- PRESENTACIÓN ---
st.markdown("<h1 class='title'>🗺️ Algoritmos de Búsqueda en el Mapa de Ecuador</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Explora cómo los algoritmos de búsqueda encuentran rutas entre las ciudades del Ecuador.</p>", unsafe_allow_html=True)

st.markdown("""
<div class='info-box'>
<h3>📘 ¿Qué hace esta aplicación?</h3>
<p>
Este sistema representa un <b>grafo simplificado del mapa del Ecuador</b>, donde las ciudades están conectadas 
por rutas con distancias aproximadas. Los algoritmos de búsqueda permiten analizar y comparar 
distintos métodos para encontrar rutas óptimas o completas entre dos ciudades.
</p>
</div>
""", unsafe_allow_html=True)

# --- DESCRIPCIÓN DE ALGORITMOS ---
col_a1, col_a2 = st.columns(2)
with col_a1:
    st.markdown("""
    <div class='algorithm-card'>
    <h4>🔹 BFS (Búsqueda en Anchura)</h4>
    <p>Explora todos los nodos vecinos antes de pasar a un nivel más profundo. Garantiza el camino más corto en número de pasos.</p>
    </div>
    <div class='algorithm-card'>
    <h4>🔹 DFS (Búsqueda en Profundidad)</h4>
    <p>Explora caminos lo más profundo posible antes de retroceder. Puede ser más rápido pero no siempre encuentra el camino más corto.</p>
    </div>
    """, unsafe_allow_html=True)

with col_a2:
    st.markdown("""
    <div class='algorithm-card'>
    <h4>🔹 UCS (Búsqueda por Costo Uniforme)</h4>
    <p>Explora los caminos con menor costo acumulado. Ideal para encontrar rutas más cortas considerando distancias reales.</p>
    </div>
    <div class='algorithm-card'>
    <h4>🔹 IDDFS (Búsqueda en Profundidad Iterativa)</h4>
    <p>Combina las ventajas de DFS y BFS, aumentando la profundidad de búsqueda gradualmente hasta encontrar el objetivo.</p>
    </div>
    """, unsafe_allow_html=True)

# --- MOSTRAR MAPA ---
st.markdown("<h3 style='text-align:center;'>🧭 Mapa de Conexiones entre Ciudades</h3>", unsafe_allow_html=True)
pos = nx.spring_layout(G, seed=42)
fig, ax = plt.subplots(figsize=(10, 7))
nx.draw(G, pos, with_labels=True, node_size=1800, node_color="#b2dfdb", font_size=10, font_weight='bold')
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
st.pyplot(fig)

# --- INTERACCIÓN ---
col1, col2, col3 = st.columns(3)
with col1:
    origen = st.selectbox("🏙️ Ciudad de Origen", ciudades)
with col2:
    destino = st.selectbox("📍 Ciudad de Destino", ciudades)
with col3:
    profundidad = st.slider("📏 Profundidad Máxima (IDDFS)", 1, 10, 5)

if st.button("🔍 Ejecutar Algoritmos"):
    resultados = []

    camino_bfs, nodos_bfs = bfs(origen, destino)
    resultados.append(["BFS", camino_bfs, len(camino_bfs)-1 if camino_bfs else "-", "-", nodos_bfs])

    camino_dfs, nodos_dfs = dfs(origen, destino)
    resultados.append(["DFS", camino_dfs, len(camino_dfs)-1 if camino_dfs else "-", "-", nodos_dfs])

    camino_ucs, costo_ucs, nodos_ucs = ucs(origen, destino)
    resultados.append(["UCS", camino_ucs, len(camino_ucs)-1 if camino_ucs else "-", costo_ucs, nodos_ucs])

    camino_iddfs, prof_iddfs = iddfs(origen, destino, profundidad)
    resultados.append(["IDDFS", camino_iddfs, len(camino_iddfs)-1 if camino_iddfs else "-", "-", prof_iddfs])

    for algoritmo, camino, pasos, costo, nodos in resultados:
        with st.expander(f"🔹 Resultado {algoritmo}"):
            if camino:
                st.markdown(f"<div class='result-box'><b>Camino:</b> {' → '.join(camino)}<br>"
                            f"<b>Pasos:</b> {pasos}<br>"
                            f"<b>Costo Total:</b> {costo if costo!='-' else 'N/A'}<br>"
                            f"<b>Nodos Expandidos:</b> {nodos}</div>", unsafe_allow_html=True)
            else:
                st.warning("❌ No se encontró un camino.")

    df = pd.DataFrame(resultados, columns=["Algoritmo", "Camino", "Pasos", "Costo Total", "Nodos Expandidos"])
    st.subheader("📊 Comparación de Algoritmos")
    st.dataframe(df)

# --- PIE DE PÁGINA ---
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p class='footer'>Presentación Interactiva - Agentes Inteligentes y Resolución de Problemas<br>Asignatura: Inteligencia Artificial | TDS</p>", unsafe_allow_html=True)
