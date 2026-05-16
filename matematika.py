import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import re

st.set_page_config(page_title="Security Auto-System", layout="wide")

# --- DATABASE VIRTUAL ---
if 'db_user' not in st.session_state:
    st.session_state.db_user = None
if 'db_pass' not in st.session_state:
    st.session_state.db_pass = None
if 'percobaan' not in st.session_state:
    st.session_state.percobaan = 0

st.title("🛡️ Security Auto-System + Retas Estimator")
st.write("Sistem Registrasi, Login Otomatis & Prediksi Keamanan Matematis")

# --- BAGIAN 1: BUAT AKUN (REGISTRASI) ---
st.header("1. Registrasi Akun")
with st.expander("Buka untuk buat akun baru"):
    new_user = st.text_input("Buat Username:")
    new_pass = st.text_input("Buat Password:", type="password")
    
    if st.button("Daftar Akun"):
        if new_user and new_pass:
            st.session_state.db_user = new_user
            st.session_state.db_pass = new_pass
            st.success(f"Akun *{new_user}* aktif! Cek analisisnya di bawah.")
        else:
            st.warning("Username dan password tidak boleh kosong!")

# --- BAGIAN 2: ANALISIS KEKUATAN & ESTIMASI WAKTU (OTOMATIS) ---
st.markdown("---")
st.header("2. Analisis Kekuatan & Estimasi Retas")
if st.session_state.db_pass:
    p = st.session_state.db_pass
    r = len(p)
    n = 0
    if re.search(r"[a-z]", p): n += 26
    if re.search(r"[A-Z]", p): n += 26
    if re.search(r"[0-9]", p): n += 10
    if re.search(r"\W", p): n += 32
    
    total_kombinasi = n**r
    # Asumsi kecepatan retas: 1 Miliar percobaan/detik
    detik_retas = total_kombinasi / 1_000_000_000
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Kombinasi ($n^r$)", f"{total_kombinasi:.1e}")
        if r < 8 or n < 30:
            st.error("KEKUATAN: LEMAH 🛑")
        elif r >= 12 and n > 60:
            st.success("KEKUATAN: SANGAT KUAT 💪")
        else:
            st.warning("KEKUATAN: SEDANG ⚠️")
    
    with col2:
        st.subheader("⏳ Berapa lama peretas bisa menjebol?")
        if detik_retas < 1:
            st.write("Waktu retas: *Sangat Instan (< 1 detik)*")
        elif detik_retas < 60:
            st.write(f"Waktu retas: *~{detik_retas:.2f} detik*")
        elif detik_retas < 3600:
            st.write(f"Waktu retas: *~{detik_retas/60:.2f} menit*")
        elif detik_retas < 86400:
            st.write(f"Waktu retas: *~{detik_retas/3600:.2f} jam*")
        elif detik_retas < 31536000:
            st.write(f"Waktu retas: *~{detik_retas/86400:.2f} hari*")
        else:
            st.write(f"Waktu retas: *~{detik_retas/31536000:.1f} tahun! (Sangat Aman)*")
else:
    st.info("Daftarkan akun di atas untuk melihat estimasi waktu retas.")

# --- BAGIAN 3: LOGIN (VERIFIKASI LOGIKA) ---
st.markdown("---")
st.header("3. Simulasi Login")
if st.session_state.db_user:
    st.write(f"Akun Terdaftar: *{st.session_state.db_user}* | Gagal: *{st.session_state.percobaan}/3*")
    in_user = st.text_input("Username:")
    in_pass = st.text_input("Password:", type="password", key="login")
    
    T = st.session_state.percobaan < 3
    if st.button("Masuk"):
        if not T:
            st.error("AKSES DIBLOKIR! (T=0) Hubungi Admin.")
        elif in_user == st.session_state.db_user and in_pass == st.session_state.db_pass:
            st.success("AKSES DITERIMA! (C=1)")
            st.session_state.percobaan = 0
        else:
            st.session_state.percobaan += 1
            st.error(f"Gagal! Sisa kesempatan: {3 - st.session_state.percobaan}")
            st.rerun()

if st.button("Hapus Semua Data"):
    st.session_state.clear()
    st.rerun()