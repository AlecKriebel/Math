#!/usr/bin/env python3
"""Exact final identities and read-only reproduction of sealed pass 1-4 checks."""
import hashlib,json,shutil,subprocess,sys,tempfile
from pathlib import Path
import sympy as s
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
checks=[]
def eq(name,lhs,rhs=0):
    difference=lhs-rhs
    if isinstance(difference,s.MatrixBase):
        ok=all(s.simplify(s.expand(z))==0 for z in difference)
    else:
        ok=s.simplify(s.expand(difference))==0
    assert ok,(name,difference)
    checks.append(name)
f=s.symbols('f0:9');g=s.symbols('g0:9')
F=s.Matrix(3,3,f);G=s.Matrix(3,3,g)
t=s.symbols('t',real=True);J=F.det();Jv=G.det()
def colon(A,B):return sum(a*b for a,b in zip(A,B))
M1=colon(F.cofactor_matrix(),G);M2=colon(G.cofactor_matrix(),F)
Jt=((1-t)*F+t*G).det()
eq('full mixed determinant expansion',Jt,(1-t)**3*J+t*(1-t)**2*M1+t*t*(1-t)*M2+t**3*Jv)
eq('mixed determinant derivative',s.diff(Jt,t).subs(t,0),M1-3*J)
j,mm=s.symbols('j mm',positive=True)
eq('mixed barrier derivative',-2*j**-3*(mm-3*j),6*j**-2-2*mm*j**-3)
eq('barrier quotient geometric sum',((1-t)**-6-1)/t,sum((1-t)**-k for k in range(1,7)))
eq('barrier quotient constant 126',sum(2**k for k in range(1,7)),126)
eq('barrier source constant six',s.limit(((1-t)**-6-1)/t,t,0),6)
u=s.Matrix(s.symbols('u0:3'));v=s.Matrix(s.symbols('v0:3'))
Ge=F+u*v.T;Je=Ge.det()
eq('rank-one first mixed minor',colon(F.cofactor_matrix(),Ge),2*J+Je)
eq('rank-one second mixed minor',colon(Ge.cofactor_matrix(),F),J+2*Je)
eq('rank-one recovered barrier source',6-2*2,2)
ss,q=s.symbols('ss q',positive=True)
Fr=s.diag(ss*q,ss,ss)
eq('radial first mixed minor',s.trace(Fr.cofactor_matrix()),ss**2*(1+2*q))
eq('radial second mixed minor',s.trace(Fr),ss*(q+2))
eq('radial mixed moment',s.trace(Fr.cofactor_matrix())/Fr.det()**3,ss**-7*(1+2*q)/q**3)
eq('radial mixed radial power',2-7*s.Rational(1,2),-s.Rational(3,2))
K,Ke,d=s.symbols('K Ke d',positive=True)
eq('inverse cubic barrier derivative',s.diff(d*((1-t)*K+t*Ke)**3,t).subs(t,0),3*d*K*K*(Ke-K))
lam,kap,kd,kr,mass=s.symbols('lam kap kd kr mass',positive=True)
eq('compensated level slack',(kd**2-kr**2-lam**2+kap**2)*mass,((kd**2-lam**2)+(kap**2-kr**2))*mass)
C0=s.symbols('C0',positive=True)
eq('compensated threshold',3*d*((kap**2+C0/(3*d))-kap**2),C0)

# Exact positive-density material stress for a pure shear.
a,b,c,h=s.symbols('a b c h',positive=True)
sh=s.symbols('sh',real=True)
Fs=s.Matrix([[1,sh,0],[0,1,0],[0,0,1]])
Cmat=Fs.T*Fs;S=s.trace(Cmat);T=s.trace(Fs.cofactor_matrix().T*Fs.cofactor_matrix())
U=6*a*S*S*Cmat+3*b*s.sqrt(T)*(S*Cmat-Cmat*Cmat)+2*c*s.eye(3)
eq('shear cofactor norm squared',T,S)
eq('shear positive Eshelby off diagonal',-U[0,1],-(6*a*(3+sh*sh)**2+3*b*s.sqrt(3+sh*sh))*sh)
g1,g2,g3=s.symbols('g1 g2 g3')
AA=s.eye(3)+s.Matrix([1,0,0])*s.Matrix([[g1,g2,g3]])
eq('triangular material determinant',AA.det(),1+g1)
eq('triangular material cofactor',AA.cofactor_matrix(),s.Matrix([[1,0,0],[-g2,1+g1,0],[-g3,0,1+g1]]))
eq('triangular material cofactor norm',colon(AA.cofactor_matrix(),AA.cofactor_matrix()),1+2*(1+g1)**2+g2*g2+g3*g3)
I=s.eye(3)
H1=s.diag(-2,-1,1);B1=s.diag(1,0,0)
eq('universal rank-one control input determinant',H1.det(),2)
eq('universal rank-one control output determinant',(I+B1*H1).det(),-1)
H2=s.diag(-2,1,-1);B2=s.diag(1,1,0)
eq('universal rank-two control input determinant',H2.det(),2)
eq('universal rank-two control output determinant',(I+B2*H2).det(),-2)
H3=s.diag(-1,-1,1)
eq('universal invertible control input determinant',H3.det(),1)
eq('universal invertible control singular output',(I+H3).det(),0)

m,be,de,ang=s.symbols('m be de ang',positive=True)
lead=(ang+m*(1-ang))*((1-ang)+(be-2)*ang)-(m-1)*ang*((be-1)*(1-ang)+2*ang)
eq('critical-axis leading angular determinant',lead,m+(be-3*m)*ang)
repair=(ang+m*(1-ang))*(1+(be+de-1)*ang)-(m-1)*(be+de-1)*(1-ang)*ang
eq('critical-axis repair angular determinant',repair,m*(1-ang)+(be+de)*ang)
gamma=2*m+be-3
eta=2*(3*m+m+2*be-6)
eq('critical-axis stress gap',eta,4*gamma)
r,qq=s.symbols('r qq',positive=True)
JF=qq**2*((be-2*m)*r**(be-3)-(be-3*m)*qq**2*r**(be-2*m-3))
Jsub=r**gamma*(1-ang)*(m+(be-3*m)*ang)
eq('critical-axis fiber substitution',s.powsimp(Jsub.subs(ang,1-qq**2*r**(-2*m)),force=True),JF)
eq('critical-axis fiber derivative',s.diff(JF,r),qq**2*((be-2*m)*(be-3)*r**(be-4)-(be-3*m)*(be-2*m-3)*qq**2*r**(be-2*m-4)))
eq('critical-axis residual coefficient after beta three',((be-3*m)*(be-2*m-3)).subs(be,3),6*m*(m-1))
eq('critical-axis impossible repaired exponent',gamma.subs({m:1,be:3}),2)
vals={m:s.Rational(3,4),be:s.Rational(9,4),de:s.Rational(1,4)}
eq('critical-axis example gamma',gamma.subs(vals),s.Rational(3,4))
eq('critical-axis example energy exponent',(2*gamma+de).subs(vals),s.Rational(7,4))
eq('critical-axis example fiber derivative',s.diff(JF,r).subs(vals),-s.Rational(9,16)*qq**2*r**(-s.Rational(7,4)))
th,eps,cc=s.symbols('th eps cc',positive=True)
primitive=-1/(2*(th*th+eps))
eq('codimension-two angular primitive',s.diff(primitive,th),th/(th*th+eps)**2)
eq('codimension-two angular integral',primitive.subs(th,cc)-primitive.subs(th,0),1/(2*eps)-1/(2*(cc*cc+eps)))
eq('codimension-two angular leading coefficient',s.limit(eps*(primitive.subs(th,cc)-primitive.subs(th,0)),eps,0),s.Rational(1,2))
alpha2,alpha3=s.symbols('alpha2 alpha3',positive=True);total=m+alpha2+alpha3
normalization=-2*(total-3)-6*(m-1)
eq('balanced whole-energy normalization exponent',normalization,12-2*(total+3*m))
eq('balanced normalization exponent vanishes',normalization.subs(alpha3,6-4*m-alpha2))
eq('balanced third-row gap', (2*(3*m+alpha2+2*alpha3-6)-2*(alpha3-m)).subs(alpha3,6-4*m-alpha2))
jj=s.Function('jj')(r)
eq('pressure gradient coefficient',s.diff(jj**-2,r),-2*jj**-3*s.diff(jj,r))
al=s.symbols('al',positive=True)
eq('logarithmic modulus critical exponent',-2*al+(1-al),1-3*al)
LL=s.log(s.E/r)
pp=LL**s.Rational(2,3)
eq('critical abstract pressure derivative',s.diff(pp,r),-s.Rational(2,3)/r*LL**(-s.Rational(1,3)))
qformal=s.Function('qformal')(r)
# This is the radial integrating-factor identity, independent of a quadrature rule.
eq('radial tensor divergence integrating factor',s.diff(r*r*qformal,r)/r**2,s.diff(qformal,r)+2*qformal/r)
eq('formal critical determinant',s.Pow(pp,-s.Rational(1,2)),LL**(-s.Rational(1,3)))

cc0,ph2,ph3,w2x,w2y,w3x,w3y=s.symbols('cc0 ph2 ph3 w2x w2y w3x w3y')
angular_rows=s.Matrix([[cc0*m,0,0],[alpha2*ph2,w2x,w2y],[alpha3*ph3,w3x,w3y]])
eq('critical angular Jacobian wedge',angular_rows.det(),cc0*m*(w2x*w3y-w2y*w3x))
eq('scalar spherical critical value',(m*(5*m-3)).subs(m,s.Rational(3,5)))
eq('subcritical first barrier gap',(7-2*total-m)-(5*m-5),2*(6-total-3*m))

sealed={
1:{'report':('EXACT_EXAMPLES.md','597768cd4b7440eedc8b957d30107f36e49e9afdb960fb18ccf7fa18f9fdbb2c'),'script':('verify_exact.py','8ede79046b74b0a736929a51124a65641d4071f1dd899ad2c1b9798b6cc973ab'),'output':('verification.json','2b8bdb708c3344b3c5ec74ced074f0c0d0f7bdb54e8406aa71bc5209adcaae71')},
2:{'report':('ENDPOINT_CERTIFICATION.md','3cc9f68b39fa3621dcdf0fa45ce4eb54e22064cd3d04c31a655f9fd176f5f904'),'script':('verify_endpoints.py','a895734ea3659eee20e62328b6cac081f6c53a0483b6f105970f59558e7479e4'),'output':('verification.json','8b959a85369fb5a02e6e15eade9aea19472c6eb734ed3a8bb730fea02cfd1a44')},
3:{'report':('COUPLED_AND_HOMOGENEOUS_CERTIFICATION.md','285fb3a803adfce18053a79c9f9c6be23ea991db766d6ce412d1c5c8df0c5055'),'script':('verify_coupled.py','2d8eec68c4a8ae1117765114ab807d7940c11d2adcf77e548c954bb6b58a84ee'),'output':('verification.json','f751e02bba07f40f959274ddd404d66927ba026e64776f10ad2842e6618c55ad')},
4:{'report':('COMPARISON_AND_TANGENT_CERTIFICATION.md','e8395733fa2564299aedd7e875dc0dc7bffa508c3f97aa74fd2723af7d2c2481'),'script':('verify_comparisons.py','977d0d188785215ebf7db503006bfb9e04f573486f0106782e20c5d79417e10d'),'output':('verification.json','91a208bb882b1995c4415fb294a5ed35d1325870d7d54dba08c554813c4cd21b')},
}
reproductions=[]
for number,entry in sealed.items():
    base=ROOT/f'research_elasticity_1791_pass{number}_20261016'/'exact'
    items=[]
    for kind,(name,expected) in entry.items():
        data=(base/name).read_bytes();actual=hashlib.sha256(data).hexdigest()
        assert actual==expected,(number,name,actual,expected)
        items.append({'kind':kind,'path':str((base/name).relative_to(ROOT)),'sha256':actual,'bytes':len(data)})
    with tempfile.TemporaryDirectory(prefix=f'elasticity_pass{number}_recheck_') as tmp:
        target=Path(tmp)/entry['script'][0];shutil.copyfile(base/entry['script'][0],target)
        run=subprocess.run([sys.executable,str(target)],check=True,capture_output=True,text=True)
        reproduced=(Path(tmp)/'verification.json').read_bytes()
        assert reproduced==(base/'verification.json').read_bytes(),f'pass {number} output is not byte-identical'
        reproductions.append({'pass':number,'sealed_files':items,'exit_code':run.returncode,'byte_identical_output':True,'stdout':json.loads(run.stdout)})
previous_exact=sum(x['stdout'].get('symbolic_checks',x['stdout'].get('exact_checks',0)) for x in reproductions)
previous_quad=sum(x['stdout'].get('quadrature_checks',0) for x in reproductions)
assert previous_exact==150 and previous_quad==14
out={'status':'pass','scope':'Exact auxiliary identities and reproduction; no benchmark proof or minimizer counterexample','pass5_exact_checks':len(checks),'pass5_checks':checks,'prior_exact_checks':previous_exact,'prior_quadrature_checks':previous_quad,'total_exact_checks':previous_exact+len(checks),'prior_reproductions':reproductions,'software':{'python':sys.version.split()[0],'sympy':s.__version__},'terminal_benchmark_status':'UNSOLVED after 5/5 research passes'}
(HERE/'verification.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':'pass','pass5_exact_checks':len(checks),'prior_exact_checks':previous_exact,'prior_quadrature_checks':previous_quad,'total_exact_checks':previous_exact+len(checks),'sealed_files_verified':12,'earlier_outputs_byte_identical':True},indent=2))
