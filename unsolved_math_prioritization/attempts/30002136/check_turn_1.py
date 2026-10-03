"""Exact sanity checks for the accompanying proofs; not a full-target solver."""
import json
import sympy as S

def canonical(w):
    return min(w[i:]+w[:i] for i in range(len(w))) if w else ''

def word_matrix(w, A, B):
    d={'a':A,'b':B,'A':A.inv(),'B':B.inv()}
    out=S.eye(3)
    for c in w:
        out=out*d[c]
    return out

def run():
    l21,l31,l32,u12,u13,u23,s,t=S.symbols('l21 l31 l32 u12 u13 u23 s t', nonzero=True)
    z=S.symbols('z')
    L=S.Matrix([[1,0,0],[l21,1,0],[l31,l32,1]])
    U=S.Matrix([[1,u12,u13],[0,1,u23],[0,0,1]])
    D=S.diag(s,t,1/(s*t)); M=L*D*U
    assert S.simplify(M.det()-1)==0
    assert S.simplify(M[:2,:2].det()-s*t)==0
    assert (M*(U.inv()*D.inv()*L.inv())-S.eye(3)).applyfunc(S.simplify)==S.zeros(3)
    assert S.simplify(M.charpoly(z).as_expr()-(z**3-S.trace(M)*z**2+S.trace(M.inv())*z-1))==0
    A=S.Matrix([[1,1,0],[0,1,1],[0,0,1]])
    B=S.Matrix([[1,0,0],[1,1,0],[1,1,1]])
    u,v='aababbaabbab','aababbabaabb'
    assert A.det()==B.det()==1 and canonical(u)!=canonical(v)
    tu,tv=map(lambda w: int(S.trace(word_matrix(w,A,B))),(u,v))
    assert (tu,tv)==(2187,2180)
    result={'status':'PASS','scope':'algebraic sanity checks and one exact rejected candidate; no full resolution',
            'pair':[u,v],'A':[[int(x) for x in row] for row in A.tolist()],'B':[[int(x) for x in row] for row in B.tolist()],
            'traces':[tu,tv],'difference':tu-tv,'nonconjugate':True,
            'gaussian_cell_determinant_and_inverse':True,'characteristic_polynomial_formula':True}
    return result

if __name__=='__main__':
    print(json.dumps(run(),indent=2))
