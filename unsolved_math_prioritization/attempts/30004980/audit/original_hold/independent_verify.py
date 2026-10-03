#!/usr/bin/env python3
"""Audit-only checks; Python 3.10+ standard library.
Usage: python independent_verify.py /path/to/author [--full]
No author file is modified. Independent oracle uses trigraph matrices, not
original-graph bit-mask partitions. --full compares author's exact DP on every
labeled graph through six; default exact comparison is exhaustive through five
plus a seed-fixed 256-graph sample of order six.
"""
import argparse, functools, hashlib, importlib.util, itertools, json, pathlib, random, sys, time
C = itertools.combinations

def require(test, message):
    if not test:
        raise RuntimeError(message)

def matrix(n, code):
    rows = [[0]*n for _ in range(n)]
    for bit, (i,j) in enumerate(C(range(n),2)):
        rows[i][j] = rows[j][i] = (code >> bit) & 1
    return tuple(map(tuple,rows))

def peak(state):
    return max((row.count(2) for row in state), default=0)

def contract(state, x, y):
    rem = [i for i in range(len(state)) if i not in (x,y)]
    rows = [list(state[i][j] for j in rem) for i in rem]
    last = []
    for k,i in enumerate(rem):
        a,b = state[x][i],state[y][i]
        value = a if a == b and a != 2 else 2
        rows[k].append(value); last.append(value)
    last.append(0); rows.append(last)
    return tuple(map(tuple, rows))

def exact_oracle(initial):
    # Independent threshold decision search over every current pair.
    for bound in range(max(1,len(initial))):
        @functools.lru_cache(None)
        def feasible(state):
            if peak(state) > bound: return False
            if len(state) <= bound+1: return True
            return any(feasible(contract(state,i,j)) for i,j in C(range(len(state)),2))
        if feasible(initial): return bound
    raise RuntimeError('No trivial upper bound found')

def quotient(g, parts):
    rows = [[0]*len(parts) for _ in parts]
    for i,j in C(range(len(parts)),2):
        colors = {g[u][v] for u in parts[i] for v in parts[j]}
        value = next(iter(colors)) if len(colors)==1 else 2
        rows[i][j]=rows[j][i]=value
    return tuple(map(tuple,rows))

def verify_sequence(g, seq, bound):
    state = g
    labels = [frozenset([i]) for i in range(len(g))]
    top = peak(state)
    for first,second in seq:
        a = frozenset(i for i in range(len(g)) if first & (1<<i))
        b = frozenset(i for i in range(len(g)) if second & (1<<i))
        require(a in labels and b in labels and a!=b, 'Invalid certificate merge')
        x,y = labels.index(a),labels.index(b)
        state = contract(state,x,y)
        labels = [v for v in labels if v!=a and v!=b]+[a|b]
        require(state == quotient(g,labels), 'Incremental/quotient disagreement')
        top = max(top,peak(state))
    while len(state)>1:
        state=contract(state,0,1); top=max(top,peak(state))
    require(top<=bound, 'Certificate exceeds bound')
    return top

def disagreement(g,a,b):
    return {v for v in range(len(g)) if v not in (a,b) and g[v][a]!=g[v][b]}

def pair_identities(g):
    n=len(g); pairs=[(i,i+1) for i in range(0,n-1,2)]
    base=[len(disagreement(g,*p)) for p in pairs]
    dis=[disagreement(g,*p) for p in pairs]
    for selected in range(1<<len(pairs)):
        s=[i for i in range(len(pairs)) if selected>>i&1]
        merged={v for i in s for v in pairs[i]}
        parts=[set(pairs[i]) for i in s]+[{v} for v in range(n) if v not in merged]
        q=quotient(g,parts)
        for pos,i in enumerate(s):
            expected=base[i]
            for j in s:
                if i==j: continue
                vals={g[u][v] for u in pairs[i] for v in pairs[j]}
                expected+=int(len(vals)>1)-len(dis[i]&set(pairs[j]))
            require(q[pos].count(2)==expected,'Pair identity fails')
    perm=[i^1 if i<n//2*2 else i for i in range(n)]
    if all(g[u][v]==g[perm[u]][perm[v]] for u,v in C(range(n),2)):
        # Explicit empty maximum convention for the audit's formulation.
        bound=max(max(base,default=0),len(pairs)+(n%2)-1)
        seq=[(1<<a,1<<b) for a,b in pairs]
        verify_sequence(g,seq,bound)
        return 1
    return 0

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('author',type=pathlib.Path); parser.add_argument('--full',action='store_true');args=parser.parse_args()
    root=args.author.resolve(); start=time.monotonic()
    manifest=json.loads((root/'MANIFEST.json').read_text())
    before={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob('*') if p.is_file()}
    for f in manifest['files']:
        data=(root/f['path']).read_bytes();require(len(data)==f['bytes'] and hashlib.sha256(data).hexdigest()==f['sha256'],'Manifest mismatch: '+f['path'])
    require(len(before)==17,'Unexpected frozen file count')
    # Disable bytecode so importing the source is genuinely read-only.
    sys.dont_write_bytecode=True
    spec=importlib.util.spec_from_file_location('author_twinwidth',root/'checks/twinwidth.py');author=importlib.util.module_from_spec(spec);spec.loader.exec_module(author)
    out={'frozen_manifest_sha256':before['MANIFEST.json'],'graph_counts':{},'independent_exact_maxima':[], 'author_exact_comparisons':0,'pair_formula_graph_checks':0,'involution_graph_checks':0}
    rng=random.Random(30004980); chosen=set(rng.sample(range(1<<15),256))
    for n in range(1,7):
        maximum=0; hist={}
        for code in range(1<<(n*(n-1)//2)):
            g=matrix(n,code); adj=tuple(sum(g[u][v]<<v for v in range(n)) for u in range(n))
            require(author.graph(n,code)==adj,'Graph decoder mismatch')
            value=exact_oracle(g); maximum=max(maximum,value);hist[value]=hist.get(value,0)+1
            sequence=author.pair_only(adj,0 if n<=3 else (n-1)//2)
            require(sequence is not None,'Missing pair-first certificate')
            verify_sequence(g,sequence,0 if n<=3 else (n-1)//2)
            if n<=5 or args.full or code in chosen:
                av,aseq=author.exact(adj);require(av==value,'Exact solver disagrees');verify_sequence(g,aseq,av);out['author_exact_comparisons']+=1
            if n>=2:
                dist=sum(len(disagreement(g,u,v)) for u,v in C(range(n),2));deg=[sum(row) for row in g]
                require(dist==sum(d*(n-1-d) for d in deg),'Degree identity fails')
                # Clear denominators in the exact degree-defect identity.
                require(4*dist==n*(n-1)**2-sum((2*d-(n-1))**2 for d in deg),'Defect identity fails')
            out['involution_graph_checks']+=pair_identities(g);out['pair_formula_graph_checks']+=1
        out['graph_counts'][n]={'count':sum(hist.values()),'exact_distribution':hist};out['independent_exact_maxima'].append(maximum)
        print('Completed order',n,'maximum',maximum,'distribution',hist,flush=True)
    require(out['independent_exact_maxima']==[0,0,0,1,2,2],'Maxima disagree')
    rng=random.Random(481); samples=0
    for n in range(7,13):
        for _ in range(250):
            g=matrix(n,rng.getrandbits(n*(n-1)//2));adj=tuple(sum(g[u][v]<<v for v in range(n)) for u in range(n)); seq=author.pair_only(adj,(n-1)//2)
            require(seq is not None,'Missing sampled certificate');verify_sequence(g,seq,(n-1)//2);samples+=1
    out['sample_certificates_verified']=samples
    # Exhaust all 16 possible cross-pair rectangles and check the unsafe type.
    rectangle_classes={}
    for bits in itertools.product((0,1),repeat=4):
        a,b,c,d=bits;nonconstant=int(len(set(bits))>1)
        updates=(nonconstant-(a!=c)-(b!=d),nonconstant-(a!=b)-(c!=d))
        bad=updates in ((1,-1),(-1,1))
        equal_nonconstant=(a==c and b==d and a!=b) or (a==b and c==d and a!=c)
        require(bad==equal_nonconstant,'Rectangle class fails');rectangle_classes[str(updates)]=rectangle_classes.get(str(updates),0)+1
    out['sixteen_rectangle_update_counts']=rectangle_classes
    # Adversarial literal reading of the frozen prose, not the corrected formula.
    k2=matrix(2,1);literal={v for v in range(2) if k2[v][0]!=k2[v][1]}
    require(len(literal)==2 and peak(contract(k2,0,1))==0,'Expected text counterexample absent')
    out['literal_attempt2_definition_counterexample']={'graph':'K2','literal_D_size':2,'actual_red_degree':0}
    # Net obstruction and named lower witnesses independently decoded.
    edges=[(0,3),(1,3),(2,5),(3,5),(1,4),(1,5)];g=[[0]*6 for _ in range(6)]
    for u,v in edges:g[u][v]=g[v][u]=1
    g=tuple(map(tuple,g));require(exact_oracle(g)==2,'Net exact width fails')
    profiles=[];pairs=[(0,1),(2,3),(4,5)]
    for order in itertools.permutations(range(3)):
        selected=[];profile=[]
        for j in order:
            selected.append(j);used={v for i in selected for v in pairs[i]}
            parts=[set(pairs[i]) for i in selected]+[{v} for v in range(6) if v not in used]
            profile.append(peak(quotient(g,parts)))
        require(profile==[2,3,2],'Bad matching profile fails');profiles.append(profile)
    out['net_bad_orders_verified']=len(profiles)
    out['lower_witnesses']={}
    for n,edges in [(4,[(0,1),(1,2),(2,3)]),(5,[(i,(i+1)%5) for i in range(5)]),(6,[(i,(i+1)%5) for i in range(5)])]:
        g=[[0]*n for _ in range(n)]
        for u,v in edges:g[u][v]=g[v][u]=1
        low=min(len(disagreement(g,u,v)) for u,v in C(range(n),2));require(low==(1 if n==4 else 2),'Lower witness fails');out['lower_witnesses'][n]=low
    after={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob('*') if p.is_file()}
    require(before==after,'Author package changed during verification')
    out['seconds']=time.monotonic()-start;out['all_computational_checks_passed']=True
    target=pathlib.Path(__file__).with_name('independent_results.json');target.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
