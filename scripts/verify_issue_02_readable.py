"""Run full editorial verification plus enforce larger exported type sizes."""
import argparse,json
from pathlib import Path
import pymupdf
from audit_issue_02 import ROOT
from verify_editorial_issue_02 import run,pdf_rect

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pdf',type=Path,default=ROOT/'revised/The_Portrait_Edit_Issue_02_Larger_Type.pdf')
    parser.add_argument('--layout',type=Path,default=ROOT/'revised/larger-type-layout-checks.json')
    parser.add_argument('--report',type=Path,default=ROOT/'revised/larger-type-verification.json')
    parser.add_argument('--samples',type=Path,default=ROOT/'revised/larger-type-samples')
    args=parser.parse_args()
    layout=json.loads(args.layout.read_text());doc=pymupdf.open(args.pdf)
    targets={'prompt':12,'working notes':11.5,'try this':11.5,'glossary definition':11.5,'contents title':11}
    checked={kind:0 for kind in targets}
    for box in layout['text_boxes']:
        if box['kind'] not in targets:continue
        expected=targets[box['kind']]
        assert box['font_size']==expected
        rect=pdf_rect(box['x'],box['y'],box['w'],box['h'])
        page=doc[box['page']-1]
        spans=[s for b in page.get_text('dict',clip=rect+(-1,-5,1,5))['blocks'] if b['type']==0 for line in b['lines'] for s in line['spans'] if s['text'].strip()]
        assert spans and all(abs(s['size']-expected)<.01 for s in spans),(box['page'],box['kind'],spans)
        checked[box['kind']]+=1
    assert checked=={'prompt':174,'working notes':174,'try this':174,'glossary definition':24,'contents title':174}
    run(args)
    report=json.loads(args.report.read_text());report['larger_type_pt']=targets;report['larger_type_blocks_checked']=checked
    args.report.write_text(json.dumps(report,indent=2)+'\n')
    print('PASS: exported larger type sizes verified for all 720 text blocks.')
