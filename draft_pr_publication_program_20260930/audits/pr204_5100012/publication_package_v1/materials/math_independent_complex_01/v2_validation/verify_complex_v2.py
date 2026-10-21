"""Finite-value guarded numerical diagnostics; the proof is in the parent audit.
No installation or bytecode writes. Optional PR204_RUNTIME_PACKAGES selects dependencies.
"""
import sys
sys.dont_write_bytecode = True
import os, json, argparse, datetime, pathlib, hashlib
PARENT_MANIFEST_SHA256 = "4ca9a0a74d59acd78865252388696b7e8b71a8ed71d1c0669b0a078413ae6071"
runtime_env = os.environ.get("PR204_RUNTIME_PACKAGES")
runtime_path = None
runtime_method = "normally installed packages"
if runtime_env:
    runtime_path = pathlib.Path(runtime_env).expanduser().resolve()
    runtime_method = "PR204_RUNTIME_PACKAGES"
    if not all((runtime_path / name).is_dir() for name in ("sympy", "mpmath")):
        raise RuntimeError("PR204_RUNTIME_PACKAGES must contain sympy and mpmath")
else:
    for ancestor in pathlib.Path(__file__).resolve().parents:
        candidate = ancestor / "pr200_5100007" / "math_algebra_family_01" / "runtime_packages"
        if all((candidate / name).is_dir() for name in ("sympy", "mpmath")):
            runtime_path = candidate
            runtime_method = "existing sibling runtime found by ancestor-relative search"
            break
if runtime_path is not None:
    sys.path.insert(0, str(runtime_path))
import sympy as sp
import mpmath as mp

class CheckFailure(RuntimeError):
    def __init__(self, kind, name, **details):
        self.payload = dict(kind=kind, name=name, **details)
        super().__init__(str(self.payload))

def run(mutation):
    checks = {}
    guarded = {}
    def finite(name, value):
        guarded[name] = guarded.get(name, 0) + 1
        if not mp.isfinite(value):
            raise CheckFailure("nonfinite", name, value=str(value))
        if not mp.im(value) == 0:
            raise CheckFailure("not_real", name, value=str(value))
        return value
    def positive(name, value):
        value = finite(name, value)
        if not value > 0:
            raise CheckFailure("not_positive", name, value=str(value))
        return value
    def below(name, value, tolerance):
        value = finite(name, value)
        if not value <= tolerance:
            raise CheckFailure("upper_bound", name, value=str(value), tolerance=str(tolerance))
        return value
    def above(name, value, threshold):
        value = finite(name, value)
        if not value > threshold:
            raise CheckFailure("lower_bound", name, value=str(value), threshold=str(threshold))
        return value
    def encoded(name, value):
        return mp.nstr(finite(name, value), 35)
    def point(name, value):
        return (finite(name + "_x", value[0]), finite(name + "_y", value[1]))
    def exact(name, expression):
        reduced = sp.factor(expression)
        if reduced != 0:
            raise CheckFailure("symbolic_identity", name, residual=str(reduced))
        checks[name] = "zero exactly"

    s,c,d,h,C,D,k,al,kp = sp.symbols("s c d h C D k al kp", nonzero=True)
    den = 1-k*k*s*s*h*h
    sm = (s*C*D-h*c*d)/den
    spl = (s*C*D+h*c*d)/den
    cm = (c*C+s*h*d*D)/den
    cpl = (c*C-s*h*d*D)/den
    # Mutation changes the actual first contact identity target from 1 to 2.
    target = 2 if mutation == "false_identity" else 1
    contact_minus = (D*s*sm+c*cm)/C-target
    contact_plus = (D*s*spl+c*cpl)/C-1
    g = sp.groebner([c*c+s*s-1,d*d+k*k*s*s-1,C*C+h*h-1,D*D+k*k*h*h-1],c,d,C,D,s,h,k)
    for name, expression in [("contact_minus",contact_minus),("contact_plus",contact_plus),("edge_cross",spl*cm-sm*cpl-2*h*C*d/den)]:
        numerator = sp.fraction(sp.together(expression))[0]
        exact(name,g.reduce(sp.expand(numerator))[1])
    qzprime = al*k*s*(d/(1+d)-k*k*c*c/(1+d)**2)
    ct = al*al*s*(d+kp*kp)/(1+d)**2
    numerator = sp.fraction(sp.together(al/k*qzprime-ct))[0]
    g2 = sp.groebner([c*c+s*s-1,d*d+k*k*s*s-1,kp*kp+k*k-1],c,d,kp,s,k,al)
    exact("residue_constant",g2.reduce(sp.expand(numerator))[1])
    a,b,L,x,y = sp.symbols("a b L x y",positive=True)
    rho = a*a*y*y+b*b*x*x
    rad = a*a*x*x+b*b*y*y
    numerator = a*a*b*b*(rho-L*L)-L*L*(a*a-b*b)**2*x*x*y*y-rho*(a*a*b*b-L*L*rad)
    exact("local_pedal_numerator",sp.rem(sp.Poly(sp.expand(numerator),x),sp.Poly(x*x+y*y-1,x)).as_expr())

    mp.mp.dps = 60
    def det(p,q):
        return finite("determinant",p[0]*q[1]-p[1]*q[0])
    def direct_areas(vertices):
        n = len(vertices)
        area = finite("original_area",mp.fsum(det(vertices[j],vertices[(j+1)%n]) for j in range(n))/2)
        feet = []
        for j in range(n):
            px,py = vertices[j]
            rx,ry = vertices[(j+1)%n]
            vx,vy = point("side_vector",(rx-px,ry-py))
            squared = positive("side_squared_length",vx*vx+vy*vy)
            fraction = finite("projection_fraction",-(px*vx+py*vy)/squared)
            feet.append(point("foot",(px+fraction*vx,py+fraction*vy)))
        pedal = finite("pedal_area",mp.fsum(det(feet[j],feet[(j+1)%n]) for j in range(n))/2)
        product = finite("area_product",area*pedal)
        return area,pedal,product
    rows = []
    first_residual = True
    wrong_parity_checked = 0
    phase_count = 0
    for modulus in ["0.3","0.7","0.95"]:
        kval = positive("modulus",mp.mpf(modulus))
        parameter = finite("parameter",kval*kval)
        kcomp = positive("complementary_modulus",mp.sqrt(1-parameter))
        K = positive("quarter_period",mp.ellipk(parameter))
        def f(name,u):
            return finite("jacobi_value",mp.ellipfun(name,u,parameter))
        for N,tau in [(3,1),(4,1),(5,1),(5,2),(6,1),(7,3),(8,3),(10,3),(12,5)]:
            v = positive("half_step",2*K*tau/N)
            delta = positive("step",2*v)
            aa = positive("outer_a",f("dn",v)/f("cn",v))
            bb = positive("outer_b",kcomp/f("cn",v))
            def P(u):
                return point("vertex",(-aa*f("sn",u),bb*f("cn",u)))
            ca = positive("C_A",aa*bb*f("sn",v)*f("cn",v)/f("dn",v))
            ctval = positive("C_T",f("sn",delta)*(kcomp*kcomp+f("dn",delta))/(1+f("dn",delta))**2)
            errors,products,phases = [],[],[]
            def S(u):
                return finite("trace",mp.fsum(f("dn",u+j*delta) for j in range(N)))
            for phase in [mp.mpf("0.123"),K/3,mp.mpf("1.317")*K]:
                phase = finite("phase",phase)
                vertices = [P(phase+j*delta) for j in range(N)]
                area,pedal,product = direct_areas(vertices)
                predicted_area = finite("predicted_original_area",ca*S(phase))
                predicted_pedal = finite("predicted_pedal_area",ctval*S(phase+v+K))
                # Each mutation is applied once to the first ACTUAL numerical identity.
                if first_residual and mutation == "false_numeric_identity":
                    predicted_area = finite("mutated_predicted_area",2*predicted_area)
                area_error = abs(area-predicted_area)
                if first_residual and mutation == "nan_residual":
                    area_error = mp.nan
                area_error = below("first_area_identity" if first_residual else "area_identity",area_error,mp.mpf("1e-50"))
                first_residual = False
                pedal_error = below("pedal_identity",abs(pedal-predicted_pedal),mp.mpf("1e-50"))
                errors.extend([area_error,pedal_error])
                products.append(product)
                phases.append(dict(phase=encoded("reported_phase",phase),area=encoded("reported_area",area),pedal=encoded("reported_pedal",pedal),product=encoded("reported_product",product)))
                phase_count += 1
            maximum = below("maximum_formula_residual",max(errors),mp.mpf("1e-50"))
            spread = finite("product_spread",max(products)-min(products))
            eligible = N%2 == 1 or N%4 == 0
            if eligible:
                below("eligible_product_spread",spread,mp.mpf("1e-48"))
                spread_check = "upper bound <=1e-48 enforced"
            else:
                above("wrong_parity_product_spread",spread,mp.mpf("1e-30"))
                spread_check = "positive diagnostic spread >1e-30 enforced"
                wrong_parity_checked += 1
            rows.append(dict(k=modulus,N=N,tau=tau,eligible=eligible,C_A=encoded("reported_C_A",ca),C_T=encoded("reported_C_T",ctval),maximum_formula_residual=encoded("reported_residual",maximum),product_spread=encoded("reported_spread",spread),spread_check=spread_check,phases=phases))

    # Actual six-vertex list and its twofold repeated twelve-entry list.
    parameter = mp.mpf("0.81")
    kcomp = positive("repeated_complement",mp.sqrt(1-parameter))
    K = positive("repeated_quarter_period",mp.ellipk(parameter))
    v = positive("repeated_half_step",K/3)
    delta = positive("repeated_step",2*v)
    def f(name,u):
        return finite("repeated_jacobi_value",mp.ellipfun(name,u,parameter))
    aa = positive("repeated_outer_a",f("dn",v)/f("cn",v))
    bb = positive("repeated_outer_b",kcomp/f("cn",v))
    def P(u):
        return point("repeated_vertex",(-aa*f("sn",u),bb*f("cn",u)))
    repeated = []
    duplicate_products = []
    for phase in [mp.mpf(0),K/3]:
        vertices = [P(phase+j*delta) for j in range(6)]
        a6,b6,p6 = direct_areas(vertices)
        a12,b12,p12 = direct_areas(vertices*2)
        below("repeated_area_scaling",abs(a12-2*a6),mp.mpf("1e-50"))
        below("repeated_pedal_scaling",abs(b12-2*b6),mp.mpf("1e-50"))
        below("repeated_product_scaling",abs(p12-4*p6),mp.mpf("1e-48"))
        duplicate_products.append(p12)
        repeated.append(dict(phase_over_K=encoded("reported_repeated_phase",phase/K),area6=encoded("reported_area6",a6),pedal6=encoded("reported_pedal6",b6),product6=encoded("reported_product6",p6),area12=encoded("reported_area12",a12),pedal12=encoded("reported_pedal12",b12),product12=encoded("reported_product12",p12)))
    repeated_spread = above("repeated_list_spread",max(duplicate_products)-min(duplicate_products),mp.mpf("1e-30"))
    parent = pathlib.Path(__file__).resolve().parent.parent / "AUTHORED_MANIFEST.json"
    parent_present = parent.is_file()
    if parent_present:
        actual = hashlib.sha256(parent.read_bytes()).hexdigest()
        if actual != PARENT_MANIFEST_SHA256:
            raise CheckFailure("parent_manifest_pin","parent_manifest",actual=actual)
    return dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),mutation=mutation,optimized=bool(sys.flags.optimize),runtime=dict(method=runtime_method,sympy=sp.__version__,mpmath=mp.__version__,bytecode_disabled=bool(sys.dont_write_bytecode)),parent_manifest=dict(expected_sha256=PARENT_MANIFEST_SHA256,available=parent_present,verified_if_available=parent_present),symbolic_checks=checks,counts=dict(symbolic_identities=len(checks),configurations=len(rows),phases=phase_count,wrong_parity_configurations_enforced=wrong_parity_checked,repeated_list_phases=len(repeated)),numeric_diagnostics_only=rows,repeated_list_diagnostics_only=repeated,repeated_list_positive_spread=encoded("reported_repeated_spread",repeated_spread),finite_guard_call_counts=guarded,proof_status="Finite noninterval diagnostics; universal theorem remains the written parent proof, unchanged by this code hardening.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mutation",choices=("none","false_identity","false_numeric_identity","nan_residual"),default="none")
    args = parser.parse_args()
    try:
        result = run(args.mutation)
    except CheckFailure as error:
        print(json.dumps(dict(mutation=args.mutation,optimized=bool(sys.flags.optimize),rejected=True,**error.payload),sort_keys=True),file=sys.stderr)
        raise SystemExit(2)
    print(json.dumps(result,sort_keys=True,separators=(",",":")))
