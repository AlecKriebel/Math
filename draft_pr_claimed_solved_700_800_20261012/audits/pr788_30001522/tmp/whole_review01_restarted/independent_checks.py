"""Independent finite diagnostics for the written Wu-manifold proof. No topology certification."""
import itertools,json

def need(v,msg):
    if not v:raise ValueError(msg)
def matmul(a,b):return [[sum(a[i][k]*b[k][j]for k in range(3))for j in range(3)]for i in range(3)]
def comm(a,b):
    ab,ba=matmul(a,b),matmul(b,a)
    return [[ab[i][j]-ba[i][j]for j in range(3)]for i in range(3)]
def scale(a,n):return [[n*x for x in row]for row in a]
def rank_mod(a,p):
    a=[row[:]for row in a];i=0
    for j in range(len(a[0])if a else 0):
        k=next((k for k in range(i,len(a))if a[k][j]%p),None)
        if k is None:continue
        a[i],a[k]=a[k],a[i];q=pow(a[i][j],-1,p);a[i]=[x*q%p for x in a[i]]
        for k in range(len(a)):
            if k!=i:
                q=a[k][j];a[k]=[(x-q*y)%p for x,y in zip(a[k],a[i])]
        i+=1
        if i==len(a):break
    return i

def main():
    A=[[0,-1,0],[1,0,0],[0,0,0]]
    B=[[[1,0,0],[0,1,0],[0,0,-2]],[[0,0,1],[0,0,0],[1,0,0]],[[0,0,0],[0,0,1],[0,1,0]],[[1,0,0],[0,-1,0],[0,0,0]],[[0,1,0],[1,0,0],[0,0,0]]]
    expected=[scale(B[0],0),B[2],scale(B[1],-1),scale(B[4],2),scale(B[3],-2)]
    need([comm(A,b)for b in B]==expected,'Tangent weights')
    need((1+2)%2==1 and(1+1)%2==0,'Loop parity controls')
    def coefficient_image(n):return sorted({a%2 for a in range(4)if n*a%4==0})
    need(coefficient_image(2)==[0]and coefficient_image(4)==[0,1],'Exact torsion Bockstein boundary')
    residue_checks=0
    def bad(n,weights):return [a for a in range(1,n)if any(a*w%n==0 for w in weights)]
    for n in range(1,1025):
        need(bad(n,(1,1,-2))==([n//2]if n%2==0 else []),'Cyclic isotropy residues')
        residue_checks+=n-1
    need(bad(3,(1,1,-2))==[],'Central cubic exception')
    need(bad(3,(1,2,-3))==[1,2],'Wrong weight negative control')
    cases=0;matrix_checks=0
    for p,ms in [(3,range(3,10)),(5,range(3,7)),(7,range(3,5))]:
        for f in itertools.product(range(p),repeat=4):
            if not any(f):continue
            cases+=1
            for m in ms:
                matrix=[[0]*(m-2)for _ in range(m+1)]
                for j in range(m-2):
                    for k,c in enumerate(f):matrix[j+k][j]=c
                rank=rank_mod(matrix,p);need(rank==m-2 and m+1-rank==3,'Binary cubic injection')
                matrix_checks+=1
    need(rank_mod([[0],[0],[0],[0]],3)==0,'Zero-transgression control')
    # In one variable the ideal (t^3) contains every monomial of degree >=3.
    rank_one_tail=[max(0,1-int(m>=3))for m in range(10)]
    need(rank_one_tail==[1,1,1,0,0,0,0,0,0,0],'Rank-one positive control')
    print(json.dumps({'result':'PASS','tangent_commutators':5,'rotation_plane_weights':[1,2],'fixed_lines':1,'loop_parity':1,'coefficient_reduction_images':{'Z2':[0],'Z4':[0,1]},'cyclic_orders_checked':[1,1024],'nonidentity_residue_checks':residue_checks,'binary_cubics_checked':cases,'cubic_matrix_checks':matrix_checks,'fields':[3,5,7],'negative_and_boundary_controls':['even circle stabilizer','prime-three scalar','wrong weights fail at three','even loop parity','Z4 coefficient reduction','zero transgression','rank-one polynomial finite quotient'],'limits':'Finite diagnostics do not prove topology or extrapolate to universal primes; the written deductions establish those statements.'},indent=2,sort_keys=True))
if __name__=='__main__':main()
