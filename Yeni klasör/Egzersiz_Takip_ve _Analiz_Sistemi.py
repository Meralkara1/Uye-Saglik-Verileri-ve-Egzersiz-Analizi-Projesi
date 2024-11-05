import json  # JSON dosyaları ile çalışmak için gerekli kütüphane
import matplotlib.pyplot as plt  # Grafik çizimleri için kullanılan kütüphane
from collections import defaultdict  # Varsayılan değerlerle çalışan sözlük oluşturmak için
import datetime  # Tarih ve zaman işlemleri için
import tkinter as tk  # Basit grafik arayüzler oluşturmak için Tkinter kütüphanesi
from tkinter import messagebox, simpledialog  # Tkinter ile mesaj kutuları ve diyaloglar
import random  # Rastgele sayı ve veri üretimi için

# Tüm üyelerin bilgilerini ve sağlık verilerini saklayacağımız liste
uyeler = []

# Üye ve egzersiz verisi oluşturmak için örnek veri listeleri
isimler = ["Ahmet Yılmaz", "Ayşe Demir", "Mehmet Kaya", "Fatma Çelik", "Ali Güler", "Elif Şahin"]
egzersiz_turleri = ["Koşu", "Bisiklet", "Yoga", "Yüzme", "Ağırlık"]
yogunluk_seviyeleri = ["Düşük", "Orta", "Yüksek"]

# Yeni bir üye eklemek için fonksiyon
def uye_ekle(isim, yas, cinsiyet, kilo, boy):
    # BMI (Vücut Kitle İndeksi) hesaplaması
    bmi = round(kilo / (boy / 100) ** 2, 2)  # Kilonun boyun karesine bölünmesi
    # Üyenin bilgilerini içeren bir sözlük oluşturuyoruz
    uye = {
        'isim': isim,
        'yas': yas,
        'cinsiyet': cinsiyet,
        'kilo': kilo,
        'boy': boy,
        'bmi': bmi,
        'egzersizler': []  # Üyenin yapacağı egzersizleri burada saklayacağız
    }
    # Yeni üyeyi 'uyeler' listesine ekliyoruz
    uyeler.append(uye)
    kaydet()  # Değişiklikleri dosyaya kaydediyoruz

# Rastgele üye ve egzersiz verisi oluşturma fonksiyonu
def rastgele_uye_ve_egzersiz_ekle():
    # 5 adet rastgele üye ekliyoruz
    for _ in range(5):
        # Her üyenin özelliklerini rastgele olarak belirliyoruz
        isim = random.choice(isimler)
        yas = random.randint(20, 60)
        cinsiyet = random.choice(["Erkek", "Kadın"])
        kilo = random.randint(50, 100)
        boy = random.randint(150, 200)
        
        # Bu rastgele özelliklerle yeni üyeyi ekliyoruz
        uye_ekle(isim, yas, cinsiyet, kilo, boy)
        
        # Her yeni üye için 5 adet rastgele egzersiz verisi oluşturuyoruz
        for _ in range(5):
            tarih = (datetime.datetime.now() - datetime.timedelta(days=random.randint(1, 100))).strftime("%Y-%m-%d")
            tur = random.choice(egzersiz_turleri)
            sure = random.randint(20, 60)
            yogunluk = random.choice(yogunluk_seviyeleri)
            egzersiz_ekle(isim, tarih, tur, sure, yogunluk)

# Veriyi JSON dosyasına kaydetme fonksiyonu
def kaydet():
    # Üyelerin bilgilerini 'uyeler.json' dosyasına kaydediyoruz
    with open("uyeler.json", "w") as dosya:
        json.dump(uyeler, dosya)

# Program açıldığında JSON dosyasından veriyi yükleyen fonksiyon
def veri_yukle():
    global uyeler
    try:
        # JSON dosyasını okuyarak üye verilerini yüklüyoruz
        with open("uyeler.json", "r") as dosya:
            uyeler = json.load(dosya)
    except FileNotFoundError:
        # Dosya bulunmazsa yeni bir liste başlatıyoruz
        uyeler = []

# Ekranda bilgi mesajı göstermek için fonksiyon
def bilgi_ekrani(mesaj):
    # Yeni bir Tkinter penceresi oluşturuyoruz
    pencere = tk.Tk()
    pencere.withdraw()  # Pencereyi gizleyerek sadece mesaj kutusu gösteriyoruz
    messagebox.showinfo("Bilgilendirme", mesaj)  # Mesajı ekrana yazdırıyoruz
    pencere.destroy()  # Pencereyi kapatıyoruz

# Üye seçimi ekranı
def uye_secim_ekrani():
    # Üye seçim ekranı için bir Tkinter penceresi oluşturuyoruz
    pencere = tk.Tk()
    pencere.title("Üye Seçimi")  # Pencere başlığını ayarlıyoruz
    pencere.geometry("300x200")  # Pencere boyutlarını belirliyoruz

    # Kullanıcının üye seçmesi için bir değişken tanımlıyoruz
    secilen_uye = tk.StringVar(pencere)
    secilen_uye.set("Üye Seçin")  # Varsayılan metni ayarlıyoruz

    # Üyelerin isimlerinden oluşan bir liste oluşturuyoruz
    uyeler_listesi = [uye['isim'] for uye in uyeler]
    # Dropdown menü oluşturup üyeleri seçenek olarak ekliyoruz
    secim_menu = tk.OptionMenu(pencere, secilen_uye, *uyeler_listesi)
    secim_menu.pack(pady=20)

    # Kullanıcı seçim yaptığında çağrılacak fonksiyon
    def secimi_tamamla():
        pencere.destroy()  # Pencereyi kapatıyoruz
        uye_analiz_secimi(secilen_uye.get())  # Seçilen üyenin analiz ekranını açıyoruz

    # Seçimi tamamlama butonunu ekliyoruz
    secim_butonu = tk.Button(pencere, text="Seçimi Tamamla", command=secimi_tamamla)
    secim_butonu.pack(pady=20)

    pencere.mainloop()  # Pencereyi çalıştırıyoruz ve kullanıcı etkileşimini bekliyoruz

# Üyenin bilgilerini gösterme ve analiz işlemleri
def uye_analiz_secimi(isim):
    uye_bilgilerini_goster(isim)  # Üyenin bilgilerini ekrana yazdırıyoruz
    ilerleme_analizi(isim)  # Üyenin toplam egzersiz süresini analiz ediyoruz
    saglik_durumu_analizi(isim)  # Üyenin BMI analizini yapıyoruz
    egzersiz_onerisi(isim)  # Üyeye yönelik egzersiz önerisi yapıyoruz

    # Üyenin egzersiz verilerini grafiklerle gösteriyoruz
    haftalik_egzersiz_grafigi(isim)       # Haftalık toplam egzersiz süresi
    yogunluk_dagilimi_grafigi(isim)       # Egzersiz yoğunluk dağılımı
    aylik_egzersiz_grafigi(isim)          # Aylık toplam egzersiz süresi

# Üyenin bilgilerini gösterme fonksiyonu
def uye_bilgilerini_goster(isim):
    for uye in uyeler:
        if uye['isim'] == isim:
            # Üyenin bilgilerini gösteren metni oluşturuyoruz
            bilgi = f"{uye['isim']} - Yaş: {uye['yas']}, BMI: {uye['bmi']}\n"
            bilgi_ekrani(bilgi)  # Bilgi ekranına gönderiyoruz
            break

# Üyeye egzersiz kaydı ekleme fonksiyonu
def egzersiz_ekle(isim, tarih, tur, sure, yogunluk):
    for uye in uyeler:
        if uye['isim'] == isim:
            # Yeni egzersiz kaydını oluşturuyoruz
            egzersiz = {
                'tarih': tarih,
                'tur': tur,
                'sure': sure,
                'yogunluk': yogunluk
            }
            uye['egzersizler'].append(egzersiz)  # Egzersizi üyenin kaydına ekliyoruz
            break
    kaydet()  # Değişiklikleri JSON dosyasına kaydediyoruz

# Üyenin egzersiz süresi analiz fonksiyonu
def ilerleme_analizi(isim):
    for uye in uyeler:
        if uye['isim'] == isim:
            toplam_sure = sum([egz['sure'] for egz in uye['egzersizler']])  # Tüm egzersiz sürelerini topluyoruz
            bilgi_ekrani(f"{isim} üyesinin toplam egzersiz süresi: {toplam_sure} dakika")
            break

# Üyenin sağlık durumu analiz fonksiyonu (BMI'ye göre)
def saglik_durumu_analizi(isim):
    for uye in uyeler:
        if uye['isim'] == isim:
            bmi = uye['bmi']  # Üyenin BMI değerini alıyoruz
            # BMI aralıklarına göre sağlık durumu mesajını belirliyoruz
            if bmi < 18.5:
                mesaj = f"{isim}: Zayıf - Daha fazla kalori almanız önerilir."
            elif 18.5 <= bmi < 24.9:
                mesaj = f"{isim}: Normal - Sağlıklı bir kilodasınız."
            elif 25 <= bmi < 29.9:
                mesaj = f"{isim}: Fazla kilolu - Kardiyo egzersizlerine odaklanabilirsiniz."
            else:
                mesaj = f"{isim}: Obez - Beslenmenizi gözden geçirmeniz önerilir."
            bilgi_ekrani(mesaj)  # Bilgi ekranına mesajı gönderiyoruz
            break

# Egzersiz önerisi fonksiyonu
def egzersiz_onerisi(isim):
    for uye in uyeler:
        if uye['isim'] == isim:
            bmi = uye['bmi']  # Üyenin BMI değeri
            toplam_sure = sum([egz['sure'] for egz in uye['egzersizler']])  # Tüm egzersiz sürelerini topluyoruz
            # BMI değerine göre uygun egzersiz önerileri
            if bmi < 18.5:
                mesaj = f"{isim} için öneri: Zayıfsınız, kas kütlenizi artırmak için direnç egzersizlerine ve daha fazla kalori almaya odaklanabilirsiniz."
            elif 18.5 <= bmi < 24.9:
                mesaj = f"{isim} için öneri: Sağlıklı bir kilodasınız, mevcut egzersiz rutininizi koruyarak dengeli bir program izleyebilirsiniz."
            elif 25 <= bmi < 29.9:
                mesaj = f"{isim} için öneri: Fazla kilolusunuz, haftada en az 150 dakika orta-yüksek yoğunlukta kardiyo eklemeniz faydalı olabilir."
            else:
                mesaj = f"{isim} için öneri: Obezite aralığındasınız, düşük yoğunluklu uzun süreli egzersizlere odaklanarak kalori açığı oluşturabilirsiniz."
            mesaj += f"\nToplam egzersiz süreniz: {toplam_sure} dakika."
            bilgi_ekrani(mesaj)  # Öneriyi bilgi ekranında gösteriyoruz
            break

# Haftalık toplam egzersiz süresi grafiği
def haftalik_egzersiz_grafigi(isim):
    for uye in uyeler:
        if uye['isim'] == isim:
            haftalik_toplamlar = defaultdict(int)  # Her hafta için toplam egzersiz sürelerini saklayacağız
            # Her egzersizin hafta başını bulup süreyi ekliyoruz
            for egz in uye['egzersizler']:
                tarih = datetime.datetime.strptime(egz['tarih'], "%Y-%m-%d")
                hafta_basi = tarih - datetime.timedelta(days=tarih.weekday())
                haftalik_toplamlar[(hafta_basi, egz['tur'])] += egz['sure']
            
            # Haftalar ve egzersiz türleri listelerini oluşturuyoruz
            haftalar = sorted(set([hafta[0] for hafta in haftalik_toplamlar.keys()]))
            egzersiz_turleri = sorted(set([tur[1] for tur in haftalik_toplamlar.keys()]))
            data = {tur: [haftalik_toplamlar[(hafta, tur)] for hafta in haftalar] for tur in egzersiz_turleri}
            
            plt.figure(figsize=(10, 6))
            for tur, sureler in data.items():
                plt.plot(haftalar, sureler, label=tur, marker='o')
            plt.xlabel("Haftalar")
            plt.ylabel("Toplam Egzersiz Süresi (dk)")
            plt.title(f"{isim} Üyesinin Haftalık Egzersiz Süresi Dağılımı")
            plt.legend()
            plt.show()
            break

# Yoğunluk dağılımı grafiği
def yogunluk_dagilimi_grafigi(isim):
    for uye in uyeler:
        if uye['isim'] == isim:
            yogunluk_sureleri = defaultdict(int)
            for egz in uye['egzersizler']:
                yogunluk_sureleri[egz['yogunluk']] += egz['sure']
            
            plt.figure(figsize=(8, 6))
            plt.pie(yogunluk_sureleri.values(), labels=yogunluk_sureleri.keys(), autopct='%1.1f%%')
            plt.title(f"{isim} Üyesinin Egzersiz Yoğunluğu Dağılımı")
            plt.show()
            break

# Aylık toplam egzersiz süresi grafiği
def aylik_egzersiz_grafigi(isim):
    for uye in uyeler:
        if uye['isim'] == isim:
            aylik_toplamlar = defaultdict(int)
            for egz in uye['egzersizler']:
                tarih = datetime.datetime.strptime(egz['tarih'], "%Y-%m-%d")
                ay_basi = tarih.replace(day=1)
                aylik_toplamlar[(ay_basi, egz['tur'])] += egz['sure']
            
            aylar = sorted(set([ay[0] for ay in aylik_toplamlar.keys()]))
            egzersiz_turleri = sorted(set([tur[1] for tur in aylik_toplamlar.keys()]))
            data = {tur: [aylik_toplamlar[(ay, tur)] for ay in aylar] for tur in egzersiz_turleri}
            
            plt.figure(figsize=(10, 6))
            for tur, sureler in data.items():
                plt.plot(aylar, sureler, label=tur, marker='o')
            plt.xlabel("Aylar")
            plt.ylabel("Toplam Egzersiz Süresi (dk)")
            plt.title(f"{isim} Üyesinin Aylık Egzersiz Süresi Dağılımı")
            plt.legend()
            plt.show()
            break

# Program başlarken veriyi yükleyelim ve rastgele üyeler ekleyelim
veri_yukle()
if not uyeler:
    rastgele_uye_ve_egzersiz_ekle()

# Üye seçimi ve analiz işlemleri
uye_secim_ekrani()
