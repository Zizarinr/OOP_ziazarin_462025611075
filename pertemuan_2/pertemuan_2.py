class Kampus:
    pass
class Mahasiswa:
    pass

print("test")

class Prodi:
    nama = ''
    jurusan = ''

    def status():
        print(f"Prodi memiliki ruangan kelas yang nyaman")
    def ruangan(self):
        print(f"Ruangannya berada di gedung {self.nama} jurusan {self.jurusan}")
    def matkul(self):
        print(f"Matkul yang diajarkan di jurusan {self.jurusan} adalah ...")
    def gudang(self, nama_gudang):
        print(f"Gudangnya berada di gedung {nama_gudang} jurusan {self.jurusan}")

prodi1 = Prodi()
prodi1.nama = "Informatika"
prodi1.jurusan = "Teknik Informatika"
prodi1.ruangan()
prodi1.matkul()
prodi1.gudang('Gudang Bawah')
Prodi.status()