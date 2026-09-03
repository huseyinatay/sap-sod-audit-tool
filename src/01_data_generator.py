import pandas as pd
import numpy as np
import os

def generate_sap_data():
    """
    Sentetik SAP yetki ve kullanıcı verilerini üreten ana fonksiyon.
    """
    # 1. Klasör Kontrolü (İşletim Sistemi Fonksiyonu)
    # Verileri kaydedeceğimiz dizini belirliyoruz.
    output_dir = "data/input"
    
    # os.makedirs(): Belirtilen yoldaki klasörleri oluşturur. 
    # exist_ok=True: Klasör zaten varsa hata vermesini engeller.
    os.makedirs(output_dir, exist_ok=True)

    # 2. AGR_1251 (Rol ve T-Code Eşleşmesi) Tablosunun Üretilmesi
    # Bir sözlük (dictionary) yapısı kurarak rolleri ve içerdikleri işlem kodlarını tanımlıyoruz.
    roles_data = {
        "ROL_ADI": [
            "Z_SATINALMA_UZMANI", "Z_SATINALMA_UZMANI", 
            "Z_DEPO_YONETICISI", "Z_DEPO_YONETICISI",
            "Z_FINANS_ONAY", "Z_FINANS_ONAY",
            "Z_SISTEM_ADMIN"
        ],
        "T_CODE": [
            "ME21N", "ME22N", # Sipariş yaratma ve değiştirme
            "MIGO", "MB1A",   # Mal girişi ve malzeme çekimi
            "MIRO", "FB60",   # Fatura girişi
            "SU01"            # Kullanıcı yönetimi (Kritik yetki)
        ]
    }
    
    # pd.DataFrame(): Sözlük (dict) formatındaki veriyi pandas'ın satır ve sütunlardan oluşan 
    # tablo yapısına (DataFrame) dönüştürür. Veri manipülasyonu için temel nesnemizdir.
    df_agr_1251 = pd.DataFrame(roles_data)


    # 3. AGR_USERS (Kullanıcı ve Rol Eşleşmesi) Tablosunun Üretilmesi
    # Sisteme sahte kullanıcılar ve onların rollerini ekliyoruz.
    users_data = {
        "KULLANICI_ADI": [
            "AHMET_YILMAZ", "AHMET_YILMAZ", # Ahmet'te SoD riski var (Satınalma + Depo)
            "AYSE_KAYA", 
            "MEHMET_DEMIR", "MEHMET_DEMIR", # Mehmet'te SoD riski var (Satınalma + Finans)
            "FATMA_CELIK", 
            "ADMIN_01"
        ],
        "ROL_ADI": [
            "Z_SATINALMA_UZMANI", "Z_DEPO_YONETICISI",
            "Z_DEPO_YONETICISI",
            "Z_SATINALMA_UZMANI", "Z_FINANS_ONAY",
            "Z_FINANS_ONAY",
            "Z_SISTEM_ADMIN"
        ]
    }
    
    df_agr_users = pd.DataFrame(users_data)

    # 4. Verilerin CSV Formatında Kaydedilmesi
    # to_csv(): Hafızadaki DataFrame'i fiziksel bir metin dosyasına (CSV) dönüştürüp kaydeder.
    # index=False: Pandas otomatik olarak 0,1,2 diye satır numarası (index) ekler. 
    # Gerçek veri tabanlarında bu tarz bir indeks sütunu olmadığı için bunu dosyaya yazdırmıyoruz.
    
    file_path_1251 = os.path.join(output_dir, "AGR_1251.csv")
    file_path_users = os.path.join(output_dir, "AGR_USERS.csv")
    
    df_agr_1251.to_csv(file_path_1251, index=False)
    df_agr_users.to_csv(file_path_users, index=False)
    
    print(f"Başarılı! Veriler şu klasöre kaydedildi: {output_dir}")
    print("Oluşturulan Kullanıcı Sayısı (Satır):", len(df_agr_users))
    print("Oluşturulan Rol-TCode Sayısı (Satır):", len(df_agr_1251))

# Script doğrudan çalıştırıldığında fonksiyonu tetikler
if __name__ == "__main__":
    generate_sap_data()
