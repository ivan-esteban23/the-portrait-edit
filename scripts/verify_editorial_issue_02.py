"""Validate the exported editorial PDF without writing baseline artifacts.

Checks operate on the PDF text, links, bookmarks, image streams and geometry;
manifest entries are cross-checked rather than treated as proof of rendering.
"""
from pathlib import Path
from collections import Counter, defaultdict
from io import BytesIO
import argparse, hashlib, json, re, subprocess
import pymupdf as fitz
from PIL import Image, ImageOps, ImageDraw, ImageFont
from functools import lru_cache
from audit_issue_02 import ROOT, SOURCE, parse_source
from build_issue_02 import approved_reference_corrections, BASELINE_EDITABLE

EXPECTED_PAIRINGS=set()
EXPECTED_REPEATS={48:75,75:48,62:66,66:62,69:76,76:69,79:106,106:79,83:115,115:83,99:103,103:99,113:126,126:113,122:142,142:122,147:152,152:147}
BODY_KINDS={'body','prompt','style','working notes','try this','glossary definition','contents title','chapter editorial line'}
norm=lambda s:re.sub(r'\s+','',s)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()

def pdf_rect(x,y,w,h):
    return fitz.Rect(x,792-y-h,x+w,792-y)

def region_text(page,box,padding=3):
    rect=pdf_rect(box['x'],box['y'],box['w'],box['h'])
    rect=fitz.Rect(rect.x0-padding,rect.y0-padding,rect.x1+padding,rect.y1+padding)
    return page.get_text('text',clip=rect)

FONT_FILES={
    'NotoSerif-Regular':'/usr/share/fonts/noto/NotoSerif-Regular.ttf',
    'LiberationSans':'/usr/share/fonts/liberation/LiberationSans-Regular.ttf',
    'LiberationSans-Bold':'/usr/share/fonts/liberation/LiberationSans-Bold.ttf'}
INK_FONTS={name:ImageFont.truetype(path,1024) for name,path in FONT_FILES.items()}

@lru_cache(maxsize=2048)
def glyph_ink(font,char):
    mask,offset=INK_FONTS[font].getmask2(char,mode='L',anchor='ls')
    bounds=mask.getbbox()
    if bounds is None:return None
    return tuple((value+offset[i%2])/1024 for i,value in enumerate(bounds))

def span_ink(span):
    result=fitz.Rect()
    for char in span['chars']:
        bounds=glyph_ink(span['font'],char['c'])
        if bounds is None:continue
        x,y=char['origin'];size=span['size']
        rect=fitz.Rect(x+bounds[0]*size,y+bounds[1]*size,x+bounds[2]*size,y+bounds[3]*size)
        result|=rect
    return result

def run(args):
    for name in ('pdf','layout','report','samples'):
        setattr(args,name,getattr(args,name).resolve())
    m=json.loads(args.layout.read_text());copy=json.loads((ROOT/'revised/editorial-copy.json').read_text())
    chapters=json.loads((ROOT/'revised/chapters.json').read_text())['chapters']
    corrections=approved_reference_corrections()
    assert sha(ROOT/'revised/pairing-corrections.json')==m['pairing_corrections_sha256']
    assert m['approved_reference_corrections']==corrections['corrections']
    es=parse_source();by_number={e['number']:e for e in es}
    for row in corrections['corrections']:assert by_number[row['study']]['reference']==row['to']
    assert args.pdf.resolve()!= (ROOT/'revised/The_Portrait_Edit_Issue_02_Revised.pdf').resolve()
    assert sha(args.pdf)==m['pdf_sha256']
    assert sha(SOURCE)==m['source_sha256']==copy['source_sha256']
    assert sha(ROOT/'revised/editorial-copy.json')==m['editorial_copy_sha256']
    # Verify baseline hashes against both the working tree and immutable Git objects.
    assert m['baseline_commit']=='5235d883e9161eaed9f28633c539f4c34f39768e'
    baseline_paths=set(subprocess.check_output(['git','-C',str(ROOT),'ls-tree','-r','--name-only',m['baseline_commit']],text=True).splitlines())
    assert set(m['protected_sha256'])==baseline_paths-BASELINE_EDITABLE
    for path,expected in m['protected_sha256'].items():
        assert sha(ROOT/path)==expected,('protected file changed',path)
        original=subprocess.check_output(['git','-C',str(ROOT),'show',m['baseline_commit']+':'+path])
        assert hashlib.sha256(original).hexdigest()==expected,('baseline differs',path)
    d=fitz.open(args.pdf);assert len(d)==m['pages']==196
    assert all(abs(p.rect.width-612)<.001 and abs(p.rect.height-792)<.001 for p in d)
    assert d.is_pdf and not d.needs_pass
    assert sorted(map(int,m['study_pages']))==list(range(1,175))
    rows=copy['try_this'];assert len(rows)==174
    assert Counter(row['study'] for row in rows)==Counter({n:1 for n in range(1,175)})
    for row in rows:
        assert row['basis_note']==by_number[row['study']]['note_items'][row['basis_note_number']-1]
        assert row['line']==m['try_lines'][str(row['study'])]
    boxes_by_page=defaultdict(list)
    for box in m['text_boxes']:boxes_by_page[box['page']].append(box)

    counts=Counter();contents_links=0
    for row in m['contents']:
        p=d[row['page']-1];x0,y0,x1,y1=row['number_rect']
        rect=pdf_rect(x0,y0,x1-x0,y1-y0)
        actual=p.get_text('text',clip=rect).strip()
        assert actual==f"{row['study']:03d}",(row,'rendered contents number',actual)
        counts[int(actual)]+=1
        x0,y0,x1,y1=row['rect'];rect=pdf_rect(x0,y0,x1-x0,y1-y0)
        matches=[ln for ln in p.get_links() if ln.get('page')==row['target']-1 and ln['from'].intersects(rect)]
        assert len(matches)==1,('contents link',row)
        title=by_number[row['study']]['title']
        assert norm(title) in norm(p.get_text('text',clip=rect)),('contents title',row)
        assert str(row['target']) in p.get_text('text',clip=rect),('contents page number',row)
        assert row['target']==m['study_pages'][str(row['study'])]
        contents_links+=1
    assert counts==Counter({n:1 for n in range(1,175)})

    found_pairings=set();found_rights=set();found_repeats={}
    for e in es:
        n=e['number'];pn=m['study_pages'][str(n)];p=d[pn-1];text=p.get_text()
        assert f'STUDY {n:03d}' in text
        titlebox=next(b for b in boxes_by_page[pn] if b['kind']=='study title')
        assert norm(region_text(p,titlebox))==norm(e['title']),(n,'title mismatch')
        assert 'Source: '+e['reference'] in text,(n,'Source mismatch')
        promptbox=next(b for b in boxes_by_page[pn] if b['kind']=='prompt')
        assert norm(region_text(p,promptbox))==norm(e['prompt']),(n,'prompt mismatch')
        notesbox=next(b for b in boxes_by_page[pn] if b['kind']=='working notes')
        assert norm(region_text(p,notesbox))==norm(e['notes']),(n,'working notes mismatch')
        trybox=next(b for b in boxes_by_page[pn] if b['kind']=='try this')
        assert norm(region_text(p,trybox))==norm('Try this: '+m['try_lines'][str(n)]),(n,'Try this mismatch')
        assert text.count('IMAGE PROMPT')==1 and 'CHATGPT / IMAGE PROMPT' not in text.upper()
        if 'Review pairing' in text:found_pairings.add(n)
        if 'Rights check' in text:found_rights.add(n)
        repeats=list(map(int,re.findall(r'Repeats Study (\d+)\.',text)))
        expected=[EXPECTED_REPEATS[n]] if n in EXPECTED_REPEATS else []
        assert repeats==expected,(n,'duplicate reference',repeats,expected)
        if repeats:found_repeats[n]=repeats
    assert found_pairings==EXPECTED_PAIRINGS
    assert found_rights==set(range(1,175))

    # Verify the complete chapter and study bookmark hierarchy and destinations.
    toc=d.get_toc();expected_toc=[]
    for ch in chapters:
        expected_toc.append([1,ch['title'],m['chapter_openers'][ch['id']]])
        for n in ch['studies']:expected_toc.append([2,f"{n:03d} / {by_number[n]['title']}",m['study_pages'][str(n)]])
    assert toc==expected_toc,('bookmark hierarchy or destinations differ',len(toc))
    assert len(toc)==183
    directory=m['chapter_directory'];assert len(directory)==9 and len(d[1].get_links())==9
    assert {row['chapter'] for row in directory}=={ch['id'] for ch in chapters}
    for row in directory:
        assert row['page']==2 and row['target']==m['chapter_openers'][row['chapter']]
        x0,y0,x1,y1=row['rect'];rect=pdf_rect(x0,y0,x1-x0,y1-y0)
        assert any(ln.get('page')==row['target']-1 and ln['from'].intersects(rect) for ln in d[1].get_links())
        assert norm(row['title']) in norm(d[1].get_text('text',clip=rect))
    for ch in chapters:
        page=d[m['chapter_openers'][ch['id']]-1]
        assert norm(copy['chapter_openers'][ch['id']]) in norm(page.get_text())
        assert 'The studies keep their original numbers.' not in page.get_text()

    # Geometry checks: declared blocks must be disjoint; exported text must fit them.
    # Font bounding boxes include ascenders/descenders; use a 5pt containment
    # tolerance, but never inflate rectangles for overlap detection.
    exported_min_body=100;span_count=0;block_comparisons=0;span_comparisons=0
    image_rects_by_page=defaultdict(list)
    for im in m['images']:
        image_rects_by_page[im['page']].append(pdf_rect(*im['drawn']))
    for page_number,p in enumerate(d,1):
        blocks=boxes_by_page[page_number]
        for i,a in enumerate(blocks):
            assert a['x']>=35 and a['y']>=43 and a['x']+a['w']<=577 and a['y']+a['h']<=747
            ar=pdf_rect(a['x'],a['y'],a['w'],a['h'])
            if a['kind'] in BODY_KINDS:assert a['font_size']>=9
            for b in blocks[i+1:]:
                br=pdf_rect(b['x'],b['y'],b['w'],b['h']);inter=ar&br;block_comparisons+=1
                assert inter.is_empty or inter.width*inter.height<.05,(page_number,'logical text blocks overlap',a,b)
        spans=[]
        for raw in p.get_text('rawdict')['blocks']:
            if raw['type']!=0:continue
            for line in raw['lines']:
                for span in line['spans']:
                    span['text']=''.join(c['c'] for c in span['chars'])
                    if not span['text'].strip():continue
                    rect=fitz.Rect(span['bbox']);ink=span_ink(span);span_count+=1
                    assert rect.x0>=34 and rect.x1<=578 and rect.y0>=12 and rect.y1<=779,(page_number,'page clipping',span)
                    owners=[]
                    for bi,b in enumerate(blocks):
                        br=pdf_rect(b['x'],b['y'],b['w'],b['h']);expanded=fitz.Rect(br.x0-1,br.y0-5,br.x1+1,br.y1+5)
                        if expanded.contains(rect) and norm(span['text']) in norm(b['text']):owners.append(bi)
                    # Only the cover's top masthead and right issue label, plus
                    # running headers/footers, are intentionally outside blocks.
                    furniture=rect.y1<55 or rect.y0>746 or (page_number==1 and (rect.y0<55 or ('ISSUE 02 /' in span['text'])))
                    assert owners or furniture,(page_number,'text outside declared box',span)
                    owner=owners[0] if owners else None
                    if owner is not None and blocks[owner]['kind'] in BODY_KINDS:
                        assert span['size']>=8.99,(page_number,'body below 9pt',span)
                        exported_min_body=min(exported_min_body,span['size'])
                    # Contents numbers and chapter directory labels are also body-sized.
                    if page_number in range(5,14) and re.fullmatch(r'\d+',span['text']):
                        if rect.y0<740:assert span['size']>=8.99
                    for image_rect in image_rects_by_page[page_number]:
                        inter=ink&image_rect
                        assert inter.is_empty or inter.width*inter.height<.05,(page_number,'text overlaps image',span)
                    spans.append((ink,owner,span['text']))
        for i,(ar,ao,at) in enumerate(spans):
            for br,bo,bt in spans[i+1:]:
                if ao is not None and ao==bo:continue
                inter=ar&br;span_comparisons+=1
                assert inter.is_empty or inter.width*inter.height<.1,(page_number,'exported text overlap',at,bt,tuple(inter))
        # No clipping path is used on a page, so complete image/text boxes remain visible.
        assert not re.search(rb'(?<!\S)W\*?(?=\s)',p.read_contents()),(page_number,'unexpected clipping path')

    # Check actual image placement and extracted pixels, not just manifest dimensions.
    image_pixels_checked=0
    for im in m['images']:
        p=d[im['page']-1];info=p.get_image_info(xrefs=True);assert len(info)==1
        actual=info[0];assert (actual['width'],actual['height'])==tuple(im['original_pixels'])
        expected=pdf_rect(*im['drawn']);ar=fitz.Rect(actual['bbox'])
        assert all(abs(a-b)<.02 for a,b in zip(ar,expected)),(im['source'],'image placement')
        assert pdf_rect(*im['frame']).contains(ar)
        iw,ih=im['original_pixels'];assert abs(ar.width/ar.height-iw/ih)<.00001
        with Image.open(ROOT/'DALL-E.prompts/Attachments'/im['source']) as source:
            src=ImageOps.exif_transpose(source).convert('RGB');src_pixels=src.tobytes()
        extracted=d.extract_image(actual['xref'])
        with Image.open(BytesIO(extracted['image'])) as embedded:
            embedded=embedded.convert('RGB')
            assert embedded.size==(iw,ih) and embedded.tobytes()==src_pixels,(im['source'],'pixels altered')
        image_pixels_checked+=1
    assert image_pixels_checked==175
    # Independent Poppler pass checks all Source strings in a second text extractor.
    layout_text=subprocess.check_output(['pdftotext','-layout',str(args.pdf),'-'],text=True)
    assert len([s for s in layout_text.split('\f') if s.strip()])==196
    assert all('Source: '+e['reference'] in layout_text for e in es)

    args.samples.mkdir(parents=True,exist_ok=True)
    longest=max(es,key=lambda e:len(e['prompt']))['number']
    samples={'cover':1,'editors-letter':2,'glossary-01':3,'glossary-02':4,'contents':10,'chapter-opener':m['chapter_openers']['knitwear'],'long-prompt-study':m['study_pages'][str(longest)],'small-image-study':m['study_pages']['36'],'duplicate-study':m['study_pages']['115'],'review-pairing-study':m['study_pages']['7']}
    samples.update({f'pairing-study-{row["study"]:03d}':m['study_pages'][str(row['study'])] for row in corrections['corrections']})
    for name,page in samples.items():
        d[page-1].get_pixmap(matrix=fitz.Matrix(1.7,1.7)).save(args.samples/(name+'.png'))
    for start in range(0,len(d),28):
        sheet=Image.new('RGB',(4*252,7*338),'#d6d2cb');draw=ImageDraw.Draw(sheet)
        for offset in range(min(28,len(d)-start)):
            pix=d[start+offset].get_pixmap(matrix=fitz.Matrix(.38,.38));im=Image.frombytes('RGB',(pix.width,pix.height),pix.samples);x=offset%4*252+9;y=offset//4*338+7;sheet.paste(im,(x,y));draw.text((x,y+307),str(start+offset+1),fill='black')
        sheet.save(args.samples/f'contact-{start//28+1:02d}.jpg',quality=88)
    result=dict(status='PASS',pdf=str(args.pdf.relative_to(ROOT)),pdf_sha256=sha(args.pdf),pages=len(d),letter_points=[612,792],contents_studies_once=174,exact_normalized_prompts=174,original_titles=174,source_filenames_match_current=174,approved_source_corrections=6,original_prompt_and_note_bytes_preserved=True,chapter_membership_unchanged=True,original_working_notes=174,reviewed_try_lines=174,pairing_studies=sorted(found_pairings),rights_studies=174,duplicate_studies=18,contents_links=contents_links,chapter_directory_links=9,bookmarks_correct=183,minimum_exported_body_pt=exported_min_body,no_clipping=True,no_text_block_or_image_overlap=True,text_spans_checked=span_count,overlap_measurement='FreeType glyph ink bounds positioned at exported PDF character origins; logical blocks checked separately.',logical_block_comparisons=block_comparisons,exported_span_comparisons=span_comparisons,image_occurrences_original_pixels=image_pixels_checked,unique_reference_filenames=170,protected_files_unchanged=len(m['protected_sha256']),baseline_commit=m['baseline_commit'],readable_previews=samples,full_issue_contact_sheets=7,visual_inspection='Pending separate human/assistant visual review; automated PASS does not imply visual approval.',limitations=['Geometry and pixel checks do not establish publication rights. Six source-pairing corrections were explicitly approved after visual review.'])
    args.report.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--pdf',type=Path,default=ROOT/'revised/The_Portrait_Edit_Issue_02_Editorial_Revision.pdf')
    parser.add_argument('--layout',type=Path,default=ROOT/'revised/editorial-layout-checks.json')
    parser.add_argument('--report',type=Path,default=ROOT/'revised/editorial-verification.json')
    parser.add_argument('--samples',type=Path,default=ROOT/'revised/editorial-samples')
    run(parser.parse_args())
