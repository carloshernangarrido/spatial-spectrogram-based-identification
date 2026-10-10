import numpy as np
# -------------------------
# GEOMETRÍA VÍA
# -------------------------
L = 200.0                               # Longitud total de vía [m]
sep_dur = 0.6                           # Separación entre durmientes [m]
n_tot = int(L / sep_dur) + 1            # Cantidad total de nodos de la vía
dof_malla = 3                           # Grados de libertad por cada nodo de la vía
g = 9.81                                # Aceleración de la gravedad [m/s²]

# -------------------------
#  PROPIEDADES RIEL UIC 60
# -------------------------
a_r = np.ones(n_tot - 1) * 7.686e-3     # Área transversal del riel [m²]
gamma_r = np.ones(n_tot - 1) * 7850     # Masa específica del acero [Kg/m³]
m_r = gamma_r * a_r                     # Masa por unidad de longitud del riel [Kg/m]
e_r = np.ones(n_tot - 1) * 2.07e11      # Módulo de Young del acero [Pa]
nu = np.ones(n_tot - 1) * 0.28          # Módulo de Poisson del acero 
i_r = np.ones(n_tot - 1) * 3.055e-5     # Momento de inercia riel UIC 60 [m⁴]

# -------------------------
#  PROPIEDADES PEDRAPLÉN
# -------------------------
k_b = np.ones(n_tot -1) * 7.5e7   # Feng (2011)
#c_b = np.ones(n_tot - 1) * 50000  # Feng (2011)
c_b = np.ones(n_tot - 1) * 0  # Feng (2011)
q0 = 0.0                                # Magnitud de la carga distribuida sobre vía [Kg/m]

def q(x, q0):
    return np.array([0, -q0, 0, 0, -q0, 0])

# -------------------------
#  NODOS DAÑADOS
# -------------------------

dano_nodal = {
    int(50/sep_dur): 0.4,
    int(100/sep_dur): 0.6,
    int(150/sep_dur): 0.8
}
# dano_nodal = None


gdl_restringidos = [0, 1, 2, (n_tot-1)*3, (n_tot-1)*3 + 1, (n_tot-1)*3 + 2]


tren_params = dict(
    n_vagones=1,                        # Cantidad de vagones
    n_ejes=6,                           # Número de ejes por vagón
    m1=4050.0,                          # Masa 1/8 vagón [Kg]
    m2=500.0,                           # Masa 1/4 bogie [Kg]
    k1=2.6e6,                          # Rigidez resorte entre vagón y bogie (susp. secundaria) [N/m]
    k2=4.3e6,                            # Rigidez resorte bogie y vía (susp. primaria) [N/m]
    c1=2.6e4,                            # Amortiguamiento entre vagón y bogie (susp. secundaria) [Ns/m]
    c2=5.8e4,                            # Amortiguamiento entre bogie y vía (susp. primaria) [Ns/m]
    d1=1.8,                             # Distancia entre ejes de bogie [m]
    d2=7.72,                            # Distancia entre ejes de diferentes vagones
    d3=0.0
)

t_sim = 15                               # Tiempo de simulación [s]
dt = 0.001                              # Dt de la salida
t_eval = np.arange(0, t_sim, dt)


vx_0 = 0.0                              # velocidad inicial [m/s]
vx_1 = 15.0                             # velocidad final   [m/s]
x0 = 40.0                               # posición inicial  [m]

# =========================
# CINEMÁTICA DE LA CARGA
# =========================
# cinematica_params = dict(
#     tipo="lineal",          # constante, lineal, trapezoidal, senoidal
#     v0=vx_0,
#     v1=vx_1,
#     t_total=t_sim,
#     x0=x0
# )
cinematica_params = dict(
    tipo="trapezoidal",          # constante, lineal, trapezoidal, senoidal
    v0=vx_0,
    v1=vx_1,
    t_total=t_sim,
    t_acc=10.0,
    t_crucero=5.0,
    x0=x0
)

if cinematica_params["tipo"] == "lineal":
    print(f"Velocidad final de la carga: {vx_1} m/s")
elif cinematica_params["tipo"] == "trapezoidal":
    v_avg = (vx_1 + vx_0) / 2
    total_distance = v_avg * cinematica_params["t_acc"] + vx_1 * cinematica_params["t_crucero"]
    print(f"Velocidad final de la carga: {vx_1} m/s")
    print(f"Distancia recorrida en aceleración y crucero: {total_distance} m")
    print(f"Posición final de la carga: {x0 + total_distance} m")

# =========================
# PARÁMETROS DE SIMULACIÓN
# =========================
sim_params = dict(
    T_rampa=1.0
)


# =========================
# CONFIGURACIÓN DE LA VÍA
# =========================
dof_malla = 3
usar_amortiguamiento_rayleigh = True


# =========================
# CARGA MÓVIL – CONFIGURACIÓN
# =========================
carga_params = dict(
    x0=x0,
    Le=sep_dur
)
