# Research provenance — Gemini Deep Research prompt (Turkish)

> This is the research prompt used to gather and cross-check the model data that
> feeds `skill/reference.md`. Kept for provenance / reproducibility. It is not
> part of the skill and nothing reads it. If you want to refresh the model data,
> this is the prompt to re-run (in Gemini Deep Research or equivalent), then
> reconcile the results against the primary sources listed in `reference.md`.

---

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
