#!/usr/bin/env python3
"""Read-only source receipts and independent finite mathematical checks.

This is an audit, not an implementation or certificate of the upstream FPRAS.
All tests use exact fractions; nothing is installed and no Lean build is run.
"""
from pathlib import Path
from fractions import Fraction as Q
from functools import lru_cache
import hashlib, json, re, subprocess, datetime

SOURCE = Path('/Users/alec/Desktop/math')
OUT = Path(__file__).resolve().parent
PIN = 'adc7f1241b42e322a6451854ab7e4b4c146bf78a'
BASE = 'preprints/A-Fully-Polynomial-Randomized-Approximation-Scheme-for-Perfect-Matchings-in-General-Graphs-September-23-2026'
ENT = 'preprints/Entropy-and-Face-Dimension-of-the-Perfect-Matching-Polytope-September-23-2026'

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def uncomment(s):
    # Nested Lean block comments, line comments, and quoted strings.
    out=[]; i=0; depth=0
    while i<len(s):
        if depth:
            if s.startswith('/-',i): depth+=1; i+=2
            elif s.startswith('-/',i): depth-=1; i+=2
            else: out.append('\n' if s[i]=='\n' else ' '); i+=1
        elif s.startswith('/-',i): depth=1; i+=2
        elif s.startswith('--',i):
            j=s.find('\n',i); i=len(s) if j<0 else j
        elif s[i]=='"':
            out.append(' '); i+=1
            while i<len(s):
                if s[i]=='\\': i+=2
                elif s[i]=='"': i+=1; break
                else: out.append('\n' if s[i]=='\n' else ' '); i+=1
        else: out.append(s[i]); i+=1
    return ''.join(out)

def receipt():
    actual=subprocess.check_output(['git','rev-parse','HEAD'],cwd=SOURCE,text=True).strip()
    assert actual==PIN,(actual,PIN)
    todo=['OAI.Combinatorics.MatchingCount.Main']; seen={}; external=set(); missing=[]
    while todo:
        name=todo.pop()
        if name in seen: continue
        p=SOURCE/'lean'/Path(*name.split('.')).with_suffix('.lean')
        if not p.exists(): missing.append(name); continue
        raw=p.read_text(); clean=uncomment(raw)
        imports=[]
        for line in clean.splitlines():
            if line.strip().startswith('import '): imports+=line.strip()[7:].split()
        seen[name]={'path':str(p.relative_to(SOURCE)), 'sha256':sha(p), 'lines':len(raw.splitlines()),
                    'imports':imports, 'trust_hits':[{'line':clean[:m.start()].count('\n')+1,'token':m.group()}
                    for m in re.finditer(r'\b(?:sorry|admit|axiom|sorryAx|native_decide|unsafe|ofReduceBool|implemented_by|partial|opaque|run_tac|run_cmd)\b',clean)]}
        for imp in imports:
            if imp.startswith('OAI.'): todo.append(imp)
            else: external.add(imp)
    sources=[SOURCE/'README.md', SOURCE/BASE/'README.md', SOURCE/BASE/'build/main.tex', SOURCE/BASE/'main.pdf',
             SOURCE/'lean/docs/113.md', SOURCE/'lean/OAI/Combinatorics/MatchingCount/Model.lean',
             SOURCE/'lean/ComparatorChallenges/MatchingFPRAS.lean', SOURCE/'lean/lean-toolchain', SOURCE/'lean/lake-manifest.json',
             SOURCE/'lean/ComparatorChallenges/MatchingFPRAS.json',SOURCE/'lean/formalization.yaml',SOURCE/'lean/lakefile.lean']
    sources += list((SOURCE/ENT).rglob('*.tex')) + [SOURCE/ENT/'README.md',SOURCE/ENT/'main.pdf']
    metadata={str(p.relative_to(SOURCE)): {'sha256':sha(p),'bytes':p.stat().st_size} for p in sources if p.exists()}
    requested=dict(metadata)
    requested.update({v['path']:{'sha256':v['sha256']} for v in seen.values()})
    pinned=subprocess.run(['git','cat-file','--batch'],cwd=SOURCE,
                          input=''.join(f'{PIN}:{name}\n' for name in requested).encode(),capture_output=True,check=True)
    cursor=0; mismatches=[]
    for name,value in requested.items():
        stop=pinned.stdout.index(b'\n',cursor)
        fields=pinned.stdout[cursor:stop].decode().split()
        assert len(fields)==3 and fields[1]=='blob',(name,fields)
        size=int(fields[2]); data=pinned.stdout[stop+1:stop+1+size];cursor=stop+1+size+1
        if hashlib.sha256(data).hexdigest()!=value['sha256']:mismatches.append(name)
    assert not mismatches,mismatches
    trust={k:v['trust_hits'] for k,v in seen.items() if v['trust_hits']}
    return {'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pinned_commit':actual,
            'source_files':metadata,'lean_import_closure':seen,'external_imports':sorted(external),
            'missing_OAI_imports':missing,'trust_token_hits':trust,
            'pin_validation_basis':'Every read source hash compared to git cat-file blob at the exact pinned commit.',
            'pinned_blob_hash_mismatches':mismatches,'lean_closure_bytes':sum((SOURCE/v['path']).stat().st_size for v in seen.values()),
            'kernel_replay':False,'static_scan_only':True}

def all_matchings(vertices,weights):
    vertices=tuple(vertices)
    if not vertices: return [(frozenset(),Q(1))]
    u=vertices[0]; result=[]
    for v in vertices[1:]:
        e=tuple(sorted((u,v)))
        if e not in weights: continue
        remaining=tuple(x for x in vertices if x not in (u,v))
        for edges,w in all_matchings(remaining,weights): result.append((edges|{e},w*weights[e]))
    return result

def z(vertices,weights): return sum((w for _,w in all_matchings(vertices,weights)),Q(0))

def math_checks():
    # Four-hole identity inequality, including empty complement, using varied
    # nonuniform weights, zeros excluded as in the source logical graph.
    import itertools
    stats={'four_hole_cases':0,'broken_path_cases':0,'cell_identity_cases':0,'replica_residual_cases':0}
    for n in (4,6):
        es=list(itertools.combinations(range(n),2))
        for salt in range(6):
            w={e:Q(1+((17*e[0]+7*e[1]+salt*11)%13),1+((3*e[0]+e[1]+salt)%7)) for e in es}
            Z=z(range(n),w)
            def g(U): return z([x for x in range(n) if x not in U],w)/Z
            for U in itertools.combinations(range(n),4):
                a,b,c,d=U
                assert g(U)<=g((a,b))*g((c,d))+g((a,c))*g((b,d))+g((a,d))*g((b,c))
                stats['four_hole_cases']+=1
    # Reconstruct the source's two equal-pair path halves with a central
    # activity. Exhaust every internal deletion subset, and all endpoint
    # present/removed choices. Compare the SOURCE's F factors with forced
    # tiling weight divided by the even-edge baseline.
    for p in (1,2,3):
        q=4*p; center=2*p+1
        for lam in (Q(1,17),Q(1),Q(7,3)):
            B=max(Q(1),lam); Hu=B*2**(p-1); Hv=B*max(1,2**(p-2))
            t={}
            for r in range(1,p+1):
                t[2*r-1]=t[2*r]=max(B,Hu/Q(2**(r-1)))
                t[4*p+3-2*r]=t[4*p+2-2*r]=max(B,Hv/Q(2**(r-1)))
            t[center]=lam
            weights={(i-1,i):t[i] for i in range(1,q+2)}
            C0=Q(1)
            for i in range(2,q+1,2):C0*=t[i]
            def T(j):return t[j] if j<=2*p else t[j+1]
            # Formula requires innermost pairs equal B; test only profiles
            # meeting that condition, as stipulated in source p=2K+2.
            if t[2*p]!=B or t[2*p+2]!=B: continue
            for mask in range(1,1<<q):
                holes=[j for j in range(1,q+1) if mask>>(j-1)&1]
                consumed=[]; neutral=holes[:]
                F=Q(1)
                if holes[0]%2==0:
                    j=neutral.pop(0); consumed.append(0)
                    F*=1 if j<=2*p else lam/T(j)
                if neutral and holes[-1]%2==1:
                    j=neutral.pop(); consumed.append(q+1)
                    F*=1 if j>=2*p+1 else lam/T(j)
                valid=all((b-a)%2==1 for a,b in zip(holes,holes[1:])) and len(neutral)%2==0
                if valid:
                    for j,k in zip(neutral[::2],neutral[1::2]):
                        assert j%2==1 and k%2==0
                        F*=1/T(j) if k<=2*p else (1/T(k) if j>=2*p+1 else lam/(T(j)*T(k)))
                # Removing terminal endpoints corresponds to a completion
                # using only this broken path. Kept endpoints must equal
                # the consumed set. Other endpoints conceptually matched
                # elsewhere and are removed from this local induced path.
                for keep_left,keep_right in itertools.product((False,True),repeat=2):
                    verts=[j for j in range(1,q+1) if j not in holes]
                    if keep_left:verts.insert(0,0)
                    if keep_right:verts.append(q+1)
                    actual=z(verts,weights)
                    expected=C0*F if valid and {0 if keep_left else -1,q+1 if keep_right else -1}-{ -1}==set(consumed) else 0
                    assert actual==expected,(p,lam,holes,keep_left,keep_right,actual,expected)
                    stats['broken_path_cases']+=1
    # Signed cell identity: all four odd arcs (including short, long, and
    # length-three cases) on cycles 4..12, arbitrary independent f values.
    def edge(a,b):return tuple(sorted((a,b)))
    def val(M):return sum((17*a+7*b+3)**2 for a,b in M)+sum((a+1)*(b+3)*(c+5)*(d+7) for (a,b),(c,d) in itertools.combinations(sorted(M),2))
    for n in (4,6,8,10,12):
        O0=frozenset(edge(i,(i+1)%n) for i in range(0,n,2)); O1=frozenset(edge(i,(i+1)%n) for i in range(1,n,2))
        for corners in itertools.combinations(range(n),4):
            arcs=[]
            for a,b in zip(corners,corners[1:]+corners[:1]):
                ids=[a];u=a
                while u!=b:u=(u+1)%n;ids.append(u)
                if (len(ids)-1)%2==0:break
                T=frozenset(edge(ids[i],ids[i+1]) for i in range(0,len(ids)-1,2))
                C=frozenset(edge(ids[i],ids[i+1]) for i in range(1,len(ids)-1,2))|{edge(a,b)}
                arcs.append((T,C))
            if len(arcs)!=4:continue
            gains={}; errors={}; AP=[]
            for idx,O in enumerate((O0,O1)):
                pair=[j for j,(T,C) in enumerate(arcs) if T<=O]
                assert len(pair)==2
                current=O
                for j in pair:
                    T,C=arcs[j]; H=(O-T)|C
                    gains[j]=val(O)-val(H)
                    nxt=(current-T)|C
                    if current!=O:errors[idx]=val(current)-val(nxt)-gains[j]
                    current=nxt
                AP.append(current)
            DC=val(O0)-val(O1);Delta=val(AP[0])-val(AP[1])
            rhs=Delta+sum(gains[j] if arcs[j][0]<=O0 else -gains[j] for j in range(4))+errors.get(0,0)-errors.get(1,0)
            assert DC==rhs
            stats['cell_identity_cases']+=1
    # ANOVA residual assignment combinatorial claim: only a component's
    # last two slots can receive it, even when allowed pairs share a slot.
    for tiers in (2,3,4):
        for replicas in (1,2,3):
            slots=[(t,j) for t in reversed(range(tiers)) for j in range(replicas)]
            allowed=[(i,j) for i,x in enumerate(slots) for j,y in enumerate(slots) if x[0]==y[0]+1]
            for mask in range(1,1<<len(slots)):
                S={i for i in range(len(slots)) if mask>>i&1}
                charges=[(x,y) for x,y in allowed if x in S and y in S and S<=(set(range(x))|{x,y})]
                assert len(charges)<=1,(slots,S,charges)
                stats['replica_residual_cases']+=1
    stats['not_a_full_FPRAS_certificate']=True
    return stats

if __name__=='__main__':
    r=receipt();r['exact_finite_checks']=math_checks()
    (OUT/'PRIMARY_RECEIPTS.json').write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'OAI_import_modules':len(r['lean_import_closure']),'missing':r['missing_OAI_imports'],
                      'trust_hits':r['trust_token_hits'],'checks':r['exact_finite_checks'],'kernel_replay':False},indent=2))
