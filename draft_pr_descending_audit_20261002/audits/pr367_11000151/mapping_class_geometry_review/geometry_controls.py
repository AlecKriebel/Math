"""Independent source-derived exact controls; standard library only."""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent

def eye(n): return [[int(i == j) for j in range(n)] for i in range(n)]
def mm(a,b): return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]
def mp(a,n):
    r=eye(len(a))
    while n:
        if n&1: r=mm(r,a)
        a=mm(a,a);n//=2
    return r

def product(g,w):
    r=eye(len(g[0]))
    for i in w: r=mm(r,g[i-1])
    return r

J=[[0,1,0,0],[-1,0,0,0],[0,0,0,1],[0,0,-1,0]]
V=[[1,0,0,0],[0,1,0,0],[1,0,-1,0],[0,0,0,1],[0,0,1,0]]
def twist(v):
    cov=[sum(v[k]*J[k][j] for k in range(4)) for j in range(4)]
    return [[int(i==j)+v[i]*cov[j] for j in range(4)] for i in range(4)]
G=list(map(twist,V))
c=[1,2,3,4];h=[5,4,3,2,1,1,2,3,4,5];d=[1,2,3,4,5]
negI=[[-int(i==j) for j in range(4)] for i in range(4)]
checks={}
for i in range(5):
    for j in range(i+1,5):
        w1=[i+1,j+1,i+1] if j==i+1 else [i+1,j+1]
        w2=[j+1,i+1,j+1] if j==i+1 else [j+1,i+1]
        checks[f'chain_braid_or_commute_{i+1}_{j+1}']=product(G,w1)==product(G,w2)
checks['c5_equals_h_on_integral_homology']=product(G,c*5)==product(G,h)
checks['c5_is_minus_identity']=product(G,c*5)==negI
checks['h_is_minus_identity']=product(G,h)==negI
checks['c10_identity_on_integral_homology']=product(G,c*10)==eye(4)
checks['five_chain6_identity_on_integral_homology']=product(G,d*6)==eye(4)
checks['h2_identity_on_integral_homology']=product(G,h*2)==eye(4)
A=[[1,1],[0,1]];B=[[1,0],[-1,1]]
checks['torus_braid']=mm(mm(A,B),A)==mm(mm(B,A),B)
checks['torus_chain6_identity_closed_homology']=mp(mm(A,B),6)==eye(2)

# Faithful Artin action of B6 on the free group with six named generators.
def reduce(w):
    r=[]
    for x in w:
        if r and r[-1]==-x:r.pop()
        else:r.append(x)
    return tuple(r)
def inv(w):return tuple(-x for x in reversed(w))
def subst(w,images):
    r=()
    for x in w:r=reduce(r+(images[x-1] if x>0 else inv(images[-x-1])))
    return r
I=tuple((i,) for i in range(1,7))
S=[]
for i in range(1,6):
    a=list(I);a[i-1]=(i,i+1,-i);a[i]=(i,);S.append(tuple(a))
def automorphism(w):
    r=I
    for i in w:r=tuple(subst(a,r) for a in S[i-1])
    return r
checks['braid_B6_splitting_identity_C6_equals_c5h']=automorphism(d*6)==automorphism(c*5+h)
P=tuple(range(1,7))
checks['B6_full_twist_conjugates_by_total_product']=automorphism(d*6)==tuple(reduce(P+(i,)+inv(P)) for i in range(1,7))
checks['quotient_relator_is_nontrivial_in_B6']=automorphism(c*5)!=automorphism(h)

# Adjacent transpositions are an S6 quotient. Both sides of the added
# relation are identity, hence this descends to Q. Transitivity is about
# the factor subgroup, not just the image of their product.
def permutation(w):
    r=list(range(1,7))
    for i in w:r[i-1],r[i]=r[i],r[i-1]
    return r
checks['quotient_relation_passes_S6']=permutation(c*5)==permutation(h)
checks['four_chain_factors_fix_sixth_point']=all(i<=4 for i in c*10)
checks['five_chain_factors_connect_all_six_points']=set(d)==set(range(1,6))

# Exact finite-image false positive with a priori Q inequality by abelianization.
# Both all chain transvections modulo3 and adjacent transpositions kill a1^6.
false_word=c*10+[1]*6
checks['finite_S6_false_positive']=permutation(false_word)==permutation(c*10)
checks['finite_Sp4_F3_false_positive']=[[x%3 for x in row] for row in product(G,false_word)]==[[x%3 for x in row] for row in product(G,c*10)]
checks['false_positive_excluded_in_Q_by_length_mod10']=len(false_word)%10!=len(c*10)%10
report={'all_checks_pass':all(checks.values()),'checks':checks,
        'c5_integral_homology':product(G,c*5),'h_integral_homology':product(G,h),
        'quotient_abelianization':'Z/10: all generators become x; added relation 20x=10x',
        'finite_collision_word':false_word,'finite_collision_length':len(false_word),
        'finite_collision_target_length':len(c*10),
        'limitation':'Homology identity is necessary, never a boundary equality or Hurwitz classification; false positive is in S6 x Sp4(F3), not in Q.'}
(OUT/'geometry_controls.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
assert all(checks.values())
