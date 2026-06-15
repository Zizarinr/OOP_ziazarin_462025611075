class userPinjol:
    __nama = ""
    __email = ""
    __nomor_telepon = ""
    __total_pinjaman = ""
    __password = ""
    def __init__(self, nama, email, nomor_telepon, total_pinjaman, password):
        self.__nama = nama
        self.__email = email
        self.__nomor_telepon = nomor_telepon
        self.__total_pinjaman = total_pinjaman
        self.__password = password
    def get_nama(self):
        return self.__nama
    def get_email(self):
        return self.__email
    def get_nomor_telepon(self):
        return self.__nomor_telepon
    def get_total_pinjaman(self, password=None):
        while password != self.__password:
            print("Password salah. Tidak dapat menampilkan total pinjaman, silakan coba lagi.")
            password = input("Password: ")
        print(f"Total pinjaman Anda saat ini: Rp.{self.__total_pinjaman}")
    
user1 = userPinjol("Ujang", "ujang@email.com", "08123456789", 1000000, "atmin123")
print("Selamat datang, " + user1.get_nama() + "!")
print("Silahkan masukkan password untuk melihat total pinjaman Anda.")
password = input("Password: ")
user1.get_total_pinjaman(password)