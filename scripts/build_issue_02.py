"""Build Issue 02 from the original Markdown and its reference attachments."""
from pathlib import Path
import re, json, html, hashlib, math
from io import BytesIO
from PIL import Image, ImageOps
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'DALL-E.prompts/dalle-prompts.md'
OUT = ROOT / 'output/pdf'
OUT.mkdir(parents=True, exist_ok=True)
PDF = OUT / 'The Portrait Edit - Issue 02 - The Prompt Issue.pdf'
for name, file in [('Serif','/usr/share/fonts/noto/NotoSerif-Regular.ttf'),('Sans','/usr/share/fonts/Adwaita/AdwaitaSans-Regular.ttf'),('Bold','/usr/share/fonts/liberation/LiberationSans-Bold.ttf')]:
    pdfmetrics.registerFont(TTFont(name, file))
BG, INK, MUTED, RED, RULE = map(HexColor, ['#f3f0e9','#201f1c','#716b63','#962e32','#ccc5ba'])
W,H=612,792
entries=[]
text=SOURCE.read_text()
for match in re.finditer(r'^## [^\n]*?(\d+)\. ([^\n]+)\n(.*?)(?=^## |\Z)',text,re.M|re.S):
    num,title,body=match.groups()
    ref=re.search(r'!\[\[attachments/([^\\|\]]+)',body,re.I)
    prompt=re.search(r'> \[!example\]- Prompt\n((?:>[^\n]*\n?)+)',body)
    notes=re.search(r'> \[!tip\] Notes\n((?:>[^\n]*\n?)+)',body)
    style=re.search(r'\*\*Style:\*\* ([^|\n]+)',body)
    tags=re.search(r'\*\*Tags:\*\* (.*?)<br>',body)
    assert ref and prompt and notes and style, (num,title)
    clean=lambda s: re.sub(r'^> ?','',s,flags=re.M).strip()
    entries.append(dict(number=int(num),title=title.strip(),reference=ref.group(1),prompt=clean(prompt.group(1)),notes=clean(notes.group(1)),style=style.group(1).strip(),tags=tags.group(1).strip() if tags else ''))
assert [e['number'] for e in entries]==list(range(1,175))
for e in entries:
    e['image']=ROOT/'DALL-E.prompts/Attachments'/e['reference']
    assert e['image'].is_file(), e['image']

c=canvas.Canvas(str(PDF),pagesize=(W,H),pageCompression=1)
c.setTitle('The Portrait Edit - Issue 02 - The Prompt Issue')
c.setAuthor('The Portrait Edit')
c.setSubject('174 reference images with their original ChatGPT image prompts')
metrics=[]

def label(s,x,y,size=7,color=INK,font='Bold'):
    c.setFillColor(color);c.setFont(font,size);c.drawString(x,y,s)

def para(s,x,top,width,size=10,leading=None,font='Sans',color=INK):
    # Preserve source wording while displaying Markdown emphasis as typography.
    s=html.escape(s).replace('\n','<br/>')
    s=re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',s)
    p=Paragraph(s,ParagraphStyle('p',fontName=font,fontSize=size,leading=leading or size*1.45,textColor=color))
    _,height=p.wrap(width,10000)
    p.drawOn(c,x,top-height)
    return height

def base(section):
    c.setFillColor(BG);c.rect(0,0,W,H,fill=1,stroke=0)
    label('THE PORTRAIT EDIT',36,765)
    c.setFont('Sans',7);c.drawRightString(576,765,'ISSUE 02 / OCTOBER 2026')
    c.setStrokeColor(RULE);c.setLineWidth(.5);c.line(36,751,576,751)
    label(section.upper(),36,27,6,font='Sans')
    c.setFont('Sans',7);c.drawRightString(576,27,f'{c.getPageNumber():03d}')

def image_fit(path,x,y,w,h):
    with Image.open(path) as im:
        im=ImageOps.exif_transpose(im).convert('RGB')
        iw,ih=im.size; scale=min(w/iw,h/ih); dw,dh=iw*scale,ih*scale
        # Full reference is visible, including garment and framing details.
        im.thumbnail((1800,2200),Image.Resampling.LANCZOS)
        buf=BytesIO();im.save(buf,format='JPEG',quality=90,optimize=True)
        c.drawImage(ImageReader(buf),x+(w-dw)/2,y+(h-dh)/2,dw,dh)
    return dw,dh

# Cover echoes the ivory, serif and inset-image design of the updated Issue 01.
c.setFillColor(BG);c.rect(0,0,W,H,fill=1,stroke=0)
label('THE',36,748,15,font='Serif')
label('PORTRAIT EDIT',36,704,41,font='Serif')
label('THE PROMPT ISSUE',36,680,8)
c.setFont('Sans',7);c.drawRightString(576,680,'02 / OCTOBER 2026')
image_fit(ROOT/'DALL-E.prompts/Attachments/4564.jpg',74,137,464,520)
label('FROM IMAGE TO IMAGINATION',36,100,23,font='Serif')
label('A reference. A prompt. A new possibility.',36,76,9,font='Sans')
label('174 STUDIES / THE COMPLETE COLLECTION',36,44,7)
c.showPage()

base('Editor\'s letter')
para('The image is\nthe beginning.',36,704,500,38,48,'Serif')
para('A working magazine for looking closely - and making something new.',36,562,465,16,24,'Serif')
para('This second issue brings the complete DALL-E prompt collection onto the page. Each study pairs its reference image with the original prompt and working notes, so that light, texture, framing and mood can be read together.',36,470,450,11,18)
para('The full image remains visible. The prompt stays beside it. This draft preserves the Markdown image links, including repeated references. Some source links do not match their prompt descriptions; these pairings still need editorial review. Every page records its linked filename for easy lookup.',36,367,450,11,18)
para('To use a study in ChatGPT, open an image-generation conversation and paste the prompt. Add its reference attachment when you want visual guidance, then describe any changes you want to make. The images shown here are source references; this issue does not present newly generated results.',36,264,450,10.5,17)
label('174',36,117,32,font='Serif');label('PROMPT STUDIES',36,96,7)
label('170',220,117,32,font='Serif');label('UNIQUE REFERENCES',220,96,7)
label('02',433,117,32,font='Serif');label('THE PROMPT ISSUE',433,96,7)
c.showPage()

# Four contents pages: every entry has a clickable page target.
front=6
for start in range(0,len(entries),44):
    base('Contents')
    label('The collection',36,707,31,font='Serif')
    label(f'STUDIES {start+1:03d}-{min(start+44,len(entries)):03d}',36,680,7,color=RED)
    for offset,e in enumerate(entries[start:start+44]):
        col,row=divmod(offset,22);x=36+col*278;top=649-row*25
        label(f'{e["number"]:03d}',x,top,7,color=RED)
        title=e['title'];font_size=7.2
        while pdfmetrics.stringWidth(title,'Sans',font_size)>207: font_size-=.1
        label(title,x+25,top,font_size,font='Sans')
        c.setFont('Sans',7);c.drawRightString(x+258,top,str(e['number']+front))
        c.linkAbsolute('',f'study-{e["number"]}',(x,top-5,x+260,top+12),thickness=0)
    c.showPage()

for e in entries:
    base('Reference / Prompt / Working notes')
    c.bookmarkPage(f'study-{e["number"]}')
    c.addOutlineEntry(f'{e["number"]:03d} / {e["title"]}',f'study-{e["number"]}',level=0)
    label(f'STUDY {e["number"]:03d}',36,720,8,color=RED)
    title_size=26
    while True:
        p=Paragraph(html.escape(e['title']),ParagraphStyle('title',fontName='Serif',fontSize=title_size,leading=title_size*1.18,textColor=INK))
        _,th=p.wrap(540,200)
        if th<=67:break
        title_size-=.5
    p.drawOn(c,36,697-th)
    image_fit(e['image'],36,198,302,408)
    label('REFERENCE / '+e['reference'].upper(),36,179,6.5,color=RED)
    sh=para(e['style'],36,159,302,12,17,'Serif')
    label('WORKING NOTES',36,159-sh-26,6.7)
    notes=e['notes'].replace('- ','',1).replace('\n- ','\n')
    nh=para(notes,36,159-sh-41,302,8.2,12,color=MUTED)
    assert 159-sh-41-nh>45,(e['number'],'notes overflow')
    label('CHATGPT / IMAGE PROMPT',360,612,7,color=RED)
    size=9.5
    while True:
        p=Paragraph(html.escape(e['prompt']).replace('\n','<br/>'),ParagraphStyle('prompt',fontName='Sans',fontSize=size,leading=size*1.48,textColor=INK))
        _,ph=p.wrap(216,2000)
        if ph<=505:break
        size-=.2
    assert size>=8.5,(e['number'],'prompt too small')
    p.drawOn(c,360,592-ph)
    metrics.append({'study':e['number'],'page':c.getPageNumber(),'prompt_font_size':size,'prompt_bottom':592-ph,'notes_bottom':159-sh-41-nh})
    c.showPage()
c.save()
manifest={'title':'The Portrait Edit - Issue 02 - The Prompt Issue','source':'DALL-E.prompts/dalle-prompts.md','source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'design_reference':'Downloads/The Portrait Edit.pdf (Issue 01, 103 pages)','studies':len(entries),'unique_references':len(set(e['reference'] for e in entries)),'pages':len(entries)+front,'entries':[{k:v for k,v in e.items() if k!='image'}|{'page':e['number']+front} for e in entries],'layout':metrics}
(OUT/'issue-02-manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
print(f'Built {PDF} ({PDF.stat().st_size:,} bytes), {len(entries)+front} pages')
