# Issue 02: baseline and editorial revision

The existing `The_Portrait_Edit_Issue_02_Revised.pdf` is the protected 196-page baseline. The separate first editorial pass is `The_Portrait_Edit_Issue_02_Editorial_Revision.pdf`; it also has 196 Letter-size pages.

## Editorial pass 01

This pass is limited to 174 explicitly reviewed “Try this” lines, a linked nine-chapter directory on the editor's letter, nine individual chapter-opener lines, and stronger verification. The first pass preserved the source. A subsequent, explicitly approved follow-up corrects only the six reference links and corresponding Source fields for Studies 7-9 and 12-14. Chapter membership, prompts, titles, original notes and attachment files remain unchanged; their obsolete pairing flags are removed, while every rights flag remains.

Files:

- `pairing-corrections.json`: the six approved old/new assignments and before/after source hashes.
- `editorial-copy.json`: all 174 explicit lines, each with its exact supporting working note; nine opener lines.
- `EDITORIAL_REVIEW.md`: baseline findings, page references, and the scope of this pass.
- `EDITORIAL_CHANGES.md`: implementation, exact validation results, protected content, and unresolved issues.
- `EDITORIAL_SUGGESTIONS.md`: prioritized proposals outside this pass.
- `editorial-layout-checks.json`: rendered layout records, directory targets, source hashes, and baseline preservation hashes.
- `editorial-verification.json`: automated results and a separately recorded visual inspection.
- `editorial-samples/`: sixteen readable PNG previews (including all six corrected study pages) and seven numbered full-issue contact sheets.

## Rebuild and verify

From `/home/ivanaguilera/Projects/the-portrait-edit`:

```bash
.venv/bin/python -B scripts/build_issue_02.py \
  --edition editorial \
  --output revised/The_Portrait_Edit_Issue_02_Editorial_Revision.pdf \
  --layout-output revised/editorial-layout-checks.json

.venv/bin/python -B scripts/verify_editorial_issue_02.py \
  --pdf revised/The_Portrait_Edit_Issue_02_Editorial_Revision.pdf \
  --layout revised/editorial-layout-checks.json \
  --report revised/editorial-verification.json \
  --samples revised/editorial-samples
```

Both scripts also default to these editorial paths. The generator refuses an output or manifest path that would overwrite a protected baseline artifact. It requires one explicit copy entry for every study and verifies the quoted supporting note against the Markdown. There is no automatic wording fallback.

Do not rerun `audit_issue_02.py`, `plan_issue_02.py`, or the original `verify_issue_02.py` for this editorial export: those legacy commands write baseline audit, mapping, verification, or preview files. This pass reads those files without changing them.

The original baseline generator is available in Git at commit `5235d883e9161eaed9f28633c539f4c34f39768e`. Reconstruct historical exports in a separate checkout if required.

## Inputs and environment

Inputs are `DALL-E.prompts/dalle-prompts.md`, `DALL-E.prompts/Attachments/`, `revised/chapters.json`, the historical `revised/audit-data.json`, and `revised/pairing-corrections.json`. The generator proves the Markdown differs from the immutable baseline only in the six approved links/Source fields and the chapter file differs only in their corresponding Source metadata. All 174 prompt and working-note texts remain byte-for-byte unchanged in the source. The historical audit is retained rather than overwritten or falsely described as current. The four baseline audit/planning/verification scripts remain available; only the existing build script is refactored for this export.

No fonts or packages were added for this pass. The existing environment provides ReportLab, Pillow, PyMuPDF and pypdf, and Poppler provides `pdftotext`. Git is used to compare protected files against the immutable baseline commit. On a fresh machine, use the repository's `requirements.txt` only if the environment is missing those packages.

The script uses these installed fonts:

- `/usr/share/fonts/noto/NotoSerif-Regular.ttf`
- `/usr/share/fonts/liberation/LiberationSans-Regular.ttf`
- `/usr/share/fonts/liberation/LiberationSans-Bold.ttf`

The verifier uses the same local font files through Pillow/FreeType to measure visible glyph bounds at exported PDF character origins. Full font ascender/descender rectangles are not treated as visible ink collisions. Logical text boxes are also checked independently. Content containment allows up to 5 points for font metrics; overlap tests do not inflate the text rectangles.

## Verification and visual review

The new verifier checks the actual exported content, links, bookmarks, text spans, image placement and decoded image pixels. It verifies every protected file against both its captured hash and its immutable Git object, including original references, baseline PDF, historical audit, previous manifests, previous verification results and previous sample PNGs. The Markdown and chapter Source metadata are instead checked against a precisely reconstructed approved delta; chapter membership must remain identical. Documentation updates are excluded from immutable-file checks.

Readable previews cover the cover, letter, both glossary pages, a dense contents page, an opener, the longest prompt, a small reference, a duplicate study and a formerly flagged study, plus dedicated readable previews of all six corrected pairings. Seven contact sheets cover all 196 pages.

A verifier run resets `visual_inspection` to pending. Inspect the rendered previews and contact sheets before recording a completed visual inspection in the report and change notes. Automated PASS alone is not a claim of visual approval, source-pairing accuracy, or publication rights.

## Protected historical files

The baseline `audit.md`, `audit-data.json`, `CHANGES.md`, `layout-checks.json`, `verification.json`, extracted text files and existing sample PNGs are retained. The historical `/mnt/user-data/` path limitation described in those reports is unchanged; this editorial export is delivered under the repository's `revised/` directory.

## Approved pairing follow-up

The current editorial export resolves these approved references: 7 → 4992.jpg, 8 → 4993.jpg, 9 → 4991.jpg, 12 → 5032.jpg, 13 → 5030.jpg, 14 → 5031.jpg. Source filenames in the Markdown and chapter metadata are updated consistently, without renaming any attachment. There are no remaining active “Review pairing” labels for this original six-study set. This resolution does not imply publication clearance; all 174 “Rights check” flags remain.

`pairing-study-007.png`, `008`, `009`, `012`, `013`, and `014` in `editorial-samples/` show all six corrected pages. The older `review-pairing-study.png` filename is retained for compatibility, but now displays the corrected Study 7 page. See the current changes report for the approved correction table and remaining decisions.

## Larger type edition

`The_Portrait_Edit_Issue_02_Larger_Type.pdf` is a separate 196-page edition with 12 pt prompts, 11.5 pt notes and glossary definitions, and 11 pt contents. It preserves all approved content and reference images. See `LARGER_TYPE_CHANGES.md` for checks and limits.

```bash
.venv/bin/python -B scripts/build_issue_02_readable.py
.venv/bin/python -B scripts/verify_issue_02_readable.py
```

These write only `larger-type-*` reports/previews and the larger-type PDF. The verifier resets visual inspection to pending; inspect rendered samples before recording visual review.
