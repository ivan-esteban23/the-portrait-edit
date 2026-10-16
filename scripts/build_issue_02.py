"""Revised Issue 02: refactored from the existing 180-page ReportLab generator.

The original PDF is preserved. Sources are parsed from Markdown without rewriting.
"""
from pathlib import Path
from io import BytesIO
import argparse, re, json, html, hashlib
from PIL import Image, ImageOps
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from audit_issue_02 import ROOT, SOURCE, parse_source

W,H=612,792
BG,INK,MUTED,RED,RULE=map(HexColor,['#f3f0e9','#201f1c','#716b63','#962e32','#ccc5ba'])
GLOSSARY=[
('High-key','A predominantly light image with bright backgrounds and restrained shadows. It describes the overall tonal treatment, rather than simply an overexposed photograph.'),
('Shallow depth of field','A narrow zone of sharp focus that leaves foreground or background details soft, helping separate the subject from the scene.'),
('Rim light','Light from behind or beside a subject that traces a bright edge around hair, clothing or the silhouette.'),
('Film grain','The visible texture associated with photographic film. In a digital prompt it usually requests a similar textured appearance.'),
('Kodak Portra','A family of color-negative photographic films often used for portraits. In a prompt, the name suggests a film-inspired color and tonal treatment.'),
('Seamless backdrop','A continuous studio background without a visible join between the wall and floor, keeping attention on the subject.'),
('Muted palette','A color scheme with restrained saturation. Colors appear subdued rather than vivid or electric.'),
('Soft focus','A deliberately gentle rendering of detail and edges. It can suggest a dreamy image, beyond simply blurring the background.'),
('Diffused light','Light spread through a broad source or scattering material to soften the transition between light and shadow.'),
('Close-up','A tight framing that concentrates on a face or a small group of details, excluding much of the surrounding scene.'),
('Full-length','A framing that includes the entire person from head to toe, often used to show a complete outfit.'),
('Mid-stride','A pose captured during a step, suggesting walking motion rather than a static stance.'),
('Mock-neck','A short, upright collar that covers part of the neck, usually lower than a folded turtleneck.'),
('A-line','A silhouette that widens from a narrower upper section toward the hem, resembling the outline of the letter A.'),
('Ruched','Fabric gathered into repeated small folds to create texture, shape or a close fit.'),
('Ribbed knit','Knitted fabric with alternating raised and recessed vertical rows, creating a ridged texture and stretch.'),
('Cable knit','Knitwear in which groups of stitches cross to form raised, rope-like patterns.'),
('Satin','A fabric structure with a smooth, lustrous face that catches light. Satin can be made from different fibers.'),
('Velvet','Fabric with a dense, short pile that creates a soft surface and changes its appearance with the direction of light.'),
('Tweed','A textured woven fabric commonly associated with wool, mottled colors and structured tailoring.'),
('Halter','A neckline or top supported around the neck, typically leaving the shoulders and much of the upper back open.'),
('Jabot','A decorative arrangement of lace or ruffles worn at the front of the neck or upper chest.'),
('Faux fur','A manufactured material designed to resemble the texture and appearance of animal fur.'),
('Pleated','Fabric arranged into intentional folds, which can give a garment structure, volume or movement.')]

class Magazine:
    def __init__(self, output):
        for name,path in [('Serif','/usr/share/fonts/noto/NotoSerif-Regular.ttf'),('Sans','/usr/share/fonts/liberation/LiberationSans-Regular.ttf'),('Bold','/usr/share/fonts/liberation/LiberationSans-Bold.ttf')]:
            pdfmetrics.registerFont(TTFont(name,path))
        self.entries={e['number']:e for e in parse_source()}
        self.mapping=json.loads((ROOT/'revised/chapters.json').read_text())
        self.audit=json.loads((ROOT/'revised/audit-data.json').read_text())
        assert self.audit['source_sha256']==hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'Rerun the audit after source changes.'
        self.chapters=self.mapping['chapters'];ns=[n for ch in self.chapters for n in ch['studies']]
        assert sorted(ns)==list(range(1,175)) and len(ns)==len(set(ns))
        self.study_pages={};self.openers={};self.contents=[];self.boxes=[];self.image_boxes=[]
        page=5+len(self.chapters)
        for ch in self.chapters:
            self.openers[ch['id']]=page;page+=1
            for n in ch['studies']:self.study_pages[n]=page;page+=1
        self.expected_pages=page-1
        output.parent.mkdir(parents=True,exist_ok=True)
        self.output=output;self.c=canvas.Canvas(str(output),pagesize=(W,H),pageCompression=1)
        self.c.setTitle('The Portrait Edit - Issue 02 - The Prompt Issue (Revised)')
        self.c.setAuthor('The Portrait Edit');self.c.setSubject('174 unchanged image prompts, 170 source references, nine themed chapters')

    def box(self,kind,x,bottom,w,height):
        assert x>=35 and bottom>=43 and x+w<=577 and bottom+height<=747,(self.c.getPageNumber(),kind,(x,bottom,w,height))
        self.boxes.append(dict(page=self.c.getPageNumber(),kind=kind,x=x,y=bottom,w=w,h=height))

    def label(self,s,x,y,size=8,color=INK,font='Bold',checked=True):
        self.c.setFillColor(color);self.c.setFont(font,size);self.c.drawString(x,y,s)
        if checked and y>=45 and y+size+4<=747:self.box('label',x,y-2,pdfmetrics.stringWidth(s,font,size),size+4)

    def measure(self,s,w,size,leading=None,font='Sans'):
        # Escape source markup; only source newlines affect layout.
        p=Paragraph(html.escape(s).replace('\n','<br/>'),ParagraphStyle('p',fontName=font,fontSize=size,leading=leading or size*1.4,textColor=INK,splitLongWords=False))
        _,height=p.wrap(w,10000)
        return p,height

    def para(self,s,x,top,w,size=10,leading=None,font='Sans',kind='body',color=INK,maxheight=None):
        p,height=self.measure(s,w,size,leading,font)
        if maxheight is not None:assert height<=maxheight,(self.c.getPageNumber(),kind,height,maxheight)
        p.style.textColor=color;p.drawOn(self.c,x,top-height)
        self.box(kind,x,top-height,w,height)
        return height

    def base(self,section):
        c=self.c;c.setFillColor(BG);c.rect(0,0,W,H,fill=1,stroke=0)
        self.label('THE PORTRAIT EDIT',36,765,7)
        c.setFont('Sans',7);c.drawRightString(576,765,'ISSUE 02 / OCTOBER 2026')
        c.setStrokeColor(RULE);c.setLineWidth(.5);c.line(36,751,576,751)
        self.label(section.upper(),36,27,7,font='Sans')
        c.setFont('Sans',7);c.drawRightString(576,27,f'{c.getPageNumber():03d}')

    def image_fit(self,filename,x,y,w,h):
        path=ROOT/'DALL-E.prompts/Attachments'/filename
        with Image.open(path) as original:
            original.load();im=ImageOps.exif_transpose(original);iw,ih=im.size
            scale=min(w/iw,h/ih,1.0);dw,dh=iw*scale,ih*scale
            # Preserve source pixels and JPEG streams. No crop or upward resampling.
            if original.getexif().get(274,1)==1:
                reader=ImageReader(str(path))
            else:
                reader=ImageReader(im.copy())
            self.c.drawImage(reader,x+(w-dw)/2,y+(h-dh)/2,dw,dh)
        self.image_boxes.append(dict(page=self.c.getPageNumber(),source=filename,original_pixels=[iw,ih],frame=[x,y,w,h],drawn=[x+(w-dw)/2,y+(h-dh)/2,dw,dh],pixel_resampling='none'))

    def cover(self):
        c=self.c;c.setFillColor(BG);c.rect(0,0,W,H,fill=1,stroke=0)
        self.label('THE',36,748,15,font='Serif')
        self.label('PORTRAIT EDIT',36,704,41,font='Serif')
        self.label('The Prompt Issue',36,677,14,font='Serif')
        c.setFont('Sans',9);c.drawRightString(576,677,'ISSUE 02 / OCTOBER 2026')
        self.image_fit('4564.jpg',74,140,464,514)
        self.label('FROM IMAGE TO IMAGINATION',36,102,23,font='Serif')
        self.label('A reference. A prompt. A new possibility.',36,77,10,font='Sans')
        self.label('174 studies · 170 unique references',36,48,10,font='Sans')
        c.showPage()

    def letter(self):
        self.base("Editor's letter")
        self.para('The image is\nthe beginning.',36,710,500,38,48,'Serif')
        self.para('A working magazine for looking closely - and making something new.',36,568,465,16,24,'Serif')
        self.para('Nine chapters bring this collection of 174 studies into focus. Each page places the complete original prompt beside its linked reference, with the original working notes below. The glossary introduces recurring photographic and clothing terms.',36,476,450,11,17)
        self.para('The prompts were written for DALL-E-style image tools. “Image Prompt” is used throughout as a neutral label. To explore a study, paste its prompt into your preferred image tool and use the reference attachment when supported. The added “Try this” line draws only from that study\'s existing notes.',36,369,450,11,17)
        self.para('Every study number, title, source filename, prompt and working note is preserved. Review pairing marks six potentially mismatched source links. Repeats Study identifies shared or closely related references. Rights check asks the publisher to verify likeness and publication permissions; it does not establish anyone\'s identity.',36,245,450,10,15)
        self.label('174 STUDIES',36,83,10);self.label('170 UNIQUE REFERENCES',220,83,10);self.label('9 CHAPTERS',458,83,10)
        self.c.showPage()

    def glossary(self):
        for half in range(2):
            self.base('Glossary')
            self.label('A language for looking',36,708,30,font='Serif')
            self.label(f'GLOSSARY / {half+1} OF 2',36,676,8,color=RED)
            for i,(term,definition) in enumerate(GLOSSARY[half*12:(half+1)*12]):
                col,row=divmod(i,6);x=36+col*280;top=640-row*94
                self.para(term,x,top,250,14,18,'Serif',kind='glossary term',maxheight=20)
                self.para(definition,x,top-27,250,9.5,13,kind='glossary definition',maxheight=60)
            self.c.showPage()

    def chapter_contents(self):
        for idx,ch in enumerate(self.chapters,1):
            self.base('Contents / '+ch['title'])
            self.label(f'CONTENTS / CHAPTER {idx:02d}',36,719,8,color=RED)
            self.para(ch['title'],36,698,540,30,36,'Serif',maxheight=38)
            self.para(ch['description'],36,647,495,10,14,maxheight=28)
            self.label(f"OPENER {self.openers[ch['id']]:03d} / {len(ch['studies'])} STUDIES",36,600,8,color=MUTED)
            columns=2 if len(ch['studies'])>18 else 1;rows=(len(ch['studies'])+columns-1)//columns
            for i,n in enumerate(ch['studies']):
                col,row=divmod(i,rows);x=36+col*280;top=572-row*29
                width=260 if columns==2 else 540;titlew=width-61
                self.label(f'{n:03d}',x,top-9,9,color=RED)
                height=self.para(self.entries[n]['title'],x+29,top,titlew,9,12,kind='contents title',maxheight=24)
                self.label(str(self.study_pages[n]),x+width-pdfmetrics.stringWidth(str(self.study_pages[n]),'Sans',9),top-9,9,font='Sans')
                rect=(x,top-25,x+width,top+2)
                self.c.linkAbsolute('',f'study-{n}',rect,thickness=0)
                self.contents.append(dict(study=n,page=self.c.getPageNumber(),target=self.study_pages[n],rect=rect,number_rect=[x-1,top-15,x+25,top+2]))
            self.c.showPage()

    def opener(self,idx,ch):
        assert self.c.getPageNumber()==self.openers[ch['id']]
        self.base(ch['title'])
        self.c.bookmarkPage('chapter-'+ch['id']);self.c.addOutlineEntry(ch['title'],'chapter-'+ch['id'],level=0)
        self.label(f'CHAPTER {idx:02d}',36,712,9,color=RED)
        self.para(ch['title'],36,649,520,40,49,'Serif',maxheight=100)
        self.para(ch['description'],36,512,540,12,18,'Sans',maxheight=18)
        self.c.setStrokeColor(RED);self.c.setLineWidth(1);self.c.line(36,401,111,401)
        self.label(f"{len(ch['studies'])} STUDIES",36,374,9,color=RED)
        self.para('Reference / Image Prompt / Working notes',36,331,450,11,17)
        self.para('The studies keep their original numbers. Use the chapter contents or PDF bookmarks to move between them.',36,291,360,10,16)
        self.label(f"FIRST STUDY / {ch['studies'][0]:03d}",36,111,9,color=MUTED)
        self.c.showPage()

    def try_line(self,e):
        overrides={2:'Try a different season or city.',3:'Warm up the palette or change the pose.',4:'Emphasize the diagonal ponytail.',5:'Try a warmer setting.',6:'Shift the costume to a different era.'}
        if e['number'] in overrides:return overrides[e['number']]
        items=[s for s in e['note_items'] if not re.search(r'only one|near-duplicate|alternate angle|tighter crop of|prompt is long',s,re.I)]
        for s in reversed(items):
            if re.match(r"(Add|Use|Swap|Consider|Describe|Adjust|Remove)\b",s):return s
        s=items[-1]
        if s.startswith('Keep '):return 'Emphasize '+s[5:]
        # Rephrase only the existing visual details, without adding any new ones.
        s=re.split(r' (?:are|is|create|define|set) ',s,maxsplit=1)[0]
        if s.startswith('The '):s='the '+s[4:]
        return 'Emphasize '+s.rstrip('.')+'.'

    def study(self,n,ch):
        e=self.entries[n];assert self.c.getPageNumber()==self.study_pages[n]
        self.base(ch['title'])
        self.c.bookmarkPage(f'study-{n}');self.c.addOutlineEntry(f'{n:03d} / {e["title"]}',f'study-{n}',level=1)
        self.label(f'STUDY {n:03d}',36,721,9,color=RED)
        size=26
        while self.measure(e['title'],540,size,size*1.18,'Serif')[1]>63:size-=.5
        self.para(e['title'],36,699,540,size,size*1.18,'Serif',kind='study title',maxheight=63)
        # Flags sit on a separate line above the fixed image frame.
        flags=['Rights check']
        if str(n) in self.audit['pairings']:flags.append('Review pairing')
        flags.extend(f'Repeats Study {other}.' for other in self.audit['repeats'].get(str(n),[]))
        self.label(' / '.join(flags),36,620,8,color=RED,checked=True)
        self.c.setStrokeColor(RULE);self.c.setLineWidth(.5);self.c.rect(36,250,302,355,stroke=1,fill=0)
        self.image_fit(e['reference'],42,256,290,343)
        self.label('Source: '+e['reference'],36,234,9,font='Sans',checked=True)
        sh=self.para(e['style'],36,216,302,11,14,'Serif',kind='style',maxheight=28)
        y=216-sh-16;self.label('WORKING NOTES',36,y,8)
        nh=self.para(e['notes'],36,y-12,302,9,12.5,kind='working notes',color=MUTED,maxheight=76)
        th=self.para('Try this: '+self.try_line(e),36,y-12-nh-12,302,9,12.5,kind='try this',maxheight=51)
        self.label('IMAGE PROMPT',360,612,8,color=RED)
        self.para(e['prompt'],360,594,216,9.5,13.7,kind='prompt',maxheight=530)
        self.c.showPage()

    def build(self):
        self.cover();self.letter();self.glossary();self.chapter_contents()
        for i,ch in enumerate(self.chapters,1):
            self.opener(i,ch)
            for n in ch['studies']:self.study(n,ch)
        assert self.c.getPageNumber()-1==self.expected_pages
        self.c.save()
        manifest=dict(pages=self.expected_pages,study_pages={str(k):v for k,v in self.study_pages.items()},chapter_openers=self.openers,contents=self.contents,text_boxes=self.boxes,images=self.image_boxes,source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),pdf_sha256=hashlib.sha256(self.output.read_bytes()).hexdigest(),prompt_font_size=9.5,notes_font_size=9,image_resampling='none',output=str(self.output),try_lines={str(n):self.try_line(e) for n,e in self.entries.items()})
        (ROOT/'revised/layout-checks.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
        print(f'Built {self.expected_pages} pages: {self.output} ({self.output.stat().st_size:,} bytes)')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=ROOT/'revised/The_Portrait_Edit_Issue_02_Revised.pdf')
    Magazine(parser.parse_args().output).build()
