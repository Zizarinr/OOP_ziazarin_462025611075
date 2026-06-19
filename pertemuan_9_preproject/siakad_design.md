# Rancangan Sistem SIAKAD Mini

## 1. Struktur File Data (.txt, CSV-style)

**`users.txt`** — gabungan mahasiswa & dosen, dibedakan kolom `role`
```
role,id,nama,password
mahasiswa,2201001,Genzme,pass123
dosen,D001,Pak Ahmad,dosen123
```

**`matakuliah.txt`** — daftar matkul yang tersedia
```
kode_mk,nama_mk,sks,dosen_id
TI101,Algoritma Pemrograman,3,D001
TI102,Basis Data,3,D001
```

**`krs.txt`** — relasi mahasiswa ke matkul yang diambil
```
mahasiswa_id,kode_mk
2201001,TI101
2201001,TI102
```

**`absensi.txt`** — rekap kehadiran per sesi
```
mahasiswa_id,kode_mk,sesi,status
2201001,TI101,1,hadir
2201001,TI101,2,absen
```

**`nilai.txt`** — nilai akhir per matkul yang sudah diambil
```
mahasiswa_id,kode_mk,nilai
2201001,TI101,85
```

---

## 2. Class Diagram (Konsep)

```
User (base class)
├── atribut: id, nama, password
├── method: login()
│
├── Mahasiswa(User)
│   ├── atribut tambahan: -nilai (private), -ipk (private)
│   ├── ambil_jadwal(kode_mk)
│   ├── lihat_jadwal()
│   ├── lihat_nilai()
│   ├── hitung_ipk()          → Encapsulation: ipk dihitung internal, read-only ke luar
│   └── tampilkan_menu()      → Polymorphism: override dari User
│
└── Dosen(User)
    ├── catat_kehadiran(kode_mk, sesi, mahasiswa_id, status)
    ├── input_nilai(mahasiswa_id, kode_mk, nilai)
    ├── lihat_rekap_kehadiran(kode_mk)
    └── tampilkan_menu()      → Polymorphism: override dari User

MataKuliah
├── atribut: kode_mk, nama_mk, sks, dosen_id

SistemAkademik (kelas pengelola / manager)
├── load_users(), load_matakuliah(), load_krs(), load_absensi(), load_nilai()
├── save_krs(), save_absensi(), save_nilai()
├── cari_user(id, password)
└── main_loop()
```

---

## 3. Custom Exceptions

```python
class JadwalBentrokError(Exception): pass
class NilaiTidakValidError(Exception): pass       # nilai di luar 0-100
class AbsensiGandaError(Exception): pass          # sesi yang sama dicatat 2x
class MataKuliahTidakDitemukanError(Exception): pass
class LoginGagalError(Exception): pass
```

> Catatan: karena tanpa konsep kapasitas kelas, `JadwalBentrokError` bisa dipakai untuk kasus mahasiswa mengambil matkul yang sama dua kali (bukan bentrok waktu, tapi duplikasi KRS).

---

## 4. Struktur File Kode (Python)

Disarankan **1 file** untuk tugas (`siakad.py`), karena studi_kasus.py juga single-file. Tapi disusun dalam section yang rapi:

```python
# siakad.py

# ============================
# 1. CUSTOM EXCEPTIONS
# ============================
class JadwalBentrokError(Exception): ...
class NilaiTidakValidError(Exception): ...
class AbsensiGandaError(Exception): ...
class MataKuliahTidakDitemukanError(Exception): ...
class LoginGagalError(Exception): ...


# ============================
# 2. CLASS: User (Base)
# ============================
class User:
    def __init__(self, id, nama, password):
        self.id = id
        self.nama = nama
        self.password = password

    def tampilkan_menu(self):
        raise NotImplementedError  # akan dioverride


# ============================
# 3. CLASS: Mahasiswa(User)
# ============================
class Mahasiswa(User):
    def __init__(self, id, nama, password):
        super().__init__(id, nama, password)
        self._nilai = {}      # encapsulation: diisi lewat method, bukan langsung
        self._ipk = 0.0

    def ambil_jadwal(self, kode_mk, daftar_matkul, daftar_krs): ...
    def lihat_jadwal(self, daftar_krs): ...
    def lihat_nilai(self, daftar_nilai): ...
    def hitung_ipk(self, daftar_nilai, daftar_matkul): ...
    def tampilkan_menu(self): ...   # override


# ============================
# 4. CLASS: Dosen(User)
# ============================
class Dosen(User):
    def catat_kehadiran(self, kode_mk, sesi, mahasiswa_id, status, daftar_absensi): ...
    def input_nilai(self, mahasiswa_id, kode_mk, nilai, daftar_nilai): ...
    def lihat_rekap_kehadiran(self, kode_mk, daftar_absensi): ...
    def tampilkan_menu(self): ...   # override


# ============================
# 5. CLASS: MataKuliah
# ============================
class MataKuliah:
    def __init__(self, kode_mk, nama_mk, sks, dosen_id):
        ...


# ============================
# 6. CLASS: SistemAkademik (Manager)
# ============================
class SistemAkademik:
    def __init__(self):
        self.users = []
        self.matakuliah = []
        self.krs = []
        self.absensi = []
        self.nilai = []

    def load_semua_data(self): ...      # baca semua .txt saat start
    def simpan_krs(self): ...
    def simpan_absensi(self): ...
    def simpan_nilai(self): ...
    def login(self, id, password): ...  # return objek Mahasiswa/Dosen, raise LoginGagalError
    def main_loop(self): ...            # menu utama, while True


# ============================
# 7. MAIN
# ============================
if __name__ == "__main__":
    sistem = SistemAkademik()
    sistem.load_semua_data()
    sistem.main_loop()
```

---

## 5. Alur Program (High-Level)

1. Start → cek semua file `.txt` ada/tidak (buat kosong kalau belum ada, seperti `studi_kasus.py`)
2. Load semua data ke memory (list of objects)
3. Tampilkan menu login → input id & password → `SistemAkademik.login()`
   - Jika gagal → `LoginGagalError`
   - Jika berhasil → buat objek `Mahasiswa` atau `Dosen` sesuai role
4. Panggil `tampilkan_menu()` → polymorphic, beda isi menu tergantung role
5. User pilih fitur sesuai role:
   - **Mahasiswa**: ambil jadwal, lihat jadwal, lihat nilai, lihat IPK
   - **Dosen**: catat kehadiran, input nilai, lihat rekap kehadiran
6. Setiap aksi yang mengubah data → langsung `simpan_*()` ke file (biar persistent)
7. Validasi pakai try/except dengan custom exception di setiap aksi
8. Logout / Exit → kembali ke menu login atau keluar program

---

## 6. Mapping OOP — Ringkasan

| Konsep | Implementasi |
|--------|--------------|
| **Inheritance** | `Mahasiswa` dan `Dosen` mewarisi `User` |
| **Encapsulation** | `_nilai`, `_ipk` di Mahasiswa diakses lewat method, bukan langsung diubah dari luar |
| **Polymorphism** | `tampilkan_menu()` beda implementasi di `Mahasiswa` vs `Dosen` |
| **Exception Handling** | 5 custom exception untuk validasi tiap aksi |
