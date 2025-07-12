import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math

def model_antrian():
    st.header("⏳ Analisis Sistem Antrian")
    st.subheader("Studi Kasus: Drive-Thru 'Ayam Goreng Juara' saat Jam Sibuk")

    col1, col2 = st.columns([1.5, 2])

    with col1:
        st.markdown("""
        *Skenario Bisnis:*  
        Manajemen 'Ayam Goreng Juara' ingin menganalisis efisiensi layanan drive-thru untuk menyeimbangkan biaya operasional dan kepuasan pelanggan (waktu tunggu).
        """)

        with st.container(border=True):
            st.subheader("📈 Parameter Sistem")
            lmbda = st.slider("Tingkat Kedatangan (λ - mobil/jam)", 1, 100, 30)
            mu = st.slider("Tingkat Pelayanan (μ - mobil/jam)", 1, 100, 35)

            with st.expander("Penjelasan Rumus Model: Antrian M/M/1"):
                st.markdown("""
                Model antrian M/M/1 digunakan untuk menganalisis sistem dengan satu server (pelayan).  
                Model ini membantu memahami metrik kinerja utama:
                - *Utilisasi (ρ):* Seberapa sibuk server.  
                - *Panjang Antrian (L, Lq):* Rata-rata jumlah pelanggan di sistem dan di antrian.  
                - *Waktu Tunggu (W, Wq):* Lama rata-rata pelanggan di sistem dan dalam antrian.  
                """)
                st.latex(r''' \rho = \frac{\lambda}{\mu} \quad | \quad L = \frac{\rho}{1 - \rho} \quad | \quad W = \frac{L}{\lambda} ''')

            if mu <= lmbda:
                st.error("Tingkat pelayanan (μ) harus lebih besar dari tingkat kedatangan (λ) agar antrian stabil.")
                return

            # Perhitungan
            rho = lmbda / mu
            L = rho / (1 - rho)
            Lq = (rho ** 2) / (1 - rho)
            W = L / lmbda
            Wq = Lq / lmbda

            with st.expander("Lihat Proses Perhitungan"):
                st.latex(fr"\rho = \frac{{{lmbda}}}{{{mu}}} = {rho:.2f}")
                st.latex(fr"L = \frac{{{rho:.2f}}}{{1 - {rho:.2f}}} = {L:.2f}")
                st.latex(fr"L_q = \frac{{{rho:.2f}^2}}{{1 - {rho:.2f}}} = {Lq:.2f}")
                st.latex(fr"W = \frac{{{L:.2f}}}{{{lmbda}}} = {W:.3f} \text{{ jam, atau }} {W*60:.2f} \text{{ menit}}")
                st.latex(fr"W_q = \frac{{{Lq:.2f}}}{{{lmbda}}} = {Wq:.3f} \text{{ jam, atau }} {Wq*60:.2f} \text{{ menit}}")

    with col2:
        st.subheader("💡 Hasil dan Wawasan Bisnis")
        st.success(f"Rekomendasi: Dengan tingkat pelayanan saat ini, rata-rata pelanggan akan menunggu *{Wq*60:.1f} menit* dalam antrian.")

        col1_res, col2_res = st.columns(2)
        with col1_res:
            st.metric(label="🚗 Rata-rata Mobil di Sistem (L)", value=f"{L:.2f} mobil")
            st.metric(label="⏳ Rata-rata Total Waktu (W)", value=f"{W*60:.2f} menit")
        with col2_res:
            st.metric(label="🚗 Rata-rata Panjang Antrian (Lq)", value=f"{Lq:.2f} mobil")
            st.metric(label="⏳ Rata-rata Waktu Tunggu (Wq)", value=f"{Wq*60:.2f} menit")

        with st.container(border=True):
            st.markdown("*Analisis Kinerja Sistem:*")
            if rho > 0.85:
                st.error(f"- *Kondisi Kritis ({rho:.1%})*: Tingkat kesibukan sangat tinggi. Waktu tunggu panjang bisa merusak reputasi.")
            elif rho > 0.7:
                st.warning(f"- *Perlu Diwaspadai ({rho:.1%})*: Sistem cukup sibuk dan bisa kewalahan saat lonjakan pelanggan.")
            else:
                st.info(f"- *Kinerja Sehat ({rho:.1%})*: Sistem terkendali.")

    # Pie Chart
    st.markdown("#### Visualisasi Kinerja Antrian")
    fig1, ax1 = plt.subplots(figsize=(8, 4))
    waktu_pelayanan_menit = (1 / mu) * 60
    waktu_tunggu_menit = Wq * 60
    labels = ['Waktu Menunggu di Antrian', 'Waktu Dilayani']
    sizes = [waktu_tunggu_menit, waktu_pelayanan_menit]
    colors = ['#ff6347', '#90ee90']
    explode = (0.1, 0)

    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            startangle=90, colors=colors)
    ax1.axis('equal')
    ax1.set_title("Bagaimana Pelanggan Menghabiskan Waktunya?")
    st.pyplot(fig1)

    # Bar Chart - Probabilitas Panjang Antrian
    st.markdown("#### Probabilitas Panjang Antrian")
    if rho >= 1:
        st.warning("⚠ Sistem antrian tidak stabil (ρ ≥ 1). Tidak bisa menampilkan distribusi probabilitas.")
    else:
        n_values = np.arange(0, 15)
        p_n_values = [(1 - rho) * (rho ** n) for n in n_values]

        fig2, ax2 = plt.subplots(figsize=(10, 4))
        ax2.bar(n_values, p_n_values, color='skyblue')
        for i, v in enumerate(p_n_values):
            ax2.text(i, v, f"{v:.1%}", ha='center', va='bottom', fontsize=9)

        ax2.set_xlabel('Jumlah Mobil dalam Sistem (n)')
        ax2.set_ylabel('Probabilitas P(n)')
        ax2.set_title(f'Peluang Jumlah Mobil di Sistem Saat Ini (ρ = {rho:.2f})')
        ax2.set_xticks(n_values)
        ax2.grid(True, axis='y', linestyle='--')
        ax2.set_yticklabels([])
        st.pyplot(fig2)

        with st.container(border=True):
            st.markdown("🔍 Penjelasan Grafik:")
            st.markdown("""
            - *Grafik Batang* menunjukkan kemungkinan jumlah mobil yang ada di sistem (baik menunggu maupun dilayani).  
            - Peluang semakin besar di kanan artinya sistem makin sering penuh atau antrian panjang terjadi.  
            """)

    # Heatmap W vs rho (simulasi)
    st.markdown("#### Simulasi Dampak Utilisasi (ρ) terhadap Waktu Tunggu")
    rho_vals = np.linspace(0.01, 0.95, 100)
    Wq_vals = [(r**2) / (1 - r) / (r * mu) * 60 for r in rho_vals]  # dalam menit

    fig3, ax3 = plt.subplots(figsize=(10, 3))
    ax3.plot(rho_vals, Wq_vals, color='tomato')
    ax3.set_xlabel("Utilisasi (ρ)")
    ax3.set_ylabel("Waktu Tunggu Rata-rata (menit)")
    ax3.set_title("Semakin Sibuk Sistem, Semakin Lama Pelanggan Menunggu")
    ax3.grid(True)
    st.pyplot(fig3)
    