#!/usr/bin/env python3
"""Uncertified independent replay using the flow pre-Schwarzian as a state.

This changes the integrated state from (w,d,e) to (w,d,b=e/d), for which
b'=v''(w)d. No submitted modules, symbolic derivatives, or optimizer are used.
"""
import json
from pathlib import Path
import sys
import numpy as np
import scipy
from scipy.integrate import solve_ivp

HERE = Path(__file__).resolve().parent
PACKET = HERE.parents[1]/"native/unsolved_math_prioritization/attempts/2306086"


def velocity_and_derivatives(w,u):
    N=w*w*w-w
    N1=3*w*w-1
    N2=6*w
    D=1-2*u*w+w*w
    D1=2*w-2*u
    D2=2
    return (N/D,
            (N1*D-N*D1)/(D*D),
            (N2*D*D-N*D2*D-2*N1*D*D1+2*N*D1*D1)/(D*D*D))


records=[]
for saved in json.loads((PACKET/"author/LOEWNER_EXPLORATION.json").read_text())["records"]:
    r=saved["r"]
    u1,u2,T1,T2,tail=saved["parameters"]
    if not (-1<=u1<=1 and -1<=u2<=1 and T1>=0 and T2>=0 and tail in (-1,1)):
        raise ValueError("saved controls outside admissible construction")
    state=np.array([1j*r,1+0j,0j])
    solver_success=[]
    for control,duration in ((u1,T1),(u2,T2)):
        def rhs(time,Y):
            w,d,b=Y
            v,v1,v2=velocity_and_derivatives(w,control)
            return [v,v1*d,v2*d]
        sol=solve_ivp(rhs,(0,duration),state,method="DOP853",rtol=2e-13,atol=2e-15)
        if not sol.success:
            raise ValueError(sol.message)
        state=sol.y[:,-1]
        solver_success.append(bool(sol.success))
    w,d,b=state
    P=(-4*tail+2*w)/(1-w*w)*d+b
    value=float(abs((1-r*r)*P+2j*r))
    difference=abs(value-saved["value"])
    if not difference<2e-9:
        raise ValueError("independent alternative-state replay mismatch")
    records.append({"r":r,"recorded_value":saved["value"],"alternative_state_value":value,
                    "absolute_difference":difference,"solver_success":solver_success,
                    "elementary_lower_bound":saved["elementary_lower_bound"],
                    "certified":False})

print(json.dumps({"status":"PASS","python_executable":sys.executable,
                  "python_version":sys.version,"numpy":np.__version__,"scipy":scipy.__version__,
                  "state":"w, d=dw/dz, b=(d2w/dz2)/(dw/dz)",
                  "method":"DOP853; rtol=2e-13, atol=2e-15; saved parameters only",
                  "records":records,"certified":False,
                  "limitations":"No interval error enclosure, optimizer rerun, certified strict lower bound, upper bound, or global extremality claim."},
                 indent=2,sort_keys=True))
