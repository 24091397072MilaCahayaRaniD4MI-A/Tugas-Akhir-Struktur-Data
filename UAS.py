import heapq
import itertools
import networkx as nx
import matplotlib.pyplot as plt

class PetaJatim:
    def __init__(self):
        self.graf = {}

    def tambah_kota(self, nama_kota):
        if nama_kota not in self.graf:
            self.graf[nama_kota] = {}

    def tambah_jalan(self, kota1, kota2, jarak):
        self.graf[kota1][kota2] = jarak
        self.graf[kota2][kota1] = jarak

# Daftar kota & koordinat (lon, lat) untuk visualisasi
KOTA_JATIM = [
    'Surabaya', 'Malang', 'Batu', 'Kediri', 'Blitar',
    'Jember', 'Banyuwangi', 'Madiun', 'Lamongan', 'Tuban'
]
POSISI_KOTA = {
    'Surabaya': (112.75, -7.25),
    'Malang': (112.63, -7.98),
    'Batu': (112.52, -7.87),
    'Kediri': (112.01, -7.82),
    'Blitar': (112.16, -8.10),
    'Jember': (113.70, -8.17),
    'Banyuwangi': (114.36, -8.22),
    'Madiun': (111.52, -7.62),
    'Lamongan': (112.41, -7.12),
    'Tuban': (111.90, -6.90)
}

# Set jalur antar kota (tuples: kota1, kota2, jarak)
JALAN_JATIM = [
    ('Surabaya', 'Malang', 90), ('Malang', 'Batu', 20), ('Batu', 'Kediri', 60),
    ('Kediri', 'Blitar', 30), ('Blitar', 'Jember', 120), ('Jember', 'Banyuwangi', 100),
    ('Banyuwangi', 'Madiun', 250), ('Madiun', 'Lamongan', 110), ('Lamongan', 'Tuban', 40),
    ('Tuban', 'Surabaya', 110), ('Surabaya', 'Lamongan', 50), ('Surabaya', 'Tuban', 110),
    ('Malang', 'Blitar', 80), ('Malang', 'Jember', 120), ('Batu', 'Blitar', 70),
    ('Batu', 'Jember', 140), ('Kediri', 'Madiun', 90), ('Kediri', 'Lamongan', 120),
    ('Blitar', 'Madiun', 100), ('Jember', 'Madiun', 200), ('Jember', 'Lamongan', 180),
    ('Banyuwangi', 'Lamongan', 220), ('Banyuwangi', 'Tuban', 260), ('Madiun', 'Tuban', 120),
    ('Lamongan', 'Batu', 100), ('Tuban', 'Kediri', 130), ('Surabaya', 'Batu', 100),
    ('Malang', 'Kediri', 70), ('Blitar', 'Banyuwangi', 150), ('Jember', 'Tuban', 210),
    ('Batu', 'Madiun', 130)
]

# Bangun graf
peta = PetaJatim()
for kota in KOTA_JATIM:
    peta.tambah_kota(kota)
for kotaA, kotaB, jarak in JALAN_JATIM:
    peta.tambah_jalan(kotaA, kotaB, jarak)

# --- Algoritma Dijkstra ---
def rute_terpendek(graf, asal, tujuan):
    prioritas = [(0, asal, [])]
    sudah_dikunjungi = set()
    while prioritas:
        biaya, simpul, jalur = heapq.heappop(prioritas)
        if simpul in sudah_dikunjungi:
            continue
        jalur = jalur + [simpul]
        sudah_dikunjungi.add(simpul)
        if simpul == tujuan:
            return biaya, jalur
        for tetangga, jarak in graf[simpul].items():
            if tetangga not in sudah_dikunjungi:
                heapq.heappush(prioritas, (biaya + jarak, tetangga, jalur))
    return float("inf"), []

# --- Algoritma TSP brute force (tanpa kembali ke asal) ---
def salesman_jawa_timur(graf, start):
    kota_lain = [k for k in graf.keys() if k != start]
    rute_optimal = None
    biaya_optimal = float("inf")
    for urutan in itertools.permutations(kota_lain):
        total = 0
        pos = start
        valid = True
        for tujuan in urutan:
            if tujuan in graf[pos]:
                total += graf[pos][tujuan]
                pos = tujuan
            else:
                valid = False
                break
        if valid and total < biaya_optimal:
            biaya_optimal = total
            rute_optimal = (start,) + urutan
    return biaya_optimal, rute_optimal if rute_optimal else (float("inf"), [])

# --- Visualisasi graph Jatim ---
def gambarkan_jatim(graf):
    grafnx = nx.Graph()
    for k1, tetangga in graf.items():
        for k2, jarak in tetangga.items():
            if not grafnx.has_edge(k1, k2):
                grafnx.add_edge(k1, k2, weight=jarak)
    plt.figure(figsize=(12, 8))
    nx.draw(
        grafnx, POSISI_KOTA, with_labels=True, node_color="#ffe599",
        node_size=1400, font_size=10, font_weight='bold', edge_color='#8e7cc3'
    )
    label_edge = nx.get_edge_attributes(grafnx, 'weight')
    nx.draw_networkx_edge_labels(grafnx, POSISI_KOTA, edge_labels=label_edge, font_size=7)
    plt.title("Visualisasi Jaringan Jalan Jawa Timur", fontsize=14)
    plt.axis('off')
    plt.show()

# ================== Menu Sederhana ==================
print("\n=== PENELUSURAN JARINGAN JAWA TIMUR ===")
print("Daftar kota:")
for k in KOTA_JATIM:
    print("•", k)

kota_asal = input("\nMasukkan kota berangkat: ").title()
kota_tujuan = input("Masukkan kota tujuan: ").title()

if kota_asal not in KOTA_JATIM or kota_tujuan not in KOTA_JATIM:
    print("Kota tidak terdaftar pada pilihan Jawa Timur.")
else:
    print("\n-- KONEKSI TIAP KOTA --")
    for k, t in peta.graf.items():
        sambungan = ", ".join(f"{kk} ({jj} km)" for kk, jj in t.items())
        print(f"{k} => {sambungan}")

    # Dijkstra
    dist, lintasan = rute_terpendek(peta.graf, kota_asal, kota_tujuan)
    print(f"\n=== Dijkstra: {kota_asal} → {kota_tujuan} ===")
    print(f"Lintasan tercepat: {' → '.join(lintasan)}")
    print(f"Jarak total: {dist} km, Estimasi waktu: {round(dist/60,2)} jam (rata-rata 60 km/jam)")

    # TSP (tanpa kembali ke asal)
    print("\n=== TSP TANPA BALIK KE ASAL ===\n(urutan perjalanan keliling seluruh kota dari kota asal)")
    print("Perhitungan bisa cukup lama, harap tunggu ...")
    total_tsp, path_tsp = salesman_jawa_timur(peta.graf, kota_asal)
    print("Lintasan optimal:", " → ".join(path_tsp))
    print(f"Jarak keliling: {total_tsp} km, Perkiraan waktu: {round(total_tsp/60,2)} jam")

    # Gambar graf dengan NetworkX
    gambarkan_jatim(peta.graf)