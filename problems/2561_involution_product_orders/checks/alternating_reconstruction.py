"""Bounded-support exact certificate for the A_n double-transposition family."""
from colored_involutions import *

def local_signature_certificate(n):
    D=alternating_class(n,2);a=D[0];S=[b for b in D if compose(a,b)==compose(b,a)];F={}
    for x in D:
        if compose(a,x)==compose(x,a):continue
        sig=tuple(order(compose(x,s)) for s in S)
        F.setdefault(sig,[]).append(x)
    sizes=dict(Counter(map(len,F.values())))
    good=all(len(f)==2 and compose(compose(a,f[0]),a)==f[1] for f in F.values())
    return {'degree':n,'class_size':len(D),'commuting_vertices':len(S),'signature_fiber_sizes':sizes,'all_noncommuting_fibers_are_conjugate_pairs':good}

if __name__=='__main__':
    results={}
    for n in range(8,13):
        t=time.monotonic();results[n]=local_signature_certificate(n);results[n]['seconds']=round(time.monotonic()-t,3)
        print(n,results[n],flush=True)
    with open('alternating_reconstruction_results.json','w') as f:json.dump(results,f,indent=2)
