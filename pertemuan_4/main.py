class Stokwarehouse:
    def __init__(self, nama_warehouse, id_barang, nama_barang, jumlah, satuan):
        self.nama_warehouse = nama_warehouse
        self.id_barang = id_barang
        self.nama_barang = nama_barang
        self.jumlah = jumlah
        self.satuan = satuan
    def __str__(self):
        return f"Stok {self.nama_barang} di {self.nama_warehouse}: {self.jumlah} {self.satuan}"
    def __eq__(self, other):
        if isinstance(other, Stokwarehouse):
            return self.id_barang == other.id_barang and self.jumlah == other.jumlah
        return False
    def __lt__(self, other):
        if isinstance(other, Stokwarehouse):
            return self.jumlah < other.jumlah
        return False
    def __gt__(self, other):
        if isinstance(other, Stokwarehouse):
            return self.jumlah > other.jumlah
        return False

stok1 = Stokwarehouse("Warehouse Gudang Garam", "GG001", "Tembakau", 50, "Ton")
stok2 = Stokwarehouse("Warehouse Gudang Cocis", "GC030", "Emulsifier", 250, "kwintal")

print(stok1)
print(stok2)
print("Gudang Garam == Gudang Cocis   : ", stok1 == stok2)  
print("Gudang Garam < Gudang Cocis    : ", stok1 < stok2)   
print("Gudang Garam > Gudang Cocis    : ", stok1 > stok2)   