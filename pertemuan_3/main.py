class opWarnet:
    nama = ""
    alamat = ""
    jumlah_komputer = 0
    harga_per_jam = 0
    def __init__(self, nama, alamat, jumlah_komputer, harga_per_jam):
        self.nama = nama
        self.alamat = alamat
        self.jumlah_komputer = jumlah_komputer
        self.harga_per_jam = harga_per_jam
    def greeting(self):
        return print("Selamat datang di " + self.nama + "!")
    def get_nama(self):
        return self.nama
    def get_alamat(self):
        return self.alamat
    def get_jumlah_komputer(self):
        return self.jumlah_komputer
    def get_harga_per_jam(self):
        return self.harga_per_jam
    @staticmethod
    def harga_paketMalam(jam):
        return print("Total Harga Paket Malam: Rp.", 3000 * jam)
    
opWarnet1 = opWarnet("Warnet Agung", "Jl. Merdeka No. 1", 10, 5000)
opWarnet1.greeting()
jam = int(input("Masukkan jumlah rencana jam: "))
opWarnet1.get_nama()
opWarnet.harga_paketMalam(jam)

