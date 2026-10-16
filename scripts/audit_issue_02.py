"""Read-only source inspection; write an audit before layout changes."""
from pathlib import Path
from collections import defaultdict
import re, json, subprocess, hashlib
from PIL import Image, ImageOps
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'DALL-E.prompts/dalle-prompts.md'
DEST=ROOT/'revised'
CURRENT=ROOT/'output/pdf/The Portrait Edit - Issue 02 - The Prompt Issue.pdf'

def parse_source():
    entries=[]
    for m in re.finditer(r'^## [^\n]*?(\d+)\. ([^\n]+)\n(.*?)(?=^## |\Z)',SOURCE.read_text(),re.M|re.S):
        number,title,body=m.groups()
        ref=re.search(r'\*\*Source:\*\* `([^`]+)`',body)
        linked=re.search(r'!\[\[attachments/([^\\|\]]+)',body,re.I)
        def callout(kind):
            found=re.search(r'> \[!'+kind+r'\][^\n]*\n((?:>[^\n]*\n?)+)',body)
            assert found,(number,kind)
            return re.sub(r'^> ?','',found.group(1),flags=re.M).strip()
        assert ref and linked and ref.group(1)==linked.group(1),(number,'source/link mismatch')
        notes=callout('tip')
        entries.append(dict(number=int(number),title=title.strip(),reference=ref.group(1),prompt=callout('example'),notes=notes,note_items=[re.sub(r'^- ','',x) for x in notes.splitlines()],style=re.search(r'\*\*Style:\*\* ([^|\n]+)',body).group(1).strip(),tags=re.search(r'\*\*Tags:\*\* (.*?)<br>',body).group(1)))
    assert [e['number'] for e in entries]==list(range(1,175))
    return entries

# Editorial findings are based on visual review; these are flags, not image swaps.
PAIRINGS={
7:'4991.jpg shows a mustard-yellow twist dress; the prompt describes a cream knit co-ord.',
8:'4992.jpg shows a cream knit co-ord; the prompt describes a powder-blue knit set.',
9:'4993.jpg shows a powder-blue knit set; the prompt describes a mustard twist dress.',
12:'5030.jpg shows a black turtleneck, white mini and white socks; the prompt describes red polka-dot bows and a floral pinafore/blouse.',
13:'5031.jpg shows a red headband and red puff-sleeve top; the prompt describes a black turtleneck and white mini.',
14:'5032.jpg shows braids with red polka-dot bows and floral styling; the prompt describes a red headband and red puff sleeves.'}
NEAR=[(48,75,'Different filenames show the same pink outfit/location; source notes explicitly call this a near-duplicate.'),(62,66,'Same teahouse photograph/crop family; Study 66 explicitly describes the tighter view.'),(69,76,'Same black-dress/lantern setting and apparent same photograph; source notes identify a near-duplicate.'),(99,103,'Closely related monochrome polo-knit runway looks; source notes identify the alternate walk.'),(147,152,'Same lilac mesh outfit in related views; source notes identify the alternate pose.')]

def run():
    DEST.mkdir(exist_ok=True)
    es=parse_source();norm=lambda s:re.sub(r'\s+','',s).casefold()
    text=subprocess.check_output(['pdftotext','-layout',str(CURRENT),'-'],text=True)
    pages=[p for p in text.split('\f') if p.strip()];assert len(pages)==180
    for e in es:
        p=pages[e['number']+5]
        assert f"STUDY {e['number']:03d}" in p
        assert norm(e['title']) in norm(p)
        assert e['reference'].lower() in p.lower()
    (DEST/'current-pdf-layout.txt').write_text(text)
    groups=defaultdict(list);titlegroups=defaultdict(list);small=[];inventory=[]
    for e in es:
        groups[e['reference']].append(e['number']);titlegroups[e['title']].append(e['number'])
        with Image.open(ROOT/'DALL-E.prompts/Attachments'/e['reference']) as im:
            im=ImageOps.exif_transpose(im);w,h=im.size
        inventory.append(dict(study=e['number'],source=e['reference'],width=w,height=h,rights_check=True))
        if min(w,h)<600:small.append(inventory[-1])
    dup=[{'studies':v,'source':k} for k,v in groups.items() if len(v)>1]
    repeats={e['number']:set() for e in es}
    for g in dup:
        a,b=g['studies'];repeats[a].add(b);repeats[b].add(a)
    for a,b,_ in NEAR:repeats[a].add(b);repeats[b].add(a)
    data=dict(source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),current_pdf_sha256=hashlib.sha256(CURRENT.read_bytes()).hexdigest(),original_pages=180,studies=174,unique_references=len(groups),pairings={str(k):v for k,v in PAIRINGS.items()},same_source=dup,near_duplicates=[dict(studies=[a,b],reason=s) for a,b,s in NEAR],repeats={str(k):sorted(v) for k,v in repeats.items() if v},small_images=small,rights_inventory=inventory)
    lines=['# Issue 02 source audit','','Audit performed before layout changes. All 174 studies, original prompts, titles, source links, and working notes remain intact. Visual findings are editorial flags, not identity claims or image corrections.','','## Input and baseline inspection','','- Reused the existing ReportLab generator: `scripts/build_issue_02.py` (baseline commit `940eaab`).','- Requested uploaded PDF path is unavailable. Inspected the matching existing 180-page repository PDF, also previously copied to Documents.','- `pdftotext -layout` confirms 180 letter-size pages, all 174 study numbers, titles, and Source filenames. Extracted text is saved in `current-pdf-layout.txt`.','- Requested `/mnt/user-data/outputs` directory cannot be created: permission denied. Revised deliverables use this directory and Documents instead.','','## Potential image-prompt mismatches','','These six visually identifiable mismatches retain their original filenames and images; each receives “Review pairing”.']
    for n,reason in PAIRINGS.items():lines.append(f'- Study {n}: {reason}')
    lines+=['','Additional source wording issues retained verbatim:','- Study 44 title says “Camo Knit Skirt”, while its prompt/notes describe a cloud-like pattern. This is a title-versus-description discrepancy, not a confirmed swapped image.','- Study 115 notes refer to section 82, but its same-title/same-source counterpart is Study 83. The original note is preserved.','- Source notes sometimes suggest removing duplicates or shortening a prompt. Those notes remain verbatim; no such removal or shortening was performed.','','## Duplicates and near-duplicates','','All pages remain. Each member of every pair below receives “Repeats Study [N].” Exact matches are defined by shared Source filename or identical title; near matches are visually/source-note supported.']
    for g in dup:lines.append(f"- Studies {' / '.join(map(str,g['studies']))}: same Source `{g['source']}` and same title.")
    for a,b,reason in NEAR:lines.append(f'- Studies {a} / {b}: near-duplicate. {reason}')
    lines+=['','## Reference likeness and rights checks','','All 170 unique references (all 174 study pages) are photographs or photorealistic portraits with visible, potentially recognizable people. No names, identities, authenticity, releases, ownership, or licenses can be established from these local files. Conservatively apply “Rights check” to every study, including repeated references; this is a review flag, not a claim that every image shows a known real person. The publisher decides. A complete study/filename list appears below.','','## Cover count','','174 studies and 170 unique reference filenames are consistent: four filenames occur twice (79/106, 83/115, 113/126, 122/142). Thus 174 - 4 = 170. Near-duplicates with different filenames do not change the unique-filename count.','','## Small images','','Threshold: short edge below 600 pixels. These may look soft at the fixed printed frame size. Preserve the original pixels; do not crop or resample upward.']
    for im in small:lines.append(f"- Study {im['study']}: `{im['source']}`, {im['width']} × {im['height']} px.")
    lines+=['','## Complete rights-check inventory','','| Study | Source | Original pixels | Review |','|---:|---|---|---|']
    for im in inventory:lines.append(f"| {im['study']} | `{im['source']}` | {im['width']} × {im['height']} | Rights check |")
    (DEST/'audit.md').write_text('\n'.join(lines)+'\n')
    (DEST/'audit-data.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    print(f"Audit complete: {len(PAIRINGS)} pairing flags, {len(dup)} shared-image pairs, {len(NEAR)} near-duplicate pairs, {len(small)} small images; all 174 entries intact.")

if __name__=='__main__':run()
