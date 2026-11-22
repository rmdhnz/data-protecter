# Data Protecter

Enkripsi dan dekripsi file atau isi folder menggunakan password. Untuk menjalankan dari source diperlukan Python 3.13 dan `uv`.

## Instalasi executable Linux

Setelah installer dan release dipublikasikan di GitHub, jalankan:

```bash
curl -fsSL https://raw.githubusercontent.com/rmdhnz/data-protecter/master/install.sh | sh
```

Installer mendukung Linux x86_64 dan ARM64, serta memasang ke `/usr/local/bin` (meminta `sudo` bila diperlukan). Lihat [panduan instalasi executable Linux](docs/instalasi-linux.md) untuk konfigurasi, direktori alternatif, dan langkah membuat release.

## Penggunaan

Periksa versi yang terpasang dengan `data-protecter --version` atau `data-protecter -v`. Executable dari GitHub Release menampilkan tag release, misalnya `v.1.1.0`. Saat dijalankan dari source, versi mengikuti `pyproject.toml`.

```bash
uv run data-protecter encrypt -f /flashdisk/data.zip -p 'Pass123' -o /flashdisk/backup_aman.dat
uv run data-protecter decrypt -f /flashdisk/backup_aman.dat -p 'Pass123' -o /flashdisk/data.zip
uv run data-protecter encrypt -f /path/ke/folder
uv run data-protecter decrypt -f /path/ke/folder -o /path/ke/folder-hasil
```

Pilih operasi `encrypt` atau `decrypt`. Jika `-f` atau `-p` tidak diberikan, program akan memintanya secara interaktif; password yang diketik secara interaktif tidak ditampilkan. Password pada argumen `-p` dapat terlihat dalam riwayat shell atau daftar proses; gunakan prompt interaktif jika ingin menghindarinya.

`-o` opsional. Untuk file, `-o` menentukan nama lengkap file hasil; tanpa `-o`, hasil disimpan di direktori yang sama dengan tambahan `.enc` saat enkripsi atau tanpa `.enc` saat dekripsi. Untuk dekripsi file tanpa ekstensi `.enc`, gunakan `-o`. Untuk folder, `-o` menentukan folder tujuan dengan struktur subfolder yang sama; tanpa `-o`, hasil disimpan di samping setiap file asal.

Untuk folder, file diproses secara rekursif; enkripsi melewati file `.enc` dan dekripsi hanya memproses file `.enc`. Program tidak menghapus file asal dan tidak menimpa file yang sudah ada. Jika salah satu file gagal diproses, program melanjutkan file lainnya dan mengembalikan status gagal. Pemrosesan membaca seluruh isi file ke memori.

## Password

Gunakan password yang kuat dan simpan dengan aman. Setiap file dapat dienkripsi dengan password yang berbeda; gunakan password yang sama saat mendekripsi file tersebut. Program tidak memerlukan `.env`. File yang dibuat oleh versi sebelumnya tetap dapat didekripsi dengan password yang digunakan saat enkripsi.
