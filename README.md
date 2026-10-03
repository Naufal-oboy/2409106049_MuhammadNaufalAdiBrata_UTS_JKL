Nama: Muhammad Naufal Adi Brata | NIM: 2409106049

# UTS Jaringan Komputer Lanjut - Integration Network with Python

Project Python terpadu untuk otomatisasi jaringan cabang virtual: identitas
perangkat, akses jarak jauh (SSH), pemantauan (SNMP), pembuatan pesan
konfigurasi terstruktur (NETCONF), dan analisis data telemetry. Semua modul
digabung oleh `main.py` menjadi satu laporan akhir cabang.

- **Mata kuliah**: Jaringan Komputer Lanjut
- **Kelas / Prodi**: B 2024 / Informatika
- **Dosen pengampu**: Reza Wardhana, M.Eng.

---

## Daftar Isi

1. [Struktur Project](#struktur-project)
2. [Prasyarat](#prasyarat)
3. [Instalasi](#instalasi)
4. [Persiapan Target (VM)](#persiapan-target-vm)
5. [Cara Menjalankan main.py](#cara-menjalankan-mainpy)
6. [Penjelasan Modul](#penjelasan-modul)
7. [Ringkasan Personalisasi](#ringkasan-personalisasi)
8. [Contoh Output](#contoh-output)
9. [Riwayat Commit](#riwayat-commit)
10. [Keamanan](#keamanan)
11. [Troubleshooting](#troubleshooting)

---

## Struktur Project

```
2409106049_MuhammadNaufalAdiBrata_UTS_JKL/
├── identitas.py        # Bagian A - identitas cabang & buat_id_perangkat()
├── ssh_modul.py        # Bagian B - akses SSH dengan Paramiko
├── snmp_modul.py       # Bagian C - monitoring SNMPv2c dengan PySNMP
├── netconf_modul.py    # Bagian D - pembuat pesan NETCONF <edit-config>
├── telemetry_modul.py  # Bagian E - klasifikasi data telemetry sampel
├── main.py             # Bagian F - integrasi + class LaporanCabang
├── .gitignore          # mengecualikan venv/, __pycache__/, log & backup
└── README.md           # dokumentasi ini
```

## Prasyarat

| Kebutuhan | Keterangan |
|-----------|------------|
| Python | 3.9 atau lebih baru (`ET.indent` butuh 3.9+) |
| Git | untuk riwayat commit bertahap |
| Pustaka | `paramiko`, `pysnmp` |
| Target SSH/SNMP | VM atau laptop yang menjalankan `openssh-server` dan `snmpd` |

Bagian NETCONF dan telemetry **tidak membutuhkan perangkat atau server
sungguhan**: NETCONF hanya membangun pesan XML, dan telemetry memakai data
sampel yang menyerupai hasil decode GPB.

## Instalasi

```bash
# 1. Clone repository
git clone https://github.com/<username>/2409106049_MuhammadNaufalAdiBrata_UTS_JKL.git
cd 2409106049_MuhammadNaufalAdiBrata_UTS_JKL

# 2. Buat dan aktifkan virtual environment
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

# 3. Pasang dependensi
pip install paramiko pysnmp
```

## Persiapan Target (VM)

Modul SSH dan SNMP membutuhkan target yang bisa dijangkau. Contoh untuk
Ubuntu/Debian (jalankan di VM):

**SSH**
```bash
sudo apt install openssh-server -y
sudo systemctl enable --now ssh
sudo adduser <username_ssh>
```

**SNMP**
```bash
sudo apt install snmpd snmp -y
sudo nano /etc/snmp/snmpd.conf
#   agentaddress udp:161
#   rocommunity <community_string> default
sudo systemctl restart snmpd
```

Jika VM memakai VirtualBox mode **NAT**, buat Port Forwarding
(Settings > Network > Adapter 1 > Advanced > Port Forwarding):

| Layanan | Protokol | Host IP | Host Port | Guest Port |
|---------|----------|---------|-----------|------------|
| SSH     | TCP      | 127.0.0.1 | 2222    | 22         |
| SNMP    | UDP      | 127.0.0.1 | 1161    | 161        |

Nama pengguna SSH dan community string mengikuti aturan personalisasi
(lihat bagian [Ringkasan Personalisasi](#ringkasan-personalisasi)).

## Cara Menjalankan main.py

Host dan port target sudah diatur langsung di dalam kode (`HOST` dan `PORT`
di `ssh_modul.py` dan `snmp_modul.py`). Sesuaikan nilainya dengan alamat
target Anda sebelum menjalankan.

Satu-satunya konfigurasi yang diisi manual adalah **password SSH**, lewat
environment variable agar tidak masuk repository.

| Variabel | Fungsi |
|----------|--------|
| `SSH_PASSWORD` | password akun SSH |

**Linux / macOS**
```bash
export SSH_PASSWORD='<password>'
python main.py
```

**Windows PowerShell**
```powershell
$env:SSH_PASSWORD="<password>"
python main.py
```

Variabel hanya berlaku di jendela terminal yang sama, jadi isi ulang jika
terminal ditutup.

Setiap modul juga bisa dijalankan sendiri untuk pengujian, misalnya
`python netconf_modul.py` atau `python telemetry_modul.py`.

Kegagalan koneksi SSH atau SNMP ditangani dengan `try/except`, sehingga
program tetap berjalan dan laporan akhir tetap dicetak dengan status `GAGAL`.

## Penjelasan Modul

### `identitas.py` (Bagian A)
Menyimpan variabel `nim`, `nama`, dan `kode_cabang` (3 digit terakhir NIM),
serta fungsi `buat_id_perangkat(jenis, nomor)` yang menghasilkan ID perangkat
berformat `JENIS-<kode_cabang>-<nomor>`.

### `ssh_modul.py` (Bagian B)
Fungsi `cek_ssh()` login ke target memakai Paramiko, menjalankan tiga perintah
diagnostik (`hostname`, `uptime`, `uname -a`), mencetak hasilnya, dan
mengembalikan dictionary status. Host dan port ditulis di kode, sedangkan
password dibaca dari environment variable `SSH_PASSWORD`.

### `snmp_modul.py` (Bagian C)
Fungsi `cek_snmp()` mengambil `sysName` (OID `1.3.6.1.2.1.1.5.0`) memakai
SNMPv2c. Kode kompatibel dengan PySNMP versi asyncio (baru) maupun sync
(lama).

### `netconf_modul.py` (Bagian D)
Fungsi `buat_pesan_netconf()` **membangun** XML `<rpc><edit-config>` dengan
`xml.etree.ElementTree` untuk membuat VLAN. Struktur pesan ditandai lewat
komentar di kode:

| Lapisan | Bagian XML |
|---------|-----------|
| Messages | elemen `<rpc>` dan atribut `message-id` |
| Operations | `<edit-config>`, `<target><running/>`, `<default-operation>` |
| Content | `<config>` berisi data VLAN (id dan name) |

Transport (SSH) tidak dibuat karena perangkat NETCONF sungguhan tidak
diwajibkan pada UTS ini.

### `telemetry_modul.py` (Bagian E)
Berisi dictionary `data_telemetry` (3 sampel `cpuUsage`) dan fungsi
`klasifikasi_telemetry()` dengan aturan:

| Nilai cpuUsage | Klasifikasi |
|----------------|-------------|
| di atas 80 | KRITIS |
| 50 sampai 80 | WASPADA |
| di bawah 50 | NORMAL |

### `main.py` (Bagian F)
Mengimpor semua modul, menjalankan fungsi-fungsinya berurutan, lalu
menampilkan laporan gabungan lewat class `LaporanCabang` dengan method
`tampilkan_laporan()`.

## Ringkasan Personalisasi

Data sensitif (kode cabang, kredensial) sengaja tidak dicantumkan di sini.

- **Repository**: dinamai `2409106049_MuhammadNaufalAdiBrata_UTS_JKL`.
- **Username SSH**: pola `admin_<kode_cabang>`.
- **Community SNMP**: pola `comm_<kode_cabang>`.
- **VLAN ID NETCONF**: diambil langsung dari `kode_cabang`.
- **Sampel telemetry**: diturunkan dari 6 digit terakhir NIM yang dipecah
  menjadi 3 pasangan digit. Pasangan pertama dan kedua dipakai apa adanya,
  pasangan ketiga ditambah offset 35 agar ketiga kelas klasifikasi
  (NORMAL, WASPADA, KRITIS) muncul.
- **Kredensial**: hanya password SSH, dibaca dari environment variable
  `SSH_PASSWORD` dan tidak disimpan di repo.

## Contoh Output

Ringkasan bagian telemetry dan NETCONF (SSH dan SNMP bergantung pada target):

```
[TELEMETRY] Klasifikasi cpuUsage
  sampel_1: cpuUsage=10% -> NORMAL
  sampel_2: cpuUsage=60% -> WASPADA
  sampel_3: cpuUsage=84% -> KRITIS
```

```xml
<rpc xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="101">
  <edit-config>
    <target>
      <running />
    </target>
    <default-operation>merge</default-operation>
    <config>
      <vlan xmlns="urn:huawei:yang:huawei-vlan">
        <vlans>
          <vlan>
            <id>[VLAN ID dari kode_cabang]</id>
            <name>VLAN_CABANG_[kode_cabang]</name>
          </vlan>
        </vlans>
      </vlan>
    </config>
  </edit-config>
</rpc>
```

Laporan akhir dari `main.py` merangkum empat bagian: status SSH, status SNMP
beserta `sysName`, pesan NETCONF yang dibuat, dan hasil klasifikasi telemetry.

## Riwayat Commit

Riwayat dibuat bertahap sesuai struktur commit pada soal:

| No | Pesan commit |
|----|--------------|
| 1 | Inisialisasi struktur project dan .gitignore |
| 2 | Tambah modul identitas cabang (identitas.py) |
| 3 | Tambah modul akses SSH (ssh_modul.py) |
| 4 | Tambah modul monitoring SNMP (snmp_modul.py) |
| 5 | Tambah modul pembuatan pesan NETCONF (netconf_modul.py) |
| 6 | Tambah modul analisis data telemetry (telemetry_modul.py) |
| 7 | Integrasi akhir: main.py dan README.md |
| 8 | UTS-final |

Periksa dengan `git log --oneline`.

## Keamanan

- Password **tidak** ditulis di kode maupun README; gunakan environment
  variable.
- `.gitignore` mengecualikan `venv/`, `__pycache__/`, serta file log dan
  backup hasil eksekusi.
- Repository ini publik, jadi pastikan tidak ada kredensial di riwayat commit.

## Troubleshooting

| Gejala | Kemungkinan penyebab dan solusi |
|--------|---------------------------------|
| SSH `timed out` | `HOST`/`PORT` di kode salah, port forwarding belum dibuat, atau service `ssh` belum aktif |
| SSH `Authentication failed` | username/password salah, atau `SSH_PASSWORD` belum diisi di terminal yang sama |
| SNMP `No SNMP response` | port forwarding bukan UDP, `snmpd` mati, atau community string tidak sama dengan `snmpd.conf` |
| `ModuleNotFoundError` | venv belum aktif atau `pip install paramiko pysnmp` belum dijalankan |
| `AttributeError: indent` | versi Python di bawah 3.9; perbarui Python |

---

