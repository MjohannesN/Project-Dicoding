import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')

# Helper function yang dibutuhkan untuk menyiapkan berbagai dataframe

def create_yearly_rent_df(day_df):
    yearly_rent_df = day_df.groupby('yr').agg({
        "cnt": "sum",
        "registered": "sum",
        "casual" : "sum"
    })
    yearly_rent_df = yearly_rent_df.reset_index()
    yearly_rent_df.rename(columns={
        "yr" : "Year",
        "cnt": "Rent_count",
        "registered": "Registered",
        "casual" : "non-Registered"
    }, inplace=True)
    
    return yearly_rent_df

def create_monthly_rent_2011_df(day_df):
    day_df_2011 = day_df[day_df["yr"] == 2011]
    monthly_rent_2011_df = day_df_2011.groupby(['yr','mnth']).agg({
        "cnt": "sum",
        "registered": "sum",
        "casual" : "sum"
    })

    monthly_rent_2011_df = monthly_rent_2011_df.reset_index()
    monthly_rent_2011_df.rename(columns={
        "mnth" : "Mounth",
        "cnt": "Rent_count",
        "registered": "Registered",
        "casual" : "non-Registered"
    }, inplace=True)

    return monthly_rent_2011_df

def create_monthly_rent_2012_df(day_df):
    day_df_2012 = day_df[day_df["yr"] == 2012]
    monthly_rent_2012_df = day_df_2012.groupby(['yr','mnth']).agg({
        "cnt": "sum",
        "registered": "sum",
        "casual" : "sum"
    })

    monthly_rent_2012_df = monthly_rent_2012_df.reset_index()
    monthly_rent_2012_df.rename(columns={
        "mnth" : "Mounth",
        "cnt": "Rent_count",
        "registered": "Registered",
        "casual" : "non-Registered"
    }, inplace=True)

    return monthly_rent_2012_df

def create_daily_rent_df(day_df):
    daily_rent_df = day_df.groupby('weekday').agg({
        "cnt": "mean",
        "registered": "mean",
        "casual" : "mean"
    })

    daily_rent_df = daily_rent_df.reset_index()
    daily_rent_df.rename(columns={
        "weekday" : "Day",
        "cnt": "Rent_count",
        "registered": "Registered",
        "casual" : "non-Registered"
    }, inplace=True)

    return daily_rent_df

def create_hourly_rent_df(hour_df):
    hourly_rent_df = hour_df.groupby('hr').agg({
      "cnt": "mean",
      "registered": "mean",
      "casual" : "mean"
    })

    hourly_rent_df = hourly_rent_df.reset_index()
    hourly_rent_df.rename(columns={
        "hr" : "Hour",
        "cnt": "Rent_count",
        "registered": "Registered",
        "casual" : "non-Registered"
    }, inplace=True)
    return hourly_rent_df

def create_byweather_df(day_df):
    byweather_df = day_df.groupby("weathersit").agg({
        "cnt": "sum",
        "registered": "sum",
        "casual": "sum"
    })

    byweather_df = byweather_df.reset_index()
    byweather_df.rename(columns={
        "weathersit" : "Weather",
        "cnt": "Rent_count",
        "registered": "Registered",
        "casual": "non Registered"
    }, inplace=True)
    
    return byweather_df

def create_byseason_df(day_df):
    byseason_df = day_df.groupby("season").agg({
        "cnt": "sum",
        "registered": "sum",
        "casual": "sum"
    })

    byseason_df.rename(columns={
        "cnt": "Rent_count",
        "registered": "Registered",
        "casual": "non Registered"
    }, inplace=True)

    return byseason_df
    
# Load cleaned data
day_df = pd.read_csv("day_data.csv")
hour_df = pd.read_csv("hour_data.csv")

datetime_columns = ["dteday"]
day_df.sort_values(by="dteday", inplace=True)
day_df.reset_index(inplace=True)

hour_df.sort_values(by="dteday", inplace=True)
hour_df.reset_index(inplace=True)

for column in datetime_columns:
    day_df[column] = pd.to_datetime(day_df[column])
    hour_df[column] = pd.to_datetime(hour_df[column])

# Filter data
min_date_day = day_df["dteday"].min()
max_date_day = day_df["dteday"].max()

min_date_hour = hour_df["dteday"].min()
max_date_hour = hour_df["dteday"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("bikesharing.jpg")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date_day,
        max_value=max_date_day,
        value=[min_date_day, max_date_day]
    )


main_df_day = day_df[(day_df["dteday"] >= str(start_date)) & 
                     (day_df["dteday"] <= str(end_date))]

main_df_hour = hour_df[(hour_df["dteday"] >= str(start_date)) & 
                       (hour_df["dteday"] <= str(end_date))]

# st.dataframe(main_df)

# # Menyiapkan berbagai dataframe
yearly_rent_df = create_yearly_rent_df(main_df_day)
monthly_rent_2011_df = create_monthly_rent_2011_df(main_df_day)
monthly_rent_2012_df = create_monthly_rent_2012_df(main_df_day)
daily_rent_df = create_daily_rent_df(main_df_day)
hourly_rent_df = create_hourly_rent_df(main_df_hour)
byweather_df = create_byweather_df(main_df_day)
byseason_df = create_byseason_df(main_df_day)


# plot number of daily orders (2021)
st.header('BIKE SHARING')
st.subheader('Data Sharing')
with st.container():
    st.write("""Bike Sharing adalah generasi baru dari penyewaan sepeda tradisional di mana seluruh 
        proses keanggotaan, penyewaan, dan pengembalian dilakukan secara otomatis.Melalui sistem 
        ini, pengguna dapat dengan mudah menyewa sepeda dari posisi tertentu dan mengembalikannya 
        di posisi lain. Saat ini, ada lebih dari 500 program berbagi sepeda di seluruh dunia yang 
        terdiri dari lebih dari 500 ribu sepeda. Hari ini, ada minat besar terhadap sistem-sistem 
        ini karena peran penting mereka dalam masalah lalu lintas, lingkungan, dan kesehatan.
        Selain dari aplikasi dunia nyata yang menarik dari sistem bike sharing, karakteristik data 
        yang dihasilkan oleh sistem-sistem ini membuatnya menarik untuk penelitian. Berbeda dengan 
        layanan transportasi lain seperti bus atau kereta bawah tanah, durasi perjalanan, posisi 
        keberangkatan, dan kedatangan secara eksplisit dicatat dalam sistem ini. Fitur ini menjadikan 
        sistem berbagi sepeda sebagai jaringan sensor virtual yang dapat digunakan untuk memantau 
        mobilitas di kota. Oleh karena itu, diharapkan bahwa sebagian besar peristiwa penting di kota 
        dapat terdeteksi melalui pemantauan data ini.
             """
             )
st.title('Analisa Data')
tab1, tab2, tab3 = st.tabs(["Tab 1", "Tab 2", "Tab 3"])
with tab1:
    st.header("Gambaran Besar")

    col1, col2, col3 = st.columns(3)

    with col1:
        total_orders = yearly_rent_df["Rent_count"].sum()
        st.metric("Total Order", value=total_orders)

    with col2:
        total_registered = yearly_rent_df["Registered"].sum()
        st.metric("Registered Order", value=total_registered)

    with col3:
        total_casual = yearly_rent_df["non-Registered"].sum()
        st.metric("non-Registered Order", value=total_casual)

    st.subheader("Bagaimana perkembangan dari penggunaan Bike Sharing dalam 2 tahun terakhir?")

    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))
    colors = ["#E7D3DF", "#D3D3D3", "#B3D3D3", "#93D3D3", "#85BCD6","#72BCD4", "#85BCD6", "#93D3D3", "#B3D3D3", "#C3D3D3","#D3D3D3","#D3D3D3"]

    sns.barplot(x="Rent_count", y="Mounth", data=monthly_rent_2011_df,hue="Mounth",legend=False,orient="h",palette=colors,ax=ax[0])
    ax[0].set_ylabel(None)
    ax[0].set_xlabel(None)
    ax[0].set_title("Rent Monthly Report in 2011", loc="center", fontsize=35)
    ax[0].tick_params(axis ='y', labelsize=25)
    ax[0].tick_params(axis ='x', labelsize=25)

    sns.barplot(x="Rent_count", y="Mounth", data=monthly_rent_2012_df,hue="Mounth",legend=False,orient="h",palette=colors,ax=ax[1])
    ax[1].set_ylabel(None)
    ax[1].set_xlabel(None)
    ax[1].set_title("Rent Monthly Report in 2012", loc="center", fontsize=35)
    ax[1].tick_params(axis ='y', labelsize=25)
    ax[1].tick_params(axis ='x', labelsize=25)

    st.pyplot(fig)
    with st.expander("Lihat penjelasan"):
        st.write(
        """Dari data diatas, dapat dilihat bahwa dari 3.292.676 yang menggunakan jasa bike sharing,
        620.017 diantaranya belum teregistrasi kedalam aplikasi. Selain itu, data diatas menunjukan 
        terjadi kenaikan penggunaan bike sharing dari tahun 2011 ke tahun 2012. Hal ini menunjukan
        telah berkembangnya jangakauan informasi mengenai aplikasi ini
        """
        )

with tab2:
    st.header("Daily Data")
    st.subheader("Bagaimana aktifitas bulanan dan harian yang dimiliki oleh aplikasi ini?")
    fig1 = plt.figure(figsize=(10, 5))
    colors =["#B3D3D3", "#93D3D3", "#85BCD6","#72BCD4", "#85BCD6", "#93D3D3", "#B3D3D3"]

    sns.barplot(
        y="Rent_count",
        x="Day",
        data=daily_rent_df.sort_values(by="Rent_count", ascending=False),
        hue = "Day", legend=False,
        palette=colors
    )
    plt.title("Daily Rent Report", loc="center", fontsize=15)
    plt.ylabel(None)
    plt.xlabel(None)
    plt.tick_params(axis='x', labelsize=12)
    plt.show()
    st.pyplot(fig1)
    with st.expander("Lihat penjelasan"):
        st.write(
        """Kekonsistenan hasil yang ditunjukan dari rata-rata pengguna bike sharing setiap harinya
        dalam satu minggu menunjukan bahwa, aplikasi ini sangat berdampak dan secara rutin digunakan
        dalam menjalankan aktifitas sehari-hari.
        """
        )

    fig2 = plt.figure(figsize=(8, 10))
    colors =["#B3D3D3", "#93D3D3", "#85BCD6","#72BCD4", "#85BCD6", "#93D3D3", "#B3D3D3"]

    sns.barplot(
        x="Rent_count",
        y="Hour",
        data=hourly_rent_df.sort_values(by="Rent_count", ascending=False),
        hue = "Rent_count", legend=False,
        orient ="h",
        palette=colors
    )
    plt.title("Hourly Rent Report", loc="center", fontsize=15)
    plt.ylabel(None)
    plt.xlabel(None)
    plt.tick_params(axis='x', labelsize=12)
    plt.show()
    st.pyplot(fig2)
    with st.expander("Lihat penjelasan"):
        st.write(
        """Dari hasil pengamatan yang dilakukan, didapti bahwa jam sibuk dari aplikasi ini berada pada
        pukul 17.00 waktu timestamp aplikasi. Dimana waktu ini menunjukan waktu jam pulang kerja atau
        aktivitas lainnya.
        """
        )


with tab3:
    st.header("Efek Lingkungan")
    fig3 = plt.figure(figsize=(10, 5))
    colors = ('#D2D583', '#93C572', '#720F07')
    st.subheader("Apa yang mempengaruhi jumlah penggunaan bike sharing dalam satu waktu?")
    sns.barplot(
        x="Weather",
        y= "Rent_count",
        data=byweather_df.sort_values(by="Rent_count", ascending=False),
        hue = "Weather", legend=False,
        palette=colors
    )
    plt.title("Rent Data for Weather", loc="center", fontsize=15)
    plt.ylabel(None)
    plt.xlabel(None)
    plt.tick_params(axis='x', labelsize=12)
    plt.show()
    st.pyplot(fig3)
    with st.expander("Lihat penjelasan"):
        st.write(
        """Efek dari lingkungan sudah pasti menjadi pengaruh besar bagi pengguna sepeda, apalagi untuk
        sepeda sewaan. Untuk itu, kita bisa memprediksi pola dari penggunaan jasa bike sharing melalui
        kondisi lingkungan yang sekarang sedang terjadi. Informasi ini berguna bagi pengguna maupun
        bagi pihak developer, untuk memprediksi situasi aktifitas aplikasi
        """
        )

    fig4 = plt.figure(figsize=(10, 5))
    colors = ('#D2D583', '#93C572', '#720F07',"#D3D3D3")

    sns.barplot(
        x="season",
        y= "Rent_count",
        data=byseason_df.sort_values(by="Rent_count", ascending=False),
        hue = "season", legend=False,
        palette=colors
    )
    plt.title("Season rent", loc="center", fontsize=15)
    plt.ylabel(None)
    plt.xlabel(None)
    plt.tick_params(axis='x', labelsize=12)

    plt.show()
    st.pyplot(fig4)
    with st.expander("Lihat penjelasan"):
        st.write(
        """Selain itu, hal lain yang mempengaruhi aktifitas aplikasi bike sharing adalah musim, dimana
        penggunaan sepeda terhadap musim yang sedang berlangsung juga berpengaruh bagi pengguna yang
        hendak ingin menggunakan jasa bike sharing. Musim gugur menjadi musim yang paling cocok untuk
        menggunakan sepeda.
        """
        )



st.caption('Copyright © Dicoding 2023')