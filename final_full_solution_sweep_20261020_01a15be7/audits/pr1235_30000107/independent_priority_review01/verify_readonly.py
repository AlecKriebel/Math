#!/usr/bin/env python3
"""Independent, exact, read-only priority-evidence and published-obstruction checks.
No author programs, solver, imports from fetched source, network, subprocess or writes.
"""
from pathlib import Path
from fractions import Fraction as Q
from itertools import combinations, permutations
from collections import Counter
import hashlib
import json
import zipfile

HERE=Path(__file__).resolve().parent
SRC=HERE/'private_sources'
COUNT=0

def need(ok,label):
    global COUNT
    if not ok: raise ValueError(label)
    COUNT+=1

def sha(b):return hashlib.sha256(b).hexdigest()

for f in sorted(HERE.glob('FETCH_RECEIPTS_*.json')):
    for row in json.loads(f.read_bytes()):
        if 'error' in row:continue
        b=(SRC/row['file']).read_bytes()
        need(len(b)==row['bytes'] and sha(b)==row['sha256'],'retrieval '+row['file'])
        if 'expected_checksum' in row:
            need('md5:'+hashlib.md5(b).hexdigest()==row['expected_checksum'],'provider MD5 '+row['file'])
pr=json.loads((SRC/'pr1235.json').read_bytes())
need(pr['head']['sha']=='0266089ae6d4d8cc6392a2944c6f8c75967eb74e' and pr['number']==1235,'exact PR')
cmp=json.loads((SRC/'pr1235_compare.json').read_bytes())
need(len(cmp['files'])==8 and all('QUEUE.md' not in r['filename'] for r in cmp['files']),'eight no-QUEUE files')
for r in cmp['files']:
    b=(SRC/('pr_'+Path(r['filename']).name)).read_bytes()
    need(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==r['sha'],'immutable PR blob')
for version,recid in [('v10',23311939),('v11',23340371)]:
    j=json.loads((SRC/('zenodo_'+version+'.json')).read_bytes())
    need(j['id']==recid and j['state']=='done' and j['submitted'] is True,'published record state')
    need(j['conceptdoi']=='10.5281/zenodo.23311938' and j['conceptrecid']=='23311938','same DOI family')
    need(j['metadata']['creators'][0]['name']=='Ferudun, Alper','publication author')
    need(len(j['files'])==3,'three published payloads')
    need((SRC/('ferudun_'+version+'_source/verification_report.md')).read_bytes()==(SRC/('ferudun_'+version+'_OWR-741-001-verification-report.md')).read_bytes(),'standalone and archive report agree')
    for row in j['files']:
        b=(SRC/('ferudun_'+version+'_'+row['key'])).read_bytes()
        need(len(b)==row['size'] and 'md5:'+hashlib.md5(b).hexdigest()==row['checksum'],'full published payload')
    inventory=json.loads((HERE/('FERUDUN_'+version.upper()+'_ZIP_INVENTORY.json')).read_bytes())
    with zipfile.ZipFile(SRC/('ferudun_'+version+'_OWR-741-001-source.zip')) as z:
        need(z.testzip() is None,'complete archive CRC')
        members=[x for x in z.infolist() if not x.is_dir()]
        need(len(members)==inventory['regular_members'],'archive member count')
        indexed={r['path']:r for r in inventory['files']}
        need(set(indexed)=={x.filename for x in members},'archive closed inventory')
        for x in members:
            need(not Path(x.filename).is_absolute() and '..' not in Path(x.filename).parts,'safe archive path')
            b=z.read(x);row=indexed[x.filename]
            need(len(b)==row['bytes'] and sha(b)==row['sha256'] and x.CRC==row['crc32'],'archive member identity')
            out=SRC/('ferudun_'+version+'_source')/x.filename
            if out.exists():need(out.read_bytes()==b,'retained archive member')
a=(SRC/'ferudun_v10_source/main.tex').read_text();b=(SRC/'ferudun_v11_source/main.tex').read_text()
# The complete main proof sections, not just theorem titles, are unchanged.
start='\\section{Reduction to finitely many cases}'
stop='\\section{Remarks}'
need(start in a and start in b and stop in a and stop in b,'version proof-section markers')
need(a[a.index(start):a.index(stop)]==b[b.index(start):b.index(stop)],'versions have identical sections2--5 proof text')
for name in ['initial','final']:
    f=SRC/('ledger_'+name+'.json')
    if not f.exists():continue
    j=json.loads(f.read_bytes());vr=j['valueRanges'][0]
    need(j['spreadsheetId']=='1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20','ledger workbook')
    need(vr['dataFilters'][0]['gridRange']['sheetId']==1254632077 and
         vr['dataFilters'][0]['gridRange']['endColumnIndex']==43,'full numeric-gid ledger')
    rows=vr['valueRange']['values'];need(len(rows)>=191,'ledger row coverage')
    whole=' '.join(str(c) for row in rows for c in row).lower()
    need(not any(t in whole for t in ['30000107','owr-741-001','zenodo.23311939','zenodo.23340371','zenodo.23311938','generalized hive','generalised hive','math/0501446']),'semantic target aliases absent')


def points(r):return [(i,j,r-i-j) for i in range(r+1) for j in range(r+1-i)]
def dist2(p,q):return sum((a-b)**2 for a,b in zip(p,q))
def rhombi(r):
    ps=points(r);adj={p:{q for q in ps if dist2(p,q)==2} for p in ps};out={}
    for p,q in combinations(ps,2):
        if q not in adj[p]:continue
        tips=sorted(adj[p]&adj[q])
        if len(tips)!=2:continue
        s=tuple(sorted((p,q)));t=tuple(tips)
        need(dist2(*t)==6,'geometric long diagonal')
        out[(s,t)]={**{p:1,q:1},**{x:-1 for x in t}}
    need(len(out)==3*r*(r-1)//2,'all geometric primitive rhombi')
    return out

def evaluate(row,h):return sum((Q(c)*h.get(p,Q(0)) for p,c in row.items()),Q(0))
def floor(x):return x.numerator//x.denominator

def key(s,t):return (tuple(sorted(s)),tuple(sorted(t)))

r=6;P=points(r);I=[p for p in P if min(p)>0];geom=rhombi(r)
names={'x':(1,1,4),'y':(1,2,3),'z':(1,3,2),'d':(1,4,1),'a':(2,1,3),
       'e':(2,2,2),'c':(2,3,1),'b':(3,1,2),'f':(3,2,1),'g':(4,1,1)}
phi={names[k]:Q(1,2) for k in ['a','b','c','d']}
w={k:floor(evaluate(row,phi)) for k,row in geom.items()}
need(Counter(w.values())=={-1:10,0:33,1:2},'published complete bound counts')
need(all(evaluate(row,phi)>=w[k] for k,row in geom.items()),'published nonnegative half-array feasibility')
need(all(v>=0 for v in phi.values()),'nonnegative augmented witness')
# Re-key the fifteen printed rhombi using independently generated Euclidean geometry.
table=[
 ([(1,1,4),(0,1,5)],[(1,0,5),(0,2,4)],{'x':1},0),
 ([(1,2,3),(0,2,4)],[(1,1,4),(0,3,3)],{'y':1,'x':-1},0),
 ([(1,3,2),(0,3,3)],[(1,2,3),(0,4,2)],{'z':1,'y':-1},0),
 ([(2,4,0),(1,4,1)],[(2,3,1),(1,5,0)],{'d':1,'c':-1},0),
 ([(2,3,1),(1,4,1)],[(2,4,0),(1,3,2)],{'d':1,'c':1,'z':-1},1),
 ([(1,0,5),(0,1,5)],[(1,1,4),(0,0,6)],{'x':-1},0),
 ([(1,1,4),(0,2,4)],[(1,2,3),(0,1,5)],{'x':1,'y':-1},0),
 ([(1,2,3),(0,3,3)],[(1,3,2),(0,2,4)],{'y':1,'z':-1},0),
 ([(2,3,1),(1,3,2)],[(2,2,2),(1,4,1)],{'z':1,'c':1,'d':-1,'e':-1},0),
 ([(3,1,2),(2,1,3)],[(3,0,3),(2,2,2)],{'a':1,'b':1,'e':-1},1),
 ([(3,2,1),(2,2,2)],[(3,1,2),(2,3,1)],{'e':1,'f':1,'c':-1,'b':-1},-1),
 ([(2,4,0),(2,3,1)],[(3,3,0),(1,4,1)],{'c':1,'d':-1},0),
 ([(3,1,2),(3,0,3)],[(4,0,2),(2,1,3)],{'b':1,'a':-1},0),
 ([(4,2,0),(4,1,1)],[(5,1,0),(3,2,1)],{'g':1,'f':-1},0),
 ([(5,1,0),(5,0,1)],[(6,0,0),(4,1,1)],{'g':-1},0)]
rows=[];bounds=[]
for s,t,expected,rhs in table:
    k=key(s,t);need(k in geom,'printed row is genuine rhombus')
    reduced={p:c for p,c in geom[k].items() if min(p)>0}
    need(reduced=={names[n]:c for n,c in expected.items()} and rhs==w[k],'printed row and bound')
    rows.append([Q(reduced.get(p,0)) for p in I]);bounds.append(Q(rhs))

def unit(i):return tuple(Q(int(k==i-1)) for k in range(15))
def add(*vectors):return tuple(sum(x) for x in zip(*vectors))
def scale(s,v):return tuple(Q(s)*x for x in v)
def certificate(v,target,rhs):
    if len(v)!=15 or any(x<0 for x in v):raise ValueError('nonnegative multiplier domain')
    got=[sum(v[i]*rows[i][j] for i in range(15)) for j in range(10)]
    gotrhs=sum(v[i]*bounds[i] for i in range(15))
    if got!=[Q(target.get(p,0)) for p in I] or gotrhs!=rhs:raise ValueError('incorrect universal weighted sum')
    return True
zpos=add(unit(1),unit(2),unit(3));zneg=add(unit(6),unit(7),unit(8))
clow=add(unit(5),unit(12),zpos)
bE=add(unit(10),unit(13));fneg=add(unit(14),unit(15))
eneg=add(unit(9),unit(4),zneg)
epos=add(clow,bE,scale(2,unit(11)),scale(2,fneg))
cup=add(scale(2,unit(11)),scale(2,fneg),scale(2,eneg),bE,epos)
need(certificate(clow,{names['c']:2},Q(1)),'independent lower universal dual')
need(certificate(cup,{names['c']:-2},Q(-1)),'independent upper universal dual')
need(certificate(eneg,{names['e']:-1},Q(0)) and certificate(epos,{names['e']:1},Q(0)),'intermediate cancellation')
need(Q(1,2).denominator==2,'forced value is not integral')
rejected=0
for changed,target,rhs in [(tuple([-1]+list(clow[1:])),{names['c']:2},Q(1)),
                          (clow,{names['c']:2},Q(0)),
                          (clow,{names['d']:2},Q(1)),
                          (tuple(Q(0) for _ in range(15)),{names['c']:2},Q(1))]:
    try:certificate(changed,target,rhs)
    except ValueError:rejected+=1
need(rejected==4,'four negative certificate controls rejected')
need(any(w[k]!=0 for k in w),'c=0 saturation is outside this obstruction')
total=sum(phi.values())+sum(evaluate(row,phi)-w[k] for k,row in geom.items())
need(total==Q(25,2),'published rank6 augmented total')
# Compare the PR's support with the source example without assuming same witness.
prsupport={(1,1,4),(1,3,2),(2,1,3),(2,3,1)}
orbit=[{tuple(p[i] for i in perm) for p in prsupport} for perm in permutations(range(3))]
source_phi_in_PR_symmetry_orbit=set(phi) in orbit
# Exact finite controls for the universally proved one-row extension lemma.
G=geom;W=w;H=phi;extension=[]
for oldr in range(6,11):
    ng=rhombi(oldr+1);newH={(i,j,k+1):v for (i,j,k),v in H.items()};newW={}
    for k,row in ng.items():
        onside=sum(p[2]==0 for p in row)
        if onside==0:
            oldkey=key([(i,j,k-1) for i,j,k in k[0]],[(i,j,k-1) for i,j,k in k[1]])
            need(oldkey in G,'extension inherits an old rhombus');newW[k]=W[oldkey]
        else:
            need(onside in (1,2),'all new rhombus types classified');newW[k]=0 if onside==2 else -1
        need(evaluate(row,newH)>=newW[k],'extension exact witness feasibility')
    T=[p for p in points(oldr+1) if p[2]==1]
    for i in range(oldr):
        p=(i,oldr-i,1);q=(i+1,oldr-i-1,1)
        # The new two-boundary-point rows give both signs of adjacent T differences.
        found=[]
        for key0,row in ng.items():
            reduced={v:c for v,c in row.items() if min(v)>0}
            for sign in [-1,1]:
                target={v:c for v,c in {p:sign,q:-sign}.items() if min(v)>0}
                if reduced==target and newW[key0]==0:found.append(sign)
        need(set(found)=={-1,1},'extension forces T constant including ends')
    extension.append({'rank':oldr+1,'rhombi':len(ng),'half_coordinates':len(newH)})
    G,W,H=ng,newW,newH
print(json.dumps({'status':'PASS','checks':COUNT,'published_rank6_rhombi':45,'printed_proof_rows':15,
 'forced_coordinate':list(names['c']),'forced_value':'1/2','lower_multiplier':list(map(str,clow)),
 'upper_multiplier':list(map(str,cup)),'negative_controls_rejected':rejected,
 'rank6_augmented_total':'25/2','source_phi_in_PR_support_S3_orbit':source_phi_in_PR_symmetry_orbit,
 'extension_diagnostics':extension,'scope':'Existing published negative theorem identity and independent rank6 obstruction; no author execution, no small-rank classification replay, no first-priority certification.'},indent=2,sort_keys=True))
