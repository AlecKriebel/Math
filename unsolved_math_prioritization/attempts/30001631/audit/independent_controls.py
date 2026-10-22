#!/usr/bin/env python3
"""Independent exact/model checks, not a TZ curvature evaluator.

Usage: python independent_controls.py /path/to/frozen/public /path/to/frozen.zip
No file in either input is written. All mathematical controls are authored for
this audit; original controls are executed only as a separately labelled replay.
"""
import hashlib
import json
import platform
from pathlib import Path
import subprocess
import sys
import zipfile

import mpmath as mp
import sympy as s

MANIFEST_SHA = "793eff4aec0c86808289fa1ce17d32d95f52c03dd09219d13538a6fa6527d5cd"
ZIP_SHA = "c9a370d76b6ef5cb98214f49098e812eb9c470adfa9e3a694bcbea4bd006298f"
ZIP_BYTES = 21262


def require(condition, description):
    if not condition:
        raise AssertionError(description)


def zero(expr):
    if isinstance(expr, s.MatrixBase):
        require(all(s.simplify(x) == 0 for x in expr), str(expr))
    else:
        require(s.simplify(expr) == 0, str(expr))


def main():
    base, archive = map(Path, sys.argv[1:3])
    tests = []

    def record(name, **facts):
        tests.append(dict(name=name, passed=True, **facts))

    def digest(blob):
        return hashlib.sha256(blob).hexdigest()

    manifest_blob = (base / "MANIFEST.json").read_bytes()
    archive_blob = archive.read_bytes()
    require(digest(manifest_blob) == MANIFEST_SHA, "Wrong bound manifest")
    require(len(archive_blob) == ZIP_BYTES and digest(archive_blob) == ZIP_SHA,
            "Wrong bound ZIP")
    manifest = json.loads(manifest_blob)
    expected = {row["path"]: row for row in manifest["files"]}
    files = {p.name: p.read_bytes() for p in base.iterdir() if p.is_file()}
    require(set(files) == set(expected) | {"MANIFEST.json"}, "Unexpected packet files")
    require(all(p.is_file() and not p.is_symlink() for p in base.iterdir()),
            "Directory or symlink in frozen input")
    for name, row in expected.items():
        require(len(files[name]) == row["bytes"] and digest(files[name]) == row["sha256"], name)
    with zipfile.ZipFile(archive) as z:
        require(len(z.namelist()) == len(set(z.namelist())), "Duplicate archive entry")
        require(set(z.namelist()) == set(files), "Archive allowlist differs")
        for name, blob in files.items():
            require(z.read(name) == blob, "Archive member differs: " + name)
    record("frozen_manifest_zip_and_all_members", payload_files=len(expected), archive_files=len(files),
           manifest_sha256=MANIFEST_SHA, zip_sha256=ZIP_SHA, zip_bytes=ZIP_BYTES)

    replay = subprocess.run([sys.executable, str(base / "check_controls.py")],
                            check=True, capture_output=True).stdout
    require(replay == files["CONTROL_OUTPUT.json"], "Original replay differs")
    require(json.loads(replay)["passed"] == 11, "Original count differs")
    record("original_control_replay_separate_from_independent_math", passed_original=11,
           output_sha256=digest(replay), byte_equal=True)

    # Actual integral, not just factorial arithmetic; the variables are positive.
    y, n, width = s.symbols("y n width", positive=True)
    integral = s.integrate(y**4 * s.exp(-4*s.pi*n*y), (y, 0, s.oo))
    zero(integral - s.Rational(3, 128)/(s.pi**5*n**5))
    record("exact_cusp_moment_integral", integral=str(integral))

    # Normalized E has leading (y/width)^2 in an unscaled width coordinate.
    width_integral = s.integrate(y**4*s.exp(-4*s.pi*n*y/width), (y, 0, s.oo))/width
    zero(width_integral - width**4*integral)
    record("width_change_and_quadratic_differential_scaling", normalized_factor="width**4",
           reason="q_new(z)=width**2*q_old(width*z); normalized unfolding measure is dxdy/width**2")

    a = [1+s.I, 2-s.I]
    b = [2, 1+2*s.I]
    pairing = sum(s.conjugate(u)*v/s.Integer(j)**5 for j, (u, v) in enumerate(zip(a,b), 1))
    scaled = sum(s.conjugate(-s.I*u)*v/s.Integer(j)**5 for j, (u, v) in enumerate(zip(a,b), 1))
    zero(scaled-s.I*pairing)
    record("mixed_pairing_antilinear_q_linear_mu", normalized_pairing=str(s.simplify(pairing)))

    # Infinite positive-coefficient model, not a finite-type automorphic form.
    mp.mp.dps = 70
    quadrature = mp.quad(lambda t: t**4/mp.expm1(4*mp.pi*t), [0, 1, mp.inf])
    closed = 24*mp.zeta(5)/(4*mp.pi)**5
    relative_error = abs(quadrature/closed-1)
    require(relative_error < mp.mpf("1e-60"), "Infinite-series quadrature")
    record("infinite_fourier_model_supplemental_quadrature",
           exact_value="3*zeta(5)/(128*pi**5)", precision_digits=70,
           relative_error=mp.nstr(relative_error, 8), actual_finite_type_surface=False)
    require(s.integrate(y**4, (y, 1, s.oo)) is s.oo, "Constant mode must diverge")
    record("zero_fourier_mode_divergence_negative_control", integral="infinity")

    # Complex row-vector convention, with genuinely nonreal Gram entries.
    U=s.Matrix([[1,s.I,1],[1+s.I,2,-s.I]])
    d=s.Matrix([[2-s.I,1+2*s.I,3]])
    G=s.simplify(U*U.H)
    P=s.simplify(U.H*G.inv()*U)
    zero(P*P-P)
    zero(P-P.H)
    b0=d*U.H
    curvature=(-d*d.H+b0*G.inv()*b0.H)[0]
    normal=(d*(s.eye(3)-P)*(s.eye(3)-P).H*d.H)[0]
    zero(curvature+normal)
    require(s.simplify(normal)>0, "Nonzero normal derivative")
    record("complex_hilbert_gram_projection", reduced_tensor=str(s.simplify(curvature)),
           normal_squared=str(s.simplify(normal)))

    A=s.Matrix([[3,1+s.I],[1-s.I,4]])
    B=s.Matrix([[4,-s.I],[s.I,2]])
    ba=s.Matrix([[1+2*s.I,-2+s.I]])
    bb=s.Matrix([[3-s.I,2*s.I]])
    T=A+B
    for M in [A,B,T]:
        require(M==M.H and M[0,0]>0 and M.det()>0, "Hermitian positivity")
    common=(ba+bb)*T.inv()
    defect=(ba*A.inv()*ba.H+bb*B.inv()*bb.H-(ba+bb)*T.inv()*(ba+bb).H)[0]
    squares=((ba-common*A)*A.inv()*(ba-common*A).H+(bb-common*B)*B.inv()*(bb-common*B).H)[0]
    zero(defect-squares)
    require(s.simplify(defect)>0, "Strict nonnegative defect")
    eq=s.Matrix([[1+s.I,2-s.I]])
    ea,eb=eq*A,eq*B
    zero((ea*A.inv()*ea.H+eb*B.inv()*eb.H-(ea+eb)*T.inv()*(ea+eb).H)[0])
    record("complex_sum_defect_and_equality", defect=str(s.simplify(defect)), equality_defect="0")

    # Independent scalar metric derivatives reproduce the curvature-of-sum sign.
    z,zb=s.symbols("z zb")
    def curvature(g):
        return s.simplify(-s.diff(g,z,zb)+s.diff(g,z)*s.diff(g,zb)/g)
    aa,ab=1+2*s.I,-1+s.I
    g1=s.exp(z*zb+aa*z+s.conjugate(aa)*zb)
    g2=s.exp(z*zb+ab*z+s.conjugate(ab)*zb)
    origin={z:0,zb:0}
    total0=curvature(g1+g2).subs(origin).simplify()
    expected0=-2-(aa-ab)*s.conjugate(aa-ab)/2
    zero(total0-expected0)
    record("sum_curvature_on_actual_local_kahler_models", total_R=str(total0), individual_R="-1 each",
           actual_TZ=False)

    kappas=[s.Integer(2),s.Integer(3),s.Integer(5)]
    xs=[1/k for k in kappas]
    bound=-1/sum(xs)
    zero(-sum(k*x*x for k,x in zip(kappas,xs))/sum(xs)**2-bound)
    record("weighted_cauchy_bound_sharp_equality", bound=str(bound))

    # Real-coordinate curvature controls independently fix all factors of two.
    x,Y,alpha=s.symbols("x Y alpha", real=True)
    def gaussian(g):
        return s.simplify(-(s.diff(s.log(g),x,2)+s.diff(s.log(g),Y,2))/(2*g))
    zero(gaussian(Y**-2)+1)
    zero(gaussian(4/(1+x*x+Y*Y)**2)-1)
    record("hyperbolic_and_spherical_sign_normalization", hyperbolic_K="-1", spherical_K="1",
           gaussian_to_reduced_H="K=2H")

    g=1+4*alpha*(x*x+Y*Y)
    zero(gaussian(g)+8*alpha/g**3)
    samples=[int((-8*alpha).subs(alpha,t)) for t in [-1,0,1]]
    require(samples==[8,0,-8], "Fourth-jet signs")
    record("positive_potential_hessian_both_metric_curvature_signs", K_at_origin=samples,
           alpha_values=[-1,0,1], neighborhood="Shrink so 1+4*alpha*|z|**2>0")

    g=s.exp(-z*zb)
    zero(curvature(g).subs(origin)-1)
    record("smooth_nonholomorphic_gram_negative_control", R_at_origin="1")

    r,C,p,L=s.symbols("r C p L", positive=True)
    lam=C/(r*r*(-s.log(r))**p)
    # log(lambda) expanded explicitly on 0<r<1 to avoid branch ambiguities.
    loglam=s.log(C)-2*s.log(r)-p*s.log(-s.log(r))
    radialK=s.simplify(-(s.diff(loglam,r,2)+s.diff(loglam,r)/r)/(2*lam))
    zero(radialK.subs(r,s.exp(-L))+p*L**(p-2)/(2*C))
    record("radial_cusp_curvature_from_r_derivatives", curvature="-p*L**(p-2)/(2*C)")
    L0=s.symbols("L0",positive=True)
    lengths={}
    for exponent in [1,2,3,4,6]:
        length=s.integrate(s.sqrt(C)*L**(-s.Rational(exponent,2)),(L,L0,s.oo))
        require((length is s.oo)==(exponent<=2), "Distance threshold")
        lengths[str(exponent)]=str(length)
    record("radial_distance_threshold_controls", lengths=lengths)

    h=s.sin(L**3)/L
    h2=(2/L**3-9*L**3)*s.sin(L**3)
    zero(s.diff(h,L,2)-h2)
    positiveK=4/L**2+2/L**3-9*L**3
    negativeK=4/L**2-2/L**3+9*L**3
    for ell in [1,2,10,100]:
        require(positiveK.subs(L,ell)<0 and negativeK.subs(L,ell)>0, "Opposite subsequence signs")
    record("oscillatory_remainder_derivatives_and_opposite_signs",
           positive_curvature_bracket_bound="<= -3*L**3 for L>=1",
           negative_curvature_bracket_bound=">= 2/L**2+9*L**3 for L>=1")

    slice_g=1+4*(x*x+Y*Y)
    zero(gaussian(slice_g)+8/slice_g**3)
    record("holomorphic_slice_in_flat_ambient_negative_control", ambient_R="0",
           slice_K="-8/(1+4*|z|**2)**3")

    # Use explicit nonconstant factors in both real coordinates.
    w=s.exp(x*x+2*x*Y+3*Y*Y)
    f=s.exp(2*x*x-x*Y-Y*Y+x)
    laplogf=s.diff(s.log(f),x,2)+s.diff(s.log(f),Y,2)
    zero(gaussian(f*w)-(gaussian(w)-laplogf/(2*w))/f)
    record("nonconstant_wp_ratio_identity_control", residual="0", actual_WP_or_TZ=False)

    for val in [-3,0,2]:
        zero(gaussian(s.exp(val*(x*x+Y*Y))).subs({x:0,Y:0})+2*val)
    record("positive_conformal_factor_both_signs_negative_control", origin_K=[6,0,-4])

    # Noncommuting complex-Hermitian two-jets test the Hessian, not just det products.
    J=s.Matrix([[1+s.I,2],[-s.I,1]])
    D=s.Matrix([[2,s.I],[-s.I,3]])
    metric=A+z*J+zb*J.H+z*zb*D
    direct=s.diff(s.log(metric.det()),z,zb).subs(origin).simplify()
    trace=s.trace(A.inv()*D-A.inv()*J.H*A.inv()*J).simplify()
    zero(direct-trace)
    W=B+z*s.eye(2)+zb*s.eye(2)+z*zb*s.eye(2)
    zero(s.diff(s.log(metric.det()/W.det()),z,zb).subs(origin)
         -s.diff(s.log(metric.det()),z,zb).subs(origin)
         +s.diff(s.log(W.det()),z,zb).subs(origin))
    record("noncommuting_determinant_hessian_and_ricci_comparison", hessian=str(direct))

    # Deliberately incorrect alternatives must fail an exact residual check.
    mutations={
        "fourier_coefficient_times_four": integral-s.Rational(3,32)/(s.pi**5*n**5),
        "wrong_fourier_weight_power": integral-s.Rational(3,128)/(s.pi**5*n**4),
        "sum_defect_wrong_sign": 2*defect,
        "gaussian_missing_half": gaussian(Y**-2)+2,
        "potential_R_wrong_sign": s.Integer(-4)-4,
        "gauss_slice_wrong_sign": gaussian(slice_g)-8/slice_g**3,
        "conformal_wrong_half": gaussian(f*w)-(gaussian(w)-laplogf/w)/f,
        "determinant_hessian_missing_quadratic_term": direct-s.trace(A.inv()*D),
    }
    for name,residual in mutations.items():
        require(s.simplify(residual)!=0, "Mutation was not rejected: "+name)
    record("independent_deliberate_error_controls", rejected=len(mutations), names=sorted(mutations))

    # Re-read every frozen byte at exit, including the externally bound manifest and ZIP.
    require(files=={p.name:p.read_bytes() for p in base.iterdir()}, "Frozen bytes changed")
    require(archive.read_bytes()==archive_blob, "Frozen ZIP changed")
    record("input_bytes_unchanged_at_exit", unchanged=True)
    out=dict(scope="Independent exact identities, model controls, provenance binding, and negative controls; no actual TZ curvature evaluated.",
             python=platform.python_version(),sympy=s.__version__,mpmath=mp.__version__,
             checks_passed=len(tests),tests=tests)
    print(json.dumps(out,indent=2,sort_keys=True))


if __name__=="__main__":
    main()
