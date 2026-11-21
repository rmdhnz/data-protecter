"""Pengaturan aplikasi yang dibaca dari environment atau berkas .env."""

import os

from dotenv import load_dotenv


def get_password() -> str:
    load_dotenv()
    password = os.getenv("DATA_PROTECTER_PASSWORD")
    if not password:
        raise ValueError("DATA_PROTECTER_PASSWORD belum diatur di environment atau .env")
    return password
