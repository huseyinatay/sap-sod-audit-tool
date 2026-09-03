import pandas as pd
import os

def run_sod_analysis():
    """
    Kullanıcı yetkilerini okuyup SoD kurallarına göre risk analizi yapan motor.
    """
    input_dir = "data/input"
    output_dir = "data/output"
    
    # Çıktı klasörünün var olduğundan emin olalım
    os.makedirs(output_dir, exist_ok=True)

    # 1. Verilerin Okunması (Kiler'den Tezgah'a)
    try:
        df_users = pd.read_csv(os.path.join(input_dir, "AGR_USERS.csv"))
        df_auths = pd.read_csv(os.path.join(input_dir, "AGR_1251.csv"))
    except FileNotFoundError:
        print("Hata: Girdi dosyaları bulunamadı. Önce 01_data_generator.py dosyasını çalıştırın.")
        return

    # 2. Tabloların Birleştirilmesi (SQL'deki INNER JOIN mantığı)
    # Hangi kullanıcının nihai olarak hangi T-Code'lara eriştiğini buluyoruz.
    df_merged = pd.merge(df_users, df_auths, on="ROL_ADI")

    # 3. SoD Kural Matrisinin Tanımlanması
    # Hangi işlem ikililerinin aynı kişide olmaması gerektiğini belirliyoruz.
    sod_rules = [
        {"risk_id": "R01", "description": "Sipariş Açma ve Mal Girişi", "tcodes": {"ME21N", "MIGO"}},
        {"risk_id": "R02", "description": "Sipariş Açma ve Fatura Girişi", "tcodes": {"ME21N", "MIRO"}},
        {"risk_id": "R03", "description": "Malzeme Çekimi ve Mal Girişi", "tcodes": {"MB1A", "MIGO"}}
    ]

    # 4. Kullanıcı Bazlı Yetki Kümeleme Algoritması
    # Her kullanıcının sahip olduğu benzersiz (unique) T-Code'ları bir set (küme) içinde topluyoruz.
    user_tcodes = df_merged.groupby("KULLANICI_ADI")["T_CODE"].apply(set).to_dict()

    # 5. Kural Motorunun Çalıştırılması (Tarama Algoritması)
    audit_findings = []
    
    for user, codes in user_tcodes.items():
        for rule in sod_rules:
            # Python'un Küme (Set) Kesişim Özelliği: Kuraldaki kodların hepsi kullanıcıda var mı?
            if rule["tcodes"].issubset(codes):
                audit_findings.append({
                    "Risk_ID": rule["risk_id"],
                    "Kullanici_Adi": user,
                    "Aciklama": rule["description"],
                    "Cakisan_Kodlar": ", ".join(rule["tcodes"])
                })

    # 6. Bulguların Raporlanması
    if audit_findings:
        df_findings = pd.DataFrame(audit_findings)
        output_file = os.path.join(output_dir, "sod_risk_report.csv")
        df_findings.to_csv(output_file, index=False)
        
        print(f"Denetim Tamamlandı! {len(df_findings)} adet risk tespit edildi.")
        print(f"Rapor kaydedildi: {output_file}")
        print("\nRiskli Kullanıcılar:")
        print(df_findings)
    else:
        print("Denetim Tamamlandı. Herhangi bir SoD riski bulunamadı.")

if __name__ == "__main__":
    run_sod_analysis()
