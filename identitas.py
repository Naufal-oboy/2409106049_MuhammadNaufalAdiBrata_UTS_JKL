#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nama File : identitas.py
Tujuan    : Menyimpan identitas cabang dan membuat ID perangkat
Pembuat   : Muhammad Naufal Adi Brata Putra Suharizman Poerwo - 24009106049
"""

nim = "24009106049"          
nama = "Muhammad Naufal Adi Brata Putra Suharizman Poerwo"       
kode_cabang = nim[-3:]      #


def buat_id_perangkat(jenis, nomor):
    """Membuat ID perangkat, contoh: ROUTER-123-01"""
    return f"{jenis.upper()}-{kode_cabang}-{int(nomor):02d}"


if __name__ == "__main__":
    print(nim, nama, kode_cabang, buat_id_perangkat("router", 1))