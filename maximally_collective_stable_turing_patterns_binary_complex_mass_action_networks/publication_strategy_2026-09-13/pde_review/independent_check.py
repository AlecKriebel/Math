"""Bounded exact checks rebuilt directly from the listed reactions.

No imports from the project's implementations. Finite-dimensional checks are
falsification probes and do not replace the manuscript's all-dimensional proof.
"""
import json
from pathlib import Path
import sympy as s
import numpy as np

Q = s.Rational

def check(m):
    n = m + 1
    x = s.Matrix(s.symbols(f'x0:{n}'))
    f = s.zeros(n, 1)
    def reaction(source, product):
        nonlocal f
        y = s.zeros(n, 1)
        yp = s.zeros(n, 1)
        for i, count in source.items():
            y[i] = count
        for i, count in product.items():
            yp[i] = count
        rate = s.prod(x[i] ** y[i] for i in range(n))
        f += (yp - y) * rate
    reaction({}, {0: 1})
    for i in range(1, m-2):
        reaction({0: 1, i: 1}, {0: 1, i+1: 1})
    reaction({0: 1, m-2: 1}, {m-1: 2})
    reaction({m-1: 2}, {1: 1})
    reaction({m: 2}, {0: 1, m-1: 1})
    reaction({0: 1, m-1: 1}, {m: 2})
    A = f.jacobian(x).subs(dict.fromkeys(x, 1))
    Bm = [s.hessian(fi, x) for fi in f]
    def B(u, v):
        return s.Matrix([(u.T * h * v)[0] for h in Bm])
    K = lambda i: 91*m-181-i
    c = s.Matrix([0] + [4]*(m-2) + [2, 1])
    r = s.Matrix([1]+[-Q(K(i),63*(m-2)) for i in range(2,m)]+[-Q(2,9),Q(5,14)])
    ell = s.Matrix([-Q(266,815)]+[Q(78260*(m-2),163*K(i-1)) for i in range(2,m)]+[Q(18368,7335),1])
    D = s.diag(Q(23,63),*[1/s.Integer(K(i)) for i in range(2,m)],Q(1,7),Q(16,45))
    assert f.subs(dict.fromkeys(x,1)) == s.zeros(n,1)
    assert c.T*A == s.zeros(1,n)
    assert (A-D)*r == s.zeros(n,1)
    assert ell.T*(A-D) == s.zeros(1,n)
    rhs = -B(r,r)/4
    w2 = (A-4*D).inv()*rhs
    rows=[]
    for L in [None, Q(4,5), Q(9,10)]:
        H = s.eye(n) if L is None else s.diag(1,*[Q(K(i),K(i-1))/L for i in range(2,m)],1,1)
        gauge = H.inv()*c
        w0 = A.col_join(gauge.T).gauss_jordan_solve(rhs.col_join(s.zeros(1,1)))[0]
        left = H.inv()*ell
        denominator = (left.T*r)[0]
        eta = (ell.T*D*r)[0]/denominator
        cubic = (ell.T*(B(r,w0)+B(r,w2)/2))[0]/denominator
        assert eta > 0 and cubic < 0
        eigens = {}
        for k in [0,1,2,3,10]:
            eigenvalues = np.linalg.eigvals(np.array(H*(A-k*k*D),dtype=float))
            if k <= 1:
                assert min(abs(eigenvalues)) < 1e-10
                eigenvalues=np.delete(eigenvalues,np.argmin(abs(eigenvalues)))
            assert max(eigenvalues.real) < -1e-9
            eigens[str(k)] = float(max(eigenvalues.real))
        rows.append({'L': 'unit' if L is None else str(L),
                     'eta_exact':str(eta),'cubic_exact':str(cubic),
                     'eta':float(eta),'cubic':float(cubic),
                     'largest_noncritical_real_part_by_mode':eigens})
    return {'m':m,'species':n,'checks':rows}

if __name__ == '__main__':
    result = [check(m) for m in [3,4,5,8,12]]
    out=Path(__file__).with_name('independent_check_results.json')
    out.write_text(json.dumps(result,indent=2)+'\n')
    print(f'PASS: exact equilibrium, conservation, critical left/right vectors, mass-compatible cubic and crossing signs for 15 cases; numerical noncritical spectra for 75 mode blocks. {out}')
