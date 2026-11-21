# Data Protecter

Enkripsi dan dekripsi file atau isi folder menggunakan password. Python 3.13 dan `uv` diperlukan.

## Penggunaan

```bash
uv run data-protecter encrypt -f /flashdisk/data.zip -p 'Pass123' -o /flashdisk/backup_aman.dat
uv run data-protecter decrypt -f /flashdisk/backup_aman.dat -p 'Pass123' -o /flashdisk/data.zip
uv run data-protecter encrypt -f /path/ke/folder
uv run data-protecter decrypt -f /path/ke/folder -o /path/ke/folder-hasil
```

Pilih operasi `encrypt` atau `decrypt`. Jika `-f` atau `-p` tidak diberikan, program akan memintanya secara interaktif; password yang diketik secara interaktif tidak ditampilkan. Password pada argumen `-p` dapat terlihat dalam riwayat shell atau daftar proses; gunakan prompt interaktif jika ingin menghindarinya.

`-o` opsional. Untuk file, `-o` menentukan nama lengkap file hasil; tanpa `-o`, hasil disimpan di direktori yang sama dengan tambahan `.enc` saat enkripsi atau tanpa `.enc` saat dekripsi. Untuk dekripsi file tanpa ekstensi `.enc`, gunakan `-o`. Untuk folder, `-o` menentukan folder tujuan dengan struktur subfolder yang sama; tanpa `-o`, hasil disimpan di samping setiap file asal.

Untuk folder, file diproses secara rekursif; enkripsi melewati file `.enc` dan dekripsi hanya memproses file `.enc`. Program tidak menghapus file asal dan tidak menimpa file yang sudah ada. Jika salah satu file gagal diproses, program melanjutkan file lainnya dan mengembalikan status gagal. Pemrosesan membaca seluruh isi file ke memori.

## Password dari `.env` (opsional)

Salin `.env.example` menjadi `.env`, lalu isi `DATA_PROTECTER_PASSWORD` dengan password yang kuat. Password yang dimasukkan melalui `-p` atau prompt harus sama dengan `DATA_PROTECTER_PASSWORD`; jika tidak cocok, proses dibatalkan. Konfigurasi password wajib tersedia sebelum program dijalankan. Variabel environment yang sudah ada memiliki prioritas di atas `.env`. Simpan password dengan aman; file tidak dapat didekripsi tanpa password yang sama. Jangan menyimpan `.env` bersama file terenkripsi di drive atau flashdisk.
