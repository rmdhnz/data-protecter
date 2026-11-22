# Membuat dan memasang executable di Linux

Panduan ini membuat executable Linux dan memasangnya ke `/usr/local/bin`, sehingga perintah `data-protecter` dapat dijalankan dari terminal tanpa menuliskan lokasi executable. Pembuatan dilakukan di Linux dengan arsitektur yang sesuai dengan komputer tujuan. Komputer yang menjalankan hasilnya tidak perlu memasang Python atau `uv`.

## Instalasi dari GitHub

Setelah `install.sh` tersedia di branch `master` dan release yang berisi executable selesai dibuat, jalankan:

```bash
curl -fsSL https://raw.githubusercontent.com/rmdhnz/data-protecter/master/install.sh | sh
```

Installer mengunduh binary dan checksum SHA-256 dari release terbaru, memeriksa checksum, lalu memasangnya ke `/usr/local/bin/data-protecter`. Installer meminta `sudo` melalui terminal jika diperlukan. Checksum mendeteksi kerusakan unduhan, tetapi bukan tanda tangan independen untuk membuktikan keaslian release. Diperlukan Linux x86_64 atau ARM64, `curl`, `sha256sum`, `mktemp`, dan `install`. Build ARM64 menggunakan Ubuntu 24.04 dan mungkin tidak berjalan pada distribusi Linux yang lebih lama.

Untuk menghindari `sudo`, buat direktori pengguna dan teruskan `INSTALL_DIR` ke `sh` (pastikan direktori tersebut ada di `PATH`):

```bash
mkdir -p "$HOME/.local/bin"
curl -fsSL https://raw.githubusercontent.com/rmdhnz/data-protecter/master/install.sh | INSTALL_DIR="$HOME/.local/bin" sh
```

Untuk melihat isi installer sebelum menjalankan:

```bash
curl -fsSL https://raw.githubusercontent.com/rmdhnz/data-protecter/master/install.sh -o install.sh
less install.sh
sh install.sh
```

## Membuat release

Push perubahan ke GitHub, kemudian publikasikan release dari tag yang berisi workflow `.github/workflows/release.yml`. GitHub Actions akan membuat binary dan checksum untuk masing-masing arsitektur dan mengunggahnya ke release. Tunggu kedua job berhasil sebelum memakai installer. Repository dan release harus dapat diakses oleh pengguna yang akan mengunduhnya.

## Membuat dan memasang secara manual

### 1. Buat executable

Pada komputer pembuat, siapkan Python 3.13 atau lebih baru, `uv`, dan source code proyek ini. Jalankan dari direktori utama proyek:

```bash
uv run --with pyinstaller pyinstaller --onefile --name data-protecter app.py
```

Perintah ini menyediakan PyInstaller saat build dan membuat executable di `dist/data-protecter`. File `app.py` sudah tersedia sebagai titik masuk program. Build tidak menyertakan `.env`.

### 2. Pasang ke /usr/local/bin

Dari direktori utama proyek, jalankan:

```bash
sudo install -m 755 dist/data-protecter /usr/local/bin/data-protecter
```

Perintah tersebut menyalin executable dan menetapkan izin agar dapat dijalankan. `sudo` diperlukan jika pengguna tidak memiliki izin menulis ke `/usr/local/bin`. Untuk memperbarui program setelah build ulang, jalankan perintah instalasi yang sama; executable lama akan diganti.

Pastikan `/usr/local/bin` tercantum dalam `PATH`, lalu periksa:

```bash
command -v data-protecter
data-protecter --help
```

Jika belum ada dalam `PATH`, tambahkan baris berikut ke konfigurasi shell, misalnya `~/.zshrc` atau `~/.bashrc`, lalu buka terminal baru:

```bash
export PATH="/usr/local/bin:$PATH"
```

## Gunakan program

Pilih password yang kuat untuk setiap enkripsi dan gunakan password yang sama saat mendekripsi. Program akan meminta password secara interaktif; `.env` tidak diperlukan. Simpan password dengan aman dan kirimkan kepada penerima melalui saluran terpisah.

```bash
data-protecter encrypt -f /flashdisk/data.zip -o /flashdisk/backup_aman.dat
data-protecter decrypt -f /flashdisk/backup_aman.dat -o /flashdisk/data-hasil.zip
```

Pastikan hasil dekripsi dapat dibuka sebelum memindahkan atau menghapus file asli. Program tidak menimpa file yang sudah ada.

## Memasang build manual di komputer lain

Salin `dist/data-protecter` ke komputer Linux tujuan, kemudian jalankan `sudo install -m 755 ./data-protecter /usr/local/bin/data-protecter` dari direktori tempat executable disalin. Penerima perlu menyiapkan password dan menguji executable di komputernya. Build Linux tidak menghasilkan executable Windows; build untuk Windows harus dibuat di Windows.

## Menghapus instalasi

```bash
sudo rm /usr/local/bin/data-protecter
```

Perintah ini hanya menghapus executable terpasang; file terenkripsi tetap ada.
