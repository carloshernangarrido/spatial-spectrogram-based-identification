import numpy as np
# -------------------------
# GEOMETRÍA VÍA
# -------------------------
L = 60.0                                # Longitud total de vía [m]
sep_dur = 0.6                           # Separación entre durmientes medidas en Albardon [m]
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

rho_b = 1.8e3                           # Masa específica del balasto Kg/m³
h_b = 0.45                              # ALtura de la capa de balasto [m]
l_e = 0.95                              # longitud efectiva de apoyo de la mitad de un durmiente [m]
l_b = 0.273                             # ancho del durmiente [m]
l_s = sep_dur                           # separación entre durmientes [m]
alpha = 35                              # angulo de fricción interna del balasto [º]
alpha_rad = np.radians(alpha)
E_b = 1.1e8                             # módulo de elasticidad del balasto [Pa]
E_f = 9e7                               # módulo K_30 de sub base [Pa/m]

h_0 = h_b - (l_s - l_b) / (2 * np.tan(alpha_rad))
print(h_0)

if h_0 <= 0:
    m_b = rho_b * h_b * (l_e * l_b + (l_e + l_b) * h_b * np.tan(alpha_rad) + 4 / 3 * h_b ** 2 * (np.tan(alpha_rad)) ** 2)
    k_b = 2 * (l_e - l_b) * np.tan(alpha_rad) / np.log ((l_e / l_b) * (l_b + 2 * h_b * np.tan(alpha_rad)) / (l_e + 2 * h_b * np.tan(alpha_rad))) * E_b
    k_f = (l_e + 2 * h_b * np.tan(alpha_rad)) * (l_b + 2 * h_b * np.tan(alpha_rad)) * E_f
    print(f'No hay solapamiento de los conos de carga')
else:
    m_b = rho_b * (l_b * h_b * (l_e + h_b * np.tan(alpha_rad)) + l_e * (h_b ** 2 - h_0 ** 2) * np.tan(alpha_rad) + 4 / 3 * (h_b ** 3 - h_0 ** 3) * (np.tan(alpha_rad)) ** 2)
    k_b1 = 2 * (l_e - l_b) * np.tan(alpha_rad) / np.log ((l_e * l_s) / (l_b * (l_e + l_s - l_b))) * E_b
    k_b2 = l_s * (l_s - l_b + 2 * l_e + 2 * h_b * np.tan(alpha_rad)) * np.tan(alpha_rad) / (l_b - l_s + 2 * h_b * np.tan(alpha_rad)) * E_b
    k_b = k_b1 * k_b2 / (k_b1 + k_b2)
    k_f = l_s * (l_e + 2 * h_b * np.tan(alpha_rad)) * E_f
    print(f'Hay solapamiento de los conos de carga')

print(f'masa vibrante del balasto: {m_b} Kg')
print(f'rigidez balasto: {k_b} [N/m] o {k_b/1e6} [MN/m]')
print(f'rigidez sub base: {k_f} [N/m] o {k_f/1e6} [MN/m]')




k_b = np.ones(n_tot - 1) * 7.5e7 #5.3e7        # Balasto vía [N/m²] 53 000 000 478 353 900
#k_b = np.ones(n_tot -1) * 15000000  # Feng (2011)
#c_b = np.ones(n_tot - 1) * 4783539 #1.0e3        # Amortiguamiento vía  [N s/m²] 
c_b = np.ones(n_tot - 1) * 0
#c_b = np.ones(n_tot - 1) * 50000  # Feng (2011)
q0 = 0.0                                # Magnitud de la carga distribuida sobre vía [Kg/m]

def q(x, q0):
    return np.array([0, -q0, 0, 0, -q0, 0])

# -------------------------
#  NODOS DAÑADOS
# -------------------------

dano_nodal = {
    #45: 0.4,
    #80: 0.6,
    #47: 0.5
}
dano_nodal = None


gdl_restringidos = [0, 1, 2, (n_tot-1)*3, (n_tot-1)*3 + 1, (n_tot-1)*3 + 2]


tren_params = dict(
    n_vagones=2,                        # Cantidad de vagones
    n_ejes=4,                           # Número de ejes por vagón
    m1=4050.0,                          # Masa 1/8 vagón [Kg]
    m2=500.0,                           # Masa 1/4 bogie [Kg]
    k1=2.6e6,                           # Rigidez resorte entre vagón y bogie (susp. secundaria) [N/m]
    k2=4.3e6,                            # Rigidez resorte bogie y vía (susp. primaria) [N/m]
    c1=2.6e4,                            # Amortiguamiento entre vagón y bogie (susp. secundaria) [Ns/m]
    c2=5.8e4,                            # Amortiguamiento entre bogie y vía (susp. primaria) [Ns/m]
    d1=1.8,                             # Distancia entre ejes de bogie [m]
    d2=7.72,                            # Distancia entre ejes de diferentes vagones
    d3=0.0
)

t_sim = 7                               # Tiempo de simulación [s]
dt = 0.001                              # Dt de la salida
t_eval = np.arange(0, t_sim, dt)


vx_0 = 4.5                              # velocidad inicial [m/s]
vx_1 = 5.0                             # velocidad final   [m/s]
x0 = 20.0                               # posición inicial  [m]

# =========================
# CINEMÁTICA DE LA CARGA
# =========================
cinematica_params = dict(
    tipo="lineal",          # constante, lineal, trapezoidal, senoidal
    v0=vx_0,
    v1=vx_1,
    t_total=t_sim,
    x0=x0
)

# =========================
# PARÁMETROS DE SIMULACIÓN
# =========================
sim_params = dict(
    T_rampa=0.0
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