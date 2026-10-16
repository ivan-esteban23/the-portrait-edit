# Editorial review - pass 01

Baseline: `The_Portrait_Edit_Issue_02_Revised.pdf`, 196 Letter-size pages, from main commit `5235d883e9161eaed9f28633c539f4c34f39768e`. All page numbers below remain the same in the separate editorial export. Review scope is the three approved editorial changes and stronger validation, with no chapter reassignment or protected source editing.

## Must fix

### Automatic “Try this” wording - implemented

The baseline's prefix-and-filter logic can attach “Emphasize” to complete clauses, producing incomplete or awkward instructions. Specific examples include:

| Study | PDF page | Baseline issue | Reviewed replacement |
|---:|---:|---|---|
| 9 | 128 | Emphasize Mustard works best against a plain backdrop, so keep the background minimal. | Use a plain backdrop to emphasize the mustard dress. |
| 11 | 94 | Emphasize the dried flowers add a soft counterpoint to the leather; drop them for a sharper look. | Drop the dried flowers for a sharper look. |
| 12 | 129 | Emphasize "Closed-mouth smile" keeps the expression soft; change to "neutral" for a more serious tone. | Try a neutral expression for a more serious tone. |
| 14 | 131 | Emphasize Adding "soft film grain" gives a more vintage print look. | Add soft film grain for a vintage print look. |
| 15 | 18 | Emphasize "Looking up and off to one side" gives the image its mood; change to "direct gaze" for a more confident tone. | Try a direct gaze for a more confident tone. |
| 93 | 106 | Emphasize the swirl motif specific to match the knit detail. | Describe the swirl motif precisely. |
| 104 | 110 | Emphasize the patch unbranded to avoid text in the image. | Keep the patch unbranded. |
| 116 | 187 | Emphasize the graphics generic to avoid text in the image. | Keep the racing graphics generic, without readable text. |
| 149 | 140 | Emphasize the rhinestone detail generic to avoid readable text in the image. | Keep the rhinestone detail generic, without readable text. |
| 151 | 142 | Emphasize the print abstract to avoid readable text in the image. | Keep the print abstract, without readable text. |
| 158 | 146 | Emphasize the white-on-white palette soft and airy. | Keep the white-on-white palette soft and airy. |
| 160 | 122 | Emphasize the monograms simple and generic to avoid readable text. | Keep monograms simple and generic. |
| 166 | 167 | Emphasize the graphic abstract to avoid readable text in the image. | Keep the skull graphic abstract, without readable text. |

All 174 lines are now explicit editorial entries with exact supporting-note quotations. The build validates coverage and note provenance, rather than inventing a line when one is missing. The underlying prompts and notes are untouched.

### Six source-pairing conflicts - publisher decision pending

Studies 7/8/9 appear on pages 91/92/128; Studies 12/13/14 on pages 129/130/131. Their linked photographs differ from their prompt descriptions, as documented in the preserved audit. This pass retains all original images/filenames and the six “Review pairing” labels. A swap is explicitly outside scope; no correction is implied by the editorial export.

### Publication rights - publisher decision pending

All 174 study pages retain “Rights check”. Appearance and local filenames cannot establish identity, whether an image depicts a real person, ownership, a model release, or a license. No clearance judgment was made.

## Should improve

### Editor's-letter navigation, page 2 - implemented

The baseline letter describes nine chapters without offering direct navigation. A compact three-column directory now names all nine chapters and links to their existing openers: pages 14, 37, 53, 58, 72, 90, 127, 150 and 170. Existing letter text remains; the count row moves slightly lower to make room. No page is added.

### Repeated opener instruction - implemented

Pages 14, 37, 53, 58, 72, 90, 127, 150 and 170 originally repeated the same navigation instruction. Each now has one chapter-specific editorial sentence. Names, descriptions, order, study assignments, page targets and the existing visual identity remain.

### Verification coverage - implemented

The earlier verifier checked content and basic bounds but did not explicitly enforce bookmark destinations, actual PDF body sizes, collisions between separate text blocks, text/image overlap, or decoded image-pixel equality. The editorial verifier checks those invariants against the export, plus the new directory links and all protected baseline files.

### Original cross-reference and title conflicts - retained

Study 115, page 86: its original prompt says “This is a duplicate of section 82.” Its original note also refers to section 82. The accurate visible cross-reference is “Repeats Study 83.” Both protected source strings remain exactly unchanged. The earlier audit mentioned the note; inspection confirms the prompt has the same conflicting number.

Study 44, page 97: the protected title uses “Camo Knit Skirt”, while the prompt and notes describe a cloud-like pattern. No title or prompt correction is made.

## Optional

- Small-image quality: the 24 small references listed in the unchanged audit cannot gain genuine detail through PDF layout. Page 25 / Study 36 is a readable-review example of visible softness. Higher-resolution originals are a future input decision. Uncertain: acceptable print sharpness depends on the printer, paper and viewing distance; no physical print proof was performed.
- Chapter pacing: Folk & Landscape has four studies, whereas Knitwear & Layers has 36 (contents pages 7 and 10; openers 53 and 90). These unequal chapter lengths may merit a later editorial discussion, but the mapping remains protected in this pass.
- Short-prompt pages intentionally retain empty space below the right column. A more varied page system could be explored later; this pass does not introduce a second study-page layout.

## Visual inspection

Inspected ten readable PNGs: cover 1, letter 2, glossary 3-4, dense contents 10, opener 90, longest-prompt Study 5 on 60, small-image Study 36 on 25, duplicate Study 115 on 86, and pairing-review Study 7 on 91. Also inspected seven contact sheets covering all 196 pages. No visible clipping, crowding from the new copy, text/image collisions, or broken framing was found. Contact sheets provide an overview, not a claim that every word was read at thumbnail size; exact source preservation is checked separately against exported text.

All 183 PDF bookmarks and 183 internal links target the correct pages. Navigation validation is structural in the actual exported PDF; cross-viewer interactive behavior was not separately exercised in every PDF application.
