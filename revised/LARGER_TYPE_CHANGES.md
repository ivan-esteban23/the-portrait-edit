# Issue 02 - Larger type edition

The earlier PDF used 9.5 pt prompts, 9 pt notes and contents, and 9.5 pt glossary definitions. These were hard to read, especially when a whole Letter page was fitted to a phone screen.

## Implemented

- Prompts: 12 pt / 16.8 pt leading.
- Original working notes and reviewed Try this lines: 11.5 pt / 16.1 pt leading.
- Glossary definitions: 11.5 pt / 15 pt leading.
- Contents titles, study numbers and page numbers: 11 pt; row spacing adjusted to fit all entries.
- Study flags and section labels: 10 pt. Source labels: 10.5 pt.
- Serif titles, reference frame sizes, original images and running furniture retained.
- New subclass builder reuses the approved editorial generator rather than replacing it. The original editorial PDF, its reports and previews remain untouched.

## Preserved and verified

196 Letter pages; all 174 study numbers, titles, prompts, working notes, reviewed Try this lines and current Source filenames. Six approved pairings, all 174 rights flags, 18 duplicate cross-references, chapter membership and all 183 bookmarks remain correct. Checks passed for 174 contents links and nine chapter-directory links. All 175 image occurrences retain their decoded original pixels, dimensions and framing. No clipping, text collisions or text/image overlap was detected. All 190 protected baseline files remain unchanged.

A dedicated verifier checks the actual exported larger font sizes in 720 blocks, in addition to the existing full editorial verifier. Its report is `larger-type-verification.json`. Seven readable previews and contact sheets 1 and 4 were visually inspected; no visible clipping or overlap was found. The full automated geometry pass covers all pages. No print proof is claimed.

PDF SHA-256: `cf47ffbb6a1277f6d90ef9d77a70cab5fcec22e1c93296373006dd1fa6760620`.

## Website companion

The separate Issue 02 website uses the larger-type page images and a 20 px flowing reading view (18/20/24 px choices). Study text is copied exactly from the verified layout; reference image streams are extracted without alteration. Original page mode remains available. On narrow screens the large-text view is the default. The earlier PDF download remains in release `edition-1`; this edition has its own `larger-type-1` release.

Browser visual QA remains unavailable because no browser is connected. Navigation and reading-mode logic are checked with desktop/mobile DOM fixtures; all 174 structured studies are checked against the PDF layout. Publication rights and source inconsistencies noted in the earlier editorial review remain unchanged. No packages or fonts were installed.
