import argparse
import base64
import getpass
import os
from pathlib import Path
from importlib.metadata import version

from ._release_version import RELEASE_VERSION

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def derive_key(password: str, salt: bytes) -> bytes:
    """Mengubah password menjadi kunci Fernet."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(), length=32, salt=salt, iterations=600_000
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))


def encrypt_file(file_path: str | Path, password: str, output_file_path: str | Path | None = None) -> None:
    path = Path(file_path)
    salt = os.urandom(16)
    ciphertext = Fernet(derive_key(password, salt)).encrypt(path.read_bytes())
    output = Path(output_file_path) if output_file_path is not None else path.with_name(path.name + ".enc")
    with output.open("xb") as destination:
        destination.write(salt + ciphertext)
    print(f"[OK] File terenkripsi disimpan di: {output}")


def decrypt_file(enc_file_path: str | Path, password: str, output_file_path: str | Path) -> None:
    path = Path(enc_file_path)
    data = path.read_bytes()
    try:
        plaintext = Fernet(derive_key(password, data[:16])).decrypt(data[16:])
    except InvalidToken as exc:
        raise ValueError(f"Dekripsi gagal untuk {path}: password salah atau file rusak") from exc
    output = Path(output_file_path)
    with output.open("xb") as destination:
        destination.write(plaintext)
    print(f"[OK] File berhasil didekripsi ke: {output}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Enkripsi atau dekripsi file dan folder.")
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s {RELEASE_VERSION or version('data-protecter')}")
    parser.add_argument("action", choices=("encrypt", "decrypt"), help="Operasi yang dijalankan")
    parser.add_argument("-f", "--file", type=Path, help="Lokasi file atau folder")
    parser.add_argument("-p", "--password", help="Password enkripsi atau dekripsi")
    parser.add_argument("-o", "--output", type=Path, help="Lokasi file hasil atau folder tujuan (opsional)")
    args = parser.parse_args()

    try:
        path = args.file or Path(input("Lokasi file atau folder: ").strip())
        password = getpass.getpass("Password: ") if args.password is None else args.password
        if not password:
            raise ValueError("Password tidak boleh kosong")
        if path.is_file():
            files = [path]
            is_directory = False
        elif path.is_dir():
            is_directory = True
            files = sorted(item for item in path.rglob("*") if item.is_file() and not item.is_symlink() and ((item.suffix == ".enc") == (args.action == "decrypt")))
        else:
            raise ValueError(f"Lokasi tidak ditemukan: {path}")

        if not files:
            raise ValueError("Tidak ada file yang sesuai untuk diproses")
        failures = 0
        for item in files:
            try:
                if args.action == "decrypt" and item.suffix != ".enc" and (is_directory or args.output is None):
                    raise ValueError(f"Gunakan -o untuk menentukan nama hasil dekripsi file tanpa ekstensi .enc: {item}")
                if is_directory and args.output is not None:
                    relative = item.relative_to(path)
                    output = args.output / (relative.with_name(relative.name + ".enc") if args.action == "encrypt" else relative.with_suffix(""))
                    output.parent.mkdir(parents=True, exist_ok=True)
                elif args.output is not None:
                    output = args.output
                else:
                    output = item.with_name(item.name + ".enc") if args.action == "encrypt" else item.with_suffix("")
                if args.action == "encrypt":
                    encrypt_file(item, password, output)
                else:
                    decrypt_file(item, password, output)
            except (OSError, ValueError) as exc:
                failures += 1
                print(f"[ERROR] {exc}")
        if failures:
            raise SystemExit(1)
    except (OSError, ValueError, EOFError, KeyboardInterrupt) as exc:
        parser.exit(1, f"[ERROR] {exc or 'Input dibatalkan'}\n")


if __name__ == "__main__":
    main()
