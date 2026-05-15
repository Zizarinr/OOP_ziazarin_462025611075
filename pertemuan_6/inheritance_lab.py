class standarLab: #p gabut
    def __init__(self, nama, jurusan, fakultas):
        self.nama = nama
        self.jurusan = jurusan
        self.fakultas = fakultas
    def info(self):
        print(f"Ini adalah Lab {self.nama}, milik jurusan {self.jurusan} di gedung fakultas {self.fakultas}")
    def quality(self):
        print(f"Lab {self.nama} memiliki kualitas yang baik untuk pembelajaran.")
class labKomputer(standarLab):
    def software(self):
        print(f"Lab Komputer {self.nama} dilengkapi dengan software terbaru untuk pembelajaran komputer.")
    def qualify_lab(self):
        super().quality()
    def cekDiamondProblem(self):
        print("Cek diamond problem di kelas labKomputer.")

class labGizi(standarLab):
    def peralatan(self):
        print(f"Lab Gizi {self.nama} dilengkapi dengan peralatan memadai untuk praktikum gizi.")
    def qualify_lab(self):
        super().quality()
    def cekDiamondProblem(self):
        print("Cek diamond problem di kelas labGizi.")

class labBioteknologi(labKomputer, labGizi):
    def info_lab_bioteknologi(self):
        print(f"Lab Bioteknologi {self.nama} merupakan gabungan dari lab komputer dan lab gizi.")
    def biotech_peralatan(self):
        super().peralatan()
    def biotech_software(self):
        super().software()
    def qualify_lab(self):
        super().quality()

lab_bio = labBioteknologi("Kenari Alpha", "Teknologi Pangan", "Teknik Industri Pertanian")
lab_bio.info()
lab_bio.info_lab_bioteknologi()
lab_bio.biotech_peralatan()
lab_bio.biotech_software()
lab_bio.qualify_lab()
lab_bio.cekDiamondProblem()