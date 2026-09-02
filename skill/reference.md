# Referans Tabloları

> **Birincil kaynak:** `platform.claude.com/docs/en/about-claude/models/overview`,
> `platform.claude.com/docs/en/build-with-claude/effort`,
> `platform.claude.com/docs/en/about-claude/pricing`,
> `code.claude.com/docs/en/model-config` — doğrudan doğrulandı (24 Temmuz 2026
> Opus 5 lansmanı sonrası).
>
> **İkincil kaynak:** "Claude Modelleri Kaynaklı Teknik Analiz", kaynak katmanı
> disiplinli rapor (10 Temmuz 2026, Opus 5 öncesi). `[K1]` = Anthropic resmi
> doküman/sistem kartı, `[K2]` = bağımsız değerlendirici, `[K3]` = içerik
> sitesi/forum. **Bu rapordaki Opus 4.8 verisi Opus 5'e miras bırakılmaz** —
> ayrı bir model, ayrı benchmark profili.
>
> Bu dosya yalnızca gerektiğinde okunur — `SKILL.md` kendi başına yeterlidir.

---

## 0. Opus 5 — 24 Temmuz 2026 lansmanı

Opus 5 (`claude-opus-5`), Opus 4.8'in yerine geçen amiral gemisi. Anthropic'in
kendi önerisi: *"Emin değilsen Opus 5'le başla."* Opus 4.8 artık "legacy"
kategorisinde — hâlâ çalışıyor ama Anthropic aktif olarak Opus 5'e geçişi
öneriyor.

**Fiyat değişmedi:** $5/$25 (girdi/çıktı MTok) — Opus 4.8 ile aynı.

**Yayınlanan benchmark iddiaları** (Anthropic'in kendi lansman notu):
- Frontier-Bench v0.1: Opus 4.8'in **2 katından fazlası**, daha düşük maliyetle
- CursorBench 3.2: `max` eforda Fable 5'in zirve skorunun **%0.5 içinde**, yarı fiyatına
- ARC-AGI-3: en yakın rakibin **3 katı**
- Zapier AutomationBench: en yakın rakibin **~1.5×**'i, eşit maliyette
- OSWorld 2.0: her maliyet noktasında en iyisi; Fable 5'in en iyi sonucunu
  **üçte birinden azına** geçiyor
- Yaşam bilimleri (iç benchmark): organik kimyada Opus 4.8'den **+10.2 puan**,
  protein görevlerinde **+7.7 puan**

⚠️ **Ne YAYINLANMADI:** SWE-bench Pro, Terminal-Bench 2.1, HLE (araçlı/araçsız),
USAMO — bu raporun Kural 2/3'ünün dayandığı asıl benchmarklar. Yani Opus 5'in
Sonnet 5'e karşı **bu spesifik testlerde** ne kadar önde olduğu bilinmiyor.
Yukarıdaki genel sıçrama güçlü bir yön işareti ama **sayı değil**.

### Güvenlik sınıflandırıcısı / fallback zinciri (Fable 5.1 ile güncellendi)

| Model | Saldırı amaçlı siber işaretlenirse | Biyoloji Ar-Ge işaretlenirse |
|---|---|---|
| Fable 5.1 | → **Opus 4.8 veya Opus 5** (izinli fallback hedefleri) | → **Opus modelleri** |
| Opus 5 | → **Opus 4.8** | → **Refuse** (fallback yok) |
| Fable 5 (legacy) | → **Opus 4.8** | → **Opus 5** |

Bu tablo `SKILL.md` Adım 1'deki iki ayrı kapının kaynağı.

**Fable 5.1 ile değişen (1 Eyl 2026 duyurusu + `platform.claude.com` doğrulaması):**
- **Savunma amaçlı zafiyet keşfi artık izinli** — Fable 5.1 "yazılım zafiyetlerini
  keşfedebilir, ama onlar için exploit geliştiremez". Yalnızca **sızma testi,
  exploit üretimi, ikili-tabanlı zafiyet taraması** Opus modellerine yönlenir.
- Selim isteklerde cyber müdahaleleri **~%60**, temel biyoloji-tıp sorularında
  **~%85** azaldı.
- **Mythos 5.1** (`claude-mythos-5-1`): Fable 5.1 ile aynı model, izinli
  safeguard'lar. **Yalnızca Project Glasswing daveti** (Cyber Verification
  Program / Life Sciences Verification Program; ABD öncelikli). Normal API /
  Claude Code erişimi buna otomatik yönlenmez — ayrı, davetli model.
- Fable 5.1'in izinli fallback hedefleri resmî dokümanda **"Opus 4.8 ve Opus 5"**
  olarak listeli; router saldırı-amaçlı kapıda Opus 4.8'i seçmeye devam ediyor
  (cyber duruşu en izinli genel model).

### Claude Code sürüm gereksinimi

`Opus 5: v2.1.219+ · Sonnet 5: v2.1.197+ · Opus 4.8: v2.1.154+`

`/model opus` alias'ı v2.1.219 öncesinde Opus 4.8'e (hatta daha eskisinde
Opus 4.7'ye) çözülüyordu. Kullanıcı eski sürümdeyse `claude update` gerekir.

---

## 0.1. Fable 5.1 / Mythos 5.1 — 1 Eylül 2026 lansmanı

Fable 5.1 (`claude-fable-5-1`), Fable 5'in yerini alan frontier model.
Anthropic'in çerçevesi: *"Çoğu iş Opus 5'le başlar; Opus 5'i `xhigh`/`max`
eforda denedikten sonra zorlu akıl yürütme veya uzun-ufuklu ajanik işte hâlâ
yetersizse Fable 5.1."* Model seçim matrisinde Fable 5.1 = "en yüksek erişilebilir
kapasite" (saatlerce süren ajan oturumları, çok-adımlı derin araştırma).

**Spesifikasyon (Fable 5.1 = Mythos 5.1):**
- Bağlam 1M (varsayılan ve maks) · Maks çıktı 128k
- Fiyat: $10 / $50 MTok (Fable 5 ile **aynı**) — ama **cache okuması $0.25/MTok**
  (baz girdinin 0.025×'i; diğer tüm modellerde 0.1×). Cache'lenmiş prefix'i
  tekrar okuyan uzun ajanik oturumlar Fable 5 oranının **¼'ünü** öder.
- Cache yazma: 5dk $12.50 · 1sa $20 · min cache'lenebilir prompt **512 token**
- Efor: `low`–`max`, varsayılan **`high`** (Claude Code); **`medium`**
  (claude.ai ve Cowork). Fable 5'e göre kazanç en çok yüksek eforda.
- Adaptif düşünme her zaman açık. Bilgi kesimi **Haz 2026** (Fable 5: Oca 2026).
- Tokenizer Fable 5 ile aynı (Opus 4.7 tokenizer'ı).

**Yayınlanan benchmark iddiaları (Anthropic lansman notu, Fable 5.1 vs Fable 5):**
- Terminal-Bench-Science: %52.6 vs %24.7 (2×'ten fazla)
- Terminal-Bench 4.0: %55.8 vs %42.0
- CursorBench 3.2.0: %73.4 vs %70.5
- Opus 5'e karşı: "test edilen çoğu benchmark'ta genel olarak üstün", "token
  başına Opus 5'ten çok daha verimli" — granüler sayı azaldığı için router bunu
  yön işareti olarak alıyor, kesin üstünlük iddiası değil.

**Davranış farkları (kod değişikliği olmadan görünür — kota-ilgili):**
- **Paralel araç çağırma daha değişken** — uzun ajan döngülerinde tur başına tek
  araç çağırabiliyor (Fable 5 batch'liyordu). Ekstra tur = ekstra token + gecikme,
  cevap kalitesi düşmüyor. Prompt'a tek satırlık batch talimatı ekle.
- **`low` eforda hafızadan cevap** — arama/getirme aracını daha seyrek çağırır.
- **Küçük düzenlemede tüm dosyayı yeniden yazma** eğilimi — daha çok çıktı token'ı.
- Sohbette daha az biçimlendirme, daha yoğun düzyazı.

**Kıran değişiklikler (API'yi elle kuranlar için — Claude Code/claude.ai halleder):**
zorunlu araç kullanımı (`tool_choice: any`/`tool`) desteklenmiyor; düşünme
blokları modele bağlı; geçmişi düzenlemek düşünme bloklarını geçersiz kılıyor.

**Mythos 5.1** (`claude-mythos-5-1`): yalnızca davet (Project Glasswing).
Fable 5.1 ile aynı spesifikasyon/fiyat, izinli safeguard'lar. Emeklilik en erken
1 Eyl 2027. Router yalnızca kullanıcı Glasswing erişimini açıkça belirtirse önerir.

---

## 1. Model kapasite tablosu (Anthropic resmi)

| Özellik | Fable 5.1 | Opus 5 | Sonnet 5 | Haiku 4.5 |
|---|---|---|---|---|
| Bağlam | 1M | 1M | 1M | 200k |
| Maks çıktı | 128k | 128k | 128k | 64k |
| Fiyat (girdi/çıktı $/MTok) | $10/$50 | $5/$25 | $3/$15* | $1/$5 |
| Cache okuma ($/MTok) | **$0.25** (0.025×) | $0.50 | $0.30 | $0.10 |
| Efor desteği | low–max | low–max | low–max | **yok** |
| Efor varsayılanı | `high` (CC) / `medium` (chat) | `high` | `high` | — |
| Adaptive thinking | evet (hep açık) | evet | evet | hayır |
| Bilgi kesim tarihi | **Haz 2026** | May 2026 | Oca 2026 | Şub 2025 |

*Sonnet 5 tanıtım fiyatı ($2/$10) 31 Ağustos 2026'da bitti, standart $3/$15.
**Mythos 5.1** = Fable 5.1 ile birebir aynı spesifikasyon/fiyat (yalnızca davet).
**Fable 5** (legacy) hâlâ erişilebilir: $10/$50, cache okuma $1.00, bilgi kesimi
Oca 2026 — ama Fable 5.1 "Fable 5'in seçildiği her yerde go-to".

**Opus 4.8** (legacy, sadece siber güvenlik kapısı için önerilir): $5/$25,
1M bağlam, 128k çıktı — spesifikasyon olarak Opus 5 ile aynı, ama genel işte
Anthropic'in kendisi migrate etmeyi öneriyor.

---

## 2. Opus 4.8 dönemi benchmark verisi — ⚠️ Opus 5'e miras bırakılmaz

Aşağıdaki tablo **Opus 4.8** dönemine ait. Kural 2 ve Kural 3'ün *yönünü*
gösteriyor (Opus'un hangi alanlarda güçlü, Sonnet'in hangi alanlarda parite
kurduğu) ama **rakamları Opus 5 için kullanma** — Opus 5 muhtemelen bu
sayıların hepsinde daha iyi, tam farkı bilinmiyor.

| Benchmark | Opus 4.8 | Sonnet 5 | Fark |
|---|---|---|---|
| **SWE-bench Pro** (ajanik, çok adımlı) | **%69.2** | %63.2 | Opus +6.0 |
| **Terminal-Bench 2.1** (Terminus-2, ham) | %74.6 | **%80.4** | Sonnet +5.8 |
| **HLE (araçlı)** | %57.9 | %57.4 | Parite (±%2.65 GA) |
| **HLE (araçsız)** | **%49.8** | %43.2 | Opus +6.6 |
| **USAMO 2026** (matematik) | **%96.7** | %79.5 | Opus +17.2 |

⚠️ **Terminal-Bench: iki sayı, iki harness.** %74.6 = izole `Terminus-2` `[K1]`
(ham yetenek); %82.7 = CLI scaffolding ile `[K2]`. Ham kıyasta %74.6 geçerli.

⚠️ **GDPval-AA v2 kullanılmaz.** Anthropic'in kendi `[K1]` tablosunda Opus 4.8
için 1890 yazıyor; dolaşımdaki 1603/1615 rakamları `[K2/K3]` ve teyitsiz.
3 Elo fark zaten güven aralığı içinde. Bu satır hiçbir kuralın gerekçesi değil.

### Bu tablodan çıkan yön (rakam değil)

1. Sonnet 5, ham terminal/CLI işinde Opus 4.8'e karşı öndeydi.
2. Opus 4.8, ajanik çok-dosya kod + matematik + araçsız akıl yürütmede önde.
3. Araç erişimi Sonnet'in açığını kapatıyor (araçsız +6.6 fark → araçlı parite).

Opus 5'in genel sıçraması göz önüne alınca (1) muhtemelen zayıflamış veya tersine
dönmüş olabilir — belirsiz. (2) ve (3) muhtemelen güçlenmiş — Opus 5'in kimya/
protein/Frontier-Bench sıçraması bu yöndeki üstünlüğü destekliyor.

---

## 2.1. Bağımsız leaderboard'lar (2 Eyl 2026) — LiveBench / BenchAlign / AA Index

> **Neden bu bölüm var:** §7'nin "Opus 5 vs Sonnet 5 eşit-eforda net kıyaslama
> yayınlanmadı" boşluğu artık **kısmen** kapandı — LiveBench (kontaminasyon-serbest,
> 6 ayda bir yenilenen, bağımsız) Opus 5, Sonnet 5, Fable 5.1'i aynı sürümde
> ölçüyor. **Yine de bunlar çapraz-model, farklı-efor kıyaslar** — 0.4 puanlık
> bir aggregate farkı routing'i değiştirmez. Bu tablo Kural 2/3'ün *yönünü*
> sağlamlaştırır, yeni bir sert kapı yaratmaz.

### LiveBench 2026-06-25 (genel / reasoning / coding / **agentic coding** / math / data / language / IF · başarılı-görev başına maliyet)

| Model (efor) | Genel | Rsn | Cod | **Agt** | Mth | Dat | Lng | IF | $/görev |
|---|---|---|---|---|---|---|---|---|---|
| **Fable 5.1** (max) | 83.4 | 91.7 | 86.4 | **66.1** | 97.0 | 80.3 | 89.5 | 73.0 | $1.21 |
| Fable 5 (max) | 83.0 | 89.7 | 86.0 | 62.2 | 96.0 | 80.5 | 90.7 | 75.8 | $1.44 |
| GPT-5.6 Sol (max) | 81.0 | 91.7 | 83.9 | 56.2 | 96.2 | 79.8 | 87.7 | 71.8 | $0.52 |
| **Opus 5** (max) | 80.1 | 91.2 | 81.4 | **65.2** | 95.7 | 74.6 | 88.7 | 63.8 | $0.70 |
| GPT-5.6 Terra (max) | 77.9 | 90.6 | 78.2 | 54.9 | 94.9 | 79.3 | 82.9 | 64.6 | $0.35 |
| Opus 4.8 (max) | 76.2 | 89.2 | 81.8 | 50.5 | 94.3 | 66.0 | 79.7 | 72.0 | $0.98 |
| **Sonnet 5** (xhigh) | 76.0 | 88.7 | 80.7 | **59.4** | 92.9 | 71.7 | 75.0 | 63.9 | $0.51 |
| GPT-5.6 Luna (max) | 73.6 | 85.6 | 82.9 | 48.4 | 87.2 | 78.0 | 72.6 | 60.1 | $0.17 |

### Aggregate index'ler (Eyl 2026)
- **AA Intelligence Index:** Fable 5.1 (max) **66** · Fable 5.1 (xhigh) 65 · Opus 5
  (max/xhigh) **63** · Fable 5.1 (high) 62. Kimi K3 (max) 60 = en iyi açık-ağırlık.
- **BenchLM BenchAlign:** Fable 5.1 **82.74** (tahmini, 90% aralık 71.2–94.3) ·
  Fable 5 82.49 · Opus 5 **82.34** · GPT-5.6 Sol 81.69 · Opus 4.8 75.96.
  ⚠️ BenchAlign Sonnet 5'i **64.7 / #39** gösteriyor — bu bir **kapsama artefaktı**
  (Sonnet 5'in yalnızca 16 benchmark satırı sourced; reasoning/math "not eligible").
  LiveBench'in tam kapsamı Sonnet 5'i 76.0'da tutuyor. **Aggregate skordan routing
  yapma** — Sonnet 5 güçlü bir günlük sürücü.

### Routing'e etkisi (yön, kural değişikliği değil)
1. **Fable 5.1 ≈ Opus 5, gürültü içinde** (BenchAlign 82.74 vs 82.34; AA 66 vs 63).
   LiveBench $/başarılı-görev Fable 5.1 $1.21 vs Opus 5 $0.70 (~1.7×). → Fable 5.1'i
   **kapılı tutma** kararı doğru; genel varsayılan yapma. Kural değişmez.
2. **Agentic coding'de Opus 5 (65.2) ≈ Fable 5.1 (66.1), ikisi de Sonnet 5'in
   (59.4) ~6 puan üstünde** — kontaminasyon-serbest kaynak. → **Kural 2(a)**
   (ajanik yapılandırılmış iş → Opus 5) artık bağımsız kanıtlı.
3. **Language'da Opus 5 (88.7) vs Sonnet 5 (75.0) = +13.7; reasoning +2.5;
   math +2.8.** → **Kural 3'ün "yükselt" notu** artık daha sağlam zeminde:
   D=3 ama Kural 2 dışı işte Sonnet 5 kota-varsayılanı kalır, ama sonuç kritikse
   Opus 5'e çıkmanın somut bir gerekçesi var (sadece "kanıtsız" değil).
4. **GPT-5.6 Sol:** reasoning/math'te Opus 5'le başa baş ama **agentic coding
   zayıf** (56.2 < Sonnet 5). Codex Kolu D=3→Sol eşlemesi doğru; ama uzun ajanik
   kod işinde Sol'un Claude tarafına göre görece zayıf olduğunu (kullanıcı sorarsa) belirt.

> **Kaynaklar:** `livebench.ai` (2026-06-25 sürümü), `artificialanalysis.ai/models`,
> `benchlm.ai` — hepsi 2 Eyl 2026'da doğrudan okundu. Üçü de tepe sıralamada
> **aynı**: Fable 5.1 ≈ Fable 5 ≈ Opus 5 > Sol > diğerleri, Fable 5.1'in Opus 5
> üzerindeki farkı her üçünde de gürültü mertebesinde.

---

## 3. Efor seviyeleri

**Efor bir token bütçesi değildir.** Davranışsal bir sinyaldir: modelin **tüm**
token harcamasını etkiler — metin, araç çağrıları, düşünme.

### Model başına destek

| Model | Seviyeler | Varsayılan |
|---|---|---|
| **Fable 5.1** / Mythos 5.1 | low, medium, high, xhigh, max | high (Claude Code) · medium (claude.ai / Cowork) |
| Fable 5 (legacy) | low, medium, high, xhigh, max | high |
| **Opus 5** | low, medium, high, xhigh, max | high |
| Sonnet 5 | low, medium, high, xhigh, max | high |
| Opus 4.8 | low, medium, high, xhigh, max | high |
| Opus 4.7 | low, medium, high, xhigh, max | **xhigh** (istisna) |
| Opus 4.6, Sonnet 4.6 | low, medium, high, max (**xhigh yok**) | high |
| Haiku 4.5 | **yok** | — |

`xhigh` istenip desteklenmiyorsa en yakın alttaki desteklenen seviyeye düşer
(örn. Opus 4.6'da `xhigh` → `high`).

### Model başına tavsiye (Anthropic'in kendi metni)

- **Opus 5:** `high`'dan (varsayılan) başla. Kodlama/ajanik işte `xhigh`'a
  çık, gerçek frontier problemde `max`'a. **"low ve medium'u eval'in tuttuğu
  her yerde maliyet/hız kontrolü için serbestçe kullan."** — önceki Opus
  nesillerinden kasıtlı bir ton farkı; low/medium artık "kısıtlanmış mod"
  değil, normal bir kadran.
- **Sonnet 5:** `high` varsayılan. En zor kodlama/ajanik işte `xhigh`.
  `medium` ≈ "Sonnet 4.6'nın `high`'ı".
- **Opus 4.8/4.7:** kodlama/ajanik işte `xhigh`'dan başla; `low`/`medium`'a
  ancak eval'le ölçüp inersin (Opus 5'ten daha muhafazakâr tavsiye).
- **Fable 5.1:** `high` (Claude Code varsayılanı) veya `medium` (chat varsayılanı)
  başla, eval'le ayarla. Fable 5'e göre kazanç en çok yüksek eforda. `low` eforda
  arama/getirme aracını daha seyrek çağırır — taze bilgi gereken turda eforu yükselt
  (Fable 5.1 mid-conversation efor değişimini destekliyor, cache'i bozmadan).

### `ultracode` — Claude Code seviyesi

`/effort` menüsünde **`ultracode` vardır.** Bir *model* efor seviyesi değil:

> "Ultracode is a Claude Code setting rather than a model effort level: it sends
> `xhigh` to the model and additionally has Claude orchestrate dynamic workflows
> for substantive tasks. It applies to the current session only."

- **Model kısıtı yok** — `xhigh` destekleyen her modelde çalışır: Fable 5.1,
  Sonnet 5, **Opus 5**, Opus 4.8, Opus 4.7. Haiku 4.5'te çalışmaz.
  Opus 4.6/Sonnet 4.6'da `xhigh` yok → `ultracode` istenirse `high`'a düşer.
- Açma yolları: `/effort ultracode` · `claude --effort ultracode` ·
  `--settings` ile `"ultracode": true` · Agent SDK `effortLevel: "ultracode"`
- **Oturumluk.** Ayar dosyasına ve `CLAUDE_CODE_EFFORT_LEVEL`'a yazılamaz.
- Workflow'lar kapalıysa `--effort ultracode` yalnızca `xhigh` uygular.

### `ultrathink` — tek seferlik derinlik

Prompt içine `ultrathink` yaz → o tur için daha derin akıl yürütme, **efor
seviyesi değişmez**. "think", "think hard" gibi ifadeler tanınmaz.

### `ultracode` ne zaman kullanılır

- **Evet:** 100+ dosyalık denetim, devasa migration, 3+ bağımsız doğrulama
  açısı gerektiren çapraz doğrulama, rekabet analizi, PRD incelemesi.
- **Hayır:** Tek dosya düzenlemesi, hızlı soru, gündelik iş.
- **Çakışma:** `ultracode` modele yalnızca `xhigh` gönderir; `max`'a ihtiyaç
  varsa `ultracode` seçme.

### `opusplan` — plan/yürütme model ayrımı

**Yalnızca Claude Code'da var** (`/model opusplan`), Claude.ai'da karşılığı yok.
Resmî tanım:

> "The `opusplan` model alias provides an automated hybrid approach:
> In plan mode: uses `opus` for complex reasoning and architecture decisions.
> In execution mode: automatically switches to `sonnet` for code generation
> and implementation. This pairs Opus's reasoning for planning with Sonnet's
> efficiency for execution."

Doğrulanmış davranış detayları:
- **Bağlam penceresi:** Plan fazındaki Opus, `opus` ayarıyla aynı bağlam
  penceresini kullanır. Otomatik 1M yükseltmesi olan planlarda plan fazı da
  yükseltilir. Yükseltme yoksa iki fazı da 1M'e zorlamak için `opusplan[1m]`.
- **Allowlist kısıtlaması varsa:** en yeni izinli Opus sürümü planlamada
  kullanılır; hiç Opus izinli değilse plan fazı da Sonnet'te kalır.
- **⚠️ Efor otomatik geçmez.** Opus 5 ve Sonnet 5'in ikisi de "hold"suz model
  (bkz. §3 "Varsayılanlar") — yani plan modunda ayarlanan efor, yürütmeye
  geçince **aynen taşınır**, otomatik düşmez. Kullanıcı yürütme fazına
  geçtiğinde eforu elle indirmezse, Sonnet 5 gereksiz yere yüksek eforla
  çalışır ve `opusplan`'ın kota tasarrufu amacı geçersiz kalır. **Bu, router'ın
  opusplan önerdiği her çıktıya eklemesi gereken zorunlu bir uyarı.**
- **İlgili ama farklı bir özellik — "advisor tool":** Resmî dokümanda şuna
  atıf var: *"For a hybrid approach where Claude decides mid-task when to
  consult a second model rather than switching at the plan boundary, see the
  advisor tool."* Bu, opusplan'ın sabit plan/yürütme sınırından farklı olarak
  görev ortasında ikinci bir modele danışma mekanizması — router bunu **henüz
  incelemedi**, kural setine dahil edilmedi. Gelecekte araştırılabilir.

### `opusplan` ne zaman kullanılır — ayırt edici teşhis

Router'ın `opusplan`'ı önermesi için üç şart birden gerekir (bkz. `SKILL.md`
Adım 3): D=3 ∧ Kural 2(a) alanı, zorluk plana ön-yüklü, W≥2.

**En kritik ayrım — zorluk nerede yoğunlaşıyor:**

| Zorluk türü | Örnek | opusplan uygun mu |
|---|---|---|
| Ön-yüklü: plan bitince yürütme tekrarlayan bir kalıp | "40 servisi ortak middleware'e geçir, tasarımı bir kez belirle" | ✅ |
| Kalıcı: her yürütme adımı kendi başına keşif/yargı gerektiriyor | Race condition avı — kod okumadan neden bilinmez | ❌ |
| Kalıcı: plan ile yürütme ayrılamaz, ispatın kendisi iştir | Formel correctness kanıtı | ❌ |
| Hacim yetersiz (W≤1) | Küçük bir mimari karar, tek dosya etkisi | ❌ — düz Opus 5 yeterli, mod değişimi ek yük |

**Canlı test bulgusu (bu oturumdan):** Bu router'ın kendi mimarisini yeniden
tasarlama görevi (Kural 2a'ya giriyor, D=3) `opusplan`'a **girmiyordu** —
hem W=1 (az dosya) hem de yürütme boyunca (kural yazarken sürekli test/düzeltme
gerekti) zorluk kalıcıydı, plan bir kerede mekanikleşmedi. Bu, kriterin
gerçek bir vaka üzerinde doğru ayrım yaptığının kanıtı.

---

## 4. Fiyatlandırma (MTok başına) — 1 Eylül 2026

| Model | Girdi | Çıktı | Cache yazma (5dk) | Cache okuma |
|---|---|---|---|---|
| **Fable 5.1** / Mythos 5.1 | $10.00 | $50.00 | $12.50 | **$0.25** |
| Fable 5 (legacy) | $10.00 | $50.00 | $12.50 | $1.00 |
| **Opus 5** | $5.00 | $25.00 | $6.25 | $0.50 |
| Opus 4.8 (legacy) | $5.00 | $25.00 | $6.25 | $0.50 |
| Opus 4.8 (Fast Mode) | $10.00 | $50.00 | $12.50 | $1.00 |
| Sonnet 5 (promo bitti 31 Ağu 2026) | $3.00 | $15.00 | $3.75 | $0.30 |
| Haiku 4.5 | $1.00 | $5.00 | $1.25 | $0.10 |

**Fable 5.1 cache okuması:** baz girdinin **0.025×'i** (diğer tüm modeller 0.1×).
Cache'lenmiş prefix'i tekrar okuyan uzun ajanik oturumlar Fable 5 oranının
**¼'ünü** öder — Fable 5.1'i frontier kapısında önermek, Fable 5 dönemine göre
kota açısından belirgin şekilde daha ucuz. Batch: $5 / $25.

**Opus 5 / Sonnet 5 oranı:** 1.67× (promo bitti). Abonelik kullanıcısı için bu,
kota yakma hızının kaba bir vekil göstergesi.

**Fast Mode artık Opus 5'i de kapsıyor** (araştırma önizlemesi): $10/$50,
2.5× hızlı çıktı. Opus 4.7'de yok, Opus 4.6'da standart hızda/fiyatta çalışır.

**Tokenizer enflasyonu:** Opus 4.7+ tokenizer'ı aynı metin için ~%30 daha
fazla token üretiyor (İngilizce 1.4×). Opus 5, Fable 5.1, Fable 5, Sonnet 5
hepsi bu tokenizer'ı kullanıyor.

**Batch API:** tüm modellerde %50 indirim.

---

## 5. Abonelik planları ve varsayılan model

| Plan | Ücret | Claude Code | Varsayılan model |
|---|---|---|---|
| Pro | $20/ay | ✅ | **Sonnet 5** |
| Max 5x / Max 20x | $100 / $200/ay | ✅ | **Opus 5** |
| Team Standard | $25/koltuk | ❌ **YOK** | — |
| Team Premium | $125/koltuk | ✅ | **Opus 5** |
| Enterprise (subscription seat) | — | ✅ | **Sonnet 5** |
| Enterprise (pay-as-you-go) / API | — | ✅ | **Opus 5** |

Opus 5 lansmanıyla varsayılanlar değişti: Max/Team Premium/Enterprise-PAYG/API
artık otomatik **Opus 5**'e geçti (önceden Opus 4.8). Pro ve Team Standard
hâlâ **Sonnet 5**.

❌ **Çürütüldü: "5 saatlik pencerede 10–40 prompt" diye sabit bir kota yok.**
Kotalar her 5 saatte sıfırlanır ama sayı değil **token + bağlam uzunluğu**
üzerinden erir.

**Agent SDK kredileri:** Pro $20, Max 5x $100, Max 20x $200 — yalnızca SDK'da
geçerli, birey bazında.

---

## 6. Gizli kota yakıcılar

1. **MCP sunucuları.** Her sunucu araç şemalarını her mesaja enjekte eder. Yük
   sunucu başına sabit değil, **araç sayısıyla orantılı** (GitHub MCP: 27 araç
   ≈ 18k token; Playwright: 21 araç ≈ 13.6k).
2. **Auto-accept sürekli açık.** Zincirleme düzenlemeler "geometrik maliyet
   makinesi" yaratır.
3. **Prompt caching kullanmamak.** Cache okuma %90'a varan indirim (Fable 5.1'de
   **%97.5** — cache okuma baz girdinin 0.025×'i). Minimum cache'lenebilir metin:
   Opus modellerinde 4096 token, **Fable 5.1'de 512**.

---

## 7. Veri durumu

### ✅ Çözüldü / doğrulandı

- **Opus 5 gerçek**, 24 Temmuz 2026'da çıktı, Opus 4.8'in yerini aldı.
- **Fable 5.1 / Mythos 5.1 gerçek**, 1 Eylül 2026'da çıktı (`claude-fable-5-1` /
  `claude-mythos-5-1`). Fable 5.1 tüm müşterilere açık; Mythos 5.1 yalnızca
  Project Glasswing daveti. Spesifikasyon/fiyat aynı; cache okuma $0.25/MTok;
  bilgi kesimi Haz 2026. `platform.claude.com/docs/en/models/fable-5-1/*` ile
  doğrulandı (2 Eyl 2026).
- Fable 5.1 saldırı-amaçlı cyber fallback hedefleri: **Opus 4.8 ve Opus 5**
  (resmî doküman). Savunma amaçlı zafiyet keşfi Fable 5.1'de artık izinli.
  Biyoloji Ar-Ge → Opus modelleri; Opus 5'in kendisi biyoloji Ar-Ge'yi reddeder.
- Fable 5 (legacy) fallback zinciri: cyber→Opus 4.8, biyoloji→Opus 5.
- `task_budget` asgarisi = 20.000 token. "2.000" iddiası `max_tokens` ile
  karıştırılmadan doğmuş, yanlış.
- Terminal-Bench'teki iki sayı (%74.6/%82.7) harness farkı, çelişki değil.
- `ultracode` API'de yok; Claude Code CLI'nin `xhigh`+workflow makrosu.

### ❌ Çürütüldü — router'a girmemeli

| İddia | Gerçek |
|---|---|
| Efor seviyelerinin token bütçeleri (~1.024/~4.000/~8.000) | Böyle bir bütçe yok |
| `task_budget` asgarisi 2.000 | 20.000 |
| "5 saatlik pencerede 10–40 prompt" | Kota token+bağlam üzerinden erir |
| Her MCP sunucusu sabit 18k token | Araç sayısıyla orantılı |
| GDPval'de "Sonnet 5 Opus'u geçti" | 3 Elo anlamlı değil, Opus'un K1 skoru 1890 |
| Opus 4.8'in benchmark profili Opus 5'e de geçerli | **Ayrı model**, granüler karşılaştırma yayınlanmadı |

### ⚠️ Hâlâ belirsiz

- **Opus 5 vs Sonnet 5**, Anthropic'in kendi SWE-bench Pro / Terminal-Bench /
  HLE eşit-efor kıyası hâlâ yayınlanmadı — ama **LiveBench 2026-06-25** (bağımsız,
  kontaminasyon-serbest) artık ikisini aynı sürümde ölçüyor (bkz. §2.1):
  agentic coding Opus +5.8, language Opus +13.7, reasoning Opus +2.5. Kural 3
  hâlâ kota gerekçesiyle Sonnet 5'i varsayılan tutuyor ama "yükselt" notu artık
  kanıtsız değil.
- **GPQA Diamond / Fable 5.** %87.8 `[K3]` — Opus 4.8'in %93.6'sının altında,
  eski raporlarla çelişiyor. Fable'ın GPQA üstünlüğü teyitsiz.
- Fable 5.1'in biyoloji Ar-Ge işaretli isteği hangi Opus'a (4.8 mi 5 mi)
  yönlttiği net değil — resmî metin sadece "Opus modelleri" diyor. Router bunu
  aşırı belirtmiyor: biyoloji-bitişik iş → Fable 5.1 öner, yönlendirme beklenen.
- Codex/ChatGPT tarafında savunma-amaçlı zafiyet keşfi için Claude'unki gibi bir
  izinli-safeguard davranışı **araştırılmadı** — Codex Kolu bu kategoride yine
  normal skorlamadan geçiyor (yalnızca saldırı-amaçlı + biyoloji Ar-Ge'de
  "doğrulanmadı" diyor).

---

## 8. Örnek kütüphanesi — skorlarken analoji için kullan

Her satır: prompt → R,D,W,C → model·efor. Kodlama dışı alanlar da dahil,
çünkü SKILL.md'nin varsayılan okuması kodlamaya kayıyor. Kendi promptun bu
listedeki bir örneğe benziyorsa, o örneğin skorunu başlangıç noktası yap.

### Kodlama

| Prompt | R,D,W,C | → |
|---|---|---|
| "Bu fonksiyondaki typo'yu düzelt" | 1,0,0,0 | Haiku 4.5 *(D=0, gerçekten trivial)* |
| "Şu API endpoint'ine input validasyonu ekle" | 1,1,0,0 | Sonnet 5 · medium *(D=1 "bilinen kalıp" → Haiku değil)* |
| "Bu bileşene dark mode desteği ekle" | 1,1,1,1 | Sonnet 5 · medium |
| "3 servisi ortak bir auth middleware'de birleştir" | 2,2,2,2 | Sonnet 5 · high |
| "Bu cache invalidation mantığındaki race condition'ı bul ve düzelt" | 2,3,1,2 | Opus 5 · xhigh *(ajanik kod domaini)* |
| "Monolit'i 12 mikroservise ayır, veri tutarlılığı dahil" | 3,3,3,3 | Opus 5 · max, ultracode **hayır** *(D=3∧R=3 çakışması)* |
| "500 dosyada eski logging kütüphanesinden yeniye geçir" | 1,1,3,1 | Sonnet 5 · **ultracode** *(ultracode tetiklenince efor alanı D'nin değerini değil "ultracode"u yazar)* |
| "Bu SQL sorgusunu N+1'den kurtar" | 1,1,0,0 | Sonnet 5 · medium *(D=1 "bilinen bug deseni" → Haiku değil)* |
| "Yeni bir rate-limiter algoritması tasarla, dağıtık sistemde tutarlı olsun" | 2,3,1,1 | Opus 5 · xhigh *(algoritmik derinlik)* |

### Yapılandırılmış sistem tasarımı (kod değil ama Kural 2a'ya girer)

Canlı testte bulundu: Kural 2(a) sadece "programlama dili kodu"na bakınca,
kural motoru/prompt mimarisi gibi işler yanlışlıkla varsayılan Sonnet'e
düşüyordu. Bu kategori, Kural 2(a)'nın kod-dışı da kapsadığını gösterir.

| Prompt | R,D,W,C | → |
|---|---|---|
| "Bu router'ın model seçimini riskten ayrıştır, çakışma kurallarını sıfırdan tasarla" | 1,3,1,2 | Opus 5 · xhigh *(yapılandırılmış sistem tasarımı — Kural 2a)* |
| "Bu skill'in eksen tanımlarına örnek ve karşı-örnek ekleyerek zenginleştir" | 1,2,1,1 | Sonnet 5 · high *(var olan çerçeveyi genişletme, sıfırdan tasarım değil)* |
| "Yeni bir karar ağacı kur: 5 girdiye göre 3 çıktı arasında seçim yapsın" | 1,3,0,1 | Opus 5 · xhigh *(karar mantığı tasarımı, kod değil ama D=3)* |

### Yazı / analiz / hukuki-iş

| Prompt | R,D,W,C | → |
|---|---|---|
| "Bu e-postayı daha kibar bir dille yeniden yaz" | 1,0,0,0 | Haiku 4.5 |
| "Bu toplantı notlarını 5 maddeye özetle" | 1,1,0,1 | Sonnet 5 · medium |
| "3 rakip firmanın fiyatlandırmasını karşılaştıran rapor yaz" | 1,2,1,2 | Sonnet 5 · high |
| "40 sayfalık sözleşmede tahkim maddesiyle çelişen hükümleri bul" | 2,3,1,2 | Sonnet 5 · xhigh *(Kural 2 dışı → varsayılan ucuz)* |
| "Bu iddianameye karşı hukuki savunma stratejisi kur (olgular promptta verilmiş, dosya okumaya gerek yok)" | 3,3,1,1 | Opus 5 · max *(araçsız derin akıl yürütme — Kural 2c; R=3 modeli değil eforu `max`'a çekiyor)* |
| "300 sayfalık API dokümantasyonunu oku, deprecated endpoint'leri listele" | 1,1,1,3 | Sonnet 5 · medium *(C=3 tek başına Opus'u tetiklemez)* |

### Araştırma / veri

| Prompt | R,D,W,C | → |
|---|---|---|
| "Bu CSV'deki aylık satış toplamını hesapla" | 1,0,0,0 | Haiku 4.5 |
| "Bu iki veri setini karşılaştır, anomalileri işaretle" | 1,1,1,1 | Sonnet 5 · medium |
| "Kullanıcı churn'üne neden olan faktörleri regresyon ile bul" | 1,3,1,2 | Sonnet 5 · xhigh *(istatistiksel modelleme, ajanik kod değil ama araç kullanıyor)* |
| "10 akademik makaleyi sentezleyip yeni bir hipotez öner" | 1,3,1,3 | Sonnet 5 · xhigh *(araştırma D=3, Kural 2 dışı)* |
| "Kod çalıştırmadan, sadece literatür bilginle, X teorisinin Y'ye üstünlüğünü tart" | 1,3,0,1 | **Opus 5 · xhigh** *(gerçek araçsız derin akıl yürütme — Kural 2c)* |

### Ops / DevSecOps (siber güvenlik hariç — o sert kapıda)

| Prompt | R,D,W,C | → |
|---|---|---|
| "CI pipeline'ındaki flaky testi bul" | 1,1,1,0 | Sonnet 5 · medium |
| "180 servisi performans regresyonu için profille" | 2,2,3,2 | Sonnet 5 · **ultracode** *(W=3 tetikledi; efor alanı D'nin `high`'ını değil "ultracode"u yazar)* |
| "Prod'da CPU spike'ına neden olan deploy'u bul, henüz rollback yapma" | 2,2,1,2 | Sonnet 5 · high |
| "Kubernetes cluster'ını sıfırdan multi-region HA'ya taşı" | 3,3,2,2 | Opus 5 · max |

### Adım 0 örnekleri (netleştirme istenmeli, skorlama başlamaz)

Bu kategori canlı bir kullanıcı örneğiyle doğrulandı: Adım 0'ın eski hâli
("başarı kriteri/kapsam yoksa sor") çok kaba kaldı ve gerçek kullanımda hiç
tetiklenmedi. Aşağıdaki örneklerin hepsinde kapsam **var görünüyor** ama
kritik bir parametre örnekle anlatılmış, genellenmemiş.

| Prompt | Neden Adım 0 tetiklenir |
|---|---|
| "Bir günde 1000 üretim olursa 500'ü aynı güne, 500'ü ertesi güne yansısın" | Sabit 500 mü, %50 mi, saat bazlı kesim mi belirsiz — örnek genel kuralın yerine geçmiyor |
| "Büyük siparişlerde ekstra indirim uygula, mesela 10.000 TL üzerinde %5 gibi" | "Gibi" kelimesi eşiğin ve oranın kesin olmadığını gösteriyor |
| "Bu tabloyu performans için optimize et" | "Performans" ölçütü yok — gecikme mi, throughput mu, hangi sorgu mu |
| "Kullanıcı aktif değilse hesabı pasife çek" | "Aktif değil" tanımsız — kaç gün, hangi eylem eksikliği |

**Karşı-örnek (Adım 0 tetiklenmez):** "Bu tabloya `deleted_at` sütunu ekle ve
soft-delete uygula, `DELETE` yerine bu alanı güncelle" — kural tam, tek
yorum çıkar, kapsam somut. Doğrudan skorlamaya geç.

### Sert kapı örnekleri (skorlama devre dışı)

| Prompt | Kapı | → |
|---|---|---|
| "1000 destek talebini kategorilere ayır" | Hacim | Haiku 4.5 |
| "Şu ortama sızma testi yap, exploit zinciri kur" | Saldırı amaçlı siber | Opus 4.8 · xhigh |
| "Bu API kodunu auth bypass açığı için denetle" | **Kapı YOK** (savunma) → normal skorlama | Sonnet 5 · xhigh (Fable 5.1 de yapabilir) |
| "Bu protein katlanma simülasyonu kodunu optimize et" | Biyoloji-bitişik Ar-Ge | Fable 5.1 · high |
| "800k tokenlik log geçmişini analiz et" | Bağlam >200k | Haiku elenir → Sonnet 5/Opus 5 |

---

## 9. Codex / ChatGPT Ekosistemi (dual-provider genişlemesi, 5 Ağustos 2026)

> **Kaynak durumu:** Kullanıcı bir "Güncel Codex Plus Modelleri Raporu" verdi
> — SEO/toplayıcı sitelerden derlenmiş (gradually.ai, felloai.com,
> analyticsvidhya, datacamp, mindstudio.ai vb.), resmî OpenAI dokümanı değil.
> Tıpkı bu projenin başındaki Claude raporları gibi, **doğrudan güvenilmedi** —
> `openai.com/index/gpt-5-6/`, `developers.openai.com/api/docs/guides/reasoning`,
> `developers.openai.com/api/docs/guides/latest-model`,
> `learn.chatgpt.com/docs/config-file/config-reference` ile çapraz doğrulandı.

### 9.1. Model ailesi — GPT-5.6 (Sol, Terra, Luna)

9 Temmuz 2026'da genel erişime açıldı. Sol amiral gemisi, Terra dengeli
orta-katman, Luna hız/maliyet odaklı bütçe modeli — resmî lansman sayfasından
doğrudan doğrulandı.

**Sol Ultra:** 26 Haziran 2026'da tanıtıldı, 9 Temmuz'da genel erişime açıldı.
Tek bir akıl yürütme zinciri yerine görevi ayrıştırıp gerçek zamanlı iletişim
kuran işbirlikçi alt-ajanlar (subagent) oluşturuyor. Varsayılan 4 paralel
ajan; "multiagent v2" modunda 64'e kadar çıkabiliyor. Codex CLI istemcisine
entegre. Context penceresi GPT-5.5'ten **%43 daha büyük** (~1.5M token —
tek kaynaklı iddia, resmî sayfadan doğrudan teyit edilemedi).

### 9.2. Fiyatlandırma (MTok başına) — 30 Temmuz 2026 indirimi sonrası

| Model | Girdi | Çıktı |
|---|---|---|
| Sol | $5.00 | $30.00 |
| Terra | $2.00 | $12.00 |
| Luna | $0.20 | $1.20 |

**Kullanıcının raporu eskiydi:** Terra $2.50/$15, Luna $1/$6 diyordu — bunlar
30 Temmuz'dan **önceki** fiyatlar. O tarihte OpenAI Luna'yı %80, Terra'yı %20
indirdi, Sol sabit kaldı. Çıktı fiyatı her üç modelde de girdinin **6 katı**
(sabit oran).

### 9.3. Efor / akıl yürütme mekaniği — rapordaki tek-boyutlu merdiven YANLIŞ

Rapor "Instant→Low→Medium→High→Extra High→Max→Ultra" diye tek bir doğrusal
merdiven tanımlıyor. Resmî dokümanlar **iki ayrı, birbirinden bağımsız
eksen** olduğunu gösteriyor:

1. **`reasoning.effort`** — API'de (`developers.openai.com/api/docs/guides/reasoning`)
   desteklenen değerler: `none, minimal, low, medium, high, xhigh, max`
   (model bazlı değişir). Codex CLI `config.toml`'da (`model_reasoning_effort`)
   ise sadece **`minimal, low, medium, high, xhigh`** doğrulandı — `none` ve
   `max` orada geçmiyor. Varsayılan: `medium`.
2. **`reasoning.mode`** — `standard` (varsayılan) veya `pro`. Resmî metin:
   *"Reasoning mode and reasoning effort are independent. Mode selects
   standard or pro execution, while reasoning.effort controls how much
   reasoning the model applies within that mode."* Bu, **yalnızca Responses
   API**'de (programatik kullanım) doğrulandı — Codex CLI config referansında
   `reasoning.mode`/`model_reasoning_mode` diye bir anahtar **bulunamadı**.

**Sonuç:** `max` ve `mode: pro`, Claude'un `ultracode`'u gibi "API'de var ama
CLI'de resmî olarak yok/doğrulanmadı" kategorisinde — router bunları tavan
olarak kullanmıyor, sadece bilgi notu olarak (kullanıcı sorarsa) sunuyor.

**Ultra bir efor seviyesi değil, ayrı bir orkestrasyon modu.** Codex CLI'nin
resmî config referansında `agents.default_subagent_model`,
`agents.default_subagent_reasoning_effort` ve alt-ajan sayısını sınırlayan
bir `agents` tablosu var — "Ultra" pazarlama/topluluk terimi, altındaki gerçek
mekanizma bu config anahtarları. Bu, Claude'un `ultracode`'unun "Claude Code
ayarı, API parametresi değil" statüsüyle simetrik ama **daha güçlü** bir
mekanizma: gerçek eşzamanlı, işbirlikçi çoklu model örneği.

### 9.4. ChatGPT Plus kotaları

| Katman | Kapasite | Not |
|---|---|---|
| Instant (hızlı) | ~160 mesaj / 3 saat | Bir kaynakta GPT-5.5'e atfedilmiş, GPT-5.6'ya taşınıp taşınmadığı taze doğrulanmadı — mekanizma muhtemelen devam ediyor |
| Thinking (akıl yürütme) | ~3.000 mesaj / hafta | Aynı doğrulama notu geçerli |
| Dosya yükleme | ~80 dosya / 3 saat | Tepe saatlerde düşebilir |

⚠️ Bu kota sayıları **help.openai.com'un kendi güncel makalesiyle taze
doğrulanmadı** (arama sonuçları üzerinden dolaylı teyit edildi) — router'a
"muhtemelen doğru, kesin değil" notuyla giriyor, kesin rakam olarak kullanma.

### 9.5. Benchmark durumu — Terminal-Bench 2.1 rakamları ÇELİŞKİLİ, kural gerekçesi olarak kullanılmadı

Kullanıcının raporu tek bir kesin sıralama veriyordu (Sol Ultra 91.9%, Sol
88.8%, Terra 87.4%, Luna 84.7%, Claude Fable 5 86.0%). Bağımsız kaynaklar
taradığında **üç farklı metodoloji, üç farklı sıralama** bulundu:

| Kaynak/metodoloji | Sonuç |
|---|---|
| "Resolution rate" metodolojisi | Opus 5 (max) %43.5 önde, GPT-5.6 Sol (max) %34.4, Fable 5 (max) %33.8 |
| Artificial Analysis | GPT-5.6 Sol (xhigh) %89.5 önde, Opus 5 (max) %89.1, Terra (max) %88.0 |
| Başka bir kaynak | Opus 5 %89.1 önde, Sol %88.8 |

**Bu router hiçbir Terminal-Bench rakamını "Claude/Codex hangisi daha
iyi" kararının gerekçesi olarak kullanmıyor** — Claude-içi kıyaslarda
uygulanan aynı disiplin (bkz. §2 "GDPval-AA v2 kullanılmaz" örneği) burada da
geçerli. Zaten 5 Ağustos 2026'dan itibaren router **ikisini birden**
öneriyor (bkz. `SKILL.md` "Çıktı formatı") — hangisinin "daha iyi" olduğuna
karar vermek zorunda değil, bu yüzden çelişkili benchmark rakamları artık
mimari açıdan da önemsiz.

**LiveBench 2026-06-25 (§2.1) tek istisna:** aynı sürümde, aynı metodolojiyle
hem Claude hem GPT-5.6 ölçülüyor — router bunu Codex Kolu için tek bir yön
işareti olarak kullanıyor: **GPT-5.6 Sol reasoning/math'te Opus 5'le başa baş
ama agentic coding'de zayıf** (Sol 56.2 vs Sonnet 5 59.4 vs Opus 5 65.2). Yani
Codex D=3→Sol eşlemesi korunuyor ama uzun ajanik kod işinde Sol'un Claude
tarafına göre görece dezavantajlı olduğu (kullanıcı sorarsa) belirtilir.

### 9.6. Veri durumu özeti

**✅ Doğrulandı (resmî kaynak):**
- GPT-5.6 Sol/Terra/Luna ailesi, 9 Temmuz 2026 genel erişim.
- Güncel fiyatlar (§9.2), 30 Temmuz indirimi.
- **LiveBench 2026-06-25 (§2.1):** GPT-5.6 Sol/Terra/Luna, Claude Fable 5.1/
  Opus 5/Sonnet 5 aynı sürümde ölçüldü. Sol reasoning/math'te başa baş, agentic
  coding'de zayıf (56.2). `livebench.ai` — 2 Eyl 2026 doğrudan okundu.
- `reasoning.effort` ve `reasoning.mode`'un birbirinden bağımsız iki eksen
  olduğu; Codex CLI'nin sadece effort'u (minimal-xhigh) desteklediği.
- Sol Ultra'nın varlığı, alt-ajan config anahtarları (`agents.*`).
- Codex CLI model seçimi: `--model`/`-m` bayrağı, `config.toml`'da `model` anahtarı.

**❌ Çürütüldü (rapor yanlıştı):**
- Terra/Luna'nın eski fiyatları ($2.50/$15, $1/$6).
- Tek boyutlu "Instant→...→Ultra" efor merdiveni — gerçekte iki bağımsız eksen
  (effort × mode) + ayrı bir orkestrasyon modu (Ultra).

**⚠️ Doğrulanamadı / araştırılmadı — router'a girmedi:**
- Codex/ChatGPT tarafında siber güvenlik veya biyoloji-bitişik içerik için
  Claude'unkine benzer bir güvenlik-sınıflandırıcı/fallback zinciri olup
  olmadığı. Bu belirsizlik yüzünden Codex Kolu bu iki kategoride model
  önermiyor, "doğrulanmadı — Claude kullan" yazıyor.
- Luna/Terra/Sol-base için model başına context pencere boyutu (sadece Sol
  Ultra için ~1.5M tek-kaynaklı bir iddia var).
- ChatGPT Plus kota rakamlarının GPT-5.6'ya taşınıp taşınmadığı (§9.4).
- `reasoning.mode: pro`'nun Codex CLI üzerinden herhangi bir şekilde
  ayarlanıp ayarlanamayacağı (config referansında yok, belki `--config`
  override ile mümkün olabilir, denenmedi).
- Terminal-Bench 2.1 ve benzeri çapraz-sağlayıcı benchmark'ların kesin
  sıralaması (§9.5) — çelişkili, kural gerekçesi olarak kullanılmadı.
