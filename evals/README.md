# model-secici eval seti

`skill/SKILL.md` (ve `skill/reference.md`) her değiştiğinde elle iz sürmek yerine
buradaki setleri kullan.

## 1. Routing eval (fonksiyonel doğruluk)

`routing/evals.json` — README.md'deki doğrulama tablosunun (16 satır, id 1-16)
makine-okunur kopyası. Kaynak README kalır; buraya elle senkronize et.

**Nasıl koşturulur (yeni bir SKILL.md değişikliğinden sonra):**
1. Yeni bir `results/iteration-<N>/` klasörü aç.
2. Her eval id için, **fresh/soğuk bir ajan** (yeni bir alt-agent veya yeni bir
   konuşma) `skill/SKILL.md`'yi doğrudan okuyup promptu yönlendirsin, sadece
   ham çıktı satırını `eval-<id>.txt`'ye yazsın. **`Skill` tool'unu kullanma** —
   aynı konuşma içinde önbellekleme yapıp eski içerik döndürdüğü bu oturumda
   doğrulandı (bkz. proje geçmişi). Fresh bir agent/konuşma bu sorunu bypass eder.
3. `python routing/grade_routing.py --results-dir routing/results/iteration-<N>`
   çalıştır — regex tabanlı, deterministik, LLM gerektirmez.

**Neden LLM gradера değil script:** çıktı formatı tek satırlık, sabit kalıplı
("Model · efor: X" veya "opusplan · plan: X · uygulama: Y") — bu, doğrulaması
öznel değil mekanik olan bir durum. skill-creator'ın kendi tavsiyesi de bu yönde
("For assertions that can be checked programmatically, write and run a script").

## 2. Trigger eval (description'ın doğru anlarda tetiklenmesi)

`trigger/trigger_eval_set.json` — 20 sorgu (10 tetiklemeli, 10 tetiklememeli,
özellikle "yakın-ıskalama" senaryoları: fiyat sorusu, ayar sorusu, çıplak görev
isteği gibi model-secici ile karışabilecek ama olmayan durumlar).

**Nasıl koşturulur:** skill-creator'ın `scripts/run_eval.py`'ı kullan:
```
python -m scripts.run_eval --eval-set trigger/trigger_eval_set.json \
  --skill-path <kurulu skill yolu> --verbose
```
Bu, her sorgu için gerçek `claude -p` alt-süreci başlatıyor (varsayılan 3 tekrar
× 20 sorgu = 60 gerçek çağrı) — **bu bir kota maliyeti**, router'ın kendi
felsefesiyle doğrudan çelişir. Sık koşturma, sadece description değiştiğinde.

## Çalıştırma geçmişi (28 Temmuz 2026)

- **iteration-1:** 13/16 geçti. 3 sapma bulundu (frontier kapısının "üç şart
  AND" okunması, `opusplan` flagship örneğinde yürütüm fiilinin yazılı
  olmaması, "mimari karar" etiketinin R=2/R=3'ü bulanıklaştırması) — kullanıcı
  onayıyla `SKILL.md`'ye düzeltildi (`claude-ai/instructions.tr.md`'ye de
  taşındı, `opusplan` kısmı hariç — o zaten Claude.ai'da geçerli değil).
- **iteration-2:** 15/16 (fix'lerden biri R=2/R=3 örneğini flagship senaryoyla
  çakıştırdı — id 10 tekrar başarısız oldu, ikinci bir düzeltmeyle giderildi).
- **iteration-2 (id 10 tekrar):** 16/16.
- **iteration-2 (id 17-21 eklendi):** Kural 2(b) matematik/ispat, Kural 2(c)
  araçsız akıl yürütme, Adım 0 madde 2 (sessiz yanlış varsayım), Adım 0 madde 4
  (iki makul yorum), ve `opusplan`+`ultracode` gelişmiş kombinasyon notu (id 21,
  gözlemsel — makine ile kesin gradelenemez) eklendi. 20/20 otomatik geçti + id
  21 gözlemsel olarak tutarlı bir cevap verdi (bkz. not aşağıda).

**İç-tutarlılık denetimi sonucu (28 Temmuz 2026):** Taze bir ajan `SKILL.md`+
`reference.md`'yi baştan sona okuyup 4 yeni (daha önce fark edilmemiş) gerçek
çelişki buldu, 1 düşük-güvenli not:

1. **R rubriği kendi örneğiyle çelişiyordu** — R=2 tanımı "tek satır config"i
   örnek gösteriyordu, ama `MAX_RETRIES` örneği R=3 etiketliydi. Düzeltme: R=2
   "izole" tek satır, R=3 "sistem-geneli davranış yöneten" tek satır (retry/
   timeout/rate-limit gibi) — kod uzunluğu değil, deploy-fark edilme
   penceresinde biriken hasar asıl kriter.
2. **"Kapı tetiklenirse skorlamayı ezer" iki farklı anlamda kullanılıyordu** —
   siber güvenlik/frontier gibi kapılar modeli tam belirliyor ("belirleyici"),
   ama 200k-bağlam kapısı sadece Haiku'yu eliyor ("eleyici"), final modeli
   Adım 2/3 veriyor. İkisi aynı tabloda ayrım yapılmadan "ezer" deniyordu.
   Ayrıca belirleyici bir kapı ateşlense bile `ultracode` uygunluğunun (W/süre)
   ayrıca kontrol edilmesi gerektiği netleştirildi (siber güvenlik örneği zaten
   `ultracode`'a çıkıyordu ama kural metni bunu açıklamıyordu).
3. **Çıktı formatı "hiçbiri yazılmaz" diyordu ama 3 ayrı yerde "notu çıktıya
   ekle" deniyordu** — Kural 1 (R=3 onay notu), opusplan'ın efor-uyarısı,
   "gelişmiş kombinasyon" notu. Düzeltme: Çıktı formatı artık sadece İKİ
   zorunlu istisnayı açıkça listeliyor (R=3 notu, opusplan uyarısı);
   "gelişmiş kombinasyon" notunun **çıktıya eklenmediği** artık açık.
4. **200k-bağlam kapısı hiç test edilmemişti** — id 22 eklendi, "eleyici kapı"
   davranışını (sadece Haiku'yu eler, final model Adım 2/3'ten gelir) doğruladı.
5. (Düşük güven, düzeltilmedi) Sözleşme-madde-analizi (R=2) ile hukuki-savunma-
   stratejisi (R=3) arasındaki sınır makul ama hiçbir yerde açıkça kural
   olarak yazılmamış — sadece iki örneğin karşıtlığından çıkarılabiliyor.

Tüm düzeltmeler `SKILL.md`, `claude-ai/instructions.tr.md`'ye taşındı
(`opusplan`'a özgü kısımlar hariç). Düzeltmeler sonrası 22 senaryo (21 otomatik
+ 1 gözlemsel) taze ajanlarla yeniden koşturuldu: **21/21 otomatik geçti**, id
21 tutarlı bir cevap verdi. Ayrıca R=3 notu artık id 4 ve id 10'da da doğru
şekilde beliriyor (önceden sadece R=3∧D=0 durumunda test edilmişti).

## Codex tarafının Luna/Terra-low'a neredeyse hiç düşmemesi — 2 kök neden bulundu (6 Ağustos 2026)

Kullanıcı raporu: gerçek kullanımda Codex tarafı hep "Sol · high" ya da
"Terra · medium" veriyor, Luna neredeyse hiç çıkmıyor. 5 taze-prompt tanılama
turu (iteration-6, t1-t5) bunu doğruladı ve **iki ayrı, hem Claude hem Codex'i
etkileyen kök neden** buldu (Codex'e özgü değil — Codex tarafında Luna/Terra-low
seyrekliği yüzünden daha görünür oldu):

1. **D=1/D=2 sınırı belirsizdi.** "İyi belgelenmiş kalıp" (ör. cursor-based
   pagination) belirsizlikte D=2'ye yuvarlanıyordu. Düzeltme: "kaç bağımsız
   tasarım kararı sende kalıyor" teşhisi + D=1/D=2 karşıt örnekleri eklendi.
2. **D=0'ın kod-dışı alanda çapası yoktu** (sadece "tek cümle"). Çok
   paragraflı ama içerik değişmeyen (salt biçim/ton) işler D=1'e yuvarlanıyordu.
   Düzeltme: "uzunluk önemsiz, seçim/kısaltma/sentez yoksa D=0" netleştirmesi.
3. **(Doğrulama sırasında bulunan 3. kök neden, R ekseni)** R rubriği "izole UI
   değeri" örneğini R=2 etiketlemişti — bu, normal PR-incelemeli kod
   değişikliklerini (buton rengi gibi) yanlışlıkla R=2'ye sokup Haiku/Luna'yı
   gereksiz eliyordu. Düzeltme: kod tabanı değişikliği varsayılan R=1, R=2/R=3
   sadece canlıya doğrudan giden (kod incelemesiz) operasyonel değerler için.

**Doğrulama:** Fix öncesi belirsiz olan 2 senaryo (pagination, çok-paragraf
yeniden yazım) + R-ekseni fix'i sonrası 2 senaryo (buton rengi → artık Haiku/
Luna; feature-flag → hâlâ doğru şekilde R=2'de kalıyor, aşırı düzeltme yok)
taze ajanlarla tekrar koşturuldu, hepsi beklenen (düşük) tier'a düştü, hiç
regresyon yok (mevcut R=3/D=3 örnekleri hâlâ doğru). 4 senaryo kalıcı sete
eklendi (r1, r2, s1, s3).

## Her zaman ikili çıktı — yeniden tasarım (6 Ağustos 2026)

Kullanıcı isteği: "Skill çalışırken hem ChatGPT hem Claude için öneri yapmalı,
ikisini birlikte yazmalı" + token kullanımı endişesi + Claude Chat güncellemesi.

**Mimari değişikliği:** "Ekosistem Seçimi" (hangi ekosistem seçilsin) adımı
tamamen kaldırıldı — artık ekosistem seçilmiyor, **her zaman ikisi de**
üretiliyor. R/D/W/C bir kez hesaplanıp iki ayrı (Claude/Codex) eşleme
tablosuna bakılıyor. Siber güvenlik/biyoloji-bitişik promptlarda Codex satırı
"doğrulanmadı — Claude kullan" yazıyor (güvenlik-fallback zinciri Codex'te
doğrulanmadığı için). Çıktı formatı `<Ekosistem> · Model · efor` tek satırından
`Claude: ...` / `Codex: ...` iki satırına geçti, paylaşılan R=3 notu artık
tekrarlanmıyor (iki tarafı da tek satırda kapsıyor).

**Token verimliliği testi:** Fresh bir doğrulama ajanına hem eski hem yeni
tasarımı karşılaştırması istendi. Sonuç: "always both" yapısı kendi başına
ihmal edilebilir ek yük getiriyor çünkü R/D/W/C paylaşılan ve eşleme
tabloları neredeyse ayna simetrik; eski "Ekosistem Seçimi" adımının kendisi de
bir karar maliyetiydi (hangi ekosistem?) — bu maliyetin kaldırılması ikinci
satırı üretmenin maliyetini büyük ölçüde dengeliyor. Net izlenim: **tek-
ekosistemli router'dan belirgin şekilde daha ağır değil.**

**Doğrulama (iteration-5, 10 senaryo, 10/10 geçti):**
- d1-d7: skill'in kendi örnekleriyle örtüşen senaryolar (hacim kapısı, taban
  durum, siber güvenlik/biyoloji "doğrulanmadı", paylaşılan R=3 notu, opusplan
  yanında Codex'in bağımsız cevabı, Adım 0 blok — iki tarafı da durdurur).
- n1-n3: **skill örneklerinde hiç geçmeyen, gerçekten yeni promptlar**
  (genelleme testi) — sahte-bağımsızlık "decoy" (Sol Ultra/`ultracode` dilini
  taklit eden ama D=1 olan bir prompt, doğru şekilde tetiklenmedi), savunma-
  vs-saldırı güvenlik ayrımı (Terraform port incelemesi doğru şekilde siber
  güvenlik kapısını tetiklemedi — "offensive" değil, savunma amaçlı), basit
  ama R=2 olan bir migration (Haiku/Luna'ya düşmediği doğrulandı).

Doğrulama ajanının kendi notu: ilk 7 senaryonun çoğu skill'in kendi örnekleriyle
örtüştüğü için "kuralları sıfırdan uygulama" değil "kendi örneklerini doğru
aktarma" testi gibiydi — bu yüzden n1-n3 ayrıca eklendi, gerçek genelleme
yeteneğini sınamak için.

`evals.json` şeması değişti: eski 28 senaryo (`format_outdated: true`
işaretlendi, Codex-tarafı geri-doldurulmadı — spekülasyonla doldurmak yerine
dürüstçe "backfill gerekiyor" bırakıldı) + yeni 10 senaryo
(`expected_claude`/`expected_codex`/`expected_shared_note`/`expected_claude_note`/
`blocked` alanlarıyla). `grade_routing.py` iki-satırlı çıktıyı ayrı ayrı
gradeleyecek şekilde yeniden yazıldı.

## Dual-provider genişlemesi (5 Ağustos 2026)

Router Claude-only'den Claude+Codex/ChatGPT'ye genişletildi (yeni "Ekosistem
Seçimi" adımı + "Codex Kolu"). 6 senaryolu regresyon (Claude tarafı, id 1/5/8/
10/14/16) + 6 yeni senaryo (c1-c5, v1 — Codex Kolu ve Ekosistem Seçimi mantığı)
`results/iteration-4/`'te koşturuldu.

**Bulunan ve düzeltilen 2 gerçek tutarsızlık** (iki bağımsız ajanın aynı promptu
farklı yorumlamasından ortaya çıktı):
1. `opusplan` çıktı formatına ekosistem öneki eklenmesi hiç belirtilmemişti —
   bir ajan `Claude Code · opusplan · ...` yazdı, diğeri `opusplan · ...`
   (öneksiz). Düzeltme: Çıktı formatı artık bunu açıkça zorunlu kılıyor.
2. Codex Kolu'nun kendi örnek listesinde "1000 destek talebini kategorilere
   ayır" (ortam belirtmeden) Codex/Luna'ya çıkıyor gösterilmişti — ama Ekosistem
   Seçimi'nin kendi kurallarına göre (ortam belirtilmemiş, gerçek paralellik
   sinyali yok) bu prompt aslında **Claude**'a düşüyor. Örnek "Codex'te 1000
   destek talebini..." şeklinde düzeltildi, ayrıca bu tam çelişkiyi açığa
   çıkaran bir eval (c3) kalıcı sete eklendi.

Ayrıca `grade_routing.py`'de bir dispatch hatası bulundu: `opusplan` tespiti
sadece string'in **başında** arıyordu (`expected.startswith("opusplan")`) —
ekosistem öneki eklenince (`"Claude Code · opusplan..."`) bu artık başta değil,
dispatch kırılıyordu. `in` ile substring kontrolüne çevrildi. Ayrıca Codex
model isimleri (Luna/Terra/Sol/Sol Ultra) ve ekosistem alanı (Claude Code vs
Codex) doğrulamasına eklendi — "Sol" / "Sol Ultra" substring çakışmasına
dikkat edildi (uzun isim önce kontrol ediliyor, kısa isim kendi üst-string'i
içinde "beklenmeyen model" olarak yanlış pozitif üretmiyor).

**Sonuç:** Claude tarafında 0 regresyon (6/6), yeni mantıkta 6/6 geçti —
toplam 27 eval'lık kalıcı set, 12/12 bu iterasyonda otomatik gradelenen geçti
(kalan 15'i önceki iterasyonlarda zaten doğrulanmıştı, tekrar koşturulmadı).

Trigger eval'ı (`trigger/trigger_eval_set.json`) henüz koşturulmadı. İki engel
var: (1) kota maliyeti (~20 sorgu × gerçek `claude -p` çağrısı), (2) bu ortamda
(Claude Desktop / local-agent-mode) `claude` CLI binary'si PATH'te yok — script
`subprocess`'le `claude -p` çağırdığı için gerçek Claude Code CLI kurulu bir
terminalde çalıştırılmalı. O ortamda şunu çalıştır (skill-creator dizininden):

```
python -m scripts.run_eval \
  --eval-set <repo>/evals/trigger/trigger_eval_set.json \
  --skill-path <kurulu skill yolu, ör. ~/.claude/skills/model-secici> \
  --runs-per-query 1 --verbose
```

`--runs-per-query 1` kota maliyetini 3'te birine indirir (varsayılan 3) —
istatistiksel güven düşer ama ilk kaba sinyal için yeterli; description
gerçekten değişip iterasyon gerekirse `run_loop.py` ile 3'e çıkarılabilir.
