# Research provenance

Bu dosya router'ı besleyen veri araştırmasının **tekrarlanabilir kaydıdır**.
Skill'in parçası değildir, çalışma zamanında hiçbir şey okumaz.

İki bölüm var:

1. **[Araştırma kaydı — 10 Eylül 2026 (iteration-16)](#arastirma-kaydi--10-eylul-2026-iteration-16)**
   — benchmark-aware routing motorunun dayandığı araştırma. Ne arandı, hangi
   kaynak hiyerarşisi kullanıldı, ne doğrulandı, ne çürütüldü, ne
   doğrulanamadı, hangi routing kuralları değişti.
2. **[Ek: Gemini Deep Research prompt'u (2026 ortası)](#ek--gemini-deep-research-promptu-2026-ortasi)**
   — `reference.md` §7'deki eski açık soruları kapatmak için kullanılan orijinal
   araştırma prompt'u. Tarihsel; kaynak disiplininin nasıl kurulduğunu gösterdiği
   için korunuyor.

---

## Araştırma kaydı — 10 Eylül 2026 (iteration-16)

**Amaç.** Router'ı yalnız R/D/W/C'den model seçen bir sistemden;
**task capability + benchmark evidence + model×effort capability + token/quota
efficiency** dörtlüsünü birlikte değerlendiren bir sisteme taşımak. Bunun için
mevcut roster'ların, effort merdivenlerinin ve göreve özgü benchmark'ların
güncel ve **karşılaştırılabilir** biçimde kaydedilmesi gerekiyordu.

### Yöntem ve kısıt

⚠️ **Bu pass boyunca web araması (WebSearch) kullanılamadı.** Tüm araştırma,
bilinen birincil URL'lerin doğrudan çekilmesiyle (WebFetch) yapıldı. Sonuç:
*aranarak bulunacak* her şey bu pass'te eksik kaldı — özellikle benchmark
sahiplerinin kendi leaderboard tabloları. Bu, §12.4'te tek tek yazılı.

### Kaynak hiyerarşisi (uygulanan)

| Katman | Ne sayılır | Bu pass'te kullanılanlar |
|---|---|---|
| **A — birincil** | Model üreticisinin resmî dokümanı, lansman yazısı, system card | `platform.claude.com/docs/*` (models/overview, effort, pricing, choosing-a-model, fable-5-1/*, opus-5/*) · `code.claude.com/docs/en/model-config` · `anthropic.com/claude-fable-and-mythos-5-1` · `anthropic.com/news/claude-opus-5` · `developers.openai.com/api/docs/models/gpt-6-astra` · `developers.openai.com/api/docs/guides/reasoning` · `developers.openai.com/api/docs/guides/latest-model` · `learn.chatgpt.com/docs/models` · `deploymentsafety.openai.com/gpt-6-astra` |
| **B — benchmark sahibi / bağımsız değerlendirici** | Leaderboard yayıncısı, ciddi bağımsız evaluator | `artificialanalysis.ai/leaderboards/models` · `artificialanalysis.ai/methodology/intelligence-benchmarking` · `tbench.ai/leaderboard` (erişildi, tablo render olmadı) |
| **C — yardımcı sinyal** | Blog, forum, agregatör **ve bu repo'nun doğrulanmadan taşıdığı eski rakamlar** | iteration-13/15'ten devralınan LiveBench 2026-06-25, OSWorld V2, DeepSWE v1.1, "Codex Coding Agent Index" satırları |

**Kural:** Katman C tek başına routing kuralı üretemez. Bir Katman C rakamı bir
kuralın *tek* dayanağıysa, ya kural yeniden temellendirilir ya da kural
"low-confidence" işaretiyle çıkar. Bu pass'te ikisi de yapıldı.

### Kullanılan benchmark'lar ve bağlandıkları capability

| Capability | Benchmark | Kaynak / katman |
|---|---|---|
| agentic-code, terminal-tool | **Terminal-Bench 4.0** · **CursorBench 3.2.0** | Anthropic lansman notu (A, vendor-run) |
| science | **Terminal-Bench-Science 0.1** (SE ±3.5–4.5 yayımlı) | A, vendor-run |
| deep-reasoning | **HLE** (araçlı ve araçsız ayrı satırlar) | A, vendor-run |
| knowledge-work | **GDPval-AA v2** (Elo) | A, vendor-run |
| workflow-automation | **AutomationBench** | A, vendor-run |
| computer-use | **OSWorld** 2.0 (partial/strict) + V2 (mod belirtilmemiş) | A + C — **karşılaştırılamaz**, bkz. çelişki 4 |
| aggregate / efficiency | **AA Intelligence Index v4.3** + cost/task + output speed + latency | B |
| long-context, research-synthesis | AA-LCR v1.1 / AA-Omniscience / AA-Briefcase (AA Index bileşenleri) | B |

**AA Index v4.3 bileşimi** (metodoloji sayfasından doğrudan): Agents %30
(AA-Briefcase, GDPval-AA v2, AutomationBench-AA) · General %30 (AA-Omniscience,
GDP.pdf, AA-LCR v1.1) · Coding %20 (Terminal-Bench v4.0, SciCode) · Scientific
Reasoning %20 (HLE, CritPt). **Index sürümleri birbiriyle karşılaştırılamaz** —
AA'nın kendi ifadesi. Bu, repo'nun taşıdığı eski 66/63/62/60 rakamlarını
otomatik olarak geçersiz kıldı.

### Doğrulanan (kural değişmedi, kaynak tazelendi)

- Claude roster'ı ve effort merdiveni (`low…max`; Haiku 4.5 effort desteklemez).
- Fable 5.1'in offensive-cyber fallback hedefleri: **Opus 4.8 ve Opus 5** →
  saldırı-amaçlı siber kapısı aynen geçerli.
- Biyoloji kapısı: Astra'nın system card'ı siber odaklı, bio eşiği yayımlanmamış
  → Codex kolu hâlâ `unverified — use Claude`.
- Astra: `gpt-6-astra`, 1.05M bağlam, 30 Nis 2026 kesim, $10/$50 (272k üstü 2×),
  `none` reddediliyor → frontier ve ≥1M kapıları aynen geçerli.
- `ultracode` ve `opusplan` mekanikleri.
- Bütün Adım 1 sert kapıları **yeniden doğrulandı ve korundu**. Hiçbiri weighted
  score'a çevrilmedi.

### Çürütülen / düzeltilen

| Eski kayıt | Gerçek (10 Eyl 2026) | Etki |
|---|---|---|
| Sonnet 5 $3/$15 (promosyon 31 Ağu'da bitti) | **$2/$10 — zam iptal edildi, standart fiyat bu** | Opus/Sonnet kota oranı 1.67× → **2.5×**; Sonnet 5'te kalmanın gerekçesi güçlendi |
| "Anthropic Sonnet 5 için `max` tavsiyesi yayımlamıyor" | Yayımlıyor — effort sayfasında açık madde | `Sonnet 5 · max` yasağının *gerekçesi* değişti: artık ölçülmüş dominance (E1), yanlış bir alıntı değil |
| `ultracode` yalnızca oturum-içi, dosyaya yazılamaz | Settings anahtarı + `CLAUDE_CODE_EFFORT_LEVEL` var | Routing etkisi yok |
| Codex `max` her GPT-5.6 katmanında | **Astra/Sol'a özel** (`learn.chatgpt.com`) | `Terra · max` yasağı tercih değil **capability limiti** oldu |
| "Astra'da Ultra modu belgelenmemiş" | Belgeli — "Astra and Sol additionally offer Max and Ultra modes" | Açık soru kapandı |
| AA Index 66/63/62/60 | Farklı index sürümü; güncel v4.3'te 53/51/48 | Eski rakamlar §2.1'de tarihsel olarak işaretlendi |
| "Codex Coding Agent Index 67/70" | AA v4.3'te böyle bağımsız bir index yok; izi sürülemedi | Katman C'ye düşürüldü, hiçbir kuralın dayanağı değil |

### Karşılaştırılamaz olarak işaretlenenler (§12.3)

1. Codex `max` erişilebilirliği — ürün yüzeyi vs API yüzeyi çelişkisi.
2. "Agentic coding" farkı — Terminal-Bench 4.0 Sol'u ~15 puan, CursorBench 2.8,
   DeepSWE 1 puan geride gösteriyor. Üç benchmark, üç büyüklük, tek etiket.
   Muhtemel neden: scaffold. **Sessizce ortalanmadı.**
3. Astra token verimliliği — OpenAI "Sol'dan az token" diyor, AA cost/task'ta
   Astra Sol'dan pahalı. İki iddia aynı şey değil.
4. OSWorld — Anthropic 2.0 (partial/strict), taşınan rakamlar V2 (mod belirsiz).
   Aynı model üzerinde partial/strict farkı ~36 puan. **Karşılaştırılamaz** →
   computer-use rozeti kalıcı olarak `low-confidence`.
5. "Codex Coding Agent Index" provenance'ı.

### Doğrulanamayanlar (§12.4) — uydurulmadı, boş bırakıldı

Terminal-Bench 4.0 leaderboard satırları (sayfa açıldı, tablo render olmadı —
bu sayfada model başına **cost, token ve %95 güven aralığı** var, bir sonraki
pass'in en değerli hedefi) · LiveBench tablosu · OSWorld leaderboard (bağlantı
reddedildi) · SWE-bench / SWE-bench Pro satırları · `openai.com/index/gpt-6-astra/`
(HTTP 403) · "Daybreak Blue" programının adı system card'da geçmedi · Astra'nın
bio/CBRN eşiği · MRCR, GraphWalks, BrowseComp, ScreenSpot-Pro, FrontierMath,
ARC-AGI, Toolathlon · Sonnet 5'in `high`/`xhigh` ve Sol'un `xhigh` rungları
(**interpolasyon yapılmadı**).

### Değişen routing kuralları

1. **Task capability profile** (Adım 2) eklendi — benchmark'lar capability'ye
   bağlandı; saf matematik promptunda kodlama benchmark'larının ağırlığı sıfır.
2. **Adım 5** eklendi: comparability → equivalence band (önce yayımlanmış CI/SE,
   sonra tekrarlı deneme varyansı, ikisi de yoksa küçük farkı üstünlük sayma;
   R=3'te bandı genişlet) → dominance (reasoning token → output token → toplam
   token → başarılı-görev başına token → kota baskısı → maliyet → gecikme).
3. **Kural E1/E2:** `Sonnet 5 · max` ve `Terra · max` domine edilmiş. Yükseltme
   artık **model** değişimi, efor değişimi değil.
4. **Kural E3:** `max`, `D=3 ∧ R=3` **artı** tek parçalı özgün tasarım/ispat
   kararı gerektiriyor.
5. **Codex computer-use kapısı** eklendi (roster notunda anılıyordu, kapı
   tablosunda satırı yoktu).
6. **`✅ RECOMMENDED AI`** (Adım 6) eklendi — capability'ye koşullu, tek
   ekosisteme çökmüyor, kanıt zayıfsa `low-confidence` işaretliyor.

### Nasıl tekrarlanır

Yukarıdaki Katman A URL'lerini sırayla çek; AA'nın leaderboard ve metodoloji
sayfalarını oku; her rakamı `skill/benchmarks.json` şemasına (benchmark,
version, model, effort, harness, tool_access, scaffold, trials, dispersion,
tokens, cost, date, source, source_tier, comparability_group) yaz; yayımlanmamış
her alanı `null` bırak. Sonra §12.3'ü yeniden gözden geçir: çelişki kapandı mı,
yeni çelişki doğdu mu.

---

## Ek — Gemini Deep Research prompt'u (2026 ortası)

> Tarihsel. `skill/reference.md` §7'de işaretlenen doğrulanamamış verileri
> kapatmak için kullanılmıştı. Kaynak disiplininin (K1/K2/K3 etiketleri, çelişki
> tablosu zorunluluğu, "bulunamadı geçerli bir cevaptır") nasıl kurulduğunu
> gösterdiği için korunuyor — yukarıdaki 10 Eylül kaydı aynı disiplinin
> devamıdır.

Aşağıdaki çizginin altındaki metni Gemini'ye (tercihen Deep Research modunda) yapıştır.

Amaç: `skill/reference.md` §7'de işaretlenen doğrulanamamış verileri kapatmak ve
router'ın çekirdek kuralını (Kural 1) sınamak.

---

Claude model ailesi üzerine, **kaynak disiplinli** bir teknik rapor hazırla.
Tarih: bugün. Kapsam: Fable 5, Opus 4.8, Sonnet 5, Haiku 4.5.

Bu bir pazarlama özeti değil. Çıktısı, hangi görevde hangi modelin ve hangi efor
seviyesinin kullanılacağına karar veren bir yönlendirme sistemini besleyecek.
Yanlış bir sayı, yanlış model seçimine yol açar. Buna göre davran.

## Kaynak hiyerarşisi — buna uy

**Katman 1 (birincil, tercih edilen):**
- `anthropic.com/news`, `anthropic.com/research`
- `platform.claude.com/docs/*` (özellikle `build-with-claude/effort`, `about-claude/pricing`, `about-claude/models/overview`)
- `support.claude.com` yardım merkezi makaleleri
- Anthropic sistem kartları (PDF)
- Anthropic'in resmi GitHub depoları

**Katman 2 (kabul edilebilir, çapraz doğrulama şartıyla):**
- Benchmark'ın kendi yayıncısı (SWE-bench, Terminal-Bench, GPQA, HLE, OSWorld ekipleri)
- Reuters, Bloomberg, AP gibi kurumsal haber kaynakları
- OpenRouter, Vellum, DataCamp gibi bağımsız değerlendirme platformları

**Katman 3 (tek başına KANIT DEĞİL):**
- `mindstudio.ai`, `codingfleet.com`, `stob.ai`, `claudefa.st`, `lorka.ai`,
  `glbgpt.com`, `crazyrouter.com`, `layer3labs.io`, `emergent.sh`, `kie.ai`,
  `sesamedisk.com`, `archisacademy.com` ve benzeri SEO/içerik siteleri
- Reddit, Twitter/X, Substack

**Kural:** Katman 3'ten gelen bir iddiayı, Katman 1 veya 2'den teyit edemiyorsan
**"DOĞRULANAMADI"** olarak işaretle. Silme, ama otorite muamelesi de yapma.
Bir Katman 3 sitesini başka bir Katman 3 sitesiyle "doğrulamak" doğrulama sayılmaz.

## Her iddia için zorunlu format

Rapordaki her sayısal veya olgusal iddianın yanına ekle:

`[K1|K2|K3]` — kaynak katmanı, ve `⟨yüksek|orta|düşük⟩` — güven.

Örnek: *Opus 4.8 girdi fiyatı $5.00/MTok* `[K1]` `⟨yüksek⟩`

## Öncelikli olarak cevaplanacak açık sorular

Bunlar raporun **ana hedefi**. Cevap bulamazsan "bulunamadı" yaz; uydurma,
tahmin etme, benzer bir kaynaktan ekstrapole etme.

**1. Efor seviyeleri.**
`low/medium/high/xhigh/max` seviyelerinin **resmi** tanımı nedir? Anthropic
dokümanı bu seviyelere somut bir düşünme-token bütçesi atıyor mu, yoksa sayılar
üçüncü taraf tahmini mi? Her model için varsayılan seviye nedir? Kaynak:
`platform.claude.com/docs/en/build-with-claude/effort`.

**2. `task_budget` parametresi.**
Var mı? Beta başlığı nedir? **Asgari değeri kaç token?** Dolaşımdaki iki
çelişkili rakam var: 20.000 ve 2.000. Hangisi doğru, ikisi farklı şeyler mi
(örn. asgari `task_budget` vs örnek alt-ajan bütçesi)? Resmi API dokümanından
teyit et.

**3. Ultra Code.**
Anthropic'in resmi bir özelliği mi, yoksa topluluk terimi mi? Hangi resmi
dokümanda geçiyor? `/effort max` ile ilişkisi ne? "Alt ajan orkestrasyonu"
iddiasının resmi karşılığı var mı?

**4. Benchmark skorları — özellikle şu üçü.**
Aşağıdaki tabloyu birincil kaynaklarla doldur. Her hücre için kaynak URL'si ver.

| Benchmark | Fable 5 | Opus 4.8 | Sonnet 5 | Kaynak |
|---|---|---|---|---|
| SWE-bench Verified | | | | |
| SWE-bench Pro | | | | |
| Terminal-Bench 2.1 | | | | |
| OSWorld-Verified | | | | |
| GPQA Diamond | | | | |
| GDPval-AA v2 (Elo) | | | | |
| HLE (araçlı) | | | | |
| HLE (araçsız) | | | | |
| USAMO 2026 | | | | |

Özellikle şunlara dikkat:

- **Terminal-Bench 2.1 / Opus 4.8:** iki farklı değer dolaşıyor, %82.7 ve %74.6.
  Hangisi doğru? Fark neden kaynaklanıyor (farklı ölçüm koşulu? farklı efor
  seviyesi? farklı sürüm?)
- **GDPval-AA v2:** Sonnet 5'in (1618) Opus 4.8'i (1615) *geçtiği* iddia
  ediliyor. 3 Elo puanlık bir fark. Bu istatistiksel olarak anlamlı mı? Güven
  aralığı yayımlanmış mı? Bu iddianın birincil kaynağı nedir? **Bu soru kritik.**
- **HLE (araçlı):** 57.4 vs 57.9 — yine parite iddiası. Güven aralığı var mı?

**5. Sonnet 5'in güvenlik yalıtımı.**
"Sonnet 5 exploit üretiminden bilinçli olarak yalıtılmıştır; Firefox 147
değerlendirmesinde çalışan exploit üretme oranı %0" iddiası doğru mu? Anthropic
sistem kartında geçiyor mu? Yoksa Katman 3 uydurması mı?

**6. Fable 5 ve "Mythos 5" anlatısı.**
Şu iddiaların her birini ayrı ayrı doğrula veya çürüt:
- Fable 5, "Mythos 5" adlı bir modelin güvenlik sınıflandırıcılı versiyonu mu?
- "Project Glasswing" diye bir program var mı?
- Fable 5 gerçekten ihracat kontrolü nedeniyle erişime kapatılıp geri açıldı mı?
  Tarihler? Resmi duyuru veya kurumsal haber kaynağı var mı?
- Fable 5 riskli sorgularda otomatik olarak Opus 4.8'e mi düşüyor? Bu davranış
  belgelenmiş mi?
- Stripe'ın 50 milyon satırlık kod tabanını tek günde taşıdığı iddiası —
  Stripe veya Anthropic'ten resmi bir açıklama var mı?
- "ExploitBench" diye bir benchmark gerçekten var mı?

Bu maddeler olağanüstü iddialar. Olağanüstü kanıt iste. Kaynak yoksa
**"DOĞRULANAMADI — muhtemelen içerik çiftliği kaynaklı"** yaz.

**7. Fiyatlandırma.**
Güncel `platform.claude.com/docs/en/about-claude/pricing` sayfasından girdi/çıktı/
cache-yazma/cache-okuma fiyatlarını al. Tarih damgası koy. Ayrıca:
- Sonnet 5 için bir promosyon fiyatı ve bitiş tarihi var mı?
- "Fast Mode" gerçek bir fiyatlandırma katmanı mı?
- **Tokenizer enflasyonu iddiası:** Opus 4.7 ile gelen yeni tokenizer'ın aynı
  metin için ~%30 (İngilizce 1.4×) daha fazla token ürettiği doğru mu? Resmi
  kaynak var mı, yoksa blog tahmini mi?

**8. Claude Code kotaları ve planlar.**
- Pro / Max 5x / Max 20x planlarının **resmi** kota tanımı nedir? "5 saatlik
  pencerede 10–40 prompt" ve "900 prompt" rakamlarının kaynağı resmi mi?
- Team Standard planında Claude Code erişimi gerçekten yok mu? Team Premium
  fiyatı nedir?
- Agent SDK kredileri ayrı mı faturalanıyor?

**9. MCP overhead.**
"Her bağlı MCP sunucusu işlem başına ~18.000 token overhead yaratır" iddiasının
kaynağı nedir? Ölçülmüş mü, tahmin mi? Sunucunun araç sayısına göre değişmez mi?

## Zorunlu çıktı bölümleri

1. **Yönetici özeti** — 10 madde, her biri kaynak katmanı etiketli.
2. **Model karşılaştırma tablosu** — yukarıdaki benchmark tablosu, kaynaklı.
3. **Efor seviyeleri** — resmi tanım; token bütçesi *varsa* kaynağıyla,
   *yoksa* "Anthropic bütçe yayımlamıyor" ifadesiyle.
4. **Fiyatlandırma tablosu** — tarih damgalı.
5. **Abonelik ve kota tablosu.**
6. **Çelişki tablosu** — ZORUNLU. Farklı kaynakların farklı sayı verdiği her
   iddia için: `iddia | kaynak A + değer | kaynak B + değer | hangisi daha
   güvenilir + neden`.
7. **Doğrulanamayanlar listesi** — ZORUNLU. Katman 1/2'de teyit edilemeyen her
   iddia, nerede geçtiğiyle birlikte.
8. **Ne değişti** — önceki bilgiye göre güncellenen veya yanlışlanan noktalar.

## Yasaklar

- Tek bir Katman 3 kaynağına dayanarak sayı verme.
- Tarihsiz fiyat yazma.
- İki kaynak çelişiyorsa birini sessizce seçme — ikisini de göster, gerekçeni yaz.
- Boşluğu makul görünen bir tahminle doldurma. "Bulunamadı" geçerli bir cevaptır
  ve uydurulmuş bir sayıdan çok daha değerlidir.
- Anthropic'in pazarlama dilini olgu gibi aktarma ("endüstrinin zirvesi",
  "emsalsiz güç" vb.).

## Son not

Raporun okuyucusu, bu verilerle bir karar otomasyonu kuracak. Emin olmadığın bir
sayıyı emin gibi sunmak, o otomasyonu sessizce bozar. Belirsizliği açıkça
işaretlemek zayıflık değil, raporun en değerli kısmıdır.
