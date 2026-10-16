# Issue 02: baseline and editorial revision

The existing `The_Portrait_Edit_Issue_02_Revised.pdf` is the protected 196-page baseline. The separate first editorial pass is `The_Portrait_Edit_Issue_02_Editorial_Revision.pdf`; it also has 196 Letter-size pages.

## Editorial pass 01

This pass is limited to 174 explicitly reviewed “Try this” lines, a linked nine-chapter directory on the editor's letter, nine individual chapter-opener lines, and stronger verification. The chapter mapping, source prompts, titles, filenames, images, working notes, and existing review flags remain unchanged.

Files:

- `editorial-copy.json`: all 174 explicit lines, each with its exact supporting working note; nine opener lines.
- `EDITORIAL_REVIEW.md`: baseline findings, page references, and the scope of this pass.
- `EDITORIAL_CHANGES.md`: implementation, exact validation results, protected content, and unresolved issues.
- `EDITORIAL_SUGGESTIONS.md`: prioritized proposals outside this pass.
- `editorial-layout-checks.json`: rendered layout records, directory targets, source hashes, and baseline preservation hashes.
- `editorial-verification.json`: automated results and a separately recorded visual inspection.
- `editorial-samples/`: ten readable PNG previews and seven numbered full-issue contact sheets.

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

Inputs are the unchanged `DALL-E.prompts/dalle-prompts.md`, `DALL-E.prompts/Attachments/`, `revised/chapters.json`, and `revised/audit-data.json`. The four baseline audit/planning/verification scripts remain available; only the existing build script is refactored for this export.

No fonts or packages were added for this pass. The existing environment provides ReportLab, Pillow, PyMuPDF and pypdf, and Poppler provides `pdftotext`. Git is used to compare protected files against the immutable baseline commit. On a fresh machine, use the repository's `requirements.txt` only if the environment is missing those packages.

The script uses these installed fonts:

- `/usr/share/fonts/noto/NotoSerif-Regular.ttf`
- `/usr/share/fonts/liberation/LiberationSans-Regular.ttf`
- `/usr/share/fonts/liberation/LiberationSans-Bold.ttf`

The verifier uses the same local font files through Pillow/FreeType to measure visible glyph bounds at exported PDF character origins. Full font ascender/descender rectangles are not treated as visible ink collisions. Logical text boxes are also checked independently. Content containment allows up to 5 points for font metrics; overlap tests do not inflate the text rectangles.

## Verification and visual review

The new verifier checks the actual exported content, links, bookmarks, text spans, image placement and decoded image pixels. It verifies every protected file against both its captured hash and its immutable Git object, including the chapter mapping, original references, baseline PDF, previous manifests, previous verification results and previous sample PNGs.

Readable previews cover the cover, letter, both glossary pages, a dense contents page, an opener, the longest prompt, a small reference, a duplicate study and a pairing-review study. Seven contact sheets cover all 196 pages.

A verifier run resets `visual_inspection` to pending. Inspect the rendered previews and contact sheets before recording a completed visual inspection in the report and change notes. Automated PASS alone is not a claim of visual approval, source-pairing accuracy, or publication rights.

## Protected historical files

The baseline `audit.md`, `audit-data.json`, `CHANGES.md`, `chapters.json`, `layout-checks.json`, `verification.json`, extracted text files and existing sample PNGs are retained. The historical `/mnt/user-data/` path limitation described in those reports is unchanged; this editorial export is delivered under the repository's `revised/` directory.
