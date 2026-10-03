#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nama File : main.py
Tujuan    : Integrasi seluruh modul dan mencetak laporan akhir cabang
Pembuat   : Muhammad Naufal Adi Brata Putra Suharizman Poerwo - 2409106049
"""
import identitas
import ssh_modul
import snmp_modul
import netconf_modul
import telemetry_modul


class LaporanCabang:
    def __init__(self, hasil_ssh, hasil_snmp, pesan_netconf, hasil_telemetry):
        self.hasil_ssh = hasil_ssh
        self.hasil_snmp = hasil_snmp
        self.pesan_netconf = pesan_netconf
        self.hasil_telemetry = hasil_telemetry

    def tampilkan_laporan(self):
        print("=" * 60)
        print("LAPORAN AKHIR CABANG")
        print(f"{identitas.nama} - {identitas.nim}")
        print(f"ID Perangkat : {identitas.buat_id_perangkat('router', 1)}")
        print("=" * 60)
        print(f"1. SSH     : {self.hasil_ssh['status']}")
        for cmd, out in self.hasil_ssh["output"].items():
            print(f"     {cmd}: {out}")
        print(f"2. SNMP    : {self.hasil_snmp['status']} "
            f"(sysName={self.hasil_snmp['sysName']})")
        print("3. NETCONF : pesan edit-config dibuat:")
        print(self.pesan_netconf)
        print("4. Telemetry:")
        for nama, nilai, status in self.hasil_telemetry:
            print(f"     {nama}: {nilai}% -> {status}")
        print("=" * 60)


def main():
    hasil_ssh = ssh_modul.cek_ssh()
    hasil_snmp = snmp_modul.cek_snmp()
    pesan = netconf_modul.buat_pesan_netconf()
    print(pesan)
    hasil_tel = telemetry_modul.klasifikasi_telemetry()
    print()
    LaporanCabang(hasil_ssh, hasil_snmp, pesan, hasil_tel).tampilkan_laporan()


if __name__ == "__main__":
    main()