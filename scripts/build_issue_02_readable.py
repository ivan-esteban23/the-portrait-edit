"""Larger-type edition; reuse the approved editorial source and page structure."""
import argparse, json
from pathlib import Path
from reportlab.pdfbase import pdfmetrics
from build_issue_02 import Magazine, ROOT, RED, MUTED, RULE

class ReadableMagazine(Magazine):
    def __init__(self, output, layout_output):
        super().__init__(output, layout_output, edition='larger-type')
        self.c.setTitle('The Portrait Edit - Issue 02 - The Prompt Issue (Larger Type Edition)')

    def glossary(self):
        from build_issue_02 import GLOSSARY
        for half in range(2):
            self.base('Glossary')
            self.label('A language for looking',36,708,30,font='Serif')
            self.label(f'GLOSSARY / {half+1} OF 2',36,676,10,color=RED)
            for i,(term,definition) in enumerate(GLOSSARY[half*12:(half+1)*12]):
                col,row=divmod(i,6); x=36+col*280; top=640-row*94
                self.para(term,x,top,250,14,18,'Serif',kind='glossary term',maxheight=20)
                self.para(definition,x,top-27,250,11.5,15,kind='glossary definition',maxheight=60)
            self.c.showPage()

    def chapter_contents(self):
        for idx,ch in enumerate(self.chapters,1):
            self.base('Contents / '+ch['title'])
            self.label(f'CONTENTS / CHAPTER {idx:02d}',36,719,10,color=RED)
            self.para(ch['title'],36,698,540,30,36,'Serif',maxheight=38)
            self.para(ch['description'],36,647,495,11.5,16,maxheight=32)
            self.label(f"OPENER {self.openers[ch['id']]:03d} / {len(ch['studies'])} STUDIES",36,600,10,color=MUTED)
            columns=2 if len(ch['studies'])>18 else 1; rows=(len(ch['studies'])+columns-1)//columns
            for i,n in enumerate(ch['studies']):
                col,row=divmod(i,rows);x=36+col*280;top=580-row*29.5
                width=260 if columns==2 else 540; titlew=width-61
                self.label(f'{n:03d}',x,top-11,11,color=RED)
                self.para(self.entries[n]['title'],x+29,top,titlew,11,14.5,kind='contents title',maxheight=29)
                page=str(self.study_pages[n])
                self.label(page,x+width-pdfmetrics.stringWidth(page,'Sans',11),top-11,11,font='Sans')
                rect=(x,top-29,x+width,top+2)
                self.c.linkAbsolute('',f'study-{n}',rect,thickness=0)
                self.contents.append(dict(study=n,page=self.c.getPageNumber(),target=self.study_pages[n],rect=rect,number_rect=[x-1,top-17,x+25,top+2]))
            self.c.showPage()

    def study(self,n,ch):
        e=self.entries[n]; assert self.c.getPageNumber()==self.study_pages[n]
        self.base(ch['title'])
        self.c.bookmarkPage(f'study-{n}'); self.c.addOutlineEntry(f'{n:03d} / {e["title"]}',f'study-{n}',level=1)
        self.label(f'STUDY {n:03d}',36,721,10,color=RED)
        size=26
        while self.measure(e['title'],540,size,size*1.18,'Serif')[1]>63:size-=.5
        self.para(e['title'],36,699,540,size,size*1.18,'Serif',kind='study title',maxheight=63)
        flags=['Rights check']
        if n in self.pending_pairings: flags.append('Review pairing')
        flags.extend(f'Repeats Study {other}.' for other in self.audit['repeats'].get(str(n),[]))
        self.label(' / '.join(flags),36,620,10,color=RED)
        self.c.setStrokeColor(RULE); self.c.setLineWidth(.5); self.c.rect(36,250,302,355,stroke=1,fill=0)
        self.image_fit(e['reference'],42,256,290,343)
        self.label('Source: '+e['reference'],36,234,10.5,font='Sans')
        sh=self.para(e['style'],36,216,302,11,14,'Serif',kind='style',maxheight=28)
        y=216-sh-16; self.label('WORKING NOTES',36,y,10)
        nh=self.para(e['notes'],36,y-14,302,11.5,16.1,kind='working notes',color=MUTED,maxheight=82)
        self.para('Try this: '+self.try_line(e),36,y-14-nh-12,302,11.5,16.1,kind='try this',maxheight=65)
        self.label('IMAGE PROMPT',360,612,10,color=RED)
        self.para(e['prompt'],360,594,216,12,16.8,kind='prompt',maxheight=530)
        self.c.showPage()

    def build(self):
        super().build()
        manifest=json.loads(self.layout_output.read_text())
        manifest.update(prompt_font_size=12,notes_font_size=11.5,glossary_font_size=11.5,contents_font_size=11,edition='larger-type')
        self.layout_output.write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=ROOT/'revised/The_Portrait_Edit_Issue_02_Larger_Type.pdf')
    parser.add_argument('--layout-output',type=Path,default=ROOT/'revised/larger-type-layout-checks.json')
    args=parser.parse_args()
    ReadableMagazine(args.output,args.layout_output).build()
