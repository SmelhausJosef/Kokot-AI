# Excel Import Notes (Zakázka sheet)

This document summarizes findings from the sample file in `ImportExcel/APT Kvilda - Rozpočet s VV.xlsx` and suggests an algorithm for extracting BudgetHeaders and BudgetItems.

## Source File
- Sample workbook: `ImportExcel/APT Kvilda - Rozpočet s VV.xlsx`
- Relevant sheet: `Zakázka`
- Sheet dimension: `A1:V5129`
- Other sheets present: `Krycí List`, `Rekapitulace`, `Figury` (ignored for now)

## Header Row
Header labels appear on row 4.

Column mapping (by header text):
- `Poř.` (order)
- `Typ`
- `Kód`
- `Popis`
- `MJ` (unit)
- `Výměra` (quantity)
- `Jedn. Cena` (unit price)
- `Cena` (total price)
- `Jedn. hmotn.` (unit mass)
- `Hmotnost` (mass)
- `Jedn. suť` (unit waste)
- `Suť` (waste)
- `Sazba DPH` (VAT rate)
- `DPH` (VAT amount)
- `Cena s DPH` (total with VAT)

## Row Types (Typ column)
Unique values observed in the `Typ` column:
- `Stavba`
- `Skupina objektů`
- `Objekt`
- `Podobjekt`
- `Oddíl`
- `SUB`

Interpretation:
- The first five values are hierarchical headers (BudgetHeaders).
- `SUB` rows are BudgetItems.

## BudgetHeader Rows
Observed patterns:
- Column `A` contains a hierarchical path (e.g., `Kvilda, penzion/00_IO/IO.01/001_IO.01/001.`).
- Column `D` (`Typ`) indicates the header level.
- Column `F` (`Popis`) contains the header name.
- Column `J` (`Cena`) often contains the total for the header.
- Columns `P` (`DPH`) and `Q` (`Cena s DPH`) can contain totals for the header.

## BudgetItem (SUB) Rows
Observed patterns:
- Column `D` is `SUB`.
- Column `C` holds the item order number (`Poř.`) for SUB rows.
- Column `E` (`Kód`) can be empty for some rows.
- Column `F` (`Popis`) is the item description.
- Column `G` (`MJ`) is the unit.
- Column `H` (`Výměra`) is the quantity.
- Column `I` (`Jedn. Cena`) is unit price.
- Column `J` (`Cena`) is total price.
- Column `O` (`Sazba DPH`) is VAT rate.
- Column `P` (`DPH`) is VAT amount.
- Column `Q` (`Cena s DPH`) is total with VAT.
- Mass/waste fields (`K`-`N`) appear but are often zero.

Some SUB rows contain empty `Kód` or `Jedn. Cena` values; treat them as valid items.

## Measurement / Quantity Detail Lines
Many items are followed by lines describing calculation details:
- Rows with `Výkaz výměr:` (in column `E`) start a measurement block.
- Rows with `Ztratné:` (in column `E`) indicate loss/waste adjustments.
- Follow-up rows often store numeric strings in column `F`, sometimes with commas and non-breaking spaces.
- These lines appear between the item row and the next header/item row.

Recommended handling:
- Either store these lines as `measurement_notes` attached to the last item, or ignore them for the initial import.
- If parsing numbers, normalize by removing spaces/NBSP and replacing comma with dot.

## Suggested Parsing Algorithm
1. Load workbook and select the `Zakázka` sheet by name.
2. Detect the header row by finding `Typ` and `Popis` in the same row (row 4 in the sample).
3. Build a column map keyed by header text for resilient parsing.
4. Initialize a `header_stack` based on type order:
   - `Stavba` -> level 1
   - `Skupina objektů` -> level 2
   - `Objekt` -> level 3
   - `Podobjekt` -> level 4
   - `Oddíl` -> level 5
5. Iterate rows after the header row:
   - If `Typ` is a header type: create/update a BudgetHeader node, update the stack at that level, and drop deeper levels.
   - If `Typ` == `SUB`: create a BudgetItem, attach it to the deepest header in the stack (usually `Oddíl`).
   - If `Kód` or `Popis` contains `Výkaz výměr:` or `Ztratné:`: treat as measurement detail for the last item.
6. Persist BudgetHeaders and BudgetItems (and optional measurement notes).

## Data Normalization Notes
- Excel values may appear as numeric strings (`593.9`) or locale-formatted text (`1 454,656`).
- Normalize numbers by:
  - Removing spaces and NBSP.
  - Replacing comma with dot.
  - Parsing to decimal to avoid float precision loss.
- Keep raw strings alongside parsed values if validation is needed later.

## Open Questions
- Should header totals (`Cena`, `DPH`, `Cena s DPH`) be stored or recomputed from items?
- Should measurement lines be stored as structured data or free-text notes?
- Should empty `Kód` be allowed or replaced with a generated placeholder?
