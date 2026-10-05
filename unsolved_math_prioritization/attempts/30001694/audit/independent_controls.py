#!/usr/bin/env python3
"""Third implementation and adversarial controls; no scientific dependencies.
No author function is used to compute the independent answers. Optional --original
only enables post-computation cross-checks and mutation tests against the authors.
"""
from pathlib import Path
from itertools import combinations, product
from collections import Counter
from fractions import Fraction as F
import argparse, csv, json, hashlib, importlib.util, tempfile, math

P=[(x,y) for y in range(5) for x in range(5)]
CELL=[(x,y) for y in range(4) for x in range(4)]

def cells(mask):return {CELL[i] for i in range(16) if mask & (1<<i)}
def encoding(c):return sum(1<<(4*y+x) for x,y in c)
def edges_and_points(c):
    edges=set(); verts=set(); directed=[]
    for x,y in c:
        v=[(x,y),(x+1,y),(x+1,y+1),(x,y+1)]
        ns=[(x,y-1),(x+1,y),(x,y+1),(x-1,y)]
        verts.update(v)
        for i in range(4):
            a,b=v[i],v[(i+1)%4];edges.add(tuple(sorted((a,b))))
            if ns[i] not in c:directed.append((a,b))
    return edges,verts,directed

def admissible_euler(c):
    if not c:return False
    roots={p:p for p in c}
    def root(p):
        while roots[p]!=p:p=roots[p]
        return p
    for x,y in c:
        for q in [(x+1,y),(x,y+1)]:
            if q in roots:roots[root((x,y))]=root(q)
    if len({root(p) for p in c})!=1:return False
    e,v,_=edges_and_points(c)
    if len(v)-len(e)+len(c)!=1:return False
    for x,y in v:
        q=[(x-1,y-1),(x,y-1),(x,y),(x-1,y)]
        bits=sum(1<<i for i,p in enumerate(q) if p in c)
        if bits in (5,10):return False
    return True

def d2(a,b):return sum((a[i]-b[i])**2 for i in (0,1))
def is_square(q):
    d=sorted((d2(a,b),a,b) for a,b in combinations(q,2))
    z=d[0][0]
    if z==0 or [a for a,_,_ in d]!=[z,z,z,z,2*z,2*z]:return False
    _,a,b=d[-1];_,c,e=d[-2]
    return len({a,b,c,e})==4 and tuple(a[i]+b[i] for i in (0,1))==tuple(c[i]+e[i] for i in (0,1)) and sum((a[i]-b[i])*(c[i]-e[i]) for i in (0,1))==0

SQUARES=[(tuple(sorted(q)),min(d2(a,b) for a,b in combinations(q,2))) for q in combinations(P,4) if is_square(q)]
BLOCKS=[]
for s in range(1,5):
    for y in range(5-s):
        for x in range(5-s):
            BLOCKS.append((s,x,y,sum(1<<(4*(y+j)+x+i) for i in range(s) for j in range(s))))

def analyze(mask):
    c=cells(mask);_,_,edges=edges_and_points(c);b={v for e in edges for v in e}
    s=max(s for s,x,y,m in BLOCKS if m&mask==m)
    sq=[(q,z) for q,z in SQUARES if set(q)<=b]
    m=max([z for q,z in sq]+[0])
    axis=sum(len({x for x,y in q})==2 and len({y for x,y in q})==2 for q,z in sq)
    return s,m,b,sq,axis

def cycle(c):
    _,_,e=edges_and_points(c);nxt=dict(e);start=min(nxt);q=[start]
    while nxt[q[-1]]!=start:
        q.append(nxt[q[-1]])
        assert len(q)<=len(e)
    assert len(q)==len(e)
    return q

def mask_inside(q):
    # Exact parity ray cast from all cell centers, doubled integer coordinates.
    out=0
    for k,(x,y) in enumerate(CELL):
        crossings=0
        for a,b in zip(q,q[1:]+q[:1]):
            if a[0]==b[0] and 2*min(a[1],b[1]) < 2*y+1 < 2*max(a[1],b[1]) and 2*a[0]>2*x+1:
                crossings+=1
        if crossings%2:out|=1<<k
    return out

def rounding_controls():
    out=Counter();samples={}
    # Alternating selected integer coordinates: x,k=a+b,l=y-b integers.
    for x,k,l in product(range(-2,3),repeat=3):
        for den in range(1,8):
            for num in range(-3*den,3*den+1):
                b=F(num,den);a=k-b;y=l+b
                q=[(F(x),y),(x+a,y-b),(x+a+b,y+a-b),(x+b,y+a)]
                if a*a+b*b==0:continue
                z0=a*a+b*b;lo=math.floor(b)-b;hi=math.ceil(b)-b
                endpoints=[]
                for d in (lo,hi):
                    v=[(q[0][0],q[0][1]+d),(q[1][0]-d,q[1][1]),(q[2][0],q[2][1]-d),(q[3][0]+d,q[3][1])]
                    assert all(vv.denominator==1 for p in v for vv in p)
                    assert (a-d)**2+(b+d)**2==d2(v[0],v[1])
                    for i in range(4):
                        varying=1 if i%2==0 else 0
                        assert math.floor(q[i][varying])<=v[i][varying]<=math.ceil(q[i][varying])
                    if d2(v[0],v[1])>0:assert is_square(v)
                    endpoints.append(d2(v[0],v[1]))
                assert max(endpoints)>=z0
                out['alternating_cases']+=1
                if min(endpoints)==0:
                    out['one_endpoint_degenerate']+=1
                    samples.setdefault('degenerate_endpoint',{'x':x,'k':k,'l':l,'b':str(b),'original_side_squared':str(z0),'endpoint_side_squared':list(map(str,endpoints))})
                if endpoints[0]<z0<endpoints[1]:out['must_choose_upper_endpoint']+=1
                if endpoints[1]<z0<endpoints[0]:out['must_choose_lower_endpoint']+=1
    # Three parallel selections, including negative parameters and translations.
    for a,b,y,n,den in product(range(-2,3),range(-2,3),range(-2,3),range(-7,8),range(1,7)):
        if a==b==0:continue
        x=F(n,den);q=[(x,F(y)),(x+a,y-b),(x+a+b,y+a-b),(x+b,y+a)]
        shift=math.ceil(x)-x;r=[(xx+shift,yy) for xx,yy in q]
        assert all(v.denominator==1 for p in r for v in p)
        assert all(math.floor(xx)<=rr[0]<=math.ceil(xx) for (xx,yy),rr in zip(q,r))
        assert is_square(r) and d2(r[0],r[1])==a*a+b*b
        out['parallel_cases']+=1
    return {'counts':dict(out),'examples':samples,'negative_control':'Choosing an arbitrary endpoint rather than a nonshrinking endpoint can shrink or collapse the square.'}

def run(original,out):
    out.mkdir(parents=True,exist_ok=True)
    results={};allmasks={};by=Counter();dist=Counter();records=[]
    for mask in range(1,65536):
        if not admissible_euler(cells(mask)):continue
        s,m,b,sq,axis=analyze(mask);by[s]+=1
        assert 2*m>=s*s
        allmasks[mask]=(s,m);records.append(f'{mask},{s},{m},{len(b)},{len(sq)},{axis}\n')
    raw=('mask,s,max_side_squared,boundary_points,square_count,axis_square_count\n'+''.join(records)).encode()
    (out/'INDEPENDENT_ENUMERATION.csv').write_bytes(raw)
    ratios=[(F(m,s*s),mask) for mask,(s,m) in allmasks.items()]
    results['enumeration']={'examined':65535,'admissible':len(allmasks),'rejected':65535-len(allmasks),'by_s':dict(sorted(by.items())),'min_ratio':str(min(ratios)[0]),'first_min_mask':min(ratios)[1],'total_possible_squares_in_5x5_points':len(SQUARES),'certificate_bytes':len(raw),'certificate_sha256':hashlib.sha256(raw).hexdigest()}
    assert len(allmasks)==9349 and by=={1:2932,2:6034,3:382,4:1}
    # All eight square-box isometries of all accepted masks.
    sym=0;quarter=0;rect=0
    for mask,(s,m) in allmasks.items():
        c=cells(mask)
        for reflect in (False,True):
            cc={(3-x,y) if reflect else (x,y) for x,y in c}
            for turns in range(4):
                assert allmasks[encoding(cc)]==(s,m);sym+=1
                cc={(3-y,x) for x,y in cc}
        x0=min(x for x,y in c);x1=max(x for x,y in c)+1;y0=min(y for x,y in c);y1=max(y for x,y in c)+1
        if len(c)==(x1-x0)*(y1-y0):
            assert s==min(x1-x0,y1-y0) and m==s*s;rect+=1
        # Rotation maps lower-left cell coordinates via the cell centers.
        if x1-x0==y1-y0:
            rotated={((x0+x1+y0+y1)//2-y-1,(y0+y1-x0-x1)//2+x) for x,y in c}
            if rotated==c:assert m>=s*s;quarter+=1
    results['symmetry']={'D4_checks':sym,'rectangular_masks':rect,'quarter_turn_invariant_masks':quarter}
    # Exhaust all unit chords and both resulting Jordan loops.
    surgery=Counter();first={}
    for mask,(s,m) in allmasks.items():
        q=cycle(cells(mask));n=len(q);B=set(q)
        for i,j in combinations(range(n),2):
            if (j-i)%n in (1,n-1) or d2(q[i],q[j])!=1:continue
            q1=q[i:j+1];q2=q[j:]+q[:i+1]
            assert 4<=len(q1)<=n-2 and 4<=len(q2)<=n-2
            assert set(q1)<=B and set(q2)<=B
            c1=mask_inside(q1);c2=mask_inside(q2)
            assert c1 in allmasks and c2 in allmasks
            assert allmasks[c1][1]<=m and allmasks[c2][1]<=m
            if c1|c2==mask and c1&c2==0:
                kind='interior';assert max(allmasks[c1][0],allmasks[c2][0])>=s
            else:
                kind='exterior';assert (c1^c2)==mask and (c1&c2) in (c1,c2)
                bigger=c1|c2;assert (bigger&mask)==mask and allmasks[bigger][0]>=s
            surgery[kind]+=1
            first.setdefault(kind,{'mask':mask,'chord':[q[i],q[j]],'result_masks':[c1,c2]})
    results['chord_surgery']={'counts':dict(surgery),'first_examples':first}
    cases={'empty':(set(),False),'disconnected':({(0,0),(2,0)},False),'diagonal_only':({(0,0),(1,1)},False),'hole':({(x,y) for x in range(3) for y in range(3)}-{(1,1)},False),'edge_connected_pinch':({(0,1),(0,0),(1,0),(2,0),(2,1),(2,2),(1,2)},False),'unit':({(0,0)},True),'u_shape':({(0,0),(1,0),(2,0),(0,1),(2,1),(0,2),(2,2)},True)}
    controls={}
    for name,(c,want) in cases.items():
        actual=admissible_euler(c);assert actual==want;controls[name]={'admissible':actual,'mask':encoding(c)}
    s,m,b,sq,axis=analyze(886)
    assert len(cells(886))==7 and (s,m,axis)==(2,5,0)
    controls['mask_886']={'s':s,'max_side_squared':m,'axis_squares':axis,'squares':sq,'boundary_rows':{y:sorted(x for x,yy in b if yy==y) for y in range(4)}}
    full={(0,0),(0,1),(1,0),(1,1),(1,2),(2,1),(2,2)}
    assert (1,1) not in analyze(encoding(full))[2]
    controls['maximum_block_corner_not_boundary']={'mask':encoding(full),'s':2,'interior_corner':[1,1]}
    assert tuple(sorted(((0,0),(3,0),(3,3),(0,3)))) in [q for q,z in analyze(encoding(cases['u_shape'][0]))[3]]
    controls['boundary_square_not_contained']={'u_shape_mask':encoding(cases['u_shape'][0]),'missing_cell':[1,1]}
    results['geometric_negative_controls']=controls
    results['rounding']=rounding_controls()
    if original:
        mods=[]
        for name in ('compute','verify'):
            sp=importlib.util.spec_from_file_location('authored_'+name,original/(name+'.py'));mod=importlib.util.module_from_spec(sp);sp.loader.exec_module(mod);mods.append(mod)
        compute,verify=mods
        for mask in range(65536):
            c=cells(mask);ok=mask in allmasks
            assert compute.valid(c)==verify.admissible(c)==ok,('predicate mismatch',mask)
        results['author_predicate_comparison']={'masks_including_empty':65536,'disagreements':0}
        with (original/'computation/certificate.csv').open() as f:rows=list(csv.DictReader(f));fields=list(rows[0])
        assert len(rows)==len(allmasks) and len({int(r['mask']) for r in rows})==len(rows)
        for row in rows:
            mask=int(row['mask']);s,m=allmasks[mask]
            assert (int(row['s']),int(row['max_side_squared']))==(s,m)
            block=sum(1<<(4*(int(row['block_y'])+j)+int(row['block_x'])+i) for i in range(s) for j in range(s))
            assert mask&block==block
            q=tuple(sorted((int(row[f'x{i}']),int(row[f'y{i}'])) for i in range(4)))
            assert (q,m) in analyze(mask)[3]
        results['author_certificate_comparison']={'rows':len(rows),'parameters_blocks_and_square_witnesses_match':True}
        mutations={}
        for kind in ['wrong_side','wrong_s','invalid_square','wrong_block','missing','duplicate','extra_mask_zero','extra_mask_65536']:
            r=[z.copy() for z in rows]
            if kind=='wrong_side':r[0]['max_side_squared']='2'
            if kind=='wrong_s':r[0]['s']='2'
            if kind=='invalid_square':r[0]['x0']='99'
            if kind=='wrong_block':r[0]['block_x']='99'
            if kind=='missing':r.pop(0)
            if kind=='duplicate':r.insert(0,r[0].copy())
            if kind.startswith('extra_mask_'):z=r[0].copy();z['mask']='0' if kind=='extra_mask_zero' else '65536';r.append(z)
            with tempfile.TemporaryDirectory() as td:
                p=Path(td)/'x.csv'
                with p.open('w') as f:w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(r)
                try:verify.check_certificate(p)
                except AssertionError as e:mutations[kind]={'rejected':True,'message':str(e)}
                else:mutations[kind]={'rejected':False,'defect':'An extra out-of-domain mask is silently accepted.'}
        results['certificate_mutations']=mutations
    results['scope']='Bounded audit controls only. No universal proof, counterexample, novelty claim or published n<=13 replay.'
    (out/'INDEPENDENT_RESULTS.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps(results,indent=2))

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--original',type=Path);ap.add_argument('--out',type=Path,default=Path(__file__).resolve().parent);a=ap.parse_args();run(a.original,a.out)
