"""Fresh analytic controls authored from the paper, before packaged helper reading.
Finite controls corroborate the proof; they do not replace its all-dimensional argument.
"""
import hashlib, itertools, json, math, platform
from pathlib import Path
from datetime import datetime, timezone
import numpy as np
import sympy as s
OUT=Path(__file__).resolve().parent
checks={}

def require(x,msg):
    if not x: raise RuntimeError(msg)

def tensor(L,coords):
    n=L.rows
    return {(k,i,j):s.expand(sum(L[a,i]*s.diff(L[k,j],coords[a])-L[a,j]*s.diff(L[k,i],coords[a])-L[k,a]*s.diff(L[a,j],coords[i])+L[k,a]*s.diff(L[a,i],coords[j]) for a in range(n))) for k in range(n) for i in range(n) for j in range(i+1,n)}

# Direct full coordinate definition, arbitrary polynomial first jets, no collar shortcut.
jet_components=0
for n in range(2,6):
    m=n-1; q=s.symbols('q:'+str(n)); t=q[-1]
    A=s.Matrix(m,m,lambda i,j:s.Symbol(f'a{i}{j}')+t*s.Symbol(f'd{i}{j}'))
    b=s.Matrix(m,1,lambda i,j:s.Symbol(f'b{i}')+t*s.Symbol(f'e{i}'))
    lam=s.Symbol('l')+t*s.Symbol('h')
    L=A.row_join(b).col_join(s.zeros(1,m).row_join(s.Matrix([[lam]])))
    expected=(A-lam*s.eye(m))*A.diff(t)
    for (k,i,j),z in tensor(L,q).items():
        target=expected[k,i] if j==m and k<m else 0
        require(s.expand(z-target)==0,f'jet mismatch {n,k,i,j}')
        jet_components+=1
checks['arbitrary_first_jet_identity']={'dimensions':[2,3,4,5],'components':jet_components,'status':'pass','covers':'all independent A,A-prime,b,b-prime,lambda,lambda-prime symbols'}

# Distinct geometric control: pushforward from the circle collar to Cartesian coordinates.
# e_theta=(-y,x), dr=(x,y)/r, A=lambda=r^2, b=r => polynomial Cartesian field.
x,y=s.symbols('x y',real=True); rr=x*x+y*y
L=s.Matrix([[rr-x*y,-y*y],[x*x,rr+x*y]])
N=tensor(L,[x,y]); require(all(v==0 for v in N.values()),'Cartesian annular control')
checks['noncartesian_pushforward']={'matrix':str(L),'torsion':{str(k):str(v) for k,v in N.items()},'domain':'r>0; polynomial extension also zero torsion','status':'pass'}

# Exact whole-block schedules. Every stage is affine in its own parameter;
# checking both product coefficients is an identity, not a sample in that parameter.
def compositions(n):
    if not n: yield ()
    else:
        for a in range(1,n+1):
            for rest in compositions(n-a): yield (a,)+rest
cases=stages=0; maxn=8
for n in range(2,maxn+1):
    for sizes in compositions(n):
        for distinguished in range(len(sizes)):
            order=[i for i in range(len(sizes)) if i!=distinguished]+[distinguished]
            for family in range(3):
                eigen=[0 if family==0 else (3 if family==1 else (-2,0,3)[i%3]) for i in range(len(sizes))]
                J=np.zeros((n,n),dtype=np.int64); cursor=0; blocks=[]
                for i in order:
                    k=sizes[i]; mu=eigen[i]
                    for j in range(k): J[cursor+j,cursor+j]=mu
                    for j in range(k-1): J[cursor+j,cursor+j+1]=1
                    blocks.append((cursor,k if i!=distinguished else k-1,mu));cursor+=k
                A=J[:-1,:-1].copy(); b=J[:-1,-1].copy(); lam=int(J[-1,-1]); ident=np.eye(n-1,dtype=np.int64)
                require(np.all(J[-1,:-1]==0),'invariant hyperplane')
                initial=np.block([[A,b[:,None]],[np.zeros((1,n-1),dtype=np.int64),np.array([[lam]])]])
                require(np.array_equal(initial,J),'initial J')
                def stage(endA,endb,endlam):
                    global A,b,lam,stages
                    D=endA-A; dl=endlam-lam
                    require(np.all((A-lam*ident)@D==0),'stage constant coefficient')
                    require(np.all((D-dl*ident)@D==0),'stage linear coefficient')
                    A=endA.copy();b=endb.copy();lam=int(endlam);stages+=1
                stage(A,np.zeros_like(b),lam)
                for start,k,mu in blocks:
                    if k==0: continue
                    stage(A,b,mu)
                    for arrow in range(k-1):
                        nextA=A.copy();nextA[start+arrow,start+arrow+1]=0
                        stage(nextA,b,mu)
                    nextA=A.copy()
                    for j in range(k):nextA[start+j,start+j]=0
                    stage(nextA,b,0)
                require(np.all(A==0) and np.all(b==0) and lam==0,'final zero')
                cases+=1
checks['exact_affine_stage_paths']={'dimensions':list(range(2,maxn+1)),'ordered_compositions':'all','distinguished_blocks':'all','eigenvalue_families':['all 0','all 3','cycling -2,0,3'],'paths':cases,'stages':stages,'status':'pass'}

# Negative controls expose product order and scalar compatibility rather than endorsing all cutoffs.
u=s.Symbol('u'); E12=s.zeros(3);E12[0,1]=1;E23=s.zeros(3);E23[1,2]=1
bad_right=E12+(1-u)*E23
right_res=s.expand(bad_right*bad_right.diff(u))
require(right_res[0,2]==-1,'right first arrow must fail')
good_left=(1-u)*E12+E23
require(good_left*good_left.diff(u)==s.zeros(3),'left first arrow')
require(good_left.diff(u)*good_left!=s.zeros(3),'ordered reverse negative')
bad_cut=u*(E12+E23)
cut_res=s.expand(bad_cut*bad_cut.diff(u));require(cut_res[0,2]==u,'nilpotent scalar cutoff')
bad_scalar=(s.diag(u,2)-s.eye(2)*0)*s.diag(1,0)
require(bad_scalar[0,0]==u,'unmatched scalar')
rot=s.Matrix([[0,-1],[1,0]]); rotN=tensor(x*rot,[x,y]);require(any(z!=0 for z in rotN.values()),'rotation cutoff must fail')
checks['negative_controls']={'reverse_arrow_order':str(right_res),'reverse_product_of_valid_stage':str(good_left.diff(u)*good_left),'nilpotent_scalar_cutoff':str(cut_res),'unmatched_scalar':str(bad_scalar),'nonreal_scalar_cutoff_torsion':{str(k):str(v) for k,v in rotN.items()},'all_rejected':True}

# Independent torus embedding differential check through d=4, with strictly nested radii.
# Closed-form diagonal Gram matrix proves immersion and confirms the stated global normal.
ths=s.symbols('th1:5',real=True); radii=[s.Integer(16),s.Integer(4),s.Integer(1),s.Rational(1,4)]
f=s.Matrix([radii[0]*s.cos(ths[0]),radii[0]*s.sin(ths[0])]); normal=s.Matrix([s.cos(ths[0]),s.sin(ths[0])]); torus=[]
for d in range(1,5):
    if d>1:
        f=(f+radii[d-1]*s.cos(ths[d-1])*normal).col_join(s.Matrix([radii[d-1]*s.sin(ths[d-1])]))
        normal=(s.cos(ths[d-1])*normal).col_join(s.Matrix([s.sin(ths[d-1])]))
    require(s.trigsimp(normal.dot(normal)-1)==0,'unit normal')
    jac=f.jacobian(ths[:d])
    require(all(s.trigsimp(z)==0 for z in (normal.T*jac)),'normal orthogonal')
    gram=jac.T*jac
    require(all(s.trigsimp(gram[i,j])==0 for i in range(d) for j in range(d) if i!=j),'orthogonal torus coords')
    torus.append({'dimension':d,'radii':[str(z) for z in radii[:d]],'ambient_dimension':d+1,'unit_normal':True,'orthogonality':True,'injectivity_scope':'analytic tubular-neighborhood proof, not inferred from samples'})
checks['torus_differential_control']=torus

# Flat collar thresholds and maximum-principle algebra boundary control.
z=s.Symbol('z'); qarg=2*(u*u-s.Rational(1,16))
require(qarg.subs(u,s.Rational(1,4))==0 and qarg.subs(u,s.Rational(3,4))==1,'q thresholds')
Lrot=s.diag(rot,rot/2); image=Lrot*Lrot+s.eye(4)
require(image==s.diag(0,0,s.Rational(3,4),s.Rational(3,4)),'polynomial pair count')
checks['boundary_algebra']={'q_argument':str(qarg),'inner_threshold':'1/4','outer_threshold':'3/4','rotation_polynomial_image':str(image),'interpretation':'source stronger theorem not refuted; its terminal literal pair count is not used'}
result={'completed_utc':datetime.now(timezone.utc).isoformat(),'python':platform.python_version(),'sympy':s.__version__,'numpy':np.__version__,'status':'pass','checks':checks,'limitations':['Finite dimensional indexing controls do not establish all-dimensional proof.','C-infinity gluing and global injectivity are justified analytically, not by sampling.','No stochastic/numerical evidence or prior helper code used.']}
(OUT/'evidence/independent-controls.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':'pass','jet_components':jet_components,'paths':cases,'stages':stages,'torus_dimensions':4}))
