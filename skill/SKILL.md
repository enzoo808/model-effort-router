---
name: model-secici
description: >-
  Bir promptu okuyup HEM Claude (Haiku 4.5 / Sonnet 5 / Opus 5 / Opus 4.8 /
  Fable 5.1) HEM Codex/ChatGPT (Luna / Terra / Sol / Sol Ultra) için ayrı ayrı
  model + efor seviyesi önerir, ikisini birlikte tek kısa çıktıda verir.
  "hangi model", "hangi efor", "model seç", "bu prompt için ne kullanayım"
  dendiğinde veya /model-secici çağrıldığında kullan.
---

# Claude & Codex Model / Efor Seçici

Kullanıcının verdiği promptu analiz et, **hem Claude hem Codex/ChatGPT için**
ayrı ayrı hangi model ve hangi efor seviyesiyle çalıştırılması gerektiğini
söyle — ikisi birlikte, tek çıktıda. Promptu **çalıştırma** — sadece
yönlendir. Kullanıcı hangi öneriyi kullanacağına kendisi karar verir, bu
router hiçbir şeyi otomatik başlatmaz.

**Kalibrasyon: iki ayrı abonelik kotası.** Korunan kaynak dolar değil —
Claude'un 5 saatlik penceresi **ve** ChatGPT Plus'ın 3 saatlik ("Instant")
+ haftalık ("Thinking") pencereleri. Asıl tehlike yetersiz model seçmek değil,
*refleks olarak en pahalı modeli seçip kotayı yakmaktır*. Şüphede kalınca
**aşağı** yuvarla.

**Token verimliliği — bunu oku.** Bu skill artık iki ayrı öneri üretiyor, bu
doğal olarak biraz daha fazla iş demek — ama **iki katı değil**. R/D/W/C'yi
**bir kez** hesapla, sonra iki ayrı (kısa) tabloya bak. Adım 0-3'ü zihinde
sessizce çalıştır — her adımı ayrı ayrı yazıya dökme, sadece final iki satırı
üret. Kullanıcı "neden?" demedikçe hiçbir ara adımı gösterme.

**Claude model kadrosu (1 Eylül 2026 itibarıyla):**

| Model | Rol |
|---|---|
| Haiku 4.5 | Hız/hacim uzmanı. Efor desteklemez |
| Sonnet 5 | Günlük iş — hız+zeka dengesi. **Varsayılan başlangıç noktası** |
| **Opus 5** | **Amiral gemisi.** Karmaşık ajanik kod ve kurumsal iş için. Opus 4.8'in yerini aldı |
| Opus 4.8 | Legacy — **yalnızca saldırı amaçlı (offensive) siber güvenlik kapısı için** kalıcı bir rolü var |
| **Fable 5.1** | Frontier ölçek: uzun ufuklu otonomi, aşırı genişlik, **biyoloji-bitişik iş**. Fable 5'in yerini aldı (1 Eyl 2026) — aynı **$10/$50** fiyat, ama cache okuması **¼'ü** ($0.25/MTok); bilgi kesimi Haz 2026 |
| Mythos 5.1 | Fable 5.1 ile **aynı model**, izinli safeguard'lar — **yalnızca Project Glasswing daveti** (doğrulanmış siber-savunmacı / yaşam bilimci; ABD öncelikli). Router yalnızca kullanıcı bu erişimi açıkça belirtirse önerir |

> Opus 4.8 hâlâ "legacy" — Anthropic genel işte Opus 5'e geçmeyi öneriyor.
> Tek kalıcı görevi: **saldırı amaçlı** siber güvenlik isteği işaretlendiğinde
> Fable 5.1'in izinli fallback hedeflerinden biri olması (diğeri Opus 5).
> Router bu yönlendirmeyi atlayıp doğrudan Opus 4.8'i öneriyor.
>
> **Fable 5.1 vs Opus 5 — Anthropic'in çerçevesi:** "Çoğu iş için Opus 5'le
> başla; Opus 5'i `xhigh`/`max` eforda denedin ve zorlu akıl yürütme veya
> uzun-ufuklu ajanik işte hâlâ yetersizse Fable 5.1'e geç." Bu router zaten
> Fable 5.1'i yalnızca frontier-ölçek ve biyoloji kapılarında öneriyor —
> çerçeveyle uyumlu, ek bir kural gerekmiyor.

**Codex/ChatGPT model kadrosu (GPT-5.6 ailesi, 9 Temmuz 2026 itibarıyla):**

| Model | Rol | Claude dengi (kaba benzerlik, eşit performans iddiası değil) |
|---|---|---|
| Luna | Hız/hacim uzmanı, en ucuz tier | Haiku 4.5 |
| Terra | Günlük iş, dengeli — **varsayılan başlangıç noktası** | Sonnet 5 |
| **Sol** | **Amiral gemisi** — kod/bilim/güvenlik | Opus 5 |
| **Sol Ultra** | Sol'un üzerine binen, gerçek zamanlı işbirlikçi çoklu-alt-ajan modu (64'e kadar) | Net dengi yok — Claude'un `ultracode`'undan daha güçlü bir paralellik primitive'i |

> Fable 5.1'in (frontier ölçek + biyoloji-bitişik) Codex tarafında doğrulanmış
> bir dengi **yok**. Saldırı amaçlı siber güvenlik ve biyoloji Ar-Ge
> promptlarında Codex satırı "doğrulanmadı" der, model önermez (bkz. Codex Kolu
> sert kapıları).

> **Kaynak notu:** Bu tablo `openai.com/index/gpt-5-6/`,
> `developers.openai.com/api/docs/guides/reasoning`,
> `learn.chatgpt.com/docs/config-file/config-reference` ile doğrudan doğrulandı
> (5 Ağustos 2026). Kullanıcının verdiği ikincil rapordaki fiyat rakamları
> **eski/yanlıştı** (30 Temmuz'daki indirimi yansıtmıyordu) — bkz.
> `reference.md` §9 "Veri durumu".

---

## Efor seviyeleri (Claude Code `/effort` menüsü)

| Seviye | Ne yapar |
|---|---|
| `low` | Kısa, kapsamı belli, zeka gerektirmeyen işler |
| `medium` | Maliyet duyarlı iş; bir miktar zekadan ödün |
| `high` | **Varsayılan** (efor destekleyen her model) |
| `xhigh` | Daha derin akıl yürütme. 30 dk+ ajanik/kodlama işleri |
| `max` | En derin muhakeme. Azalan getiri riski, aşırı düşünme eğilimi. Oturumluk |
| `ultracode` | `xhigh` + her önemli görev için **dinamik workflow orkestrasyonu**. Oturumluk |

Dört şeyi bil:

1. **`ultracode` bir model efor seviyesi değil, Claude Code ayarıdır.** Modele
   `xhigh` gönderir, üstüne dinamik workflow orkestrasyonu ekler. `/effort
   ultracode` veya `claude --effort ultracode`. Ayar dosyasına yazılamaz.
   **Model kısıtı yok** — `xhigh` destekleyen her modelde çalışır: Fable 5.1,
   Sonnet 5, **Opus 5**, Opus 4.8, Opus 4.7.
2. **Haiku 4.5 efor parametresini desteklemez.** Haiku önerirken efor yazma.
3. **Opus 5'e özel (genel bilgi, bkz. Adım 4 Kural 4):** Anthropic düşük/orta
   eforu "eval'in tuttuğu her yerde normal bir maliyet kontrolü" olarak
   öneriyor — önceki Opus nesillerinde (4.7/4.8) düşük efor gölgede kalan bir
   seçenekti. Bu router Opus 5'i yalnızca `D=3` durumunda önerdiği için kendi
   çıktısında bu hep `xhigh`/`max` demek; ama kullanıcı Opus 5'i elle
   çalıştırırken low/medium'dan çekinmemeli.
4. Efor ölçeği **modele göre kalibre**. Aynı isim farklı modelde farklı değer.

Efor bir token bütçesi değil, davranışsal sinyaldir. "low = 1.024 token" gibi
rakamlar uydurmadır; kullanma.

---

## Adım 0 — Prompt kalite kapısı

**Bu adımı atlama.** Skorlamaya geçmeden önce şu dört kontrolü sırayla çalıştır.
"Başarı kriteri/kapsam var mı" diye tek bir soru sormak yetmez — çoğu gerçek
prompt kapsam içerir ama içinde fark edilmeyen bir belirsizlik taşır.
Herhangi biri "evet" ise **model önerme**, önce netleştir.

1. **Örnekle anlatılan ama genellenmemiş bir kural var mı?** Prompt "mesela
   şöyle olursa böyle olur" diyor ama genel formülü/yüzdeyi/eşiği söylemiyor mu?
   > "1000 üretimin 500'ü aynı güne yansır" — bu %50 mi, sabit 500 mü, üretim
   > saatine göre bir kesim mi? **Örnek, genel kuralın yerine geçmez.**
2. **Yanlış varsayım sessizce yanlış sonuç üretir mi?** Kod hatasız çalışır
   ama gerçek veride sistematik olarak yanlış hesaplar mı? (Çökme değil, sessiz
   yanlışlık — fark edilmesi en uzun süren ve en tehlikeli tür.)
3. **Hedef somut mu?** "Sistemde şöyle yapacağız" demek *hangi sorgu/servis/
   tablo/dosya* olduğunu söylemiyor. Kapsam varmış gibi görünür ama değildir.
4. **Aynı prompttan iki makul ama farklı implementasyon çıkar mı?** Çıkıyorsa
   hangisinin istendiği belirsizdir — sen (router) hangisini seçtiğini fark
   etmeden bir varsayım yapıyor olabilirsin.

Netleştirirken **"belirsiz" deyip geçme** — tam olarak neyin eksik olduğunu
somut biçimde sor:

> "Şu kodu düzelt" → *Hangi kod? Neye göre bozuk? Nasıl anlarız düzeldiğini?*
> "1000 üretimin 500'ü aynı güne yansısın" → *Bu her zaman sabit 500 mü, yoksa
> üretimin bir yüzdesi mi (örn. %50)? Yoksa üretim saatine göre mi belirleniyor
> (örn. 14:00 öncesi aynı gün)? Bu, hesaplama mantığını tamamen değiştirir —
> R/D skorunu da etkiler.*

Belirsiz promptu en pahalı modele göndermek saf kota israfıdır — model bağlamı
tahmin etmeye çalışır, yanlış tahmin eder, iş baştan yapılır. Daha kötüsü: (2)
maddesindeki gibi sessizce yanlış çalışan bir kod üretilirse, hatanın fark
edilmesi haftalar sürebilir.

---

## Adım 1 — Sert kapılar (Claude tarafı)

Sırayla kontrol et. İki tür kapı var — karıştırma:

- **Belirleyici kapı** (satır 1-3, 5): **hangi model** olduğunu tek başına
  karara bağlar, Adım 2/3'ün model-seçim mantığını **atlatır**. Ama bu, W/süre
  gibi efor-değiştirici sinyalleri (ör. `ultracode` uygunluğu) değerlendirmeyi
  atlatmaz — onlar model seçiminden ayrı, gate sonrası da kontrol edilir (bkz.
  "Neden siber güvenlik" altındaki not).
- **Eleyici kapı** (satır 4, bağlam>200k): sadece bir adayı **listeden çıkarır**
  (Haiku), hangi model olacağına karar vermez — Adım 2/3 skorlaması kalan
  adaylar (Sonnet 5/Opus 5/Fable 5.1) arasından normal şekilde çalışır.

| Koşul | Tür | Sonuç |
|---|---|---|
| Saniye altı gecikme **veya** yüksek hacimli sınıflandırma/ayrıştırma | Belirleyici | **Haiku 4.5.** Efor yok. Dur, bitti |
| **Saldırı amaçlı siber güvenlik:** exploit üretimi, sızma testi, ikili (binary) tabanlı zafiyet taraması | Belirleyici | **Opus 4.8**, **efor tabanı `xhigh`** (W/süre sinyalleri hâlâ değerlendirilir → `ultracode`'a çıkabilir, bkz. altındaki not) — Glasswing erişimi varsa **Mythos 5.1** |
| **Biyoloji-bitişik Ar-Ge:** genomik, protein/kimya ağırlıklı pipeline, biyo-CTF | Belirleyici | **Fable 5.1** (bkz. not aşağıda) |
| Bağlam 200k token'ı aşıyor | **Eleyici** | **Haiku 4.5 elenir**, Adım 2/3 kalan adaylarla normal çalışır |
| **1000+ dosya / tüm kod tabanı ölçeğinde** (frontier ölçek) | Belirleyici | **Fable 5.1** |

> **Savunma amaçlı güvenlik işi bu kapıyı tetiklemez.** "Bu kodu/altyapıyı
> zafiyet için denetle", "açık portları bul", "güvenlik grubu kurallarını
> gözden geçir" — exploit üretmeyen savunma işidir. Fable 5.1 bunu 1 Eyl
> 2026'dan beri **kendisi yapabiliyor** (Fable 5'te bloktu); normal skorlamaya
> girer (genelde Sonnet 5 · `xhigh` veya Opus 5). Yalnızca yukarıdaki üç
> saldırı-amaçlı kategori kapıyı tetikler.

> **Frontier-ölçek kapısı — tek sinyal yeterli.** Bu kapı "binlerce dosya **VE**
> eşzamanlı 1M bağlam doldurma **VE** kalıcı bellek" gibi üç ayrı şart aramaz —
> **sadece dosya/kapsam sayısı** (1000+) yeterli tetikleyicidir. Bu ölçekte bir
> işi anlamak zaten eşzamanlı 1M bağlam doldurmayı ve çok-oturumlu kalıcı
> belleği **gerektirir**; prompt bunu ayrıca belirtmez, belirtmesi beklenmez.
> ✅ "4000 dosyalık legacy monolitini modüllere ayır" — sadece dosya sayısı
> (4000) yazıyor, "eşzamanlı bağlam" veya "kalıcı bellek" hiç geçmiyor, yine de
> kapı tetiklenir → **Fable 5.1**.
> **Adım 2'nin `W=3` eşiğiyle (100+ dosya) karışma:** 100-999 dosya bu kapıyı
> tetiklemez, normal skorlamaya girer (`W=3`, model Adım 3'e göre — genelde
> Opus 5 veya `opusplan`). Bu kapı yalnızca gerçekten binler mertebesinde
> (1000+) tetiklenir.

### Neden saldırı amaçlı siber güvenlik → doğrudan Opus 4.8

Fable 5.1, Opus 5, Sonnet 5'in **kendi** güvenlik sınıflandırıcıları var.
Saldırı amaçlı (exploit üretimi, sızma testi, ikili-tabanlı zafiyet taraması)
bir istek işaretlenince Fable 5.1'in izinli fallback hedefleri **Opus 4.8 ve
Opus 5**. Router bu dolambacı atlar, doğrudan **Opus 4.8**'i önerir (cyber
duruşu en izinli genel model; Opus 5 de geçerli hedef). Sonnet 5'i önerme —
exploit üretiminden bilinçli yalıtılmış (Firefox 147'de çalışan exploit oranı %0).

Fable 5.1 ile Fable 5'e göre değişen: (a) savunma amaçlı zafiyet keşfi artık
**bloklanmıyor** — Fable 5.1 kendisi yapıyor (yukarıdaki kapı notu), (b) selim
isteklerde cyber müdahaleleri oturum başına **~%60 azaldı**.

> **Doğrulanmış savunmacılar için Mythos 5.1.** Cyber Verification Program /
> Project Glasswing'e kabul edilmiş savunma güvenliği ekipleri izinli
> safeguard'larla **Mythos 5.1** (`claude-mythos-5-1`) kullanabilir — ama
> **yalnızca davet**, ABD öncelikli. Kullanıcı bu erişimi belirtmezse router'ın
> önerisi **Opus 4.8** kalır; belirtirse `Claude: Mythos 5.1 · efor: xhigh` öner.

**Efor tabanı `xhigh`'ın üzerine `ultracode` hâlâ çıkabilir.** Bu kapı
"belirleyici" olsa da sadece **modeli** karara bağlıyor — Adım 2/3'ün W/süre
sinyallerini değerlendirmesini atlatmıyor. Kapı ateşlendikten **sonra** normal
şekilde `W=3 ∧ süre>30dk ∧ ¬(D=3∧R=3)` kontrol et; sağlanıyorsa efor `xhigh`
değil **`ultracode`** olur (bkz. Çıktı formatı'ndaki "180 servislik sızma testi" örneği).

### Neden biyoloji-bitişik → Fable 5.1 (Opus 5 değil)

Selim/eğitim amaçlı biyoloji-tıp sorularında safeguard'lar artık **%85 daha az**
tetikleniyor — bunlar kapı değil, normal skorlamaya girer. Kapı yalnızca
**Ar-Ge yoğun** biyoloji-bitişik iş için:
- **Fable 5.1** → Ar-Ge-işaretli kısımlar otomatik **Opus modellerine** yönlenir
  (beklenen davranış, hata değil)
- **Opus 5** → biyoloji Ar-Ge'de **hiç fallback yok, doğrudan reddeder**

Yani Opus 5'i doğrudan önerirsen kullanıcı düz bir refuse mesajıyla karşılaşabilir.
Fable 5.1'i öner. Life Sciences Verification Program'a kabul edilmiş
araştırmacılar profesyonel Ar-Ge için **Mythos 5.1** kullanır (yalnızca davet,
ABD öncelikli) — kullanıcı bu erişimi belirtirse Mythos 5.1 öner.

**Fable 5.1'e efor tabanı koyma.** Varsayılanı `high`; Fable 5'e göre kazanç en
çok yüksek eforda ama düşük eforda da güçlü. Not: Fable 5.1 `low` eforda
arama/getirme araçlarını daha seyrek çağırır — taze bilgi gereken işte eforu
yükselt.

---

## Adım 2 — Dört eksende 0–3 puanla

Tek satırlık sıfat ("karmaşık", "çok adımlı") kararsız kalır. Her eksen için
**önce teşhis sorusunu sor**, sonra seviyeye bak. Kararsızsan `reference.md`
§8'deki örnek kütüphanesinden en yakın analojiyi bul.

### R — Risk / geri dönülemezlik

*Teşhis: Çıktı yanlışsa düzeltmek dakikalar mı sürer, günler mi? Otomatik geri
alma var mı (git revert, feature flag, rollback)? Kaç kullanıcı/sistem etkilenir?
Para/sağlık/hukuk/itibar riski var mı?*

`0` Atılabilir taslak — hiç kullanılmasa da kayıp yok (fikir, alternatif, keşif)
`1` Kullanılacak ama bir insan gözden geçirip onaylayacak (PR, taslak e-posta)
`2` Doğrudan gerçek sisteme gidecek ama geri alınabilir (izole tek satır config, feature-flag'li deploy, tersinir migration) — **mimari/çok-servisli olması tek başına R=3 yapmaz**, ama **sistem-geneli davranışı yöneten tek satır da otomatik R=2 sayılmaz**, bkz. notlar
`3` Geri dönüşü yok/çok maliyetli — veri kaybı riski, tersinmez migration, dışarı giden mesaj/ödeme, geri alınamaz/orantısız maliyetli mimari karar, tıbbi/hukuki/finansal tavsiye, canlı kullanıcı verisine dokunma

> **"Mimari karar" etiketi tek başına R=3 yapmaz.** Asıl soru geri
> alınabilirlik: yeni bileşen servis-servis / feature-flag'li / kademeli
> olarak devreye alınabiliyor ve sorun çıkarsa durdurulup geri sarılabiliyorsa,
> **mimari olsa bile R=2**'dir. R=3 iki durumda geçerli: (a) gerçek bir
> rollback mekanizması yok (canlı veri şeması migrasyonu, tersinmez veri
> dönüşümü), **veya** (b) tasarlanan şey tüm sistemin bağımlı olduğu **merkezi/
> paylaşılan** bir çekirdek (kimlik/auth altyapısı, veri modeli, trust
> boundary) — burada geri dönüş "hangi bileşeni kapatayım" sorusu değil, onlarca
> servisin çoktan bağımlı hale geldiği paylaşılan bir kararı sökme sorunudur.
> ✅ R=2: "40 mikroservisi ortak bir auth middleware'e geçir" — her servis
> kendi middleware'ini **bağımsız** kullanır, servis-servis aşamalı geçiş ve
> rollback mümkün; mimari ama tersinir.
> ❌ R=3: "Prod'daki 200 servisin auth mimarisini baştan tasarla" — burada
>
> **Büyük ayrıştırma — modül mü, servis mi:** "monoliti **modüllere** ayır"
> = iç refactor, kademeli/strangler-fig ile tersinir → **R=2** (bkz. doğrulama
> id 8, `Fable 5.1 · ultracode`). "Ayrı **servislere / süreçlere** böl" = ağ +
> veri sahipliği + deploy topolojisi sınırı getirir; bir kez servisler
> birbirine bağımlı hale geldiğinde geri birleştirmek orantısız pahalı → **R=3**
> (kriter b: paylaşılan çekirdek). Frontier kapısı model'i (Fable 5.1) her iki
> durumda da belirler, ama efor değişir: R=2 → `ultracode`, R=3∧D=3 → `max`.
> tasarlanan şey 200 servisin **ortak bağımlı olduğu tek, merkezi** bir kimlik/
> yetkilendirme altyapısı (token şeması, trust boundary); servis-servis
> aşamalı devreye alma bunu tersinir yapmaz, çünkü tasarım kararının kendisi
> paylaşılan ve servisler ona bağımlı hale geldikçe sökülmesi orantısız
> pahalılaşan bir şey — gerçek R=3.

> **Önce şunu ayır: kod tabanında bir değişiklik mi, yoksa canlı/operasyonel
> bir değer mi?** Normal kod tabanı değişikliği (bileşen rengi, metin, CSS,
> herhangi bir kaynak kod satırı) **varsayılan olarak R=1**'dir — mühendislik
> akışının normali PR ile gözden geçirilip öyle deploy edilmesidir (R=1'in
> kendi tanımı zaten bu). **R=2/R=3 sadece prompt açıkça canlı sisteme
> doğrudan, kod-incelemesi olmadan giden bir değeri işaret ediyorsa** devreye
> girer — prod config dosyası, canlı bir yönetim paneli, feature-flag
> anahtarı, veritabanında saklanan bir ayar. "Ayarlar sayfasının varsayılan
> temasını değiştir" gibi belirsiz bir ifade **kod tabanı değişikliği
> varsayılır** → R=1, aksini belirten bir sinyal yoksa.
>
> Doğrudan-operasyonel bir değer için de **"tek satır config" tek başına
> R=2 yapmaz.** Asıl soru satırın **kod uzunluğu değil, etki genişliği**:
> geri almak teknik olarak anlık olsa bile, **deploy ile fark edilme
> arasındaki pencerede** kaç sistem/kullanıcı etkileniyor? İzole bir
> operasyonel değeri değiştiriyorsan (tek bir feature-flag varsayılanı) R=2.
> Ama satır **sistem-geneli davranışı** yönetiyorsa (retry sayısı, timeout,
> rate limit, connection pool boyutu) ve yanlış değer insan fark etmeden
> **kademeli bir kesintiye** (retry storm, bağlantı tükenmesi) yol
> açabiliyorsa, tek satır olsa bile R=3.
> ✅ R=3 örneği: "Prod config'inde `MAX_RETRIES`'ı 3'ten 5'e çek" — "prod
> config'inde" açıkça canlı/operasyonel bir değeri işaret ediyor, kod
> incelemesinden geçmiyor; retry sayısı sistem-geneli yük/dayanıklılık
> davranışını yönetiyor → gerçek R=3.
> ❌ R=1 karşılaştırma: "Ayarlar sayfasındaki varsayılan tema rengini
> (bileşen kodunda) değiştir" — normal bir kod değişikliği, PR'dan geçer;
> canlıya doğrudan gitme sinyali yok → R=1, Haiku/Luna için engel değil.

### D — Derinlik

*Teşhis: Bunun bilinen/standart bir çözüm kalıbı var mı, yoksa sıfırdan mı
düşünülmeli? Kaç farklı yaklaşım arasında seçim yapılıyor? Deneme-hatayla mı
yoksa tek seferde doğru tasarımla mı çözülüyor?*

Alan farklı anlama gelir — kodlamaya göre değil, **işin türüne göre** bak:

| Seviye | Kodlama | Yazı/analiz | Araştırma | Veri |
|---|---|---|---|---|
| `0` | Örüntü eşleştirme, bilinen sabiti hatırlama; **tam belirtilmiş additive şema değişikliği** (sütun adı + tip + nullable hepsi verilmiş — tasarım kararı yok) | Tek cümlelik yanıt **veya** içerik değişmeden salt biçim/ton değişikliği (uzunluk önemsiz — 3 paragraf da olsa, hiçbir seçim/kısaltma/sentez yoksa D=0) | Tek kaynak arama | Tek sayıyı okuma |
| `1` | Standart kalıp (CRUD, bilinen bug deseni); şema değişikliği ama bir seçim var (index tipi, geriye-dolum stratejisi, kısıt) | Basit özet/taslak | Tek kaynak özeti | Basit filtre/agregasyon |
| `2` | Çok adımlı ama iyi belgelenmiş özellik | Çok kaynaklı senteze dayalı rapor | Çoklu kaynak sentezi | İstatistiksel çıkarım |
| `3` | Sıfırdan tasarım, eşzamanlılık, algoritmik karmaşıklık, çelişen kısıtları dengeleme | Orijinal argüman kurma, çelişen kaynakları uzlaştırma | Yeni hipotez/çerçeve üretme | Modelleme, nedensel çıkarım |

> **D=1 / D=2 sınırı — "iyi belgelenmiş" tek başına D=2 yapmaz.** Asıl soru:
> kaç **bağımsız tasarım kararı** sende (uygulayanda) kalıyor? Tarif/kütüphane/
> tutorial takip ediliyorsa ve tek bir makul yaklaşım varsa → D=1, kalıp
> "standart" olması onu D=2'ye taşımaz. Birden fazla makul yaklaşım arasında
> seçim yapman gerekiyorsa (ve seçim sonucu etkiliyorsa) → D=2.
> ✅ D=1: "Bu API'ye cursor-based pagination ekle" — yaygın, iyi belgelenmiş
>    tek bir kalıp; kütüphane/tutorial takip edilir, tasarım kararı yok.
> ❌ D=2: "Bu API'ye hem cursor hem offset pagination'ı geriye-uyumlu şekilde
>    ekle, hangisinin ne zaman kullanılacağına karar ver" — gerçek bir seçim
>    var (iki yaklaşım + geriye-uyumluluk kısıtı).
>
> **Şüphede kalınca D=1'de kal, D=2'ye zorlama** — "bu bir liner'dan fazla"
> hissi D=2 için yeterli gerekçe değil, kota-bilinçli varsayılan aşağı
> yuvarlamaktır (bkz. kalibrasyon notu).

### W — Genişlik

*Teşhis: Kaç dosya/belge okunacak veya değişecek? İşin parçaları birbirinden
bağımsız (paralelleştirilebilir) mi, yoksa sıralı mı?*

`0` Tek dosya/belge
`1` 2–5 dosya, tek modül içinde
`2` **6–99 dosya/birim** (bir alt-sistem geneli, birçok servise tekrarlanan aynı küçük değişiklik dahil) **veya** 2–3 farklı doğrulama açısı (örn. doğruluk + performans)
`3` **100+ dosya** / tüm kod tabanı **veya** 3+ bağımsız, paralelleştirilebilir doğrulama açısı (örn. güvenlik + performans + stil + test-coverage birlikte)

> **W=2 / W=3 eşiği sayısaldır — 100.** "60 mikroservise aynı endpoint'i ekle"
> kulağa büyük gelir ama 60 < 100 → **W=2**, W=3 değil. `ultracode` W=3
> gerektirir, dolayısıyla 20–99 birimlik tekrarlı mekanik iş `ultracode`'a
> **çıkmaz** (efor D'yi takip eder). Gerçekten 100+ dosya veya 3+ bağımsız
> doğrulama açısı varsa W=3.

### C — Bağlam sentezi

*Teşhis: Model kendi bilgisiyle mi yeterli, yoksa dışarıdan (dosya, doküman,
sohbet geçmişi) ne kadar okuması gerekiyor?*

`0` Kendi kendine yeter, ekstra referans gerekmiyor
`1` Birkaç küçük dosya/doküman
`2` Orta ölçekli kod tabanı/dokümantasyon (birkaç bin satır, bir README + birkaç modül)
`3` Büyük külliyat (yüzlerce sayfa doküman, devasa kod tabanı, uzun sohbet geçmişi) sentezi

---

## Adım 3 — Eşleme

Model seçimi **zeka ihtiyacına** (D, C) dayanır — risk (R) modeli değil,
insan gözetimini yükseltir. Bu ayrım önemli: eski tasarımda R doğrudan modeli
Opus'a zorluyor, sonra ayrı bir kuralla geri indiriliyordu. Artık R modeli
etkilemiyor, sadece "insan onayı" notu ve efor tabanını etkiliyor.

**Model** ← `max(D, C)`. Önemli: **Opus 5 yalnızca `D=3` ise** aday olur —
`C=3` tek başına (D düşükken büyük bağlam sentezi) Opus 5'i tetiklemez, Sonnet
5'te kalır. Sebep: Opus 5'in gerekçesi derin akıl yürütme ihtiyacı; büyük ama
sığ bir sentez işi Sonnet 5'in 1M bağlam penceresiyle zaten çözülür.

| Koşul | Model |
|---|---|
| `D = 0` **∧** `W=0` **∧** `C≤1` **∧** `R≤1` | **Haiku 4.5** |
| Yukarıdaki koşul sağlanmıyor ve `max(D,C) ≤ 1` | Sonnet 5 |
| `max(D,C) = 2` | Sonnet 5 |
| `max(D,C) = 3`, ama `D<3` (yani `C=3` tetikledi) | **Sonnet 5** — büyük bağlam, sığ akıl yürütme |
| `max(D,C) = 3`, `D=3` | **Opus 5** — eğer görev ajanik çok adımlı kod / matematik-ispat / araçsız derin akıl yürütmeyse (Kural 2). **Değilse Sonnet 5** (kota-bilinçli varsayılan — bkz. Kural 3) |

**Haiku neden sadece D=0'da:** D=1 "bilinen kalıp" demek — N+1 sorgu düzeltmesi,
standart input validasyonu, bilinen bug deseni. Bunlar örüntü eşleştirme değil,
gerçek yargı gerektiriyor. `max(D,C)≤1` iken D=1 ise taban Sonnet 5'tir, Haiku
değil. Haiku sadece D=0 (gerçekten trivial — typo, tek satır ifade değişikliği,
bilinen bir sabiti hatırlama) durumunda uygun.

**R eşiği neden 1, 3 değil:** `R=2` demek "prod'a gidecek ama geri alınabilir" —
bu hâlâ gerçek bir prod değişikliği, Haiku'nun hız/hacim profiline bırakılacak
kadar önemsiz değil. Haiku'yu sadece atılabilir taslak/gözden geçirilecek
işlere (`R≤1`) ayır; `R=2` en az Sonnet 5 ister.

**R tabanı (genel):** `R = 3` ise Haiku hiçbir zaman seçilmez, taban Sonnet 5'tir —
basit ama geri alınamaz işi en zayıf modele bırakma. Ayrıca `R=3` her zaman
çıktıya insan onayı notu ekletir (Adım 4, Kural 1).

**Efor** ← `D` — **modelden bağımsız, her zaman bu tabloyla.** Hangi model
seçildiyse seçilsin (Opus 5 dahil), efor D'yi takip eder. Model tablosundaki
"xhigh" gibi ifadeler efor tablosunun D=3 satırıyla **çakışmaz**, sadece D=3
durumunda ne olacağını hatırlatır.

| D | Efor |
|---|---|
| 0 | `low` |
| 1 | `medium` |
| 2 | `high` |
| 3 | `xhigh` |
| 3 ∧ R=3 | `max` |

Haiku 4.5 seçildiyse efor alanını boş bırak — model bu parametreyi desteklemiyor.

**Sonuç:** Opus 5 bu router'da **her zaman D=3 ile birlikte çıkar** (`xhigh`
veya `max`) — asla `low`/`medium` ile önerilmez, çünkü Opus 5 zaten sadece D=3
durumunda seçiliyor. Bu, Adım 0'daki "Opus 5'te low/medium'u gölgede tutma"
notuyla çelişmiyor: o not router'ın **kendi önerisi** için değil, kullanıcının
Opus 5'i **elle** çalıştırırken (`/effort` ile) bilmesi gereken genel bilgi.
Router zaten D=3 olmayan hiçbir işte Opus 5 önermiyor.

**`ultracode`** ⇔ üçü birden doğruysa:
`W = 3` **∧** tahmini süre > 30 dk **∧** `¬(D=3 ∧ R=3)`

`ultracode` modele `xhigh` gönderir. Efor alanına `xhigh` değil, **`ultracode`**
yaz. Model kısıtı yok — Haiku hariç her modelde çalışır (Sonnet 5, Opus 5,
Opus 4.8, Fable 5.1 dahil); model **ne şekilde belirlendiyse** (Adım 3 skorlaması
**veya** Adım 1'in belirleyici kapısı — ör. siber güvenlik → Opus 4.8) onun
üzerinde çalışır. `ultracode` model seçiminin bir parçası değil, seçilmiş
modelin üzerine binen bağımsız bir efor-değiştirici — bu yüzden Adım 1 kapısı
"skorlamayı ezse" bile W/süre kontrolü ayrıca yapılır.

> **Çakışma çözümü.** `D=3 ∧ R=3` ise efor `max`, `ultracode` **hayır**.
> `ultracode` yalnızca `xhigh` gönderir; `max`'ın derinliğini kaybedersin.
> Üstelik geri alınamaz bir işi paralel workflow'lara dağıtmak denetimi
> zorlaştırır. Derinlik → `max`. Genişlik → `ultracode`.

### `opusplan` — plan/yürütme model ayrımı

**Sadece Claude Code'da var, Claude.ai'da yok.** `/model opusplan`: plan modunda
`opus` (→ Opus 5), yürütme modunda otomatik `sonnet`'e (→ Sonnet 5) geçer.
Amaç: mimari kararı pahalı modelle ver, hacimli mekanik uygulamayı ucuz modelle
yap — tek modeli baştan sona koşturmaktan daha az token.

**`opusplan`** ⇔ üçü birden doğruysa (Adım 3'ün `Opus 5` dalını **geçersiz kılar**):

1. `max(D,C)=3 ∧ D=3` **∧** görev Kural 2(a) alanına giriyor (yapılandırılmış
   tasarım/mimari)
2. **Zorluk plana ön-yükleniyor.** Teşhis: *plan tamamlandıktan sonra, yürütme
   adımlarının çoğu birbirine benzeyen/tekrar eden bir kalıbı mı takip
   ediyor?* Evetse ön-yüklü. Karşıt durum — zorluk yürütme boyunca sürüyor:
   debug (gerçek neden koda bakmadan bilinmez), formel ispat (ispatın kendisi
   hem plan hem yürütme, ayrılamaz), yeni algoritma tasarımı (tasarım=yürütme).
   Bu durumda `opusplan` **önerme**, düz Opus 5 kalır.

   > **Yürütüm fiili yazılı olmayabilir — hedef kapsam sayısı yeterli sinyal.**
   > Prompt "uygula/geçir/yay" gibi bir yürütüm fiili içermese bile, tasarımın
   > **hedef kapsamı sayıyla somutlaşmışsa** ("200 servisin X'ini tasarla",
   > "40 mikroservisin Y'sini belirle"), bu sayı yürütüm fazının zaten var
   > olduğunu ima eder — bir tasarımın "kaç sisteme uygulanacağı" belirtiliyorsa,
   > uygulanmayacak olması anlamsız olurdu. Sadece "tasarla" kelimesi tek
   > başına ön-yükleme sinyalini geçersiz kılmaz.
   > ✅ "Prod'daki 200 servisin auth mimarisini baştan tasarla" — fiil sadece
   > "tasarla", ama hedef "200 servis" diye somut; yürütüm (200 servise
   > uygulama) ima ediliyor → ön-yüklü, `opusplan` adayı.
3. `W ≥ 2` — yeterli uygulama hacmi var ki mod değişimi karşılığını versin.
   `W≤1`'lik küçük bir karar için mod değişimi sadece ek yük, düz Opus 5 yeterli.

> ✅ "40 mikroservisi yeni bir auth middleware'e geçir; tasarımı bir kez
>    belirle, her serviste aynı kalıbı uygula" — middleware tasarımı ön-yüklü,
>    40 servise tekrarlanan kalıp = mekanik yürütme, W=3.
> ❌ "Prod'da ara sıra düşen race condition'ı bul" — zorluk yürütme boyunca
>    sürüyor (kod okumadan neden bilinmez), düz Opus 5 · max kalır.
> ❌ "Bu router'ın model seçimini riskten ayrıştır" — W=1, hacim yetersiz;
>    üstelik yürütme de yargı gerektiriyordu (bu oturumda canlı test edildi,
>    plan tek seferde mekanikleşmedi), düz Opus 5 kalır.

**Çıktı formatı (`Claude:` etiketinin altında, uyarı ayrı satır olarak
eklenir — Codex satırı bundan etkilenmez, kendi normal eşlemesinden gelir):**
```
Claude: opusplan · plan: <efor> · uygulama: <efor>
```
Plan eforu = Kural 2(a)'nın normal sonucu (`xhigh`, `R=3` ise `max`).
Uygulama eforu = plan-sonrası tahmini D'ye göre (genelde `medium`, nadiren `high`).

> ⚠️ **Efor otomatik geçmez.** Opus 5 ve Sonnet 5'in ikisi de "hold"suz —
> plan modunda ayarladığın efor, yürütmeye geçince **aynen kalır**, otomatik
> düşmez. Yürütme moduna geçtiğinde `/effort <uygulama eforu>` ile elle
> ayarlaman gerekiyor; atlarsan Sonnet 5 gereksiz yere pahalı efor koşar ve
> `opusplan`'ın kota tasarrufu amacı boşa çıkar.

Bu uyarı **her `opusplan` çıktısına** ikinci satır olarak eklenir — Çıktı
formatı bölümündeki iki mandatory istisnadan biri budur, "sadece sorulunca
açıkla" kuralının dışındadır.

**Gelişmiş kombinasyon (doğrulanmamış, opsiyonel öneri — çıktıya EKLENMEZ).**
`W=3` ise, yürütme fazında Sonnet 5 üzerinde `ultracode` da düşünülebilir
(devasa migration'ı paralel uygula). Bu kombinasyon resmî dokümanda test
edilmemiş; mandatory-istisna listesinde değil, yani varsayılan çıktıya
girmez — kullanıcı "başka ne yapabilirim/neden?" diye sorarsa, "dene, işe
yaramazsa düz `high`'a dön" notuyla öner, kesin tavsiye olarak sunma.

---

## Adım 4 — Kota koruma ve doğruluk kuralları

**1. R=3 → insan onayı notu.**
İş geri alınamazsa (prod migration, mimari karar, tıbbi/hukuki/finansal),
model/efor Adım 3'ten geldiği gibi kalır ama çıktıya "insan onayı olmadan
uygulama" notu eklenir. Basit-ama-riskli işlerde (D≤1) bu tek başına yeterli
uyarı; modeli yükseltmeye gerek yok.

**2. Şu üç alanda Opus 5'i tercih et (Kural 2 alanları).**
Bu üçü Opus 4.8 döneminden kalan, kısmen doğrulanmış bir örüntü — Opus 5'in
kendi granüler sayıları (SWE-bench Pro / Terminal-Bench / HLE) ayrı
yayınlanmadı, ama Opus 5'in Opus 4.8'e göre genel sıçraması (Frontier-Bench'te
2 katından fazla, GDPval-AA/OSWorld'de liderlik) bu üç alanda da en az aynı
yönde bir avantaj olduğunu güçlü şekilde işaret ediyor:
**a) Ajanik çok adımlı yapılandırılmış iş** — çoklu dosya, sıfırdan mimari
tasarım, büyük refactor/migration; D=3 gerektiren gerçek bir tasarım kararı
var. **Programlama diliyle sınırlı değil** — kural motoru/karar ağacı tasarımı,
sistem/prompt mimarisi, çakışan kısıtları dengeleyen herhangi bir yapılandırılmış
sistem de girer (örn. bir skill'in kendi karar mantığını sıfırdan tasarlamak).
> ✅ "Bu servisi event-driven mimariye taşı, mesaj sırası ve idempotency dahil"
> ✅ "Bu router'ın model seçimini riskten ayrıştır, çakışma kurallarını tasarla"
> ❌ "Bu tek dosyadaki bug'ı düzelt" — dosya sayısı önemli değil, D genelde 1-2'dir

**b) Matematik / formel ispat** — algoritmik karmaşıklık analizi, correctness
kanıtı, sayısal optimizasyon.
> ✅ "Bu algoritmanın en kötü durum karmaşıklığını kanıtla ve daha iyisini bul"
> ❌ "Şu ortalamayı/yüzdeyi hesapla" — aritmetik D=0-1'dir, matematik D=3 değil

**c) Araçsız derin akıl yürütme** — model **hiçbir araç çağırmadan** (dosya
okuma, kod çalıştırma, arama yok), sadece promptun içeriğiyle derin bir
analiz/karar üretmesi gerekiyor.
> ✅ "Kod çalıştırmadan, şu iki mimari yaklaşımın trade-off'larını tartış"
> ❌ Claude Code içinde çalışan herhangi bir görev — dosya okuma/test çalıştırma
>    zaten "araçlı" sayılır, bu istisnaya girmez (aşağıdaki not bunu açıklıyor)

> **Araç erişimi kararı çevirir.** Sonnet 5'in ham zeka açığı araç
> orkestrasyonuyla kapanma eğiliminde (Opus 4.8 dönemi verisi: araçsız HLE'de
> Opus +6.6 önde, araç verilince parite). Görev Claude Code / web araması /
> kod çalıştırma içeriyorsa Sonnet 5 genelde yeter. Saf bağlamdan ispat/analiz
> isteniyorsa Opus 5'e çık. **Pratik sonuç:** Claude Code oturumunda çalışan
> işlerin büyük çoğunluğu zaten "araçlı" — bu yüzden (c) alt-kuralı nadiren
> tetiklenir; asıl sık tetiklenen (a) ve (b)'dir.

**3. D=3 ama Kural 2'ye girmiyorsa → varsayılan Sonnet 5 · xhigh (kota gerekçesi).**
Anthropic'in kendi eşit-efor kıyası hâlâ yok, ama **LiveBench 2026-06-25**
(bağımsız, kontaminasyon-serbest) Opus 5'i Sonnet 5'in üstünde gösteriyor:
agentic coding +5.8, language +13.7, reasoning +2.5, math +2.8 (bkz. `reference.md`
§2.1). Router yine de kota gerekçesiyle ucuz tarafı (Sonnet 5) varsayılan tutuyor
— Opus 5'in $/başarılı-görev'i LiveBench'te Sonnet 5'inkinin ~1.4×'i, fark her
işi haklı çıkarmıyor. Ama:

> ⚠️ Yükselt: sonuç yetersizse veya iş kritikse → Opus 5 · xhigh. Artık kanıtsız
>   değil — LiveBench'te Opus 5 bu eksende Sonnet 5'in belirgin önünde, özellikle
>   language/muhakeme ağırlıklı D=3 işlerde.

**4. Kullanıcı bilgisi (router çıktısını değiştirmez): Opus 5'te low/medium
"israf" değildir.** Anthropic'in Opus 5'e özel tavsiyesi: `high`'dan
(varsayılan) başla, kodlama/ajanik işte `xhigh`'a çık, **ve eval'in tuttuğu
her yerde low/medium'u maliyet kontrolü için serbestçe kullan.** Bu, Opus
4.7/4.8'in "düşük eforda israf" çerçevesinden kasıtlı bir sapma.

Bu router Opus 5'i zaten sadece `D=3` durumunda öneriyor (→ efor `xhigh`/`max`),
yani kendi çıktısında Opus 5'i hiç `low`/`medium` ile önermeyecek — o kombinasyon
mantıken oluşmuyor. Bu not, kullanıcı router'ın önerisinin **üzerine** kendi
kararıyla Opus 5'i düşük eforla çalıştırmak isterse "bu israf değil" bilgisini
vermek için var, router'ın kendi kararı için değil.

**5. 30 dakikanın altındaki işte `ultracode` önerme.**
Her önemli görev için workflow planlar; gündelik işte gecikme ve kota ekler,
kalite eklemez. Tek seferlik derin düşünme istiyorsan **prompt içine `ultrathink`
yaz** — efor seviyesini değiştirmeden o tur için derinlik ekler.

**6. Uzun oturum uyarısı.** MCP sunucuları bağlıysa hatırlat: her sunucu araç
şemalarını her mesaja enjekte eder. Yük sunucu başına sabit değil, **araç
sayısıyla orantılı** (GitHub MCP: 27 araç ≈ 18k token; Playwright: 21 araç
≈ 13.6k). Kullanılmayanları kapat.

**7. Auto-accept uyarısı.** R≥2 ise auto-accept'i kapatmayı öner — zincirleme
düzenlemeler hem kotayı geometrik yakar hem geri dönüşü zorlaştırır.

**8. Alias güvenliği.** Kullanıcı `/model opus` yazdığında Claude Code
v2.1.219+ ise bu **Opus 5**'e çözülür; daha eski sürümde Opus 4.8'e düşebilir.
Router "Opus 5" önerdiğinde ve kullanıcı hâlâ Opus 4.8 görüyorsa, `claude
update` çalıştırmasını veya `/model claude-opus-5` ile açıkça pinlemesini öner.

---

## Codex Kolu

Claude Kolu ile **paralel, aynı anda** hesapla — ekosistem seçimi yok, ikisi
de her zaman üretilir. R/D/W/C skorlaması **Adım 2'deki tanımlarla birebir
aynı**, bir kez hesapla, iki tabloya (Adım 3 ve buradaki) bak. Sadece eşleme
tablosu ve model kadrosu değişiyor.

### Codex sert kapıları

| Koşul | Sonuç |
|---|---|
| Saniye altı gecikme / yüksek hacimli sınıflandırma | **Luna**, efor `minimal` |
| **Siber güvenlik / biyoloji-bitişik** (Adım 1'deki aynı tanımlar) | Codex satırı: **"doğrulanmadı — Claude kullan"**, model önerilmez. Codex'te bu kategoriler için Claude'unkine benzer bir güvenlik-sınıflandırıcı/fallback davranışı **araştırılmadı** — bilmediğim bir şeyi uydurmak yerine dürüstçe boş bırakıyorum. |
| Çok büyük bağlam | ⚠️ Model başına context pencereleri **doğrulanamadı** (sadece Sol Ultra için ~1.5M tek-kaynaklı bir iddia var). Eşik koymuyorum — C skoruna göre normal eşlemeye bırak. |

### Codex eşleme (R/D/W/C → Model, Adım 3 ile paralel mantık)

| Koşul | Model |
|---|---|
| `D=0 ∧ W=0 ∧ C≤1 ∧ R≤1` | **Luna** |
| Yukarıdaki dışında `max(D,C)≤1` | Terra (`D=1` → `efor: low`) |
| `max(D,C)=2` | Terra (`efor: medium`) |
| `max(D,C)=3`, `D<3` (C tetikledi) | Terra — büyük bağlam/sığ akıl yürütme mantığı Claude'dan taşındı, Codex'te ayrıca doğrulanmadı ama aynı ilke uygulanıyor |
| `max(D,C)=3`, `D=3` | **Sol** — *aşağıdaki koşul sağlanıyorsa* **Sol Ultra** |

> **Luna ve `Terra · low` gerçek, sık çıkması gereken sonuçlar — "her zaman
> Sol high ya da Terra medium" çıkıyorsa bu bir hata.** Canlı kullanımda
> bulunan bir sorun: D=1 işler (yaygın kalıp) belirsizlikte D=2'ye
> yuvarlanıyor, D=0 işler (gerçekten mekanik) belirsizlikte D=1'e
> yuvarlanıyor — yukarıdaki D=1/D=2 sınır notuna bak, kota-bilinçli varsayılan
> **aşağı** yuvarlamaktır.
> ✅ Luna: "Bu değişkenin adını `usr` yerine `user` yap" (D=0, mekanik) ·
>    "Bu üç paragrafı daha resmi bir dille yeniden yaz" (D=0, içerik değişmiyor)
> ✅ `Terra · low`: "Bu formda email validasyonu ekle" (D=1, standart kalıp) ·
>    "Bu API'ye cursor-based pagination ekle" (D=1, iyi belgelenmiş tek kalıp)

**Sol → Sol Ultra teşhisi** (`ultracode`'un Codex dengi, ama Adım 3'ün
`ultracode` şartından biraz farklı — burada "bağımsızlık" asıl kriter):
*İş, birbirinden habersiz çalışabilecek 3+ ayrı parçaya (farklı modül/servis/
doğrulama açısı) ayrılıyor ve sonunda birleştirilebilir mi — yoksa parçalar
birbirine bağımlı, tek bir tutarlı tasarım kararı mı gerektiriyor?* Gerçekten
bağımsızsa (ve zaten `D=3→Sol`'a çıkmışsa) → **Sol Ultra**. Ultra yalnızca
Sol üzerinde doğrulandı, Terra/Luna'da yok.
> ✅ "40 farklı mikroservisin güvenlik taramasını, her biri bağımsız olarak
>    aynı anda yap" — gerçekten bağımsız 40 parça → Sol Ultra.
> ❌ "Bu monolitik kod tabanını modüllere ayır" — parçalar birbirine bağımlı,
>    tek tutarlı bir tasarım kararı gerekiyor → düz **Sol** (Claude tarafında
>    da bu örnek `opusplan`'a giriyor, bkz. Adım 3 — aynı görevin Codex'teki
>    dengi "Sol, düz" olması tutarlı: paralelleştirme her iki tarafta da
>    yanıltıcı).

**R tabanı (Claude Kolu'ndaki "R tabanı (genel)" ile aynı ilke):** `R=3` ise
**Luna hiçbir zaman seçilmez**, taban Terra'dır — basit ama geri alınamaz işi
en zayıf modele bırakma. `R=3` ayrıca çıktıya insan onayı notu ekletir (aşağıda,
Çıktı formatı'ndaki tek/paylaşılan not).

**Efor ← D**, Claude Kolu ile aynı mantık: `0→minimal · 1→low · 2→medium · 3→high`.
`D=3 ∧ R=3` ise **`xhigh`** (Codex CLI `config.toml`'da doğrulanan tavan —
bkz. aşağıdaki not, bu "Claude'daki `max`'ın karşılığı" gibi düşünülmeli).

> ⚠️ **"max" ve "mode: pro" Codex CLI'de doğrulanamadı.** Resmî API dokümanı
> `reasoning.effort`'ta `max`'tan, ayrıca ondan bağımsız bir `reasoning.mode`
> (standard/pro) ekseninden bahsediyor — ama bunlar "Responses API" (programatik
> kullanım) için doğrulandı. Codex CLI'nin kendi `config.toml`'unda
> (`model_reasoning_effort`) sadece `minimal|low|medium|high|xhigh` doğrulandı;
> ne `max` ne `mode` orada geçiyor. Bu router **Codex CLI kullanımını**
> hedefliyor — `xhigh`'ı tavan olarak kullan, `max`/`mode:pro`'yu "API'de var
> olabilir ama Codex CLI'de doğrulanmadı" notuyla ancak kullanıcı sorarsa bahset.

### Codex'te insan onayı notu

`R=3` → Adım 4 Kural 1 ile birebir aynı mantık: model/efor değişmez, çıktıya
insan onayı notu eklenir (mandatory istisna, bkz. Çıktı formatı). MCP/
auto-accept uyarıları (Adım 4 Kural 6/7) Codex CLI'de de geçerli olabilir ama
Codex'in kendi araç-şeması/oturum maliyeti mekaniği **doğrulanmadı** — bu iki
kuralı Codex koluna taşımıyorum, yalnızca Claude Kolu'nda geçerliler.

### `mode: pro` — doğrulanmamış, opsiyonel öneri (çıktıya EKLENMEZ)

`max(D,C)=3, D=3` ve Terra'da kalınmışsa (D<3 ama sonuç kritikse), `reasoning.mode: pro`
denenebilir — ama Codex CLI'de doğrulanmadığı için varsayılan çıktıya girmez,
kullanıcı "başka ne yapabilirim?" diye sorarsa "dene, çalışmazsa standart
moda dön" notuyla öner (Claude Kolu'nun `opusplan`+`ultracode` gelişmiş
kombinasyon notuyla aynı ihtiyat seviyesi).

---

## Çıktı formatı

**İki satır, her zaman ikisi birden — Claude ve Codex.** Gerekçe, skor,
yükseltme notu — hiçbiri yazılmaz. R/D/W/C'yi bir kez hesapla (zihinde,
yazıya dökmeden), iki tabloya bak, sonuçları yaz:

```
Claude: <Model> · efor: <seviye>
Codex: <Model> · efor: <seviye>
```

Haiku 4.5 için efor yazma; Codex tarafında **her model efor alır** (Luna
dahil — Luna'nın efor desteğini dışlayan doğrulanmış bir bilgi yok):

```
Claude: Haiku 4.5
Codex: Luna · efor: minimal
```

**Siber güvenlik / biyoloji-bitişik promptlarda Codex satırı model önermez:**

```
Claude: Opus 4.8 · efor: ultracode
Codex: doğrulanmadı — Claude kullan
```

**Bu kuralın istisnaları — sadece şu ikisi, çıktıya her zaman eklenir (iki
satırın ALTINA, ayrı satır(lar) olarak; metnin kalanında "not/uyarı/öner" diye
geçen başka hiçbir şey otomatik eklenmez):**
1. `R=3` → insan onayı notu — **tek satır, iki tarafı da kapsar** (görev
   riski ekosisteme göre değişmez, tekrar yazma).
2. `opusplan` (yalnızca Claude satırında olabilir) → efor-otomatik-geçmez
   uyarısı, sadece Claude satırının altına.

Bunların dışında kalan her şey — Adım 4 Kural 2-8'deki notlar, `opusplan`'ın
"gelişmiş kombinasyon" paragrafı, Codex'in `mode: pro` notu, yükseltme
koşulları — **sadece kullanıcı sorduğunda** açıklanır, varsayılan çıktıya
eklenmez.

Kullanıcı gerekçe sorarsa (*"neden?"*, *"niye bu?"*) o zaman açıkla — ama
istenmeden ekleme, ve o zaman bile kısa tut.

### Örnekler

Girdi: *"Bu 200 müşteri yorumunu olumlu/olumsuz diye etiketle"*
```
Claude: Haiku 4.5
Codex: Luna · efor: minimal
```

Girdi: *"Repodaki auth akışını anlayıp OAuth2'ye taşı"*
```
Claude: Sonnet 5 · efor: high
Codex: Terra · efor: low
```
(Aynı D=1 girdi, iki farklı sayısal efor kelimesi — Claude ölçeği `low→max`
D=1'de `medium`'dan başlıyor gibi görünse de burada D=2 sonucu `high`; Codex
ölçeği `minimal→xhigh` daha alt basamaktan başlıyor. İki ölçek birbirine
çevrilmez, karıştırma.)

Girdi: *"Prod'da ara sıra düşen şu race condition'ı bul"*
```
Claude: Opus 5 · efor: max
Codex: Sol · efor: xhigh
İnsan onayı olmadan uygulanmasın.
```

Girdi: *"Şu 180 servislik ortama sızma testi yap, auth bypass zincirleri kur"*
```
Claude: Opus 4.8 · efor: ultracode
Codex: doğrulanmadı — Claude kullan
```
(Sızma testi = saldırı amaçlı sert kapı. Ama **"bu 180 servisin kodunu auth
bypass açığı için denetle"** savunma işidir — kapı tetiklenmez, normal
skorlamaya girer: `Claude: Sonnet 5 · efor: ultracode` / `Codex: Terra · efor: medium`.)

Girdi: *"Bu genomik pipeline'daki varyant çağırma mantığını denetle"*
```
Claude: Fable 5.1 · efor: high
Codex: doğrulanmadı — Claude kullan
```

Girdi: *"Prod config'inde `MAX_RETRIES`'ı 3'ten 5'e çek"*
```
Claude: Sonnet 5 · efor: low
Codex: Terra · efor: minimal
İnsan onayı olmadan uygulanmasın.
```
(R=3 ama D=0 — Claude tarafında model Haiku'ya düşmüyor, Sonnet'te taban
buluyor; Codex tarafında böyle bir taban kuralı yok çünkü Luna zaten efor
alıyor, D=0 direkt Luna'ya düşer... ama R=3 nedeniyle Codex tarafında da
Luna yerine Terra'da kalınır, aynı "R=3 en zayıf modele bırakılmaz" ilkesi.)

Girdi: *"Prod'daki 200 servisin auth mimarisini baştan tasarla"*
```
Claude: opusplan · plan: max · uygulama: medium
⚠️ Efor otomatik geçmez — yürütme moduna geçince /effort medium ile elle ayarla.
Codex: Sol · efor: xhigh
İnsan onayı olmadan uygulanmasın.
```
(`opusplan` yalnızca Claude'da var; Codex tarafı kendi normal eşlemesinden
düz Sol çıkar, iki taraf farklı mekanizma kullanabilir, bu normal.)

Girdi: *"40 tamamen bağımsız mikroservisin güvenlik açığı taramasını aynı anda yap, her biri kendi başına"*
```
Claude: Sonnet 5 · efor: ultracode
Codex: Sol Ultra · efor: high
```
(Gerçek bağımsız-paralel iş — Claude tarafında `ultracode`, Codex tarafında
Sol Ultra tetikleniyor; iki taraf da kendi paralellik mekanizmasını kullanıyor.)

---

## Detay gerekirse

Benchmark tabloları, fiyatlandırma, abonelik planları ve kaynak veri kalitesi
notları için `reference.md` dosyasını oku. Kullanıcı "neden bu model?",
"rakamlar ne?" diye sorarsa oraya bak — özellikle **§2.1** (LiveBench /
BenchAlign / AA Index, 2 Eyl 2026) ve **§0.1** (Fable 5.1 / Mythos 5.1).

**Router benchmark rakamıyla model seçmez.** Leaderboard'lar Kural 2/3'ün
*yönünü* doğruluyor; skorlama R/D/W/C üzerinden yürür, aggregate skor üzerinden
değil (BenchAlign Sonnet 5'i kapsama artefaktıyla düşük gösteriyor — bkz. §2.1).
