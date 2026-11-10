# Bulgu raporu — Claude ve OpenCode Go veri güncellemesi (iteration-27 adayı)

**Okuma tarihi:** 10 Kasım 2026 · **Karşılaştırılan skill durumu:** `routing-policy-version: iteration-26` (Claude kadrosu 8 Eki, OpenCode havuzu 20 Eki 2026) · **Aşama:** 1 — skill, policy, evals ve docs dosyalarına **dokunulmadı**; yalnız bu rapor yazıldı.

## Özet

1. **Claude tarafı:** 9 Kas'ta **Fable 5.2** (`claude-fable-5-2`, USD 8/40, 5.1'in %20 altı) ve **Mythos 5.2** (sınırlı erişim) çıktı; Claude Code 2.1.321 `fable` takma adını 5.2'ye çevirdi. Opus 5.5 / Sonnet 5.5 / Haiku 5.5 fiyatları ve takma adları **değişmedi**; Haiku 4.5 hâlâ "Active" (emeklilik duyurusu yok). Opus 4.8'in `/fast` modu **30 Kas'ta kalkıyor**.
2. **Artificial Analysis (AA) 27 Eki'de Intelligence Index v5'e geçti** (GDPval-AA, SciCode, AA-LCR çıktı; FrontierCode 2.0 ve Terminal-Bench-Science girdi). Skill'in tüm II / USD-görev rakamları v4.3.2 — "sürüm karıştırma" kuralı yüzünden bu **en büyük karar**: eski satırlar ile v5 satırları aynı tabloda yan yana kullanılamaz (Karar D1).
3. **OpenCode Go'da iki yapısal değişiklik:** (a) **Gemini 4 Argon artık Contributor değil** — Go sayfası "Not used" (eğitimde kullanılmaz), 0 gün saklama, cap USD 30, %50 indirim 30 Kas'a kadar; (b) **MiniMax M3.1 Flash Free Go'dan çıktı** (yerine ücretli "MiniMax M3.1 Flash", cap USD 20; bedava sürüm yalnız Zen'de).
4. Diğer Go değişiklikleri: **Kimi K3.1 Pro** eklendi (cap USD 15, AA v5'te 46 puanla açık modellerin birincisi); **DeepSeek V4.1 Flash cap USD 80 → 100**; DeepSeek sıfır-saklama anlaşması yenilendi (**30 Kas 2026'ya kadar**); zirve saatleri aynı; **Go Teams** (USD 20/üye) planı eklendi.
5. **Öneri — uygula (must apply):** Fable 5.2 kadro/fiyat/takma ad, Mythos 5.2 ifadesi, Opus 4.8 `/fast` çıkarımı, Argon'un Go verileri, MiniMax Free'nin düşmesi (FR1'in kendi yedek planı), DeepSeek cap/ZDR tarihi, Kimi K3.1 Pro'nun premium (P) olarak havuza girmesi. **Havuz sayısı 19 kalır** (MiniMax Free çıkar, Kimi K3.1 Pro girer).
6. **Karar gerektiren 4 konu** (aşağıda): D1 AA v5 yaklaşımı, D2 Argon'un gizli işlerde kullanımı + katman, D3 Fable 5.2 ile Opus 5.5 `max` / A1 ilişkisi, D4 A1-OC'de Kimi K3.1 Pro.
7. Doğrulanamayanlar `n/p`: AA v5'te GPT 6 Luna / Muse Spark 1.3 / MiMo-V2.6-Flash / Qwen3.8 Flash / Kimi K3 satırları, v5 bileşen bazlı skorlar (model sayfaları yalnız toplam veriyor), DeepSWE v1.1 ve FrontierSWE v2'nin yeni modelleri, Fable 5.2'nin kullanıcının planındaki durumu.

## Yöntem ve sınırlar

- Kaynaklar `web-fetch` alt-ajanlarıyla okundu; ajan raporları **model çıktısıdır**. Her kritik iddia en az iki ayrı sayfadan/kaynaktan çıkarıldı (Fable 5.2: sürüm notları + fiyat sayfası + duyuru + Claude Code changelog + AA; Argon: Go dokümanı + models.dev; MiniMax: Go dokümanı + models.dev + Zen; AA v5: makale + liderlik tablosu).
- Birkaç uzun sayfa (AA liderlik tablosu, Claude Code changelog, model-config) tek seferde okunamadı; araç kalan kısmı **model özeti** ile değiştirdi. Özet ile ham metin çeliştiğinde yalnız ham metin kullanıldı. AA liderlik tablosunun sonu (≈13 bin karakter) **okunamadı** — oradaki satırlar `n/p`.
- OpenCode Go sayfasında tarih/değişiklik günlüğü yok; "değişiklik tarihi" yalnız OpenCode changelog'unda geçtiği yerde verildi, aksi hâlde "not stated".
- Alt-ajan raporlarındaki rakamlar bu oturumda ikinci kez elle doğrulanmadı; yine de Aşama 2'de her rakam yazılmadan önce kaynağından bir kez daha kontrol edilmeli (özellikle AA v5 sayıları).
- **Hiçbir sayı enterpole edilmedi.** "Türetilmiş" işaretli satırlar skill'in kendi formülüdür (tasks/mo = cap ÷ Arena p50 görev maliyeti) ve girdileri belirtilmiştir.

## Karar bekleyen konular

**D1 — AA Index v5.** Skill'in kuralı: aynı sürüm, sürüm karıştırma yok. v4.3.2'nin hâlâ yayımlandığı veya v4.3.2→v5 dönüşümü yayımlandığı **doğrulanamadı** (makale yalnız "v4.3" der). Seçenekler: **(a) önerilen —** mevcut satırlar "v4.3.2, dondurulmuş" olarak kalır, v5 yalnız yeni/yeniden doğrulanan satırlar için ayrı sütunda (`II v5`) tutulur, hiçbir karşılaştırmada iki sürüm karışmaz; **(b)** 19 modelin hepsi v5'e taşınır (şu an yalnız 8-9 modelin v5 satırı doğrulandı; kalanı `n/p` olur → birçok sıralama çözümsüz kalır); **(c)** v5 yok sayılır (Kimi K3.1 Pro ve Fable 5.2 kanıtsız kalır). Kural mantığı (B1/BD1/E1–E3) v5 sayılarıyla da tutuyor (tablo B), bu yüzden (a) kural değiştirmez.

**D2 — Gemini 4 Argon.** Skill: "yalnız Contributor, eğitir, yalnız NC1". Veri: Go sayfasında düz "Gemini 4 Argon", "Not used", 0 gün. Bu, kuralın **gerekçesini** ortadan kaldırıyor (kural mantığı veriyle zorlanıyor). Önerilen: Argon gizli işlerde de kullanılabilir hâle gelir (kullanıcı daha önce "Gemini ücretli API gizli işe izinli" demişti), GM1 yuvası aynı kalır (yalnız `D = 3` / `R = 3` sütunu), ancak cap yarıya (USD 30) indi ve %50 indirim 30 Kas'ta bitiyor → türetilmiş tasks/mo ≈ 38 (liste fiyatı varsayımıyla, Arena p50 USD 0.78) / ≈ 77 (promo fiyatıyla) — BUD1'in "premium ≤ 35" eşiğine yakın. **Alternatif:** Argon'u premium (P) say, yalnız A1-OC'de kullan. Hangi fiyatın Arena maliyetine yansıdığı `n/p`.

**D3 — Fable 5.2 / Opus 5.5.** A1'in gerekçe cümlesi ("Opus 5.5, Fable 5.1'e 8/8 satırda eşit-veya-üstün") Fable 5.2 için **artık geçerli değil**: satıcı tablosunda Fable 5.2 Opus 5.5'in önünde (FrontierCode 2.0 49.1 vs 45.5, FrontierSWE v2 69.9 vs 62.3, HLE 74.2 vs 67.7, …), bağımsız Vals TB 4.0'da eşit (65.15 = 65.15), AA v5'te Fable 5.2 `high` (62 @ USD 9.08) Opus 5.5 `max`'ı (59 @ 10.04) geçiyor. Ancak AA USD'si ≠ Claude abonelik kotası ve Fable ayrı haftalık limite sahip. Önerilen: kadro/fiyat değişsin, **A1/M1/bayrak listesi mantığı değişmesin**; "Fable 5.2 `high` ≥ Opus 5.5 `max`" gözlemi `reference.md`'ye not olarak girsin. Kural değişikliği ister misiniz?

**D4 — A1-OC premium.** Kimi K3.1 Pro (AA TB 4.0 %67 — AA'nın listelediği en yüksek; Vals TB 4.0 63.64) kodlama için GLM-5.3'ten (v4.3.2 TB 42; v5 TB değeri `n/p`) güçlü görünüyor. Önerilen: K3.1 Pro havuza P olarak girer; A1-OC'de Kimi K3 → Kimi K3.1 Pro (deep-reasoning, science, long-context, doc) ve `agentic-code` / `terminal-tool` için GLM-5.3 yerine K3.1 Pro **düşük güvenle**. Onay?

## Tablo A — Claude tarafı

Kaynak anahtarları sayfa sonunda. "Tür": V = vendor-reported, B = bağımsız.

| # | Madde | Skill'deki eski değer | Yeni değer | Kaynak | Tür | Karar |
|---|---|---|---|---|---|---|
| A1 | Fable 5.2 yayında | Kadro: Fable 5.1, USD 10/50 | `claude-fable-5-2`, **9 Kas 2026**, USD 8/40, 1M bağlam, 128K çıktı, bilgi sınırı Haz 2026, cache read 0.025×; Fable 5.1 "legacy" (deprecations: Active, ≥1 Eyl 2027) | S1, S2, S3, S4, S6 | V | **must apply** |
| A2 | Mythos 5.2 | "Mythos 5.1 = Fable 5.1, Glasswing invite only" | `claude-mythos-5-2`, "limited availability": Cyber Verification Program / Life Sciences Verification Program ile doğrulanmış kuruluşlar; USD 8/40; "Glasswing" okunan sayfalarda geçmiyor | S1, S4, S6 | V | **must apply** (ifade); Glasswing'in sürüp sürmediği **not verified** |
| A3 | `fable` takma adı | Step 7'de yalnız opus/sonnet/haiku | `fable` → Fable 5.2 (v2.1.321+, 9 Kas); `best` = opus; kayıtlı Fable 5.1 seçimleri `fable`'a taşınır; Fable 5.2 org'a açık değilse önceki Fable'a düşer (2.1.301); hiçbir planda varsayılan model değil | S7, S8 | V | **must apply** |
| A4 | Fable 5.2 efor | Efor tablosu: "`high` = API varsayılanı, Opus 5.5 hariç" (Haiku 5.5 de `medium`, tablo kendi içinde tutarsız) | 5 seviye (low…max). **API varsayılanı:** Fable 5.2 `high`, Opus 5.5 `medium`, Sonnet 5.5 `high`, Haiku 5.5 `medium`. **Claude Code / uygulama varsayılanı:** dört modelde de `medium` | S2, S5 (API); S6, S8 (Claude Code) | V | **must apply** (API ve Claude Code varsayılanını ayır) |
| A5 | Fable 5.2 plan erişimi | Skill'de yok | Max/Ultra/premium koltuk: haftalık limitin ≤ %50'sine dahil, ayrı Fable haftalık limiti; Pro/standart koltuk: kullanım kredisi (yardım merkezi) — duyuru ise Pro için lansman teklifi diyor → **iki kaynak çelişiyor**; Enterprise'da admin açana dek kapalı | S6, S10 | V | **not verified** (kullanıcının planı `n/p`) |
| A6 | Fable 5.2 bağımsız skorlar | Fable 5.1 AA satırı yok | AA v5.0.1: max 65 @ USD 26.54 · xhigh 62 @ 14.83 · high 62 @ 9.08 · medium 56 @ 3.80 · low 54 @ 3.10 (süre 6.5–46.4 dk). Vals TB 4.0 (Mini-SWE-agent, avg@3, 9 Kas): Fable 5.2 = Opus 5.5 = 65.15 | S12, S13, S19 | B | **apply with low-confidence** (AA aralık yayımlamaz → UNRESOLVED; yalnız verimlilik/yön) |
| A7 | Fable 5.2 satıcı tablosu | A1: "Opus 5.5 ≥ Fable 5.1, 8/8" | Fable 5.2 vs Opus 5.5 (en yüksek efor, safeguards açık): FrontierCode 2.0 49.1/45.5 · FrontierSWE v2 69.9/62.3 · AutomationBench 51.4/42.5 · OSWorld 2.1 89.3/87.2 · HLE(tools) 74.2/67.7 · AA-Briefcase v1.1 66.1/61.2 · RLI 41.3/21.3 | S6 | V | **note only** (A1 gerekçesi için D3) |
| A8 | Fable 5.2 `high` vs Opus 5.5 `max` | M1/E3 (`max` yalnız flagship) | AA v5: Fable 5.2 high 62 @ 9.08 > Opus 5.5 max 59 @ 10.04 (makale 58); Fable 5.2 low 54 @ 3.10 ≥ Opus 5.5 high 52 @ 3.46 | S11, S12 | B | **not verified** kota sonucu olarak (AA USD ≠ abonelik kotası) → D3 |
| A9 | Claude fiyatları | Opus 5.5 4/20 · Sonnet 5.5 2/10 · Haiku 5.5 0.10/0.50 (≤100k), 0.50/2.50 | **Değişmedi.** Sonnet 5.5 cache read 0.10 (7 Eki, skill'de zaten var). Sonnet 5 yeniden tanıtım fiyatı kalıcı (3/15 artışı iptal) | S4 | V | **note only** (doğrulandı) |
| A10 | Haiku 4.5 | "Legacy — never selected (retires 'not sooner than 15 Oct 2026')" | Hâlâ **Active**, Deprecated tarihi yok; "not sooner than 15 Oct 2026" satırı aynen duruyor (tarih geçti, duyuru yok) | S3 | V | **note only** (ifadeyi "floor passed, no retirement announced" yap) |
| A11 | Opus 4.8 | "Legacy — offensive-security gate"; Step 7 `/fast` satırı Opus 5.5/4.8 | Active, ≥ 28 May 2027. **Fast modu 30 Eki'de deprecated, 30 Kas 2026'da kalkıyor** (sonra hata verir, standart moda düşmez) | S1, S7, S9 | V | **must apply** (`/fast` satırından Opus 4.8 çıkar) |
| A12 | `/fast` | "2.5x faster, 2× price" (Opus 5.5 / 4.8) | Destek: Fable 5.2 (USD 16/80, v2.1.321+), Opus 5.5 (8/40; "research preview" etiketi 2.1.304'te kalktı), Opus 5, Opus 4.8; Sonnet/Haiku yok; yalnız kullanım kredisi, abonelik limitine dahil değil. **Hız çarpanı bu okumada doğrulanamadı (`n/p`)** | S9, S7 | V | **apply with low-confidence** (Fable'ı satıra ekleme; "2.5x" yeniden doğrulanmalı) |
| A13 | `ultrathink` | v2.1.311+ terminalde `xhigh` | Aynı; changelog Opus 5.5 / Sonnet 5.5 / Haiku 5.5 / Fable 5.1 sayıyor, Fable 5.2'yi adıyla anmıyor; `CLAUDE_CODE_DISABLE_ULTRATHINK` (2.1.316) | S7 | V | **note only** |
| A14 | `ultracode` | Bayrak (v2.1.284+), efor seviyesi değil | Değişmedi; `--effort ultracode` hâlâ xhigh+ultracode başlatır; `/effort ultracode off` ile kapanır | S8 | V | **note only** (doğrulandı) |
| A15 | `opusplan` | opus plan → sonnet icra | Değişmedi; `opusplan[1m]` mevcut | S8 | V | **note only** (doğrulandı) |
| A16 | Takma ad eşlemesi (API) | opus→5.5 (v2.1.280+) · sonnet→5.5 (v2.1.284+) · haiku→5.5 (v2.1.293+) | Değişmedi. Sağlayıcıya göre farklı: Bedrock/Vertex Opus 5.5 / Sonnet 4.5 / Haiku 4.5; Foundry Opus 4.6; Platform on AWS Sonnet 4.6 | S8 | V | **note only** |
| A17 | Alt-ajan eforu | `reference.md`'de kayıtlı | `CLAUDE_CODE_SUBAGENT_EFFORT` (2.1.316); farklı modeldeki alt-ajan o modelin kayıtlı eforunu kullanır (2.1.317); `CLAUDE_CODE_WORKFLOW_SUBAGENT_MODEL` (2.1.296) | S7 | V | **note only** |
| A18 | Eski model emeklilikleri | Skill'de yok | Opus 4.5 ≥ 24 Kas 2026; Sonnet 4.5 deprecated, **30 Kas 2026'da emekli**; kadro dışı | S3 | V | **note only** |
| A19 | Anthropic sayfa çelişkisi | — | `models/overview` Fable 5.1 / Opus 5 / Haiku 4.5'e "legacy (still available)" der, deprecations tablosu "Active" der | S2, S3 | V | **note only** |

## Tablo B — Artificial Analysis Index v5 (bağımsız)

| # | Madde | Skill'deki eski değer | Yeni değer | Kaynak | Tür | Karar |
|---|---|---|---|---|---|---|
| B1 | Index sürümü | v4.3.2, asla karıştırma | **v5 (27 Eki 2026); sayfalarda "v5.0.1"** (metodoloji güncellemesi 3 Kas). Makale eskiyi "v4.3" diye anar, "v4.3.2" geçmez. Dönüşüm tablosu / eski skorların erişilebilirliği: not stated | S11, S12 | B | **must apply** (D1) |
| B2 | Bileşenler ve ağırlıklar | Çapalar: GDPval-AA, AA-LCR, SciCode, AA-Omniscience, HLE, CritPt, TB 4.0 … | Çıkan: GDPval-AA v2.1, SciCode, AA-LCR v1.1. Yeni: FrontierCode 2.0, Terminal-Bench-Science 0.1. Yükselen: HLE-Diamond, AA-Omniscience v1.1, CritPt v2 (hard). Kalan: AA-Briefcase v1.1, AutomationBench-AA, GDP.pdf, TB 4.0. Ağırlık: Knowledge 25 (Briefcase 15, AutoBench 5, GDP.pdf 5) · Coding 25 (FrontierCode 15, TB 4.0 10) · Science 25 (TB-Sci 15, CritPt 10) · General 25 (Omniscience 15, HLE-D 10). TB 4.0 skorlarının v4.3.2'den beri aynı kaldığı: not stated | S11 | B | **must apply** (Step 2 çapaları: knowledge-work/long-context/science) |
| B3 | Claude v5 efor eğrisi | Opus 5.5: low 42 · med 51 · high 54 · xhigh 56 · max 58; Sonnet 5.5 max 56; Haiku 5.5 High 38 / Max 43 | Opus 5.5: low 35 @ 0.98 · med 48 @ 2.45 · high 52 @ 3.46 · xhigh 57 @ 6.05 · max 59 @ 10.04 (makalede max 58). Sonnet 5.5: low 26 @ 0.51 · med 31 @ 0.78 · high 42 @ 1.64 · xhigh 50 @ 4.09 · max 55 @ 10.02. Haiku 5.5: low 19 @ 0.04 · med 25 @ 0.09 · high 30 @ 0.16 · xhigh 35 @ 0.25 · max 36 @ 0.41 | S12 | B | **apply with low-confidence** (`II v5` sütunu) |
| B4 | E1/E3/E8/H1 v5'te | E1: Sonnet max 56 @ 5.46 ← Opus xhigh 56 @ 3.46 | v5'te de geçerli: Sonnet max 55 @ 10.02 hâlâ Opus xhigh 57 @ 6.05 tarafından domine; Opus max'ın xhigh'a getirisi +2 puan, +66% maliyet. **Yeni:** Haiku `low`/`medium` artık ölçülmüş (19 @ 0.04, 25 @ 0.09) — skill "ölçülmemiş" diyordu; Haiku medium 25 @ 0.09 ≈ Sonnet low 26 @ 0.51 | S12 | B | **apply with low-confidence** (kural mantığı değişmez) |
| B5 | Açık modeller v5 | II: MiMo-Pro 46 · GLM-5.3 45 · Kimi K3 44 · Grok 4.7 46 · Qwen Max 45 · GLM-Flash 42 · DeepSeek 39 | MiMo-V2.6-Pro 30 @ 0.26 · GLM-5.3 max 32 @ 5.01 (low 23) · GLM-5.3-Flash 28 · DeepSeek V4.1 Flash "1017" max 33 @ 0.60 (makale 32), high 29, non-reasoning 19 · MiniMax-M3.1-Flash 29 @ 0.49 · Grok 4.7 xhigh 35 @ 7.77 (high 35, low 31) · Qwen3.8 Max 34 @ 10.02 · Kimi K3.1 Pro 46 @ 3.68 · Gemini 4 Argon high 50 @ 9.95. Açık modeller v4.3.2'ye göre ~12–16 puan düştü, Claude ≤ 7 | S12, S13 | B | **apply with low-confidence** |
| B6 | v5'te bulunamayan satırlar | — | GPT 6 Luna, Muse Spark 1.3 (Contributor), MiMo-V2.6-Flash, Qwen3.8 Flash ("Qwen3.8-Flash-Next" farklı ad), Kimi K3, Fable 5.1: okunan kısımda yok | S12 | B | **not verified** (`n/p`) |
| B7 | DeepSeek revizyonu ve E7 | E7: "AA'nın DeepSeek `low`/`high` rakamı yok" | AA eski sayfayı "deprecated" işaretlemiş, güncel ölçüm "1017" sürümü; Go'daki `deepseek-v4.1-flash`'ın hangisi olduğu not stated. v5'te `high` 29 / `max` 33 var → E7'nin dayanağı güncellenebilir (D = 2 `high` mantığı çelişmiyor) | S13, S12 | B | **apply with low-confidence** |
| B8 | Olası çıkarma hatası | — | Gemini 3.8 Flash (high 31) ile Grok 4.7 (xhigh 35) aynı "USD 7.77" değerini gösteriyor; şüpheli | S12 | B | **not verified** (kullanılmaz) |
| B9 | Okunamayan kısım | — | Liderlik tablosunun ≈ son 13 bin karakteri okunamadı | S12 | — | **not verified** |

## Tablo C — OpenCode Go

| # | Madde | Skill'deki eski değer | Yeni değer | Kaynak | Tür | Karar |
|---|---|---|---|---|---|---|
| C1 | **Gemini 4 Argon** | Yalnız `gemini-4-argon-contributor`; cap USD 60 (promo, sonra 30); **prompt'lar eğitimde kullanılır**; yalnız NC1 | Go'da düz **"Gemini 4 Argon"** (`gemini-4-argon`): cap **USD 30** (Plus 120, Teams 35), eğitim **"Not used"**, saklama **0 gün**, "%50 indirim **30 Kas 2026'ya kadar**" (USD 2/10; liste 4/20), 1 Ara'dan itibaren maliyet çarpanı ×2 (models.dev). `gemini-4-argon-contributor` models.dev'de **deprecated**. Değişiklik tarihi/sebebi ve 30 Kas sonrası cap: not stated | S15, S18, S17 | V (+ topluluk) | **must apply** (veri); kural etkisi → **D2** |
| C2 | Argon bağımsız kanıt | AA v4.3.2: II 53, TB 57, AutomationBench 77.5, Omniscience 42, halüsinasyon %15 | AA v5: high 50 @ 9.95, AutomationBench-AA %78 (listenin birincisi). Vals TB 4.0 57.58 (sıra 9, maliyet/test USD 17.64), Vibe Code Bench v1.1 91.91 (sıra 3), Arena Agent sıra 8 (net iyileşme %10.83 ±0.87, p50 USD 0.78), Arena Text sıra 2. AA'da Omniscience/halüsinasyon v5 değerleri: n/p | S11, S19, S20 | B | **apply with low-confidence** |
| C3 | **MiniMax M3.1 Flash Free** | Havuz #19, "Free on Go (limited time), unlimited, zero retention", FR1 | Go sayfasında **yok**; yerinde ücretli **"MiniMax M3.1 Flash"**, cap **USD 20** (Plus 80, Teams 25), 0 gün, eğitim yok. models.dev'de `minimax-m3.1-flash-free` = **deprecated**. Bedava sürüm yalnız **Zen**'de (`minimax-m3.1-flash-free`, sınırlı süre, sıfır saklama, eğitim yok). Kaldırılma tarihi: not stated | S15, S16, S18 | V | **must apply** (FR1'in kendi yedeği: satırlar GLM-5.3-Flash `#2` / Qwen3.8 Flash · MiMo-V2.6-Pro'ya döner; Zen ikizi yalnız `Evidence:`'ta anılır) |
| C4 | Ücretli MiniMax M3.1 Flash | Havuzda yok | AA v5: 29 @ 0.49. Bağımsız TB/Arena/DeepSWE satırı yok; ücretli ve bedava sürümün aynı model olduğu: models.dev'de aynı efor listesi, doğrudan beyan yok | S12, S18 | B / topluluk | **not verified** → "never selected" |
| C5 | **Kimi K3.1 Pro** | Havuzda yok | Go: id `kimi-k3.1-pro`, cap **USD 15** (Plus 60, Teams 20), USD 2/10 (cache 0.20), 0 gün, eğitim yok. Efor: `low`/`high`/`max`, varsayılan `max` (models.dev; "Go'da doğrulanmadı" notu). AA v5: **46, sıra #1/26 (açık modeller), USD 3.68/görev**, TB 4.0 **%67**, CritPt %45, HLE-Diamond %37, TB-Sci %34. Vals TB 4.0 63.64 (sıra 4), Vibe Code 84.89 (sıra 19), Arena Agent sıra 13 (net iyileşme %5.24 ±1.12, p50 USD 1.25), Arena WebDev sıra 10. Türetilmiş tasks/mo = 15 ÷ 1.25 ≈ **12** → premium (P). Çelişki: AA sayfası ağırlık bağlantısı veriyor, makale "weights not yet released" diyor | S15, S13, S11, S19, S20 | V + B | **apply with low-confidence** (P olarak havuza gir; **D4**) |
| C6 | DeepSeek V4.1 Flash cap | USD 80, tasks/mo 615 | **USD 100** (Plus 200, Teams 105); OpenCode changelog v2.2.4 (30 Eki): "Raised OpenCode Go limits for DeepSeek V4.1 Flash" (rakam verilmez). Türetilmiş tasks/mo = 100 ÷ 0.13 ≈ 770 | S15, S17 | V | **must apply** |
| C7 | DeepSeek ZDR | "valid through 31 Oct 2026" | "ZDR agreement is renewed monthly. The current agreement is valid through **November 30, 2026**." → **yenilendi** | S15 | V | **must apply** (tarih; Step 7 kural 10 ve örnek çıktılar) |
| C8 | DeepSeek zirve saati | Pzt–Cum 01–04 ve 06–10 UTC (2×) | **Aynı.** Fiyat: off-peak USD 0.15/0.60, peak 0.30/1.20 | S15, S18 | V | **note only** (doğrulandı) |
| C9 | Go planları | Go USD 10; Go Plus USD 40 | Aynı + **Go Teams USD 20/üye/ay** (28 Eki; her üye kendi limitleri, her modelde Go'dan USD 5 yüksek; "Extra Usage" açık başlar). Limit yapısı aynı: 5 saat %20 / hafta %50 / ay %100. Limit dolunca Extra Usage (kredi) veya bedava modeller | S15, S17 | V | **note only** (tek üyeli kullanıcı için) |
| C10 | Cap karşılaştırması | 15 modelin cap'i skill'de | MiMo-Pro 15 · GLM-5.3 15 · Kimi K3 15 · Grok 4.7 15 · Muse Spark 1.3 Contributor 60 · GLM-5.3-Flash 60 · MiMo-V2.6-Flash 60 · GPT 6 Luna 15 · Qwen3.8 Flash 30 · Qwen3.8 Max 15 · DeepSeek V4 Pro 15 · MiniMax M3 60 · Kimi K2.7 Code 60 · Qwen3.7 Plus 60 · Haiku 5.5 15 → **hepsi aynı** | S15 | V | **note only** (doğrulandı) |
| C11 | Saklama / eğitim | 30 gün: Grok, GPT Luna, Haiku 5.5; Muse Spark eğitir; diğerleri 0 gün | **Aynı.** Ek: GPT 5.6 Luna 30 gün; Beam Free 30 gün; Iceman Contributor Free eğitir + "Not ZDR"; LongCat 2.5 Free Çin'de barınır (Global bölge gerekir) | S15 | V | **note only** (doğrulandı) |
| C12 | Havuza girmeyen yeni/değişen Go modelleri | "Never selected" listesi | Listede zaten olanlar: GLM-5.2 (USD 60), MiMo-V2.5 (60) / V2.5-Pro (15), Muse Spark 1.2 Contributor (60), Hy4 Preview (30), LongCat-2.0 (60), Hy3 (60), GPT 5.6 Luna (15), Step 5 Preview (15). **Yeni:** **Hy4** (USD 60, ana sayfada "New"; AA v5 "Tencent Hy4" 35 @ 1.03 — DeepSeek 33 / MiMo-Pro 30'dan yüksek ama TB/Arena/DeepSWE satırı yok), **Iceman Contributor Free** (eğitir). Go sayfasında artık görünmeyenler: Grok 4.6, Kimi K2.6, MiniMax M2.7, LL Alpha Free, Exo Free, Big Pickle (kaldırıldıkları doğrulanmadı) | S15, S12 | V / B | Hy4: **not verified** (never selected, "aday" notuyla); diğerleri **note only** |
| C13 | Bedava modeller (Zen) | Zen ikizleri: `glm-5.3-flash-free`, `deepseek-v4.1-flash-free` | Hâlâ var + **`minimax-m3.1-flash-free`** (sıfır saklama, eğitim yok, sınırlı süre). `mimo-v2.6-flash-free` eğitir. Crouton Alpha Free 9 Kas'ta emekli | S16 | V | **must apply** (FR1 ikiz listesine MiniMax eklenir) |
| C14 | Efor varyantları (models.dev) | DeepSeek low/high/max · GLM low/high/max · MiMo yok · Kimi K3 max · Grok low–xhigh · Qwen low/medium/xhigh · Argon low/medium/high | **Aynı.** Yeni: Kimi K3.1 Pro `low`/`high`/`max`; MiniMax M3.1 Flash `low…max`. Çoğu liste "Go aboneliği anahtarı olmadığı için Go'da doğrulanmadı" notu taşır | S18 | topluluk | **note only** |
| C15 | Contributor yolları | Muse Spark 1.3 Contributor (eğitir, USD 60), Argon Contributor | Muse Spark 1.3 / 1.2 Contributor **aynı** (USD 60, Not ZDR, sınırlı bölgeler). Argon Contributor yok (C1) | S15 | V | **note only** |
| C16 | Go dışı yeni model | — | Gemini 4 Carbon (Google): 28 Eki'de AA v5'te #1 ilan edildi (AA makale başlığı); bugünkü tabloda Fable 5.2 (max 65) önde, Carbon high 60. Go'da değil, Google üyeliği OpenCode'da kullanılamıyor. Meta Muse Ember (36 @ 0.14) ve Muse Wonder (44 @ 6.95) AA'da var, Go'da yok | S12, S14, S15 | B | **note only** |

## Doğrulanamayanlar (`n/p`)

- AA v5 skorları: GPT 6 Luna, Muse Spark 1.3 (Contributor), MiMo-V2.6-Flash, Qwen3.8 Flash, Kimi K3, Fable 5.1; v5 bileşen bazlı skorlar (TB 4.0, FrontierCode, Omniscience/halüsinasyon, AutomationBench, Briefcase) model sayfalarında verilmiyor — yalnız makalede birkaç değer var.
- v4.3.2'nin AA'da hâlâ erişilebilir olup olmadığı; TB 4.0 skorlarının v5'te değişip değişmediği.
- DeepSWE v1.1 (Mercor) ve FrontierSWE v2 sahibi yayını: bu turda **okunmadı** (URL elimde yoktu, tahmin edilmedi) → Fable 5.2, Kimi K3.1 Pro, Argon için `n/p`. TB 4.0 için yayımlanmış güven aralığı: bulunamadı.
- Fable 5.2'nin ofansif güvenlik kapısındaki durumu (kapı Opus 4.8'de bırakıldı) — yeniden doğrulanmadı; Mythos 5.2 fiyat ayrıntısı ve plan düzeyi erişimi: not stated.
- Fable 5.2 `/fast` hız çarpanı; Fable 5.2'nin `ultrathink` kapsamı.
- Argon için 30 Kas sonrası cap; Argon Contributor'ın kalkma tarihi ve geri dönüp dönmeyeceği; MiniMax Free'nin Go'dan kalkma tarihi; Kimi K3.1 Pro'nun Go'ya eklenme tarihi (en erken anılma 28 Eki).
- `openai.com` gibi erişilemeyen sayfalar bu turda gerekmedi; Anthropic'in `news/claude-fable-5-2` URL'si 404 verdi (gerçek duyuru `anthropic.com/claude-fable-and-mythos-5-2`).

## Kaynaklar arası çelişkiler

- Opus 5.5 (max): AA makalesi **58**, liderlik tablosu **59** → olası v5 → v5.0.1 farkı (doğrulanmadı). DeepSeek V4.1 Flash 1017: makale **32**, tablo **33**.
- Fable 5.2 varsayılan eforu: API sayfaları `high`, Claude Code sayfası `medium` → farklı yüzeyler (A4'te ayrıldı).
- Fable'ın Pro planındaki durumu: duyuru dahil diyor (lansman teklifi), yardım merkezi kredi diyor (A5).
- Kimi K3.1 Pro: AA model sayfası ağırlık bağlantısı, makale "ağırlıklar henüz yayımlanmadı".
- `models/overview` ile deprecations tablosu (A19).

## Aşama 2 için önerilen uygulama listesi (onayınıza bağlı)

1. **Kadro:** Fable 5.1 → Fable 5.2 (USD 8/40), Fable 5.1 / Mythos 5.1 legacy; Mythos 5.2 ifadesi (Glasswing → doğrulama programları); `fable` takma adı (v2.1.321+); efor varsayılanlarında API / Claude Code ayrımı; `/fast` satırından Opus 4.8 çıkar; Haiku 4.5 ifadesi; ofansif kapıda Mythos 5.1 → 5.2.
2. **Havuz (19 → 19):** MiniMax M3.1 Flash Free çıkar, Kimi K3.1 Pro (P) girer; Argon satırı yeniden yazılır (D2); DeepSeek cap 100 ve tasks/mo; ZDR 30 Kas; "never selected" listesine Hy4 / Iceman; FR1 ikiz listesine `minimax-m3.1-flash-free`; yeniden türetme `scripts/derive_opencode_rows.py` ile (elle satır düzenlenmez).
3. **AA v5 (D1-a):** `II v5` sütunu yalnız doğrulanan satırlara; Step 2 çapalarında kaldırılan benchmark'lar işaretlenir; E1/E3/E8/H1 notlarına v5 karşılığı; E7'ye v5 DeepSeek `high` 29 / `max` 33 notu.
4. **Policy / evals / docs:** `routing-policy-version: iteration-27`; `routing_policy.json` aynası; `check_opencode_pool.py` (GM1/NC1 değişikliği ve yeni sayılar); evals'te yalnız bu değişikliklerin oynattığı goldenlar (Argon'a dokunanlar: `w1`–`w4`, `d1`, `g1`, `j1`, `t1`, `v1`, `z1`, `p1`; FR1'e dokunanlar: `r1`, `a*` deep-reasoning/science/doc-data satırları; `/fast`'a dokunanlar: Opus 4.8 örnekleri); README ×2, `claude-ai/instructions.tr.md`, `docs/LAUNCH.md`, `evals/README.md` (iteration-27 girişi). Eski `results/iteration-*` dosyalarına dokunulmaz.
5. **Kontroller:** `check_policy_sync.py`, `check_opencode_pool.py`, `check_examples.py`, `validate_benchmarks`, frontier testleri, `grade_routing.py --selftest`; soğuk-ajan çalıştırma listesi (yalnızca `skill/SKILL.md` okuyan taze ajanlar).

## Kaynaklar (10 Kas 2026'da okundu)

- **S1** https://platform.claude.com/docs/en/release-notes/overview — V
- **S2** https://platform.claude.com/docs/en/about-claude/models/overview — V
- **S3** https://platform.claude.com/docs/en/about-claude/model-deprecations — V
- **S4** https://platform.claude.com/docs/en/about-claude/pricing — V
- **S5** https://platform.claude.com/docs/en/build-with-claude/effort — V
- **S6** https://www.anthropic.com/claude-fable-and-mythos-5-2 (9 Kas 2026) — V
- **S7** https://code.claude.com/docs/en/changelog (v2.1.293 – v2.1.322) — V
- **S8** https://code.claude.com/docs/en/model-config — V
- **S9** https://code.claude.com/docs/en/fast-mode — V
- **S10** https://support.claude.com/en/articles/15424964-claude-fable-models-on-your-plan — V
- **S11** https://artificialanalysis.ai/articles/artificial-analysis-intelligence-index-v5 (27 Eki 2026) — B
- **S12** https://artificialanalysis.ai/leaderboards/models — B (kısmen okundu)
- **S13** https://artificialanalysis.ai/models/{kimi-k3-1-pro, claude-fable-5-2, gemini-4-argon, mimo-v2-6-pro, glm-5-3, deepseek-v4-1-flash} — B
- **S14** https://artificialanalysis.ai/articles (başlık/tarih listesi) — B
- **S15** https://opencode.ai/docs/go/ (sayfada tarih yok) ve https://opencode.ai/go — V
- **S16** https://opencode.ai/docs/zen/ — V
- **S17** https://opencode.ai/changelog, https://opencode.ai/console/changelog, https://opencode.ai/console/changelog/go-teams — V
- **S18** https://github.com/anomalyco/models.dev/tree/dev/providers/opencode-go/models (+ `raw.githubusercontent.com/.../opencode-go/models/*.toml`) — topluluk bakımlı, ikincil
- **S19** https://www.vals.ai/benchmarks/terminal-bench-4 (9 Kas), https://www.vals.ai/benchmarks/vibe-code — B
- **S20** https://arena.ai/leaderboard/agent (8 Kas), /text (9 Kas), /code/webdev (8 Kas) — B
