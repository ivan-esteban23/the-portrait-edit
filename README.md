# The Portrait Edit

## Issue 02 - The Prompt Issue (editorial draft)

[Open the magazine PDF](output/pdf/The%20Portrait%20Edit%20-%20Issue%2002%20-%20The%20Prompt%20Issue.pdf)

180 letter-size pages: a cover, an opening letter, four linked contents pages, and 174 individual studies. Each study displays its full reference image alongside the complete original ChatGPT image prompt, style description, working notes, and source filename. PDF bookmarks provide direct access to every study.

The layout follows the updated Issue 01 PDF supplied locally as `Downloads/The Portrait Edit.pdf`: warm ivory stock, serif headlines, fine rules, restrained red accents, and inset photography. The large original PDF remains outside Git; this repository contains the new issue and its reproducible source.

### Editorial review pending

This draft preserves the image links in the original Markdown. Visual review found source pairings that do not agree with their prompt descriptions, including studies 7-9: `4991.jpg` shows the mustard dress, `4992.jpg` the cream knit set, and `4993.jpg` the powder blue set, while their Markdown assignments use a different order. Other entries also require pairing review. The draft should not be treated as a fully verified semantic image-to-prompt match.

No original prompt text or attachment has been changed. Repeated image references remain as separate studies. The magazine contains source references, rather than newly generated images.

### Sources and build

- [Original Markdown](DALL-E.prompts/dalle-prompts.md)
- [Reference attachments](DALL-E.prompts/Attachments)
- [Build script](scripts/build_issue_02.py)
- [Study/page manifest](output/pdf/issue-02-manifest.json)

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python scripts/build_issue_02.py
```

The script currently uses the installed Linux Noto Serif, Adwaita Sans, and Liberation Sans Bold fonts at the paths listed near its beginning. Adjust those paths on another machine.

Validation: all 174 source prompts were checked against extracted PDF text; all linked filenames, embedded-image counts, text boundaries, and 174 contents links were checked. All 180 pages were rendered and reviewed in contact sheets, with selected pages inspected at larger size. This structural validation does not resolve the source pairing issues above.
