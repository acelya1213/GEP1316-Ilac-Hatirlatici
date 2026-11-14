# PROMPTLAR.md – Yapay Zekâ Kullanım Günlüğü

**Öğrenci:** Açelya Çayırcı  
**Ders:** GEP1316 Kodlama Okuryazarlığı  
**Proje:** İlaç ve Tedavi Saatleri Hatırlatıcı  
**Kullanılan YZ Aracı:** OpenAI ChatGPT

## 1. Projenin Oluşturulması

**Gerçek istem:** "Bu ödev python dilinde hazırlanacak detaylar zaten yazıyor iyice incele ve bana ilaç tedavi saatleri hatırlatıcı ile ilgili bir şey geliştirmek istiyorum ban kodu hazırla ve ben bunu run yaptığımda çalışmış olsun."

**YZ yanıtı:** Python ile ilaç kullanım saatlerini planlayan bir uygulama için kod oluşturuldu.

**Karar:** Kabul ve değerlendirme.

**Gerekçe:** Proje fikri eczacılık alanımla ilgiliydi ve dersin Python uygulaması geliştirme amacına uygundu.

## 2. Kullanıcı Girişlerinin Doğrulanması

**İncelenen konu:** Hatalı saat ve sayı girişlerinin kontrol edilmesi.

**YZ çözümünün değerlendirilmesi:** `saat_dogrula()` ve `pozitif_sayi_iste()` fonksiyonlarıyla kullanıcı girdilerinin doğrulanması hedeflendi.

**Karar:** Kontrol edilmesi gereken çözüm.

**Gerekçe:** Kullanıcı yanlış bilgi girdiğinde programın beklenmedik şekilde kapanmaması gerekir.

## 3. İlaç Saatlerinin Hesaplanması

**İncelenen konu:** Kullanım aralığına göre ilaç saatlerinin oluşturulması.

**YZ çözümünün değerlendirilmesi:** Python `datetime` ve `timedelta` yapılarının kullanılması.

**Karar:** Kabul edilen tasarım yaklaşımı.

**Gerekçe:** Örneğin 23:00'te başlayan ve 8 saatte bir tekrarlanan kullanımda sonraki saat ertesi gün 07:00 olmalıdır.

## 4. Dosyaya Kayıt İşlemleri

**İncelenen konu:** İlaç planlarının CSV dosyasına kaydedilmesi.

**YZ çözümünün değerlendirilmesi:** Python `csv` modülüyle verilerin saklanması.

**Karar:** Kabul edilen tasarım yaklaşımı.

**Gerekçe:** Program kapatıldığında ilaç planlarının kaybolmaması amaçlanmıştır.

## 5. Test Senaryolarının Değerlendirilmesi

**İncelenen konu:** Normal, hatalı ve uç girdilerin test edilmesi.

**Test örnekleri:**
- 08:30 → Geçerli saat
- 25:99 → Hatalı saat
- Boş saat → Geçersiz giriş
- 08:00 başlangıç, 8 saat aralık → Düzenli kullanım saatleri
- 23:00 başlangıç, 8 saat aralık → Ertesi gün 07:00

**Karar:** Test sonuçlarına göre değerlendirme.

**Gerekçe:** Kodun yalnızca normal girdilerde değil, hatalı ve sınır durumlarında da doğru davranması gerekir.

## 6. Eleştirel Değerlendirme

Projenin en önemli kontrol noktalarından biri gece yarısını geçen saat hesaplamalarıdır. Sadece saat bilgisini kullanmak gün değişiminin gözden kaçmasına neden olabilir.

Bu nedenle tarih ve saat hesaplamalarında `datetime` ve `timedelta` kullanımı önemli bir tasarım tercihidir.

Bu durum, yapay zekâ tarafından oluşturulan kodun test edilmesi gerektiğini göstermektedir.

## 7. Sonuç

Bu projede ChatGPT, Python kodunun oluşturulması ve programlama yapılarının anlaşılması için yardımcı araç olarak kullanılmıştır.

Yapay zekâdan alınan yanıtların doğruluğunun değerlendirilmesi, test edilmesi ve uygulamanın çalışma mantığının anlaşılması önemlidir.

**Not:** Birinci bölümdeki istem gerçek konuşmadan alınmıştır. Diğer bölümler, kodun tasarım ve kontrol konularının özetidir; birebir gönderilmiş ayrı istemler olarak sunulmamıştır.
