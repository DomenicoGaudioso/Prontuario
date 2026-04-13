import streamlit as st
import numpy as np
from src_code import *
from src_code import genera_pdf_prontuario

st.set_page_config(page_title="Prontuario Strutturale", layout="wide")
st.title("Prontuario delle Travi Semplici 🏗️")

# --- SIDEBAR ---
# --- SIDEBAR E LOGICA DEI MENU DIPENDENTI ---
# Dizionario che associa ad ogni vincolo solo i suoi carichi specifici
# Dizionario che associa ad ogni vincolo solo i suoi carichi specifici
MAPPA_SCHEMI = {
    "Appoggio - Appoggio": [
        "Uniformemente Distribuito", "Concentrato in Mezzeria", "Triangolare",
        "Gradiente Termico", "Cedimento Appoggio Destro"
    ],
    "Mensola": [
        "Concentrato in Punta", "Uniformemente Distribuito", "Triangolare"
    ],
    "Incastro - Appoggio": [
        "Uniformemente Distribuito", "Concentrato in Mezzeria"
    ],
    "Incastro - Incastro": [
        "Uniformemente Distribuito", "Concentrato in Mezzeria", 
        "Concentrato a distanza a", "Triangolare Max Sx", "Momento in Mezzeria",
        "Gradiente Termico", "Cedimento Verticale Appoggio"
    ],
    "Arco a 3 Cerniere": ["Carico in Chiave"],
    "Arco a 2 Cerniere": ["Carico in Chiave"],
    "Cavo Sospeso": ["Carico Distribuito (Fune)"],
    "Trave Continua": [
        "2 Campate con Carico Distribuito",
        "2 Campate Diverse (Uniforme totale)", 
        "2 Campate Uguali (Uniforme solo su campata 1)", 
        "2 Campate Uguali (Concentrato in campata 1)", 
        "3 Campate Uguali (Uniforme totale)"
],
    "Ponte Sospeso": ["Impalcato con Carico Uniforme"],
    "Ponte ad Arco a Spinta Eliminata": ["Impalcato con Carico Uniforme"],
    "Ponte Langer": [
        "Catena Rigida - Carico Totale",
        "Catena Rigida - Carico a Metà",
        "Arco Rigido - Carico Totale",
        "Arco Rigido - Carico a Metà"
    ],
"Trave Gerber": ["Uniforme totale con Cerniera"],
    "Mensola (Urto Dinamico)": ["Caduta Massa in Punta"],
    "Incastro - Appoggio": [
        "Uniformemente Distribuito", "Concentrato in Mezzeria", "Rotazione Incastro"
    ],
    "Cavo Sospeso": ["Carico Distribuito (Fune)", "Fune con Appoggi Sfalsati"]
}

st.sidebar.header("Impostazioni Struttura")

# Il primo menu seleziona il vincolo
vincolo = st.sidebar.selectbox("Schema Statico dei Vincoli:", list(MAPPA_SCHEMI.keys()))

# Il secondo menu legge cosa hai scelto nel primo e ti mostra solo le opzioni valide!
carico = st.sidebar.selectbox("Tipologia di Carico/Azione:", MAPPA_SCHEMI[vincolo])

st.sidebar.markdown("---")


st.sidebar.markdown("---")
E_mpa = st.sidebar.number_input("Modulo Elastico E (MPa)", value=210000.0, step=1000.0)
I_cm4 = st.sidebar.number_input("Momento Inerzia I (cm⁴)", value=1000.0, step=10.0)

st.header(f"Schema: {vincolo} | Carico: {carico}")
# Creo un segnaposto vuoto. Lo riempirò con l'immagine SOLO dopo che l'utente ha messo i numeri!
schema_placeholder = st.empty()

# Inizializzo a zero le variabili speciali che potrebbero non esserci in tutti i casi
L_m, L1_m, L2_m, a_m, f_m = 4.0, 0.0, 0.0, 0.0, 0.0

col_teoria, col_input = st.columns([1.5, 1])
x_mm, V_n, M_nmm, theta_rad, v_mm = None, None, None, None, None

# Conversioni iniziali
E = E_mpa
I = I_cm4 * 10000

# =========================================================
# BLOCCHI CONDIZIONALI (10 CASI)
# =========================================================

# 1. APPOGGIO - DISTRIBUITO
if vincolo == "Appoggio - Appoggio" and carico == "Uniformemente Distribuito":
    with col_teoria:
        st.markdown(r"**Taglio:** $$V(x) = \frac{qL}{2} - qx$$")
        st.markdown(r"**Momento:** $$M(x) = \frac{qx}{2}(L - x)$$")
        st.markdown(r"**Deformata:** $$v(x) = \frac{qx}{24EI} (L^3 - 2Lx^2 + x^3)$$")
    with col_input:
        L_m = st.number_input("Luce L (m)", 4.0)
        q_kn = st.number_input("Carico q (kN/m)", 10.0)
        x_mm, V_n, M_nmm, theta_rad, v_mm = calc_appoggio_distribuito(L_m*1000, q_kn, E, I)

# 2. APPOGGIO - CONCENTRATO MEZZERIA
elif vincolo == "Appoggio - Appoggio" and carico == "Concentrato in Mezzeria":
    with col_teoria:
        st.markdown(r"**Taglio:** $$V(x) = \pm \frac{F}{2}$$")
        st.markdown(r"**Momento max:** $$M_{max} = \frac{FL}{4}$$")
        st.markdown(r"**Deformata max:** $$v_{max} = \frac{FL^3}{48EI}$$")
    with col_input:
        L_m = st.number_input("Luce L (m)", 4.0)
        F_kn = st.number_input("Carico F (kN)", 50.0)
        x_mm, V_n, M_nmm, theta_rad, v_mm = calc_appoggio_concentrato_mezzeria(L_m*1000, F_kn*1000, E, I)

# 3. APPOGGIO - TRIANGOLARE
elif vincolo == "Appoggio - Appoggio" and carico == "Triangolare":
    with col_teoria:
        st.markdown(r"**Taglio:** $$V(x) = \frac{qL}{6} - \frac{qx^2}{2L}$$")
        st.markdown(r"**Momento:** $$M(x) = \frac{qLx}{6} - \frac{qx^3}{6L}$$")
    with col_input:
        L_m = st.number_input("Luce L (m)", 4.0)
        q_kn = st.number_input("Carico max q (kN/m)", 10.0)
        x_mm, V_n, M_nmm, theta_rad, v_mm = calc_appoggio_triangolare(L_m*1000, q_kn, E, I)

# 4. MENSOLA - CONCENTRATO PUNTA
elif vincolo == "Mensola" and carico == "Concentrato in Punta":
    with col_teoria:
        st.markdown(r"**Taglio:** $$V(x) = F$$")
        st.markdown(r"**Momento:** $$M(x) = -F(L - x)$$")
        st.markdown(r"**Deformata:** $$v(x) = \frac{Fx^2}{6EI} (3L - x)$$")
    with col_input:
        L_m = st.number_input("Luce L (m)", 2.0)
        F_kn = st.number_input("Carico F (kN)", 50.0)
        x_mm, V_n, M_nmm, theta_rad, v_mm = calc_mensola_concentrato_punta(L_m*1000, F_kn*1000, E, I)

# 5. MENSOLA - DISTRIBUITO
elif vincolo == "Mensola" and carico == "Uniformemente Distribuito":
    with col_teoria:
        st.markdown(r"**Taglio:** $$V(x) = q(L - x)$$")
        st.markdown(r"**Momento:** $$M(x) = -\frac{q(L - x)^2}{2}$$")
        st.markdown(r"**Deformata:** $$v(x) = \frac{qx^2}{24EI} (x^2 - 4Lx + 6L^2)$$")
    with col_input:
        L_m = st.number_input("Luce L (m)", 2.0)
        q_kn = st.number_input("Carico q (kN/m)", 10.0)
        x_mm, V_n, M_nmm, theta_rad, v_mm = calc_mensola_distribuito(L_m*1000, q_kn, E, I)

# 6. MENSOLA - TRIANGOLARE
elif vincolo == "Mensola" and carico == "Triangolare":
    with col_teoria:
        st.markdown(r"**Taglio:** $$V(x) = \frac{q}{2L}(L - x)^2$$")
        st.markdown(r"**Momento:** $$M(x) = -\frac{q}{6L}(L - x)^3$$")
    with col_input:
        L_m = st.number_input("Luce L (m)", 2.0)
        q_kn = st.number_input("Carico max q (kN/m)", 10.0)
        x_mm, V_n, M_nmm, theta_rad, v_mm = calc_mensola_triangolare(L_m*1000, q_kn, E, I)

# 7. INCASTRO/APPOGGIO - DISTRIBUITO
elif vincolo == "Incastro - Appoggio" and carico == "Uniformemente Distribuito":
    with col_teoria:
        st.markdown(r"**Taglio:** $$V(x) = \frac{5qL}{8} - qx$$")
        st.markdown(r"**Momento:** $$M(x) = -\frac{qL^2}{8} + \frac{5qLx}{8} - \frac{qx^2}{2}$$")
    with col_input:
        L_m = st.number_input("Luce L (m)", 4.0)
        q_kn = st.number_input("Carico q (kN/m)", 10.0)
        x_mm, V_n, M_nmm, theta_rad, v_mm = calc_incastro_appoggio_distribuito(L_m*1000, q_kn, E, I)

# 8. INCASTRO/APPOGGIO - CONCENTRATO MEZZERIA
elif vincolo == "Incastro - Appoggio" and carico == "Concentrato in Mezzeria":
    with col_teoria:
        st.markdown(r"**Reazione Incastro:** $$R_A = \frac{11F}{16}$$")
        st.markdown(r"**Momento Incastro:** $$M_A = -\frac{3FL}{16}$$")
    with col_input:
        L_m = st.number_input("Luce L (m)", 4.0)
        F_kn = st.number_input("Carico F (kN)", 50.0)
        x_mm, V_n, M_nmm, theta_rad, v_mm = calc_incastro_appoggio_concentrato(L_m*1000, F_kn*1000, E, I)

# 9. INCASTRO/INCASTRO - DISTRIBUITO
elif vincolo == "Incastro - Incastro" and carico == "Uniformemente Distribuito":
    with col_teoria:
        st.markdown(r"**Taglio:** $$V(x) = q(\frac{L}{2} - x)$$")
        st.markdown(r"**Momento:** $$M(x) = \frac{q}{12}(6Lx - 6x^2 - L^2)$$")
        st.markdown(r"**Deformata:** $$v(x) = \frac{qx^2}{24EI} (L - x)^2$$")
    with col_input:
        L_m = st.number_input("Luce L (m)", 4.0)
        q_kn = st.number_input("Carico q (kN/m)", 10.0)
        x_mm, V_n, M_nmm, theta_rad, v_mm = calc_incastro_incastro_distribuito(L_m*1000, q_kn, E, I)

# 10. INCASTRO/INCASTRO - CONCENTRATO MEZZERIA
elif vincolo == "Incastro - Incastro" and carico == "Concentrato in Mezzeria":
    with col_teoria:
        st.markdown(r"**Momento Incastri:** $$M_A = M_B = -\frac{FL}{8}$$")
        st.markdown(r"**Momento Mezzeria:** $$M_{max} = \frac{FL}{8}$$")
    with col_input:
        L_m = st.number_input("Luce L (m)", 4.0)
        F_kn = st.number_input("Carico F (kN)", 50.0)
        x_mm, V_n, M_nmm, theta_rad, v_mm = calc_incastro_incastro_concentrato(L_m*1000, F_kn*1000, E, I)

# 11. APPOGGIO - CONCENTRATO DISTANZA A
elif vincolo == "Appoggio - Appoggio" and carico == "Concentrato a distanza a":
    with col_teoria:
        st.markdown(r"**Taglio:** $V_A = \frac{Fb}{L}$ ; $V_B = -\frac{Fa}{L}$")
        st.markdown(r"**Momento Max:** $M_{max} = \frac{Fab}{L}$ in x=a")
    with col_input:
        L_m = st.number_input("Luce L (m)", 4.0)
        a_m = st.number_input("Distanza a (m)", 1.0)
        F_kn = st.number_input("Carico F (kN)", 50.0)
        x_mm, V_n, M_nmm, theta_rad, v_mm = calc_appoggio_concentrato_a(L_m*1000, F_kn*1000, a_m*1000, E, I)

# 12. APPOGGIO - MOMENTO IN A
elif vincolo == "Appoggio - Appoggio" and carico == "Momento in Appoggio":
    with col_teoria:
        st.markdown(r"**Taglio:** $V(x) = -\frac{M_0}{L}$")
        st.markdown(r"**Momento:** $M(x) = M_0 (1 - \frac{x}{L})$")
    with col_input:
        L_m = st.number_input("Luce L (m)", 4.0)
        M0_knm = st.number_input("Momento M0 (kNm)", 20.0)
        x_mm, V_n, M_nmm, theta_rad, v_mm = calc_appoggio_momento_A(L_m*1000, M0_knm*1000000, E, I)

# 13. APPOGGIO - DUE CARICHI SIMMETRICI
elif vincolo == "Appoggio - Appoggio" and carico == "Due carichi simmetrici":
    with col_teoria:
        st.markdown(r"**Taglio max:** $V = \pm F$")
        st.markdown(r"**Momento Costante Centrale:** $M = F \cdot a$")
    with col_input:
        L_m = st.number_input("Luce L (m)", 4.0)
        a_m = st.number_input("Distanza carichi dagli appoggi a (m)", 1.0)
        F_kn = st.number_input("Valore di ogni F (kN)", 20.0)
        x_mm, V_n, M_nmm, theta_rad, v_mm = calc_appoggio_2F_simmetrici(L_m*1000, F_kn*1000, a_m*1000, E, I)

# 14. APPOGGIO - TRIANGOLARE SIMMETRICO
elif vincolo == "Appoggio - Appoggio" and carico == "Triangolare Simmetrico":
    with col_teoria:
        st.markdown(r"**Taglio:** Max in appoggio $V = \frac{qL}{4}$")
        st.markdown(r"**Momento:** $M_{max} = \frac{qL^2}{12}$")
    with col_input:
        L_m = st.number_input("Luce L (m)", 4.0)
        q_kn = st.number_input("Carico max in mezzeria q (kN/m)", 10.0)
        x_mm, V_n, M_nmm, theta_rad, v_mm = calc_appoggio_triangolare_simmetrico(L_m*1000, q_kn, E, I)

# 15. MENSOLA - CONCENTRATO DISTANZA A
elif vincolo == "Mensola" and carico == "Concentrato a distanza a":
    with col_teoria:
        st.markdown(r"**Taglio:** $V(x) = F$ per $x < a$")
        st.markdown(r"**Momento Incastro:** $M_A = -F \cdot a$")
    with col_input:
        L_m = st.number_input("Luce L (m)", 3.0)
        a_m = st.number_input("Distanza carico da incastro a (m)", 2.0)
        F_kn = st.number_input("Carico F (kN)", 50.0)
        x_mm, V_n, M_nmm, theta_rad, v_mm = calc_mensola_concentrato_a(L_m*1000, F_kn*1000, a_m*1000, E, I)

# 16. MENSOLA - MOMENTO IN PUNTA
elif vincolo == "Mensola" and carico == "Momento in Punta":
    with col_teoria:
        st.markdown(r"**Taglio:** $V(x) = 0$")
        st.markdown(r"**Momento:** $M(x) = -M_0$ (Costante)")
    with col_input:
        L_m = st.number_input("Luce L (m)", 2.0)
        M0_knm = st.number_input("Momento M0 in punta (kNm)", 15.0)
        x_mm, V_n, M_nmm, theta_rad, v_mm = calc_mensola_momento_punta(L_m*1000, M0_knm*1000000, E, I)

# 17. MENSOLA - DISTRIBUITO PARZIALE
elif vincolo == "Mensola" and carico == "Distribuito parziale":
    with col_teoria:
        st.markdown(r"**Taglio Max Incastro:** $V_A = q(L-a)$")
        st.markdown(r"**Momento Incastro:** $M_A = -q\frac{(L-a)(L+a)}{2}$")
    with col_input:
        L_m = st.number_input("Luce L (m)", 4.0)
        a_m = st.number_input("Inizio carico da incastro a (m)", 2.0)
        q_kn = st.number_input("Carico q (kN/m)", 10.0)
        x_mm, V_n, M_nmm, theta_rad, v_mm = calc_mensola_distribuito_parziale(L_m*1000, q_kn, a_m*1000, E, I)

# 18. MENSOLA - TRIANGOLARE PUNTA
elif vincolo == "Mensola" and carico == "Triangolare Max Punta":
    with col_teoria:
        st.markdown(r"**Taglio Incastro:** $V_A = \frac{qL}{2}$")
        st.markdown(r"**Momento Incastro:** $M_A = -\frac{qL^2}{3}$")
    with col_input:
        L_m = st.number_input("Luce L (m)", 2.0)
        q_kn = st.number_input("Carico max in punta q (kN/m)", 10.0)
        x_mm, V_n, M_nmm, theta_rad, v_mm = calc_mensola_triangolare_punta(L_m*1000, q_kn, E, I)

# 19. INCASTRO/APPOGGIO - MOMENTO IN B
elif vincolo == "Incastro - Appoggio" and carico == "Momento in Appoggio":
    with col_teoria:
        st.markdown(r"**Momento Incastro:** $M_A = \frac{M_0}{2}$")
        st.markdown(r"**Taglio:** $V(x) = -\frac{3M_0}{2L}$")
    with col_input:
        L_m = st.number_input("Luce L (m)", 4.0)
        M0_knm = st.number_input("Momento appoggio destro M0 (kNm)", 20.0)
        x_mm, V_n, M_nmm, theta_rad, v_mm = calc_incastro_appoggio_momento_B(L_m*1000, M0_knm*1000000, E, I)

# 20. INCASTRO/INCASTRO - CONCENTRATO DISTANZA A
elif vincolo == "Incastro - Incastro" and carico == "Concentrato a distanza a":
    with col_teoria:
        st.markdown(r"**Momento Incastro sx:** $M_A = -\frac{F \cdot a \cdot b^2}{L^2}$")
        st.markdown(r"**Momento Incastro dx:** $M_B = -\frac{F \cdot a^2 \cdot b}{L^2}$")
    with col_input:
        L_m = st.number_input("Luce L (m)", 4.0)
        a_m = st.number_input("Distanza carico da incastro sx a (m)", 1.0)
        F_kn = st.number_input("Carico F (kN)", 50.0)
        x_mm, V_n, M_nmm, theta_rad, v_mm = calc_incastro_incastro_concentrato_a(L_m*1000, F_kn*1000, a_m*1000, E, I)

# 21. APPOGGIO - DISTRIBUITO PARZIALE SX
elif vincolo == "Appoggio - Appoggio" and carico == "Distribuito parziale sx":
    with col_teoria:
        st.markdown(r"**Reazione A:** $R_A = \frac{qa}{L}(L - \frac{a}{2})$")
        st.markdown(r"**Reazione B:** $R_B = \frac{qa^2}{2L}$")
    with col_input:
        L_m = st.number_input("Luce L (m)", 4.0)
        a_m = st.number_input("Estensione carico a (m)", 2.0)
        q_kn = st.number_input("Carico q (kN/m)", 10.0)
        x_mm, V_n, M_nmm, theta_rad, v_mm = calc_appoggio_distribuito_parziale_sx(L_m*1000, q_kn, a_m*1000, E, I)

# 22. APPOGGIO - MOMENTO IN MEZZERIA
elif vincolo == "Appoggio - Appoggio" and carico == "Momento in Mezzeria":
    with col_teoria:
        st.markdown(r"**Taglio:** $V = -\frac{M_0}{L}$")
        st.markdown(r"**Salto di Momento:** $M(L/2^+) - M(L/2^-) = M_0$")
    with col_input:
        L_m = st.number_input("Luce L (m)", 4.0)
        M0_knm = st.number_input("Momento M0 (kNm)", 15.0)
        x_mm, V_n, M_nmm, theta_rad, v_mm = calc_appoggio_momento_mezzeria(L_m*1000, M0_knm*1000000, E, I)

# 23. APPOGGIO - FLESSIONE PURA
elif vincolo == "Appoggio - Appoggio" and carico == "Flessione Pura":
    with col_teoria:
        st.markdown(r"**Taglio:** $V(x) = 0$")
        st.markdown(r"**Momento:** $M(x) = M_0$")
        st.markdown(r"**Deformata:** $v(x) = \frac{M_0}{2EI}x(L-x)$")
    with col_input:
        L_m = st.number_input("Luce L (m)", 4.0)
        M0_knm = st.number_input("Momento Costante M0 (kNm)", 20.0)
        x_mm, V_n, M_nmm, theta_rad, v_mm = calc_appoggio_flessione_pura(L_m*1000, M0_knm*1000000, E, I)

# 24. APPOGGIO - TRIANGOLARE MAX IN A
elif vincolo == "Appoggio - Appoggio" and carico == "Triangolare Max Sx":
    with col_teoria:
        st.markdown(r"**Reazione A:** $R_A = \frac{qL}{3}$")
        st.markdown(r"**Reazione B:** $R_B = \frac{qL}{6}$")
    with col_input:
        L_m = st.number_input("Luce L (m)", 4.0)
        q_kn = st.number_input("Carico max in A q (kN/m)", 10.0)
        x_mm, V_n, M_nmm, theta_rad, v_mm = calc_appoggio_triangolare_sx(L_m*1000, q_kn, E, I)

# 25. MENSOLA - TRAPEZOIDALE
elif vincolo == "Mensola" and carico == "Trapezoidale":
    with col_teoria:
        st.markdown(r"**Taglio Incastro:** $V_A = \frac{(q_1 + q_2)L}{2}$")
        st.markdown(r"**Momento Incastro:** $M_A = -\frac{L^2}{6}(q_1 + 2q_2)$")
    with col_input:
        L_m = st.number_input("Luce L (m)", 3.0)
        q1_kn = st.number_input("Carico q1 incastro (kN/m)", 20.0)
        q2_kn = st.number_input("Carico q2 punta (kN/m)", 5.0)
        x_mm, V_n, M_nmm, theta_rad, v_mm = calc_mensola_trapezoidale(L_m*1000, q1_kn, q2_kn, E, I)

# 26. MENSOLA - DUE CARICHI CONCENTRATI
elif vincolo == "Mensola" and carico == "Due carichi concentrati":
    with col_teoria:
        st.markdown(r"**Taglio max:** $V_A = F_1 + F_2$")
        st.markdown(r"**Momento Incastro:** $M_A = -F_1 a - F_2 L$")
    with col_input:
        L_m = st.number_input("Luce L (m)", 3.0)
        a_m = st.number_input("Distanza F1 da incastro a (m)", 1.5)
        F1_kn = st.number_input("Carico F1 (kN)", 20.0)
        F2_kn = st.number_input("Carico in punta F2 (kN)", 15.0)
        x_mm, V_n, M_nmm, theta_rad, v_mm = calc_mensola_due_concentrati(L_m*1000, F1_kn*1000, F2_kn*1000, a_m*1000, E, I)

# 27. INCASTRO/APPOGGIO - CONCENTRATO DISTANZA A
elif vincolo == "Incastro - Appoggio" and carico == "Concentrato a distanza a":
    with col_teoria:
        st.markdown(r"**Reazione Appoggio B:** $R_B = \frac{Fa^2(3L-a)}{2L^3}$")
        st.markdown(r"**Momento Incastro:** $M_A = -\frac{F a b (L+b)}{2L^2}$")
    with col_input:
        L_m = st.number_input("Luce L (m)", 4.0)
        a_m = st.number_input("Distanza carico da incastro a (m)", 2.0)
        F_kn = st.number_input("Carico F (kN)", 50.0)
        x_mm, V_n, M_nmm, theta_rad, v_mm = calc_incastro_appoggio_concentrato_a(L_m*1000, F_kn*1000, a_m*1000, E, I)

# 28. INCASTRO/APPOGGIO - MOMENTO IN MEZZERIA
elif vincolo == "Incastro - Appoggio" and carico == "Momento in Mezzeria":
    with col_teoria:
        st.markdown(r"**Momento Incastro:** $M_A = -\frac{M_0}{8}$")
        st.markdown(r"**Taglio Costante:** $V(x) = \mp \frac{9M_0}{8L}$")
    with col_input:
        L_m = st.number_input("Luce L (m)", 4.0)
        M0_knm = st.number_input("Momento M0 in mezzeria (kNm)", 20.0)
        x_mm, V_n, M_nmm, theta_rad, v_mm = calc_incastro_appoggio_momento_mezzeria(L_m*1000, M0_knm*1000000, E, I)

# 29. INCASTRO/INCASTRO - TRIANGOLARE SX
elif vincolo == "Incastro - Incastro" and carico == "Triangolare Max Sx":
    with col_teoria:
        st.markdown(r"**Momento Incastro sx:** $M_A = -\frac{qL^2}{20}$")
        st.markdown(r"**Momento Incastro dx:** $M_B = -\frac{qL^2}{30}$")
    with col_input:
        L_m = st.number_input("Luce L (m)", 4.0)
        q_kn = st.number_input("Carico max all'incastro sx q (kN/m)", 20.0)
        x_mm, V_n, M_nmm, theta_rad, v_mm = calc_incastro_incastro_triangolare_sx(L_m*1000, q_kn, E, I)

# 30. INCASTRO/INCASTRO - MOMENTO IN MEZZERIA
elif vincolo == "Incastro - Incastro" and carico == "Momento in Mezzeria":
    with col_teoria:
        st.markdown(r"**Momenti agli Incastri:** $M_A = -\frac{M_0}{4} \quad M_B = \frac{M_0}{4}$")
        st.markdown(r"**Taglio Costante:** $V(x) = -\frac{3M_0}{2L}$")
    with col_input:
        L_m = st.number_input("Luce L (m)", 4.0)
        M0_knm = st.number_input("Momento M0 in mezzeria (kNm)", 25.0)
        x_mm, V_n, M_nmm, theta_rad, v_mm = calc_incastro_incastro_momento_mezzeria(L_m*1000, M0_knm*1000000, E, I)

# 31. ARCO A 3 CERNIERE - CARICO IN CHIAVE
elif vincolo == "Arco a 3 Cerniere" and carico == "Carico in Chiave":
    with col_teoria:
        st.markdown(r"**Spinta Orizzontale:** $H = \frac{FL}{4f}$")
        st.markdown(r"**Momento Flettente:** $M(x) = M_{trave} - H \cdot y(x)$")
        st.info("In un arco parabolico con carico concentrato, il momento flettente è massimo sotto il carico e assume andamenti invertiti rispetto a una trave rettilinea grazie all'effetto stabilizzante della spinta H.")
    with col_input:
        L_m = st.number_input("Luce orizzontale L (m)", 10.0)
        f_m = st.number_input("Freccia in chiave f (m)", 2.5)
        F_kn = st.number_input("Carico F in chiave (kN)", 100.0)
        x_mm, V_n, M_nmm, theta_rad, v_mm, H_n = calc_arco_3_cerniere_chiave(L_m*1000, f_m*1000, F_kn*1000, E, I)
        st.success(f"🔥 **Spinta Orizzontale H:** {H_n/1000:.2f} kN")

# 32. INCASTRO/INCASTRO - GRADIENTE TERMICO
elif vincolo == "Incastro - Incastro" and carico == "Gradiente Termico":
    with col_teoria:
        st.markdown(r"**Momento Indotto:** $M = \frac{EI \alpha \Delta T}{h}$")
        st.markdown(r"**Deformazione e Taglio:** $v(x) = 0 \quad V(x) = 0$")
        st.info("Essendo una struttura iperstatica, la deformazione termica è bloccata dagli incastri. Questo genera uno sforzo di flessione puramente interno (Momento costante) senza che la trave subisca abbassamenti visibili.")
    with col_input:
        L_m = st.number_input("Luce L (m)", 4.0)
        delta_T = st.number_input("Gradiente Termico ΔT tra estradosso e intradosso (°C)", 30.0)
        h_mm = st.number_input("Altezza della sezione h (mm)", 300.0)
        alpha = st.number_input("Coefficiente espansione termica α (1/°C)", value=1.2e-5, format="%.6f")
        x_mm, V_n, M_nmm, theta_rad, v_mm = calc_incastro_incastro_termico(L_m*1000, delta_T, h_mm, alpha, E, I)

# 33. INCASTRO/INCASTRO - CEDIMENTO VINCOLARE
elif vincolo == "Incastro - Incastro" and carico == "Cedimento Verticale Appoggio":
    with col_teoria:
        st.markdown(r"**Taglio Indotto:** $V = -\frac{12EI\delta}{L^3}$")
        st.markdown(r"**Momenti agli Incastri:** $M_A = M_B = \frac{6EI\delta}{L^2}$")
        st.markdown(r"**Equazione Deformata:** $v(x) = \delta [3(\frac{x}{L})^2 - 2(\frac{x}{L})^3]$")
    with col_input:
        L_m = st.number_input("Luce L (m)", 4.0)
        delta_mm = st.number_input("Cedimento verticale δ appoggio destro (mm)", 15.0)
        x_mm, V_n, M_nmm, theta_rad, v_mm = calc_incastro_incastro_cedimento(L_m*1000, delta_mm, E, I)
        
# 34. ARCO A 2 CERNIERE - CARICO IN CHIAVE
elif vincolo == "Arco a 2 Cerniere" and carico == "Carico in Chiave":
    with col_teoria:
        st.markdown(r"**Grado Iperstaticità:** 1")
        st.markdown(r"**Spinta Orizzontale:** $H = \frac{25FL}{128f}$")
        st.markdown(r"**Momento Flettente:** $M(x) = M_{iso} - H \cdot y(x)$")
    with col_input:
        L_m = st.number_input("Luce orizzontale L (m)", 10.0)
        f_m = st.number_input("Freccia in chiave f (m)", 2.5)
        F_kn = st.number_input("Carico F in chiave (kN)", 100.0)
        x_mm, V_n, M_nmm, theta_rad, v_mm, H_n = calc_arco_2_cerniere(L_m*1000, f_m*1000, F_kn*1000, E, I)
        st.success(f"🔒 **Spinta Orizzontale (Vincolo):** {H_n/1000:.2f} kN")

# 35. CAVO SOSPESO - CARICO DISTRIBUITO
elif vincolo == "Cavo Sospeso" and carico == "Carico Distribuito (Fune)":
    with col_teoria:
        st.markdown(r"**Tiro Orizzontale Costante:** $H = \frac{qL^2}{8f}$")
        st.markdown(r"**Trazione Massima negli Appoggi:** $T_{max} = \sqrt{H^2 + (\frac{qL}{2})^2}$")
        st.info("I cavi non portano flessione ($M=0$). Il grafico rosso mostrerà la componente verticale del tiro, mentre qui sotto leggerai la Trazione assiale massima a cui dimensionare la fune.")
    with col_input:
        L_m = st.number_input("Luce orizzontale L (m)", 20.0)
        f_m = st.number_input("Freccia (Sag) f (m)", 2.0)
        q_kn = st.number_input("Carico distribuito (peso + accidentali) q (kN/m)", 5.0)
        # Sfruttiamo il campo Inerzia dell'interfaccia usandolo come Area fittizia per la fune
        x_mm, V_n, M_nmm, theta_rad, v_mm, H_n, T_array = calc_cavo_parabolico(L_m*1000, f_m*1000, q_kn, E, I)
        st.success(f"⛓️ **Tiro Orizzontale H:** {H_n/1000:.2f} kN")
        st.error(f"⚠️ **Trazione Assiale Max (negli ancoraggi):** {np.max(T_array)/1000:.2f} kN")

# 36. TRAVE CONTINUA - 2 CAMPATE
elif vincolo == "Trave Continua" and carico == "2 Campate con Carico Distribuito":
    with col_teoria:
        st.markdown(r"**Reazioni (A, B, C):** $R_A = R_C = \frac{3qL}{8} \quad R_B = \frac{10qL}{8}$")
        st.markdown(r"**Momento Appoggio Centrale:** $M_B = -\frac{qL^2}{8}$")
        st.markdown(r"**Momento Max in Campata:** $M_{max}^+ = \frac{9qL^2}{128}$")
    with col_input:
        L_m = st.number_input("Luce della SINGOLA campata L (m)", 5.0)
        q_kn = st.number_input("Carico q su entrambe le campate (kN/m)", 15.0)
        # La trave sarà lunga 2L in totale
        x_mm, V_n, M_nmm, theta_rad, v_mm = calc_trave_continua_2_campate(L_m*1000, q_kn, E, I)
        st.info("Nota: L'asse X del grafico mostrerà l'estensione totale (2L). L'appoggio centrale si trova esattamente a metà.")

# --- APPOGGIO: GRADIENTE TERMICO ---
elif vincolo == "Appoggio - Appoggio" and carico == "Gradiente Termico":
    with col_teoria:
        st.markdown(r"**Taglio e Momento:** $V(x) = 0 \quad M(x) = 0$")
        st.markdown(r"**Deformata:** $v(x) = \frac{\alpha \Delta T}{2h} x(L-x)$")
        st.info("💡 **Magia Isostatica:** Le variazioni termiche incurvano la trave (creano freccia) ma NON generano alcuno sforzo interno (coazione nulla). I grafici V e M saranno piatti!")
    with col_input:
        L_m = st.number_input("Luce L (m)", 4.0)
        delta_T = st.number_input("Gradiente ΔT tra estradosso e intradosso (°C)", 30.0)
        h_mm = st.number_input("Altezza sezione h (mm)", 300.0)
        alpha = st.number_input("Coeff. termico α (1/°C)", value=1.2e-5, format="%.6f")
        x_mm, V_n, M_nmm, theta_rad, v_mm = calc_appoggio_termico(L_m*1000, delta_T, h_mm, alpha, E, I)

# --- APPOGGIO: CEDIMENTO VINCOLARE ---
elif vincolo == "Appoggio - Appoggio" and carico == "Cedimento Appoggio Destro":
    with col_teoria:
        st.markdown(r"**Taglio e Momento:** $V(x) = 0 \quad M(x) = 0$")
        st.markdown(r"**Deformata (Moto Rigido):** $v(x) = \delta \frac{x}{L}$")
        st.info("💡 Un cedimento in una struttura isostatica provoca solo un moto rigido. La trave si inclina dritta ma non si flette, quindi non nascono sforzi.")
    with col_input:
        L_m = st.number_input("Luce L (m)", 4.0)
        delta_mm = st.number_input("Cedimento verticale δ (mm)", 15.0)
        x_mm, V_n, M_nmm, theta_rad, v_mm = calc_appoggio_cedimento(L_m*1000, delta_mm, E, I)

# 37. TRAVE CONTINUA - 2 CAMPATE DIVERSE (q)
elif vincolo == "Trave Continua" and carico == "2 Campate Diverse (Uniforme totale)":
    with col_teoria:
        st.markdown(r"**Momento Appoggio B:** $M_B = -\frac{q(L_1^3 + L_2^3)}{8(L_1 + L_2)}$")
        st.markdown(r"**Reazione B:** $R_B = V_{B,sx} + V_{B,dx}$")
    with col_input:
        L1_m = st.number_input("Luce Campata 1 L1 (m)", 4.0)
        L2_m = st.number_input("Luce Campata 2 L2 (m)", 6.0)
        q_kn = st.number_input("Carico distribuito q (kN/m)", 15.0)
        x_mm, V_n, M_nmm, theta_rad, v_mm = calc_continua_2_campate_diverse_q(L1_m*1000, L2_m*1000, q_kn, E, I)

# 38. TRAVE CONTINUA - 2 CAMPATE UGUALI (q solo su campata 1)
elif vincolo == "Trave Continua" and carico == "2 Campate Uguali (Uniforme solo su campata 1)":
    with col_teoria:
        st.markdown(r"**Momento Appoggio B:** $M_B = -\frac{qL^2}{16}$")
        st.markdown(r"**Reazioni:** $R_A = \frac{7qL}{16} \quad R_B = \frac{5qL}{8} \quad R_C = -\frac{qL}{16}$")
    with col_input:
        L_m = st.number_input("Luce della singola campata L (m)", 5.0)
        q_kn = st.number_input("Carico q SOLO su Campata 1 (kN/m)", 15.0)
        x_mm, V_n, M_nmm, theta_rad, v_mm = calc_continua_2_campate_q_parziale(L_m*1000, q_kn, E, I)

# 39. TRAVE CONTINUA - 2 CAMPATE UGUALI (F in campata 1)
elif vincolo == "Trave Continua" and carico == "2 Campate Uguali (Concentrato in campata 1)":
    with col_teoria:
        st.markdown(r"**Momento Appoggio B:** $M_B = -\frac{3FL}{32}$")
        st.markdown(r"**Reazione C (Trazione):** $R_C = -\frac{3F}{32}$")
    with col_input:
        L_m = st.number_input("Luce della singola campata L (m)", 5.0)
        F_kn = st.number_input("Carico concentrato F in mezzeria Campata 1 (kN)", 50.0)
        x_mm, V_n, M_nmm, theta_rad, v_mm = calc_continua_2_campate_F_mezzeria(L_m*1000, F_kn*1000, E, I)

# 40. TRAVE CONTINUA - 3 CAMPATE UGUALI (q totale)
elif vincolo == "Trave Continua" and carico == "3 Campate Uguali (Uniforme totale)":
    with col_teoria:
        st.markdown(r"**Momenti Interni:** $M_B = M_C = -\frac{qL^2}{10}$")
        st.markdown(r"**Reazioni Esterne:** $R_A = R_D = 0.4qL$")
    with col_input:
        L_m = st.number_input("Luce della singola campata L (m)", 4.0)
        q_kn = st.number_input("Carico distribuito totale q (kN/m)", 20.0)
        x_mm, V_n, M_nmm, theta_rad, v_mm = calc_continua_3_campate_q(L_m*1000, q_kn, E, I)
        
# 41. PONTE SOSPESO
elif vincolo == "Ponte Sospeso" and carico == "Impalcato con Carico Uniforme":
    with col_teoria:
        st.markdown(r"**Spinta Orizzontale Fune:** $H = \frac{qL^2}{8f}$")
        st.markdown(r"**Trazione Max Fune (ai piloni):** $T_{max} = \sqrt{H^2 + V^2}$")
        st.markdown(r"**Sforzo singola Sospensione:** $S = q \cdot L_1$")
        st.markdown(r"**Momento Impalcato (Appoggio):** $M_a \approx -\frac{qL_1^2}{12}$")
    with col_input:
        L_m = st.number_input("Luce totale del ponte L (m)", 100.0)
        f_m = st.number_input("Freccia parabolica fune f (m)", 10.0)
        n_campate = st.number_input("Numero di campate L1 tra sospensioni", value=10, min_value=2, step=1)
        q_kn = st.number_input("Carico distribuito sull'impalcato q (kN/m)", 50.0)

        x_mm, V_n, M_nmm, theta_rad, v_mm, H_n, Tmax_n, S_n = calc_ponte_sospeso(L_m*1000, f_m*1000, q_kn, n_campate, E, I)
        
        st.success(f"⛓️ **Tiro Orizzontale Fune H:** {H_n/1000:.2f} kN")
        st.error(f"⚠️ **Trazione Max Fune $T_{{max}}$:** {Tmax_n/1000:.2f} kN")
        st.info(f"📍 **Trazione singola Sospensione S:** {S_n/1000:.2f} kN")

        # Inietto n_campate in L1_m per far disegnare al plotter il numero esatto di pendini
        L1_m = float(n_campate)

# 42. PONTE AD ARCO A SPINTA ELIMINATA
elif vincolo == "Ponte ad Arco a Spinta Eliminata" and carico == "Impalcato con Carico Uniforme":
    with col_teoria:
        st.markdown(r"**Spinta Assorbita dall'Impalcato:** $H = \frac{qL^2}{8f}$")
        st.markdown(r"**Sforzo singolo Pendino:** $S = q \cdot L_1$")
        st.markdown(r"**Momento Impalcato (Appoggio):** $M_a \approx -\frac{qL_1^2}{12}$")
        st.info("Essendo a 'spinta eliminata' (Bowstring), l'impalcato funge da tirante elastico (catena) e assorbe l'intera spinta orizzontale dell'arco. Gli appoggi a terra ricevono solo sforzi verticali.")
    with col_input:
        L_m = st.number_input("Luce totale dell'arco L (m)", 50.0)
        f_m = st.number_input("Altezza in chiave dell'arco f (m)", 8.0)
        n_campate = st.number_input("Numero di intervalli tra i pendini", value=8, min_value=2, step=1)
        q_kn = st.number_input("Carico distribuito impalcato q (kN/m)", 30.0)

        x_mm, V_n, M_nmm, theta_rad, v_mm, H_n, S_n = calc_arco_spinta_eliminata(L_m*1000, f_m*1000, q_kn, n_campate, E, I)
        
        st.success(f"🔒 **Trazione nell'Impalcato (Catena) H:** {H_n/1000:.2f} kN")
        st.info(f"📍 **Trazione singolo Pendino S:** {S_n/1000:.2f} kN")

        L1_m = float(n_campate)
        
# 43. PONTE LANGER (Catena Rigida / Arco Rigido)
elif vincolo == "Ponte Langer":
    with col_teoria:
        if "Catena Rigida" in carico:
            st.markdown(r"**Tipologia:** Catena Rigida e Arco Flessibile")
            st.info("L'impalcato (catena) ha una rigidezza flessionale molto maggiore dell'arco. L'arco assorbe solo compressione pura, mentre tutto il momento flettente indotto dai carichi asimmetrici viene assorbito dall'impalcato.")
        else:
            st.markdown(r"**Tipologia:** Arco Rigido e Catena Flessibile")
            st.info("L'arco ha un'elevata rigidezza flessionale, mentre l'impalcato è un semplice tirante flessibile. È l'arco superiore ad assorbire il momento flettente e il taglio derivanti dai carichi.")
        
        if "Totale" in carico:
            st.markdown(r"**Spinta (Carico Totale):** $H = \frac{qL^2}{8f}$")
            st.markdown(r"**Momento Flettente Globale:** $M(x) \approx 0$")
        else:
            st.markdown(r"**Spinta (Carico a Metà):** $H = \frac{qL^2}{16f}$")
            st.markdown(r"**Momento Flettente:** $M(x) = M_{iso} - H \cdot y(x)$")

    with col_input:
        L_m = st.number_input("Luce totale del ponte L (m)", 40.0)
        f_m = st.number_input("Freccia dell'arco f (m)", 8.0)
        q_kn = st.number_input("Carico distribuito q (kN/m)", 20.0)

        # Il calcolo matematico di M e V è identico per catena o arco rigido. 
        # Quello che cambia è QUALE elemento lo assorbe fisicamente (spiegato in teoria).
        if "Totale" in carico:
            x_mm, V_n, M_nmm, theta_rad, v_mm, H_n = calc_ponte_langer_totale(L_m*1000, f_m*1000, q_kn, E, I)
        else:
            x_mm, V_n, M_nmm, theta_rad, v_mm, H_n = calc_ponte_langer_meta(L_m*1000, f_m*1000, q_kn, E, I)

        st.success(f"🔒 **Spinta Orizzontale (H):** {H_n/1000:.2f} kN")
        
        if "Metà" in carico:
            elemento = "dall'impalcato (catena)" if "Catena" in carico else "dall'arco"
            st.warning(f"📊 Il grafico M(x) mostra l'andamento del momento flettente assorbito {elemento}.")

# 45. TRAVE GERBER
elif vincolo == "Trave Gerber" and carico == "Uniforme totale con Cerniera":
    with col_teoria:
        st.markdown(r"**Taglio nella cerniera:** $V_c = \frac{qL_3}{2}$")
        st.markdown(r"**Momento nella cerniera:** $M_c = 0$")
        st.info("La cerniera annulla il momento flettente ma trasmette il taglio alla mensola sottostante. È uno schema isostatico geniale inventato da Heinrich Gerber.")
    with col_input:
        L1_m = st.number_input("Luce Campata A-B (m)", value=4.0)
        L2_m = st.number_input("Sbalzo B-C (fino a cerniera) (m)", value=1.5)
        L3_m = st.number_input("Luce Trave Sospesa C-D (m)", value=3.0)
        q_kn = st.number_input("Carico distribuito q (kN/m)", value=15.0)

        x_mm, V_n, M_nmm, theta_rad, v_mm = calc_gerber_standard(L1_m*1000, L2_m*1000, L3_m*1000, q_kn, E, I)

# 46. URTO SU MENSOLA
elif vincolo == "Mensola (Urto Dinamico)" and carico == "Caduta Massa in Punta":
    with col_teoria:
        st.markdown(r"**Spostamento Statico:** $v_{st} = \frac{Mg L^3}{3EI}$")
        st.markdown(r"**Fattore Dinamico:** $K_d = 1 + \sqrt{1 + \frac{2h}{v_{st}}}$")
        st.markdown(r"**Forza Equivalente:** $F_{eq} = Mg \cdot K_d$")
    with col_input:
        L_m = st.number_input("Luce Mensola L (m)", value=2.0)
        Massa_kg = st.number_input("Massa in caduta libera M (kg)", value=100.0)
        h_m = st.number_input("Altezza di caduta h (metri)", value=0.5)

        x_mm, V_n, M_nmm, theta_rad, v_mm, Kd, Feq = calc_urto_mensola(L_m*1000, Massa_kg, h_m*1000, E, I)
        
        st.error(f"💥 **Fattore di Amplificazione (Kd):** {Kd:.2f}x")
        st.warning(f"⚠️ **Forza Dinamica Impattante:** {Feq/1000:.2f} kN")
        st.info("A causa della velocità d'impatto, la struttura 'sente' una forza decine di volte superiore al semplice peso della massa!")

# 47. ROTAZIONE INCASTRO
elif vincolo == "Incastro - Appoggio" and carico == "Rotazione Incastro":
    with col_teoria:
        st.markdown(r"**Momento Incastro:** $M_A = \frac{3EI\varphi}{L}$")
        st.markdown(r"**Reazioni Verticali:** $R_A = -R_B = -\frac{3EI\varphi}{L^2}$")
    with col_input:
        L_m = st.number_input("Luce L (m)", value=4.0)
        phi_deg = st.number_input("Rotazione imposta (Gradi)", value=1.0)
        phi_rad = np.radians(phi_deg) # Converti in radianti

        x_mm, V_n, M_nmm, theta_rad, v_mm = calc_incastro_appoggio_rotazione(L_m*1000, phi_rad, E, I)

# 48. FUNE SFALSATA
elif vincolo == "Cavo Sospeso" and carico == "Fune con Appoggi Sfalsati":
    with col_teoria:
        st.markdown(r"**Tiro Orizzontale:** $H = \frac{qL^2}{8f}$")
        st.info("Il dislivello tra gli appoggi non altera la Spinta orizzontale, ma sbilancia le reazioni verticali, rendendo la fune asimmetrica.")
    with col_input:
        L_m = st.number_input("Luce orizzontale L (m)", value=20.0)
        f_m = st.number_input("Freccia f (rispetto alla corda) (m)", value=2.0)
        h_m = st.number_input("Dislivello appoggio dx (m)", value=3.0)
        q_kn = st.number_input("Carico distribuito q (kN/m)", value=5.0)

        x_mm, V_n, M_nmm, theta_rad, v_mm, H_n, T_array = calc_fune_sfalsata(L_m*1000, f_m*1000, h_m*1000, q_kn, E, I)
        st.error(f"⚠️ **Trazione Assiale Max (Ancoraggio Alto):** {np.max(T_array)/1000:.2f} kN")
        
# Caso non trovato
else:
    st.warning("⚠️ Questa combinazione non è ancora stata compilata nel codice sorgente. Aggiungi il blocco `elif` in app.py!")


# --- RENDERING GRAFICI ---
if x_mm is not None:
    # 1. Ora che ho tutti i veri input (L, a, f), inietto lo schema corretto nel segnaposto in alto!
    schema_placeholder.plotly_chart(disegna_schema_statico(vincolo, carico, L_m, L1_m, L2_m, a_m, f_m), use_container_width=True)

    st.markdown("---")
    figura = crea_4_grafici_plotly(x_mm/1000, V_n/1000, M_nmm/1000000, theta_rad*1000, v_mm)
    st.plotly_chart(figura, use_container_width=True)

    # --- DOWNLOAD PDF ---
    try:
        parametri_input_pdf = {}
        risultati_extra_pdf = {}

        parametri_input_pdf["Luce L"] = f"{L_m:.2f} m"
        parametri_input_pdf["Modulo E"] = f"{E_mpa:.0f} MPa"
        parametri_input_pdf["Inerzia I"] = f"{I_cm4:.1f} cm4"

        if 'q_kn' in dir():
            parametri_input_pdf["Carico q"] = f"{q_kn:.2f} kN/m"
        if 'F_kn' in dir():
            parametri_input_pdf["Forza F"] = f"{F_kn:.2f} kN"
        if 'M0_knm' in dir():
            parametri_input_pdf["Momento M0"] = f"{M0_knm:.2f} kNm"
        if 'a_m' in dir() and a_m > 0:
            parametri_input_pdf["Distanza a"] = f"{a_m:.2f} m"
        if 'f_m' in dir() and f_m > 0:
            parametri_input_pdf["Freccia f"] = f"{f_m:.2f} m"

        if 'H_n' in dir():
            risultati_extra_pdf["Spinta Orizzontale H"] = f"{H_n/1000:.2f} kN"
        if 'Kd' in dir():
            risultati_extra_pdf["Fattore Amplificazione Kd"] = f"{Kd:.2f}"
            risultati_extra_pdf["Forza Dinamica Feq"] = f"{Feq/1000:.2f} kN"

        pdf_bytes = genera_pdf_prontuario(vincolo, carico, parametri_input_pdf, risultati_extra_pdf, x_mm/1000, V_n, M_nmm, theta_rad, v_mm, L_m)
        st.download_button(
            label="📄 Scarica Relazione PDF",
            data=pdf_bytes,
            file_name="relazione_prontuario.pdf",
            mime="application/pdf"
        )
    except Exception as e:
        st.warning(f"Generazione PDF non disponibile: {e}")