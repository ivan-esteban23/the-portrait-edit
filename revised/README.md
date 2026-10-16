# Rebuild the revised Issue 02

## Deliverables

- `The_Portrait_Edit_Issue_02_Revised.pdf`: 196 letter-size pages.
- `audit.md`: pre-design inspection and the complete rights-check inventory.
- `chapters.json`: one explicit chapter assignment for every study.
- `CHANGES.md`: revision summary, limitations, validation and a copy of the audit.
- `sample-cover.png`, `sample-chapter-opener.png`, `sample-study.png`: visually checked samples.
- `verification.json`: results of the content, page, image and layout checks.

The original 180-page PDF remains unchanged in `output/pdf/` in the repository. The revised build refactors the existing `scripts/build_issue_02.py`; it does not reconstruct an unknown template. Its earlier version remains in Git at commit `940eaab`.

## Source location

Repository: `/home/ivanaguilera/Projects/the-portrait-edit`.

The unchanged inputs are `DALL-E.prompts/dalle-prompts.md` and `DALL-E.prompts/Attachments/`. Markdown source filenames are authoritative. Do not rename attachments or silently resolve the six flagged pairings.

## Commands

Run from the repository root:

```bash
.venv/bin/python scripts/audit_issue_02.py
.venv/bin/python scripts/plan_issue_02.py
.venv/bin/python scripts/build_issue_02.py
.venv/bin/python scripts/verify_issue_02.py
```

The audit must run before the build. It checks that the source SHA-256 has not changed. `plan_issue_02.py` creates `revised/chapters.json`; omit this command when retaining deliberate manual edits to that mapping. The build reads the mapping and audit without modifying the Markdown or images.

The default PDF output is `revised/The_Portrait_Edit_Issue_02_Revised.pdf`. Use `--output /a/writable/path/The_Portrait_Edit_Issue_02_Revised.pdf` with the build command to change it. The verification script reads the output path from `revised/layout-checks.json`.

On a fresh machine, create a virtual environment and install `requirements.txt` if needed. This revision added no packages or fonts: it reused the existing ReportLab, Pillow, PyMuPDF and pypdf environment. Poppler's `pdftotext` is also required for inspection and verification.

Installed font paths used by the script:

- `/usr/share/fonts/noto/NotoSerif-Regular.ttf`
- `/usr/share/fonts/liberation/LiberationSans-Regular.ttf`
- `/usr/share/fonts/liberation/LiberationSans-Bold.ttf`

Adjust these paths for existing local fonts on another machine. There was no internet font or package installation for this revision.

## Verification details

The verifier compares normalized prompt text in the right-hand prompt boxes against the Markdown, checks all original notes, titles and Source strings, counts actual rendered contents numbers, and verifies each contents link target. It checks every text span against the page boundaries and recorded layout boxes, allowing 5 points for font ascent/descent metrics. The renderer additionally asserts paragraph heights against their allotted boxes. Every embedded reference retains its source pixel dimensions, aspect ratio and complete frame; there is no cropping or upward pixel resampling.

Body, working-note, glossary-definition and contents text are at least 9 pt. Running furniture and small labels retain the established smaller style. All labels/body use the Liberation Sans family, while headings use Noto Serif. Deep red is the only chromatic accent.

## Path limitation

The requested `/mnt/user-data/uploads/` location does not exist here. The baseline inspection therefore used the existing repository PDF, previously verified against its Documents copy. `/mnt/user-data/outputs/` could not be created because of host permissions. Files are delivered in this repository's `revised/` directory and `/home/ivanaguilera/Documents/The Portrait Edit - Issue 02 Revised/` instead.
