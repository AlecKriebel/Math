"""Independent exact audit controls. Imports none of the frozen author code.
These falsification/reproducibility controls do not prove universal equalities.
"""
import json
from collections import Counter
from itertools import product
import sympy as S

INV = dict(zip('aAbB','AaBb'))
def reduce_cyclic(w):
    s=[]
    for c in w:
        if s and INV[c]==s[-1]:s.pop()
        else:s.append(c)
    while len(s)>1 and INV[s[0]]==s[-1]:s=s[1:-1]
    return ''.join(s)
def plus(p,q,scale=1):
    d=p.copy()
    for e,c in q.items():d[e]=d.get(e,0)+scale*c
    return {e:c for e,c in d.items() if c}
def times_scalar(p,c):return {e:c*v for e,v in p.items() if c*v}
def shift(p,e):return {k+e:v for k,v in p.items()}
def append(M,c):
    # A flat 2x2 matrix; right multiplication is evaluated column by column.
    m,n,p,q=M
    if c=='a':return (plus(times_scalar(m,2),n),plus(m,n),plus(times_scalar(p,2),q),plus(p,q))
    if c=='A':return (plus(m,n,-1),plus(times_scalar(n,2),m,-1),plus(p,q,-1),plus(times_scalar(q,2),p,-1))
    if c=='b':return (shift(m,1),shift(n,-1),shift(p,1),shift(q,-1))
    if c=='B':return (shift(m,-1),shift(n,1),shift(p,-1),shift(q,1))
    raise ValueError(c)
def identity():return ({0:1},{},{},{0:1})
def check_counts():
    counts=Counter(); examples=[]
    swap=dict(zip('aAbB','bBaA'))
    def visit(w,M,N):
        r=reduce_cyclic(w)
        for generator,mat in [('b',M),('a',N)]:
            trace=plus(plus(mat[0],mat[3]),{0:1})
            got=max(trace)
            expected=sum(c.lower()==generator for c in r)
            assert got==expected,(w,r,generator,got,expected)
            counts['degree_checks']+=1
        counts['freely_reduced_words']+=1
        if w!=r:counts['noncyclically_reduced_words']+=1
        if len(w)==9:return
        for c in 'aAbB':
            if not w or c!=INV[w[-1]]:visit(w+c,append(M,c),append(N,swap[c]))
    visit('',identity(),identity())
    # Deliberate ordinary cancellation, cyclic cancellation, pure powers,
    # identity and longer block exponents absent from author's finite box.
    words=['aAbB','abBA','a'*17+'b'*9+'A'*17,
           'a'*23+'B'*11+'A'*23,'abAB','a'*41,'B'*37,
           'a'*31+'b'*13+'A'*7+'B'*19,
           'b'*3+'a'*8+'B'*3]
    for w in words:
        M=identity();N=identity()
        for c in w:M=append(M,c);N=append(N,swap[c])
        r=reduce_cyclic(w)
        degs=[]
        for generator,mat in [('b',M),('a',N)]:
            trace=plus(plus(mat[0],mat[3]),{0:1});got=max(trace)
            assert got==sum(c.lower()==generator for c in r)
            degs.append(got)
        examples.append({'word':w,'cyclic_reduction':r,'degrees_b_a':degs})
    return dict(counts),examples

def core_algebra():
    a,b,c,d,e,f,g,h=S.symbols('a b c d e f g h')
    delta=a*e-b*d
    i=(1-b*f*g-c*d*h+c*e*g+a*f*h)/delta
    M=S.Matrix([[a,b,c],[d,e,f],[g,h,i]])
    L=S.Matrix([[1,0,0],[d/a,1,0],[g/a,(a*h-b*g)/delta,1]])
    D=S.diag(a,delta/a,1/delta)
    U=S.Matrix([[1,b/a,c/a],[0,1,(a*f-c*d)/delta],[0,0,1]])
    assert all(S.cancel(x)==0 for x in L*D*U-M)
    assert S.cancel(M.det())==1
    # Same individual scalar trace but different inverse trace and charpoly.
    T=S.symbols('T')
    X=S.Matrix([[0,0,1],[1,0,-2],[0,1,3]])
    Y=S.eye(3)
    assert X.det()==Y.det()==1 and S.trace(X)==S.trace(Y)==3
    assert S.trace(X.inv())==2 and S.trace(Y.inv())==3
    assert X.charpoly(T).as_expr()!=Y.charpoly(T).as_expr()
    A=S.Matrix([[1,2,0],[0,1,1],[0,0,1]])
    B=S.Matrix([[1,0,0],[1,1,0],[2,1,1]])
    def evalword(w,P,Q):
        maps={'a':P,'A':P.inv(),'b':Q,'B':Q.inv()};m=S.eye(3)
        for c in w:m=m*maps[c]
        return m
    words=['','a','A','abAB','aaBab','bABaBa']
    for w in words:
        assert evalword(w,A.inv().T,B.inv().T)==evalword(w,A,B).inv().T
    assert evalword('ab',A.inv(),B.inv())!=evalword('ab',A,B).inv()
    # Signed GL3 scalar factors, including negative abelianization.
    for w in words:
        ea=w.count('a')-w.count('A');eb=w.count('b')-w.count('B')
        assert evalword(w,2*A,3*B)==S.Rational(2)**ea*S.Rational(3)**eb*evalword(w,A,B)
    # Commuting matrices miss nontrivial commutators.
    Xd=S.diag(2,3,S.Rational(1,6));Yd=S.diag(5,7,S.Rational(1,35))
    assert S.trace(evalword('abAB',Xd,Yd))==3
    assert S.trace(evalword('abAB',A,B))!=3
    # An exact independent separation of the source's length-12 candidate.
    u,v='aababbaabbab','aababbabaabb'
    tu,tv=S.trace(evalword(u,A,B)),S.trace(evalword(v,A,B))
    assert tu!=tv
    assert all(v!=u[k:]+u[:k] for k in range(len(u)))
    return {'generic_cell_inverse_parameterization':'PASS','actual_pivots':['s','t','1/(s*t)'],'leading_minors':['s','s*t'],
            'same_scalar_trace_counterexample':{'X':X.tolist(),'Y':Y.tolist(),'traces':[3,3],'inverse_traces':[2,3]},
            'contragredient_word_controls':len(words),'plain_inversion_is_not_word_homomorphism':'verified',
            'scalar_GL3_controls':len(words),'diagonal_commutator_false_positive':'verified',
            'independent_candidate_refutation':{'A':A.tolist(),'B':B.tolist(),'traces':[tu,tv],'difference':tu-tv}}

def signed_exponent_controls():
    # Integer Laurent coefficient signatures, including zero and negative p.
    seen={}
    for p in range(-100,101):
        sig=Counter({(p,0):1})
        sig[(0,p)]+=1;sig[(-p,-p)]+=1
        key=tuple(sorted(sig.items()))
        assert key not in seen or seen[key]==p
        seen[key]=p
    return len(seen)

if __name__=='__main__':
    counts,examples=check_counts()
    result={'status':'PASS','audit_controls_not_universal_identity_certificates':True,
            'unsigned_counts':counts,'adversarial_count_examples':examples,
            'signed_exponent_sum_signatures':signed_exponent_controls(),'core_algebra':core_algebra()}
    print(json.dumps(result,indent=2,default=str))
