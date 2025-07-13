import streamlit as st
import math
import pandas as pd
import plotly.express as px

# --- Page Configuration ---
st.set_page_config(
    page_title="EOQ untuk Botol Minuman",
    page_icon="🧃",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for a more appealing UI ---
st.markdown("""
<style>
    .main {
        background-color: #f0f2f6;
        padding: 20px;
    }
    .stApp {
        max-width: 800px;
        margin: auto;
    }
    .st-emotion-cache-1pxazr7 { /* Target the Streamlit primary button */
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        padding: 10px 24px;
        font-size: 18px;
        font-weight: bold;
        border: none;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
    }
    .st-emotion-cache-1pxazr7:hover {
        background-color: #45a049;
    }
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 1.1rem;
    }
    h1 {
        color: #2e86de; /* A nice blue for titles */
        text-align: center;
        font-size: 2.5em;
        margin-bottom: 20px;
    }
    h2 {
        color: #34495e; /* Darker shade for sections */
        font-size: 1.8em;
        border-bottom: 2px solid #aec6cf;
        padding-bottom: 5px;
        margin-top: 30px;
    }
    .metric-box {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
        text-align: center;
    }
    .metric-value {
        font-size: 2.2em;
        font-weight: bold;
        color: #28a745; /* Green for key metrics */
    }
    .metric-label {
        font-size: 1em;
        color: #555;
    }
    .stAlert {
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# --- Title and Introduction ---
st.title("🧃 EOQ untuk Botol Minuman")
st.markdown("### *komponen, seperti botol plastik kosong*")
st.write("""
Selamat datang di aplikasi simulasi Economic Order Quantity (EOQ)!
Aplikasi ini membantu Anda mengoptimalkan jumlah pemesanan komponen, seperti botol plastik,
untuk menekan biaya persediaan tahunan Anda. Mari kita mulai!
""")

# --- Tabs for navigation ---
tab1, tab2, tab3, tab4 = st.tabs(["💡 Tentang EOQ", "📊 Input Data", "📈 Hasil & Analisis", "❓ FAQ"])

with tab1:
    st.header("💡 Apa Itu EOQ?")
    st.write("""
    EOQ (Economic Order Quantity) adalah model pemesanan persediaan yang digunakan untuk menentukan
    jumlah optimal unit yang harus dipesan untuk meminimalkan biaya persediaan total.
    Model ini mempertimbangkan dua biaya utama:
    * **Biaya Pemesanan (Ordering Cost):** Biaya yang terkait dengan penempatan pesanan, seperti biaya administrasi, biaya pengangkutan, dll.
    * **Biaya Penyimpanan (Holding Cost):** Biaya yang terkait dengan penyimpanan persediaan, seperti biaya gudang, asuransi, biaya modal, dll.
    """)
    st.write("Tujuan utama EOQ adalah menemukan titik di mana biaya pemesanan dan biaya penyimpanan seimbang, menghasilkan biaya total persediaan yang paling rendah.")
    st.write("#### Asumsi Model EOQ:")
    st.markdown("""
    * Permintaan konstan dan diketahui.
    * Biaya pemesanan dan penyimpanan tetap.
    * Tidak ada kekurangan stok (stockout).
    * Lead time (waktu antara pemesanan dan penerimaan) konstan.
    """)

with tab2:
    st.header("📊 Masukkan Data Anda")
    st.markdown("Isi kolom di bawah ini dengan data spesifik perusahaan Anda untuk menghitung EOQ.")

    # Input fields without default values
    st.subheader("Parameter Input:")
    annual_demand = st.number_input(
        "Permintaan Tahunan (D) - unit/tahun",
        min_value=0, # Changed from 1 to 0, allowing user to start from scratch
        value=0,     # Set default value to 0
        step=1,
        help="Total unit layar LCD yang dibutuhkan dalam satu tahun. Masukkan angka bulat."
    )
    ordering_cost = st.number_input(
        "Biaya Pemesanan (S) - Rp/order",
        min_value=0, # Changed from 1000 to 0
        value=0,     # Set default value to 0
        step=1000,
        help="Biaya untuk menempatkan satu pesanan, tidak termasuk biaya unit. Masukkan angka bulat."
    )
    holding_cost = st.number_input(
        "Biaya Penyimpanan (H) - Rp/unit/tahun",
        min_value=0, # Changed from 100 to 0
        value=0,     # Set default value to 0
        step=10,
        help="Biaya untuk menyimpan satu unit layar LCD selama satu tahun. Masukkan angka bulat."
    )

    # Validate inputs before calculation
    if st.button("Hitung EOQ"):
        if annual_demand <= 0 or ordering_cost <= 0 or holding_cost <= 0:
            st.error("Semua input (Permintaan Tahunan, Biaya Pemesanan, Biaya Penyimpanan) harus lebih besar dari nol untuk melakukan perhitungan.")
            st.session_state['calculate'] = False
        else:
            st.session_state['calculate'] = True
            st.session_state['D'] = annual_demand
            st.session_state['S'] = ordering_cost
            st.session_state['H'] = holding_cost
    else:
        # Initialize if button not pressed yet or if navigating away and back
        if 'calculate' not in st.session_state:
            st.session_state['calculate'] = False

with tab3:
    st.header("📈 Hasil Perhitungan & Analisis")
    if st.session_state.get('calculate', False):
        D = st.session_state['D']
        S = st.session_state['S']
        H = st.session_state['H']

        try:
            # EOQ Calculation
            eoq = math.sqrt((2 * D * S) / H)
            eoq_rounded = round(eoq)

            # Other derived metrics
            orders_per_year = D / eoq
            orders_per_year_rounded = math.ceil(orders_per_year) # Round up for practical orders

            total_ordering_cost = orders_per_year_rounded * S
            total_holding_cost = (eoq / 2) * H
            total_inventory_cost = total_ordering_cost + total_holding_cost

            st.success("Perhitungan berhasil!")

            st.markdown("### Ringkasan Hasil:")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                <div class="metric-box">
                    <div class="metric-value">{eoq_rounded:,.0f} unit</div>
                    <div class="metric-label">EOQ (Unit Optimal per Pesanan)</div>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div class="metric-box">
                    <div class="metric-value">{orders_per_year_rounded} kali</div>
                    <div class="metric-label">Jumlah Pesanan per Tahun</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-value">Rp {total_inventory_cost:,.0f}</div>
                <div class="metric-label">Total Biaya Persediaan Tahunan</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("### Detail Biaya:")
            st.info(f"**Total Biaya Pemesanan:** Rp {total_ordering_cost:,.0f} (dihitung dari {orders_per_year_rounded} pesanan x Rp {S:,.0f}/pesanan)")
            st.info(f"**Total Biaya Penyimpanan:** Rp {total_holding_cost:,.0f} (dihitung dari ({eoq_rounded} unit / 2) x Rp {H:,.0f}/unit/tahun)")

            st.markdown("### Rekomendasi:")
            st.write(f"""
            Berdasarkan perhitungan EOQ, perusahaan disarankan untuk memesan sekitar
            **{eoq_rounded:,.0f} unit** layar LCD setiap kali melakukan pesanan.
            Ini akan menghasilkan sekitar **{orders_per_year_rounded} kali** pemesanan dalam setahun.
            Dengan mengikuti rekomendasi ini, biaya persediaan total tahunan Anda dapat diminimalkan menjadi
            sekitar **Rp {total_inventory_cost:,.0f}**.
            """)
            st.write("Model EOQ ini dapat digunakan sebagai dasar pengambilan keputusan strategis dalam logistik persediaan Anda.")

            st.markdown("### Visualisasi Biaya EOQ")
            st.write("Grafik di bawah ini menunjukkan bagaimana biaya pemesanan, biaya penyimpanan, dan total biaya berubah seiring dengan jumlah pesanan.")

            # --- Data for plotting ---
            order_quantities = []
            ordering_costs = []
            holding_costs = []
            total_costs = []

            # Generate data points around EOQ
            # We'll go from a small fraction of EOQ up to double EOQ
            # Ensure min_q is at least 1 to avoid division by zero later
            min_q_plot = max(1, int(eoq_rounded * 0.1))
            max_q_plot = int(eoq_rounded * 2.0)
            step_q = max(1, int(eoq_rounded / 50)) # Ensure enough points for smooth curve

            # Add more points around the EOQ for better visualization
            for q in range(min_q_plot, max_q_plot + step_q, step_q):
                if q == 0: continue # Should not happen with min_q_plot > 0, but as a safeguard
                current_ordering_cost = (D / q) * S
                current_holding_cost = (q / 2) * H
                current_total_cost = current_ordering_cost + current_holding_cost

                order_quantities.append(q)
                ordering_costs.append(current_ordering_cost)
                holding_costs.append(current_holding_cost)
                total_costs.append(current_total_cost)

            # Add the exact EOQ point if it's not already in the list for better highlight
            # Check if eoq_rounded is positive to avoid adding 0 to lists
            if eoq_rounded > 0 and eoq_rounded not in order_quantities:
                order_quantities.append(eoq_rounded)
                ordering_costs.append((D / eoq_rounded) * S)
                holding_costs.append((eoq_rounded / 2) * H)
                total_costs.append(((D / eoq_rounded) * S) + ((eoq_rounded / 2) * H))

            # Sort the lists based on order_quantities to ensure correct plotting
            # Create a list of tuples and sort it
            combined = sorted(zip(order_quantities, ordering_costs, holding_costs, total_costs))
            order_quantities, ordering_costs, holding_costs, total_costs = zip(*combined)


            # Create DataFrame
            df_costs = pd.DataFrame({
                'Jumlah Pesanan (Unit)': order_quantities,
                'Biaya Pemesanan': ordering_costs,
                'Biaya Penyimpanan': holding_costs,
                'Total Biaya': total_costs
            })

            # Melt DataFrame for Plotly Express
            df_melted = df_costs.melt(id_vars=['Jumlah Pesanan (Unit)'], var_name='Jenis Biaya', value_name='Biaya (Rp)')

            # Create the plot
            fig = px.line(
                df_melted,
                x='Jumlah Pesanan (Unit)',
                y='Biaya (Rp)',
                color='Jenis Biaya',
                title='Kurva Biaya EOQ',
                labels={'Biaya (Rp)': 'Biaya (Rp)', 'Jumlah Pesanan (Unit)': 'Jumlah Pesanan (Unit)'},
                hover_data={'Biaya (Rp)': ':, .0f'}
            )

            # Add a vertical line for EOQ, only if eoq_rounded is valid
            if eoq_rounded > 0:
                fig.add_vline(x=eoq_rounded, line_dash="dash", line_color="red",
                              annotation_text=f"EOQ: {eoq_rounded}", annotation_position="top right")

            fig.update_layout(
                xaxis_title="Jumlah Pesanan (Unit)",
                yaxis_title="Biaya (Rp)",
                legend_title="Jenis Biaya",
                hovermode="x unified"
            )

            st.plotly_chart(fig, use_container_width=True)


        except ZeroDivisionError:
            st.error("Biaya penyimpanan (H) tidak boleh nol. Mohon masukkan nilai yang valid.")
        except Exception as e:
            st.error(f"Terjadi kesalahan saat menghitung: {e}. Pastikan semua input valid dan positif.")
    else:
        st.info("Silakan masukkan data di tab 'Input Data' dan klik 'Hitung EOQ' untuk melihat hasilnya.")

with tab4:
    st.header("❓ Pertanyaan Umum (FAQ)")
    st.subheader("Mengapa EOQ penting?")
    st.write("""
    EOQ membantu perusahaan menyeimbangkan biaya pemesanan dan biaya penyimpanan, yang keduanya
    berkontribusi pada total biaya persediaan. Dengan menemukan EOQ, perusahaan dapat menghindari
    kelebihan stok (yang meningkatkan biaya penyimpanan) dan kekurangan stok (yang mengganggu produksi).
    """)

    st.subheader("Apakah asumsi EOQ selalu berlaku di dunia nyata?")
    st.write("""
    Tidak selalu. Model EOQ memiliki asumsi tertentu (permintaan konstan, lead time konstan, dll.).
    Di dunia nyata, permintaan bisa berfluktuasi. Namun, EOQ tetap menjadi dasar yang baik
    untuk memulai optimasi dan dapat disesuaikan dengan mempertimbangkan faktor-faktor lain
    seperti diskon kuantitas atau ketidakpastian permintaan.
    """)

    st.subheader("Bagaimana jika permintaan tidak konstan?")
    st.write("""
    Jika permintaan tidak konstan, model EOQ dasar mungkin kurang akurat. Dalam kasus seperti itu,
    metode peramalan yang lebih canggih atau model persediaan yang mempertimbangkan
    variabilitas permintaan (misalnya, ROP dengan safety stock) mungkin lebih sesuai.
    """)

# --- Footer ---
st.markdown("""
---
<p style='text-align: center; color: gray;'>
    Aplikasi ini dibuat untuk tujuan edukasi dan demonstrasi berdasarkan studi kasus optimasi EOQ.
</p>
""", unsafe_allow_html=True)
