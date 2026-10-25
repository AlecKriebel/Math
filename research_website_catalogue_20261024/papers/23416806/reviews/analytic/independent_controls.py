import itertools,collections,json,time,hashlib
from pathlib import Path
START=time.time(); A='01'
def words(n): return [''.join(x) for x in itertools.product(A,repeat=n)]
def even(w):
    pos=[i for i,c in enumerate(w) if c=='0']
    return all((b-a-1)%2==0 for a,b in zip(pos,pos[1:]))
def gm(w): return '11' not in w
def alt(w): return all(a!=b for a,b in zip(w,w[1:]))
def local(w,n,allowed): return all(allowed(w[i:i+n]) for i in range(len(w)-n+1)) if len(w)>=n else allowed(w)
def profiles(w,k):
    left=k//2; right=k-left
    return [(w[max(0,i-left):i],w[i:min(len(w),i+right)]) for i in range(len(w))]
def join(u,v,pred,maxgap=12):
    for l in range(maxgap+1):
        for c in words(l):
            if pred(u+c+v): return u+c+v,c
    raise ValueError(('no bridge',u,v))
def even_step(state,c):
    # subsets of the two graph states E=0,O=1; all nonempty subsets accept
    ans=set()
    for s in state:
        if c=='1': ans.add(1-s)
        elif s==0: ans.add(0)
    return frozenset(ans)
def bad_even_shortest(n):
    vertices=[w for w in words(n-1) if even(w)]
    adjacency={v:[(v[1:]+c,c) for c in A if even(v+c)] for v in vertices}
    init=frozenset({0,1}); todo=collections.deque((v,init,'') for v in vertices)
    seen={(v,init) for v in vertices}
    while todo:
        v,s,w=todo.popleft()
        for z,c in adjacency[v]:
            t=even_step(s,c); nw=w+c
            if not t:return nw,len(seen)
            if (z,t) not in seen: seen.add((z,t));todo.append((z,t,nw))
    return None,len(seen)
def monoid(transforms):
    one=tuple(range(len(transforms[0]))); seen={one}; todo=[one]
    while todo:
        u=todo.pop()
        for v in transforms:
            z=tuple(v[u[i]] for i in range(len(u)))
            if z not in seen: seen.add(z);todo.append(z)
    return seen
checks=0; results={}
# Complete factor-language DFA and the identity bad language share the same monoid.
states=[frozenset({0,1}),frozenset({0}),frozenset({1}),frozenset()]
tr=[tuple(states.index(even_step(s,c)) for s in states) for c in A]
M=monoid(tr); results['even_identity_common_monoid']={'states':[sorted(s) for s in states],'letter_transformations':tr,'size':len(M),'k':4*(len(M)+1),'note':'Canonical graph at k is deliberately not materialized.'}
for l in range(13):
    for w in words(l):
        s=states[0]
        for c in w:s=even_step(s,c)
        if bool(s)!=even(w):raise AssertionError(('dfa',w))
        checks+=1
results['dfa_words_through_length']=12
# Check true ideal behavior independently with left and right padding.
ideal=0
for l in range(8):
    for w in words(l):
        if even(w):continue
        for a in ['','0','1','01','10']:
            for b in ['','0','1','01','10']:
                if even(a+w+b):raise AssertionError(('ideal',a,w,b))
                ideal+=1
results['bad_ideal_controls']=ideal
# Completion variation on the golden mean: ell=2. Output first letter except absent11.
completion=0
for l in range(2,13):
    for w in words(l):
        for missing in A:
            out=''.join((missing if w[i:i+2]=='11' else w[i]) for i in range(l-1))
            if gm(w) and out!=w[:-1]:raise AssertionError(('restriction',w,missing))
            if missing=='0' and not gm(out):raise AssertionError(('full_shift_image',w,out))
            completion+=1
results['golden_mean_completion_checks']=completion
results['golden_mean_completion_meaning']='11->0 maps full shift into golden mean;11->1 is identity and fails full-shift image inclusion. Both restrict to identity and succeed on T[2]=T.'
# Exact saturation-profile construction for even shift finite approximations.
saturation=[]
for n in range(2,6):
    targets=[w for w in words(n) if even(w)]
    U=targets[0]
    for v in targets[1:]:U,_=join(U,v,even,4)
    while len(U)<2*n:U,_=join(U,targets[0],even,4)
    m=n-1 if (n-1)%2 else n
    w='0'+'1'*m+'0'
    if even(w) or not local(w,n,even):raise AssertionError(('bad witness',n,w))
    W,_=join(U,w,lambda z:local(z,n,even),2*n)
    W,_=join(W,U,lambda z:local(z,n,even),2*n)
    V,_=join(U,U,even,4)
    for k in range(2,n+1):
        if set(profiles(V,k))!=set(profiles(W,k)):raise AssertionError(('profiles',n,k))
        if even(W) or not even(V):raise AssertionError(('membership',n))
        saturation.append({'n':n,'k':k,'U':U,'V':V,'W':W,'bad_word':w,'profile_set_size':len(set(profiles(V,k))),'profile_multisets_equal':collections.Counter(profiles(V,k))==collections.Counter(profiles(W,k))})
results['saturation_profile_pairs']=saturation
results['all_path_negative_controls']=[]
for n in range(2,9):
    w,size=bad_even_shortest(n)
    if w is None or even(w) or not local(w,n,even) or len(w)<=n:raise AssertionError(('reachability',n,w))
    results['all_path_negative_controls'].append({'n':n,'shortest_bad_path_word':w,'length':len(w),'states_explored':size})
# Every finite periodic approximation witness is genuine and this formula proves it for all n.
periodic=[]
for n in range(2,31):
    m=n-1 if (n-1)%2 else n; cycle='0'+'1'*m; z=cycle*4
    if any(not even(z[i:i+n]) for i in range(len(z)-n+1)):raise AssertionError(('periodic',n))
    periodic.append({'n':n,'odd_gap':m,'period':len(cycle)})
results['periodic_even_shift_controls']=periodic
# Irreducible but nonmixing period2 is already SFT and the all-vertex graph has both cycles.
for n in range(2,9):
    vs=[w for w in words(n-1) if alt(w)]
    if len(vs)!=2:raise AssertionError(('period2 vertices',n))
    for v in vs:
        successors=[v[1:]+c for c in A if alt(v+c)]
        if len(successors)!=1 or successors[0] not in vs:raise AssertionError(('period2 graph',n))
    checks+=1
results['onto_boundary']='Constant output0 maps full binary shift into even shift but image={0^Z}, strictly smaller. This is excluded by onto self-code hypothesis.'
results['reducible_boundary']='For T={0^Z,1^Z}, no word in Lang(T) contains both 0^n and1^n; irreducible saturation construction fails. No reducible extension theorem is inferred.'
results['base_checks']=checks
results['elapsed_seconds']=time.time()-START
results['status']='All explicit checks passed; finite controls supplement the universal proof and do not establish it.'
Path(__file__).with_name('INDEPENDENT_CONTROL_RESULTS.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps({'status':results['status'],'elapsed_seconds':results['elapsed_seconds'],'dfa_and_periodic_graph_checks':checks,'ideal_controls':ideal,'completion_controls':completion,'profile_pairs':len(saturation),'monoid_size':len(M)}))
