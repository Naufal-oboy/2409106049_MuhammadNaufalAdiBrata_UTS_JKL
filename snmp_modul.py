#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nama File : snmp_modul.py
Tujuan    : Mengambil sysName (OID 1.3.6.1.2.1.1.5.0) via SNMPv2c
Pembuat   : Muhammad Naufal Adi Brata Putra Suharizman Poerwo - 2409106049
"""
import os

from identitas import kode_cabang

HOST = os.environ.get("SNMP_HOST", "127.0.0.1")
PORT = int(os.environ.get("SNMP_PORT", "1161"))
COMMUNITY = f"comm_{kode_cabang}"
OID_SYSNAME = "1.3.6.1.2.1.1.5.0"


def _get_sysname():
    """Mendukung pysnmp versi baru (asyncio) dan versi lama (sync)."""
    try:
        import asyncio
        from pysnmp.hlapi.v3arch.asyncio import (
            SnmpEngine, CommunityData, UdpTransportTarget, ContextData,
            ObjectType, ObjectIdentity, get_cmd)

        async def ambil():
            target = await UdpTransportTarget.create((HOST, PORT), timeout=3, retries=1)
            return await get_cmd(SnmpEngine(), CommunityData(COMMUNITY, mpModel=1),
                                target, ContextData(),
                                ObjectType(ObjectIdentity(OID_SYSNAME)))
        err_ind, err_stat, _, var_binds = asyncio.run(ambil())
    except ImportError:
        from pysnmp.hlapi import (
            getCmd, SnmpEngine, CommunityData, UdpTransportTarget,
            ContextData, ObjectType, ObjectIdentity)
        err_ind, err_stat, _, var_binds = next(getCmd(
            SnmpEngine(), CommunityData(COMMUNITY, mpModel=1),
            UdpTransportTarget((HOST, PORT), timeout=3, retries=1),
            ContextData(), ObjectType(ObjectIdentity(OID_SYSNAME))))
    if err_ind:
        raise RuntimeError(str(err_ind))
    if err_stat:
        raise RuntimeError(err_stat.prettyPrint())
    return var_binds[0][1].prettyPrint()


def cek_snmp():
    """Ambil sysName; kembalikan dict hasil."""
    hasil = {"status": "GAGAL", "sysName": None, "error": None}
    try:
        hasil["sysName"] = _get_sysname()
        hasil["status"] = "BERHASIL"
    except Exception as e:
        hasil["error"] = str(e)

    print(f"[SNMP] {HOST}:{PORT} (SNMPv2c) -> {hasil['status']}")
    if hasil["sysName"]:
        print(f"  sysName = {hasil['sysName']}")
    if hasil["error"]:
        print(f"  Error: {hasil['error']}")
    return hasil


if __name__ == "__main__":
    cek_snmp()