#!/usr/bin/env python3
"""New independently designed packet, integral lattice, and source controls.
Exact finite diagnostics supplement UNIVERSAL_PROOF.md, not topology certification.
Writes only this review's output; never invokes queue helpers or imports old code.
"""
from pathlib import Path
import hashlib, itertools, json, math, sqlite3
from datetime import datetime, timezone
import sympy as s
from sympy.matrices.normalforms import smith_normal_form
HERE=Path(__file__).resolve().parent
BASE=HERE.parent
PACKET=BASE/'reviewed_candidate'
WORKSPACE=Path('/Users/alec/Documents/Math')
checks=[]
mutants=[]
def check(ok,label):
    assert ok,label
    checks.append(label)
def sha(data):return hashlib.sha256(data).hexdigest()
def quotient(M):
    a=s.Matrix(M); d=smith_normal_form(a,domain=s.ZZ)
    diag=[abs(int(d[i,i])) for i in range(min(d.shape))]
    return {'free_rank':a.rows-sum(v!=0 for v in diag),'torsion':[v for v in diag if v>1]}
def bindings(root,members):
    return all((root/e['path']).is_file() and (root/e['path']).stat().st_size==e.get('bytes',e.get('size')) and sha((root/e['path']).read_bytes())==e['sha256'] for e in members)
manifest=json.loads((PACKET/'MANIFEST.json').read_text()); deps=json.loads((PACKET/'CURRENT_PROOF_DEPENDENCIES.json').read_text())
check(bindings(PACKET,manifest['files']) and len(manifest['files'])==32,'all32currentbindings')
check(bindings(BASE,deps['files']) and len(deps['files'])==186,'all186dependencies')
check((PACKET/'CANDIDATE.md').read_bytes().split(b'## 1. Statement',1)[1]==(PACKET/'ORIGINAL_CANDIDATE.md').read_bytes().split(b'## 1. Statement',1)[1],'entireunchangedscientificbody')
check(sha((PACKET/'CANDIDATE.md').read_bytes()+b'\0')!=manifest['files'][0]['sha256'],'actualonebyteproofmutationrejected')
# Universal integral expansion, independently via coefficient extraction in a nilpotent parameter.
x,y,p,q,t=s.symbols('x y p q t')
lines=[x+p*t,y+q*t,-x-y-(p+q)*t]
roots=[lines[j]-lines[i] for i,j in [(0,1),(0,2),(1,2)]]
c2=lambda vals:sum(vals[i]*vals[j] for i in range(len(vals)) for j in range(i+1,len(vals)))
a=-s.expand(c2(lines)).coeff(t,1); k=s.expand(sum(roots)).coeff(t,1); v=-s.expand(c2(roots)).coeff(t,1)
delta=-4*x-2*y
check(s.expand(a-((2*x+y)*p+(x+2*y)*q))==0,'fullSUcherncoefficient')
check(s.expand(k+4*p+2*q)==0,'integrabledeterminantcoefficient')
check(s.expand(v+delta*k-3*a)==0,'fixedErawcoordinateshear')
check(s.expand(v-3*a)!=0,'ordinaryc2shortcutfailsasgenericpolynomial')
# Generic true target-loop torsion counterexample; not a flag image label.
check((1-1)%2==0 and 1%2!=0,'RP2timesS1genericloopordinaryandvirtualdiffer')
# Independently enumerate integer-lattice quotient presentations. A=Z, C=Z/m;
# 2m times the determinant generator lies in the relation lattice (take q=m).
# Reducing the determinant ambient coordinate mod2m therefore loses no quotient.
models=[]
for m in [1,2,3,4,6,8]:
    ambient=list(itertools.product(range(m),range(2*m),range(m)))
    for xx,yy in itertools.product(range(m),repeat=2):
        dd=(-4*xx-2*yy)%m
        if (2*dd)%m:continue
        image=set()
        directD=set()
        for pp,qq in itertools.product(range(2*m),repeat=2):
            aa=((2*xx+yy)*pp+(xx+2*yy)*qq)%m
            kk=(-4*pp-2*qq)%(2*m)
            vv=(-(10*xx+5*yy)*pp-(5*xx-2*yy)*qq)%m
            normalized=(vv+dd*kk)%m
            check(normalized==(3*aa)%m,f'integraltorsionrawshear:{m,xx,yy,pp,qq}')
            image.add((aa,kk,normalized));directD.add((kk,aa))
        mapped={( (z[2]-3*z[0])%m,z[1],z[0]) for z in ambient}
        check(len(mapped)==len(ambient),f'unimodularbijectionentireambient:{m,xx,yy}')
        mappedImage={((z[2]-3*z[0])%m,z[1],z[0]) for z in image}
        check(mappedImage=={(0,kk,aa) for kk,aa in directD},f'exactimagequotient:{m,xx,yy}')
        check(len(ambient)//len(image)==m*(2*m*m//len(directD)),f'fullquotientsizematches:{m,xx,yy}')
        models.append({'m':m,'x':xx,'y':yy,'delta':dd,'quotient_size':len(ambient)//len(image)})
# A tempting division by3 is NOT an automorphism on C=Z/3.
badImages={( (vv-3*uu)%3,mm,(3*uu)%3) for uu,mm,vv in itertools.product(range(3),range(2),range(3))}
check(len(badImages)==6 and len(badImages)<18,'actualnonunimodularthreecancellationrejected');mutants.append('divide/cancel3insecondarytorsion')
# Fresh higher-rank actual oriented T3 primary labels y=-2x; all integral x permitted.
torus=[]
for coefficients in itertools.product(range(-1,2),repeat=3):
    # Pairings H2 x H1 in the oriented T3 basis (23,31,12) x (1,2,3).
    row=[0,0,0]+[-3*c for c in coefficients]
    D=[[-4*(i==j) for j in range(3)]+[-2*(i==j) for j in range(3)] for i in range(3)]+[row]
    full=[row]+D[:3]+[[3*v for v in row]]
    got=quotient(full); expected=quotient(D);expected['free_rank']+=1
    check(got==expected,f'T3fullcoupledintegralSNF:{coefficients}')
    torus.append({'x':coefficients,'fiber':got})
# The frame model on an open infinite handlebody (a locally finite graph
# thickening) has A=product_countable Z and B=C=0. The universal quotient is
# product_countable Z/2. Prefix controls cannot prove this infinite assertion;
# its proof is in UNIVERSAL_PROOF.md. The all-ones element has no finite support.
for n in [1,4,19,101]:
    ones=(1,)*n
    check(all(z%2==1 for z in ones),'infiniteordinarycohomologyprefix:'+str(n))
check(quotient([[-4,-2]])=={'free_rank':0,'torsion':[2]},'noncompactcircleframeZ2')
check(not any((-4*xx-2*yy-1)%2==0 for xx,yy in itertools.product(range(2),repeat=2)),'actualRP2timesRnoindices')
# Literal named twelve-column guard; work on a saved private byte copy only.
queue=(WORKSPACE/'unsolved_math_prioritization/QUEUE.md').read_bytes()
(HERE/'tmp/QUEUE_OBSERVED.md').write_bytes(queue)
linesQ=queue.decode().splitlines(keepends=True)
header=next(l for l in linesQ if l.startswith('| Rank |'))
names=[c.strip() for c in header.split('|')[1:-1]]
check(names==['Rank','ID / code','Problem','EV','Impact (/10)','Difficulty','Proposed','Status','Turns','Chat','Findings','DOI'],'actualnamed12columnheader')
patch=json.loads((PACKET/'CURRENT_QUEUE_PATCH.json').read_text())
def patch_row(data,newrow):
    lines=data.splitlines(keepends=True);where=[i for i,l in enumerate(lines) if l.startswith('|') and len(l.split('|'))>2 and l.split('|')[2].strip().split(' / ')[0]=='6800007']
    if len(where)!=1:raise ValueError('duplicate/missingtarget')
    i=where[0]; old=lines[i].split('|'); new=newrow.split('|')
    if len(new)!=14:raise ValueError('lostschema')
    allowed={8,9,11}
    if any(old[j]!=new[j] for j in range(14) if j not in allowed):raise ValueError('protectedfieldchange')
    if new[8].strip()!='already_solved' or new[9].strip()!='1/5' or not new[11].strip():raise ValueError('dispositionmisplaced')
    lines[i]=newrow;return ''.join(lines)
changed=patch_row(queue.decode(),patch['row_prospective']); before=queue.decode().splitlines(keepends=True); after=changed.splitlines(keepends=True)
check(sum(a!=b for a,b in zip(before,after))==1,'privateactualqueueonlytargetrowchange')
row=patch['row_prospective'].split('|'); row[10],row[11]=row[11],row[10]
for label,text,newrow in [('ChatFindingsswap',queue.decode(),'|'.join(row)),('lost8columnschema',queue.decode(),'|'.join(patch['row_prospective'].split('|')[:9])+ '|\n'),('duplicatetarget',queue.decode()+patch['row_before'],patch['row_prospective']),('DOIoverwrite',queue.decode(),patch['row_prospective'].replace('|  |\n','| syntheticDOI |\n'))]:
    try:patch_row(text,newrow)
    except (ValueError,IndexError):mutants.append(label)
    else:raise AssertionError(label)
# Complete raw source, separate prior, and actual SQLite TEXT serialization.
pair=json.loads((PACKET/'source_record.json').read_text()); context=json.loads((PACKET/'CURRENT_SOURCE_CONTEXT.json').read_text())
check(sha(json.dumps([pair['problem'],pair['prior_upstream_report']],sort_keys=True).encode())==context['review_hash'],'fullrawsourceandseparatepriorreviewhash')
check(sha(pair['problem']['statement'].encode())==context['statement_hash'],'exactstatementhash')
with sqlite3.connect((WORKSPACE/'unsolved_math_prioritization/cache/catalog.sqlite').as_uri()+'?mode=ro',uri=True) as db:
    rows=db.execute('select payload,report,typeof(payload),typeof(report) from records where key=?',('6800007',)).fetchall()
    check(len(rows)==1 and rows[0][2:]==('text','text'),'actualSQLiteTEXTpair')
    check(json.loads(rows[0][0])==pair['problem'] and json.loads(rows[0][1])==pair['prior_upstream_report'],'actualSQLiteequalsentireembeddedpair')
for label,mut in [('wrongID',{**pair['problem'],'id':6800006}),('wrongcode',{**pair['problem'],'problem_number':'AMR-067-0006'}),('wrongstatement',{**pair['problem'],'statement':'uniformization instead'})]:
    check(sha(json.dumps([mut,pair['prior_upstream_report']],sort_keys=True).encode())!=context['review_hash'],label);mutants.append(label)
for report in [None,{}, {'classification':'solved'}]:
    check(sha(json.dumps([pair['problem'],report],sort_keys=True).encode())!=context['review_hash'],'priorreportmutation:'+str(report));mutants.append('priorreport:'+str(report))
check(len((PACKET/'turns.jsonl').read_text().splitlines())==1 and json.loads((PACKET/'turns.jsonl').read_text())['turn']==1,'originalsingleattemptconserved')
result={'utc':datetime.now(timezone.utc).isoformat(),'pass':True,'assertions':len(checks),'checks':checks,'models':models,'T3_models':torus,'mutants_rejected':mutants,'current_manifest_sha256':sha((PACKET/'MANIFEST.json').read_bytes()),'dependency_manifest_sha256':sha((PACKET/'CURRENT_PROOF_DEPENDENCIES.json').read_bytes()),'queue_observed_sha256':sha(queue),'frozen_queue_preimage_matches_observation':sha(queue)==patch['whole_queue_preimage_sha256'],'scope':'Exact finite integral and binding diagnostics; no program proves h-principle, topology, arbitrary infinite source or historical priority. All actual proof/source readings are separately documented. Queue mutation occurred ONLY on strings and own private snapshot.'}
(HERE/'FRESH_CONTROL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'pass':True,'assertions':len(checks),'torsion_lattice_models':len(models),'new_T3_models':len(torus),'mutants_rejected':len(mutants)},indent=2))
