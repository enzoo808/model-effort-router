# Research provenance

Bu dosya router'ı besleyen veri araştırmasının **tekrarlanabilir kaydıdır**.
Skill'in parçası değildir, çalışma zamanında hiçbir şey okumaz.

Üç bölüm var, en yenisi önce:

1. **Araştırma kaydı — 10 Eylül 2026, Faz 2 (iteration-17)** — benchmark-**sahibi**
   kaynakların kapatılması, ham kanıttan routing kuralına giden yolun
   mekanikleştirilmesi, ve vendor-run benchmarkların cross-ecosystem tavsiyesi
   üzerindeki etkisinin ölçülmesi.
2. **Araştırma kaydı — 10 Eylül 2026, Faz 1 (iteration-16)**
   — benchmark-aware routing motorunun dayandığı araştırma. Ne arandı, hangi
   kaynak hiyerarşisi kullanıldı, ne doğrulandı, ne çürütüldü, ne
   doğrulanamadı, hangi routing kuralları değişti.
3. **[Ek: Gemini Deep Research prompt'u (2026 ortası)](#ek--gemini-deep-research-promptu-2026-ortasi)**
   — `reference.md` §7'deki eski açık soruları kapatmak için kullanılan orijinal
   araştırma prompt'u. Tarihsel; kaynak disiplininin nasıl kurulduğunu gösterdiği
   için korunuyor.

---

## Metodoloji düzeltmesi — 11 Eylül 2026 (iteration-18)

**Kaldırılan: gözlenen skor yayılımının bir kesri, eşdeğerlik bandı olarak.**

`benchmarks.json` → `no_dispersion_rule` bir grup CI veya SE yayınlamadığında
bandı `0.15 × roster'ın gözlenen yayılımı` olarak hesaplıyordu. Bu, istatistik
gibi okunuyor ama istatistik değil:

- Yayılım, modellerin **tesadüfen ne kadar uzak durduğunu** ölçer; hiçbirinin
  skorunun **ne kadar hassas ölçüldüğünü** değil.
- 40–59 arası yayılan dört modelli bir hücrede ~2.9 puanı aşan her farkı
  "kazanılmış" ilan ediyordu.
- İki satırlık bir karşılaştırmada yayılım **farkın kendisidir**, yani her
  karışılaştırma kazanırdı.

**Yerine gelen hiyerarşi** (`direction_setting_hierarchy`, sırayla):

1. yayımlanmış güven aralığı (CI)
2. yayımlanmış standart hata (SE) → band = 2 × SE
3. tek harness altında tekrarlı-deneme dağılımı
4. benchmark **sahibinin** yayımladığı pratik-anlamlılık eşiği
5. hiçbiri yoksa → o kanıt hücresi için **`UNRESOLVED`** — fark ne kadar büyük
   görünürse görünsün

**Bedeli, açıkça:** artık yalnızca `science` sertifikalı bir yöne sahip
(Terminal-Bench-Science'ın yayımladığı SE ±3.5–4.5 sayesinde). `agentic-code` ve
`terminal-tool` dahil diğer her capability `UNRESOLVED`'a düştü ve verimlilik
tie-break'ine düşüyor. Kaydın **işaret ettiği yön değişmedi** — kaybolan şey,
o yönün ölçülmüş olduğu iddiasıydı. Step 6'nın rozet tablosu **köken** sırasına
göre karar verir (kim, kimin harness'ında ölçtü), anlamlılık testine göre
değil, o yüzden geçerliliğini koruyor — ama `low-confidence` artık daha dürüst
bir kelime.

**E1 ve E3 etkilenmedi.** İkisinin de kanıtı "daha yüksek maliyete **daha iyi
olmayan** bir kademe" — yani dominans, küçük bir farkın büyüttülmesi değil; ve
eşitlik için aralığa gerek yok. Opus 5'in `max`-üzeri-`xhigh` bir puanlık
kazancı "bandın içinde"den `unresolved_rungs`'a taşındı — ki bu zaten
`SKILL.md` §5c'nin düz yazıyla söylediği şeydi.

**Kapanması gereken tek boşluk:** Terminal-Bench sahibinin leaderboard'undaki
%95 CI çubukları. Kayıttaki en değerli açık iş bu; çıkarılırsa setin en önemli
iki capability'si gerçek belirsizlik üzerinde karara bağlanır.

**Yeniden üretmek için:** `python scripts/compile_benchmark_frontiers.py` ·
`python scripts/test_frontier_compiler.py`. Derleyici, `min_fraction_of_spread`
geri gelirse `SpreadFallbackResurrected` fırlatır.

## Araştırma kaydı — 10 Eylül 2026, Faz 2 (iteration-17)

**Amaç.** Faz 1'in mimarisini değiştirmek DEĞİL. Üç şey: (1) Faz 1'de
doğrulanamayan **benchmark-sahibi** kaynakları kapatmak, (2) ham benchmark
verisinden routing kuralına giden yolu mekanik ve denetlenebilir hâle getirmek,
(3) vendor-run benchmarkların cross-ecosystem tavsiyesi üzerinde gereğinden
fazla etkisi olup olmadığını **ölçmek**.

### Faz 1'in kısıtı kalktı

Faz 1 boyunca **WebSearch kullanılamıyordu**; her şey bilinen URL'leri doğrudan
çekerek yapılmıştı ve bu yüzden benchmark sahiplerinin kendi leaderboard'larının
hiçbiri okunamamıştı. Faz 2'de arama çalıştı. Bulunanlar Faz 1'in en önemli
sonucunu düzeltti.

### Terminal-Bench — setteki en büyük düzeltme

| Kaynak | Sınıf | Satırlar |
|---|---|---|
| **Vals.ai, TB 2.1, her model Terminus 2 harness'ında** | model_intrinsic, B | Astra 87.27 · Sol 85.77 · Fable 5.1 85.02 · Opus 5 84.64 |
| **tbench.ai sahibi leaderboard, TB 2.1** | ecosystem_end_to_end, B | Codex CLI + Sol **89.5** · Claude Code + Opus 5 (max) **89.1** |
| **Artificial Analysis, TB 4.0** | model_intrinsic, B | **Astra 59 · Fable 5.1 52 · Sol 40** |
| OpenAI lansman tablosu, TB 4.0 (aktarma) | vendor_relative, C | Astra 57.7 · Fable 5.1 55.8 · Opus 5 52.3 · Fable 5 42.0 · Sol 37.3 |
| Anthropic lansman notu, TB 4.0 | vendor_relative, A | Mythos 5.1 60.9 · Fable 5.1 55.8 · Opus 5 52.3 · Fable 5 42.0 · Sol 37.3 |

Dört sonuç, dördü de önemli:

1. **İki vendor tablosu aslında tek tablo.** OpenAI'nin TB 4.0 rakamları
   Fable 5.1 (55.8), Opus 5 (52.3), Fable 5 (42.0) ve Sol (37.3) için
   Anthropic'inkiyle **rakam rakam aynı**. Bu, iki bağımsız koşu değil, tek bir
   yayımlanmış sayının iki tarafça yeniden alıntılanması — yani teyit değil,
   iki kez sayılmamalı.
2. **Anthropic'in tablosunda Astra satırı hiç yok.** iteration-16'nın
   "agentic-code → Claude" kuralı, karşısında kullanıldığı modeli hiç ölçmemiş
   bir tablodan okunmuştu. Bu bir muhakeme hatası değil **örnekleme** hatası.
3. **Bağımsız koşu Sol konusunda hemfikir, Astra konusunda değil.** AA'nın TB
   4.0'ı Claude-over-Sol yönünü aynen üretiyor (52 vs 40) ve Astra'yı ikisinin
   de üstüne koyuyor. Rozetin model-koşullu hâle gelmesinin sebebi bu.
4. **TB 2.1 doygun, TB 4.0 değil.** 84–88'e karşı 40–59. İkisi de veri
   deposunda `saturated: true` işaretli; compiler doygun bir gruptan sıralama
   okumayı reddediyor.

**TB 2.1 ile TB 4.0 asla karşılaştırılmıyor.** 2.1'in açık dataset reposu var
(`harbor-framework/terminal-bench-2-1`) ve submission protokolü belgeli:
`metadata.yaml` (agent + model), iş başına `config.json`, deneme başına
`result.json`, görev başına **en az 5 deneme**. Sahibin leaderboard sütunları:
Rank / Model / Agent / Resolution rate / Cost / Tokens + **%95 güven aralığı**.

**Hâlâ çıkarılamayan:** leaderboard'un satırlarının kendisi. `tbench.ai`
client-side render ediyor, Hugging Face aynası (`harborframework/terminal-bench-2-leaderboard`)
yalnız 2.0 ve dataset viewer'ı kapalıydı, repo ise toplu tablo yerine ham
deneme artefaktları tutuyor. Yukarıdaki iki end-to-end satır leaderboard'u
alıntılayan arama indeksinden geldi — grup B ama **CI sütunu hâlâ elde yok**.
Yayımlanmış %95 CI'lar bir sonraki pass'in en değerli hedefi olmayı sürdürüyor.

### LiveBench — mutable snapshot olarak doğrulandı, sonra dışlandı

Genel skorlar teyit edildi: Fable 5.1 83.4 · Fable 5 83.0 · Sol 81.0 · Opus 5
80.1 · Sonnet 5 76.0 (53 model varyantı, 23 görev, 7 kategori). **Canonical
artefakt bulunamadı:** LiveBench GitHub reposu yalnız 2025-04-25'e kadar
release belgeliyor ve `all_groups.csv` / `all_tasks.csv`'yi release başına
yayımlanan bir dosya değil, yerel bir script'in *ürettiği* çıktı olarak tarif
ediyor. Bu yüzden satırlar `mutable_snapshot: true` + retrieval tarihi taşıyor
ve LiveBench **dışlanmış listede** — hiçbir yön belirlemiyor. iteration-14'e
kadar kullanılan kategori satırları (Codex +1 kademesinin dayanağı dahil) yine
doğrulanamadı; kademe ayakta çünkü Faz 1'de TB 4.0'a yeniden temellendirilmişti.

### SWE-bench — bilerek NULL

SWE-bench Verified doygun: Opus 5 ~96, Sol ~96.2, Fable 5 ~95 — frontier ~1
puan içinde ve hiçbir agregatör scaffold'u belirtmiyor. SWE-bench Pro rakamları
(Fable 5.1 ~81.2) yalnız C katmanı bloglarda, harness yok, Sonnet 5 / Terra
satırı yok. **Hiçbir SWE-bench sayısı router'a girmedi** ve eski Claude 4.x /
GPT-5.x sonuçlarından ekstrapolasyon yapılmadı.

### OSWorld — computer-use kapısı ayakta, cross-vendor rozet değil

OpenAI tablosu, Faz 1'de eksik olan metadata ile: **OSWorld 2.0, offline set,
partial scoring** — Astra 72.6 · Opus 5 70.2 · Sol 65.7; görev başına ~40 dk,
Sol ~75 dk (~%47 azalma). Anthropic tablosu, aynı sürüm ve aynı skorlama
*etiketi*: Fable 5.1 77.9 · Opus 5 75.4 · Fable 5 72.9 (partial); 41.7 / 39.6 /
36.1 (strict).

**İki vendor da Opus 5'i OSWorld 2.0 partial'da yayımlıyor ve 5.2 puan
ayrışıyorlar** (70.2 vs 75.4). Muhtemel fark "offline set" — ki bunu yalnız
OpenAI adlandırıyor. Sonuç: **Codex-içi** yön (Astra > Sol) üç ayrı benchmark'la
teyitli (OSWorld, ScreenSpot-Pro 92.7 vs 76.9, Agents' Last Exam 59.3 vs 53.6),
o yüzden GUI işini Astra'ya yollayan kapı duruyor. Ama **cross-ecosystem**
karşılaştırma geçersiz: Astra 72.6 ile Fable 5.1 77.9 iki farklı vendor
harness'ı. Computer-use rozeti tam olarak bu yüzden `low-confidence`.

### Faz 1'de olmayan yeni cross-ecosystem satırlar

- **Araçlı HLE** (OpenAI'nin kendi tablosu): Fable 5.1 65.0 · Opus 5 63.6 ·
  **Astra 57.2**. Bir vendor'ın rakibi lehine sonuç yayımlaması
  *against-interest*'tir ve vendor kanıtının en güvenilir türüdür.
  `deep-reasoning`'in Claude'da kalmasının sebebi bu.
- **FrontierMath Tier 4 (v2)**: Astra 97.6 · Fable 5.1 87.8 · Opus 5 73.2 —
  ters yönde, ve **dışlandı**: benchmark'ı Epoch AI koşuyor ama kaynağın kendisi
  OpenAI'nin geliştirmesini finanse ettiğini ve bir kısmına özel erişimi
  olduğunu açıklıyor.
- **ARC-AGI-3**: Astra 99.9 · Opus 5 30.2 · Sol 7.8 — **dışlandı**: Anthropic'in
  kendi Opus 5 notu bu benchmark'ta "en yakın rakibin üç katı" diyor, 30.2 ile
  uzlaşmıyor, ve iki taraf da harness belirtmiyor.
- **AA Coding Agent Index (güncel)**: Astra+Codex 62 = Fable 5.1+Claude Code 62 ·
  Opus 5 60 · Sol 55. iteration-15'in izi sürülemeyen "67/70" rakamları bunun
  **eski sürümüne** ait (Fable 5 68.1 · Fable 5.1 67.2 · Astra 67.0). **Faz 1
  açık maddesi kapandı.**
- **AA Intelligence Index v4.1.1**: Fable 5.1 65.7 · Opus 5 63.1 · Astra 61.2.
  Repo'nun taşıdığı 66/63/62 rakamları buradan geliyor. v4.1.1'de Astra
  Fable 5.1'in 4.5 puan *altında*, v4.3'te 53'te eşit. **İkinci Faz 1 açık
  maddesi kapandı.**
- **Görev başına output token** (AA v4.3): Astra 27k / $3.26 · Fable 5.1 78k /
  $7.63. Setteki ilk gerçek output-token rakamları.
- **MRCR v2 8-needle**: Astra 100 vs Sol 91.5 (256–512K), 96.3 vs 73.8
  (512K–1M). Claude satırı yok.
- **ExploitBench gerçek.** Faz 1 §7 bunu "muhtemelen içerik çiftliği uydurması"
  diye işaretlemişti; OpenAI'nin lansman tablosunda var. Hiçbir routing kuralını
  etkilemiyor (saldırı-amaçlı siber sert bir güvenlik kapısı) ama o not yanlıştı.

### Vendor-bias ablation — ölçüm, zorlama değil

`python scripts/ablate_evidence.py` aynı kanıt setini üç görünümde derliyor:

| görünüm | tutulan kayıt | claude | codex | verimlilik karar verir |
|---|---|---|---|---|
| tümü | 123 | 14 | 7 | 10 |
| yalnız bağımsız (B katmanı) | 31 | 11 | 6 | 14 |
| vendor-cross-model kapalı | 48 | 11 | 6 | 14 |

**Yalnız `agentic-code` ve `terminal-tool` her iki filtreden sağ çıkıyor.**
Diğer her capability, bir vendor'ın rakibi kendi harness'ında ölçtüğü satırlar
çıkarılınca UNRESOLVED'a düşüyor: `knowledge-work` (GDPval, yalnız Anthropic),
`science` ve `workflow-automation` (iki vendor'ın da kendi tablosu),
`computer-use` (yalnız OpenAI), `deep-reasoning` (yalnız OpenAI'nin HLE satırı).

**İki tarafın da terminal dışındaki üstünlüğü vendor-bağımlı.** Bu, 50/50'ye
zorlamak için bir sebep değil — dengeli bir rozet uydurma olurdu. Yapılan şey
router'ın bunu **söylemek zorunda** kalması: bu capability'ler Adım 6 tablosunda
† işaretli ve Evidence satırları `low-confidence` demek zorunda.

### Değişen tek routing kuralı

`agentic-code` / `terminal-tool` rozeti artık **hangi Codex modelinin hatta
olduğuna** bağlı. Terra/Sol'a karşı Claude üstünlüğü her kaynakta ve her
filtrede ayakta; **Astra**'ya karşı değil. Model ve efor seçimine dokunulmadı.

### Nasıl tekrarlanır

```
python scripts/validate_benchmarks.py
python scripts/compile_benchmark_frontiers.py
python scripts/compile_benchmark_frontiers.py --check
python scripts/test_frontier_compiler.py
python scripts/ablate_evidence.py
```

Ham kanıtı değiştirip frontier'ı yeniden derlemezsen hem `--check` hem validator
FAIL eder (`benchmark_frontiers.json` girdinin sha256'sını saklıyor). Compiler
iki kez çalıştırıldığında çıktı bayt-bayt aynı olmalı; değilse bu bir hatadır.

---

## Araştırma kaydı — 10 Eylül 2026, Faz 1 (iteration-16)

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
