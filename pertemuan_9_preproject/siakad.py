import os
import time
from datetime import datetime

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
    @staticmethod
    def konversi_bobot(nilai):
        if nilai >= 80:
            return 4.0
        elif nilai >= 70:
            return 3.0
        elif nilai >= 60:
            return 2.0
        elif nilai >= 50:
            return 1.0
        else:
            return 0.0

class Mahasiswa(User):
    def __init__(self, user_id, nama, password):
        super().__init__(user_id, nama, password)
        self._ipk = 0.0
    def ambil_jadwal(self, kode_mk, daftar_matkul, daftar_krs):
        if kode_mk not in daftar_matkul:
            raise DataTidakDitemukanError(f"Matkul dengan kode {kode_mk} tidak ditemukan")
        for k in daftar_krs:
            if k["mahasiswa_id"] == self.id and k["kode_mk"] == kode_mk:
                print(f"Jadwal matakuliah {kode_mk} sudah diambil sebelumnya")
                return
        daftar_krs.append({"mahasiswa_id": self.id, "kode_mk": kode_mk})
        print(f"Berhasil mengambil jadwal matakuliah {kode_mk}")
    def lihat_jadwal(self, daftar_krs, daftar_matkul):
        print(f"Jadwal {self.nama}:")
        for k in daftar_krs:
            if k["mahasiswa_id"] ==self.id and k["kode_mk"] in daftar_matkul:
                mk = daftar_matkul[k["kode_mk"]]
                print(f"{k['kode_mk']} - {mk['nama']} ({mk['sks']} SKS)")
    def lihat_nilai(self, daftar_nilai, daftar_matkul):
        print(f"Nilai {self.nama}:")
        found = False
        for n in daftar_nilai:
            if n["mahasiswa_id"] == self.id and n["kode_mk"] in daftar_matkul:
                mk = daftar_matkul[n["kode_mk"]]
                print(f"{n['kode_mk']} - {mk['nama']}: {n['nilai']}")
                found = True
        if not found:
            print("Belum ada nilai yang dicatat")
    def hitung_ipk(self, daftar_nilai, daftar_matkul):
        total_bobot = 0.0
        total_sks = 0
        for n in daftar_nilai:
            if n["mahasiswa_id"] == self.id and n["kode_mk"] in daftar_matkul:
                sks = daftar_matkul[n["kode_mk"]]["sks"]
                bobot = self.konversi_bobot(n["nilai"])
                total_bobot += bobot * sks
                total_sks += sks
        if total_sks == 0:
            print("Nilai belum keluar, IPK tidak dapat dihitung")
            return 0.0
        self._ipk = total_bobot / total_sks
        print(f"IPK kamu adalah: {self._ipk:.2f}")
        return self._ipk
    def tampilkan_menu(self):
        print("""
1. Ambil Jadwal
2. Lihat Jadwal
3. Lihat Nilai
4. Hitung IPK
5. Logout
6. Logout dan Keluar
""")

class Dosen(User):
    def catat_kehadiran(self, kode_mk, sesi, mahasiswa_id, status, daftar_absensi):
        for a in daftar_absensi:
            if a["mahasiswa_id"] == mahasiswa_id and a["kode_mk"] == kode_mk and a["sesi"] == sesi:
                raise AbsensiGandaError("Absensi untuk mahasiswa ini pada matakuliah ini dan sesi ini sudah dicatat")
        daftar_absensi.append({"mahasiswa_id": mahasiswa_id, "kode_mk": kode_mk, "sesi": sesi, "status": status})
        print(f"Mahasiswa {mahasiswa_id} pada matakuliah {kode_mk} sesi {sesi} berhasil dicatat kehadirannya sebagai {status}")
    def input_nilai(self, kode_mk, mahasiswa_id, nilai, daftar_nilai):
        if not (0 <= nilai <= 100):
            raise NilaiTidakValidError("Nilai harus diantara 0 dan 100")
        for n in daftar_nilai:
            if n["mahasiswa_id"] == mahasiswa_id and n["kode_mk"] == kode_mk:
                raise NilaiTidakValidError("Nilai untuk mahasiswa ini pada matakuliah ini sudah dicatat")
        daftar_nilai.append({"mahasiswa_id": mahasiswa_id, "kode_mk": kode_mk, "nilai": nilai})
        print(f"Nilai {nilai} untuk mahasiswa {mahasiswa_id} pada matakuliah {kode_mk} berhasil dicatat")
    def lihat_rekap_kehadiran(self, kode_mk, daftar_absensi):
        print(f"Rekap Kehadiran untuk matakuliah {kode_mk}:")
        found = False
        for a in daftar_absensi:
            if a["kode_mk"] == kode_mk:
                print(f"Mahasiswa {a['mahasiswa_id']} - Sesi {a['sesi']}: {a['status']}")
                found = True
        if not found:
            print("Belum ada absensi yang dicatat untuk matakuliah ini")
    def tampilkan_menu(self):
        print(""" 
1. Catat Kehadiran
2. Input Nilai
3. Lihat Rekap Kehadiran
4. Logout
5. Logout dan Keluar
""")

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
                daftar_absensi.append({"mahasiswa_id": parts[1], "kode_mk": parts[2], "sesi": int(parts[3]), "status": parts[4]})

            elif prefix == "NILAI":
                daftar_nilai.append({"mahasiswa_id": parts[1], "kode_mk": parts[2], "nilai": float(parts[3])})

    return users, daftar_matkul, daftar_krs, daftar_absensi, daftar_nilai

def save_semua_data(users, daftar_matkul, daftar_krs, daftar_absensi, daftar_nilai):
    with open ("data.txt", "w") as f:
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
            elif u["role"] == "dosen":
                return Dosen(u["id"], u["nama"], u["password"])
    raise DataTidakDitemukanError("Data tidak ditemukan atau ID/Password salah")

def main():
    users, daftar_matkul, daftar_krs, daftar_absensi, daftar_nilai = load_semua_data()
    waktu_sekarang = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("Selamat datang di Sistem Informasi Akademik (SIAKAD) \n", waktu_sekarang)
    time.sleep(1)

    while True:
        id_input = input("Masukkan ID: ")
        password_input = input("Masukkan Password: ")
        try:
            user = login(users, id_input, password_input)
        except DataTidakDitemukanError as e:
            print(e)
            continue
        print(f"Selamat datang, {user.nama}!")

        while True:
            user.tampilkan_menu()
            pilihan = input("Pilih opsi > ")

            if isinstance(user, Mahasiswa):
                if pilihan == "1":
                    kode_mk = input("Masukkan kode matakuliah: ")
                    try:
                        user.ambil_jadwal(kode_mk, daftar_matkul, daftar_krs)
                        save_semua_data(users, daftar_matkul, daftar_krs, daftar_absensi, daftar_nilai)
                    except DataTidakDitemukanError as e:
                        print(e)
                elif pilihan == "2":
                    user.lihat_jadwal(daftar_krs, daftar_matkul)
                elif pilihan == "3":
                    user.lihat_nilai(daftar_nilai, daftar_matkul)
                elif pilihan == "4":
                    user.hitung_ipk(daftar_nilai, daftar_matkul)
                elif pilihan == "5":
                    print("Logout berhasil")
                    break
                elif pilihan == "6":
                    print("Logout dan keluar berhasil")
                    return
                else:
                    print("Pilihan tidak valid")

            if isinstance(user, Dosen):
                if pilihan == "1":
                    kode_mk = input("Masukkan kode matakuliah: ")
                    sesi = int(input("Masukkan sesi: "))
                    mahasiswa_id = input("Masukkan ID mahasiswa: ")
                    status = input("Masukkan status (Hadir/Izin/Sakit/Ghaib): ")
                    try:
                        user.catat_kehadiran(kode_mk, sesi, mahasiswa_id, status, daftar_absensi)
                        save_semua_data(users, daftar_matkul, daftar_krs, daftar_absensi, daftar_nilai)
                    except AbsensiGandaError as e:
                        print(e)
                elif pilihan == "2":
                    kode_mk = input("Masukkan kode matakuliah: ")
                    mahasiswa_id = input("Masukkan ID mahasiswa: ")
                    nilai = float(input("Masukkan nilai (0-100): "))
                    try:
                        user.input_nilai(kode_mk, mahasiswa_id, nilai, daftar_nilai)
                        save_semua_data(users, daftar_matkul, daftar_krs, daftar_absensi, daftar_nilai)
                    except NilaiTidakValidError as e:
                        print(e)
                elif pilihan == "3":
                    kode_mk = input("Masukkan kode matakuliah: ")
                    user.lihat_rekap_kehadiran(kode_mk, daftar_absensi)
                elif pilihan == "4":
                    print("Logout berhasil")
                    break
                elif pilihan == "5":
                    print("Logout dan keluar berhasil")
                    return
                else:
                    print("Pilihan tidak valid")

if __name__ == "__main__":
    main()