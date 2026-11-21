#!/bin/sh
set -eu

repo='rmdhnz/data-protecter'
install_dir=${INSTALL_DIR:-/usr/local/bin}

if [ "$(uname -s)" != Linux ]; then
    echo 'Error: installer ini hanya mendukung Linux.' >&2
    exit 1
fi
case "$(uname -m)" in
    x86_64|amd64) arch=x86_64 ;;
    aarch64|arm64) arch=aarch64 ;;
    *) echo "Error: arsitektur tidak didukung: $(uname -m)" >&2; exit 1 ;;
esac
for cmd in curl sha256sum mktemp install; do
    command -v "$cmd" >/dev/null 2>&1 || { echo "Error: $cmd diperlukan." >&2; exit 1; }
done

tmp_dir=$(mktemp -d)
trap 'rm -rf "$tmp_dir"' EXIT HUP INT TERM
asset="data-protecter-linux-$arch"
base_url="https://github.com/$repo/releases/latest/download"
echo "Mengunduh $asset dari release terbaru..."
curl -fsSL "$base_url/$asset" -o "$tmp_dir/$asset"
curl -fsSL "$base_url/$asset.sha256" -o "$tmp_dir/$asset.sha256"
(cd "$tmp_dir" && sha256sum -c "$asset.sha256")

if [ -d "$install_dir" ] && [ -w "$install_dir" ]; then
    install -m 755 "$tmp_dir/$asset" "$install_dir/data-protecter"
else
    command -v sudo >/dev/null 2>&1 || { echo "Error: tidak dapat menulis ke $install_dir dan sudo tidak tersedia. Gunakan INSTALL_DIR untuk memilih direktori lain." >&2; exit 1; }
    echo "Memerlukan sudo untuk memasang ke $install_dir."
    sudo install -d "$install_dir" </dev/tty
    sudo install -m 755 "$tmp_dir/$asset" "$install_dir/data-protecter" </dev/tty
fi
echo "Terpasang: $install_dir/data-protecter"
case ":$PATH:" in
    *":$install_dir:"*) ;;
    *) echo "Tambahkan $install_dir ke PATH agar perintah dapat dijalankan langsung." ;;
esac
