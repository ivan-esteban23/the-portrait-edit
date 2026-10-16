# Editorial changes - pass 01

## Implemented

- Reused and refactored `scripts/build_issue_02.py` on feature branch `editorial-revision-pass-01`, based on main commit `5235d883e9161eaed9f28633c539f4c34f39768e`.
- Replaced all automatic “Try this” wording with 174 explicit, reviewed lines in `editorial-copy.json`. Every line records its exact supporting original note. Missing, duplicate or stale-source entries fail the build.
- Added a compact nine-link chapter directory to the existing editor's letter on page 2. No page was added; the original letter wording remains and the count row is moved lower.
- Replaced the repeated generic navigation instruction on all nine openers with individual chapter-specific editorial lines. Chapter order, names, descriptions and assignments remain unchanged.
- Produced the separate `The_Portrait_Edit_Issue_02_Editorial_Revision.pdf`, with its own layout manifest, verifier report and preview directory. The generator refuses protected baseline output paths.
- Added actual-PDF bookmark, directory-link, font-size, overlap and decoded-pixel checks. Label bounds use the installed font's ascent/descent; overlap checks use visible glyph bounds to avoid mistaking unused font metrics for collisions.
- Updated `README.md` with editorial-only rebuild/verification commands and warnings about legacy commands that write baseline files.

## Protected content preserved

All 174 prompts, original working notes, study numbers, titles, Source filenames and reference images remain unchanged. Four shared-source pairs and five near-duplicate pairs remain, with accurate visible cross-references on both pages. “Review pairing” occurs only on Studies 7-9 and 12-14. All 174 studies retain “Rights check”. The neutral “Image Prompt” heading remains.

The chapter map and 193 protected repository files match their captured hashes and immutable Git objects. These include the source note, all 170 attachments, existing PDFs, audit files, mapping, original layout/verification JSON, original sample PNGs, root README and the unchanged legacy audit/planning/verification scripts. The only modified existing files are the approved build script and `revised/README.md`.

## Exact export verification results

- Opened successfully: 196 pages, each 612 × 792 points.
- Studies exactly once in rendered contents: 174.
- Normalized prompt matches: 174 / 174.
- Original titles, Source filenames and working notes preserved: 174 each.
- Explicit “Try this” lines with quoted note provenance: 174.
- Correct duplicate cross-references: 18 study pages.
- Pairing-review studies: 7, 8, 9, 12, 13, 14 only.
- Rights flags: 174 studies.
- Correct contents links: 174; chapter-directory links: 9.
- Correct chapter/study bookmarks and hierarchy: 183.
- Minimum measured exported body/notes/contents/glossary text: 9.0 pt.
- Text spans checked: 5191; logical-block comparisons: 28907; separate exported-span comparisons: 68412.
- No clipping operators, logical text collisions, visible glyph collisions, or text/image overlap found.
- Original decoded image pixels, dimensions, aspect ratio and full placement verified: 175 occurrences (174 study images plus cover), representing 170 unique reference filenames. No crop, distortion, retouch or upsampling.
- Independent `pdftotext -layout` pass confirms 196 pages and all Source strings.
- PDF SHA-256: `d50cd1f76b9cc896acd37a579727d860a914e40514bfa08f4d9df81ca9e6f015`.

Machine-readable results are in `editorial-verification.json`; geometry, source hashes and baseline hashes are in `editorial-layout-checks.json`.

## Rendered visual review

Ten readable PNGs were rendered and inspected: pages 1, 2, 3, 4, 10, 90, 60 (Study 5), 25 (Study 36), 86 (Study 115), and 91 (Study 7). Seven contact sheets covering all 196 pages were also inspected. No visible clipping, crowding caused by the editorial changes, overlap or missing image framing was found. The directory fits page 2 and the chapter-specific lines fit the existing openers.

The small-image preview remains softer than high-resolution references. This is an original-source limitation, with no pixel invention or enlargement performed. Navigation targets were verified in the actual PDF; interactive behavior was not manually exercised in every PDF viewer.

## Unresolved issues and limits

- The six original image-prompt conflicts remain intentionally flagged, with no image swaps.
- All rights flags remain; rights, identities, licenses and publication clearance were not inferred.
- Study 115's protected prompt and note both refer to section 82, while its accurate visible repeat label points to Study 83. Study 44's protected title differs from its cloud-pattern description. These require approval for a later source correction.
- Twenty-four small references remain; better original files would improve genuine detail.
- Chapter mapping and wider redesign/rebalancing remain outside this pass.
- No required verification check was unavailable. Physical print proofing, publication-clearance research and cross-viewer interactive testing are not claimed.
- No package or font was installed or downloaded. Existing ReportLab, Pillow/FreeType, PyMuPDF, Poppler, Git, Noto Serif and Liberation Sans were used.

## Handoff

This pass is delivered as a feature-branch PR for review. It does not modify main, force-push, or merge. See `EDITORIAL_REVIEW.md` for page-specific findings and `EDITORIAL_SUGGESTIONS.md` for prioritized future work.
