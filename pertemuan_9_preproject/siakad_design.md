# Rancangan Sistem SIAKAD Mini (Versi Simplified)

> Filosofi: kompleksitas teknis dibuat semirip mungkin dengan `studi_kasus.py` (1 file data, tanpa class manager terpisah), tapi 4 fitur dan konsep OOP dari proposal tetap dipertahankan.

## 1. Struktur File Data — `data.txt` (1 file saja)

Semua entitas digabung dalam satu file, dibedakan lewat kolom pertama (prefix):

```
USER,mahasiswa,2201001,Genzme,pass123
USER,dosen,D001,PakAhmad,dosen123
MK,TI101,Algoritma Pemrograman,3,D001
MK,TI102,Basis Data,3,D001
KRS,2201001,TI101
ABSEN,2201001,TI101,1,hadir
NILAI,2201001,TI101,85
```

**Penjelasan kolom per prefix:**
- `USER,role,id,nama,password`
- `MK,kode_mk,nama_mk,sks,dosen_id`
- `KRS,mahasiswa_id,kode_mk`
- `ABSEN,mahasiswa_id,kode_mk,sesi,status`
- `NILAI,mahasiswa_id,kode_mk,nilai`

Saat program start, file ini dibaca baris per baris, lalu tiap baris di-routing ke struktur data di memory (list/dict) berdasarkan prefix-nya.

---

## 2. Struktur Data di Memory (tanpa class manager)

Daripada bikin class `SistemAkademik`, cukup pakai variabel global biasa di `main()`, persis seperti `bank = Bank(...)` di `studi_kasus.py`:

```python
daftar_matkul = {}      # { kode_mk: {"nama": ..., "sks": ..., "dosen_id": ...} }
daftar_krs = []         # [ {"mahasiswa_id":..., "kode_mk":...}, ... ]
daftar_absensi = []     # [ {"mahasiswa_id":..., "kode_mk":..., "sesi":..., "status":...}, ... ]
daftar_nilai = []       # [ {"mahasiswa_id":..., "kode_mk":..., "nilai":...}, ... ]
```

> `MataKuliah` **tidak dibuat sebagai class** karena ia tidak punya behavior sendiri (cuma data referensi) — cukup disimpan sebagai dictionary.

---

## 3. Class Diagram (Tetap Mempertahankan Inheritance & Polymorphism)

```
User (base class)
├── atribut: id, nama, password
├── method: tampilkan_menu()   → akan dioverride (raise NotImplementedError di base)
│
├── Mahasiswa(User)
│   ├── atribut tambahan: -_ipk (private, encapsulation)
│   ├── ambil_jadwal(kode_mk)
│   ├── lihat_jadwal()
│   ├── lihat_nilai()
│   ├── hitung_ipk()             → method, tidak bisa diakses/diubah langsung dari luar
│   └── tampilkan_menu()         → override (polymorphism)
│
└── Dosen(User)
    ├── catat_kehadiran(kode_mk, sesi, mahasiswa_id, status)
    ├── input_nilai(mahasiswa_id, kode_mk, nilai)
    ├── lihat_rekap_kehadiran(kode_mk)
    └── tampilkan_menu()         → override (polymorphism)
```

---

## 4. Custom Exceptions (dipangkas jadi 3 saja)

```python
class DataTidakDitemukanError(Exception): pass    # gabungan: matkul/akun/user tidak ditemukan
class NilaiTidakValidError(Exception): pass        # nilai di luar 0-100
class AbsensiGandaError(Exception): pass           # sesi yang sama dicatat 2x
```

> 5 exception dari rancangan awal disederhanakan jadi 3 dengan menggabungkan kasus-kasus "data tidak ditemukan" (akun, matkul, login) jadi satu exception generik.

---

## 5. Struktur Kode (Single File, seperti `studi_kasus.py`)

```python
# siakad.py
import os
import time

# ============================
# 1. CUSTOM EXCEPTIONS
# ============================
class DataTidakDitemukanError(Exception): pass
class NilaiTidakValidError(Exception): pass
class AbsensiGandaError(Exception): pass


# ============================
# 2. CLASS: User (Base)
# ============================
class User:
    def __init__(self, id, nama, password):
        self.id = id
        self.nama = nama
        self.password = password

    def tampilkan_menu(self):
        raise NotImplementedError


# ============================
# 3. CLASS: Mahasiswa(User)
# ============================
class Mahasiswa(User):
    def __init__(self, id, nama, password):
        super().__init__(id, nama, password)
        self._ipk = 0.0   # encapsulation: diisi lewat hitung_ipk(), bukan langsung

    def ambil_jadwal(self, kode_mk, daftar_matkul, daftar_krs):
        ...

    def lihat_jadwal(self, daftar_krs):
        ...

    def lihat_nilai(self, daftar_nilai):
        ...

    def hitung_ipk(self, daftar_nilai, daftar_matkul):
        # update self._ipk, lalu return nilainya
        ...

    def tampilkan_menu(self):
        print("1. Ambil Jadwal\n2. Lihat Jadwal\n3. Lihat Nilai\n4. Lihat IPK\n5. Logout")


# ============================
# 4. CLASS: Dosen(User)
# ============================
class Dosen(User):
    def catat_kehadiran(self, kode_mk, sesi, mahasiswa_id, status, daftar_absensi):
        ...

    def input_nilai(self, mahasiswa_id, kode_mk, nilai, daftar_nilai):
        if not (0 <= nilai <= 100):
            raise NilaiTidakValidError("Nilai harus di antara 0-100")
        ...

    def lihat_rekap_kehadiran(self, kode_mk, daftar_absensi):
        ...

    def tampilkan_menu(self):
        print("1. Catat Kehadiran\n2. Input Nilai\n3. Lihat Rekap Kehadiran\n4. Logout")


# ============================
# 5. FUNGSI LOAD & SAVE DATA (global, bukan method class)
# ============================
def load_semua_data():
    users = []
    daftar_matkul = {}
    daftar_krs = []
    daftar_absensi = []
    daftar_nilai = []

    if not os.path.exists("data.txt"):
        open("data.txt", "w").close()
        return users, daftar_matkul, daftar_krs, daftar_absensi, daftar_nilai

    with open("data.txt", "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(",")
            prefix = parts[0]

            if prefix == "USER":
                users.append({"role": parts[1], "id": parts[2], "nama": parts[3], "password": parts[4]})
            elif prefix == "MK":
                daftar_matkul[parts[1]] = {"nama": parts[2], "sks": int(parts[3]), "dosen_id": parts[4]}
            elif prefix == "KRS":
                daftar_krs.append({"mahasiswa_id": parts[1], "kode_mk": parts[2]})
            elif prefix == "ABSEN":
                daftar_absensi.append({"mahasiswa_id": parts[1], "kode_mk": parts[2], "sesi": parts[3], "status": parts[4]})
            elif prefix == "NILAI":
                daftar_nilai.append({"mahasiswa_id": parts[1], "kode_mk": parts[2], "nilai": int(parts[3])})

    return users, daftar_matkul, daftar_krs, daftar_absensi, daftar_nilai


def simpan_semua_data(users, daftar_matkul, daftar_krs, daftar_absensi, daftar_nilai):
    with open("data.txt", "w") as f:
        for u in users:
            f.write(f"USER,{u['role']},{u['id']},{u['nama']},{u['password']}\n")
        for kode_mk, mk in daftar_matkul.items():
            f.write(f"MK,{kode_mk},{mk['nama']},{mk['sks']},{mk['dosen_id']}\n")
        for k in daftar_krs:
            f.write(f"KRS,{k['mahasiswa_id']},{k['kode_mk']}\n")
        for a in daftar_absensi:
            f.write(f"ABSEN,{a['mahasiswa_id']},{a['kode_mk']},{a['sesi']},{a['status']}\n")
        for n in daftar_nilai:
            f.write(f"NILAI,{n['mahasiswa_id']},{n['kode_mk']},{n['nilai']}\n")


def login(users, id_input, password_input):
    for u in users:
        if u["id"] == id_input and u["password"] == password_input:
            if u["role"] == "mahasiswa":
                return Mahasiswa(u["id"], u["nama"], u["password"])
            else:
                return Dosen(u["id"], u["nama"], u["password"])
    raise DataTidakDitemukanError("ID atau password salah")


# ============================
# 6. MAIN
# ============================
def main():
    print("Memuat data...")
    users, daftar_matkul, daftar_krs, daftar_absensi, daftar_nilai = load_semua_data()
    time.sleep(1)
    print("Selamat datang di SIAKAD!")

    while True:
        id_input = input("ID: ")
        password_input = input("Password: ")
        try:
            user = login(users, id_input, password_input)
        except DataTidakDitemukanError as e:
            print(e)
            continue

        user.tampilkan_menu()
        # ... lanjut logic menu sesuai pilihan, panggil method user.* yang sesuai
        # ... setelah aksi yang ubah data, panggil simpan_semua_data(...)

        break  # placeholder, nanti diganti logic menu lengkap


if __name__ == "__main__":
    main()
    print("Terima kasih telah menggunakan SIAKAD. Sampai jumpa!")
```

---

## 6. Perbandingan dengan Rancangan Awal

| Aspek | Rancangan Awal | Versi Simplified |
|-------|----------------|-------------------|
| File data | 5 file `.txt` | 1 file `data.txt` |
| Class | 5 (`User`, `Mahasiswa`, `Dosen`, `MataKuliah`, `SistemAkademik`) | 3 (`User`, `Mahasiswa`, `Dosen`) |
| Custom exception | 5 | 3 |
| Fungsi load/save | Method di class manager | Fungsi global (seperti pola `studi_kasus.py`) |
| Inheritance & Polymorphism | Ada | **Tetap ada** |
| Encapsulation | Ada | **Tetap ada** |
| 4 fitur proposal (absensi, jadwal, nilai, IPK) | Ada | **Tetap ada, tidak dipotong** |

---

## 7. Catatan Implementasi

- Bagian `main()` di atas baru kerangka — logic menu lengkap (input pilihan 1-5, percabangan tiap aksi, try/except per aksi) menyusul mengikuti pola `studi_kasus.py` yang sudah kamu pelajari.
- `hitung_ipk()` perlu skala nilai yang jelas dulu (0-100 dikonversi ke bobot 0-4, atau langsung dirata-rata dari skala 100). Putuskan ini sebelum mulai isi method-nya.
- `AbsensiGandaError` dicek dengan memastikan kombinasi `(mahasiswa_id, kode_mk, sesi)` belum ada di `daftar_absensi` sebelum `catat_kehadiran()` menambah entri baru.
