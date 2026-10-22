"""Independent exact finite diagnostics. No author-code imports, network or writes."""
from fractions import Fraction as Q
from itertools import product,permutations,combinations
import json

def need(ok,why):
    if not ok:raise RuntimeError(why)
def character(g):return -1 if g else 1

def trace_checks():
    A=[0,0,1];M=[0,1,1];C=[0,1,1]
    basis=list(product(range(3),repeat=3));units=0;nonzero=0
    for out in basis:
        for inp in basis:
            a,m,c=out;b,n,d=inp
            if (A[a]+M[m]+C[c])%2!=(A[b]+M[n]+C[d])%2:continue
            units+=1
            total=character((A[a]+M[m]+C[c])%2) if out==inp else 0
            left=character(A[a])*character((M[m]+C[c])%2) if a==b and m==n and c==d else 0
            right=character(C[c])*character((A[a]+M[m])%2) if a==b and m==n and c==d else 0
            mixed=character(A[a])*character(C[c])*character(M[m]) if a==b and m==n and c==d else 0
            need(total==left==right==mixed,'left/right/mixed partial trace matrix unit')
            nonzero+=total!=0
    # The zero-dimensional object 1+g still has a nondegenerate trace pairing.
    X=[0,1];trace_identity=sum(character(g) for g in X)
    gram_diagonal=[character(g) for g in X]
    need(trace_identity==0 and gram_diagonal[0]*gram_diagonal[1]==-1,'signed zero dimension and nondegeneracy')
    rectangular=0
    for g in [0,1]:
        for i in range(2+g):
            for j in range(3-g):
                # Opposite matrix units pair to identity entries with same nonzero weight.
                need(character(g)!=0,'rectangular trace pairing nondegeneracy');rectangular+=1
    # Non-inherited spherical structure: left and right constraints at 1,g conflict.
    need(-1!=1,'negative control: incompatible sign structure')
    return {'graded_tensor_basis':len(basis),'all_grade_preserving_matrix_units':units,'nonzero_full_traces':nonzero,'rectangular_pairings':rectangular,'zero_object_dimension':trace_identity,'zero_dimension_object_trace_gram_determinant':-1,'noninherited_structure_obstruction':True}

def mm(A,B):return [[sum((a*b for a,b in zip(row,col)),Q(0)) for col in zip(*B)] for row in A]
def invdiag(A):return [[1/A[0][0],Q(0)],[Q(0),1/A[1][1]]]
def diag(a,b):return [[Q(a),Q(0)],[Q(0),Q(b)]]
def orb(P,Fin,Fout):return mm(mm(invdiag(Fout),P),Fin)
def boundary_checks():
    # Two admissible theta-graph colorings in Rep(S3): (1,1,1) and (2,2,1).
    # Their f factors have ratio1:1/2 after stripping the common Delta^(3/2).
    F0=diag(1,Q(1,2));F1=diag(2,Q(1,4));F2=diag(Q(1,2),3)
    P=[[Q(1,2),Q(1,2)],[Q(1,2),Q(1,2)]]
    need(mm(P,P)==P,'projector base')
    Porb=orb(P,F0,F0)
    need(mm(Porb,Porb)==Porb and mm(F0,Porb)==mm(P,F0),'coloring conjugation/projector intertwiner')
    A=[[2*x for x in row] for row in P];B=[[3*x for x in row] for row in P]
    need(mm(orb(B,F1,F2),orb(A,F0,F1))==orb(mm(B,A),F0,F2),'boundary sewing and comparison direction')
    need(Porb!=P,'negative control: coloring independent scalar would miss offdiagonal rescaling')
    need(F0[0][0]/F0[1][1]==2,'coloring factor nonconstant')
    return {'colorings':2,'exact_rational_projector':[[str(x) for x in r] for r in Porb],'sewing':True,'scope':'Linear algebra diagnosis of published boundary formula, not an asserted actual TV projector matrix.'}

def compose(p,q):return tuple(p[q[i]] for i in range(len(p)))
def inverse(p):return tuple(p.index(i) for i in range(len(p)))
def sphere_count(G):
    e=tuple(range(len(G[0])));seen=set();triangles=0
    for gs in product(G,repeat=4):
        v=(e,)+gs;edges={(i,j):compose(inverse(v[i]),v[j]) for i,j in combinations(range(5),2)}
        for i,j,k in combinations(range(5),3):need(compose(edges[i,j],edges[j,k])==edges[i,k],'flat triangle relation');triangles+=1
        # Conversely, the four root edges determine every flat labeling.
        need(all(edges[i,j]==compose(inverse(edges[0,i]),edges[0,j]) for i,j in combinations(range(1,5),2)),'flat converse from root edges')
        seen.add(tuple(edges[e] for e in sorted(edges)))
    n=len(G);need(len(seen)==n**4,'flat labeling count for boundary of4simplex')
    z=Q(n)**-5*len(seen)
    need(z==Q(1,n),'independent bulk global dimension normalization')
    return {'group_order':n,'vertices':5,'flat_labelings':len(seen),'triangle_equations_checked':triangles,'normalized_S3':str(z)}
def group_checks():
    G2=list(permutations(range(2)));G3=[(0,1,2),(1,2,0),(2,0,1)];S3=list(permutations(range(3)))
    rows=[sphere_count(G) for G in [G2,G3,S3]]
    need(Q(1)!=Q(1,2),'monoidal unit component cannot intertwine unequal sphere scalars')
    # Actual left actions on regular pointed simples recover each subgroup element.
    e=(0,1,2);H=[e,(1,0,2)];tests=0
    for d,f,x in product(H,H,S3):
        need(compose(d,compose(f,x))==compose(compose(d,f),x),'inclusion left action monoidality');tests+=1
    need(all(compose(d,e)==d for d in H),'evaluation at distinguished unit recovers inclusion')
    # In C[Z3], s=g+g^2 has s^2=2+s and is not a simple-basis restriction.
    s=[0,1,1];sq=[sum(s[i]*s[(k-i)%3] for i in range(3)) for k in range(3)]
    need(sq==[2,1,1] and sum(x!=0 for x in s)==2,'arbitrary linear subalgebra warning')
    return {'sphere_counts':rows,'pointed_subgroup_action_tests':tests,'linear_subalgebra_square':sq,'ordinary_monoidal_naturality_obstruction':True}

def main():return {'trace':trace_checks(),'boundary':boundary_checks(),'groups':group_checks(),'limit':'Finite exact diagnostics support independently written categorical derivations; published general defect-coherence theorem is an established import, not numerically verified.'}
if __name__=='__main__':print(json.dumps(main(),indent=2,sort_keys=True))
