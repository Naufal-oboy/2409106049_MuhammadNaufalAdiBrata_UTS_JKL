#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nama File : telemetry_modul.py
Tujuan    : Klasifikasi sampel data telemetry cpuUsage (hasil decode GPB)
Pembuat   : Muhammad Naufal Adi Brata Putra Suharizman Poerwo - 2409106049
"""
from identitas import nim

# Aturan turunan: 6 digit terakhir NIM dipecah jadi 3 pasang (p1, p2, p3).
# Nilai = pasangan + offset agar bervariasi (maks 99):
_pasang = [int(nim[-6:][i:i + 2]) for i in (0, 2, 4)]
_offset = [0, 0, 35]

data_telemetry = {
    f"sampel_{i + 1}": {
        "node": f"router-{i + 1}",
        "cpuUsage": min(99, p + o),   # in-uti (%)
    }
    for i, (p, o) in enumerate(zip(_pasang, _offset))
}


def klasifikasi_telemetry():
    """Klasifikasi tiap sampel; kembalikan list hasil."""
    hasil = []
    print("[TELEMETRY] Klasifikasi cpuUsage")
    for nama, sampel in data_telemetry.items():
        nilai = sampel["cpuUsage"]
        if nilai > 80:
            status = "KRITIS"
        elif nilai >= 50:
            status = "WASPADA"
        else:
            status = "NORMAL"
        hasil.append((nama, nilai, status))
        print(f"  {nama}: cpuUsage={nilai}% -> {status}")
    return hasil


if __name__ == "__main__":
    klasifikasi_telemetry()