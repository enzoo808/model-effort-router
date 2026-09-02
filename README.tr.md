# Claude & Codex Model / Ekosistem / Efor Seçici

> 🇬🇧 **English:** [README.md](README.md) · Bu, Türkçe ayrıntılı sürümdür.
> **Not:** 2 Eyl 2026'da skill gövdesi (`skill/SKILL.md` + `reference.md`)
> İngilizce'ye taşındı — çıktı artık `effort:` / `unverified — use Claude` /
> `Do not apply without human review.` yazıyor. Bu Türkçe README karar
> mantığının ayrıntılı anlatımı olarak korunuyor; kural değişiminde bununla
> `SKILL.md` elle senkron tutulmalı.

Bir promptu verdiğinde **hangi ekosistemle** (Claude Code veya Codex/ChatGPT
Plus), hangi modelle (Haiku 4.5 / Sonnet 5 / **Opus 5** / Opus 4.8 / Fable 5.1 /
Mythos 5.1 / Luna / Terra / Sol / Sol Ultra) ve hangi efor seviyesiyle çalıştırman
gerektiğini söyleyen router.

**Kalibrasyon: iki ayrı abonelik kotası (Pro/Max + ChatGPT Plus).** Korunan
kaynak dolar değil — Claude'un 5 saatlik penceresi **ve** ChatGPT Plus'ın
3 saatlik/haftalık pencereleri. Router'ın asıl işi seni "en pahalı modeli/
yanlış ekosistemi seç" refleksinden kurtarmak.

**5 Ağustos 2026'da eklendi:** Router artık Claude-only değil. Önce hangi
ekosistemin kotasından harcanacağına karar veriyor (bkz. "Ekosistem Seçimi"),
sonra o ekosistemin kendi model+efor mantığına giriyor. Detay için
`skill/SKILL.md`'deki "Ekosistem Seçimi" ve "Codex Kolu" bölümlerine bak.

---

## Model kadrosu (1 Eylül 2026 — Fable 5.1 / Mythos 5.1 lansmanı)

| Model | Rol |
|---|---|
| Haiku 4.5 | Hız/hacim uzmanı. Efor desteklemez |
| Sonnet 5 | Günlük iş — hız+zeka dengesi. Varsayılan başlangıç noktası |
| **Opus 5** | **Amiral gemisi.** Opus 4.8'in yerini aldı, aynı fiyata (~$5/$25) çok daha güçlü |
| Opus 4.8 | Legacy — **yalnızca saldırı amaçlı siber güvenlik kapısı için** kalıcı bir rolü var |
| **Fable 5.1** | Frontier ölçek: uzun ufuklu otonomi, aşırı genişlik, **biyoloji-bitişik Ar-Ge**. Fable 5'in yerini aldı — aynı $10/$50, cache okuması ¼'ü ($0.25/MTok), bilgi kesimi Haz 2026 |
| Mythos 5.1 | Fable 5.1 = izinli safeguard. **Yalnızca Project Glasswing daveti** (doğrulanmış siber-savunmacı / yaşam bilimci). Router yalnızca kullanıcı bu erişimi belirtirse önerir |

Opus 4.8'in genel işte kalmasının tek nedeni şu: saldırı amaçlı siber güvenlik
isteği işaretlendiğinde Fable 5.1'in izinli fallback hedeflerinden biri
(diğeri Opus 5). Router bu dolambaçlı yolu atlayıp doğrudan Opus 4.8'i öneriyor.
**Yeni (Fable 5.1):** savunma amaçlı zafiyet keşfi artık bloklanmıyor —
Fable 5.1 kendisi yapıyor, o iş kapı tetiklemez, normal skorlamaya girer.

**Biyoloji tarafı farklı davranıyor:** selim biyoloji-tıp soruları artık kapı
değil (%85 daha az işaretleniyor). Ar-Ge yoğun işte Fable 5.1 Ar-Ge-işaretli
kısımları Opus modellerine yönlendirir; ama Opus 5'in kendisinde biyoloji Ar-Ge
için **hiç fallback yok** — direkt reddediyor. Bu yüzden router Fable 5.1
öneriyor, Opus 5 değil. Life Sciences Verification Program araştırmacısı →
Mythos 5.1.

### Codex/ChatGPT kadrosu (GPT-5.6 ailesi, 9 Temmuz 2026)

| Model | Rol | Claude dengi (kaba) |
|---|---|---|
| Luna | Hız/hacim, en ucuz ($0.20/$1.20 MTok) | Haiku 4.5 |
| Terra | Günlük iş, dengeli ($2/$12) — varsayılan | Sonnet 5 |
| **Sol** | Amiral gemisi — kod/bilim/güvenlik ($5/$30) | Opus 5 |
| **Sol Ultra** | Sol'da açılan Codex ürün modu (Plus+): ~4 paralel işbirlikçi ajan. Efor değeri değil | Net dengi yok — `ultracode`'dan daha güçlü |

Siber güvenlik ve biyoloji-bitişik iş **her zaman Claude'a** yönlendirilir —
Codex tarafında bu kategoriler için doğrulanmış bir güvenlik-fallback zinciri
yok (araştırılmadı, uydurulmadı).

---

## Neden gerekli

**Model seçimi artık risk değil, zeka ihtiyacına göre yapılıyor.** Önceki
tasarımda risk (R) doğrudan modeli en pahalıya zorluyor, sonra ayrı bir kuralla
geri indiriliyordu — dolambaçlı ve az çeşitli çıktı üretiyordu. Yeni tasarımda:

- **Model** ← derinlik/bağlam ihtiyacına (`max(D,C)`) göre seçilir
- **Risk (R)** modeli değiştirmez; sadece insan onayı notu ekler ve Haiku'yu eler

Bu ayrım, aynı promptun hep aynı iki modele (Sonnet 5 + eski Opus 4.8) çökmesini
önlüyor — artık Haiku, Sonnet 5 (5 efor seviyesinde), Opus 5 (5 efor + ultracode),
Opus 4.8 (saldırı-amaçlı güvenlik + ultracode) ve Fable 5.1 (frontier + biyoloji)
hepsi gerçekten erişilebilir çıktılar.

**Opus 4.8 döneminden kalan iki kural, hâlâ yön gösteriyor** (rakamlar Opus 5'e
miras değil — bkz. `reference.md` §2):

| Alan | Opus 4.8 | Sonnet 5 | Yön |
|---|---|---|---|
| Terminal-Bench 2.1 (ham) | 74.6 | **80.4** | Sonnet önde |
| HLE (araçlı) | 57.9 | 57.4 | Parite |
| HLE (**araçsız**) | **49.8** | 43.2 | Opus önde |
| SWE-bench Pro (ajanik kod) | **69.2** | 63.2 | Opus önde |
| USAMO 2026 (matematik) | **96.7** | 79.5 | Opus önde |

Opus 5, Opus 4.8'e göre genel olarak büyük bir sıçrama yaptı (Frontier-Bench'te
2 katından fazla, GDPval-AA/OSWorld'de liderlik) — ama bu spesifik testlerdeki
**tam farkı bilmiyoruz**, sadece yönün büyük ihtimalle aynı veya daha güçlü
olduğunu biliyoruz. Router bunu dürüstçe işaretliyor, kanıtlanmamış üstünlük
iddia etmiyor.

---

## Kurulum

### Claude Code (birincil)

```powershell
.\install.ps1
```

`skill/` klasörünü `~\.claude\skills\model-secici\` altına kopyalar. Claude Code'u
yeniden başlat, sonra:

```
/model-secici Repodaki auth akışını OAuth2'ye taşı
```

**`/model opus` artık Opus 5'e çözülüyor** (Claude Code v2.1.219+). Eski
sürümdeysen `claude update` çalıştır, yoksa alias Opus 4.8'e (veya daha eskiye)
düşebilir.

### Claude.ai / Claude Chat (birincil — artık native Skill desteği var)

29 Temmuz 2026 itibarıyla claude.ai **custom Skills**'i doğrudan destekliyor —
Project'e bağlı değil, bir kez yüklenince **her sohbette** otomatik tetikleniyor.
Gereksinim: Pro/Max/Team/Enterprise plan + Settings'te *code execution* açık.

```powershell
.\build-claude-ai-zip.ps1
```

`dist/model-secici.zip` üretir (aynı `skill/SKILL.md`+`reference.md`'den —
ayrı, elle senkronize edilen bir kopya değil). Sonra: Claude.ai → **Settings →
Features → Custom Skills → Upload** → `dist/model-secici.zip` seç.

> **Sınırlama (resmî dokümandan):** claude.ai'a yüklenen skill Claude Code'daki
> ile **otomatik senkronize olmaz** — SKILL.md değiştikçe `build-claude-ai-zip.ps1`'i
> tekrar çalıştırıp zip'i yeniden yüklemen gerekir. Ayrıca claude.ai'daki custom
> Skill'ler **kullanıcıya özel** (org geneli merkezi dağıtım/yönetim yok).

### Claude.ai — eski yöntem (code execution kapalıysa fallback)

Yukarıdaki native Skill yüklemesi için code execution gerekiyor; plan/ayar
izin vermiyorsa `claude-ai/instructions.tr.md` dosyasındaki çizginin altındaki
metni kopyala → Claude.ai → Projects → yeni proje → *Custom instructions* →
yapıştır. Dezavantajı: tek bir Project'e bağlı kalır (her sohbette değil) ve
`SKILL.md` ile elle senkronize tutulması gerekir.

---

## Dosyalar

```
skill/SKILL.md                  Router kuralları — tek kaynak
skill/reference.md              Benchmark/fiyat/abonelik tabloları + veri kalitesi notları
claude-ai/instructions.tr.md    Claude.ai fallback'i (code execution kapalıysa) — kendi kendine yeten türev
install.ps1                     skill/ → ~/.claude/skills/model-secici/ (Claude Code)
build-claude-ai-zip.ps1         skill/ → dist/model-secici.zip (Claude.ai native Skill yüklemesi)
evals/                          Regresyon eval seti (routing + trigger) + koşu geçmişi
```

`SKILL.md` kısa tutuldu; tablolar `reference.md`'de. Kural değişikliği yaparsan:
1. `build-claude-ai-zip.ps1`'i tekrar çalıştır ve claude.ai'a yeniden yükle
   (otomatik senkronize olmuyor).
2. `claude-ai/instructions.tr.md`'yi de güncelle — sadece fallback yöntemi
   kullananlar için, ama hâlâ elle senkron tutuluyor.

---

## Karar mantığı

**Adım 0 — Kalite kapısı.** Dört mekanik kontrol: (1) örnekle anlatılan ama
genellenmemiş kural var mı, (2) yanlış varsayım sessizce yanlış sonuç üretir
mi, (3) hedef somut mu, (4) iki farklı makul yorum çıkar mı. Biri tetiklenirse
model önerme — canlı kullanıcı testinde eski, tek soruluk hâli ("başarı
kriteri/kapsam var mı") hiç tetiklenmedi; gerçek promptlar genelde kapsam
içerir ama içine gömülü bir belirsizlik taşır (bkz. `reference.md` §8,
"Adım 0 örnekleri").

**Adım 1 — Sert kapılar.**
- Yüksek hacim/gecikme → Haiku, dur.
- **Saldırı amaçlı** siber güvenlik (exploit, sızma testi, binary tarama) → **Opus 4.8**, efor tabanı `xhigh` (Glasswing erişimi varsa Mythos 5.1). Savunma amaçlı denetim kapı **değil** — Fable 5.1 kendisi yapar.
- Biyoloji-bitişik Ar-Ge → **Fable 5.1** (Opus 5'te fallback yok, direkt reddeder). Life Sciences Verification Program → Mythos 5.1.
- Bağlam >200k → Haiku elenir.
- Frontier ölçek (binlerce dosya) → Fable 5.1.

**Adım 2 — Skorlama.** R, D, W, C — her biri 0–3. Her eksenin artık teşhis
sorusu ve alan-bazlı çapası var (kodlama/yazı/araştırma/veri için "derinlik"
farklı anlama gelir) — `SKILL.md` Adım 2'de. Kararsız kalınırsa `reference.md`
§8'deki ~25 örnekten en yakın analojiyi bul.

**Adım 3 — Eşleme.** Model ← `max(D,C)` (risk değil!). **Opus 5 yalnızca
`D=3` ise aday** — `C=3` tek başına (büyük bağlam ama sığ akıl yürütme) Opus 5'i
tetiklemez, Sonnet 5'te kalır:
- `D=0∧W=0∧C≤1∧R≤1` → **Haiku** — D=1 ("bilinen kalıp") hiçbir zaman Haiku'ya düşmez
- Yukarıdaki dışında max(D,C)≤1 → Sonnet 5
- 2 → Sonnet 5
- 3, `D<3` (C tetikledi) → **Sonnet 5**
- 3, `D=3` → **Opus 5** (ajanik kod/matematik/araçsız akıl yürütme) / **Sonnet 5** (diğer her şey, kota-bilinçli)

`R=3` → Haiku hiç seçilmez + insan onayı notu. **Efor ← D, modelden bağımsız,
her zaman.** `ultracode` ⇔ `W=3 ∧ >30dk ∧ ¬(D=3∧R=3)` — model kısıtsız (Haiku
hariç); tetiklenirse efor alanı **`ultracode`** olur, D'nin eforuyla birleşmez.

**Sonuç:** Opus 5 bu router'da hep `D=3` ile çıkar (`xhigh`/`max`) — hiçbir
zaman `low`/`medium` ile önerilmez, çünkü D=3 olmadan zaten seçilmiyor.

**`opusplan` (yalnızca Claude Code).** D=3∧Kural2(a) durumunda, üç şart daha
sağlanıyorsa düz Opus 5 yerine önerilir: (1) zorluk plana **ön-yüklü**
(plan bitince yürütüm tekrarlayan bir kalıba dönüşüyor — debug/ispat gibi
"zorluk yürütme boyunca sürüyor" işlerde değil), (2) `W≥2`. Çıktı iki fazlı:
`opusplan · plan: xhigh · uygulama: medium`. **Efor otomatik geçmez** — plan
modunda `xhigh` yürütmeye de taşınır, elle indirilmezse Sonnet 5 gereksiz
pahalı çalışır ve amaç ters teper. Router bu uyarıyı her `opusplan`
önerisine ekler.

**Adım 4 — Kota koruma.** D=3 ama Kural 2'ye girmiyorsa Sonnet 5 (efor `xhigh`)
varsayılan — kota gerekçesi. Yükseltme notu artık **kanıtsız değil**: LiveBench
2026-06-25 (bağımsız, kontaminasyon-serbest) Opus 5'i Sonnet 5'in üstünde
gösteriyor (agentic coding +5.8, language +13.7 — bkz. `reference.md` §2.1).
(Opus 5'te low/medium'un "israf" olmadığı bilgisi router'ın kendi çıktısını
değiştirmez — Opus 5 zaten hep D=3'te çıkıyor.)

**Benchmark politikası.** Router benchmark rakamıyla model **seçmez** —
leaderboard'lar (LiveBench / BenchAlign / AA Index, `reference.md` §2.1)
yalnızca Kural 2/3'ün *yönünü* doğrular. Aggregate skorlar yanıltıcı olabilir:
BenchAlign Sonnet 5'i kapsama artefaktıyla #39 gösteriyor, LiveBench tam
kapsamda 76.0 (güçlü günlük sürücü).

---

## Doğrulama

Kurulumdan sonra bu senaryolarla sına. Router artık beş modelin de gerçekten
çıkabildiğini göstermeli — sadece Sonnet 5 + Opus'a çökmemeli. Bu tablonun
makine-okunur, tekrar koşturulabilir kopyası `evals/routing/evals.json`
— `SKILL.md` her değiştiğinde elle iz sürmek yerine oradaki `grade_routing.py`
ile regresyon kontrolü yap (bkz. `evals/README.md`). **Taze/soğuk
ajanlarla** (README'nin kendi bağlamını bilmeyen) koşturmak önemli — bu oturumda
tam da bu yöntemle 3 gerçek belirsizlik bulundu ve `SKILL.md`'ye düzeltildi:
frontier-ölçek kapısının "üç şart AND" okunması, `opusplan`'ın flagship
örneğinde yürütüm fiilinin yazılı olmaması, ve "mimari karar" etiketinin R=2/R=3
ayrımını bulanıklaştırması. Aşağıdaki tablonun beklenen çıktıları bu düzeltmelerden
sonra 16/16 doğrulandı.

> **1–2 Eyl 2026 — Fable 5.1 / Mythos 5.1 güncellemesi + taze-ajan eval koşusu:**
> model kadrosu, siber güvenlik kapısı (savunma/saldırı ayrımı), fiyat/efor
> tabloları güncellendi; `reference.md` §0.1 + §2.1 eklendi (LiveBench /
> BenchAlign / AA Index). Ayrıca R/D/W rubriklerine üç netleştirme: W eşiği
> sayısal (100+ = W=3, "60 mikroservis" = W=2), tam-belirtilmiş additive şema
> değişikliği = D=0, "monoliti modüllere ayır" (R=2) vs "ayrı servislere böl"
> (R=3, paylaşılan çekirdek).
>
> **iteration-7** (17 dual eval, 4 taze paralel ajan): 12/17 otomatik geçti —
> 5 sapmanın hepsi *efor seviyesi* (model 17/17 doğru). Fable 5.1'e özel
> değişiklikler (offensive→Opus 4.8, biyoloji→Fable 5.1, savunma→kapı yok,
> frontier→Fable 5.1) hepsi geçti. Sapmalar D/W/R sınır belirsizliğiydi.
> **iteration-8** (aynı 17, rubrik netleştirmeleri sonrası, taze ajan re-run):
> **17/17**. Yeni kalıcı evaller: `5b`, `f1` (monolit→servis, R=3), `f2`.
>
> **iteration-9** (2 Eyl 2026 — `SKILL.md` + `reference.md` İngilizce'ye
> taşındıktan sonra, taze ajan re-run): **17/17**. Çıktı formatı `efor:` →
> `effort:`, `doğrulanmadı` → `unverified — use Claude`,
> `İnsan onayı olmadan uygulanmasın.` → `Do not apply without human review.`;
> grader + `evals.json` aynı turda güncellendi. Büyük savunma denetimi
> (adversarial zafiyet avı) artık D=3 (§8 ile tutarlı) → `5b` beklenen çıktısı
> `Sonnet 5 · ultracode` / `Sol Ultra · high`.
> **Ardından (aynı iterasyon):** Codex efor tavanı `xhigh` → **`max`** olarak
> düzeltildi — `max` Codex'te gerçek bir ayar (2 Eyl 2026 doğrulandı;
> `learn.chatgpt.com` config referansı eski). `D=3 ∧ R=3` olan Codex çıktıları
> (d6, f1) yeniden koşuldu. `ultra` bir efor değeri değil, ürün modu.
> Legacy id 1–22 hâlâ `format_outdated`.

| # | Prompt | Beklenen | Sınadığı kural |
|---|---|---|---|
| 1 | 200 müşteri yorumunu olumlu/olumsuz etiketle | **Haiku 4.5, efor yok** | Hacim kapısı |
| 2 | Şu React bileşenine dark mode ekle | Sonnet 5 · medium | Taban durum |
| 3 | Repodaki auth akışını OAuth2'ye taşı | Sonnet 5 · **high** | Skorlama (D=2) |
| 4 | Prod'da ara sıra düşen race condition'ı bul | **Opus 5** · **max** | max(D,C)=3, ajanik/derin — R sadece insan onayı ekler |
| 5 | Şu 180 servislik ortama sızma testi yap, auth bypass zincirleri kur | **Opus 4.8** · **ultracode** | Saldırı amaçlı siber güvenlik kapısı |
| 5b | Bu 180 servisin kodunu auth bypass açığı için denetle (exploit yazma) | **Claude: Sonnet 5 · ultracode** · **Codex: Sol Ultra · high** | Savunma denetimi — offensive kapı **tetiklenmez** (Fable 5.1 sonrası). Adversarial zafiyet avı = D=3, 180 birim bağımsız = W=3 + Sol Ultra |
| 6 | Şu kodu düzelt | Model önerme, netleştir | Adım 0 (hedef somut değil) |
| 6b | "Bir günde 1000 üretim olursa 500'ü aynı güne, 500'ü ertesi güne yansısın" | Model önerme, netleştir | Adım 0 (kural örnekle anlatılmış, genellenmemiş — canlı kullanıcı testi) |
| 7 | Prod config'inde MAX_RETRIES'ı 3'ten 5'e çek | **Sonnet 5 · low** + insan onayı notu | R=3∧D=0 — model/efor **değişmez** (D takip eder), sadece onay notu eklenir |
| 8 | 4000 dosyalık legacy monolitini modüllere ayır | **Fable 5.1 · ultracode** | Frontier-ölçek kapısı + W=3 |
| 9 | Prod'daki 200 servisin auth mimarisini baştan tasarla | **opusplan · plan: max · uygulama: medium** | Mimari karar ön-yüklü (bir kez tasarlanır, 200 servise mekanik uygulanır), W=3, R=3∧Kural2a — opusplan'ın flagship senaryosu |
| 9b | 40 mikroservisi ortak bir auth middleware'e geçir, tasarımı bir kez belirle | **opusplan · plan: xhigh · uygulama: medium** | Aynı örüntü, R=2 (geri alınabilir) — plan eforu `xhigh` kalır, `max`'a çıkmaz |
| 10 | 40 sayfalık sözleşmede çelişen hükümleri bul | **Sonnet 5 · xhigh** | Kural 3 (D=3, Kural 2 dışı, kanıtsız-ama-ucuz) |
| 11 | 300 dosyada require()'ları import'a çevir (mekanik, geri alınabilir) | **Sonnet 5 · ultracode** | `ultracode` model kısıtsız — Sonnet'te de çalışır |
| 12 | Bu genomik pipeline'daki varyant çağırma mantığını denetle | **Fable 5.1 · high** | Biyoloji Ar-Ge kapısı — Opus 5 **değil** |
| 13 | 300 sayfalık API dokümantasyonunu oku, deprecated endpoint'leri listele | **Sonnet 5 · medium** | `C=3, D=1` — büyük bağlam Opus 5'i **tetiklemez**, model Sonnet'te kalır, efor D'yi takip eder |
| 14 | Bu router'ın model seçimini riskten ayrıştır, çakışma kurallarını sıfırdan tasarla | **Opus 5 · xhigh** | Kural 2a artık kod-dışı yapılandırılmış tasarımı da kapsıyor — canlı testte bulunan gerçek boşluk |

**3 ile 4'ün ayrışması** artık R değil, D/C üzerinden çalışıyor — ikisi de
"çok adımlı" ama 4'te gerçek derinlik (D=3) var, 3'te yok (D=2).

**4, 9 ve 14'ün ayrışması `opusplan`'ın en önemli sınırını çizer.** Üçü de
D=3∧Kural2a, ama sadece 9 (ve 9b) `opusplan`'a giriyor: 4'te zorluk yürütme
boyunca sürüyor (kod okumadan race condition'ın nedeni bilinmez), 14'te W=1
yetersiz VE yürütüm de kendi başına yargı gerektiriyordu (bu oturumda canlı
kanıtlandı — plan bir kerede mekanikleşmedi), 9'da ise mimari karar gerçekten
tek seferlik ve 200 servise **tekrarlanan** bir kalıp olarak uygulanıyor.
`opusplan`, W=3'ü `ultracode` gibi paralel değil, **zamansal** olarak (önce
pahalı plan, sonra ucuz mekanik uygulama) çözüyor — ikisi farklı problemlere
cevap.

**5 ile 12'nin ayrışması router'ın güvenlik mimarisini kanıtlar:** ikisi de
"sert kapı", ama saldırı-amaçlı siber Opus 4.8'e, biyoloji Ar-Ge Fable 5.1'e
gider — aynı kapı değiller, fallback zinciri ikisinde farklı davranıyor. **5b**
ise (savunma denetimi) Fable 5.1 sonrası kapı **değil** — savunma/saldırı ayrımı
artık router'da açık.

**7, modelin artık riskten etkilenmediğinin kanıtı.** Eski tasarımda bu senaryo
"Opus·low → Sonnet·high" dolambaçlı düzeltmesinden geçerdi; yeni tasarımda
model zaten Sonnet — R sadece bir uyarı notu ekliyor.

**13, C'nin tek başına Opus 5'i tetikleyemediğinin kanıtı.** `max(D,C)=3` ama
bunu C sağlıyor, D sadece 1. Model tablosunun "3, D<3" satırı burada devreye
giriyor: Opus 5 aday olmuyor, Sonnet 5'te kalıyor; efor D=1'i takip ediyor →
`medium`. Bu, "büyük bağlam = otomatik Opus 5" yanlış sezgisini kırıyor —
Opus 5 bu router'da **her zaman ve sadece** D=3 ile birlikte çıkar.

### Ekosistem Seçimi doğrulaması (5 Ağustos 2026)

| # | Prompt | Beklenen | Sınadığı kural |
|---|---|---|---|
| c1 | "Codex'te şu React bileşenine dark mode ekle" | **Codex (ChatGPT Plus) · Terra · effort: low** | Açık ortam belirtimi (madde 2), sinyal değerlendirmeye gerek yok |
| c2 | "80 tamamen bağımsız endpoint dokümantasyonu, aynı anda" | **Codex (ChatGPT Plus) · Terra · effort: low** (Sol Ultra **değil**) | Ekosistem (paralellik/W) ile model katmanı (derinlik/D) farklı sinyaller — gerçek paralel iş ama D=1, Sol'a çıkmamalı |
| c3 | "1000 destek talebini kategorilere ayır" (ortam belirtilmemiş) | **Claude Code · Haiku 4.5** | Madde 5 varsayılanı — c1'in aynı-prompt-ortamsız çifti, Codex Kolu'nun kendi örneğiyle çelişmediğini doğrular |
| c4 | "Şu React bileşenine dark mode ekle" (ortam belirtilmemiş) | **Claude Code · Sonnet 5 · effort: medium** | c1'in çifti — aynı D=1, Claude ölçeğinde `medium` (Codex'teki `low` değil) |
| c5 | "Bu monolitik kod tabanını modüllere ayır" | **Claude Code · opusplan · plan: xhigh · uygulama: medium** | Ekosistem Seçimi'nin kendi ❌ karşı-örneği — yüzeysel paralel ama parçalar bağımlı, Codex/Ultra'ya gitmemeli |

**c1/c4 ve c2/c5 çiftleri** router'ın iki ayrı hatayı önlediğini kanıtlıyor:
(1) aynı iş ortamsız sorulunca sessizce Codex'e kaymıyor — açık sinyal yoksa
Claude'da kalıyor; (2) "büyük ölçek = güçlü model" yanlış sezgisi burada da
kırılıyor — paralellik ekosistemi belirler, derinlik modeli belirler, ikisi
karıştırılmıyor.

---

## Bilinen veri sorunları

Model/efor mekaniği doğrudan resmî dokümandan doğrulandı — 27 Temmuz 2026:
[platform.claude.com/.../overview](https://platform.claude.com/docs/en/about-claude/models/overview),
[.../effort](https://platform.claude.com/docs/en/build-with-claude/effort),
[.../pricing](https://platform.claude.com/docs/en/about-claude/pricing),
[code.claude.com/.../model-config](https://code.claude.com/docs/en/model-config).

**Fable 5.1 / Mythos 5.1 (1 Eyl 2026)** ayrıca doğrulandı — 2 Eyl 2026:
[anthropic.com/claude-fable-and-mythos-5-1](https://www.anthropic.com/claude-fable-and-mythos-5-1),
[platform.claude.com/.../fable-5-1/whats-new](https://platform.claude.com/docs/en/models/fable-5-1/whats-new-fable-5-1),
[.../mythos-5-1/overview](https://platform.claude.com/docs/en/models/mythos-5-1/overview),
[.../choosing-a-model](https://platform.claude.com/docs/en/about-claude/models/choosing-a-model).

Opus 4.8 dönemi benchmark verisi "Claude Modelleri Kaynaklı Teknik Analiz"
raporundan (`[K1]` Anthropic · `[K2]` bağımsız · `[K3]` içerik sitesi).

**Codex/ChatGPT verisi de aynı disiplinle işlendi (5 Ağustos 2026):**
kullanıcının verdiği "Codex Plus Modelleri Raporu" SEO-toplayıcı sitelerden
derlenmişti, resmî değildi — `openai.com/index/gpt-5-6/`,
`developers.openai.com/api/docs/guides/reasoning`,
`learn.chatgpt.com/docs/config-file/config-reference` ile çapraz doğrulandı.
Rapor Terra/Luna için **eski fiyat** veriyordu (30 Temmuz indirimini
yansıtmıyordu) ve efor mekaniğini **tek boyutlu, yanlış** bir merdiven olarak
tanımlıyordu (gerçekte `reasoning.effort` ve `reasoning.mode` birbirinden
bağımsız iki eksen). Detay: `skill/reference.md` §9.

**En önemli metodolojik kural: eski model verisini yeni modele miras bırakma.**
Opus 4.8'in Terminal-Bench/SWE-bench-Pro/HLE/USAMO sayıları **Opus 5'e ait
değil** — Opus 5 ayrı bir model, kendi granüler sayıları henüz yayınlanmadı.
Router bunu §2/§7'de (`reference.md`) açıkça işaretliyor ve rakamları sadece
"yön göstergesi" olarak kullanıyor, kesin üstünlük iddiası olarak değil.

**Çürütülen, router'a girmeyen veriler** (ayrıntı: `skill/reference.md` §7):
- Efor seviyelerinin token bütçeleri — böyle bir bütçe yok, efor davranışsal sinyal.
- `task_budget` asgarisi 2.000 değil **20.000**.
- "5 saatlik pencerede 10–40 prompt" — kota token+bağlam üzerinden erir.
- Her MCP sunucusu sabit 18k token — araç sayısıyla orantılı.
- GDPval'de "Sonnet 5 Opus'u geçti" — 3 Elo anlamlı değil.

Sonnet 5 promosyonu **31 Ağustos 2026**'da bitti ($2/$10 → $3/$15); Opus/Sonnet
kota oranı 1.67×.

---

## Kota tasarrufu notları

- **MCP sunucuları** araç şemalarını her mesaja enjekte eder, araç sayısıyla
  orantılı (GitHub MCP: 27 araç ≈ 18k token). Kullanılmayanları kapat.
- **Auto-accept** sürekli açıksa kota geometrik yanar.
- **Team Standard** ($25/koltuk) planında Claude Code erişimi **yok**.
- **Opus 5'i elle çalıştırırken low/medium'dan çekinme** — Anthropic'in kendi
  tavsiyesi, önceki Opus nesillerinden farklı bir duruş. (Router'ın kendi
  önerisi bunu hiç göstermez — Opus 5 router çıktısında hep D=3 ile çıkar.)
- **Alias kontrolü:** `/model opus` Opus 5'e çözülüyor mu, yoksa eski sürümden
  dolayı Opus 4.8'e mi düşüyor — `claude update` ile kontrol et.
