from __future__ import annotations

from typing import Any

import numpy as np


def _sign(value: float) -> str:
    if not np.isfinite(value) or abs(value) < 1e-12:
        return "0"
    return "+" if value > 0 else "-"


def _row(label: str, values, x_m, scale: float, unit: str) -> dict[str, Any]:
    values = np.asarray(values, dtype=float)
    x_m = np.asarray(x_m, dtype=float)
    index = int(np.nanargmax(np.abs(values)))
    value = float(values[index] / scale)
    return {
        "Grandezza": label,
        "Valore": round(value, 3),
        "Unita": unit,
        "Ascissa x [m]": round(float(x_m[index]), 3),
        "Segno": _sign(value),
    }


def build_result_summary(x_m, V, M, theta, v) -> list[dict[str, Any]]:
    return [
        _row("Vmax", V, x_m, 1000.0, "kN"),
        _row("Mmax", M, x_m, 1_000_000.0, "kNm"),
        _row("theta max", theta, x_m, 0.001, "mrad"),
        _row("vmax", v, x_m, 1.0, "mm"),
    ]
