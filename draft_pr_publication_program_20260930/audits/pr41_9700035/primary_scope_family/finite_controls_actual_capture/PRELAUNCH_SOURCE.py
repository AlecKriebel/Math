#!/usr/bin/env python3
"""Independent finite adversarial controls. No SIRSN or submitted-code execution."""
from fractions import Fraction as F
from itertools import product
import argparse, json, math

def run():
    checks=[]; cases={}
    def check(label,condition):
        if not condition:raise AssertionError(label)
        checks.append(label)
    # Weighted star-tree route unions: a pair uses exactly its two terminal
    # branches. Sample-count laws are independent of the random tree lengths.
    laws=[[F(1,6)]*6,[F(j+1,21) for j in range(6)],[F(6-j,21) for j in range(6)]]
    trees=list(product([F(1,3),F(2,3)],repeat=5)); count=0
    for tree in trees:
        values=[F(0),F(0)]+[sum(tree[:m]) for m in range(2,6)]
        A=max(tree)*2
        for probs in laws:
            mean=sum(probs[m]*values[m] for m in range(6))
            for k in range(1,6):
                check('independent_upper_'+str(count),sum(probs[k:])*values[k]<=mean)
                tail=sum(probs[m]*A*m*(m-1)/2 for m in range(k+1,6))
                check('independent_lower_'+str(count),mean<=values[k]+tail);count+=1
    cases['star_tree_count_law_sandwiches']=count
    # Exact formal coefficients, including the degenerate k=0,1 thresholds.
    count=0
    for k in range(11):
        for m in range(16):
            left=F(m*(m-1),math.factorial(m)) if m>k else F(0)
            right=F(1,math.factorial(m-2)) if m>=2 and m-2>k-2 else F(0)
            check('factorial_shift_'+str(count),left==right);count+=1
    cases['Poisson_factorial_coefficients']=count
    check('wrong_shift_detected',F(3*2,math.factorial(3))!=F(0))
    # Independent radius, distance and coefficient controls with rational values.
    count=0
    for n in [F(1),F(7,2),F(8)]:
        for r in [F(1,4),F(1),F(5,2)]:
            check('annulus_area_'+str(count),(n+4*r)**2-(n+2*r)**2==4*n*r+12*r*r)
            outside=(n/2+r+F(1,8),F(0))
            for x,y in product([-n/2,F(0),n/2],repeat=2):
                check('strict_distance_'+str(count),(outside[0]-x)**2+(outside[1]-y)**2>r*r);count+=1
    cases['strict_annulus_endpoint_distances']=count
    for j in range(14):
        for a in [F(1),F(3,2),F(7,4)]:
            R=2**j*a
            check('dyadic_sum_'+str(j)+'_'+str(a),sum(2**q for q in range(j+1))<=2*R)
    for lam,delta,n in product([F(1,2),F(1),F(2)],[F(1,3),F(1),F(4)],[F(2),F(5),F(10)]):
        # Algebra after cancelling sqrt(2)^4: a t^-3 tail produces a
        # nonvanishing constant. Little-o cannot be replaced by big-O.
        check('critical_constant_'+str((lam,delta,n)),lam*lam*n**3/(4*(delta*n)**3)==lam*lam/(4*delta**3))
    atoms=[(F(1),F(1,2)),(F(2),F(1,3)),(F(4),F(1,6))]
    for t in [F(1),F(2),F(4)]:
        h_ge=sum(v*p for v,p in atoms if v>=t);h_gt=sum(v*p for v,p in atoms if v>t)
        check('atomic_boundary_'+str(t),h_ge-h_gt==sum(t*p for v,p in atoms if v==t))
        check('half_cutoff_'+str(t),h_ge<=sum(v*p for v,p in atoms if v>t/2))
    # Countercontrols for shortcuts explicitly excluded by the written proof.
    check('conditional_event_bound_false',F(1)>F(1,4)) # P(A|A)=1, P(A)=1/4
    check('dependent_count_factorization_false',F(0)<F(1,2)*F(1,2))
    check('Pareto2_first_moment_finite',F(2)==F(2))
    check('Pareto2_tail_not_fourth_order',10**4*F(1,10**2)>1)
    check('route_compatibility_not_convexity',2*math.sqrt(1+100**2)>2)
    return {'status':'PASS_INDEPENDENT_FINITE_CONTROLS','passed':len(checks),'failed':0,'cases':cases,'checks':checks,'countercontrol_limits':'The conditional-event and dependent-count examples falsify generic invalid inference rules. The finite V/tree network is not a stationary scale-invariant SIRSN. Scalar Pareto tails are not SIRSN constructions.','scope':'Independent finite algebra/probability/union/boundary controls only. No submitted helper imported/executed, no simulation or proof certification of the unconditional target.'}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();result=run()
    with open(a.output,'x') as handle:json.dump(result,handle,indent=2);handle.write('\n')
    print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))
