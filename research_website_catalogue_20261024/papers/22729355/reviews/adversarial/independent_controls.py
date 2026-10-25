"""Fresh adversarial controls: no published construction/verifier imports.

The model is differentiated from its polynomial vector field. Exact polynomial
division supplies a separate all-dimension cubic contraction route. Numerical
eigenvalues are supplementary finite stress tests, not universal certificates.
"""
from pathlib import Path
from itertools import combinations
import datetime, hashlib, json, re
import numpy as np
import scipy.linalg as la
import sympy as s

HERE=Path(__file__).resolve().parent
SOURCE=HERE.parents[1]/'sources'
TEX=SOURCE/'published-source/Exact_Diffusion_Design_Source_v1.0.11'
R=s.Rational
checks=[]
def check(name,condition,detail=None):
    assert bool(condition), (name,detail)
    checks.append({'name':name,'detail':detail})

def model(m,a=s.Integer(1),b=s.Integer(1)):
    # Polynomial reaction field from the displayed reactions, with flux a,b at 1.
    x=s.Matrix(s.symbols('x1:'+str(m+1))+s.symbols('z',seq=True))
    f=s.zeros(m+1,1)
    f[0]+=a
    for j in range(1,m-2):
        rate=a*x[0]*x[j]; f[j]-=rate; f[j+1]+=rate
    rate=a*x[0]*x[m-2]; f[0]-=rate; f[m-2]-=rate; f[m-1]+=2*rate
    rate=a*x[m-1]**2; f[m-1]-=2*rate; f[1]+=rate
    rate=b*(x[m]**2-x[0]*x[m-1]); f[0]+=rate; f[m-1]+=rate; f[m]-=2*rate
    eq={xi:1 for xi in x}; A=f.jacobian(x).subs(eq)
    hs=[s.hessian(fi,x) for fi in f]
    def B(u,v): return s.Matrix([(u.T*h*v)[0] for h in hs])
    c=s.Matrix([0]+[4]*(m-2)+[2,1])
    return x,f,A,B,c

def profile(m):
    K=lambda i:91*m-181-i
    r=s.Matrix([1]+[-R(K(i),63*(m-2)) for i in range(2,m)]+[-R(2,9),R(5,14)])
    d=s.Matrix([R(23,63)]+[R(1,K(i)) for i in range(2,m)]+[R(1,7),R(16,45)])
    ell=s.Matrix([-R(266,815)]+[R(78260*(m-2),163*K(i-1)) for i in range(2,m)]+[R(18368,7335),1])
    return r,s.diag(*d),ell

def rh_positive(M):
    aa=M.charpoly().all_coeffs(); n=M.rows
    return all(s.det(s.Matrix(k,k,lambda i,j:aa[2*i-j+1] if 0<=2*i-j+1<=n else 0))>0 for k in range(1,n+1))

def matrix_controls():
    for m in range(3,8):
        for a,b in [(R(1,7),R(8,3)),(R(5,2),R(1,9)),(s.Integer(1),s.Integer(2))]:
            _,f,A,B,c=model(m,a,b)
            h=[R((i+3)**2,i+2) for i in range(m+1)]
            J=A*s.diag(*h)
            check(f'mass polynomial m={m} a={a} b={b}',(c.T*f)[0].expand()==0)
            check(f'rank m={m} a={a} b={b}',A.rank()==m)
            for order in range(1,m):
                for I in combinations(range(m+1),order):
                    check(f'proper principal Hurwitz m={m} a={a} b={b} I={I}',rh_positive(J.extract(I,I)))
            omissions=[]
            for k in range(m+1):
                I=[i for i in range(m+1) if i!=k]
                omissions.append(s.factor((-1)**m*J.extract(I,I).det()))
            wanted=[0]+[16*a**(m-1)*b*h[-1]*s.prod(h[j] for j in range(m) if j!=k) for k in range(1,m-1)]+[0,-2*a**(m-1)*b*s.prod(h[:m])]
            check(f'all omissions m={m} a={a} b={b}',omissions==wanted)
    # Exact threshold boundary and positive-real-root count via Sturm, m=3..6.
    t=s.symbols('t')
    for m in range(3,7):
        _,_,A,_,_=model(m)
        for excess in [-R(1,3),s.Integer(0),R(1,3)]:
            d=[1]*m+[8*(m-2)+excess]
            q=s.Poly(s.cancel((t*s.diag(*d)-A).det()/t),t)
            expected=1 if excess>0 else 0
            # Ignore zero at the boundary by stripping its multiplicity.
            while q.eval(0)==0: q=s.Poly(q.as_expr()/t,t)
            check(f'exact Sturm band threshold m={m} excess={excess}',q.count_roots(0,s.oo)==expected)
        check(f'equal diffusion cannot cross m={m}',all(v>=0 for v in s.Poly(s.cancel((t*s.eye(m+1)-A).det()/t),t).all_coeffs()))
    # Degenerate H on the excluded homogeneous-stability boundary.
    _,_,A,_,_=model(3)
    H=s.diag(1,8,1,1); cp=(A*H).charpoly().as_poly()
    check('T(H)=1 gives at least double homogeneous zero',cp.nth(0)==0 and cp.nth(1)==0)

def modulus_controls():
    x,y,z,t,A,U=s.symbols('x y z t A U',real=True); l=x+s.I*y
    def abs2(p):
        py=s.Poly(s.expand(p*s.conjugate(p)),y)
        check('modulus contains only even imaginary powers',all(k[0]%2==0 for k,_ in py.terms()))
        return s.expand(sum(v*z**(k[0]//2) for k,v in py.terms()))
    P=l**4+12*l**3+42*l**2+47*l+16; R2=5*l**2+33*l+16
    g1=l+2+(1+t)*R(23,63); gm=l+5+(1+t)*R(1,7); gz=l+4+(1+t)*R(16,45)
    F=g1*gm*gz-4*g1-4*gm+gz; G=gz*(4*g1+gm)-36
    F0=l**3+11*l**2+31*l+16
    polys=[(abs2((1+l)*P)-abs2(R2),(x,z),None,35),
           ((R(91,90)**2+z)*abs2(F)-abs2(G),(x,z,t),None,77),
           ((1+(U+R(1,4))*x+R(5,4)*z)*abs2(F0)-abs2(R2),(x,z),U,22),
           (R(91,90)**2*(1+A*x+z/3)*abs2(F)-abs2(G),(x,z,t),A,84)]
    text=(TEX/'data/certificate_tables.tex').read_text()
    tables=text.split('\\begin{longtable}')[1:]
    for (expr,variables,aux,count),table in zip(polys,tables):
        poly=s.Poly(s.expand(expr),*variables); rows={}
        for line in table.splitlines():
            if re.match(r'^\d+ & ',line):
                cells=line.split('&'); powers=tuple(int(k.strip()) for k in cells[:-1])
                coefficient=cells[-1].split('$')[1]
                rows[powers]=s.sympify(coefficient.replace('U','*U').replace('A','*A').replace('+*','+').lstrip('*'),locals={'A':A,'U':U})
        actual=dict(poly.terms())
        check(f'printed {count}-term coefficient table equals regeneration',rows==actual,{'terms':len(actual)})
        check(f'{count}-term nonnegative coefficients',all(all(v>0 for v in (s.Poly(c,aux).coeffs() if aux else [c])) for c in actual.values()))
        check(f'{count}-term equality only at origin',all((poly.coeff_monomial(v**2).subs(aux,0) if aux else poly.coeff_monomial(v**2))>0 for v in variables))
        check(f'{count}-term constant zero',poly.coeff_monomial(1)==0)

def exact_harmonic_controls():
    for m in [3,4,5,7,11]:
        _,_,A,B,c=model(m); r,D,ell=profile(m); n=m+1
        check(f'right and left mode m={m}',(A-D)*r==s.zeros(n,1) and ell.T*(A-D)==s.zeros(1,n))
        forcing=-B(r,r)/4
        for L in [None,R(9,10),R(90*(m-2),90*(m-2)+1)]:
            H=s.eye(n) if L is None else s.diag(1,*[R(91*m-181-i,91*m-180-i)/L for i in range(2,m)],1,1)
            q=H.inv()*c
            # Constrained direct solve, not the supplied closed w0/w2 routines.
            mat=A.copy(); rhs=forcing.copy(); mat[n-1,:]=q.T; rhs[n-1]=0
            w0=mat.inv()*rhs; w2=(A-4*D).inv()*forcing
            check(f'forcing and mass gauge m={m} L={L}',A*w0==forcing and (q.T*w0)[0]==0 and (A-4*D)*w2==forcing)
            left=H.inv()*ell
            numerator=s.factor((ell.T*(B(r,w0)+B(r,w2)/2))[0])
            cubic=s.factor(numerator/(left.T*r)[0]); eta=s.factor((ell.T*D*r)[0]/(left.T*r)[0])
            check(f'supercritical cubic and transverse sign m={m} L={L}',cubic<0 and eta>0,{'cubic':str(cubic),'eta':str(eta),'N':str(numerator)})
            # Independent conservation and Fourier-factor mutation sensitivity.
            if L is not None and H!=s.eye(n):
                unscaled=A.copy(); rhs0=forcing.copy(); unscaled[n-1,:]=c.T; rhs0[n-1]=0
                wrong=unscaled.inv()*rhs0
                check(f'wrong old mass gauge is rejected m={m} L={L}',(q.T*wrong)[0]!=0)
            wrong2=(A-D).rank() # second harmonic cannot use the critical operator
            check(f'wrong second-harmonic multiplier is singular m={m} L={L}',wrong2==n-1)
        # Finite spectral stress tests at certified endpoints and modes, no universal inference.
        for L in [1/np.sqrt(3) if m==3 else np.sqrt(5/(4*(m-2))),90*(m-2)/(90*(m-2)+1)]:
            hs=np.array([1]+[(91*m-181-i)/(L*(91*m-180-i)) for i in range(2,m)]+[1,1]); H=np.diag(hs)
            for t in [0,1,1.0001,4,9,100]:
                vals=la.eigvals(H@(np.array(A,dtype=float)-t*np.array(D,dtype=float)))
                nz=np.delete(vals,np.argmin(abs(vals))) if t in [0,1] else vals
                check(f'finite spectral stress m={m} L={L} t={t}',np.max(nz.real)<0,{'max_noncentral_real':float(np.max(nz.real))})
    # The near-threshold path actually has the opposite nonlinear sign.
    _,_,A,B,c=model(3)
    for e in [R(1,1000),R(1,10000)]:
        r=s.Matrix([1,-(1+R(16,9)*e+e**2/2),-e,R(1,2)-R(13,18)*e]); d=s.Matrix([(A*r)[i]/r[i] for i in range(4)]); D=s.diag(*d)
        ell=(A-D).T.nullspace()[0]; forcing=-B(r,r)/4
        mat=A.copy(); rhs=forcing.copy(); mat[3,:]=c.T; rhs[3]=0
        w0=mat.inv()*rhs; w2=(A-4*D).inv()*forcing
        cubic=s.factor((ell.T*(B(r,w0)+B(r,w2)/2))[0]/(ell.T*r)[0])
        check(f'subcritical counter-control e={e}',cubic>0 and all(di>0 for di in d) and d[3]>8*d[1],{'cubic':str(cubic)})

if __name__=='__main__':
    matrix_controls(); print('matrix controls complete',flush=True)
    modulus_controls(); print('modulus controls complete',flush=True)
    exact_harmonic_controls(); print('harmonic controls complete',flush=True)
    result={'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checks_passed':len(checks),'checks':checks,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'limitations':'Finite matrix/eigenvalue controls are corroboration. All-dimension results additionally require the analytic arguments and symbolic cubic bridge.'}
    (HERE/'independent-controls.json').write_text(json.dumps(result,indent=2)+'\n')
    print('PASS',len(checks))
