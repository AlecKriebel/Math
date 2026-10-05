#!/usr/bin/env python3
"""Read-only freeze verification and independent symbolic audit for target 2306086.

Usage: python3 audit_controls.py --freeze-directory PATH --freeze-zip PATH
Add --numerical to independently reevaluate the four saved ODE controls.
Requires SymPy; --numerical also requires NumPy and SciPy.
Prints JSON, does not write to or import modules from the authored freeze.
Finite tests and symbolic identities do not replace the analytical proof review.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import zipfile

import sympy as s

EXPECTED_ZIP_SHA256 = "6897b0a5f2efc08daddd87ff4ce44c35d61fc29ba44b1dc5a8179df2dc7f35a5"
EXPECTED_ZIP_BYTES = 19163
EXPECTED_NAMES = {
    "APPROACH_LOG.md", "EXACT_CONTROL_RESULTS.json", "FROZEN_MANIFEST.json",
    "LIMITATIONS.md", "LOEWNER_EXPLORATION.json", "PROOF_PARTIALS.md",
    "README.md", "SOURCE_VERIFICATION.json", "exact_controls.py",
    "explore_loewner.py",
}
checks = []


def check(label, condition):
    if not bool(condition):
        raise RuntimeError("Audit failure: " + label)
    checks.append(label)


def zero(label, expression):
    check(label, s.cancel(s.together(expression)) == 0)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def symbolic_checks():
    z, zb, a, p, w = s.symbols("z zb a p w")
    x, y, t, u = s.symbols("x y t u", real=True)
    den = (1-z*z)*(1-zb*zb)
    delta2 = -(z-zb)**2/(4*den)
    zero("delta_denominator", den-(1-z*zb)**2+(z-zb)**2)
    for sign in (-1, 1):
        f = z/(1-sign*z)**2
        pf = s.cancel(s.diff(f,z,2)/s.diff(f,z))
        zero("koebe_derivative_"+str(sign), pf-(4*sign+2*z)/(1-z*z))
        af = s.cancel((1-z*zb)*pf-2*zb)
        abar = af.xreplace({z:zb, zb:z})
        zero("koebe_deficit_"+str(sign), af*abar-(16-48*delta2))
        zero("real_axis_"+str(sign), af.subs(zb,z)-4*sign)
    h = z/(1-z*z)
    zero("two_slit_injectivity_factor", h-h.subs(z,w)-(z-w)*(1+z*w)/((1-z*z)*(1-w*w)))
    ph = s.cancel(s.diff(h,z,2)/s.diff(h,z))
    zero("two_slit_log_derivative",ph-(2*z/(1+z*z)+4*z/(1-z*z)))
    zero("two_slit_imaginary",(1-t*t)*ph.subs(z,s.I*t)+2*s.I*t-8*s.I*t/(1+t*t))
    phi=(z+a)/(1+a*z)
    phib=(zb+a)/(1+a*zb)
    dphi=s.diff(phi,z)
    pphi=s.diff(phi,z,2)/dphi
    phase=(1+a*zb)/(1+a*z)
    zero("covariance_arbitrary_P",(1-z*zb)*(p*dphi+pphi)-2*zb-phase*((1-phi*phib)*p-2*phib))
    zero("covariance_phase_modulus",phase*phase.xreplace({z:zb,zb:z})-1)
    zero("disk_automorphism_inverse",((phi-a)/(1-a*phi))-z)
    zero("delta_invariance",-(phi-phib)**2/(4*(1-phi**2)*(1-phib**2))-delta2)
    zero("automorphism_imaginary_factor",(phi-phib)/(z-zb)-(1-a*a)/((1+a*z)*(1+a*zb)))
    inverse=(z-a)/(1-a*z)
    inverseb=(zb-a)/(1-a*zb)
    numerator=s.cancel((inverse+inverseb)*((1-a*z)*(1-a*zb))/2)
    zero("imaginary_axis_reduction_quadratic",numerator.subs({z:x+s.I*y,zb:x-s.I*y})-(x*a*a-(1+x*x+y*y)*a+x))
    zero("imaginary_axis_invariant",delta2.subs({z:s.I*t,zb:-s.I*t})-t*t/(1+t*t)**2)
    zero("lower_bound_crossing",16*(1-3*s.Rational(1,7))-64*s.Rational(1,7))
    zero("half_point_koebe_square",(16-48*delta2).subs({z:s.I/2,zb:-s.I/2})-s.Rational(208,25))
    zero("half_point_two_slit_square",64*delta2.subs({z:s.I/2,zb:-s.I/2})-s.Rational(256,25))
    q=(z/(1-z)**2+z/(1+z)**2)/2
    zero("convex_average_derivative",s.diff(q,z)-(1+6*z*z+z**4)/(1-z*z)**3)
    critical=s.I*(s.sqrt(2)-1)
    check("convex_average_critical_point",s.simplify(s.diff(q,z).subs(z,critical))==0)
    check("convex_average_simple_critical_point",s.simplify(s.diff(q,z,2).subs(z,critical))!=0)
    check("convex_average_critical_inside_disk",0<s.sqrt(2)-1<1)
    imbalance=(z/(1-z)**2-z/(1+z)**2)/2
    check("convex_perturbation_derivative_nonzero",s.simplify(s.diff(imbalance,z).subs(z,critical))!=0)
    p_u=(1-z*z)/(1-2*u*z+z*z)
    log_h=1/z+(u-1)/(z-1)-(u+1)/(z+1)
    zero("loewner_tail_starlike_identity",z*log_h-1/p_u)
    zero("growth_integrand",(4+2*t)/(1-t*t)-(1/(1+t)+3/(1-t)))
    zero("growth_integral",s.diff(t/(1-t)**2,t)-(1+t)/(1-t)**3)
    # Negative controls must actually fail the mathematical identity being tested.
    check("negative_wrong_covariance_rejected",s.cancel((1-z*zb)*(p*dphi+pphi)-2*zb-(1/phase)*((1-phi*phib)*p-2*phib))!=0)
    check("negative_koebe_only_bound_rejected",s.Rational(256,25)>s.Rational(208,25))
    check("negative_uniform_gap_rejected",s.Rational(4)>s.Rational(399,100))
    check("negative_constant_47_rejected",s.cancel(16-48*delta2-(16-47*delta2))!=0)


def numerical_checks(directory):
    import numpy as np
    import scipy
    from scipy.integrate import solve_ivp
    z,u=s.symbols("z u")
    velocity=-z*(1-z*z)/(1-2*u*z+z*z)
    funcs=[s.lambdify((z,u),s.diff(velocity,z,n),"numpy") for n in range(3)]
    records=[]
    for record in json.loads((directory/"LOEWNER_EXPLORATION.json").read_text())["records"]:
        c1,c2,d1,d2,tail=record["parameters"]
        r=record["r"]
        jet=np.array([1j*r,1+0j,0j])
        for control,duration in [(c1,d1),(c2,d2)]:
            def rhs(time,state):
                point,first,second=state
                return [funcs[0](point,control),funcs[1](point,control)*first,funcs[2](point,control)*first*first+funcs[1](point,control)*second]
            sol=solve_ivp(rhs,(0,duration),jet,method="RK45",rtol=2e-13,atol=2e-15)
            check("independent_ode_solver_success",sol.success)
            jet=sol.y[:,-1]
        point,first,second=jet
        # Saved tails are exactly +/-1, so independently differentiate the
        # ordinary Koebe tail instead of using the author's generic tail code.
        check("saved_tail_is_real_koebe",tail in (-1.0,1.0))
        pf=((-4*tail+2*point)/(1-point*point))*first+second/first
        result=float(abs((1-r*r)*pf+2j*r))
        difference=abs(result-record["value"])
        check("independent_ode_reproduction",difference<2e-9)
        records.append({"r":r,"recorded":record["value"],"independent_rk45":result,"absolute_difference":difference,"certified":False})
    return {"method":"RK45, rtol=2e-13, atol=2e-15; no optimization rerun","records":records,"numpy":np.__version__,"scipy":scipy.__version__,"certified":False}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--freeze-directory",type=Path,required=True)
    parser.add_argument("--freeze-zip",type=Path,required=True)
    parser.add_argument("--numerical",action="store_true")
    args=parser.parse_args()
    directory=args.freeze_directory
    data=args.freeze_zip.read_bytes()
    check("archive_byte_count",len(data)==EXPECTED_ZIP_BYTES)
    check("archive_sha256",digest(data)==EXPECTED_ZIP_SHA256)
    with zipfile.ZipFile(args.freeze_zip) as archive:
        check("archive_member_count",len(archive.namelist())==10)
        check("archive_members",set(archive.namelist())==EXPECTED_NAMES)
        for name in sorted(EXPECTED_NAMES):
            check("archive_directory_binding",archive.read(name)==(directory/name).read_bytes())
    manifest=json.loads((directory/"FROZEN_MANIFEST.json").read_text())
    check("manifest_members",{r["path"] for r in manifest["files"]}==EXPECTED_NAMES-{"FROZEN_MANIFEST.json"})
    for row in manifest["files"]:
        content=(directory/row["path"]).read_bytes()
        check("manifest_size",len(content)==row["bytes"])
        check("manifest_hash",digest(content)==row["sha256"])
    replays={}
    expected=json.loads((directory/"EXACT_CONTROL_RESULTS.json").read_text())
    for mode,flags in [("normal",[]),("optimized",["-O"])]:
        completed=subprocess.run([sys.executable,*flags,"-B",str(directory/"exact_controls.py")],check=True,capture_output=True,text=True)
        result=json.loads(completed.stdout)
        check("authored_replay_matches_saved",result==expected)
        check("authored_replay_count",result["checks"]==3558)
        replays[mode]=result
    symbolic_checks()
    numerical=numerical_checks(directory) if args.numerical else None
    # Recheck the immutable inputs after all subprocesses and numerical work.
    check("archive_preserved",digest(args.freeze_zip.read_bytes())==EXPECTED_ZIP_SHA256)
    with zipfile.ZipFile(args.freeze_zip) as archive:
        for name in EXPECTED_NAMES:
            check("directory_preserved",archive.read(name)==(directory/name).read_bytes())
    print(json.dumps({"status":"PASS","audit_checks":len(checks),"by_family":dict(sorted(Counter(checks).items())),"authored_replays":replays,"symbolic_engine":"SymPy "+s.__version__,"numerical":numerical,"limitations":"Analytical proof audit is separate. Numerical ODE values are reproducibility evidence only, not interval-certified mathematical bounds."},indent=2,sort_keys=True))


if __name__=="__main__":
    main()
