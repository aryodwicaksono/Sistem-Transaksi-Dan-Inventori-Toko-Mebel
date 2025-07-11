import csv
import os
from datetime import datetime
from collections import deque
import json

class Node:
    """Node untuk implementasi Linked List"""
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    """Implementasi Linked List untuk menyimpan data produk"""
    def __init__(self):
        self.head = None
        self.size = 0
    
    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        self.size += 1
    
    def search(self, kode_produk):
        current = self.head
        while current:
            if current.data['kode_produk'] == kode_produk:
                return current.data
            current = current.next
        return None
    
    def update(self, kode_produk, new_data):
        current = self.head
        while current:
            if current.data['kode_produk'] == kode_produk:
                current.data.update(new_data)
                return True
            current = current.next
        return False
    
    def delete(self, kode_produk):
        if not self.head:
            return False
        
        if self.head.data['kode_produk'] == kode_produk:
            self.head = self.head.next
            self.size -= 1
            return True
        
        current = self.head
        while current.next:
            if current.next.data['kode_produk'] == kode_produk:
                current.next = current.next.next
                self.size -= 1
                return True
            current = current.next
        return False
    
    def get_all(self):
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result

class TransactionQueue:
    """Implementasi Queue untuk mengelola antrian transaksi"""
    def __init__(self):
        self.queue = deque()
    
    def enqueue(self, transaction):
        self.queue.append(transaction)
    
    def dequeue(self):
        if self.queue:
            return self.queue.popleft()
        return None
    
    def is_empty(self):
        return len(self.queue) == 0
    
    def get_all(self):
        return list(self.queue)

class CategoryHashMap:
    """Implementasi HashMap untuk kategori produk"""
    def __init__(self, size=10):
        self.size = size
        self.buckets = [[] for _ in range(size)]
    
    def _hash(self, key):
        return hash(key) % self.size
    
    def put(self, key, value):
        index = self._hash(key)
        bucket = self.buckets[index]
        
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        
        bucket.append((key, value))
    
    def get(self, key):
        index = self._hash(key)
        bucket = self.buckets[index]
        
        for k, v in bucket:
            if k == key:
                return v
        return None
    
    def get_all_categories(self):
        categories = []
        for bucket in self.buckets:
            for key, value in bucket:
                categories.append(key)
        return categories

class FurnitureStore:
    """Sistem utama untuk toko mebel"""
    def __init__(self):
        self.products = LinkedList()
        self.transaction_queue = TransactionQueue()
        self.categories = CategoryHashMap()
        self.csv_file = 'furniture_inventory.csv'
        self.transaction_file = 'transactions.csv'
        self.initialize_categories()
        self.load_data()
    
    def initialize_categories(self):
        """Inisialisasi kategori produk"""
        categories = {
            'SOFA': 'Sofa dan Kursi',
            'MEJA': 'Meja dan Kursi Makan',
            'LEMARI': 'Lemari dan Penyimpanan',
            'TEMPAT_TIDUR': 'Tempat Tidur dan Kasur',
            'DEKORASI': 'Dekorasi dan Aksesoris'
        }
        
        for key, value in categories.items():
            self.categories.put(key, value)
    
    def load_data(self):
        """Memuat data dari file CSV"""
        if os.path.exists(self.csv_file):
            try:
                with open(self.csv_file, 'r', newline='', encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        row['harga'] = float(row['harga'])
                        row['stok'] = int(row['stok'])
                        self.products.append(row)
                print(f"Data berhasil dimuat dari {self.csv_file}")
            except Exception as e:
                print(f"Error loading data: {e}")
        else:
            self.create_sample_data()
    
    def create_sample_data(self):
        """Membuat data contoh jika file tidak ada"""
        sample_products = [
            {'kode_produk': 'SF001', 'nama': 'Sofa Minimalis 3 Seater', 'kategori': 'SOFA', 'harga': 3500000, 'stok': 5},
            {'kode_produk': 'MJ001', 'nama': 'Meja Makan Kayu Jati', 'kategori': 'MEJA', 'harga': 2500000, 'stok': 3},
            {'kode_produk': 'LM001', 'nama': 'Lemari Pakaian 3 Pintu', 'kategori': 'LEMARI', 'harga': 4000000, 'stok': 2},
            {'kode_produk': 'TT001', 'nama': 'Tempat Tidur King Size', 'kategori': 'TEMPAT_TIDUR', 'harga': 5000000, 'stok': 4},
            {'kode_produk': 'DK001', 'nama': 'Vas Bunga Keramik', 'kategori': 'DEKORASI', 'harga': 250000, 'stok': 10}
        ]
        
        for product in sample_products:
            self.products.append(product)
        
        self.save_data()
    
    def save_data(self):
        """Menyimpan data ke file CSV"""
        try:
            with open(self.csv_file, 'w', newline='', encoding='utf-8') as file:
                fieldnames = ['kode_produk', 'nama', 'kategori', 'harga', 'stok']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                
                products = self.products.get_all()
                for product in products:
                    writer.writerow(product)
            print("Data berhasil disimpan ke CSV")
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def save_transaction(self, transaction):
        """Menyimpan transaksi ke file CSV"""
        try:
            file_exists = os.path.exists(self.transaction_file)
            with open(self.transaction_file, 'a', newline='', encoding='utf-8') as file:
                fieldnames = ['id_transaksi', 'tanggal', 'kode_produk', 'nama_produk', 'jumlah', 'harga_satuan', 'total']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                
                if not file_exists:
                    writer.writeheader()
                
                writer.writerow(transaction)
        except Exception as e:
            print(f"Error saving transaction: {e}")
    
    def add_product(self):
        """Menambah produk baru"""
        print("\n=== TAMBAH PRODUK BARU ===")
        kode_produk = input("Kode Produk: ").upper()
        
        # Cek apakah kode sudah ada
        if self.products.search(kode_produk):
            print("Kode produk sudah ada!")
            return
        
        nama = input("Nama Produk: ")
        
        # Tampilkan kategori yang tersedia
        print("\nKategori yang tersedia:")
        categories = self.categories.get_all_categories()
        for i, cat in enumerate(categories, 1):
            print(f"{i}. {cat} - {self.categories.get(cat)}")
        
        try:
            cat_choice = int(input("Pilih kategori (nomor): ")) - 1
            if 0 <= cat_choice < len(categories):
                kategori = categories[cat_choice]
            else:
                print("Pilihan tidak valid!")
                return
        except ValueError:
            print("Input tidak valid!")
            return
        
        try:
            harga = float(input("Harga: "))
            stok = int(input("Stok: "))
        except ValueError:
            print("Input harga atau stok tidak valid!")
            return
        
        new_product = {
            'kode_produk': kode_produk,
            'nama': nama,
            'kategori': kategori,
            'harga': harga,
            'stok': stok
        }
        
        self.products.append(new_product)
        self.save_data()
        print("Produk berhasil ditambahkan!")
    
    def view_products(self):
        """Menampilkan semua produk"""
        print("\n=== DAFTAR PRODUK ===")
        products = self.products.get_all()
        
        if not products:
            print("Tidak ada produk dalam inventori.")
            return
        
        print(f"{'Kode':<8} {'Nama':<30} {'Kategori':<15} {'Harga':<12} {'Stok':<5}")
        print("-" * 75)
        
        for product in products:
            category_name = self.categories.get(product['kategori'])
            print(f"{product['kode_produk']:<8} {product['nama']:<30} {category_name:<15} {product['harga']:<12,.0f} {product['stok']:<5}")
    
    def search_product(self):
        """Mencari produk berdasarkan kode"""
        print("\n=== CARI PRODUK ===")
        kode = input("Masukkan kode produk: ").upper()
        
        product = self.products.search(kode)
        if product:
            print(f"\nProduk ditemukan:")
            print(f"Kode: {product['kode_produk']}")
            print(f"Nama: {product['nama']}")
            print(f"Kategori: {self.categories.get(product['kategori'])}")
            print(f"Harga: Rp {product['harga']:,.0f}")
            print(f"Stok: {product['stok']}")
        else:
            print("Produk tidak ditemukan!")
    
    def update_product(self):
        """Mengupdate informasi produk"""
        print("\n=== UPDATE PRODUK ===")
        kode = input("Masukkan kode produk: ").upper()
        
        product = self.products.search(kode)
        if not product:
            print("Produk tidak ditemukan!")
            return
        
        print(f"Produk saat ini: {product['nama']}")
        print("Kosongkan field yang tidak ingin diubah")
        
        nama = input(f"Nama baru ({product['nama']}): ").strip()
        harga_str = input(f"Harga baru ({product['harga']:,.0f}): ").strip()
        stok_str = input(f"Stok baru ({product['stok']}): ").strip()
        
        update_data = {}
        if nama:
            update_data['nama'] = nama
        if harga_str:
            try:
                update_data['harga'] = float(harga_str)
            except ValueError:
                print("Harga tidak valid!")
                return
        if stok_str:
            try:
                update_data['stok'] = int(stok_str)
            except ValueError:
                print("Stok tidak valid!")
                return
        
        if update_data:
            self.products.update(kode, update_data)
            self.save_data()
            print("Produk berhasil diupdate!")
        else:
            print("Tidak ada perubahan.")
    
    def delete_product(self):
        """Menghapus produk"""
        print("\n=== HAPUS PRODUK ===")
        kode = input("Masukkan kode produk: ").upper()
        
        product = self.products.search(kode)
        if not product:
            print("Produk tidak ditemukan!")
            return
        
        print(f"Produk: {product['nama']}")
        confirm = input("Yakin ingin menghapus? (y/n): ").lower()
        
        if confirm == 'y':
            if self.products.delete(kode):
                self.save_data()
                print("Produk berhasil dihapus!")
            else:
                print("Gagal menghapus produk!")
        else:
            print("Penghapusan dibatalkan.")
    
    def process_transaction(self):
        """Memproses transaksi penjualan"""
        print("\n=== TRANSAKSI PENJUALAN ===")
        kode = input("Masukkan kode produk: ").upper()
        
        product = self.products.search(kode)
        if not product:
            print("Produk tidak ditemukan!")
            return
        
        print(f"Produk: {product['nama']}")
        print(f"Harga: Rp {product['harga']:,.0f}")
        print(f"Stok tersedia: {product['stok']}")
        
        try:
            jumlah = int(input("Jumlah pembelian: "))
            if jumlah <= 0:
                print("Jumlah harus lebih dari 0!")
                return
            
            if jumlah > product['stok']:
                print("Stok tidak mencukupi!")
                return
        except ValueError:
            print("Input tidak valid!")
            return
        
        total = product['harga'] * jumlah
        
        # Buat transaksi
        transaction = {
            'id_transaksi': f"TRX{datetime.now().strftime('%Y%m%d%H%M%S')}",
            'tanggal': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'kode_produk': product['kode_produk'],
            'nama_produk': product['nama'],
            'jumlah': jumlah,
            'harga_satuan': product['harga'],
            'total': total
        }
        
        print(f"\n=== DETAIL TRANSAKSI ===")
        print(f"ID Transaksi: {transaction['id_transaksi']}")
        print(f"Produk: {transaction['nama_produk']}")
        print(f"Jumlah: {jumlah}")
        print(f"Harga Satuan: Rp {product['harga']:,.0f}")
        print(f"Total: Rp {total:,.0f}")
        
        confirm = input("\nKonfirmasi transaksi? (y/n): ").lower()
        if confirm == 'y':
            # Update stok
            new_stock = product['stok'] - jumlah
            self.products.update(kode, {'stok': new_stock})
            
            # Simpan transaksi
            self.transaction_queue.enqueue(transaction)
            self.save_transaction(transaction)
            self.save_data()
            
            print("Transaksi berhasil!")
        else:
            print("Transaksi dibatalkan.")
    
    def view_transactions(self):
        """Menampilkan riwayat transaksi"""
        print("\n=== RIWAYAT TRANSAKSI ===")
        
        if not os.path.exists(self.transaction_file):
            print("Belum ada transaksi.")
            return
        
        try:
            with open(self.transaction_file, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                transactions = list(reader)
                
                if not transactions:
                    print("Belum ada transaksi.")
                    return
                
                print(f"{'ID Transaksi':<20} {'Tanggal':<20} {'Produk':<25} {'Jumlah':<8} {'Total':<12}")
                print("-" * 90)
                
                total_revenue = 0
                for transaction in transactions:
                    total = float(transaction['total'])
                    total_revenue += total
                    print(f"{transaction['id_transaksi']:<20} {transaction['tanggal']:<20} {transaction['nama_produk']:<25} {transaction['jumlah']:<8} {total:<12,.0f}")
                
                print("-" * 90)
                print(f"Total Pendapatan: Rp {total_revenue:,.0f}")
                
        except Exception as e:
            print(f"Error reading transactions: {e}")
    
    def generate_report(self):
        """Membuat laporan inventori"""
        print("\n=== LAPORAN INVENTORI ===")
        products = self.products.get_all()
        
        if not products:
            print("Tidak ada produk dalam inventori.")
            return
        
        # Hitung statistik
        total_products = len(products)
        total_value = sum(p['harga'] * p['stok'] for p in products)
        low_stock_products = [p for p in products if p['stok'] < 5]
        
        print(f"Total Produk: {total_products}")
        print(f"Total Nilai Inventori: Rp {total_value:,.0f}")
        print(f"Produk Stok Rendah (< 5): {len(low_stock_products)}")
        
        if low_stock_products:
            print("\nProduk dengan stok rendah:")
            for product in low_stock_products:
                print(f"- {product['nama']}: {product['stok']} unit")
        
        # Laporan per kategori
        print("\n=== LAPORAN PER KATEGORI ===")
        category_stats = {}
        for product in products:
            cat = product['kategori']
            if cat not in category_stats:
                category_stats[cat] = {'count': 0, 'value': 0}
            category_stats[cat]['count'] += product['stok']
            category_stats[cat]['value'] += product['harga'] * product['stok']
        
        for cat, stats in category_stats.items():
            cat_name = self.categories.get(cat)
            print(f"{cat_name}: {stats['count']} unit, Nilai: Rp {stats['value']:,.0f}")
    
    def main_menu(self):
        """Menu utama aplikasi"""
        while True:
            print("\n" + "="*50)
            print("    SISTEM INVENTORI TOKO MEBEL")
            print("="*50)
            print("1. Tambah Produk")
            print("2. Lihat Semua Produk")
            print("3. Cari Produk")
            print("4. Update Produk")
            print("5. Hapus Produk")
            print("6. Proses Transaksi")
            print("7. Riwayat Transaksi")
            print("8. Laporan Inventori")
            print("0. Keluar")
            print("="*50)
            
            choice = input("Pilih menu (0-8): ").strip()
            
            if choice == '1':
                self.add_product()
            elif choice == '2':
                self.view_products()
            elif choice == '3':
                self.search_product()
            elif choice == '4':
                self.update_product()
            elif choice == '5':
                self.delete_product()
            elif choice == '6':
                self.process_transaction()
            elif choice == '7':
                self.view_transactions()
            elif choice == '8':
                self.generate_report()
            elif choice == '0':
                print("Terima kasih telah menggunakan sistem inventori!")
                break
            else:
                print("Pilihan tidak valid!")
            
            input("\nTekan Enter untuk melanjutkan...")

# Jalankan aplikasi
if __name__ == "__main__":
    store = FurnitureStore()
    store.main_menu()