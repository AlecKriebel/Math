"""Independent exact-integer exhaustive verification; units scaled by denominator."""
from itertools import product

def run(a,d,phase):
    a=list(a);n=len(a);M=sum(a)
    target=[max(0,min(d,M-d*(n-i-1))) for i in range(n)]
    if a==target:return 0
    for k in range(1,n+1):
        for i in range((phase+k-1)%2,n-1,2):
            z=a[i]+a[i+1]
            a[i],a[i+1]=max(0,z-d),min(d,z)
        if a==target:return k
    raise RuntimeError('MATHEMATICAL CHECK: exact sorting failed '+str((n,d,phase,a,target)))

if __name__=='__main__':
    cases=0
    for d,N in [(1,13),(2,9),(4,7)]:
        for n in range(1,N+1):
            maxima=[]
            for phase in (0,1):
                worst=0;example=None
                for a in product(range(d+1),repeat=n):
                    k=run(a,d,phase);cases+=1
                    if k>worst:worst=k;example=a
                maxima.append((worst,example))
            print('denominator',d,'n',n,'maxima',maxima,flush=True)
    print('PASS',cases,'initial-state/phase cases')
