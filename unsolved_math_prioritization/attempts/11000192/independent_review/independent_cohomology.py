"""Independent direct quotient audit of the frozen genus-two tangent certificate.

Usage: python independent_cohomology.py PATH/TO/TURN_5_COCHAIN_CERTIFICATE.json
No author checker is imported. The cohomology action is computed on an actual
kernel/mod-conjugation basis, rather than by dividing the raw characteristic polynomial.
"""
import json,sys
from fractions import Fraction
from collections import Counter
import sympy as s
from sympy.polys.matrices import DomainMatrix

counts=Counter()
def ck(t,name):
    assert t,name
    counts[name]+=1

cert=json.load(open(sys.argv[1]))
X0=s.symbols('X');p=X0**4-3*X0**3+2*X0**2+2*X0-1
root=s.CRootOf(p,0);K=s.QQ.algebraic_field(root)
x=K.from_sympy(root);y=x/(x-1);o=K.one;z=K.zero
def dm(rows):return DomainMatrix([[K.convert(v) for v in row] for row in rows],(len(rows),len(rows[0])),K)
def zeros(n,m):return dm([[0]*m for _ in range(n)])
def eye(n):return dm([[int(i==j) for j in range(n)] for i in range(n)])
def take(M,rows,cols):
    a=M.to_list();return dm([[a[i][j] for j in cols] for i in rows])
def hcat(A,B):return dm([a+b for a,b in zip(A.to_list(),B.to_list())])
def vcat(*M):return dm(sum((a.to_list() for a in M),[]))
def rank(M):return len(M.rref()[1])
def decode(v):return sum((K.convert(s.Rational(c))*x**j for j,c in enumerate(v)),z)
def decoded(name):return dm([[decode(v) for v in row] for row in cert[name]])
I=eye(3)

U=1-x*x/4;V=1-y*y/4;W=x*y/4-x/2;T=U*V-W*W
Gram=dm([[U,W,0],[W,V,0],[0,0,T]])
ck(T==K.convert(s.Rational(3,4)),'positive_vector_Gram_minor')
def dot(a,b):
    return U*a[0]*b[0]+V*a[1]*b[1]+W*(a[0]*b[1]+a[1]*b[0])+T*a[2]*b[2]
def cross(a,b):
    a12=a[0]*b[1]-a[1]*b[0];a13=a[0]*b[2]-a[2]*b[0];a23=a[1]*b[2]-a[2]*b[1]
    return (a13*W+a23*V,-a13*U-a23*W,a12)
def quat(c,v):return (K.convert(c),tuple(K.convert(w) for w in v))
unit=quat(1,(0,0,0));A=quat(x/2,(1,0,0));B=quat(y/2,(0,1,0))
def mul(a,b):
    c,v=a;d,w=b;t=cross(v,w)
    return (c*d-dot(v,w),tuple(c*w[i]+d*v[i]+t[i] for i in range(3)))
def qi(a):return (a[0],tuple(-t for t in a[1]))
def qword(word,images):
    result=unit
    for letter in word:result=mul(result,images[abs(letter)-1] if letter>0 else qi(images[-letter-1]))
    return result
def adj(a):
    cols=[]
    for j in range(3):
        v=[0,0,0];v[j]=1
        q=mul(mul(a,quat(0,v)),qi(a));ck(q[0]==z,'adjoint_is_imaginary');cols.append(q[1])
    return dm(list(map(list,zip(*cols))))
ck(mul(A,qi(A))==unit and mul(B,qi(B))==unit,'actual_unit_quaternions')
C=qword((1,2,-1,-2),(A,B))
ck(2*C[0]==-o,'SU2_commutator_trace')
ck(mul(mul(C,C),C)==unit,'SU2_boundary_cube_not_just_adjoint')
RA,RB=adj(A),adj(B)
AB=mul(A,B);BAB=mul(B,AB)
ck(AB[0]==A[0] and BAB[0]==B[0],'intertwiner_actual_scalar_parts')
O=dm(list(map(list,zip(AB[1],BAB[1],cross(AB[1],BAB[1])))))
ck(O.transpose()*Gram*O==Gram,'intertwiner_metric')
ck(O.det()==o,'intertwiner_positive_orientation')
Oi=O.inv();Oi3=Oi*Oi*Oi
for name,M in [('adjoint_a',RA),('adjoint_b',RB),('intertwiner',O),('gram_matrix',Gram),('end_cochain_action',Oi3)]:
    ck(M==decoded(name),'primary_matrix_reconstruction')

# Free words and a generic Schreier rewriting from coset representatives.
def reduce(w):
    a=[]
    for i in w:
        if a and a[-1]==-i:a.pop()
        else:a.append(i)
    return tuple(a)
def inverse(w):return tuple(-i for i in reversed(w))
def substitute(w,images):return reduce(sum((tuple(images[abs(i)-1]) if i>0 else inverse(images[-i-1]) for i in w),()))
phi=((1,2),(2,1,2));phi_inv=((1,1,-2),(2,-1));phi3=((1,),(2,));inv3=phi3
for _ in range(3):
    phi3=tuple(substitute(w,phi) for w in phi3)
    inv3=tuple(substitute(w,phi_inv) for w in inv3)
hs=((1,1,1),(2,),(1,2,-1,-1),(1,1,2,-1))
reps=((),(1,),(1,1))
def transition(j,letter):
    if abs(letter)==1:return (j+(1 if letter>0 else -1))%3
    return (-j)%3
schreier={}
for j in range(3):
    for letter in (1,2):
        v=transition(j,letter)
        raw=reduce(reps[j]+(letter,)+inverse(reps[v]))
        schreier[(j,letter)]=0 if not raw else hs.index(raw)+1
def rewrite(w):
    state=0;out=[]
    for letter in w:
        nxt=transition(state,letter)
        label=schreier[(state,letter)] if letter>0 else -schreier[(nxt,-letter)]
        if label:out.append(label)
        state=nxt
    ck(state==0,'Schreier_closed_path')
    result=reduce(out)
    ck(substitute(result,hs)==reduce(w),'Schreier_free_word_roundtrip')
    return result
rel=rewrite((1,2,-1,-2)*3)
images=tuple(rewrite(substitute(w,phi3)) for w in hs)
inverse_images=tuple(rewrite(substitute(w,inv3)) for w in hs)
for name,obj in [('base_cube',phi3),('cover_generators_in_base',hs),('cover_cube_images',images),('inverse_cover_cube_images',inverse_images)]:
    ck(tuple(map(tuple,cert[name]))==obj,'word_certificate_reconstruction')
ck(tuple(cert['filled_relator'])==rel,'filled_relator_reconstruction')
ck(substitute(rel,images)==rel,'exact_surface_relator_preservation')
for j in range(4):
    ck(substitute(images[j],inverse_images)==(j+1,),'cover_inverse_on_free_basis')
    ck(substitute(inverse_images[j],images)==(j+1,),'cover_inverse_on_free_basis')
qh=tuple(qword(w,(A,B)) for w in hs)
ck(qword(rel,qh)==unit,'filled_SU2_relation')
RH=tuple(adj(q) for q in qh)

# Exact left-logarithmic Fox differentiation, with quaternion-derived adjoints.
def differential(w,rotations):
    result=[[z]*(3*len(rotations)) for _ in range(3)];prefix=I
    for letter in w:
        j=abs(letter)-1
        if letter<0:prefix=prefix*rotations[j].inv()
        block=prefix.to_list();sign=1 if letter>0 else -1
        for row in range(3):
            for col in range(3):result[row][3*j+col]+=sign*block[row][col]
        if letter>0:prefix=prefix*rotations[j]
    return dm(result)
def coboundary(rotations):return vcat(*(I-R for R in rotations))
D=differential(rel,RH);B0=coboundary(RH)
L=vcat(*(Oi3*differential(w,RH) for w in images))
for name,M in [('relation_d1',D),('coboundary_d0',B0),('normalized_cochain_action',L)]:
    ck(M==decoded(name),'cochain_matrix_reconstruction')
ck(D*B0==zeros(3,3),'cochain_complex')
ck(D*L==Oi3*D,'relation_chain_map')
ck(L*B0==B0*Oi3,'conjugation_chain_map')

def quotient(D,B,L):
    ambient=L.shape[0]
    N=D.nullspace().transpose()
    combined=hcat(B,N)
    pivots=combined.rref()[1]
    ck(pivots[:3]==(0,1,2),'conjugation_basis_first')
    E=take(combined,range(ambient),pivots)
    rows=E.transpose().rref()[1]
    Einv=take(E,rows,range(E.shape[1])).inv()
    action=Einv*take(L*E,rows,range(E.shape[1]))
    ck(E*action==L*E,'actual_kernel_action_solved')
    ck(D*E==zeros(D.shape[0],E.shape[1]),'chosen_basis_satisfies_constraints')
    ck(take(action,range(3,E.shape[1]),range(3))==zeros(E.shape[1]-3,3),'conjugations_removed')
    H=take(action,range(3,E.shape[1]),range(3,E.shape[1]))
    representatives=take(E,range(ambient),range(3,E.shape[1]))
    return H,representatives,E,rows,Einv

ck(rank(D)==3 and rank(B0)==3,'closed_constraint_and_conjugation_ranks')
H,Hrep,E,rows,Einv=quotient(D,B0,L)
ck(H.shape==(6,6),'closed_H1_dimension')
cp=H.charpoly()
ck(cp==[decode(a) for a in cert['H1_characteristic']],'direct_H1_characteristic')

# Independently reconstruct the relative 2-plane and its inclusion in closed H1.
Rbase=(RA,RB);BC=coboundary(Rbase);Dc=differential((1,2,-1,-2),Rbase)
row=dm([[-2*sum((C[1][i]*Gram.to_list()[i][j] for i in range(3)),z) for j in range(3)]])
Dtrace=row*Dc
Lbase=vcat(*(Oi*differential(w,Rbase) for w in phi))
ck(Dtrace*BC==zeros(1,3),'boundary_trace_is_conjugation_invariant')
Tbase,base_reps,_,_,_=quotient(Dtrace,BC,Lbase)
ck(Tbase.shape==(2,2),'relative_H1_dimension')
tau=2*x*y-1
ck(Tbase.charpoly()==[o,-tau,o],'relative_characteristic_reconstruction')
J=vcat(*(differential(w,Rbase) for w in hs))
lift=J*base_reps
ck(D*lift==zeros(3,2),'relative_deformations_extend_over_cap')
coordinates=Einv*take(lift,rows,range(2))
inc=take(coordinates,range(3,9),range(2))
ck(rank(inc)==2,'relative_tangent_restriction_injective')
ck(H*inc==inc*Tbase*Tbase*Tbase,'relative_plane_exact_intertwining')

sigma=2-tau;ck(sigma*sigma==K.convert(13),'quadratic_subfield_identity')
aa=(53-5*sigma)/2;bb=(705-163*sigma)/2;ta=80-22*sigma
expected=[z]*7
for i,a in enumerate([o,-ta,o]):
    for j,b in enumerate([o,-aa,bb,-aa,o]):expected[i+j]+=a*b
ck(cp==expected,'direct_normal_quartic_factor')
ck(ta==tau**3-3*tau,'relative_cube_trace')
lo=Fraction(18,5);hi=Fraction(361,100)
ck(lo*lo<13<hi*hi,'positive_sqrt13_interval')
ck((387*lo-1237)/2>0,'normal_reduced_discriminant_positive')
ck((53-5*hi)/2>4,'normal_vertex_beyond_two')
ck((603-153*hi)/2>0,'normal_value_at_two_positive')
ck(-2<80-22*hi<80-22*lo<2,'center_pair_remains_elliptic')
ck(s.Poly(p,X0).count_roots(s.Rational(-723,1000),s.Rational(-722,1000))==1,'selected_real_embedding')
ck(s.Poly(p,X0).count_roots(-s.oo,s.oo)==2,'two_nonreal_conjugates')
ck(s.Poly(p,X0,modulus=2).is_irreducible,'irreducibility_mod_two')

print(json.dumps({'status':'PASS','exact_controls':sum(counts.values()),'groups':dict(sorted(counts.items())),
 'closed_H1_dimension':6,'relative_H1_dimension':2,'normal_dimension':4,
 'method':'Quaternion-derived adjoints; generic Schreier rewriting; direct kernel modulo conjugation basis and direct 6x6 characteristic polynomial; independent relative-plane injection.',
 'normal_polynomial':'t^4-((53-5sqrt(13))/2)t^3+((705-163sqrt(13))/2)t^2-((53-5sqrt(13))/2)t+1',
 'scope':'Exact frozen-point linearization and geometric input controls, not global ergodicity or a full-measure nonergodicity theorem.'},indent=2,sort_keys=True))
