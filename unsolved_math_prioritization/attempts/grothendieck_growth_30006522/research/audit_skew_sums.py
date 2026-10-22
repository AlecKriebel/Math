"""Check skew-sum factorization using independent staircase pipe-dream polynomials."""
from audit_pipe_dreams import pipe_family, accumulate
import itertools, json, os

def skew(a,b): return tuple(x+len(b) for x in a)+tuple(b)

def skew_product(f,g,m,n):
    out = {}
    for p,c in f.items():
        for q,d in g.items():
            accumulate(out, tuple(e+n for e in p)+q, c*d)
    return out

def main(max_n=6):
    families = {n:pipe_family(n) for n in range(1,max_n+1)}
    comparisons = 0; failures = []
    for size in range(2,max_n+1):
        for m in range(1,size):
            n=size-m
            for a in families[m][0]:
                for b in families[n][0]:
                    comparisons += 1
                    w=skew(a,b)
                    for kind in (0,1):
                        if skew_product(families[m][kind][a],families[n][kind][b],m,n) != families[size][kind][w]:
                            failures.append({'a':a,'b':b,'kind':kind})
    result={'max_n':max_n,'skew_sum_instances':comparisons,'polynomial_comparisons':2*comparisons,'failures':failures}
    with open(os.path.join(os.path.dirname(__file__),'independent_skew_sum_audit.json'),'w') as f:json.dump(result,f,indent=2)
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
