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
def disegna_schema_statico(vincolo, carico, L_m, L1_m=0.0, L2_m=0.0, a_m=0.0, f_m=0.0):
    fig = go.Figure()
    
    # 1. Determino la lunghezza visiva totale
    L_draw = L_m
    appoggi = [] 
    
    if vincolo == "Trave Continua":
        if "3 Campate" in carico:
            L_draw = L_m * 3
            appoggi = [0, L_m, L_m*2, L_m*3]
        elif "Diverse" in carico:
            L_draw = L1_m + L2_m if (L1_m + L2_m) > 0 else 10
            appoggi = [0, L1_m, L_draw]
        else: # 2 campate uguali
            L_draw = L_m * 2
            appoggi = [0, L_m, L_draw]
    
    # Gestione limiti Y per non "schiacciare" archi molto alti
    y_max, y_min = 1.0, -1.0
    
    # 2. Disegno l'elemento strutturale
    if "Arco" in vincolo or "Cavo" in vincolo:
        h = f_m if f_m > 0 else L_draw * 0.2
        if "Cavo" in vincolo: h = -h
        
        x_curve = np.linspace(0, L_draw, 100)
        # Parabola esatta adattata al tuo input f_m
        y_curve = (4 * h / L_draw**2) * x_curve * (L_draw - x_curve)
        
        fig.add_trace(go.Scatter(x=x_curve, y=y_curve, mode='lines', line=dict(color='black', width=5), showlegend=False))
        fig.add_shape(type="line", x0=0, y0=0, x1=L_draw, y1=0, line=dict(color="gray", width=2, dash="dash"))
        
        # PALLINO BIANCO per Arco a 3 cerniere
        if vincolo == "Arco a 3 Cerniere":
            raggio = L_draw * 0.015
            fig.add_shape(type="circle", x0=L_draw/2 - raggio, y0=h - raggio, x1=L_draw/2 + raggio, y1=h + raggio, fillcolor="white", line_color="black", line_width=2)
        
        y_max = max(1.0, h + 0.5)
        y_min = min(-1.0, h - 0.5)
    else:
        fig.add_shape(type="line", x0=0, y0=0, x1=L_draw, y1=0, line=dict(color="black", width=6))

    # 3. Disegno i Vincoli
    if vincolo in ["Appoggio - Appoggio", "Arco a 2 Cerniere", "Arco a 3 Cerniere", "Cavo Sospeso"]:
        appoggi = [0, L_draw]
    elif vincolo == "Mensola":
        fig.add_shape(type="rect", x0=-L_draw*0.05, y0=-0.6, x1=0, y1=0.6, fillcolor="gray", line_color="black")
    elif "Incastro - Appoggio" in vincolo:
        fig.add_shape(type="rect", x0=-L_draw*0.05, y0=-0.6, x1=0, y1=0.6, fillcolor="gray", line_color="black")
        appoggi = [L_draw]
    elif vincolo == "Incastro - Incastro":
        fig.add_shape(type="rect", x0=-L_draw*0.05, y0=-0.6, x1=0, y1=0.6, fillcolor="gray", line_color="black")
        fig.add_shape(type="rect", x0=L_draw, y0=-0.6, x1=L_draw*1.05, y1=0.6, fillcolor="gray", line_color="black")
    elif vincolo == "Ponte Sospeso":
        pylon_h = f_m if f_m > 0 else L_draw * 0.25
        # Piloni
        fig.add_shape(type="line", x0=0, y0=-0.5, x1=0, y1=pylon_h, line=dict(color="black", width=4))
        fig.add_shape(type="line", x0=L_draw, y0=-0.5, x1=L_draw, y1=pylon_h, line=dict(color="black", width=4))
        # Impalcato
        fig.add_shape(type="line", x0=0, y0=0, x1=L_draw, y1=0, line=dict(color="black", width=6))
        # Fune Parabolica
        x_curve = np.linspace(0, L_draw, 100)
        y_curve = pylon_h - (4 * pylon_h / L_draw**2) * x_curve * (L_draw - x_curve)
        fig.add_trace(go.Scatter(x=x_curve, y=y_curve, mode='lines', line=dict(color='black', width=3), showlegend=False))
        # Pendini
        n_camp = int(L1_m) if L1_m > 0 else 6
        for i in range(1, n_camp):
            xh = i * (L_draw / n_camp)
            yh = pylon_h - (4 * pylon_h / L_draw**2) * xh * (L_draw - xh)
            fig.add_shape(type="line", x0=xh, y0=0, x1=xh, y1=yh, line=dict(color="gray", width=1))
        appoggi = [0, L_draw]
        y_max = max(1.0, pylon_h + 0.5)
    elif vincolo == "Mensola (Urto Dinamico)": # <-- MODIFICATO
        fig.add_shape(type="rect", x0=-L_draw*0.05, y0=-0.6, x1=0, y1=0.6, fillcolor="gray", line_color="black")
    elif vincolo == "Trave Gerber": # <-- NUOVO
        # Due appoggi per la trave principale, uno per quella sospesa
        appoggi = [0, L1_m, L_draw]
        # PALLINO BIANCO per la cerniera Gerber (tra L1 e l'ultimo appoggio)
        raggio = L_draw * 0.015
        fig.add_shape(type="circle", x0=(L1_m+L2_m)-raggio, y0=-raggio, x1=(L1_m+L2_m)+raggio, y1=+raggio, fillcolor="white", line_color="black", line_width=2) 

    elif vincolo == "Ponte ad Arco a Spinta Eliminata" or vincolo == "Ponte Langer":
        arch_h = f_m if f_m > 0 else L_draw * 0.25
        # Impalcato (Catena)
        fig.add_shape(type="line", x0=0, y0=0, x1=L_draw, y1=0, line=dict(color="black", width=6))
        # Arco Parabolico
        x_curve = np.linspace(0, L_draw, 100)
        y_curve = (4 * arch_h / L_draw**2) * x_curve * (L_draw - x_curve)
        fig.add_trace(go.Scatter(x=x_curve, y=y_curve, mode='lines', line=dict(color='black', width=4), showlegend=False))
        # Pendini
        n_camp = int(L1_m) if L1_m > 0 else 6
        for i in range(1, n_camp):
            xh = i * (L_draw / n_camp)
            yh = (4 * arch_h / L_draw**2) * xh * (L_draw - xh)
            fig.add_shape(type="line", x0=xh, y0=0, x1=xh, y1=yh, line=dict(color="gray", width=1))
        # Appoggi (di cui uno carrello perché la spinta è interna)
        appoggi = [0, L_draw]
        y_max = max(1.0, arch_h + 0.5)   

    for pos in appoggi:
        base = L_draw * 0.02 # I triangolini scalano con la lunghezza della trave
        fig.add_shape(type="path", path=f"M {pos-base} -0.5 L {pos+base} -0.5 L {pos} 0 Z", fillcolor="gray", line_color="black")

    # 4. Disegno i Carichi Visivi alle coordinate esatte
    if "Distribuito" in carico or "Fune" in carico or "Uniforme" in carico or "Totale" in carico or "Metà" in carico:
        x_start, x_end = 0, L_draw
        if "parziale" in carico or "Metà" in carico:
            if "sx" in carico or "Metà" in carico: x_end = a_m if a_m > 0 else L_draw/2
            else: x_start = a_m if a_m > 0 else L_draw/2
        elif "campata 1" in carico:
            x_end = L_m
            
        fig.add_shape(type="rect", x0=x_start, y0=0, x1=x_end, y1=0.4, fillcolor="rgba(30, 144, 255, 0.2)", line_color="blue")
        
        n_arrows = max(3, int((x_end - x_start) / (L_draw / 10 + 1e-5)))
        for x_arrow in np.linspace(x_start + (x_end-x_start)*0.05, x_end - (x_end-x_start)*0.05, n_arrows):
            fig.add_annotation(x=x_arrow, y=0, ax=x_arrow, ay=0.4, xref="x", yref="y", axref="x", ayref="y", showarrow=True, arrowhead=2, arrowcolor="blue")

    elif "Triangolare" in carico or "Trapezoidale" in carico:
        if "Sx" in carico: path = f"M 0 0 L 0 0.5 L {L_draw} 0 Z"
        elif "Punta" in carico and vincolo == "Mensola": path = f"M 0 0 L {L_draw} 0.5 L {L_draw} 0 Z"
        elif "Trapezoidale" in carico: path = f"M 0 0 L 0 0.5 L {L_draw} 0.2 L {L_draw} 0 Z"
        else: path = f"M 0 0 L {L_draw/2} 0.5 L {L_draw} 0 Z"
        fig.add_shape(type="path", path=path, fillcolor="rgba(30, 144, 255, 0.2)", line_color="blue")

    elif "Concentrato" in carico or "Chiave" in carico:
        pos_x = L_draw / 2 
        if "Punta" in carico: pos_x = L_draw
        elif "a distanza" in carico: pos_x = a_m if a_m > 0 else L_draw/2
        elif "campata 1" in carico: pos_x = L_m / 2
        
        pos_y = 0
        if "Arco" in vincolo and "Chiave" in carico:
            pos_y = f_m if f_m > 0 else L_draw * 0.2
        elif "Urto" in carico:
            # Disegna un blocco che cade
            fig.add_shape(type="rect", x0=L_draw-0.5, y0=0.5, x1=L_draw+0.5, y1=1.2, fillcolor="orange", line_color="red")
            fig.add_annotation(x=L_draw, y=0, ax=L_draw, ay=0.5, xref="x", yref="y", axref="x", ayref="y", showarrow=True, arrowhead=2, arrowsize=2, arrowcolor="red")
            fig.add_annotation(x=L_draw/2, y=0.5, text="💥 URTO DINAMICO", showarrow=False, font=dict(size=14, color="red", weight="bold"))
            
        fig.add_annotation(x=pos_x, y=pos_y, ax=pos_x, ay=pos_y+0.7, xref="x", yref="y", axref="x", ayref="y", showarrow=True, arrowhead=2, arrowsize=1.5, arrowwidth=3, arrowcolor="red")
        
        if "Due" in carico: 
            if "simmetrici" in carico:
                pos_x1 = a_m if a_m > 0 else L_draw/4
                pos_x2 = L_draw - pos_x1
            else:
                pos_x1 = a_m if a_m > 0 else L_draw/2
                pos_x2 = L_draw
            fig.add_annotation(x=pos_x1, y=0, ax=pos_x1, ay=0.7, xref="x", yref="y", axref="x", ayref="y", showarrow=True, arrowhead=2, arrowsize=1.5, arrowwidth=3, arrowcolor="red")
            if pos_x2 != pos_x1:
                fig.add_annotation(x=pos_x2, y=0, ax=pos_x2, ay=0.7, xref="x", yref="y", axref="x", ayref="y", showarrow=True, arrowhead=2, arrowsize=1.5, arrowwidth=3, arrowcolor="red")

    elif "Momento" in carico or "Termico" in carico or "Cedimento" in carico:
         icona = "🌡️" if "Termico" in carico else "📉" if "Cedimento" in carico else "🔄"
         pos_x = L_draw / 2
         if "Appoggio" in carico and "Incastro" in vincolo: pos_x = L_draw
         elif "Punta" in carico: pos_x = L_draw
         elif "A" in carico: pos_x = 0
         fig.add_annotation(x=pos_x, y=0.5, text=f"{icona} {carico}", showarrow=False, font=dict(size=14, color="purple"))

    fig.update_layout(xaxis=dict(range=[-L_draw*0.05, L_draw*1.05], visible=False), 
                      yaxis=dict(range=[y_min, y_max], visible=False), 
                      height=180, margin=dict(l=0, r=0, t=10, b=10), plot_bgcolor="white")
    return fig

def crea_4_grafici_plotly(x, V, M, theta, v):
    fig = make_subplots(rows=4, cols=1, shared_xaxes=True, vertical_spacing=0.05,
                        subplot_titles=("Taglio (V) [kN]", "Momento Flettente (M) [kNm]", "Rotazione (θ) [mrad]", "Deformata (v) [mm]"))

    fig.add_trace(go.Scatter(x=x, y=V, fill='tozeroy', mode='lines', line=dict(color='red', width=2), fillcolor='rgba(255,0,0,0.3)', name='Taglio'), row=1, col=1)
    fig.add_trace(go.Scatter(x=x, y=M, fill='tozeroy', mode='lines', line=dict(color='blue', width=2), fillcolor='rgba(0,0,255,0.3)', name='Momento'), row=2, col=1)
    # Rotazione (Cambiata in Viola per distinguerla)
    fig.add_trace(go.Scatter(x=x, y=theta, mode='lines', line=dict(color='purple', width=2), name='Rotazione'), row=3, col=1)
    
    # Deformata (Linea semplice Verde, senza fillcolor)
    fig.add_trace(go.Scatter(x=x, y=v, mode='lines', line=dict(color='green', width=2), name='Deformata'), row=4, col=1)

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
    
    # Equazione esatta della deformata a tratti
    v = np.where(x <= a, 
                 (F * b * x / (6 * L * EI)) * (L**2 - b**2 - x**2), 
                 (F * a * (L - x) / (6 * L * EI)) * (L**2 - a**2 - (L - x)**2))
    theta = np.zeros_like(x) # Lasciamo theta a 0 per brevità
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
    
    # Equazione esatta della deformata a tratti
    v = np.where(x <= a, 
                 (F * x**2 / (6 * EI)) * (3*a - x), 
                 (F * a**2 / (6 * EI)) * (3*x - a))
    theta = np.zeros_like(x)
    return x, V, M, theta, v

# 16. Mensola: Momento M0 applicato in punta
def calc_mensola_momento_punta(L, M0, E, I):
    EI = E * I
    x = np.linspace(0, L, 500)
    V = np.zeros_like(x)
    M = np.full_like(x, -M0)
    theta = (M0 * x) / EI
    # Equazione parabolica esatta
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
    L_tot = 2 * L
    x = np.linspace(0, L_tot, 500)
    
    R_A = (3 * q * L) / 8
    R_B = (10 * q * L) / 8
    
    V = np.where(x < L, R_A - q*x, R_A + R_B - q*x)
    M = np.where(x <= L, R_A*x - q*x**2/2, R_A*x + R_B*(x-L) - q*x**2/2)
    
    # Deformata esatta per la campata continua
    v = np.where(x <= L,
                 (q * x / (48 * EI)) * (L**3 - 3*L*x**2 + 2*x**3),
                 (q * (L_tot - x) / (48 * EI)) * (L**3 - 3*L*(L_tot - x)**2 + 2*(L_tot - x)**3))
    theta = np.zeros_like(x)
    return x, V, M, theta, v

# ==========================================
# CALCOLO TERMICO E CEDIMENTI (ISOSTATICI)
# ==========================================

# Trave appoggiata con gradiente termico (Isostatica)
def calc_appoggio_termico(L, deltaT, h, alpha, E, I):
    x = np.linspace(0, L, 500)
    V = np.zeros_like(x) # Nessun taglio
    M = np.zeros_like(x) # Nessun momento
    
    # Curvatura termica costante. La deformata è una parabola esatta.
    v = (alpha * deltaT / (2 * h)) * x * (L - x)
    theta = (alpha * deltaT / (2 * h)) * (L - 2 * x)
    return x, V, M, theta, v

# Trave appoggiata con cedimento dell'appoggio destro (Isostatica)
def calc_appoggio_cedimento(L, delta, E, I):
    x = np.linspace(0, L, 500)
    V = np.zeros_like(x) # Nessun sforzo
    M = np.zeros_like(x)
    
    # Moto rigido: la trave si inclina ma non si flette. È una linea retta.
    v = delta * (x / L)
    theta = np.full_like(x, delta / L)
    return x, V, M, theta, v

# 37. Trave Continua a 2 Campate DIVERSE (L1, L2) con carico uniforme totale
def calc_continua_2_campate_diverse_q(L1, L2, q, E, I):
    L_tot = L1 + L2
    x = np.linspace(0, L_tot, 500)
    
    # Momento sull'appoggio centrale B (Teorema di Clapeyron)
    M_B = - (q * (L1**3 + L2**3)) / (8 * (L1 + L2))
    
    # Reazioni vincolari
    R_A = (q * L1 / 2) + (M_B / L1)
    V_B_sx = (q * L1 / 2) - (M_B / L1)
    V_B_dx = (q * L2 / 2) - (M_B / L2)
    R_C = (q * L2 / 2) + (M_B / L2)
    R_B = V_B_sx + V_B_dx
    
    V = np.where(x < L1, R_A - q*x, R_A + R_B - q*x)
    M = np.where(x <= L1, R_A*x - q*x**2/2, R_A*x + R_B*(x-L1) - q*x**2/2)
    
    theta = np.zeros_like(x)
    v = np.zeros_like(x)
    return x, V, M, theta, v

# 38. Trave Continua a 2 Campate UGUALI (L), carico uniforme SOLO sulla prima campata
def calc_continua_2_campate_q_parziale(L, q, E, I):
    L_tot = 2 * L
    x = np.linspace(0, L_tot, 500)
    
    M_B = - (q * L**2) / 16
    R_A = (7 * q * L) / 16
    R_B = (10 * q * L) / 16
    R_C = - (q * L) / 16
    
    # Il taglio nella campata 2 è costante pari a R_C
    V = np.where(x < L, R_A - q*x, R_A + R_B - q*L)
    M = np.where(x <= L, R_A*x - q*x**2/2, M_B - R_C*(x-L))
    
    theta = np.zeros_like(x)
    v = np.zeros_like(x)
    return x, V, M, theta, v

# 39. Trave Continua a 2 Campate UGUALI (L), carico concentrato F in mezzeria della prima campata
def calc_continua_2_campate_F_mezzeria(L, F, E, I):
    L_tot = 2 * L
    x = np.linspace(0, L_tot, 500)
    
    M_B = - (3 * F * L) / 32
    R_A = (13 * F) / 32
    R_B = (22 * F) / 32
    R_C = - (3 * F) / 32
    
    V = np.where(x < L/2, R_A, np.where(x < L, R_A - F, -R_C))
    M = np.where(x <= L/2, R_A*x, np.where(x <= L, R_A*x - F*(x - L/2), M_B - R_C*(x-L)))
    
    theta = np.zeros_like(x)
    v = np.zeros_like(x)
    return x, V, M, theta, v

# 40. Trave Continua a 3 Campate UGUALI (L), carico uniforme totale
def calc_continua_3_campate_q(L, q, E, I):
    L_tot = 3 * L
    x = np.linspace(0, L_tot, 500)
    
    M_B = - (q * L**2) / 10
    M_C = M_B
    R_A = 0.4 * q * L
    R_B = 1.1 * q * L
    R_C = 1.1 * q * L
    R_D = 0.4 * q * L
    
    V = np.where(x < L, R_A - q*x, np.where(x < 2*L, R_A + R_B - q*x, R_A + R_B + R_C - q*x))
    M = np.where(x <= L, R_A*x - q*x**2/2, np.where(x <= 2*L, R_A*x + R_B*(x-L) - q*x**2/2, R_A*x + R_B*(x-L) + R_C*(x-2*L) - q*x**2/2))
    
    theta = np.zeros_like(x)
    v = np.zeros_like(x)
    return x, V, M, theta, v

# ==========================================
# PONTI SOSPESI E ARCHI A SPINTA ELIMINATA
# ==========================================

def calc_ponte_sospeso(L, f_sag, q, n_campate, E, I):
    # n_campate è il numero di intervalli tra le sospensioni
    L1 = L / n_campate
    
    # Formule globali della Fune (dai dati dell'immagine)
    H = (q * L**2) / (8 * f_sag)
    V_reaz = (q * L) / 2
    T_max = np.sqrt(H**2 + V_reaz**2)
    
    # Sforzo di trazione su singola sospensione S
    S = q * L1
    
    # Array per i grafici dell'impalcato
    x = np.linspace(0, L, 500)
    V = np.zeros_like(x)
    M = np.zeros_like(x)
    
    # Calcolo dei grafici "Locali" dell'impalcato (concio L1)
    for i in range(int(n_campate)):
        x_start = i * L1
        x_end = (i + 1) * L1
        mask = (x >= x_start) & (x <= x_end)
        x_local = x[mask] - x_start
        
        # Taglio locale: zero in mezzeria, massimo sugli appoggi (pendini)
        V[mask] = (q * L1 / 2) - q * x_local
        # Momento locale: M_incastro = qL1^2/12 (come da immagine)
        M[mask] = (q * L1 * x_local / 2) - (q * x_local**2 / 2) - (q * L1**2 / 12)

    theta = np.zeros_like(x)
    v = np.zeros_like(x)
    return x, V, M, theta, v, H, T_max, S

def calc_arco_spinta_eliminata(L, f_arco, q, n_campate, E, I):
    L1 = L / n_campate
    
    # La spinta H è interamente assorbita dall'impalcato che funge da tirante (catena)
    H = (q * L**2) / (8 * f_arco) 
    
    # Sforzo di trazione su singolo pendino S
    S = q * L1
    
    x = np.linspace(0, L, 500)
    V = np.zeros_like(x)
    M = np.zeros_like(x)
    
    # Calcolo dei grafici Locali dell'impalcato (come per il ponte sospeso)
    for i in range(int(n_campate)):
        x_start = i * L1
        x_end = (i + 1) * L1
        mask = (x >= x_start) & (x <= x_end)
        x_local = x[mask] - x_start
        
        V[mask] = (q * L1 / 2) - q * x_local
        M[mask] = (q * L1 * x_local / 2) - (q * x_local**2 / 2) - (q * L1**2 / 12)

    theta = np.zeros_like(x)
    v = np.zeros_like(x)
    return x, V, M, theta, v, H, S

# 43. PONTE LANGER (Carico Totale)
def calc_ponte_langer_totale(L, f, q, E, I):
    # Con carico totale uniforme, l'arco parabolico è funicolare del carico.
    # Spinta massima, Momento flettente teorico macroscopico nullo.
    H = (q * L**2) / (8 * f)
    x = np.linspace(0, L, 500)
    
    V = np.zeros_like(x)
    M = np.zeros_like(x)
    theta = np.zeros_like(x)
    v = np.zeros_like(x)
    
    return x, V, M, theta, v, H

# 44. PONTE LANGER (Carico su Metà Luce)
def calc_ponte_langer_meta(L, f, q, E, I):
    # La spinta H è dimezzata rispetto al carico totale
    H = (q * L**2) / (16 * f)
    x = np.linspace(0, L, 500)
    
    # Reazioni e Taglio/Momento Isostatici (come trave appoggiata con carico a metà)
    R_A = (3 * q * L) / 8
    R_B = (q * L) / 8
    
    V_iso = np.where(x < L/2, R_A - q*x, -R_B)
    M_iso = np.where(x <= L/2, R_A*x - q*x**2/2, R_B*(L-x))
    
    # Geometria dell'arco parabolico e sua derivata (inclinazione)
    y = (4 * f / L**2) * x * (L - x)
    y_prime = (4 * f / L**2) * (L - 2*x)
    
    # Gli sforzi flettenti e taglianti passano interamente all'elemento rigido
    # (Catena rigida o Arco rigido)
    V = V_iso - H * y_prime
    M = M_iso - H * y
    
    theta = np.zeros_like(x)
    v = np.zeros_like(x)
    
    return x, V, M, theta, v, H

# ==========================================
# CATEGORIE SPECIALI (GERBER, URTI, ROTAZIONI, FUNI SFALSATE)
# ==========================================

# 45. TRAVE GERBER (Appoggio, Appoggio, Sbalzo con Cerniera, Appoggio)
def calc_gerber_standard(L1, L2, L3, q, E, I):
    # L1 = luce prima campata, L2 = sbalzo fino alla cerniera, L3 = campata sospesa
    L_tot = L1 + L2 + L3
    x = np.linspace(0, L_tot, 500)
    
    # 1. Risolvo la campata sospesa (isostatica appoggiata sulla cerniera e sul rullo finale)
    V_cerniera = (q * L3) / 2  # Reazione trasmessa allo sbalzo
    R_D = (q * L3) / 2         # Reazione appoggio finale
    
    # 2. Risolvo la trave principale con lo sbalzo (che ora subisce q + il carico concentrato V_cerniera)
    # Equilibrio alla rotazione in A per trovare R_B:
    R_B = (q * (L1 + L2)**2 / 2 + V_cerniera * (L1 + L2)) / L1
    R_A = q * (L1 + L2) + V_cerniera - R_B
    
    # 3. Costruisco le equazioni a tratti
    V = np.where(x < L1, R_A - q*x, 
                 np.where(x < L1 + L2, R_A + R_B - q*x, 
                          V_cerniera - q*(x - (L1+L2))))
    
    M = np.where(x < L1, R_A*x - q*x**2/2, 
                 np.where(x <= L1 + L2, R_A*x + R_B*(x-L1) - q*x**2/2, 
                          V_cerniera*(x - (L1+L2)) - q*(x - (L1+L2))**2/2))
    
    theta, v = np.zeros_like(x), np.zeros_like(x)
    return x, V, M, theta, v

# 46. URTO SU MENSOLA (Massa M che cade da altezza h in punta)
def calc_urto_mensola(L, massa_kg, h_caduta, E, I):
    g = 9.81
    Forza_statica = massa_kg * g
    
    # Spostamento statico in punta
    v_st = (Forza_statica * L**3) / (3 * E * I)
    
    # Coefficiente di Amplificazione Dinamica (K_d)
    K_d = 1 + np.sqrt(1 + (2 * h_caduta) / v_st)
    
    # Forza Dinamica Equivalente
    F_eq = Forza_statica * K_d
    
    x = np.linspace(0, L, 500)
    V = np.full_like(x, F_eq)
    M = -F_eq * (L - x)
    
    theta = (F_eq / (2 * E * I)) * (2*L*x - x**2)
    v = (F_eq * x**2 / (6 * E * I)) * (3*L - x)
    
    return x, V, M, theta, v, K_d, F_eq

# 47. INCASTRO-APPOGGIO CON ROTAZIONE IMPOSITA ALL'INCASTRO
def calc_incastro_appoggio_rotazione(L, phi_rad, E, I):
    # phi_rad positivo = rotazione antioraria dell'incastro
    x = np.linspace(0, L, 500)
    
    M_A = (3 * E * I * phi_rad) / L
    R_A = -(3 * E * I * phi_rad) / L**2
    R_B = (3 * E * I * phi_rad) / L**2
    
    V = np.full_like(x, R_A)
    M = M_A + R_A * x
    
    theta = phi_rad * (1 - 4*(x/L) + 3*(x/L)**2)
    v = phi_rad * x * (1 - x/L)**2
    
    return x, V, M, theta, v

# 48. FUNE SOSPESA CON APPOGGI SFALSATI (Dislivello h)
def calc_fune_sfalsata(L, f_sag, dislivello_h, q, E, A):
    # Il dislivello h altera le reazioni verticali ma non la spinta orizzontale
    H = (q * L**2) / (8 * f_sag)
    
    x = np.linspace(0, L, 500)
    
    # V rappresenta la componente verticale della trazione
    V_verticale = (q * L / 2) - H * (dislivello_h / L) - q * x
    T_trazione = np.sqrt(H**2 + V_verticale**2)
    
    V = V_verticale
    M = np.zeros_like(x)
    theta = np.zeros_like(x)
    
    # Geometria della fune
    v = (dislivello_h / L) * x + (q * x * (L - x)) / (2 * H)
    
    return x, V, M, theta, v, H, T_trazione