# Editorial changes - pass 01 and approved pairing follow-up

## Implemented editorial pass

- Reused `scripts/build_issue_02.py` on `editorial-revision-pass-01`, based on main commit `5235d883e9161eaed9f28633c539f4c34f39768e`.
- Replaced automatic “Try this” wording with 174 explicit, reviewed lines and supporting-note quotations in `editorial-copy.json`.
- Added nine linked chapter entries to page 2 without adding a page, and nine chapter-specific opener lines.
- Added a separate editorial export, layout manifest, verification report, readable previews and full-issue contact sheets. Historical baseline output paths are protected from overwrite.

## Subsequently approved reference corrections

After reviewing current/proposed image boards, the user explicitly approved these six reference-link and corresponding Source-field changes:

| Study | PDF page | Previous Source | Approved Source |
|---:|---:|---|---|
| 7 | 91 | `4991.jpg` | `4992.jpg` |
| 8 | 92 | `4992.jpg` | `4993.jpg` |
| 9 | 128 | `4993.jpg` | `4991.jpg` |
| 12 | 129 | `5030.jpg` | `5032.jpg` |
| 13 | 130 | `5031.jpg` | `5030.jpg` |
| 14 | 131 | `5032.jpg` | `5031.jpg` |

The Markdown changes only those six attachment links and six Source fields. The corresponding Source metadata in `chapters.json` is updated, but no chapter assignments, order, names or titles change. No attachment is renamed, retouched or resampled. All 174 prompt and original working-note texts remain byte-for-byte unchanged in the source.

The six obsolete “Review pairing” labels are removed from the current editorial export. All 174 “Rights check” flags and all duplicate/near-duplicate pages with accurate cross-references remain. The editor's letter and current documentation explain the approved corrections; `pairing-corrections.json` records approval and before/after hashes.

The generator/verifier reconstruct the precisely authorized source delta from Git and reject every other Markdown or chapter-map change. The historical `audit.md`, `audit-data.json`, old manifests, verification results, sample PNGs and baseline PDFs remain unchanged. Earlier claims that all links/Source fields were untouched describe the initial pass before this separate approval; the current explicit exception is limited to the six rows above. The pre-correction editorial PDF and source remain available in Git at `854d94a`.

## Exact current export verification

- Opens successfully: 196 Letter pages, 612 × 792 points each.
- All 174 studies appear exactly once in the rendered contents.
- All 174 exported prompts, original notes and titles match the source; reconstructing the approved delta proves original prompt/note bytes were preserved against the immutable baseline.
- All 174 displayed Source filenames match the current source, with exactly six approved corrections.
- Chapter membership unchanged; 174 reviewed “Try this” entries retain exact note provenance.
- Rights flags: 174; remaining active pairing flags from the original six-study set: 0.
- Accurate duplicate cross-references: 18 study pages.
- Correct navigation: 174 contents links, 9 directory links and 183 chapter/study bookmarks.
- Minimum exported body/notes/glossary/contents text: 9.0 pt.
- Checked 5191 text spans, 28907 logical-block comparisons and 68412 separate-span comparisons; no clipping, text collisions or text/image overlap found.
- Original decoded pixels, dimensions, aspect ratio and full placement verified for 175 image occurrences, representing 170 unique filenames. No crop, distortion, retouch or upsampling.
- 190 unchanged protected files match both captured hashes and immutable Git objects. Source and chapter metadata are checked separately against the approved delta; current README/build changes are documented exceptions.
- Independent `pdftotext -layout` pass confirms 196 pages and all current Source strings.
- Documented relative-path build/verification commands completed successfully.
- PDF SHA-256: `1dbee4ff29e34585b941352edb588493c420d3a79b8f2e1a4bf188b760f91756`.

## Visual review

Six dedicated corrected-study previews and the updated letter were inspected at readable resolution (pages 91, 92, 128, 129, 130, 131 and 2). Updated contact sheets 1, 4 and 5 were inspected. Eight other readable previews and contact sheets 2, 3, 6 and 7 are byte-identical to the earlier inspected export. The current set contains 16 readable PNG files and seven sheets covering all 196 pages. No visible clipping, crowding, overlap or broken framing was found. All six images/Source fields match the user-approved assignments.

## Remaining decisions and limits

- Reference publication permissions remain a publisher decision; no identity, ownership, license or clearance was inferred.
- Twenty-four small original references remain; better original files would improve genuine detail.
- Study 115's protected prompt and note still say section 82, while its accurate visible label points to Study 83. Study 44's protected title still differs from its cloud-pattern description. These were not included in the six-reference approval.
- No chapter rebalancing, original prompt rewriting or note removal occurred.
- No required export check was blocked. Physical print proofing and interactive testing in every PDF viewer are not claimed.
- No package or font was installed or downloaded.

## GitHub handoff

The changes are committed to the existing feature branch and PR #2 for review. No direct change to main, force-push or merge is part of this task. See `EDITORIAL_REVIEW.md` for findings and `EDITORIAL_SUGGESTIONS.md` for the remaining priorities.
