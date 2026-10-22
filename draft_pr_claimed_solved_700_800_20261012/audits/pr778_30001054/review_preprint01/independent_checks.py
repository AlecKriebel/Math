from pathlib import Path
from itertools import permutations,product
from collections import Counter
from io import BytesIO
import zipfile,hashlib,json,datetime,os,stat
B=Path(__file__).resolve().parent
P=B.parent/'preprint'; S=B/'extracted'
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def require(x,m):
 if not x:raise RuntimeError(m)
# Different formulation: relative orientations identify the one inverted pair.
v=[p for p in permutations(range(4)) if p.index(0)<p.index(1) and p.index(2)<p.index(3)]
def rev(p):return tuple(x^1 for x in p[::-1])
def ev(a,b):
 changed=[(x,y) for x in range(4) for y in range(x+1,4) if (a.index(x)<a.index(y))!=(b.index(x)<b.index(y))]
 if len(changed)!=1:return None
 x,y=changed[0]
 if x//2==y//2:return None
 require(abs(a.index(x)-a.index(y))==1,'Kendall1 must be adjacent')
 return tuple(sorted((x,y),key=b.index))
counts=Counter();examples=[]
for half in product(v,repeat=4):
 w=half+tuple(rev(x) for x in half)
 events=[ev(w[k],w[(k+1)%8]) for k in range(8)]
 if None in events:continue
 if any(all(w[k]==w[(k+d)%8] for k in range(8)) for d in [1,2,4]):continue
 mixed=sum(x%2!=y%2 for x,y in events)
 sep=any(p in [(0,1,2,3),(2,3,0,1)] for p in w)
 once=len(set(events))==8
 counts[(mixed,sep,once)]+=1
A=(0,2,1,3);BB=(0,2,3,1);C=(2,0,3,1);word=(A,BB,A,BB,C,BB,C,BB)
require(all(word[k+4]==rev(word[k]) for k in range(4)),'half')
require(all(ev(word[k],word[(k+1)%8]) for k in range(8)),'edges')
require(counts==Counter({(0,False,False):32,(4,True,True):16}),'counts')
# Every ZIP member inspected for path/mode/compression/signature, every byte bound.
z=zipfile.ZipFile(P/'source-and-verification.zip'); names=z.namelist()
require(len(names)==123 and names==sorted(set(names)),'source names')
manifest=json.loads(z.read('MANIFEST.json'));rows=manifest['files']
require(set(names)=={r['path'] for r in rows}|{'MANIFEST.json'},'closed names')
for row in rows:require(ident(z.read(row['path']))=={k:row[k] for k in ('bytes','sha256')},'member bytes')
for info in z.infolist():
 require(info.date_time==(2026,10,16,0,0,0),'fixed date')
 require((info.external_attr>>16)==0o100644,'mode')
 require(info.compress_type==zipfile.ZIP_DEFLATED,'DEFLATE')
 require(not info.filename.startswith('/') and '..' not in info.filename.split('/') and '\\' not in info.filename,'path')
 require(not z.read(info.filename).startswith(b'%PDF'),'no PDF body')
 require((S/info.filename).read_bytes()==z.read(info.filename),'extraction')
kit=zipfile.ZipFile(P/'zenodo-upload-kit.zip')
require(set(kit.namelist())=={'README.md','paper.pdf','source-and-verification.zip','zenodo-deposit.json','zenodo-metadata.json'},'kit members')
require(kit.read('paper.pdf')==(P/'output/pdf/paper.pdf').read_bytes(),'kit PDF')
require(kit.read('source-and-verification.zip')==(P/'source-and-verification.zip').read_bytes(),'kit source')
meta=json.loads((P/'zenodo-metadata.json').read_bytes());deposit=json.loads((P/'zenodo-deposit.json').read_bytes())
require(meta['metadata']==deposit['metadata']==json.loads(kit.read('zenodo-deposit.json'))['metadata']==json.loads(kit.read('zenodo-metadata.json'))['metadata']==json.loads(z.read('zenodo-metadata.json'))['metadata'],'metadata')
require(z.read('paper.tex')==(P/'paper.tex').read_bytes(),'tex')
require(json.loads(z.read('PREPRINT_BINDINGS.json'))['paper.pdf']==ident((P/'output/pdf/paper.pdf').read_bytes()),'pdf binding')
allfiles=[]
for n in names:
 raw=z.read(n)
 typ='zip' if raw.startswith(b'PK\x03\x04') else 'json' if n.endswith('.json') else 'code' if n.endswith('.py') else 'authored_text'
 if typ=='json':json.loads(raw)
 if typ=='code':compile(raw,n,'exec')
 allfiles.append({'path':n,'kind':typ,**ident(raw)})
 if typ=='zip':
  nested=zipfile.ZipFile(BytesIO(raw))
  part='audit' if 'REBUILT' in n else 'review'
  base='audit/original/unsolved_math_prioritization/attempts/30001054/'+part+'/'
  require(len(nested.namelist())==(14 if part=='audit' else 7),'nested count')
  for sub in nested.namelist(): require(nested.read(sub)==z.read(base+sub),'nested extracted byte match')
expected=json.loads((B.parent/'PREPRINT_REVIEW_INPUTS_01.json').read_text())['six']
for name,row in expected.items(): require(ident((P/name).read_bytes())==row,'external six pin '+name)
(B/'MEMBER_INSPECTION.json').write_text(json.dumps(allfiles,indent=2)+'\n')
(B/'INDEPENDENT_RESULTS.json').write_text(json.dumps({'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','enumerated':1296,'primitive':48,'groups':[{'mixed_events':k[0],'separated_term':k[1],'switch_once':k[2],'count':n} for k,n in counts.items()],'source_members':123,'all_members_inspected':True,'nested_member_counts':[14,7],'no_PDF_signatures':True,'exact_six':expected,'metadata_equal':True},indent=2)+'\n')
print('independent math and complete ZIP/metadata checks PASS')
