 # SAP SoD (Segregation of Duties) Audit Tool

Bu proje, şirketlerin Kurumsal Kaynak Planlama (ERP) sistemlerindeki (özellikle SAP) yetki çakışmalarını ve olası suistimal (fraud) risklerini tespit etmek amacıyla geliştirilmiş kural tabanlı bir IT Denetim aracıdır.

## Proje Amacı

Büyük ölçekli organizasyonlarda "Görevler Ayrılığı" (Segregation of Duties - SoD) prensibi, finansal güvenliği sağlamanın temelidir. Bir kullanıcının hem satın alma siparişi açıp hem de mal girişi onaylaması büyük bir denetim bulgusudur. 

Bu araç, gerçek bir SAP veritabanına ihtiyaç duymadan sentetik yetki tabloları (`AGR_USERS` ve `AGR_1251`) üretir ve bir kural motoru (Rule Engine) üzerinden bu verileri çapraz sorgulayarak riskli kullanıcıları tespit eder.

## Kullanılan Teknolojiler
* **Programlama Dili:** Python
* **Veri İşleme ve Analiz:** Pandas
* **Veri Yapıları:** Set (Kesişim algoritmaları için), Dictionary

## Sistem Mimarisi ve Çalışma Mantığı

Proje iki ana modülden oluşmaktadır:

1. **Veri Üreticisi (`01_data_generator.py`):**
   * Sahte SAP kullanıcılarını, rollerini ve bu rollere bağlı işlem kodlarını (T-Code) oluşturarak `/data/input` klasörüne CSV formatında kaydeder.
   
2. **SoD Kural Motoru (`02_sod_engine.py`):**
   * Üretilen verileri Pandas DataFrame olarak hafızaya alır.
   * `INNER JOIN` mantığı ile kullanıcı ve yetki tablolarını birleştirir.
   * Her bir kullanıcının erişebildiği benzersiz yetki kümesini oluşturur ve önceden tanımlanmış Risk Matrisi ile kesişim (Subset) testine sokar.
   * Kural ihlali yapan kullanıcıları `/data/output/sod_risk_report.csv` olarak raporlar.

## Kurulum ve Kullanım

Projeyi kendi bilgisayarınızda çalıştırmak için aşağıdaki adımları izleyebilirsiniz:

```bash
# Repoyu klonlayın
git clone [https://github.com/huseyinatay/sap-sod-audit-tool.git](https://github.com/huseyinatay/sap-sod-audit-tool.git)

# Gerekli kütüphaneleri yükleyin
pip install -r requirements.txt

# 1. Sentetik verileri üretin
python src/01_data_generator.py

# 2. Denetim algoritmasını çalıştırın
python src/02_sod_engine.py
