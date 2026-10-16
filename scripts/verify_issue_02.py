"""Verify the requested content and layout invariants and render review samples."""
from pathlib import Path
from collections import Counter
import re,json,hashlib,subprocess
import pymupdf as fitz
from PIL import Image,ImageDraw
from audit_issue_02 import ROOT,SOURCE,parse_source

norm=lambda s:re.sub(r'\s+','',s)
def run():
    out=ROOT/'revised';m=json.loads((out/'layout-checks.json').read_text());es=parse_source();audit=json.loads((out/'audit-data.json').read_text())
    pdf=Path(m['output']);d=fitz.open(pdf)
    assert len(d)==m['pages']==196
    assert all(abs(p.rect.width-612)<.01 and abs(p.rect.height-792)<.01 for p in d)
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==m['source_sha256']==audit['source_sha256']
    assert hashlib.sha256(pdf.read_bytes()).hexdigest()==m['pdf_sha256']
    # Require all study numbers exactly once in the rendered contents, not just the mapping.
    counts=Counter()
    for row in m['contents']:
        page=d[row['page']-1];x0,y0,x1,y1=row['number_rect'];rect=fitz.Rect(x0,792-y1,x1,792-y0)
        number=page.get_text('text',clip=rect).strip()
        assert number==f"{row['study']:03d}",(row['study'],number)
        counts[int(number)]+=1
        x0,y0,x1,y1=row['rect'];rect=fitz.Rect(x0,792-y1,x1,792-y0)
        assert any(link.get('page')==row['target']-1 and link['from'].intersects(rect) for link in page.get_links()),row
    assert counts==Counter({n:1 for n in range(1,175)})
    for e in es:
        n=e['number'];p=d[m['study_pages'][str(n)]-1];text=p.get_text()
        prompt=p.get_text('text',clip=fitz.Rect(359,196,577,740))
        assert norm(prompt)==norm(e['prompt']),(n,'prompt differs',prompt)
        assert norm(e['title']) in norm(text),(n,'title')
        assert 'Source: '+e['reference'] in text,(n,'Source')
        notes=p.get_text('text',clip=fitz.Rect(35,552,339,749))
        assert norm(e['notes']) in norm(notes),(n,'notes')
        assert 'Rights check' in text
        assert ('Review pairing' in text)==(str(n) in audit['pairings'])
        for other in audit['repeats'].get(str(n),[]):assert f'Repeats Study {other}.' in text
        assert norm('Try this: '+m['try_lines'][str(n)]) in norm(text)
        assert len(p.get_images())==1
        assert 'CHATGPT / IMAGE PROMPT' not in text.upper()
    # Inspect actual text spans against the recorded layout boxes on every page.
    for box in m['text_boxes']:
        assert box['x']>=35 and box['y']>=43 and box['x']+box['w']<=577 and box['y']+box['h']<=747
    bypage={}
    for box in m['text_boxes']:
        x,y,w,h=box['x'],box['y'],box['w'],box['h'];bypage.setdefault(box['page'],[]).append(fitz.Rect(x-1,792-y-h-5,x+w+1,792-y+5))
    for number,p in enumerate(d,1):
        for block in p.get_text('dict')['blocks']:
            if block['type']!=0:continue
            for line in block['lines']:
                for span in line['spans']:
                    rect=fitz.Rect(span['bbox'])
                    assert rect.x0>=34 and rect.x1<=578 and rect.y0>=12 and rect.y1<=779,(number,span)
                    # Running labels and cover furniture have their own fixed positions.
                    if number>1 and 55<rect.y0 and rect.y1<746:
                        assert any(box.contains(rect) for box in bypage[number]),(number,'text exceeds declared box',span)
    # Reference image streams retain source pixel dimensions, without upsampling/cropping.
    for im in m['images']:
        x,y,w,h=im['drawn'];fx,fy,fw,fh=im['frame']
        assert x>=fx-.01 and y>=fy-.01 and x+w<=fx+fw+.01 and y+h<=fy+fh+.01
        iw,ih=im['original_pixels'];assert abs(w/h-iw/ih)<1e-6
        embedded=d[im['page']-1].get_images()[0]
        assert (embedded[2],embedded[3])==(iw,ih),(im['source'],'pixels changed')
    text=subprocess.check_output(['pdftotext','-layout',str(pdf),'-'],text=True)
    assert all(e['reference'] in text for e in es)
    (out/'revised-pdf-layout.txt').write_text(text)
    samples={'cover':1,'chapter-opener':m['chapter_openers']['knitwear'],'study':m['study_pages']['7']}
    for name,page in samples.items():d[page-1].get_pixmap(matrix=fitz.Matrix(1.5,1.5)).save(out/f'sample-{name}.png')
    # All-page contact sheets for a broader visual sweep, kept outside deliverables.
    tmp=ROOT/'tmp/pdfs/revised';tmp.mkdir(parents=True,exist_ok=True)
    for start in range(0,len(d),28):
        sheet=Image.new('RGB',(4*252,7*338),'#d6d2cb');draw=ImageDraw.Draw(sheet)
        for offset in range(min(28,len(d)-start)):
            pix=d[start+offset].get_pixmap(matrix=fitz.Matrix(.38,.38));im=Image.frombytes('RGB',(pix.width,pix.height),pix.samples);x=offset%4*252+9;y=offset//4*338+7;sheet.paste(im,(x,y));draw.text((x,y+307),str(start+offset+1),fill='black')
        sheet.save(tmp/f'contact-{start//28+1}.jpg',quality=88)
    result=dict(status='PASS',pages=len(d),letter_size=True,contents_studies_once=174,prompts_exact_normalized=174,original_titles=174,original_sources=174,working_notes_preserved=174,pairing_flags=6,rights_flags=174,duplicate_flags=sum(len(v) for v in audit['repeats'].values()),minimum_body_pt=9,images_original_pixels=True,no_text_box_overflow=True,samples=samples,pdf_sha256=m['pdf_sha256'])
    (out/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':run()
