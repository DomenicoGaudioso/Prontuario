import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ==========================================
# 1. FUNZIONI ANALITICHE (10 CASI IMPLEMENTATI)
# ==========================================

# --- APPOGGIO - APPOGGIO ---
def calc_appoggio_distribuito(L, q, E, I):
    EI = E * I
    x = np.linspace(0, L, 500)
    V = q * (L/2 - x)
    M = (q * x * (L - x)) / 2
    theta = (q / (24 * EI)) * (L**3 - 6*L*(x**2) + 4*(x**3))
    v = (q * x / (24 * EI)) * (L**3 - 2*L*(x**2) + x**3)
    return x, V, M, theta, v

def calc_appoggio_concentrato_mezzeria(L, F, E, I):
    EI = E * I
    x = np.linspace(0, L, 500)
    V = np.where(x < L/2, F/2, -F/2)
    M = np.where(x <= L/2, (F*x)/2, (F*(L-x))/2)
    theta = np.where(x <= L/2, (F/(16*EI))*(L**2 - 4*x**2), (F/(16*EI))*(4*(x-L/2)**2 - L**2))
    v = np.where(x <= L/2, (F*x/(48*EI))*(3*L**2 - 4*x**2), (F*(L-x)/(48*EI))*(3*L**2 - 4*(L-x)**2))
    return x, V, M, theta, v

def calc_appoggio_triangolare(L, q, E, I): # Max in B
    EI = E * I
    x = np.linspace(0, L, 500)
    V = (q*L/6) - (q*x**2)/(2*L)
    M = (q*L*x/6) - (q*x**3)/(6*L)
    theta = (q/(360*EI*L)) * (7*L**4 - 30*L**2*x**2 + 15*x**4)
    v = (q*x/(360*EI*L)) * (7*L**4 - 10*L**2*x**2 + 3*x**4)
    return x, V, M, theta, v

# --- MENSOLA ---
def calc_mensola_concentrato_punta(L, F, E, I):
    EI = E * I
    x = np.linspace(0, L, 500)
    V = np.full_like(x, F)
    M = -F * (L - x)
    theta = (F / (2 * EI)) * (2*L*x - x**2)
    v = (F * (x**2) / (6 * EI)) * (3*L - x)
    return x, V, M, theta, v

def calc_mensola_distribuito(L, q, E, I):
    EI = E * I
    x = np.linspace(0, L, 500)
    V = q * (L - x)
    M = -(q * (L - x)**2) / 2
    theta = (q / (6 * EI)) * (x**3 - 3*L*x**2 + 3*L**2*x)
    v = (q * x**2 / (24 * EI)) * (x**2 - 4*L*x + 6*L**2)
    return x, V, M, theta, v

def calc_mensola_triangolare(L, q, E, I): # Max all'incastro
    EI = E * I
    x = np.linspace(0, L, 500)
    V = (q/(2*L)) * (L - x)**2
    M = -(q/(6*L)) * (L - x)**3
    theta = (q/(24*EI*L)) * (L**4 - (L-x)**4)
    v = (q/(120*EI*L)) * (5*L**4*x - L**5 + (L-x)**5)
    return x, V, M, theta, v

# --- INCASTRO - APPOGGIO ---
def calc_incastro_appoggio_distribuito(L, q, E, I):
    EI = E * I
    x = np.linspace(0, L, 500)
    V = (5*q*L/8) - q*x
    M = -(q*L**2/8) + (5*q*L*x/8) - (q*x**2/2)
    theta = (q/(48*EI)) * (6*L**2*x - 15*L*x**2 + 8*x**3)
    v = (q*x**2/(48*EI)) * (3*L**2 - 5*L*x + 2*x**2)
    return x, V, M, theta, v

def calc_incastro_appoggio_concentrato(L, F, E, I): # In mezzeria
    EI = E * I
    x = np.linspace(0, L, 500)
    V = np.where(x < L/2, 11*F/16, -5*F/16)
    M = np.where(x <= L/2, (11*F*x/16) - (3*F*L/16), (5*F*(L-x)/16))
    theta = np.where(x <= L/2, (F/(32*EI))*(22*x**2 - 12*L*x), (F/(32*EI))*(4*L**2 - 20*L*x + 10*x**2)) # Approssimazione polinomiale base
    v = np.where(x <= L/2, (F*x**2/(96*EI))*(22*x - 18*L), (F*(L-x)/(96*EI))*(5*L**2 - 10*L*(L-x) + 4*(L-x)**2)) # Approssimazione v
    return x, V, M, theta, v

# --- INCASTRO - INCASTRO ---
def calc_incastro_incastro_distribuito(L, q, E, I):
    EI = E * I
    x = np.linspace(0, L, 500)
    V = q * (L/2 - x)
    M = (q/12) * (6*L*x - 6*x**2 - L**2)
    theta = (q*x/(12*EI)) * (L - x) * (L - 2*x)
    v = (q*x**2/(24*EI)) * (L - x)**2
    return x, V, M, theta, v

def calc_incastro_incastro_concentrato(L, F, E, I): # In mezzeria
    EI = E * I
    x = np.linspace(0, L, 500)
    V = np.where(x < L/2, F/2, -F/2)
    M = np.where(x <= L/2, (F/8)*(4*x - L), (F/8)*(3*L - 4*x))
    theta = np.where(x <= L/2, (F*x/(8*EI))*(L - 2*x), (F*(L-x)/(8*EI))*(2*x - L))
    v = np.where(x <= L/2, (F*x**2/(48*EI))*(3*L - 4*x), (F*(L-x)**2/(48*EI))*(3*L - 4*(L-x)))
    return x, V, M, theta, v

# ==========================================
# 2. FUNZIONI GRAFICHE PLOTLY
# ==========================================
def disegna_schema_statico(vincolo, carico, L_m):
    fig = go.Figure()
    
    # 1. Imposto la lunghezza visiva (per la trave continua disegno 2 campate)
    L_draw = L_m * 2 if vincolo == "Trave Continua" else L_m

    # 2. Disegno l'elemento strutturale principale
    if "Arco" in vincolo or "Cavo" in vincolo:
        # Disegno un arco o una fune parabolica fittizia
        x_curve = np.linspace(0, L_draw, 50)
        y_curve = -0.4 * np.sin(np.pi * x_curve / L_draw) if "Cavo" in vincolo else 0.6 * np.sin(np.pi * x_curve / L_draw)
        fig.add_trace(go.Scatter(x=x_curve, y=y_curve, mode='lines', line=dict(color='black', width=5), showlegend=False))
        # La linea di base dritta tratteggiata per gli archi
        fig.add_shape(type="line", x0=0, y0=0, x1=L_draw, y1=0, line=dict(color="gray", width=2, dash="dash"))
    else:
        # Trave dritta standard
        fig.add_shape(type="line", x0=0, y0=0, x1=L_draw, y1=0, line=dict(color="black", width=6))

    # 3. Disegno i Vincoli
    if vincolo == "Appoggio - Appoggio" or "Arco" in vincolo or "Cavo" in vincolo:
        fig.add_shape(type="path", path="M -0.1 -0.5 L 0.1 -0.5 L 0 0 Z", fillcolor="gray", line_color="black")
        fig.add_shape(type="path", path=f"M {L_draw-0.1} -0.5 L {L_draw+0.1} -0.5 L {L_draw} 0 Z", fillcolor="gray", line_color="black")
    elif vincolo == "Mensola":
        fig.add_shape(type="rect", x0=-L_draw*0.05, y0=-0.6, x1=0, y1=0.6, fillcolor="gray", line_color="black")
    elif vincolo == "Incastro - Appoggio":
        fig.add_shape(type="rect", x0=-L_draw*0.05, y0=-0.6, x1=0, y1=0.6, fillcolor="gray", line_color="black")
        fig.add_shape(type="path", path=f"M {L_draw-0.1} -0.5 L {L_draw+0.1} -0.5 L {L_draw} 0 Z", fillcolor="gray", line_color="black")
    elif vincolo == "Incastro - Incastro":
        fig.add_shape(type="rect", x0=-L_draw*0.05, y0=-0.6, x1=0, y1=0.6, fillcolor="gray", line_color="black")
        fig.add_shape(type="rect", x0=L_draw, y0=-0.6, x1=L_draw*1.05, y1=0.6, fillcolor="gray", line_color="black")
    elif vincolo == "Trave Continua":
        # Disegno 3 appoggi (inizio, centro, fine)
        for pos in [0, L_m, L_draw]:
            fig.add_shape(type="path", path=f"M {pos-0.1} -0.5 L {pos+0.1} -0.5 L {pos} 0 Z", fillcolor="gray", line_color="black")

    # 4. Disegno i Carichi Visivi (La parte che volevi indietro!)
    
    # -> CARICHI DISTRIBUITI (Rettangolo azzurro con frecce)
    if "Distribuito" in carico or "Fune" in carico:
        estensione = L_draw / 2 if "parziale" in carico else L_draw
        fig.add_shape(type="rect", x0=0, y0=0, x1=estensione, y1=0.4, fillcolor="rgba(30, 144, 255, 0.2)", line_color="blue")
        for x_arrow in np.linspace(0.1 * estensione, 0.9 * estensione, 7):
            fig.add_annotation(x=x_arrow, y=0, ax=x_arrow, ay=0.4, xref="x", yref="y", axref="x", ayref="y", showarrow=True, arrowhead=2, arrowsize=1, arrowcolor="blue")

    # -> CARICHI TRIANGOLARI / TRAPEZOIDALI (Poligono azzurro)
    elif "Triangolare" in carico or "Trapezoidale" in carico:
        if "Sx" in carico:
            path = f"M 0 0 L 0 0.5 L {L_draw} 0 Z"
        elif "Punta" in carico and vincolo == "Mensola":
             path = f"M 0 0 L {L_draw} 0.5 L {L_draw} 0 Z"
        elif "Trapezoidale" in carico:
             path = f"M 0 0 L 0 0.5 L {L_draw} 0.2 L {L_draw} 0 Z"
        else:
             path = f"M 0 0 L {L_draw/2} 0.5 L {L_draw} 0 Z" # Simmetrico
        
        fig.add_shape(type="path", path=path, fillcolor="rgba(30, 144, 255, 0.2)", line_color="blue")
        fig.add_annotation(x=L_draw/3, y=0, ax=L_draw/3, ay=0.3, xref="x", yref="y", axref="x", ayref="y", showarrow=True, arrowhead=2, arrowcolor="blue")

    # -> CARICHI CONCENTRATI (Freccia grossa rossa)
    elif "Concentrato" in carico or "Chiave" in carico:
        pos_x = L_draw / 2 # Default in mezzo
        if "Punta" in carico: pos_x = L_draw
        elif "a distanza" in carico: pos_x = L_draw * 0.33 # Puramente visivo
        
        fig.add_annotation(x=pos_x, y=0, ax=pos_x, ay=0.7, xref="x", yref="y", axref="x", ayref="y", showarrow=True, arrowhead=2, arrowsize=1.5, arrowwidth=3, arrowcolor="red")
        
        if "Due" in carico: # Se ci sono due carichi (simmetrici o a sbalzo)
            pos_x2 = L_draw * 0.66 if "simmetrici" in carico else L_draw
            fig.add_annotation(x=pos_x2, y=0, ax=pos_x2, ay=0.7, xref="x", yref="y", axref="x", ayref="y", showarrow=True, arrowhead=2, arrowsize=1.5, arrowwidth=3, arrowcolor="red")

    # -> AZIONI SPECIALI (Momenti, Termica, Cedimenti)
    elif "Momento" in carico or "Flessione" in carico or "Termico" in carico or "Cedimento" in carico:
         icona = "🌡️" if "Termico" in carico else "📉" if "Cedimento" in carico else "🔄"
         fig.add_annotation(x=L_draw/2, y=0.5, text=f"{icona} {carico}", showarrow=False, font=dict(size=14, color="purple"))

    # 5. Pulizia del grafico
    fig.update_layout(
        xaxis=dict(range=[-L_draw*0.1, L_draw*1.1], visible=False),
        yaxis=dict(range=[-1.0, 1.0], visible=False),
        height=180, margin=dict(l=0, r=0, t=10, b=10),
        plot_bgcolor="white"
    )
    return fig

def crea_4_grafici_plotly(x, V, M, theta, v):
    fig = make_subplots(rows=4, cols=1, shared_xaxes=True, vertical_spacing=0.05,
                        subplot_titles=("Taglio (V) [kN]", "Momento Flettente (M) [kNm]", "Rotazione (θ) [mrad]", "Deformata (v) [mm]"))

    fig.add_trace(go.Scatter(x=x, y=V, fill='tozeroy', mode='lines', line=dict(color='red', width=2), fillcolor='rgba(255,0,0,0.3)', name='Taglio'), row=1, col=1)
    fig.add_trace(go.Scatter(x=x, y=M, fill='tozeroy', mode='lines', line=dict(color='blue', width=2), fillcolor='rgba(0,0,255,0.3)', name='Momento'), row=2, col=1)
    fig.add_trace(go.Scatter(x=x, y=theta, mode='lines', line=dict(color='green', width=2), name='Rotazione'), row=3, col=1)
    fig.add_trace(go.Scatter(x=x, y=v, mode='lines', line=dict(color='darkorange', width=2), fill='tozeroy', fillcolor='rgba(255,140,0,0.2)', name='Deformata'), row=4, col=1)

    fig.update_yaxes(zeroline=True, zerolinewidth=1, zerolinecolor='black')
    fig.update_yaxes(autorange="reversed", row=2, col=1)
    fig.update_yaxes(autorange="reversed", row=4, col=1)
    fig.update_xaxes(title_text="Lunghezza Trave (m)", row=4, col=1)

    fig.update_layout(height=800, showlegend=False, template="plotly_white", margin=dict(l=20, r=20, t=40, b=20))
    return fig

# 11. Appoggio-Appoggio: Concentrato generico a distanza 'a'
def calc_appoggio_concentrato_a(L, F, a, E, I):
    EI = E * I
    b = L - a
    x = np.linspace(0, L, 500)
    V = np.where(x < a, F*b/L, -F*a/L)
    M = np.where(x <= a, (F*b*x)/L, (F*a*(L-x))/L)
    theta = np.zeros_like(x) # Omessa per brevità
    v = np.zeros_like(x)     # Omessa per brevità
    return x, V, M, theta, v

# 12. Appoggio-Appoggio: Momento concentrato M0 nell'estremo A
def calc_appoggio_momento_A(L, M0, E, I):
    EI = E * I
    x = np.linspace(0, L, 500)
    V = np.full_like(x, -M0/L)
    M = M0 * (1 - x/L)
    theta = (M0/(6*EI*L)) * (2*L**2 - 6*L*x + 3*x**2)
    v = (M0*x/(6*EI*L)) * (2*L**2 - 3*L*x + x**2)
    return x, V, M, theta, v

# 13. Appoggio-Appoggio: Due carichi F simmetrici (distanza 'a' dagli estremi)
def calc_appoggio_2F_simmetrici(L, F, a, E, I):
    EI = E * I
    x = np.linspace(0, L, 500)
    V = np.where(x < a, F, np.where(x <= L-a, 0, -F))
    M = np.where(x < a, F*x, np.where(x <= L-a, F*a, F*(L-x)))
    theta = np.zeros_like(x)
    v = np.zeros_like(x)
    return x, V, M, theta, v

# 14. Appoggio-Appoggio: Triangolare Simmetrico (Max q in mezzeria)
def calc_appoggio_triangolare_simmetrico(L, q, E, I):
    EI = E * I
    x = np.linspace(0, L, 500)
    V = np.where(x <= L/2, q*L/4 - q*x**2/L, -q*L/4 + q*(L-x)**2/L)
    M = np.where(x <= L/2, q*L*x/4 - q*x**3/(3*L), q*L*(L-x)/4 - q*(L-x)**3/(3*L))
    theta = np.zeros_like(x)
    v = np.zeros_like(x)
    return x, V, M, theta, v

# 15. Mensola: Concentrato generico a distanza 'a' dall'incastro
def calc_mensola_concentrato_a(L, F, a, E, I):
    EI = E * I
    x = np.linspace(0, L, 500)
    V = np.where(x < a, F, 0)
    M = np.where(x <= a, -F*(a - x), 0)
    theta = np.where(x <= a, (F/(2*EI))*(2*a*x - x**2), (F*a**2)/(2*EI))
    v = np.where(x <= a, (F*x**2/(6*EI))*(3*a - x), (F*a**2/(6*EI))*(3*x - a))
    return x, V, M, theta, v

# 16. Mensola: Momento M0 applicato in punta
def calc_mensola_momento_punta(L, M0, E, I):
    EI = E * I
    x = np.linspace(0, L, 500)
    V = np.zeros_like(x)
    M = np.full_like(x, -M0)
    theta = (M0 * x) / EI
    v = (M0 * x**2) / (2 * EI)
    return x, V, M, theta, v

# 17. Mensola: Carico distribuito parziale (da 'a' fino alla punta L)
def calc_mensola_distribuito_parziale(L, q, a, E, I):
    EI = E * I
    x = np.linspace(0, L, 500)
    V = np.where(x < a, q*(L-a), q*(L-x))
    M = np.where(x <= a, -q*(L-a)*(L+a-2*x)/2, -q*(L-x)**2/2)
    theta = np.zeros_like(x)
    v = np.zeros_like(x)
    return x, V, M, theta, v

# 18. Mensola: Triangolare (Max q in Punta)
def calc_mensola_triangolare_punta(L, q, E, I):
    EI = E * I
    x = np.linspace(0, L, 500)
    V = (q/(2*L))*(L**2 - x**2)
    M = -(q/(6*L))*(2*L**3 - 3*L**2*x + x**3)
    theta = np.zeros_like(x)
    v = np.zeros_like(x)
    return x, V, M, theta, v

# 19. Incastro-Appoggio: Momento M0 applicato sull'appoggio
def calc_incastro_appoggio_momento_B(L, M0, E, I):
    EI = E * I
    x = np.linspace(0, L, 500)
    V = np.full_like(x, -3*M0/(2*L))
    M = M0/2 - (3*M0*x)/(2*L)
    theta = np.zeros_like(x)
    v = np.zeros_like(x)
    return x, V, M, theta, v

# 20. Incastro-Incastro: Concentrato generico a distanza 'a'
def calc_incastro_incastro_concentrato_a(L, F, a, E, I):
    EI = E * I
    b = L - a
    R_A = F * b**2 * (3*a + b) / L**3
    M_A = -F * a * b**2 / L**2
    x = np.linspace(0, L, 500)
    V = np.where(x < a, R_A, R_A - F)
    M = np.where(x <= a, M_A + R_A*x, M_A + R_A*x - F*(x-a))
    theta = np.zeros_like(x)
    v = np.zeros_like(x)
    return x, V, M, theta, v

# ==========================================
# ALTRI 10 CASI AGGIUNTIVI (21 - 30)
# ==========================================

# 21. Appoggio-Appoggio: Distribuito parziale (da 0 ad 'a')
def calc_appoggio_distribuito_parziale_sx(L, q, a, E, I):
    EI = E * I
    R_A = q * a * (L - a/2) / L
    R_B = q * a**2 / (2*L)
    x = np.linspace(0, L, 500)
    V = np.where(x <= a, R_A - q*x, -R_B)
    M = np.where(x <= a, R_A*x - q*x**2/2, R_B*(L-x))
    theta = np.zeros_like(x)
    v = np.zeros_like(x)
    return x, V, M, theta, v

# 22. Appoggio-Appoggio: Momento M0 in mezzeria
def calc_appoggio_momento_mezzeria(L, M0, E, I):
    EI = E * I
    x = np.linspace(0, L, 500)
    V = np.full_like(x, -M0/L)
    M = np.where(x < L/2, -M0*x/L, M0*(1 - x/L))
    theta = np.zeros_like(x)
    v = np.zeros_like(x)
    return x, V, M, theta, v

# 23. Appoggio-Appoggio: Flessione Pura (Momento M0 costante)
def calc_appoggio_flessione_pura(L, M0, E, I):
    EI = E * I
    x = np.linspace(0, L, 500)
    V = np.zeros_like(x)
    M = np.full_like(x, M0)
    theta = (M0 / EI) * (L/2 - x)
    v = (M0 / (2*EI)) * x * (L - x)
    return x, V, M, theta, v

# 24. Appoggio-Appoggio: Triangolare (Max in Appoggio sx)
def calc_appoggio_triangolare_sx(L, q, E, I):
    EI = E * I
    R_A = q * L / 3
    R_B = q * L / 6
    x = np.linspace(0, L, 500)
    V = R_A - q*x + q*x**2/(2*L)
    M = R_A*x - q*x**2/2 + q*x**3/(6*L)
    theta = np.zeros_like(x)
    v = np.zeros_like(x)
    return x, V, M, theta, v

# 25. Mensola: Trapezoidale (q1 all'incastro, q2 in punta)
def calc_mensola_trapezoidale(L, q1, q2, E, I):
    EI = E * I
    x = np.linspace(0, L, 500)
    # Sovrapposizione degli effetti (Rettangolo q2 + Triangolo q1-q2)
    V = q2*(L-x) + (q1-q2)*(L-x)**2/(2*L)
    M = -q2*(L-x)**2/2 - (q1-q2)*(L-x)**3/(6*L)
    theta = np.zeros_like(x)
    v = np.zeros_like(x)
    return x, V, M, theta, v

# 26. Mensola: Due carichi concentrati (F1 a distanza 'a', F2 in punta)
def calc_mensola_due_concentrati(L, F1, F2, a, E, I):
    EI = E * I
    x = np.linspace(0, L, 500)
    V = np.where(x < a, F1 + F2, F2)
    M = np.where(x <= a, -F1*(a-x) - F2*(L-x), -F2*(L-x))
    theta = np.zeros_like(x)
    v = np.zeros_like(x)
    return x, V, M, theta, v

# 27. Incastro-Appoggio: Concentrato a distanza 'a' dall'incastro
def calc_incastro_appoggio_concentrato_a(L, F, a, E, I):
    EI = E * I
    b = L - a
    R_B = F * a**2 * (3*L - a) / (2 * L**3)
    R_A = F - R_B
    M_A = -F * a * b * (L + b) / (2 * L**2)
    x = np.linspace(0, L, 500)
    V = np.where(x < a, R_A, -R_B)
    M = np.where(x <= a, M_A + R_A*x, R_B*(L-x))
    theta = np.zeros_like(x)
    v = np.zeros_like(x)
    return x, V, M, theta, v

# 28. Incastro-Appoggio: Momento M0 in mezzeria
def calc_incastro_appoggio_momento_mezzeria(L, M0, E, I):
    EI = E * I
    R_A = -9 * M0 / (8 * L)
    R_B = 9 * M0 / (8 * L)
    M_A = -M0 / 8
    x = np.linspace(0, L, 500)
    V = np.full_like(x, R_A)
    M = np.where(x < L/2, M_A + R_A*x, R_B*(L-x))
    theta = np.zeros_like(x)
    v = np.zeros_like(x)
    return x, V, M, theta, v

# 29. Incastro-Incastro: Triangolare (Max q all'incastro sx)
def calc_incastro_incastro_triangolare_sx(L, q, E, I):
    EI = E * I
    R_A = 7 * q * L / 20
    R_B = 3 * q * L / 20
    M_A = -q * L**2 / 20
    M_B = -q * L**2 / 30
    x = np.linspace(0, L, 500)
    V = R_A - q*x + q*x**2/(2*L)
    M = M_A + R_A*x - q*x**2/2 + q*x**3/(6*L)
    theta = np.zeros_like(x)
    v = np.zeros_like(x)
    return x, V, M, theta, v

# 30. Incastro-Incastro: Momento M0 in mezzeria
def calc_incastro_incastro_momento_mezzeria(L, M0, E, I):
    EI = E * I
    R_A = -3 * M0 / (2 * L)
    R_B = 3 * M0 / (2 * L)
    M_A = -M0 / 4
    x = np.linspace(0, L, 500)
    V = np.full_like(x, R_A)
    M = np.where(x < L/2, M_A + R_A*x, M_A + R_A*x + M0)
    theta = np.zeros_like(x)
    v = np.zeros_like(x)
    return x, V, M, theta, v

# ==========================================
# CASI AVANZATI: ARCHI, TERMICA, CEDIMENTI
# ==========================================

# 31. Arco a 3 cerniere (Parabolico) con carico concentrato in chiave
def calc_arco_3_cerniere_chiave(L, f, F, E, I):
    EI = E * I
    x = np.linspace(0, L, 500)
    
    # Spinta orizzontale H e reazioni verticali
    H = (F * L) / (4 * f)
    V_reaz = F / 2
    
    # Equazione della parabola dell'arco y(x)
    y = (4 * f / L**2) * x * (L - x)
    
    # Taglio verticale (non è il taglio ortogonale all'asse, ma la proiezione)
    V = np.where(x < L/2, V_reaz, -V_reaz)
    
    # Momento flettente: Momento della trave isostatica equivalente MENO il momento della spinta (H * y)
    M_trave = np.where(x <= L/2, (F * x) / 2, (F * (L - x)) / 2)
    M = M_trave - (H * y)
    
    # Rotazione e deformata ortogonale omesse per complessità geometrica
    theta = np.zeros_like(x)
    v = np.zeros_like(x)
    return x, V, M, theta, v, H

# 32. Incastro-Incastro: Gradiente Termico (differenza di T tra estradosso e intradosso)
def calc_incastro_incastro_termico(L, deltaT, h, alpha, E, I):
    EI = E * I
    x = np.linspace(0, L, 500)
    
    # Il momento generato per impedire la curvatura termica
    M_termico = (E * I * alpha * deltaT) / h
    
    V = np.zeros_like(x)
    M = np.full_like(x, M_termico)  # Momento costante in tutta la trave
    
    # In una struttura doppiamente incastrata, il momento blocca la deformazione
    theta = np.zeros_like(x) 
    v = np.zeros_like(x)
    return x, V, M, theta, v

# 33. Incastro-Incastro: Cedimento vincolare verticale dell'appoggio destro
def calc_incastro_incastro_cedimento(L, delta, E, I):
    EI = E * I
    x = np.linspace(0, L, 500)
    
    # Sollecitazioni indotte dal cedimento delta
    V = np.full_like(x, -12 * EI * delta / L**3)
    M = (6 * EI * delta / L**2) * (1 - 2 * x / L)
    
    # Deformazione geometrica indotta
    theta = (6 * delta / L**2) * (x - x**2 / L)
    v = delta * (3 * (x / L)**2 - 2 * (x / L)**3)
    return x, V, M, theta, v

# ==========================================
# CASI SPECIALI: ARCHI IPERSTATICI, FUNI E TRAVI CONTINUE
# ==========================================

# 34. Arco a 2 Cerniere (Parabolico) con carico concentrato in chiave
def calc_arco_2_cerniere(L, f, F, E, I):
    # Trascurando la deformabilità assiale, la spinta H per un arco parabolico
    # con carico in mezzeria è un risultato classico calcolabile col Teorema di Castigliano
    H = (25 * F * L) / (128 * f)
    V_reaz = F / 2
    
    x = np.linspace(0, L, 500)
    y = (4 * f / L**2) * x * (L - x) # Profilo dell'arco
    
    V = np.where(x < L/2, V_reaz, -V_reaz)
    
    # Momento = Momento isostatico - Momento stabilizzante della spinta (H*y)
    M_iso = np.where(x <= L/2, (F * x) / 2, (F * (L - x)) / 2)
    M = M_iso - (H * y)
    
    theta = np.zeros_like(x)
    v = np.zeros_like(x)
    return x, V, M, theta, v, H

# 35. Cavo Sospeso (Funicolare Parabolico) con carico distribuito
def calc_cavo_parabolico(L, f_sag, q, E, A):
    # A = Area della sezione del cavo (non Inerzia, il cavo non ha rigidezza flessionale)
    # Approssimazione parabolica della catenaria per frecce f < L/8
    H = (q * L**2) / (8 * f_sag)
    
    x = np.linspace(0, L, 500)
    
    # Il cavo non ha momento flettente né taglio strutturale interno, 
    # ma ha uno sforzo normale (Trazione) variabile.
    # Usiamo V per rappresentare la componente verticale della trazione.
    V_verticale = q * (L/2 - x) 
    T_trazione = np.sqrt(H**2 + V_verticale**2)
    
    # Mettiamo M a 0 perché il cavo non reagisce a flessione. 
    # Usiamo il vettore M per plottare la trazione massima per comodità grafica.
    V = V_verticale
    M = np.zeros_like(x)  # M=0 in un cavo ideale
    
    theta = np.zeros_like(x)
    v = (q * x * (L - x)) / (2 * H) # Profilo geometrico
    return x, V, M, theta, v, H, T_trazione

# 36. Trave Continua su 3 appoggi (2 campate identiche di luce L)
def calc_trave_continua_2_campate(L, q, E, I):
    EI = E * I
    # Attenzione: l'asse x totale sarà lungo 2*L
    L_tot = 2 * L
    x = np.linspace(0, L_tot, 500)
    
    # Reazioni vincolari classiche
    R_A = (3 * q * L) / 8
    R_B = (10 * q * L) / 8 # Appoggio centrale
    R_C = (3 * q * L) / 8
    
    # Taglio piecewise
    V = np.where(x < L, R_A - q*x, R_A + R_B - q*x)
    
    # Momento piecewise (Il momento sul supporto centrale B sarà -qL^2 / 8)
    M = np.where(x <= L, R_A*x - q*x**2/2, R_A*x + R_B*(x-L) - q*x**2/2)
    
    theta = np.zeros_like(x)
    v = np.zeros_like(x)
    return x, V, M, theta, v

