"""İlaç saatleri planlayıcısı. Python 3.9+; harici paket gerekmez."""
import csv
from datetime import datetime, timedelta
from pathlib import Path

DOSYA = Path(__file__).with_name('ilac_plani.csv')


def saat_dogrula(metin):
    try:
        saat = datetime.strptime(metin, '%H:%M')
        if saat.strftime('%H:%M') != metin:
            return None
        return metin
    except ValueError:
        return None


def pozitif_sayi_iste(mesaj, en_fazla):
    while True:
        deger = input(mesaj).strip()
        if deger.isdigit() and 1 <= int(deger) <= en_fazla:
            return int(deger)
        print(f'Hatalı giriş! 1 ile {en_fazla} arasında tam sayı giriniz.')


def saat_iste():
    while True:
        saat = input('İlk kullanım saati (SS:DD, örn. 08:30): ').strip()
        if saat_dogrula(saat):
            return saat
        print('Hatalı saat! Örnek: 08:30 (00:00–23:59).')


def plan_olustur(baslangic, aralik, gun_sayisi):
    ilk = datetime.strptime(baslangic, '%H:%M')
    # Tarih içermeyen saatler için bugünün tarihi kullanılır.
    ilk = datetime.combine(datetime.now().date(), ilk.time())
    son = ilk + timedelta(days=gun_sayisi)
    zamanlar = []
    an = ilk
    while an < son:
        zamanlar.append(an.strftime('%Y-%m-%d %H:%M'))
        an += timedelta(hours=aralik)
    return zamanlar


def kaydet(planlar):
    with DOSYA.open('w', newline='', encoding='utf-8-sig') as dosya:
        yazici = csv.writer(dosya)
        yazici.writerow(['Ilac', 'Doz_aciklamasi', 'Tarih_saat', 'Durum'])
        for plan in planlar:
            for kayit in plan['kayitlar']:
                yazici.writerow([plan['ad'], plan['doz'], kayit['zaman'], kayit['durum']])


def yukle():
    planlar = []
    if not DOSYA.exists():
        return planlar
    try:
        with DOSYA.open('r', newline='', encoding='utf-8-sig') as dosya:
            for satir in csv.DictReader(dosya):
                ad, doz = satir['Ilac'], satir['Doz_aciklamasi']
                zaman = satir['Tarih_saat']
                datetime.strptime(zaman, '%Y-%m-%d %H:%M')
                durum = satir['Durum'] if satir['Durum'] in ('Bekliyor', 'Alındı') else 'Bekliyor'
                plan = next((p for p in planlar if p['ad'] == ad and p['doz'] == doz), None)
                if plan is None:
                    plan = {'ad': ad, 'doz': doz, 'kayitlar': []}
                    planlar.append(plan)
                plan['kayitlar'].append({'zaman': zaman, 'durum': durum})
    except (OSError, ValueError, KeyError, csv.Error) as hata:
        print('Kayıt dosyası okunamadı:', hata)
        print('Mevcut dosya korunuyor. Önce dosyayı kontrol edin.')
        return None
    return planlar


def ekle(planlar):
    ad = input('İlaç adı: ').strip()
    while not ad:
        print('İlaç adı boş olamaz.')
        ad = input('İlaç adı: ').strip()
    doz = input('Reçetedeki doz açıklaması (örn. 1 tablet): ').strip()
    while not doz:
        print('Doz açıklaması boş olamaz.')
        doz = input('Doz açıklaması: ').strip()
    print('Yalnızca doktor/eczacı tarafından belirtilen saat aralığını giriniz.')
    aralik = pozitif_sayi_iste('Kaç saatte bir? (1–24): ', 24)
    gun = pozitif_sayi_iste('Kaç gün? (1–30): ', 30)
    baslangic = saat_iste()
    zamanlar = plan_olustur(baslangic, aralik, gun)
    planlar.append({'ad': ad, 'doz': doz, 'kayitlar': [
        {'zaman': z, 'durum': 'Bekliyor'} for z in zamanlar]})
    kaydet(planlar)
    print(f'✓ {len(zamanlar)} kullanım saati planlandı ve CSV dosyasına kaydedildi.')


def listele(planlar):
    if not planlar:
        print('Henüz kayıt yok.')
        return
    print('\n' + '=' * 78)
    print(f"{'No':<5}{'İlaç':<19}{'Doz':<18}{'Tarih ve saat':<19}Durum")
    print('-' * 78)
    no = 0
    for plan in planlar:
        for kayit in plan['kayitlar']:
            no += 1
            print(f"{no:<5}{plan['ad'][:18]:<19}{plan['doz'][:17]:<18}{kayit['zaman']:<19}{kayit['durum']}")
    print('=' * 78)


def yaklasanlari_goster(planlar, simdi=None):
    simdi = simdi or datetime.now()
    bitis = simdi + timedelta(hours=24)
    bulunan = []
    geciken = []
    for plan in planlar:
        for kayit in plan['kayitlar']:
            if kayit['durum'] == 'Alındı':
                continue
            zaman = datetime.strptime(kayit['zaman'], '%Y-%m-%d %H:%M')
            if simdi <= zaman <= bitis:
                bulunan.append((zaman, plan['ad'], plan['doz']))
            elif zaman < simdi:
                geciken.append((zaman, plan['ad']))
    print('\nÖnümüzdeki 24 saatte planlanan kullanımlar:')
    for zaman, ad, doz in sorted(bulunan):
        print(f'  {zaman:%d.%m.%Y %H:%M} | {ad} | {doz}')
    if not bulunan:
        print('  Yaklaşan kullanım bulunamadı.')
    if geciken:
        print(f'⚠ {len(geciken)} geçmiş saatli, henüz onaylanmamış kayıt var.')
        print('Geciken doz için çift doz almayın; sağlık uzmanınıza danışın.')


def alindi_isaretle(planlar):
    kayitlar = [(p, k) for p in planlar for k in p['kayitlar']]
    if not kayitlar:
        print('İşaretlenecek kayıt yok.')
        return
    listele(planlar)
    while True:
        secim = input('Alındı işaretlenecek kayıt numarası (iptal: 0): ').strip()
        if secim == '0':
            return
        if secim.isdigit() and 1 <= int(secim) <= len(kayitlar):
            _, kayit = kayitlar[int(secim) - 1]
            kayit['durum'] = 'Alındı'
            kaydet(planlar)
            print('✓ Kayıt güncellendi.')
            return
        print('Geçersiz kayıt numarası.')


def main():
    print('=== İLAÇ / TEDAVİ SAATLERİ PLANLAYICI ===')
    print('Bu program doz veya tedavi önermez; yalnızca girilen planı takip eder.')
    planlar = yukle()
    if planlar is None:
        return
    while True:
        print('\n1) Yeni ilaç planı ekle\n2) Tüm planı göster\n3) Önümüzdeki 24 saati kontrol et')
        print('4) Kullanımı alındı olarak işaretle\n5) Çıkış')
        secim = input('Seçiminiz (1-5): ').strip()
        if secim == '1':
            ekle(planlar)
        elif secim == '2':
            listele(planlar)
        elif secim == '3':
            yaklasanlari_goster(planlar)
        elif secim == '4':
            alindi_isaretle(planlar)
        elif secim == '5':
            print('Plan kaydedildi. Görüşmek üzere!')
            break
        else:
            print('Geçersiz seçim. 1–5 arasında bir sayı giriniz.')


if __name__ == '__main__':
    main()
