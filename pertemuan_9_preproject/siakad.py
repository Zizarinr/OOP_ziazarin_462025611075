import os
import time

class DataTidakDitemukanError(Exception): pass
class NilaiTidakValidError(Exception): pass
class AbsensiGandaError(Exception):pass

class User:
    def __init__(self, user_id, nama, password):
        self.id = user_id
        self.nama = nama
        self.password = password
    def tampilkan_menu(self):
        raise NotImplementedError("tidak diimplementasikan")

class Mahasiswa(User):
    def __init__(self, user_id, nama, password):
        super().__init__(user_id, nama, password)
        self._ipk = 0.0
    def ambil_jadwal(self, kode_mk, daftar_matkul, daftar_krs):
        ...
    def lihat_jadwal(self, daftar_krs):
        ...
    def lihat_nilai(self, daftar_nilai):
        ...
    def hitung_ipk(self, daftar_nilai, daftar_matkul):
        ...
    def tampilkan_menu(self):
        print("""
1. Ambil Jadwal
2. Lihat Jadwal
3. Lihat Nilai
4. Hitung IPK
5. Logout
""")

class Dosen(User):
    def catat_kehadiran(self, kode_mk, sesi, mahasiswa_id, status, daftar_absensi):
        ...
    def input_nilai(self, kode_mk, mahasiswa_id, nilai, daftar_nilai):
        if not (0 <= nilai <= 100):
            raise NilaiTidakValidError("Nilai harus diantara 0 dan 100")
    def lihat_rekap_kehadiran(self, kode_mk, daftar_absensi):
        ...
    def tampilkan_menu(self):
        print("""
1. Catat Kehadiran
2. Input Nilai
3. Lihat Rekap Kehadiran
4. Logout
""")

def load_semua_data():
    users = []
    daftar_matkul = []
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
            elif prefix == "ABSENSI":
                daftar_absensi.append({"mahasiswa_id": parts[1], "kode_mk": parts[2], "sesi": int(parts[3]), "status": parts[4]})

            elif prefix == "NILAI":
                daftar_nilai.append({"mahasiswa_id": parts[1], "kode_mk": parts[2], "nilai": float(parts[3])})

    return users, daftar_matkul, daftar_krs, daftar_absensi, daftar_nilai