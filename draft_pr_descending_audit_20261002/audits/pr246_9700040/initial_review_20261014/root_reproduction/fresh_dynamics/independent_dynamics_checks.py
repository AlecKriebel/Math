#!/usr/bin/env python3
"""Independent finite controls. Standard library; no submitted code imports.

Run from any directory. JSON goes to stdout; optional --output PATH must be
inside this audit family directory. These finite controls support, and do not
replace, the analytic construction/uniqueness proof.
"""
from __future__ import annotations
import argparse
import bisect
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import itertools
import json
import math
from pathlib import Path
import random


def tops_greedy(values):
    tops=[]
    for u in values:
        i=bisect.bisect_right(tops,u)
        if i==len(tops): tops.append(u)
        else: tops[i]=u
    return tops


def terminal_minima_dp(values):
    # Independent O(n^2) recurrence, no patience sorting or determinant calls.
    lengths=[]
    for j,u in enumerate(values):
        lengths.append(1+max((lengths[i] for i in range(j) if values[i]<u),default=0))
    longest=max(lengths,default=0)
    return [min(u for u,d in zip(values,lengths) if d>=r) for r in range(1,longest+1)]


def exhaustive_rectangle_control():
    permutations=prefixes=rectangle_restrictions=count_identities=0
    for n in range(9):
        for perm in itertools.permutations(range(1,n+1)):
            permutations+=1
            for j in range(n+1):
                values=perm[:j]
                full=tops_greedy(values)
                assert full==terminal_minima_dp(values),(perm,j)
                prefixes+=1
                for m in range(n+1):
                    truncated=[u for u in values if u<=m]
                    expected=terminal_minima_dp(truncated)
                    actual=[u for u in full if u<=m]
                    assert actual==expected,(perm,j,m)
                    rectangle_restrictions+=1
                    assert len(expected)==sum(u<=m for u in full)
                    count_identities+=1
    return {'max_n':8,'permutations':permutations,'prefixes':prefixes,'rectangle_restrictions':rectangle_restrictions,'count_identities':count_identities,'status':'PASS'}


def update_fixed(state,event):
    # Work directly in Y coordinates at the event time.
    for i,x in enumerate(state):
        if x>event:
            state[i]=event
            return i
    return None


def transformed_path_control():
    rng=random.Random(9700040)
    trials=events_checked=projection_checks=0
    for trial in range(1000):
        # Five guaranteed initial chains, then random distinct rational events.
        events=[(Fraction(i),Fraction(i)) for i in range(1,6)]
        us=rng.sample([u for u in range(1,2001) if u not in (73,146,219,292,365)],60)
        for j,u in enumerate(us,1):
            events.append((Fraction(u,73),Fraction(500+j,100)))
        events.sort(key=lambda p:p[1])
        at_start=[u for u,v in events if v<=5]
        base=terminal_minima_dp(at_start)
        assert len(base)>=5
        states={k:[5*u for u in base[:k]] for k in range(1,6)}
        old_v=Fraction(5)
        history=list(at_start)
        for u,v in events:
            if v<=5: continue
            # Exact drift is multiplication by v/old_v because s=log(v).
            for state in states.values():
                for i in range(len(state)): state[i]*=v/old_v
                update_fixed(state,u*v)
            history.append(u)
            expected=terminal_minima_dp(history)
            for k,state in states.items():
                assert state==[v*z for z in expected[:k]],(trial,u,v,k)
                assert all(0<state[i] and (i==0 or state[i-1]<state[i]) for i in range(k))
                if k<5:
                    assert state==states[5][:k]
                    projection_checks+=1
            events_checked+=1
            old_v=v
        trials+=1
    return {'seed':9700040,'trials':trials,'post_initial_events':events_checked,'finite_projection_checks':projection_checks,'exact_arithmetic':'fractions.Fraction','status':'PASS'}


def deterministic_coupling_control():
    # Coalesced lower coordinates jump twice before the strip forces i=3.
    # Work in w=x/exp(s), so drift disappears; q=exp(s) is rational.
    left=[Fraction(2),Fraction(5),Fraction(7),Fraction(15)]
    right=[Fraction(2),Fraction(5),Fraction(11),Fraction(20)]
    b=Fraction(5); a=Fraction(7)
    events=[(Fraction(2),Fraction(1)),(Fraction(3),Fraction(7,2)),(Fraction(4),Fraction(9)),(Fraction(5),Fraction(6))]
    lower_jumps=0
    for q,w in events:
        # Every (event x=q*w,s=log q) is handled directly.
        yl=[q*x for x in left]; yr=[q*x for x in right]
        i=update_fixed(yl,q*w); update_fixed(yr,q*w)
        left=[x/q for x in yl]; right=[x/q for x in yr]
        if i is not None and i<2: lower_jumps+=1
        assert left[:2]==right[:2]
        assert left[1]<=b
        if left[2]!=right[2]: assert min(left[2],right[2])==a
        if b<w<a: assert left[2]==right[2]
    assert left[:3]==right[:3]
    # Event below lower coordinates can be removed from i-th dynamics; last event forces agreement.
    return {'lower_jumps_before_coalescence':lower_jumps,'coalesced_coordinates':3,'moving_strip_in_scaled_coordinates':[str(b),str(a)],'status':'PASS'}


def crossing_and_stopping_state_control():
    rng=random.Random(2469700040)
    trials=crossings=event_checks=random_stage_starts=lower_jumps=0
    for trial in range(1000):
        k=5
        left=[Fraction(x,97) for x in sorted(rng.sample(range(1,2001),k))]
        right=[Fraction(x,97) for x in sorted(rng.sample(range(1,2001),k))]
        diffs=[x-y for x,y in zip(left,right)]
        if min(diffs)<0<max(diffs): crossings+=1
        stage=None; saved_a=saved_b=None
        # Independent future sample used for a pathwise control, not claimed to be a PPP sample.
        forbidden=set(left+right)
        event_pool=[x for x in range(1,4500) if Fraction(x,211) not in forbidden]
        events=[Fraction(x,211) for x in rng.sample(event_pool,500)]
        for w in events:
            first=next((i for i in range(k) if left[i]!=right[i]),k)
            if first==k: break
            if first!=stage:
                stage=first
                saved_a=min(left[first],right[first])
                saved_b=left[first-1] if first else Fraction(0)
                random_stage_starts+=1
            assert left[:first]==right[:first]
            old_lower=left[first-1] if first else Fraction(0)
            update_fixed(left,w); update_fixed(right,w)
            assert all(left[j]<left[j+1] and right[j]<right[j+1] for j in range(k-1))
            assert left[:first]==right[:first]
            if first and left[first-1]<old_lower: lower_jumps+=1
            if left[first]!=right[first]:
                assert min(left[first],right[first])==saved_a
            if first: assert left[first-1]<=saved_b
            if saved_b<w<saved_a: assert left[first]==right[first]
            event_checks+=1
        # Finite samples need not coalesce. Explicit forcing events then check all stages.
        for i in range(k):
            assert left[:i]==right[:i]
            if left[i]!=right[i]:
                lower=left[i-1] if i else Fraction(0)
                forcing=(lower+min(left[i],right[i]))/2
                update_fixed(left,forcing); update_fixed(right,forcing)
                assert left[:i+1]==right[:i+1]
        assert left==right
        trials+=1
    assert crossings>0 and lower_jumps>0
    return {'seed':2469700040,'trials':trials,'crossing_initial_pairs':crossings,'events_checked':event_checks,'random_stage_starts':random_stage_starts,'coalesced_lower_coordinate_jumps':lower_jumps,'sampling_limit':'arbitrary exact finite event histories; no statistical assertion','status':'PASS'}


def analytic_controls():
    moment_residuals={}
    for p in range(13):
        residual=Fraction(p*math.factorial(p))-Fraction(p,p+1)*math.factorial(p+1)
        assert residual==0
        moment_residuals[str(p)]=str(residual)
    semigroup=[]
    for t in (0.0,0.25,1.0,3.0):
        for z in (0.125,1.0,4.0):
            result=math.exp(-z*math.exp(-t))*math.exp(-z*(1-math.exp(-t)))
            assert math.isclose(result,math.exp(-z),rel_tol=2e-15)
            semigroup.append({'t':t,'z':z,'stationary_survival':result,'expected':math.exp(-z)})
    a=0.01; larger=100.0
    survival_at_one=math.exp(-a*math.expm1(1.0))
    source_claimed_upper=1/(larger-a)
    assert survival_at_one>source_claimed_upper
    # E[T]>=P(T>1), sufficient for an analytic contradiction; no integration oracle.
    e_upper=sum((Fraction(1,math.factorial(n)) for n in range(9)),Fraction(0))+Fraction(1,math.factorial(9))/Fraction(9,10)
    exact_survival_lower=1-Fraction(1,100)*(e_upper-1)
    exact_source_bound=Fraction(100,9999)
    assert exact_survival_lower/exact_source_bound>98
    counterexample={'exact_rational_survival_lower_bound':str(exact_survival_lower),'exact_rational_source_bound':str(exact_source_bound),'exact_rational_contradiction_factor_lower_bound':str(exact_survival_lower/exact_source_bound),'smaller_initial':a,'larger_initial':larger,'exact_survival_P_T_gt_1':survival_at_one,'rigorous_mean_lower_bound_P_T_gt_1':survival_at_one,'source_printed_mean_upper_bound':source_claimed_upper,'contradiction_factor_lower_bound':survival_at_one/source_claimed_upper,'source_location':'1993 notes printed p.37, paragraph immediately above Lemma 33'}
    sign={'y':1,'s':math.log(2),'correct_survival':math.exp(-1),'wrong_sign_survival':math.exp(-4),'wrong_sign_intensity_at_s':4}
    return {'exponential_stationary_generator_moments_p_0_to_12':moment_residuals,'one_particle_semigroup_checks':semigroup,'negative_control_source_mean_bound':counterexample,'negative_control_spatial_scaling_sign':sign,'status':'PASS'}


def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--output',type=Path); args=parser.parse_args()
    receipt={'created_utc':datetime.now(timezone.utc).isoformat(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'imports_submitted_code':False,'controls':{'finite_rectangles':exhaustive_rectangle_control(),'transformed_event_dynamics_and_autonomy':transformed_path_control(),'moving_lower_boundary_coupling':deterministic_coupling_control(),'crossing_configurations_and_random_stage_states':crossing_and_stopping_state_control(),'analytic_low_index_and_negative_controls':analytic_controls()},'limitations':'Finite controls are not a proof of PPP stationarity, strong Markov, or all-k uniqueness. Those are derived analytically in the frozen independent derivation and REPORT.md.'}
    rendered=json.dumps(receipt,indent=2)+'\n'
    if args.output:
        expected_root=Path(__file__).resolve().parent
        if not args.output.resolve().is_relative_to(expected_root): raise ValueError('Output must remain inside this audit folder')
        args.output.write_text(rendered)
    print(rendered,end='')

if __name__=='__main__': main()
