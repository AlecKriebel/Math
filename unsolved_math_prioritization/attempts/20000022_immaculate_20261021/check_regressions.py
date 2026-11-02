"""Bounded independent cohomology evaluations, not a novelty or general proof claim."""
import json

def need(ok,message):
    if not ok: raise ValueError(message)

def cohomology(n,a,b):
    if a==-1: return (0,0,0)
    if a<=-2:
        h=cohomology(n,-2-a,-n-2-b)
        return h[::-1]
    degrees=[b-j*n for j in range(a+1)]
    return (sum(max(k+1,0) for k in degrees),sum(max(-k-1,0) for k in degrees),0)

def classified(n,a,b):
    return a==-1 or (b==-1 if n==0 else (a,b) in [(0,-1),(-2,-n-1)])

# Degree-sensitive independent known witnesses: O, K, and product P1 x P1.
# These constants check H0/H2 placement, not only Euler characteristics or zeros.
witnesses=[(0,0,0,(1,0,0)),(2,1,0,(1,1,0)),
           (0,-3,-3,(0,0,4)),(2,-2,-5,(0,0,2)),
           (2,-2,-2,(0,1,0))]
witnesses += [(n,-2,-n-2,(0,0,1)) for n in range(9)]
for n,a,b,expected in witnesses:
    need(cohomology(n,a,b)==expected,'degree-sensitive cohomology witness')

checks=0
for n in range(9):
    for a in range(-12,13):
        for b in range(-40,41):
            h=cohomology(n,a,b)
            need((not any(h))==classified(n,a,b),'Hirzebruch classification')
            chi=(a+1)*(b+1)-n*a*(a+1)//2
            need(h[0]-h[1]+h[2]==chi,'Euler formula')
            checks+=1
need(cohomology(2,1,0)==(1,1,0),'Euler cancellation at S')
ts=list(range(-60,61))
need(all(sum((1,-1,1)[j]*cohomology(2,t+1,t)[j] for j in range(3))==0 for t in ts),'chi identically zero regression')
need([t for t in ts if not any(cohomology(2,t+1,t))]==[-3,-2,-1],'three immaculate integers')
print(json.dumps({'verdict':'PASS','classification_cases':checks,'degree_sensitive_witnesses':len(witnesses),'family_integer_interval':[-60,60],'immaculate_t':[-3,-2,-1]},sort_keys=True))
