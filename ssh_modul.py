#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nama File : ssh_modul.py
Tujuan    : Login SSH dengan Paramiko dan menjalankan perintah diagnostik
Pembuat   : Muhammad Naufal Adi Brata Putra Suharizman Poerwo - 24009106049
"""
import os

import paramiko

from identitas import kode_cabang

HOST = os.environ.get("SSH_HOST", "127.0.0.1")   # IP VM/laptop
PORT = int(os.environ.get("SSH_PORT", "2222"))
USERNAME = f"admin_{kode_cabang}"
PASSWORD = os.environ.get("SSH_PASSWORD", "")          
PERINTAH = ["hostname", "uptime", "uname -a"]


def cek_ssh():
    """Login SSH, jalankan perintah diagnostik, kembalikan dict hasil."""
    hasil = {"status": "GAGAL", "output": {}, "error": None}
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(HOST, port=PORT, username=USERNAME,
                        password=PASSWORD, timeout=5)
        for cmd in PERINTAH:
            _, stdout, _ = client.exec_command(cmd)
            hasil["output"][cmd] = stdout.read().decode().strip()
        hasil["status"] = "BERHASIL"
    except Exception as e:
        hasil["error"] = str(e)
    finally:
        client.close()

    print(f"[SSH] {USERNAME}@{HOST} -> {hasil['status']}")
    for cmd, out in hasil["output"].items():
        print(f"  $ {cmd}\n    {out}")
    if hasil["error"]:
        print(f"  Error: {hasil['error']}")
    return hasil


if __name__ == "__main__":
    cek_ssh()