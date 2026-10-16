"""Black-and-white editorial edition inspired by the supplied portfolio reference.

Reuse the approved source, chapter mapping and original reference pixels. All
previous editions remain separate. No Canva asset or template file is copied.
"""
import argparse,html,json
from pathlib import Path
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.pdfbase import pdfmetrics
from build_issue_02 import Magazine,ROOT,GLOSSARY

BLACK=HexColor('#090909'); WHITE=HexColor('#f5f5f1'); GRAY=HexColor('#b9b9b6'); LINE=HexColor('#343434')

class NoirMagazine(Magazine):
    def __init__(self,output,layout_output):
        super().__init__(output,layout_output,edition='noir-editorial')
        self.c.setTitle('The Portrait Edit - Issue 02 - The Prompt Issue (Noir Editorial Edition)')
        self.variants={}

    def label(self,s,x,y,size=9,color=WHITE,font='Sans',checked=True):
        return super().label(s,x,y,size,color,font,checked)

    def para(self,s,x,top,w,size=10.5,leading=None,font='Sans',kind='body',color=WHITE,maxheight=None):
        p=Paragraph(html.escape(s).replace('\n','<br/>'),ParagraphStyle('noir',fontName=font,fontSize=size,leading=leading or size*1.4,textColor=color,splitLongWords=False))
        _,height=p.wrap(w,10000)
        if maxheight is not None:assert height<=maxheight,(self.c.getPageNumber(),kind,height,maxheight)
        p.style.textColor=color;p.drawOn(self.c,x,top-height)
        self.box(kind,x,top-height,w,height)
        self.boxes[-1].update(text=s,font=font,font_size=size)
        return height

    def rule(self,y,x=36,width=540):
        self.c.setStrokeColor(LINE);self.c.setLineWidth(.5);self.c.line(x,y,x+width,y)

    def base(self,section):
        c=self.c;c.setFillColor(BLACK);c.rect(0,0,612,792,fill=1,stroke=0)
        self.label('THE PORTRAIT EDIT',36,765,7.5)
        c.setFont('Sans',7.5);c.setFillColor(GRAY);c.drawRightString(576,765,'ISSUE 02 / THE PROMPT ISSUE')
        self.rule(751)
        self.label(section.upper(),36,27,7.5,color=GRAY)
        c.drawRightString(576,27,f'{c.getPageNumber():03d}')

    def cover(self):
        self.base('174 studies / 170 unique references')
        self.label('THE PORTRAIT EDIT',36,705,30)
        self.label('THE PROMPT ISSUE',36,678,11)
        self.label('02 / OCTOBER 2026',451,680,9,color=GRAY)
        self.rule(658)
        self.image_fit('24573.jpg',36,207,340,430)
        self.image_fit('5089.jpg',398,435,178,202)
        self.image_fit('24393.jpg',398,207,178,202)
        self.label('STUDY 026 / 24573.jpg',36,192,9,color=GRAY)
        self.label('016 / 5089.jpg',398,420,9,color=GRAY)
        self.label('051 / 24393.jpg',398,192,9,color=GRAY)
        self.rule(169)
        self.label('FROM IMAGE TO IMAGINATION',36,136,18)
        self.para('A reference. A prompt. A new possibility.',36,115,330,10.5,15)
        self.label('174 studies · 170 unique references',36,68,10,color=GRAY)
        self.label('Rights check / reference images',398,68,9,color=GRAY)
        self.c.showPage()

    def letter(self):
        self.base("Editor's letter")
        self.para('THE IMAGE IS\nTHE BEGINNING.',36,714,540,24,28,maxheight=56)
        self.para('A working magazine for looking closely - and making something new.',36,633,318,12,17,maxheight=51)
        self.para('Nine chapters bring this collection of 174 studies into focus. Each page places the complete original prompt beside its linked reference, with the original working notes below. The glossary introduces recurring photographic and clothing terms.',36,558,318,10.5,15)
        self.para('The prompts were written for DALL-E-style image tools. “Image Prompt” is used throughout as a neutral label. To explore a study, paste its prompt into your preferred image tool and use the reference attachment when supported. The added “Try this” line draws only from that study\'s existing notes.',36,435,318,10.5,15)
        self.para('Study numbers, titles, prompts and working notes are preserved. Six reference links and Source filenames were corrected with publisher approval. Repeats Study identifies shared or closely related references. Rights check asks the publisher to verify likeness and publication permissions; it does not establish anyone\'s identity.',36,282,540,10,14)
        self.image_fit('5089.jpg',383,388,193,230)
        self.label('STUDY 016 / 5089.jpg',383,371,9,color=GRAY)
        self.para('Rights check',383,347,193,9,13,color=GRAY)
        self.rule(183)
        self.label('CHAPTER DIRECTORY',36,160,9)
        for i,ch in enumerate(self.chapters):
            col,row=divmod(i,3);x=36+col*180;y=136-row*20
            self.label(ch['title'],x,y,9)
            target=self.openers[ch['id']];number=f'{target:03d}'
            self.label(number,x+164-pdfmetrics.stringWidth(number,'Sans',9),y,9,color=GRAY)
            rect=[x,y-4,x+168,y+12]
            self.c.linkAbsolute('','chapter-'+ch['id'],rect,thickness=0)
            self.directory.append(dict(chapter=ch['id'],title=ch['title'],page=2,target=target,rect=rect))
        self.label('174 STUDIES / 170 UNIQUE REFERENCES / 9 CHAPTERS',36,62,9,color=GRAY)
        self.c.showPage()

    def glossary(self):
        for half in range(2):
            self.base('Glossary')
            self.label('A LANGUAGE FOR LOOKING',36,708,23)
            self.label(f'GLOSSARY / {half+1} OF 2',36,676,9,color=GRAY)
            self.rule(657)
            for i,(term,definition) in enumerate(GLOSSARY[half*12:(half+1)*12]):
                col,row=divmod(i,6);x=36+col*280;top=630-row*93
                self.para(term,x,top,250,13,17,kind='glossary term',maxheight=18)
                self.para(definition,x,top-25,250,10.5,14.5,kind='glossary definition',maxheight=60,color=GRAY)
            self.c.showPage()

    def chapter_contents(self):
        for idx,ch in enumerate(self.chapters,1):
            self.base('Contents / '+ch['title'])
            self.label(f'CONTENTS / {idx:02d}',36,718,9,color=GRAY)
            self.para(ch['title'].upper(),36,690,540,24,29,maxheight=58)
            self.para(ch['description'],36,614,500,10.5,15,maxheight=30,color=GRAY)
            self.label(f"OPENER {self.openers[ch['id']]:03d} / {len(ch['studies'])} STUDIES",36,557,9,color=GRAY)
            self.rule(541)
            columns=2 if len(ch['studies'])>18 else 1;rows=(len(ch['studies'])+columns-1)//columns
            for i,n in enumerate(ch['studies']):
                col,row=divmod(i,rows);x=36+col*280;top=517-row*25.5
                width=260 if columns==2 else 540; titlew=width-61
                self.label(f'{n:03d}',x,top-10,10,color=GRAY)
                self.para(self.entries[n]['title'],x+29,top,titlew,10,12,kind='contents title',maxheight=24)
                page=str(self.study_pages[n]);self.label(page,x+width-pdfmetrics.stringWidth(page,'Sans',10),top-10,10)
                rect=(x,top-24,x+width,top+1);self.c.linkAbsolute('',f'study-{n}',rect,thickness=0)
                self.contents.append(dict(study=n,page=self.c.getPageNumber(),target=self.study_pages[n],rect=rect,number_rect=[x-1,top-16,x+25,top+2]))
            self.c.showPage()

    def opener(self,idx,ch):
        assert self.c.getPageNumber()==self.openers[ch['id']]
        self.base(ch['title']);self.c.bookmarkPage('chapter-'+ch['id']);self.c.addOutlineEntry(ch['title'],'chapter-'+ch['id'],level=0)
        self.label(f'CHAPTER {idx:02d} / {len(ch["studies"])} STUDIES',36,716,9,color=GRAY)
        self.para(ch['title'].upper(),36,682,540,26,31,maxheight=62)
        self.para(ch['description'],36,599,540,10.5,15,maxheight=30,color=GRAY)
        selected=[ch['studies'][i] for i in [0,len(ch['studies'])//2,-1]]
        for i,n in enumerate(selected):
            x=36+i*184
            self.image_fit(self.entries[n]['reference'],x,287,172,273)
            self.label(f'{n:03d} / {self.entries[n]["reference"]}',x,270,9,color=GRAY)
        self.rule(246)
        self.para(self.copy['chapter_openers'][ch['id']],36,218,390,11,16,kind='chapter editorial line',maxheight=64)
        self.label('REFERENCE / IMAGE PROMPT / WORKING NOTES',36,108,9,color=GRAY)
        self.label('Rights check / reference images',36,82,9,color=GRAY)
        self.c.showPage()

    def study(self,n,ch):
        e=self.entries[n];assert self.c.getPageNumber()==self.study_pages[n]
        self.base(ch['title']);self.c.bookmarkPage(f'study-{n}');self.c.addOutlineEntry(f'{n:03d} / {e["title"]}',f'study-{n}',level=1)
        self.label(f'STUDY {n:03d}',36,724,9,color=GRAY)
        size=22
        while self.measure(e['title'],540,size,size*1.18,'Sans')[1]>54:size-=.5
        self.para(e['title'],36,697,540,size,size*1.18,kind='study title',maxheight=54)
        flags=['Rights check'];flags.extend(f'Repeats Study {other}.' for other in self.audit['repeats'].get(str(n),[]))
        if n in self.pending_pairings:flags.append('Review pairing')
        self.label(' / '.join(flags),36,632,9,color=GRAY)
        # Alternate intact image/prompt positions; no crops or decorative image edits.
        image_x,prompt_x=(36,318) if n%2 else (318,36)
        self.variants[str(n)]='image-left' if n%2 else 'image-right'
        self.image_fit(e['reference'],image_x,270,258,342)
        self.label('Source: '+e['reference'],image_x,252,9,color=GRAY)
        self.label('IMAGE PROMPT',prompt_x,620,9)
        self.para(e['prompt'],prompt_x,598,258,10.5,14.5,kind='prompt',maxheight=530)
        sh=self.para(e['style'],image_x,231,258,10,13,kind='style',maxheight=39,color=GRAY)
        y=231-sh-17;self.label('WORKING NOTES',image_x,y,9)
        nh=self.para(e['notes'],image_x,y-13,258,10,14,kind='working notes',maxheight=98,color=GRAY)
        self.para('Try this: '+self.try_line(e),image_x,y-13-nh-12,258,10,14,kind='try this',maxheight=56)
        self.c.showPage()

    def build(self):
        super().build()
        m=json.loads(self.layout_output.read_text())
        m.update(edition='noir-editorial',prompt_font_size=10.5,notes_font_size=10,contents_font_size=10,glossary_font_size=10.5,study_title_max_pt=22,study_layouts=self.variants,palette={'background':'#090909','text':'#f5f5f1','secondary':'#b9b9b6'},image_occurrences=len(self.image_boxes))
        self.layout_output.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,default=ROOT/'revised/The_Portrait_Edit_Issue_02_Noir_Editorial.pdf')
    p.add_argument('--layout-output',type=Path,default=ROOT/'revised/noir-layout-checks.json')
    a=p.parse_args();NoirMagazine(a.output,a.layout_output).build()
