"""Document failure of the sufficient raw-signature criterion; not a counterexample."""
from colored_involutions import *

if __name__=='__main__':
    out={}
    for n in (9,10):
        D=alternating_class(n,4);a=D[0]
        S=[s for s in D if compose(a,s)==compose(s,a)];fib={}
        for x in D:
            if compose(a,x)==compose(x,a):continue
            sig=tuple(order(compose(x,s)) for s in S)
            fib.setdefault(sig,[]).append(x)
        out[n]={'vertices':len(D),'commuting':len(S),'fiber_sizes':dict(Counter(map(len,fib.values()))),'two_point_criterion_pass':all(len(f)==2 and compose(compose(a,f[0]),a)==f[1] for f in fib.values())}
        print(n,out[n])
    json.dump(out,open('four_transposition_results.json','w'),indent=2)
