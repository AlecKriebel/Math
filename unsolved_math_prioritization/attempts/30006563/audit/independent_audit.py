"""Independent audit of the frozen packet. No author code imported or executed.
Rebuilds mathematical objects from their stated specifications and verifies the
finite certificate, with complete Boolean semantics and symmetry validation.
Writes only in the sibling audit directory.
"""
from pathlib import Path
from itertools import combinations as C, product as P, permutations
from collections import Counter, defaultdict
import hashlib, json, copy
ROOT=Path(__file__).resolve().parent
AUTHOR=ROOT.parent/'author'
REPORT={}
def require(condition,message):
    if not condition: raise ValueError(message)

def edges(n): return list(C(range(n),2))
def typ(colors,t): return tuple(sorted(Counter(colors[e] for e in C(t,2)).items()))
def triangle_data(colors,n):
    return [(t,sum(1<<v for v in t),typ(colors,t)) for t in C(range(n),3)]
def violation(colors,n):
    # Vertex masks rather than the author's six-set iteration.
    ts=triangle_data(colors,n)
    for (t,m,s),(u,k,r) in C(ts,2):
        if not m&k and s==r:return t,u,s
    return None

def k9():
    groups=['A']*3+['B']*3+['z','x','y']
    palette={frozenset(['A']):1,frozenset(['B']):0,
             frozenset(['A','B']):0,frozenset(['A','z']):1,
             frozenset(['B','z']):1,frozenset(['A','x']):0,
             frozenset(['B','x']):2,frozenset(['A','y']):1,
             frozenset(['B','y']):2,frozenset(['z','x']):1,
             frozenset(['z','y']):0,frozenset(['x','y']):2}
    return {e:palette[frozenset(groups[v] for v in e)] for e in edges(9)}

def audit_manifest():
    m=AUTHOR/'MANIFEST.json'
    h=hashlib.sha256(m.read_bytes()).hexdigest()
    require(h=='d862a64b69ccfbf06f1c56dee1dcd8aedc86fccee2af0c325fb0897e31894dfc','manifest identity')
    j=json.loads(m.read_text()); require(j['file_count']==len(j['files'])==16,'file count')
    for f in j['files']:
        b=(AUTHOR/f['path']).read_bytes()
        require(len(b)==f['bytes'],'byte count '+f['path'])
        require(hashlib.sha256(b).hexdigest()==f['sha256'],'file digest '+f['path'])
    require({str(p.relative_to(AUTHOR)) for p in AUTHOR.rglob('*') if p.is_file()}=={'MANIFEST.json'}|{f['path'] for f in j['files']},'unlisted files')
    REPORT['frozen_manifest']={'sha256':h,'files_verified':16}

def audit_constructions():
    c=k9(); ts=triangle_data(c,9)
    require(violation(c,9) is None,'K9')
    require(len(c)==36 and set(c.values())=={0,1,2},'K9 complete coloring')
    n7={e:v for e,v in c.items() if e[1]<7}
    require(violation(n7,7) is None,'K7')
    expected={'000':10,'001':12,'002':9,'011':18,'012':16,'022':6,'111':7,'112':3,'122':0,'222':3}
    actual=Counter(''.join(str(c[e]) for e in sorted(C(t,2), key=lambda e:c[e])) for t,_,_ in ts)
    require({s:actual[s] for s in expected}==expected,'type counts')
    for t,_,_ in ts:
        s=''.join(map(str,sorted(c[e] for e in C(t,2))))
        if s in ('000','022'):require(len(set(t)&{3,4,5})>=2,'B intersection')
        if s in ('001','111'):require(len(set(t)&{0,1,2})>=2,'A intersection')
        fixed={'002':{7},'011':{6},'012':{8},'112':{6,7},'222':{7,8}}
        if s in fixed:require(fixed[s]<=set(t),'fixed intersection '+s)
    witness=json.loads((AUTHOR/'checks/extend_k7_results.json').read_text())
    require(c=={tuple(row[:2]):row[2] for row in witness['edge_colors']},'K9 stored witness')
    finite=[]
    for record in json.loads((AUTHOR/'checks/small_two_color_results.json').read_text()):
        if record['status']=='SAT':
            n=record['n']; red=set(map(tuple,record['color1_edges']))
            cc={e:int(e in red) for e in edges(n)}
            require(violation(cc,n) is None,'stored SAT witness')
            finite.append(n)
    extensions={}
    for n in [10,12,16]:
        cc=dict(c)
        for v in range(9,n):
            for u in range(v):cc[u,v]=v-6
        require(violation(cc,n) is None,'extension')
        require(len(set(cc.values()))==n-6,'extension colors')
        extensions[n]=sum(not x[1]&y[1] for x,y in C(triangle_data(cc,n),2))
    require(violation({e:0 for e in edges(6)},6) is not None,'negative control')
    # Exhaustive verification of the multiset/isomorphism correspondence for 3 colors.
    ee=edges(3)
    for a,b in P(list(P(range(3),repeat=3)),repeat=2):
        iso=any(all(a[i]==b[ee.index(tuple(sorted((p[u],p[v]))))] for i,(u,v) in enumerate(ee)) for p in permutations(range(3)))
        require(iso==(Counter(a)==Counter(b)),'triangle type equivalence')
    REPORT['constructions']={'K7':'PASS','K9_type_counts':expected,'stored_SAT_witnesses':finite,'extension_disjoint_pairs':extensions,'type_isomorphism_tests':729,'negative_control':'PASS'}

def clauses_with_documented_order():
    e=edges(8);index={uv:i for i,uv in enumerate(e)};ts=list(C(range(8),3));out=[]
    for t,u in C(ts,2):
        if set(t).intersection(u):continue
        te=list(C(t,2));ue=list(C(u,2))
        for b in P([0,1],repeat=6):
            if sum(b[:3])==sum(b[3:]):out.append(tuple((index[uv],1-b[i]) for i,uv in enumerate(te+ue)))
    return out

def audit_proof():
    cs=clauses_with_documented_order(); canonical={frozenset(c) for c in cs}
    require(len(cs)==len(canonical)==5600,'5600 distinct clauses')
    # Independently enumerate balanced edge subsets, directly from vertex cuts
    # of each six-set. Verify every local six-bit truth table, no solver involved.
    edge_index={e:i for i,e in enumerate(edges(8))}; required=set();pairs=0
    for six in C(range(8),6):
        for t in C(six,3):
            u=tuple(v for v in six if v not in t)
            if t>u:continue
            pairs+=1
            te=tuple(edge_index[e] for e in C(t,2));ue=tuple(edge_index[e] for e in C(u,2))
            for k in range(4):
                for red_t,red_u in P(C(te,k),C(ue,k)):
                    reds=set(red_t+red_u)
                    required.add(frozenset((v,int(v not in reds)) for v in te+ue))
            local=[c for c in canonical if {v for v,_ in c}==set(te+ue)]
            require(len(local)==20,'local clause count')
            for bits in P([0,1],repeat=6):
                val=dict(zip(te+ue,bits))
                satisfies=all(any(val[v]==b for v,b in cl) for cl in local)
                require(satisfies==(sum(bits[:3])!=sum(bits[3:])),'local formula semantics')
    require(pairs==280 and canonical==required,'complete forbidden condition')
    require({frozenset((v,1-b) for v,b in c) for c in canonical}==canonical,'color-complement symmetry')
    proof=json.loads((AUTHOR/'checks/k8_two_color_unsat_certificate.json').read_text())
    stats=Counter()
    def validate(node,assignment,depth=0):
        require(isinstance(node,dict),'node shape')
        stats['nodes']+=1; stats['max_depth']=max(stats['max_depth'],depth)
        a=assignment.copy()
        def unresolved(index):
            require(type(index) is int and 0<=index<len(cs),'clause index')
            cc=cs[index]
            require(not any(a.get(v,-1)==b for v,b in cc),'reason already satisfied')
            return {(v,b) for v,b in cc if v not in a}
        for v,b,i in node['units']:
            require(type(v) is int and 0<=v<28 and v not in a,'unit variable')
            require(type(b) is int and b in [0,1],'unit bit')
            require(unresolved(i)=={(v,b)},'not a unit reason')
            a[v]=b;stats['unit_assignments']+=1
        if 'conflict' in node:
            require(set(node)=={'units','conflict'},'leaf extra fields')
            require(not unresolved(node['conflict']),'nonempty conflict')
            stats['leaves']+=1;return
        require(set(node)=={'units','branch','zero','one'},'branch shape')
        v=node['branch'];require(type(v) is int and 0<=v<28 and v not in a,'branch variable')
        stats['branches']+=1
        for b,label in [(0,'zero'),(1,'one')]:validate(node[label],a|{v:b},depth+1)
    validate(proof,{0:0})
    require(stats['nodes']==571 and stats['leaves']==stats['branches']+1,'full proof tree')
    # A wrong root assumption must be rejected by the same validation semantics.
    saved=dict(stats)
    try:validate(proof,{0:1})
    except ValueError:negative='PASS'
    else:raise ValueError('proof negative control failed')
    REPORT['K8_UNSAT']={'clauses':len(cs),'disjoint_pairs':pairs,'truth_assignments_checked':pairs*64,'color_swap_symmetry':'PASS','proof_stats':saved,'wrong_root_negative_control':negative,'status':'PASS'}

def audit_reproduction():
    cc=k9();seed={e:v for e,v in cc.items() if e[1]<7}
    def add(c,row,v):return c|{(i,v):value for i,value in enumerate(row)}
    patterns=[]
    for row in P(range(3),repeat=7):
        if violation(add(seed,row,7),8) is None:patterns.append(row)
    first=[r for r in patterns if r[:3]==tuple(sorted(r[:3])) and r[3:6]==tuple(sorted(r[3:6]))]
    tested=0;found=None
    for a in first:
        for b in patterns:
            for d in range(3):
                tested+=1
                full=add(add(seed,a,7),b,8)|{(7,8):d}
                if violation(full,9) is None:found=full;break
            if found:break
        if found:break
    require(len(patterns)==58 and len(first)==26 and tested==27 and found==cc,'K7 extension reproduction')
    rows={}
    for base in [0,1]:
        rows[base]=[r for tail in P(range(4),repeat=3) if violation(add(cc,r:=(base,)*3+(3,)*3+tail,9),10) is None]
    require(len(rows[0])==8 and len(rows[1])==3,'individually feasible rows')
    failures=[]
    for a,b in P(rows[0],rows[1]):
        full=add(add(cc,a,9),b,10)|{(9,10):3}
        bad=violation(full,11);require(bad is not None,'24 case rejection')
        failures.append({'u_tail':a[6:],'v_tail':b[6:],'disjoint_repeat':bad})
    require(len(failures)==24,'24 coverage')
    (ROOT/'ansatz_failure_witnesses.json').write_text(json.dumps(failures,indent=2)+'\n')
    REPORT['bounded_reproduction']={'valid_K8_rows':len(patterns),'canonical_first_rows':len(first),'combinations_before_K9':tested,'ansatz_valid_u_rows':len(rows[0]),'ansatz_valid_v_rows':len(rows[1]),'ansatz_rejected_pairs':len(failures)}

audit_manifest();audit_constructions();audit_proof();audit_reproduction();audit_manifest()
REPORT['overall']='PASS'
(ROOT/'independent_results.json').write_text(json.dumps(REPORT,indent=2)+'\n')
print(json.dumps(REPORT,indent=2))
