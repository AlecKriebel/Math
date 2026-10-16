"""Independent exact comparison of primary C4 probability tables and relabelings."""
from itertools import product, combinations
from fractions import Fraction
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
assert __debug__, 'Verification requires assertions; do not use -O.'
A=Path(__file__).resolve().parent;X=list(product((0,1),repeat=4));E=[(0,1),(1,2),(2,3),(3,0)]
V=set(range(4));U=['0000','0011','1101','1110'];W=['0001','0010','1100','1111']
bits=lambda s:tuple(map(int,s));sha=lambda b:hashlib.sha256(b).hexdigest()
sources={
    'GL2016':('priority_sources_private/native_retrieval003/GL2016/GL2016.pdf','77287aa615ac5291b927a91c3a7622b362ddf747cf529f7d3e1be74b237282d1'),
    'KS2024':('priority_sources_private/native_retrieval002/KS2024v1/KS2024v1.pdf','45382694fde65d1c97399faac0d8d15a6049af198a6b4a16cc4fa228b11a3b6d'),
    'GMS2006':('priority_sources_private/native_retrieval001/GMS2006/GMS2006.pdf','1aa0d14f5822f7e5664180b92bb3c0f97e022d8276134ae949eaf4ceccc42441')}
for rel,h in sources.values():assert sha((A/rel).read_bytes())==h
def separated(I,J,C):
    seen=set(I);front=list(I)
    while front:
        i=front.pop()
        for a,b in E:
            j=b if a==i else a if b==i else None
            if j is not None and j not in C and j not in seen:seen.add(j);front.append(j)
    return not (seen & set(J))
seps=[]
for assignment in product(range(4),repeat=4):
    I=tuple(i for i,v in enumerate(assignment) if v==0);J=tuple(i for i,v in enumerate(assignment) if v==1);C=tuple(i for i,v in enumerate(assignment) if v==2)
    if I and J and separated(I,J,C):seps.append((I,J,C))
assert len(seps)==4
def audit(w):
    z=sum(w.values());assert z>0 and all(v>=0 for v in w.values())
    failures=[]
    for x,y in product(X,repeat=2):
        lo=tuple(min(a,b) for a,b in zip(x,y));hi=tuple(max(a,b) for a,b in zip(x,y))
        if w[lo]*w[hi]<w[x]*w[y]:failures.append([''.join(map(str,t)) for t in (x,y,lo,hi)])
    minors=0;ci_fail=[]
    for I,J,C in seps:
        for c in product((0,1),repeat=len(C)):
            table={(i,j):sum(w[x] for x in X if tuple(x[k] for k in I)==i and tuple(x[k] for k in J)==j and tuple(x[k] for k in C)==c)
                   for i in product((0,1),repeat=len(I)) for j in product((0,1),repeat=len(J))}
            for i0,i1 in combinations(list(product((0,1),repeat=len(I))),2):
                for j0,j1 in combinations(list(product((0,1),repeat=len(J))),2):
                    minors+=1
                    if table[i0,j0]*table[i1,j1]!=table[i0,j1]*table[i1,j0]:ci_fail.append([I,J,C,c])
    return dict(normalizer=z,normalized_sum=str(sum(Fraction(w[x],z) for x in X)),mtp2_ordered_pairs=256,mtp2_failures=failures,
                ordered_nontrivial_global_separations=len(seps),global_ci_minors=minors,global_ci_failures=ci_fail)
gl={x:(2 if x==(1,1,1,1) else 1) if x[2]==x[3] else 0 for x in X}
candidate={x:(2 if x==(1,1,1,1) else 1) if x[0]==x[1] else 0 for x in X}
ks={x:(7 if x==(0,0,0,0) else 1) if x[0]==x[1] else 0 for x in X}
rot=lambda old:(old[2],old[3],old[0],old[1])
assert all(candidate[rot(x)]==gl[x] for x in X)
for clique in [(),(0,),(1,),(2,),(3,),*E]:
    assert sorted(tuple(bits(s)[i] for i in clique) for s in U)==sorted(tuple(bits(s)[i] for i in clique) for s in W)
from math import prod
def quartic(w):
    z=sum(w.values());return dict(left=str(Fraction(prod(w[bits(s)] for s in U),z**4)),right=str(Fraction(prod(w[bits(s)] for s in W),z**4)),
                               difference=str(Fraction(prod(w[bits(s)] for s in U)-prod(w[bits(s)] for s in W),z**4)))
laws={name:audit(w) for name,w in [('GL_lemma5_2',gl),('submitted_C4',candidate),('KS_example6_5_normalized',ks)]}
for j in laws.values():assert not j['mtp2_failures'] and not j['global_ci_failures'] and j['normalized_sum']=='1'
assert quartic(candidate)['left']!=quartic(candidate)['right'];assert quartic(ks)['left']!=quartic(ks)['right']
oldsets={'GMS_example7':['0000','1000','1100','1110','0001','0011','0111','1111'],
         'GMS_example8':['0100','0111','1001','1010']}
controls={}
for name,ss in oldsets.items():
    w={x:int(x in set(map(bits,ss))) for x in X};r=audit(w);assert not r['global_ci_failures'] and r['mtp2_failures']
    flips=[]
    for mask in X:
        transformed={tuple(a^b for a,b in zip(x,mask)):v for x,v in w.items()}
        if not audit(transformed)['mtp2_failures']:flips.append(mask)
    controls[name]=dict(**r,coordinate_bit_reversals_tested=16,mtp2_after_bit_reversal=flips)
    assert not flips
j=dict(actual_utc=datetime.now(timezone.utc).isoformat(),status='PASS_PRIOR_LAWS_AND_EXACT_SUBMITTED_ROTATION',source_pdf_sha256={k:h for k,(_,h) in sources.items()},
       actual_laws= {'GL_lemma5_2':{''.join(map(str,x)):v for x,v in gl.items()},'KS_example6_5':{''.join(map(str,x)):v for x,v in ks.items()}},
       laws=laws,submitted_rotation='new=(old3,old4,old1,old2)',all_16_cells_and_C4_edges_preserved=True,
       classical_clique_balanced_quartic=dict(positive=U,negative=W,candidate=quartic(candidate),KS=quartic(ks)),negative_controls=controls,
       qualification='Prior C2/C3 witnesses verified; no closure-priority conclusion; KS overlapping mass-assignment typo interpreted explicitly as seven nonbottom states.')
p=A/'ROOT_PRIORITY_LAW_CHECKS.json';assert not p.exists();p.write_text(json.dumps(j,indent=2)+'\n');print(json.dumps(j,indent=2))
