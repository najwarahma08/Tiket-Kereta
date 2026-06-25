import csv
import os
from datetime import datetime
from collections import defaultdict

# ==================== STRUKTUR DATA ====================

class Node:
    """Node untuk Linked List"""
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    """Implementasi Linked List untuk menyimpan tiket kereta"""
    def __init__(self):
        self.kepala = None
        self.ekor = None
        self.ukuran = 0

    def tambah(self, data):
        """Menambahkan data di akhir linked list"""
        simpul_baru = Node(data)
        if self.kepala is None:
            self.kepala = simpul_baru
            self.ekor = simpul_baru
        else:
            self.ekor.next = simpul_baru
            self.ekor = simpul_baru
        self.ukuran += 1

    def ke_list(self):
        """Mengubah linked list menjadi list Python"""
        hasil = []
        saat_ini = self.kepala
        while saat_ini:
            hasil.append(saat_ini.data)
            saat_ini = saat_ini.next
        return hasil

    def cari(self, kunci, nilai):
        """Mencari data berdasarkan kunci dan nilai"""
        saat_ini = self.kepala
        while saat_ini:
            if saat_ini.data.get(kunci) == nilai:
                return saat_ini.data
            saat_ini = saat_ini.next
        return None

    def hapus(self, kunci, nilai):
        """Menghapus data berdasarkan kunci dan nilai"""
        saat_ini = self.kepala
        sebelumnya = None
        while saat_ini:
            if saat_ini.data.get(kunci) == nilai:
                if sebelumnya:
                    sebelumnya.next = saat_ini.next
                else:
                    self.kepala = saat_ini.next
                if saat_ini == self.ekor:
                    self.ekor = sebelumnya
                self.ukuran -= 1
                return True
            sebelumnya = saat_ini
            saat_ini = saat_ini.next
        return False

    def perbarui(self, kunci, nilai, data_baru):
        """Memperbarui data berdasarkan kunci dan nilai"""
        saat_ini = self.kepala
        while saat_ini:
            if saat_ini.data.get(kunci) == nilai:
                saat_ini.data.update(data_baru)
                return True
            saat_ini = saat_ini.next
        return False

class Tumpukan:
    """Implementasi Stack/Tumpukan untuk riwayat pembelian"""
    def __init__(self):
        self.item = []

    def dorong(self, item):
        """Menambahkan item ke tumpukan"""
        self.item.append(item)

    def ambil(self):
        """Mengambil item dari tumpukan (LIFO)"""
        if not self.kosong():
            return self.item.pop()
        return None

    def lihat_teratas(self):
        """Melihat item teratas tanpa menghapus"""
        if not self.kosong():
            return self.item[-1]
        return None

    def kosong(self):
        """Memeriksa apakah tumpukan kosong"""
        return len(self.item) == 0

    def semua(self):
        """Mengambil semua item dalam tumpukan"""
        return self.item.copy()

class TabelHash:
    """Implementasi Hash Table untuk indeks pencarian cepat"""
    def __init__(self):
        self.tabel = defaultdict(list)

    def sisipkan(self, kunci, nilai):
        """Menambahkan pasangan kunci-nilai ke hash table"""
        self.tabel[kunci].append(nilai)

    def cari(self, kunci):
        """Mencari nilai berdasarkan kunci"""
        return self.tabel.get(kunci, [])

    def hapus(self, kunci, nilai):
        """Menghapus nilai dari kunci tertentu"""
        if kunci in self.tabel:
            self.tabel[kunci] = [v for v in self.tabel[kunci] if v != nilai]
            if not self.tabel[kunci]:
                del self.tabel[kunci]

# ==================== MANAJEMEN CSV ====================

class DatabaseTiketKereta:
    """Manajemen database dengan file CSV"""
    def __init__(self, nama_file="data_tiket_kereta.csv"):
        self.nama_file = nama_file
        self.kolom = ["id_tiket", "nama_penumpang", "asal", "tujuan", "tanggal_keberangkatan", "jam_keberangkatan", "harga", "status"]
        self.tiket = LinkedList()
        self.riwayat = Tumpukan()
        self.indeks = TabelHash()
        self.muat_data()

    def muat_data(self):
        """Memuat data dari file CSV"""
        if os.path.exists(self.nama_file):
            with open(self.nama_file, 'r', encoding='utf-8') as file:
                pembaca = csv.DictReader(file)
                for baris in pembaca:
                    self.tiket.tambah(dict(baris))
                    # Indexing by id_tiket, nama_penumpang, and tujuan
                    self.indeks.sisipkan(baris['id_tiket'].lower(), baris['id_tiket'])
                    self.indeks.sisipkan(baris['nama_penumpang'].lower(), baris['id_tiket'])
                    self.indeks.sisipkan(baris['tujuan'].lower(), baris['id_tiket'])
        else:
            # Buat file CSV dengan header jika belum ada
            with open(self.nama_file, 'w', newline='', encoding='utf-8') as file:
                penulis = csv.DictWriter(file, fieldnames=self.kolom)
                penulis.writeheader()
            self.inisialisasi_data_contoh()

    def inisialisasi_data_contoh(self):
        """Menambahkan data contoh awal"""
        data_contoh = [
            {"id_tiket": "T001", "asal": "Jakarta", "nama_penumpang": "Kevin Juliano", "tanggal_keberangkatan": "2026-07-01",
             "tujuan": "Bandung", "jam_keberangkatan": "08:00", "harga": "15000", "status": "Dipesan"},
            {"id_tiket": "T002", "asal": "Surabaya", "nama_penumpang": "Seano", "tanggal_keberangkatan": "2026-07-02",
             "tujuan": "Jakarta", "jam_keberangkatan": "10:00", "harga": "20000", "status": "Dipesan"},
            {"id_tiket": "T003", "asal": "Subang", "nama_penumpang": "Julian", "tanggal_keberangkatan": "2026-07-03",
             "tujuan": "Purwakarta", "jam_keberangkatan": "12:00", "harga": "25000", "status": "Dipesan"},
            {"id_tiket": "T004", "asal": "Bogor", "nama_penumpang": "Martin Ed", "tanggal_keberangkatan": "2026-07-04",
             "tujuan": "Tasik", "jam_keberangkatan": "14:00", "harga": "35000", "status": "Dibatalkan"},
        ]
        for tiket in data_contoh:
            self.tambah(tiket)

    def simpan_data(self):
        """Menyimpan data ke file CSV"""
        with open(self.nama_file, 'w', newline='', encoding='utf-8') as file:
            penulis = csv.DictWriter(file, fieldnames=self.kolom)
            penulis.writeheader()
            for tiket in self.tiket.ke_list():
                penulis.writerow(tiket)

    def tambah(self, data_tiket):
        """CREATE: Menambah tiket baru"""
        # Cek apakah ID sudah ada
        existing = self.tiket.cari("id_tiket", data_tiket["id_tiket"])
        if existing:
            return False, "ID Tiket sudah ada!"

        self.tiket.tambah(data_tiket)
        self.indeks.sisipkan(data_tiket['id_tiket'].lower(), data_tiket['id_tiket']) # Index by id_tiket
        self.indeks.sisipkan(data_tiket['nama_penumpang'].lower(), data_tiket['id_tiket'])
        self.indeks.sisipkan(data_tiket['tujuan'].lower(), data_tiket['id_tiket'])
        self.simpan_data()
        self.riwayat.dorong(f"TAMBAH: {data_tiket['id_tiket']} - {data_tiket['nama_penumpang']} ({datetime.now()})")
        return True, "Tiket berhasil ditambahkan!"

    def baca_semua(self):
        """READ: Membaca semua tiket"""
        return self.tiket.ke_list()

    def baca_by_id(self, id_tiket):
        """READ: Mencari tiket berdasarkan ID"""
        return self.tiket.cari("id_tiket", id_tiket)

    def cari_tiket(self, kata_kunci):
        """SEARCH: Mencari tiket dengan kata kunci"""
        kata_kunci = kata_kunci.lower()
        hasil = []
        for tiket in self.tiket.ke_list():
            if (kata_kunci in tiket['id_tiket'].lower() or
                kata_kunci in tiket['nama_penumpang'].lower() or
                kata_kunci in tiket['asal'].lower() or
                kata_kunci in tiket['tujuan'].lower()):
                hasil.append(tiket)
        return hasil

    def urutkan_tiket(self, berdasarkan="id_tiket", terbalik=False):
        """SORTING: Mengurutkan tiket berdasarkan field tertentu"""
        daftar_tiket = self.tiket.ke_list()
        try:
            # Sorting dengan Bubble Sort
            n = len(daftar_tiket)
            for i in range(n):
                for j in range(0, n-i-1):
                    nilai1 = daftar_tiket[j].get(berdasarkan, "")
                    nilai2 = daftar_tiket[j+1].get(berdasarkan, "")
                    if terbalik:
                        if str(nilai1) < str(nilai2):
                            daftar_tiket[j], daftar_tiket[j+1] = daftar_tiket[j+1], daftar_tiket[j]
                    else:
                        if str(nilai1) > str(nilai2):
                            daftar_tiket[j], daftar_tiket[j+1] = daftar_tiket[j+1], daftar_tiket[j]
            return daftar_tiket
        except Exception:
            # Catch broader exception to ensure function doesn't crash on unexpected data types
            return daftar_tiket

    def perbarui(self, id_tiket, data_baru):
        """UPDATE: Memperbarui data tiket"""
        # Cari tiket
        tiket_lama = self.tiket.cari("id_tiket", id_tiket)
        if not tiket_lama:
            return False, "Tiket tidak ditemukan!"

        # Update data
        # No need for this line: if data_baru.get("status") is not None: data_baru["status"] = data_baru["status"]
        # The update will be handled by the self.tiket.perbarui method

        self.tiket.perbarui("id_tiket", id_tiket, data_baru)
        self.simpan_data()
        self.riwayat.dorong(f"PERBARUI: {tiket_lama['id_tiket']} -> {data_baru.get('nama_penumpang', tiket_lama['nama_penumpang'])} ({datetime.now()})")
        return True, "Data tiket berhasil diperbarui!"

    def hapus(self, id_tiket):
        """DELETE: Menghapus tiket"""
        tiket = self.tiket.cari("id_tiket", id_tiket)
        if not tiket:
            return False, "Tiket tidak ditemukan!"

        self.tiket.hapus("id_tiket", id_tiket)
        # Hapus dari indeks
        self.indeks.hapus(tiket['nama_penumpang'].lower(), id_tiket)
        self.indeks.hapus(tiket['tujuan'].lower(), id_tiket)
        self.simpan_data()
        self.riwayat.dorong(f"HAPUS: {tiket['id_tiket']} - {tiket['nama_penumpang']} ({datetime.now()})")
        return True, "Tiket berhasil dihapus!"

    def ambil_riwayat(self):
        """Mengambil riwayat transaksi/aktivitas tiket kereta"""
        return self.riwayat.semua()

    def ambil_statistik(self):
        """Menghitung statistik tiket kereta"""
        daftar_tiket = self.tiket.ke_list()
        total = len(daftar_tiket)
        dipesan = sum(1 for t in daftar_tiket if t['status'].lower() == 'dipesan')
        dibatalkan = sum(1 for t in daftar_tiket if t['status'].lower() == 'dibatalkan')
        selesai = sum(1 for t in daftar_tiket if t['status'].lower() == 'selesai') # Added 'selesai' status

        # Statistik tujuan
        statistik_tujuan = defaultdict(int)
        for tiket in daftar_tiket:
            statistik_tujuan[tiket['tujuan']] += 1

        return {
            'total_tiket': total,
            'dipesan': dipesan,
            'dibatalkan': dibatalkan,
            'selesai': selesai, # Added 'selesai'
            'tujuan': dict(statistik_tujuan)
        }

# ==================== ANTARMUKA PENGGUNA ====================

class Aplikasi_Tiket_Kereta:
    """Aplikasi Manajemen Tiket Kereta"""
    def __init__(self):
        self.db = DatabaseTiketKereta()
        self.handler_menu = {
            '1': self.menu_tambah_tiket,
            '2': self.menu_lihat_tiket,
            '3': self.menu_cari_tiket,
            '4': self.menu_perbarui_tiket,
            '5': self.menu_hapus_tiket,
            '6': self.menu_urutkan_tiket, # Renamed method
            '7': self.menu_riwayat,
            '8': self.menu_statistik,
            '0': self.keluar
        }

    def bersihkan_layar(self):
        """Membersihkan layar terminal"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def cetak_header(self, judul):
        """Mencetak header menu"""
        self.bersihkan_layar()
        print("=" * 70)
        print(f"{' SISTEM MANAJEMEN TIKET KERETA ':=^70}")
        print("=" * 70)
        print(f"\n>>> {judul}\n")

    def tampilkan_menu_utama(self):
        """Menampilkan menu utama"""
        self.bersihkan_layar()
        print("=" * 70)
        print(f"{' SISTEM MANAJEMEN TIKET KERETA ':=^70}")
        print("=" * 70)
        print("\n MENU UTAMA:")
        print("=" * 70)
        print("  1.Tambah Tiket Baru")
        print("  2.Lihat Semua Tiket")
        print("  3.Cari Tiket")
        print("  4.Perbarui Data Tiket")
        print("  5.Hapus Tiket")
        print("  6.Urutkan Tiket")
        print("  7.Riwayat Aktivitas")
        print("  8.Statistik Tiket Kereta")
        print("  0.Keluar")
        print("=" * 70)

    def jalankan(self):
        """Menjalankan aplikasi"""
        while True:
            self.tampilkan_menu_utama()
            pilihan = input("\nPilih menu (0-8): ").strip()

            if pilihan in self.handler_menu:
                self.handler_menu[pilihan]()
            else:
                print("\n Pilihan tidak valid! Tekan Enter untuk melanjutkan...")
                input()

    def menu_tambah_tiket(self):
        """Menu tambah tiket baru"""
        self.cetak_header("TAMBAH TIKET BARU")

        print("Masukkan data tiket:")
        id_tiket = input("ID Tiket (contoh: TK006): ").strip()

        # Cek ID duplikat
        if self.db.baca_by_id(id_tiket): # Corrected from id_buku
            print("\n ID Tiket sudah ada! Gunakan ID lain.")
            input("\nTekan Enter untuk kembali...")
            return

        nama_penumpang = input("Nama Penumpang: ").strip()
        asal = input("Asal: ").strip()
        tujuan = input("Tujuan: ").strip()
        tanggal_keberangkatan = input("Tanggal Keberangkatan (YYYY-MM-DD): ").strip()
        jam_keberangkatan = input("Jam Keberangkatan (HH:MM): ").strip()
        harga = input("Harga: ").strip()
        status = input("Status (Dipesan/Dibatalkan/Selesai): ").strip()

        if not all([id_tiket, nama_penumpang, asal, tujuan, tanggal_keberangkatan, jam_keberangkatan, harga, status]):
            print("\n Semua field harus diisi!")
            input("\nTekan Enter untuk kembali...")
            return

        try:
            float(harga) # Price can be float
        except ValueError:
            print("\n Harga harus berupa angka!")
            input("\nTekan Enter untuk kembali...")
            return

        data_tiket = {
            "id_tiket": id_tiket,
            "nama_penumpang": nama_penumpang,
            "asal": asal,
            "tujuan": tujuan,
            "tanggal_keberangkatan": tanggal_keberangkatan,
            "jam_keberangkatan": jam_keberangkatan,
            "harga": harga,
            "status": status
        }

        berhasil, pesan = self.db.tambah(data_tiket)
        print(f"\n{'Berhasil' if berhasil else 'Gagal'} {pesan}")
        input("\nTekan Enter untuk kembali...")

    def menu_lihat_tiket(self):
        """Menu melihat semua tiket"""
        self.cetak_header("DAFTAR SEMUA TIKET")

        daftar_tiket = self.db.baca_semua()

        if not daftar_tiket:
            print("Belum ada data tiket.")
        else:
            print(f"Total: {len(daftar_tiket)} tiket\n")
            print("-" * 130)
            print(f"{'ID TIKET':<10} {'Penumpang':<20} {'Asal':<15} {'Tujuan':<15}"
                  f"{'Tanggal':<12} {'Jam':<8} {'Harga':<12} {'Status':<12}")
            print("-" * 130)
            for tiket in daftar_tiket: # Corrected from buku
                print(f"{tiket['id_tiket']:<10} {tiket['nama_penumpang']:<20} {tiket['asal']:<15} "
                      f"{tiket['tujuan']:<15} {tiket['tanggal_keberangkatan']:<12} {tiket['jam_keberangkatan']:<8} {tiket['harga']:<12} {tiket['status']:<12}")
            print("-" * 130)

        input("\nTekan Enter untuk kembali...")

    def menu_cari_tiket(self):
        """Menu mencari tiket"""
        self.cetak_header("CARI TIKET")

        kata_kunci = input("Masukkan kata kunci (ID Tiket/Nama Penumpang/Asal/Tujuan): ").strip()

        if not kata_kunci:
            print("\n Kata kunci tidak boleh kosong!")
            input("\nTekan Enter untuk kembali...")
            return

        hasil = self.db.cari_tiket(kata_kunci)

        if not hasil:
            print(f"\n Tidak ditemukan tiket dengan kata kunci '{kata_kunci}'")
        else:
            print(f"\n Ditemukan {len(hasil)} tiket:\n")
            print("-" * 130)
            print(f"{'ID Tiket':<10} {'Penumpang':<20} {'Asal':<15} {'Tujuan':<15}"
                  f"{'Tanggal':<12} {'Jam':<8} {'Harga':<12} {'Status':<12}")
            print("-" * 130)

            for tiket in hasil:
                print(f"{tiket['id_tiket']:<10} {tiket['nama_penumpang']:<20} {tiket['asal']:<15} "
                      f"{tiket['tujuan']:<15} {tiket['tanggal_keberangkatan']:<12} {tiket['jam_keberangkatan']:<8} {tiket['harga']:<12} {tiket['status']:<12}") # Corrected key

            print("-" * 130)

        input("\nTekan Enter untuk kembali...")

    def menu_perbarui_tiket(self):
        """Menu memperbarui data tiket"""
        self.cetak_header("PERBARUI DATA TIKET")

        id_tiket = input("Masukkan ID Tiket yang akan diperbarui: ").strip()

        tiket = self.db.baca_by_id(id_tiket)
        if not tiket:
            print("\n Tiket tidak ditemukan!")
            input("\nTekan Enter untuk kembali...")
            return

        print(f"\n Data Tiket Saat Ini:")
        print(f"  ID Tiket    : {tiket['id_tiket']}")
        print(f"  Penumpang     : {tiket['nama_penumpang']}")
        print(f"  Asal        : {tiket['asal']}")
        print(f"  Tujuan        : {tiket['tujuan']}")
        print(f"  Tanggal        : {tiket['tanggal_keberangkatan']}")
        print(f"  Jam          : {tiket['jam_keberangkatan']}")
        print(f"  Harga       : {tiket['harga']}")
        print(f"  Status      : {tiket['status']}")

        print("\n Masukkan data baru (kosongkan jika tidak diubah):")
        nama_penumpang  = input(f"Nama Penumpang [{tiket['nama_penumpang']}]: ").strip()
        asal  = input(f"Asal [{tiket['asal']}]: ").strip()
        tujuan  = input(f"Tujuan [{tiket['tujuan']}]: ").strip()
        tanggal_keberangkatan  = input(f"Tanggal Keberangkatan [{tiket['tanggal_keberangkatan']}]: ").strip()
        jam_keberangkatan = input(f"Jam Keberangkatan [{tiket['jam_keberangkatan']}]: ").strip()
        harga = input(f"Harga [{tiket['harga']}]: ").strip()
        status = input(f"Status [{tiket['status']}]: ").strip()

        data_baru = {}
        if nama_penumpang: data_baru['nama_penumpang'] = nama_penumpang
        if asal: data_baru['asal'] = asal
        if tujuan: data_baru['tujuan'] = tujuan # Corrected typo
        if tanggal_keberangkatan: data_baru['tanggal_keberangkatan'] = tanggal_keberangkatan # Corrected assignment
        if jam_keberangkatan: data_baru['jam_keberangkatan'] = jam_keberangkatan # Corrected assignment
        if harga:
            try:
                float(harga)
                data_baru['harga'] = harga
            except ValueError: # Corrected indentation
                print("\nHarga tiket harus berupa angka!")
                input("\nTekan Enter untuk kembali...")
                return
        if status: data_baru['status'] = status # Added status update

        if not data_baru:
            print("\n Tidak ada perubahan data.")
            input("\nTekan Enter untuk kembali...")
            return

        berhasil, pesan = self.db.perbarui(id_tiket, data_baru)
        print(f"\n{'Berhasil' if berhasil else 'Gagal'} {pesan}") # Corrected 'Benar'/'Tidak'
        input("\nTekan Enter untuk kembali...")

    def menu_hapus_tiket(self):
        """Menu menghapus tiket"""
        self.cetak_header("HAPUS TIKET")

        id_tiket = input("Masukkan ID Tiket yang akan dihapus: ").strip()

        tiket = self.db.baca_by_id(id_tiket) # Corrected from id_buku
        if not tiket:
            print("\n Tiket tidak ditemukan!")
            input("\nTekan Enter untuk kembali...")
            return

        print(f"\n Data Tiket yang akan dihapus:")
        print(f"  ID Tiket     : {tiket['id_tiket']}")
        print(f"  Penumpang    : {tiket['nama_penumpang']}") # Corrected typo 'nama_penumpangd'
        print(f"  Asal       : {tiket['asal']}")
        print(f"  Tujuan        : {tiket['tujuan']}") # Corrected capitalization 'Tujuan'
        print(f"  Tanggal    : {tiket['tanggal_keberangkatan']}")
        print(f"  Jam        : {tiket['jam_keberangkatan']}")
        print(f"  Harga      : {tiket['harga']}")
        print(f"  Status     : {tiket['status']}")

        konfirmasi = input(f"\n Yakin ingin menghapus tiket '{tiket['id_tiket']} - {tiket['nama_penumpang']}'? (y/n): ").strip().lower()

        if konfirmasi == 'y':
            berhasil, pesan = self.db.hapus(id_tiket)
            print(f"\n{'Berhasil' if berhasil else 'Gagal'} {pesan}") # Corrected 'Benar'/'Tidak'
        else:
            print("\nPenghapusan dibatalkan.")

        input("\nTekan Enter untuk kembali...")

    def menu_urutkan_tiket(self): # Renamed method
        """Menu mengurutkan tiket"""
        self.cetak_header("URUTKAN TIKET")

        print("Pilih field untuk diurutkan:")
        print("  1. ID Tiket")
        print("  2. Nama Penumpang")
        print("  3. Asal")
        print("  4. Tujuan")
        print("  5. Tanggal Keberangkatan")
        print("  6. Jam Keberangkatan")
        print("  7. Harga")
        print("  8. Status")

        pilihan_field = input("\nPilih (1-8): ").strip()

        field_map = {
            '1': 'id_tiket',
            '2': 'nama_penumpang',
            '3': 'asal',
            '4': 'tujuan',
            '5': 'tanggal_keberangkatan',
            '6': 'jam_keberangkatan',
            '7': 'harga',
            '8': 'status'
        }

        if pilihan_field not in field_map:
            print("\n Pilihan tidak valid!")
            input("\nTekan Enter untuk kembali...")
            return

        urutan = input("Urutan (a=ascending/menaik, d=descending/menurun): ").strip().lower()
        terbalik = urutan == 'd'

        tiket_terurut = self.db.urutkan_tiket(field_map[pilihan_field], terbalik) # Corrected method name and variable name

        self.cetak_header(f"HASIL URUTAN ({'Menurun' if terbalik else 'Menaik'})")

        if not tiket_terurut:
            print("\ud83d\udcda Tidak ada data tiket.")
        else:
            print("-" * 130)
            print(f"{'ID Tiket':<10} {'Penumpang':<20} {'Asal':<15} {'Tujuan':<15} {'Tanggal':<12} {'Jam':<8} {'Harga':<12} {'Status':<12}")
            print("-" * 130)
            for tiket in tiket_terurut: # Corrected from buku
                print(f"{tiket['id_tiket']:<10} {tiket['nama_penumpang']:<20} {tiket['asal']:<15} "
                      f"{tiket['tujuan']:<15}  {tiket['tanggal_keberangkatan']:<12} {tiket['jam_keberangkatan']:<8} {tiket['harga']:<12} {tiket['status']:<12}")
            print("-" * 130)

        input("\nTekan Enter untuk kembali...")

    def menu_riwayat(self):
        """Menu melihat riwayat aktivitas"""
        self.cetak_header("RIWAYAT AKTIVITAS")

        riwayat = self.db.ambil_riwayat()

        if not riwayat:
            print("Belum ada riwayat aktivitas.")
        else:
            print(f"Total: {len(riwayat)} aktivitas\n")
            print("-" * 70)
            for i, catatan in enumerate(riwayat, 1):
                print(f"{i:3}. {catatan}")
            print("-" * 70)

        input("\nTekan Enter untuk kembali...")

    def menu_statistik(self):
        """Menu menampilkan statistik"""
        self.cetak_header("STATISTIK TIKET KERETA")

        statistik = self.db.ambil_statistik()

        print("DATA TIKET KERETA")
        print("=" * 50)
        print(f"Total Tiket      : {statistik['total_tiket']}")
        print(f"Dipesan          : {statistik['dipesan']}")
        print(f"Dibatalkan       : {statistik['dibatalkan']}")
        print(f"Selesai          : {statistik['selesai']}") # Added 'selesai'
        print("=" * 50)

        if statistik['tujuan']: # Corrected typo 'tujua'
            print("\n STATISTIK TUJUAN:")
            print("-" * 50)
            for tujuan, jumlah in sorted(statistik['tujuan'].items(), key=lambda x: x[1], reverse=True):
                print(f"  {tujuan:<30}: {jumlah} tiket")
            print("-" * 50)

        input("\nTekan Enter untuk kembali...")

    def keluar(self):
        """Keluar dari aplikasi"""
        self.bersihkan_layar()
        print("=" * 70)
        print("Terima kasih telah menggunakan Sistem Manajemen Tiket Kereta!")
        print("=" * 70)
        exit()

# ==================== PROGRAM UTAMA ====================

if __name__ == "__main__":
    aplikasi = Aplikasi_Tiket_Kereta() # Corrected class name
    aplikasi.jalankan()