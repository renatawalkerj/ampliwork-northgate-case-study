# Open-source invoice/tax data search

Status: researched (fast pass, web search only — no datasets downloaded or inspected firsthand).

## Bottom line

**Recommend hand-building synthetic invoice data**, not adopting any of the open receipt/form datasets as-is. None of them are multinational supplier invoices with VAT/GST fields — they're consumer retail receipts or generic forms, single-country, single-language. Use one open VAT-rate dataset as a realism anchor for the numbers (rates, jurisdiction names) in the synthetic invoices. This also sidesteps a real risk: the brief wants the prototype to demo messy *business logic* (bad format, duplicate vendor, missing field), not OCR robustness — real-world scanned datasets pull effort toward solving OCR, which isn't the case-study's point.

## Invoice/receipt document datasets checked

| Dataset | What it actually is | License | Verdict |
|---|---|---|---|
| **SROIE / ICDAR2019** ([GitHub](https://github.com/zzzDavid/ICDAR-2019-SROIE), [paper](https://arxiv.org/abs/2103.10213)) | 1,000 scanned Malaysian retail receipts (grocery/restaurant), English, flat key-info fields (company, date, address, total) | CC-BY-4.0 (permissive, commercial OK w/ attribution) | Shape reference only — no VAT/tax fields at all, single country, retail not B2B supplier invoices. Not usable as-is. |
| **CORD** ([GitHub](https://github.com/clovaai/cord)) | ~11,000 Indonesian retail receipts, 30 fine-grained annotation classes (menu/subtotal/total) | CC-BY-4.0 | Same problem as SROIE — Indonesian retail receipts, not multinational B2B invoices with VAT breakdowns. Shape/layout reference only, if that. |
| **FUNSD** ([site](https://guillaumejaume.github.io/FUNSD/)) | 199 real scanned English-language forms (not invoices specifically), noisy/varied layout | **Research/non-commercial only** — explicitly restricted | Excluded on license alone even before relevance. Skip. |
| **Kaggle "Invoices Dataset" (cankatsrc)** ([Kaggle](https://www.kaggle.com/datasets/cankatsrc/invoices)) | Synthetic, generated with Python's Faker library | Kaggle-hosted, license not clearly stated on the page as CC0 — unverified | Faker-generated data has no real VAT/GST logic behind it (Faker doesn't model tax jurisdictions). Would need as much rework as building from scratch. Not worth adopting. |
| **"High-Quality Invoice Images for OCR"** (Kaggle/HF mirror, [HF](https://huggingface.co/datasets/Voxel51/high-quality-invoice-images-for-ocr)) | ~8,000 synthetic invoice *images* (seller/client, line items, tax calc, payment) | ODbL (Open Database License — share-alike on the data) | Closest in shape to a real invoice, but it's rendered images for OCR training, not structured multi-jurisdiction VAT data, and ODbL's share-alike clause is an extra complication for a client deliverable. Not worth the license friction for what it'd save. |

None of these are multi-language or multi-jurisdiction VAT/GST-aware. The brief's own detail — invoices in fourteen languages, three SAP instances, format rules that vary by jurisdiction — isn't representable by any of these sets regardless of license.

## VAT/GST rate reference data

| Dataset | Contents | License | Verdict |
|---|---|---|---|
| **vatnode/eu-vat-rates-data** ([GitHub](https://github.com/vatnode/eu-vat-rates-data)) | Standard/reduced/super-reduced/parking VAT rates + VAT-ID regex patterns for 45 European jurisdictions (EU-27 + UK, Switzerland, Norway, etc.), sourced from the EC's TEDB, refreshed daily, JSON | **MIT** (permissive, commercial use fine) | **Use this.** Real, current, well-licensed rates and ID-format patterns — exactly what's needed to make synthetic EU invoices numerically realistic (correct rate for the jurisdiction, plausible VAT ID format to violate for the "non-compliant format" messy-input variant). |
| gisostallenberg/vat-rates-1, dmitry/vat_rates, MiczFlor/VAT-EU-rates (GitHub) | Same underlying EC source, less actively maintained, CSV/gem/array formats | Mixed, mostly permissive | Redundant with vatnode — no reason to use a second source. |

No open dataset was found covering GST rates for non-EU jurisdictions (e.g. Singapore, where Northgate has a hub) or US sales/use tax at the same structured quality — those would need to be hand-entered from published government rate tables (a handful of values, not a dataset problem).

## Recommendation for the prototype

1. **Hand-build 3–5 synthetic invoices** (JSON or a simple structured format, not scanned images — the demo doesn't need OCR to make its point) representing a legal entity, jurisdiction, supplier, and transaction, per the information model in `answers/03-information-model.md`.
2. **Anchor the numbers** (VAT rates, VAT ID format) in the vatnode MIT-licensed rate table so a tax-literate panelist doesn't spot an implausible rate.
3. **Build in exactly one messy input** per the brief's own menu — recommend the **duplicate-vendor-with-different-tax-profiles** case, since it's the complaint the EMEA regional manager raised unprompted ("a third of our supplier master data is wrong... no model fixes that") and it's the one that most directly demos the exception path / human-in-the-loop rather than a clean OCR-to-answer pipeline. (Final choice belongs in `answers/04-prototype-notes.md` — this file only clears the data-sourcing question.)
4. Skip OCR/scanned-document datasets entirely for v1. If a later version needs to demo ingest from an actual scanned/PDF invoice, SROIE/CORD are fine as a *layout* reference (what fields sit where) but should not be presented as Northgate-realistic data.

## Claims for claims.md

| Claim | Status | Source | Notes |
|---|---|---|---|
| SROIE/ICDAR2019 dataset is CC-BY-4.0 licensed | ASSUMED | https://github.com/zzzDavid/ICDAR-2019-SROIE — needs check against official rrc.cvc.uab.es terms | Web-search-derived, not confirmed against the primary license file |
| CORD dataset is CC-BY-4.0 licensed | ASSUMED | https://github.com/clovaai/cord | Same caveat — verify against repo's LICENSE file directly |
| FUNSD dataset is restricted to non-commercial/research use only | ASSUMED | https://guillaumejaume.github.io/FUNSD/work/ | High-confidence exclusion regardless; worth a direct read of the terms page before citing in the deck |
| None of the surveyed open invoice/receipt datasets contain multinational VAT/GST-structured B2B invoices in multiple languages | ASSUMED | Fast-pass web search only, not a first-hand dataset inspection | If challenged in the room, be ready to say this was a search-based judgment, not exhaustive |
| vatnode/eu-vat-rates-data is MIT licensed and covers 45 European jurisdictions, updated daily from the EC's TEDB | ASSUMED | https://github.com/vatnode/eu-vat-rates-data | Verify the LICENSE file and spot-check one or two rate values against the EC source directly before relying on it in a live demo |
| No comparably-licensed open structured GST rate dataset exists for non-EU jurisdictions (e.g. Singapore) | ASSUMED | Web search only | Absence-of-evidence claim — worth a targeted follow-up search if a non-EU jurisdiction ends up in the demo |
| "High-Quality Invoice Images for OCR" dataset is ODbL licensed | ASSUMED | https://huggingface.co/datasets/Voxel51/high-quality-invoice-images-for-ocr | Not planned for use; recorded in case the option resurfaces |
