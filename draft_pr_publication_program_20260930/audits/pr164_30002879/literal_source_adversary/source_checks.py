"""Independent exact GF(2) convention and wrong-module controls.
No candidate verification code or prior review is imported. All failures raise explicitly.
"""
import json
from pathlib import Path

def require(test, message):
    if not test:
        raise RuntimeError(message)

N=7

def add(*vectors):
    result=0
    for v in vectors: result ^= v
    return result

def bits(v):
    return [i for i in range(N) if v >> i & 1]

def bilinear(table,a,b):
    out=0
    for i in bits(a):
        for j in bits(b): out ^= table[i][j]
    return out

# Upper triangular basis f,x,y,xy,e,m0,m1. M=A/(y).
def upper_table(trivial=False):
    t=[[0]*N for _ in range(N)]
    exponents=[(0,0),(1,0),(0,1),(1,1)]
    for i,(a,b) in enumerate(exponents):
        for j,(c,d) in enumerate(exponents):
            if a+c<2 and b+d<2: t[i][j]=1<<exponents.index((a+c,b+d))
    t[4][4]=1<<4
    for j in [5,6]: t[0][j]=1<<j;t[j][4]=1<<j
    if not trivial: t[1][5]=1<<6
    return t

# Actual f*g=f composed with g category convention; X->Y arrows.
def category_table():
    t=[[0]*N for _ in range(N)]
    for i in range(4):
        for j in range(4):t[i][j]=1<<(i^j)
    t[4][4]=1<<4
    for arrow in [5,6]:
        t[4][arrow]=1<<arrow
        for group in range(4):t[arrow][group]=1<<(5+((arrow-5)^(group&1)))
    return t

def rank(vectors,width):
    pivots={}
    for value in vectors:
        while value:
            p=value.bit_length()-1
            if p in pivots:value ^= pivots[p]
            else:pivots[p]=value;break
    return len(pivots)

def center_dimension(t):
    columns=[]
    for k in range(N):
        v=0
        for j in range(N):v |= (t[k][j]^t[j][k]) << (N*j)
        columns.append(v)
    return N-rank(columns,N*N)

def right_projective_dimensions(t):
    # All named idempotents here are primitive: the A corner is local, the K corner simple.
    return sorted(rank([t[e][j] for j in range(N)],N) for e in [0,4])

def check():
    upper=upper_table(); category=category_table(); trivial=upper_table(True)
    # Source basis idX,g,h,gh,idY,alpha,beta mapped into upper radical basis.
    conversion=[1,1^2,1^4,1^2^4^8,16,32,32^64]
    require(rank(conversion,N)==N,'The basis conversion must be invertible')
    def convert(v):return add(*(conversion[i] for i in bits(v)))
    for i in range(N):
        for j in range(N):
            require(convert(category[j][i])==bilinear(upper,conversion[i],conversion[j]),
                    f'Opposite-algebra product identity fails at {i},{j}')
    for name,t in [('upper',upper),('category',category),('trivial',trivial)]:
        for i in range(N):
            for j in range(N):
                for k in range(N):
                    require(bilinear(t,t[i][j],1<<k)==bilinear(t,1<<i,t[j][k]),
                            f'{name} associativity failed at {i},{j},{k}')
    # Source g action on the two arrows is a swap, h is the identity.
    g=[[0,1],[1,0]];h=[[1,0],[0,1]]
    require(category[5][1]==64 and category[6][1]==32,'g is not swapping arrows')
    require(category[5][2]==32 and category[6][2]==64,'h is not fixing arrows')
    require(upper[1][5]==64 and upper[1][6]==0,'x-action does not identify A/(y)')
    require(upper[2][5]==0 and upper[2][6]==0,'y must annihilate M')
    upper_dims=right_projective_dimensions(upper);category_dims=right_projective_dimensions(category)
    require(upper_dims==[1,6] and category_dims==[3,4], 'Wrong orientation diagnostic')
    require(upper_dims!=category_dims,'False literal same-orientation identification went undetected')
    require(center_dimension(upper)==3,'Intended module center dimension mismatch')
    require(center_dimension(trivial)==4,'Wrong trivial module negative control went undetected')
    # The original e=lower K corner gives I=BeB, of dimension three. The multiplication
    # Be tensor_K eB is column-times-row; eB has dimension one, so its three images are independent.
    Be=[bilinear(upper,1<<i,16) for i in range(N)]
    eB=[bilinear(upper,16,1<<j) for j in range(N)]
    I=[bilinear(upper,b,e) for b in Be for e in eB]
    require(rank(Be,N)==3 and rank(eB,N)==1 and rank(I,N)==3,'Stratifying multiplication control failed')
    return {
        'all_checks_passed':True,'field':'GF(2); dimension-independent arguments recorded separately',
        'intended_module_action':{'g':g,'h':h,'radical_x_rank':1,'radical_y_rank':0},
        'opposite_identification_checked_products':49,
        'associativity_checked_basis_triples_per_algebra':343,
        'upper_primitive_right_projective_dimensions':upper_dims,
        'literal_source_category_primitive_right_projective_dimensions':category_dims,
        'literal_same_orientation_isomorphism_negative_control':'FAILS, as required',
        'intended_center_dimension':center_dimension(upper),
        'trivial_two_dimensional_module_center_dimension':center_dimension(trivial),
        'wrong_module_negative_control':'FAILS, as required',
        'stratifying_multiplication_domain_dimension':3,'stratifying_image_dimension':3,
        'limitations':'Finite diagnostics do not certify the all-degree bracket; SOURCE_DERIVATIONS.md supplies independent arguments.'
    }

if __name__=='__main__':
    result=check()
    print(json.dumps(result,indent=2))
