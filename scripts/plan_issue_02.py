"""Write the explicit chapter assignments; no source files are changed."""
from audit_issue_02 import ROOT, parse_source
import json
specs=[
('portraits','Portraits & Light','Faces, gestures and the way light shapes a mood.',[2,3,4,15,16,26,27,31,34,35,36,42,43,51,52,57,60,65,71,73,74,82]),
('winter','Winter','Snow, shearling and layers made for the cold.',[20,21,23,24,25,28,61,67,70,72,88,94,119,161,165]),
('folk','Folk & Landscape','Embroidery, adornment and portraits rooted in place.',[17,22,29,32]),
('fantasy','Fantasy & Period','Imagined worlds, historical details and romantic atmosphere.',[1,5,6,19,30,33,59,118,120,121,127,128,134]),
('runway','Runway','Tailoring, movement and silhouettes in stride.',[37,40,46,54,56,58,83,90,98,99,102,103,108,115,125,139,145]),
('knitwear','Knitwear & Layers','Tactile knits, playful proportions and considered layers.',[7,8,10,11,38,41,44,47,63,77,79,80,87,89,92,93,95,96,97,104,106,107,109,110,117,131,138,144,146,153,156,160,164,168,170,171]),
('studio','Studio','Controlled backdrops and graphic clothing studies.',[9,12,13,14,64,81,85,129,137,141,143,147,149,150,151,152,154,157,158,159,169,173]),
('night','Night & Lifestyle','Interior stories, after-dark light and everyday scenes.',[50,53,55,62,66,69,76,86,113,123,124,126,132,133,136,155,166,167,174])]
assigned=[n for *_,ns in specs for n in ns];assert len(assigned)==len(set(assigned))
remaining=sorted(set(range(1,175))-set(assigned))
specs.append(('street','Street & City','Candid settings, urban textures and personal style.',remaining))
es={e['number']:e for e in parse_source()}
chapters=[dict(id=k,title=t,description=d,studies=ns) for k,t,d,ns in specs]
data={'version':1,'assignment_basis':'Editorial theme of the unchanged prompt; original source filenames and study numbers remain unchanged. Grouping does not certify a reference pairing.','chapters':chapters,'assignments':[dict(study=n,title=es[n]['title'],source=es[n]['reference'],chapter=k) for k,t,d,ns in specs for n in ns]}
assert len(data['assignments'])==174
(ROOT/'revised/chapters.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
print([(c['title'],len(c['studies'])) for c in chapters])
