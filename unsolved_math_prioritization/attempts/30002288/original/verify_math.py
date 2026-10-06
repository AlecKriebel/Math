"""Finite corroboration of PROOF.md; not a proof of a continuum statement."""
import sys
if not sys.flags.isolated or not sys.flags.no_site:
    raise SystemExit("Use the separately pinned bootstrap with python -I -S")
import json
import math
from fractions import Fraction as F

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def slope_identity_checks():
    count = 0
    for a in range(1, 7):
        for b in range(0, 7):
            for c in range(0, 7):
                for d in range(0, 7):
                    if c + d == 0:
                        continue
                    h = max(abs(a-c), abs(b-d))
                    numerator = c*b-a*d
                    require(numerator == c*(b-d)+d*(c-a), "polynomial identity")
                    upper = c*(h-b+d)+d*(h-c+a)
                    lower = c*(h+b-d)+d*(h+c-a)
                    require(upper >= 0 and lower >= 0, "nonnegative certificate")
                    require(upper == h*(c+d)-numerator, "upper certificate identity")
                    require(lower == h*(c+d)+numerator, "lower certificate identity")
                    difference = F(c, c+d)-F(a, a+b)
                    require(abs(difference) <= F(h, a+b), "profile slope inequality")
                    count += 1
    return count

def exact_axis_checks():
    def delta(x):
        return max(F(0), min(F(2)-abs(x), F(1)))
    def profile(x, pole):
        a = delta(x)
        return a/(a+abs(x-pole))
    def u(x):
        return max(profile(x, F(-1)), F(3,4)*profile(x,F(1)))
    points = [F(i,8) for i in range(-24,25)]
    inside = [x for x in points if delta(x)>0]
    pair_count = 0
    for x in inside:
        a = delta(x)
        value = u(x)
        for y in points:
            if x != y:
                require(abs(u(y)-value) <= value*abs(x-y)/a, "exact envelope slope")
                pair_count += 1
        if x not in (F(-1),F(1)):
            active = F(-1) if profile(x,F(-1)) >= F(3,4)*profile(x,F(1)) else F(1)
            slope = (u(active)-value)/abs(active-x)
            require(slope == value/a, "active pole equality")
        else:
            require(a == 1, "ridge eigenvalue branch")
    require(u(F(-1)) == 1 and u(F(1)) == F(3,4), "counterexample values")
    require(profile(F(1),F(-1)) == F(1,3), "unweighted comparison value")
    require([x for x in points if u(x)==1] == [F(-1)], "sample maximum set")
    require(u(F(1)) != u(F(-1)), "reflection obstruction")
    return pair_count

def numerical_rectangle_checks():
    """Floating-point sample, explicitly subordinate to the analytic proof."""
    def delta(x):
        return max(0.0, min(2.0-abs(x[0]), 1.0-abs(x[1])))
    def boundary(x):
        if 2-abs(x[0]) <= 1-abs(x[1]):
            return (2.0 if x[0]>=0 else -2.0,x[1])
        return (x[0],1.0 if x[1]>=0 else -1.0)
    a=(-1.0,0.0)
    b=(1.0,0.0)
    inside=[(i/4,j/4) for i in range(-7,8) for j in range(-3,4)]
    exterior=sorted(set(boundary(x) for x in inside))
    points=inside+exterior
    count=0
    for alpha in (0.25,0.5,0.75,1.0):
        def profile(x,pole):
            d=delta(x)**alpha
            return d/(d+math.dist(x,pole)**alpha)
        def u(x):
            return max(profile(x,a),0.75*profile(x,b))
        for x in inside:
            value=u(x)
            bound=value/delta(x)**alpha
            for y in points:
                if x==y:
                    continue
                slope=(u(y)-value)/math.dist(x,y)**alpha
                require(abs(slope)<=bound+2e-12,"sample global slope bound")
                count+=1
            neg=(u(boundary(x))-value)/math.dist(x,boundary(x))**alpha
            require(abs(neg+bound)<2e-12,"sample nearest exterior equality")
            if x not in (a,b):
                pole=a if profile(x,a)>=0.75*profile(x,b) else b
                pos=(u(pole)-value)/math.dist(x,pole)**alpha
                require(abs(pos-bound)<2e-12,"sample active pole equality")
            else:
                require(abs(neg+value)<2e-12,"sample eigenvalue branch")
        require(u(a)==1 and u(b)==0.75,"sample normalized ridge values")
        require(1/(1+2**alpha)<0.5,"sample strict threshold")
    return count

result={
    "schema":"finite-corroboration-v1",
    "problem_id":30002288,
    "exact_slope_identity_cases":slope_identity_checks(),
    "exact_axis_ordered_pairs":exact_axis_checks(),
    "numerical_rectangle_ordered_pairs":numerical_rectangle_checks(),
    "numerical_tolerance":"2e-12",
    "status":"PASS",
    "scope":"Finite arithmetic corroboration only; continuum and viscosity proof is PROOF.md.",
    "compound_problem_status":"PARTIAL: representation counterexample; general p-limit unresolved",
}
sys.stdout.write(json.dumps(result,sort_keys=True,indent=2)+"\n")
