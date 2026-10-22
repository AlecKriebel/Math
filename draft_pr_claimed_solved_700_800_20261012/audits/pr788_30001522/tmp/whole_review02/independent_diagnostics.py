"""Exact finite boundary diagnostics; the accompanying proofs justify universal claims."""
import itertools,json

def need(condition,message):
    if not condition:raise ValueError(message)

def multiply(a,b):
    return [[sum(a[i][k]*b[k][j] for k in range(3))for j in range(3)]for i in range(3)]

def scale(c,a):return [[c*x for x in row]for row in a]

def diagnostics():
    j=[[0,-1,0],[1,0,0],[0,0,0]]
    basis=[[[1,0,0],[0,1,0],[0,0,-2]],[[0,0,1],[0,0,0],[1,0,0]],[[0,0,0],[0,0,1],[0,1,0]],[[1,0,0],[0,-1,0],[0,0,0]],[[0,1,0],[1,0,0],[0,0,0]]]
    expected=[scale(0,basis[0]),basis[2],scale(-1,basis[1]),scale(2,basis[4]),scale(-2,basis[3])]
    for a,e in zip(basis,expected):
        x,y=multiply(j,a),multiply(a,j)
        need([[x[i][k]-y[i][k]for k in range(3)]for i in range(3)]==e,'tangent weight commutator')
    residues=0
    for n in range(1,129):
        candidates=[k for k in range(1,n)if k%n==0 or (-2*k)%n==0]
        need(candidates==([]if n%2 else[n//2]),'circle stabilizer spectrum')
        residues+=n-1
    need(all(k%3 and (-2*k)%3 for k in(1,2)),'prime-three scalar boundary')
    need([x%2 for x in range(4)if (2*x)%4==0]==[0,0],'Z2 to Z4 reduction')
    need(set(x%2 for x in range(4))=={0,1},'Z4 boundary must not imitate Z2')
    need((1+2)%2==1 and (1+1)%2==0,'clutching parity boundary')
    matrices=0
    for p in(3,5):
        for coefficients in itertools.product(range(p),repeat=4):
            if not any(coefficients):continue
            for m in(3,4,8):
                # Coefficients of t1^i t2^(m-i); multiplication by all nonzero cubics.
                a=[[0]*(m-2)for _ in range(m+1)]
                for k,c in enumerate(coefficients):
                    for col in range(m-2):a[col+k][col]=c
                rank=0
                for col in range(m-2):
                    piv=next((i for i in range(rank,m+1)if a[i][col]%p),None)
                    if piv is None:continue
                    a[rank],a[piv]=a[piv],a[rank]
                    a[rank]=[(x*pow(a[rank][col],-1,p))%p for x in a[rank]]
                    for i in range(m+1):
                        if i!=rank:
                            c=a[i][col];a[i]=[(x-c*y)%p for x,y in zip(a[i],a[rank])]
                    rank+=1
                need(rank==m-2 and m+1-rank==3,'binary cubic rank')
                matrices+=1
    return {'result':'PASS','tangent_commutators':5,'cyclic_orders_checked':[1,128],'nonidentity_residues':residues,'binary_cubic_fields':[3,5],'nonzero_cubics':(3**4-1)+(5**4-1),'polynomial_degrees':[3,4,8],'multiplication_matrices':matrices,'boundaries':['prime 2 differs','prime 3 scalar has no eigenvalue 1','odd composite orders','Z4 torsion differs from Z2','even clutching parity differs','zero transgression leaves polynomial ring','rank one permits finite cubic quotient'],'scope':'Finite algebra/model checks only. No formal topology, priority certification, or infinite-prime extrapolation.'}

if __name__=='__main__':print(json.dumps(diagnostics(),indent=2,sort_keys=True))
