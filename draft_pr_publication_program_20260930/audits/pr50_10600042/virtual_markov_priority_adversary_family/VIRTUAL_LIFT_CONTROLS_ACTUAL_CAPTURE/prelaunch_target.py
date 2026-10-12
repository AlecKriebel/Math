"""Independent bounded exact virtual-word and closure-invariant controls.
No candidate import, braid equality oracle, or claim to reprove Kamada's theorem.
"""
from pathlib import Path
from itertools import product, permutations
import datetime as dt, hashlib, json, os
F=Path(__file__).absolute().parent;tests=0;coverage={};counterexamples={}
def test(v,n):
    global tests
    if not v:raise ValueError(n)
    tests+=1
def S(i,e=1):return ('s',i,e)
def V(i):return ('v',i,1)
def inv(w):return tuple((t,i,-e if t=='s' else 1) for t,i,e in reversed(w))
def shift(w):return tuple((t,i+1,e) for t,i,e in w)
def good(n,w):return n>=1 and all(t in ('s','v') and 1<=i<n and ((t=='v' and e==1) or (t=='s' and e in (-1,1))) for t,i,e in w)
def supported(w,k):return all(1<=i<=k for _,i,_ in w)
def pad(n,w):return (n,w) if n%2==0 else (n+1,w+(S(n),))
def invariant(n,w):
    # Classical crossing signs grouped by ordered pairs of distinct closure components.
    labels=list(range(n));cross=[]
    for t,i,e in w:
        a,b=labels[i-1],labels[i]
        if t=='s':cross.append((a,b,e) if e==1 else (b,a,e))
        labels[i-1],labels[i]=b,a
    components=[None]*n;count=0
    for start in range(n):
        if components[start] is not None:continue
        k=start
        while components[k] is None:components[k]=count;k=labels[k]
        count+=1
    matrix=[[0]*count for _ in range(count)]
    for a,b,e in cross:
        ca,cb=components[a],components[b]
        if ca!=cb:matrix[ca][cb]+=e
    # Exact comparison independent of component labels, used only for <=4 components.
    key=min(tuple(matrix[i][j] for i in p for j in p) for p in permutations(range(count))) if count<=4 else None
    return dict(component_count=count,ordered_linking_matrix=matrix,unlabelled_matrix_key=key)
def words(k):
    alphabet=[S(i,e) for i in range(1,k+1) for e in (-1,1)]+[V(i) for i in range(1,k+1)]
    # Compact deterministic set: all letters and mixed two-letter boundary-support blocks.
    return [()]+[(x,) for x in alphabet]+[(x,y) for x in alphabet for y in alphabet if x[1]==k or y[1]==k]
def verify_edge(kind,n,a,b,g=None):
    if kind=='conj':old=[(n,b),(n,a+b+inv(a))]
    elif kind=='stab':old=[(n,b),(n+1,b+(g,))]
    elif kind=='right':old=[(n,a+(S(n-1,-1),)+b+(S(n-1),)),(n,a+(V(n-1),)+b+(V(n-1),))]
    elif kind=='left':old=[(n,shift(a)+(S(1,-1),)+shift(b)+(S(1),)),(n,shift(a)+(V(1),)+shift(b)+(V(1),))]
    actual=[pad(*x) for x in old];N=n+n%2
    if kind=='conj':name='C' if n%2==0 else 'BC';tail=() if n%2==0 else (S(N-1),);expected=[(N,b+tail),(N,a+b+inv(a)+tail)];bound=N-1 if name=='C' else N-2
    elif kind=='stab':
        name='D' if n%2==0 else 'T';bound=N-1 if name=='D' else N-2
        expected=[(N,b),(N+2,b+(g,S(N+1)))] if name=='D' else [(N,b+(S(N-1),)),(N,b+(g,))]
    else:
        name=('R' if kind=='right' else 'L') if n%2==0 else ('BR' if kind=='right' else 'BL');bound=N-2 if n%2==0 else N-3;tail=() if n%2==0 else (S(N-1),);aa,bb=(a,b) if kind=='right' else (shift(a),shift(b));i=(N-1 if n%2==0 else N-2) if kind=='right' else 1;expected=[(N,aa+(S(i,-1),)+bb+(S(i),)+tail),(N,aa+(V(i),)+bb+(V(i),)+tail)]
    test(supported(a+b,bound),'support '+name);test(all(good(*x) for x in old+actual),'valid tags/indices');test(actual==expected,'independently computed literal '+name);test(actual[::-1]==expected[::-1],'reverse '+name);test(all(x[0]%2==0 for x in actual),'parity');test(max(x[0] for x in actual)==2*((max(x[0] for x in old)+1)//2),'height')
    test(all(invariant(*x)['component_count']==invariant(*pad(*x))['component_count'] for x in old),'positive pad joins component');coverage[name]=coverage.get(name,0)+1
def main():
    for n in range(1,7):
        blocks=words(n-1)
        for a in blocks:
            b=inv(a)+(V(1),) if n>1 else ()
            verify_edge('conj',n,a,b)
            for g in [S(n),S(n,-1),V(n)]:verify_edge('stab',n,(),a,g)
        if n>=2:
            ws=words(n-2)
            for a in ws:
                for b in ws[:min(len(ws),10)]:verify_edge('right',n,a,b);verify_edge('left',n,a,b)
    # Every defining relation family from Kamada §2; arbitrary contexts are handled in proof.
    relation_counts={}
    for n in range(2,7):
        pairs=[]
        for i in range(1,n):pairs.extend([('inverse+', (S(i),S(i,-1)),()),('inverse-',(S(i,-1),S(i)),()),('virtual_square',(V(i),V(i)),())])
        for i in range(1,n-1):pairs.extend([('classical_braid',(S(i),S(i+1),S(i)),(S(i+1),S(i),S(i+1))),('virtual_braid',(V(i),V(i+1),V(i)),(V(i+1),V(i),V(i+1))),('mixed_detour',(S(i),V(i+1),V(i)),(V(i+1),V(i),S(i+1)))])
        for i in range(1,n):
            for j in range(i+2,n):pairs.extend([('classical_far',(S(i),S(j)),(S(j),S(i))),('virtual_far',(V(i),V(j)),(V(j),V(i))),('mixed_far',(S(i),V(j)),(V(j),S(i)))])
        pre=(V(n-1),);post=(S(n-1,-1),)
        for name,lhs,rhs in pairs:
            x,y=pad(n,pre+lhs+post),pad(n,pre+rhs+post);tail=(S(n),) if n%2 else ();test(x==(n+n%2,pre+lhs+post+tail) and y==(n+n%2,pre+rhs+post+tail),'context relation tail');test(good(*x) and good(*y) and x[0]%2==0,'relation indices');test(invariant(*x)['component_count']==invariant(*y)['component_count'],'relation component sanity');relation_counts[name]=relation_counts.get(name,0)+1
    test(set(coverage)=={'C','BC','T','D','R','L','BR','BL'},'all edge families');test(pad(1,())==(2,(S(1),)),'one-strand unknot');test(pad(2,())==(2,()) and invariant(2,())['component_count']==2 and invariant(4,())['component_count']==4,'tags essential')
    naive=[invariant(1,()),invariant(2,())];test(naive[0]['component_count']!=naive[1]['component_count'],'plain inclusion adds component');counterexamples['naive_trivial_padding']=dict(before=naive[0],after=naive[1])
    badT=[invariant(2,(S(1),S(1))),invariant(2,())];test(badT[0]['unlabelled_matrix_key']!=badT[1]['unlabelled_matrix_key'],'T wrong support changes Hopf to unlink');counterexamples['T_if_block_uses_terminal_strand']=dict(block=[S(1)],left=badT[0],right=badT[1],proper_support_bound=0)
    for name,n,w1,w2,bound in [('R',2,(S(1),S(1)),(S(1),V(1),S(1),V(1)),0),('BR',4,(S(2),S(2),S(3)),(S(2),V(2),S(2),V(2),S(3)),1)]:
        a,b=invariant(n,w1),invariant(n,w2);test(a['component_count']==b['component_count'] and a['unlabelled_matrix_key']!=b['unlabelled_matrix_key'],'wrong-support exchange invariant '+name);counterexamples[name+'_without_support']=dict(strands=n,left_word=w1,right_word=w2,left=a,right=b,proper_block_support_bound=bound)
    # Search a compact explicit wrong-support buffered LEFT exchange witness.
    found=None
    for a in words(2):
        for b in words(2):
            if supported(a+b,1):continue
            left=shift(a)+(S(1,-1),)+shift(b)+(S(1),S(3));right=shift(a)+(V(1),)+shift(b)+(V(1),S(3));x,y=invariant(4,left),invariant(4,right)
            if x['unlabelled_matrix_key']!=y['unlabelled_matrix_key']:
                found=dict(strands=4,a=a,b=b,left_word=left,right_word=right,left=x,right=y,proper_unshifted_block_support_bound=1);break
        if found:break
    # Lack of a finite witness would not prove broader support sound.
    counterexamples['BL_enlarged_support_search']=dict(witness=found,finite_search_only=True)
    result=dict(schema='pr50-independent-virtual-lift-controls/v1',status='PASS_BOUNDED_EXACT_VIRTUAL_LIFT_CONTROLS',actual_pid=os.getpid(),created_utc=dt.datetime.now(dt.timezone.utc).isoformat(),assertions=tests,edge_cases=sum(coverage.values()),coverage=coverage,defining_relation_counts=relation_counts,counterexamples=counterexamples,unrestricted_Markov_theorem_reproved=False,link_equivalence_oracle_used=False,braid_word_problem_solved=False,novelty_established=False,limits='Word/index controls and necessary closure invariants supplement the universal theorem deduction. No finite test proves full Markov completeness.')
    with (F/'CONTROL_RESULT.json').open('xb') as h:h.write((json.dumps(result,indent=2,allow_nan=False)+'\n').encode())
    print(json.dumps(result,sort_keys=True))
if __name__=='__main__':main()
