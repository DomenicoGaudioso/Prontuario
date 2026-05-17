from __future__ import annotations


MAPPA_SCHEMI: dict[str, list[str]] = {
    "Appoggio - Appoggio": [
        "Uniformemente Distribuito",
        "Concentrato in Mezzeria",
        "Triangolare",
        "Concentrato a distanza a",
        "Momento in Appoggio",
        "Due carichi simmetrici",
        "Triangolare Simmetrico",
        "Distribuito parziale sx",
        "Momento in Mezzeria",
        "Flessione Pura",
        "Triangolare Max Sx",
        "Gradiente Termico",
        "Cedimento Appoggio Destro",
    ],
    "Mensola": [
        "Concentrato in Punta",
        "Uniformemente Distribuito",
        "Triangolare",
        "Concentrato a distanza a",
        "Momento in Punta",
        "Distribuito parziale",
        "Triangolare Max Punta",
        "Trapezoidale",
        "Due carichi concentrati",
    ],
    "Incastro - Appoggio": [
        "Uniformemente Distribuito",
        "Concentrato in Mezzeria",
        "Momento in Appoggio",
        "Concentrato a distanza a",
        "Momento in Mezzeria",
        "Rotazione Incastro",
    ],
    "Incastro - Incastro": [
        "Uniformemente Distribuito",
        "Concentrato in Mezzeria",
        "Concentrato a distanza a",
        "Triangolare Max Sx",
        "Momento in Mezzeria",
        "Gradiente Termico",
        "Cedimento Verticale Appoggio",
    ],
    "Arco a 3 Cerniere": ["Carico in Chiave"],
    "Arco a 2 Cerniere": ["Carico in Chiave"],
    "Cavo Sospeso": ["Carico Distribuito (Fune)", "Fune con Appoggi Sfalsati"],
    "Trave Continua": [
        "2 Campate con Carico Distribuito",
        "2 Campate Diverse (Uniforme totale)",
        "2 Campate Uguali (Uniforme solo su campata 1)",
        "2 Campate Uguali (Concentrato in campata 1)",
        "3 Campate Uguali (Uniforme totale)",
    ],
    "Ponte Sospeso": ["Impalcato con Carico Uniforme"],
    "Ponte ad Arco a Spinta Eliminata": ["Impalcato con Carico Uniforme"],
    "Ponte Langer": [
        "Catena Rigida - Carico Totale",
        "Catena Rigida - Carico a Metà",
        "Arco Rigido - Carico Totale",
        "Arco Rigido - Carico a Metà",
    ],
    "Trave Gerber": ["Uniforme totale con Cerniera"],
    "Mensola (Urto Dinamico)": ["Caduta Massa in Punta"],
}


def iter_menu_combinations() -> set[tuple[str, str]]:
    return {
        (vincolo, carico)
        for vincolo, carichi in MAPPA_SCHEMI.items()
        for carico in carichi
    }
