#!/usr/bin/env python3
"""Read-only independent finite checks; no candidate code, network, or writes.
These finite controls support, rather than replace, the all-field proof in REVIEW.md.
"""
import json

def require(ok, message):
    if not ok:
        raise ValueError(message)

def rank(vectors, p):
    a=[list(v) for v in vectors]; r=0
    for c in range(2):
        k=next((k for k in range(r,len(a)) if a[k][c]%p),None)
        if k is None: continue
        a[r],a[k]=a[k],a[r]; inv=pow(a[r][c]%p,-1,p)
        a[r]=[(v*inv)%p for v in a[r]]
        for k in range(len(a)):
            if k!=r:
                q=a[k][c];a[k]=[(x-q*y)%p for x,y in zip(a[k],a[r])]
        r+=1
    return r

def main():
    # Ground element 0 is F^2; 1,2,3 are three distinct lines, even over F_2.
    spaces=[[(1,0),(0,1)],[(1,0)],[(0,1)],[(1,1)]]
    results=[]
    for p in (2,3,5,7):
        for mask in range(16):
            vs=[v for i,u in enumerate(spaces) if mask>>i&1 for v in u]
            expected=min(2,2*(mask&1)+sum((mask>>i)&1 for i in (1,2,3)))
            require(rank(vs,p)==expected,'all-field specialization rank mismatch')
        results.append({'field':p,'subsets':16,'passed':True})
    def f(s):return min(2,sum(2 if i==0 else 1 for i in s))
    H=[[f({i,j})-f({i})-f({j}) for j in range(4)] for i in range(4)]
    v=[1,-1,-1,-1]; value=sum(v[i]*H[i][j]*v[j] for i in range(4) for j in range(4))
    require(value==1,'Hessian witness mismatch')
    # All ranks on <=4 points induced by a partition into parallel classes (loops omitted):
    # each Hessian is block -ones, so quadratic form is minus sum block sums squared.
    for mask in range(16):
        active=[i for i in range(4) if mask>>i&1]
        def partitions(xs):
            if not xs:yield [];return
            for tail in partitions(xs[1:]):
                yield [[xs[0]]]+[b[:] for b in tail]
                for k in range(len(tail)):
                    q=[b[:] for b in tail];q[k].append(xs[0]);yield q
        for blocks in partitions(active):
            matrix=[[-int(any(i in b and j in b for b in blocks)) for j in range(4)] for i in range(4)]
            q=sum(v[i]*matrix[i][j]*v[j] for i in range(4) for j in range(4))
            require(q==-sum(sum(v[i] for i in b)**2 for b in blocks),'parallel class identity mismatch')
    # Bell GE comparison reduces by monotonicity of logarithm to (9/5)^2>3.
    require(81>75,'Bell comparison failed')
    print(json.dumps({'independent_code':True,'finite_field_specializations':results,'polymatroid_H':H,'positive_quadratic_form':value,'nonnegative_MRS_obstruction':'negative all-ones parallel-class blocks','Bell_log_inequality':'81 > 75','limits':'Finite checks do not establish entire prior paper correctness or priority.'},indent=2))
if __name__=='__main__':main()
