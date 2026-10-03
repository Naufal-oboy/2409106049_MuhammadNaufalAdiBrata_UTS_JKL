#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nama File : netconf_modul.py
Tujuan    : Membangun pesan NETCONF <rpc><edit-config> untuk membuat VLAN
Pembuat   : Muhammad Naufal Adi Brata Putra Suharizman Poerwo - 2409106049
"""
import xml.etree.ElementTree as ET

from identitas import kode_cabang

NS_NETCONF = "urn:ietf:params:xml:ns:netconf:base:1.0"
NS_VLAN = "urn:huawei:yang:huawei-vlan"


def buat_pesan_netconf():
    """Membangun dan mengembalikan string XML <rpc><edit-config>."""
    # === MESSAGES LAYER: pembungkus <rpc> + message-id ===
    rpc = ET.Element("rpc", {"xmlns": NS_NETCONF, "message-id": "101"})

    # === OPERATIONS LAYER: operasi <edit-config> pada datastore running ===
    edit = ET.SubElement(rpc, "edit-config")
    target = ET.SubElement(edit, "target")
    ET.SubElement(target, "running")
    ET.SubElement(edit, "default-operation").text = "merge"

    # === CONTENT LAYER: data konfigurasi VLAN (ID = kode_cabang) ===
    config = ET.SubElement(edit, "config")
    vlans = ET.SubElement(config, "vlan", {"xmlns": NS_VLAN})
    vlan = ET.SubElement(ET.SubElement(vlans, "vlans"), "vlan")
    ET.SubElement(vlan, "id").text = str(int(kode_cabang))
    ET.SubElement(vlan, "name").text = f"VLAN_CABANG_{kode_cabang}"

    ET.indent(rpc)  # butuh Python 3.9+
    return ET.tostring(rpc, encoding="unicode")


if __name__ == "__main__":
    print(buat_pesan_netconf())