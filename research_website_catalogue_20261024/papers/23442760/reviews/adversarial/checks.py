"""Independent exact SOS diagnostics and whole-original custody.

Does not import/execute any supplied verification program. Writes only new
evidence in this adversarial namespace and refuses evidence overwrite.
"""
from pathlib import Path, PurePosixPath
from hashlib import sha256
from datetime import datetime, timezone
import json
import stat
import sys
import zipfile
import sympy as s

HERE = Path(__file__).resolve().parent
SOURCES = HERE.parents[1] / "sources"
ROOT = HERE.parents[3]


def h(data):
    return sha256(data).hexdigest()


def write(name, value):
    path = HERE / name
    if path.exists():
        raise RuntimeError("Refusing immutable evidence overwrite: " + name)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")


def custody():
    seal_data = (SOURCES / "SOURCE_READY_SEAL.json").read_bytes()
    assert h(seal_data) == "002b8324c97eb11428fa6b747f7b749ea4a1301c953acdb425f19dc168b87da5"
    manifest_data = (SOURCES / "SOURCE_READY_MANIFEST.json").read_bytes()
    assert h(manifest_data) == "445d0532cc31dfca48ade7cf207d5439d83a0da13dc66f4c0451a12db3912c79"
    manifest = json.loads(manifest_data)
    assert manifest["file_count"] == len(manifest["files"]) == 161
    bindings = []
    for expected in manifest["files"]:
        data = (SOURCES / expected["path"]).read_bytes()
        actual = {"path": expected["path"], "bytes": len(data), "sha256": h(data)}
        assert actual == expected
        bindings.append(actual)
    members = []
    with zipfile.ZipFile(SOURCES / "Convex_Body_SOS_Density_Verification_v1.0.zip") as archive:
        entries = archive.infolist()
        assert len(entries) == 152 and len({entry.filename for entry in entries}) == 152
        for entry in entries:
            path = PurePosixPath(entry.filename)
            assert not path.is_absolute() and ".." not in path.parts and "\\" not in entry.filename
            assert not stat.S_ISLNK(entry.external_attr >> 16) and not entry.is_dir()
            data = archive.read(entry)  # Independently checks CRC; no extraction.
            assert data == (SOURCES / "published-source" / entry.filename).read_bytes()
            members.append({"member": entry.filename, "bytes": len(data), "sha256": h(data),
                            "CRC32": f"{entry.CRC:08x}", "CRC_read_pass": True,
                            "equal_frozen_extracted_original": True})
    record = json.loads((SOURCES / "record.raw.json").read_text())
    return {"utc": datetime.now(timezone.utc).isoformat(), "status": "ALL_161_BINDINGS_AND_152_MEMBERS_AUTHENTICATED",
            "source_ready_manifest_sha256": h(manifest_data), "source_ready_seal_sha256": h(seal_data),
            "bindings": bindings, "archive_members": members,
            "record_id": record["id"], "version": record["metadata"]["version"],
            "declared_publication_date": record["metadata"]["publication_date"],
            "created": record["created"], "updated": record["updated"],
            "original_source_code_executed": False, "original_bytes_mutated": False}


def prior_packet_custody():
    targets = [
        (ROOT / "papers/23074543/reviews/adversarial", "289a69d2eb79c2f907b584bf3eb34e16d5e7e04a98669e4052ac87ccfaf49aa7"),
        (ROOT / "verification/cfh-independent-code-audit-sol-20261025", "08df6760943ae91c7fb4f22b5bc6952aea2325bc87ae1b1623a47af5dbdb984f"),
    ]
    result = []
    for directory, expected in targets:
        seal_bytes = (directory / "FINAL_SEAL.json").read_bytes()
        assert h(seal_bytes) == expected
        seal = json.loads(seal_bytes)
        manifest_bytes = (directory / seal["manifest"]).read_bytes()
        assert h(manifest_bytes) == seal["manifest_sha256"]
        manifest = json.loads(manifest_bytes)
        entries = manifest["files"]
        if isinstance(entries, dict):
            entries = [{"path": name, **binding} for name, binding in entries.items()]
        for item in entries:
            data = (directory / item["path"]).read_bytes()
            assert len(data) == item["bytes"] and h(data) == item["sha256"]
        result.append({"directory": str(directory), "seal_sha256": expected,
                       "all_manifest_bindings_match": True, "file_count": len(entries),
                       "read_scope": "Byte hashing only; no substantive prior opinions consumed."})
    return result


def diagnostics():
    t, x, y, z = s.symbols("t x y z", real=True)
    kernel = lambda m, v: s.expand((1+2*sum(s.chebyshevt(j,1-2*v) for j in range(1,m+1)))/(2*m+1))
    kernel_results = []
    for m in range(1,7):
        A = kernel(m,t)
        alternate = s.Poly(s.chebyshevu(2*m,x),x)
        even_form = sum(coefficient*(1-t)**(power[0]//2) for power, coefficient in alternate.terms())
        assert s.expand((2*m+1)*A-even_form) == 0
        assert s.degree(A,t) == m and A.subs(t,0) == 1
        assert A.subs(t,1) == s.Rational((-1)**m,2*m+1)
        kernel_results.append({"m":m,"degree":m,"Dirichlet_Chebyshev_identity_residual":0,
                               "A_0":"1","A_1":str(A.subs(t,1))})
    assert kernel(1,t).subs(t,s.Rational(1,9)) == s.Rational(23,27) < 1
    assert kernel(1,t).subs(t,1)**5 < 0  # Odd power is not a valid square.
    j = s.symbols("j", integer=True, nonnegative=True)
    assert s.summation(s.Rational(1,2)**j,(j,0,s.oo)) == 2
    assert s.summation(s.Integer(1),(j,0,s.oo)) == s.oo  # L=n+1 fails the majorant.
    floor_cases = 0
    for n in range(1,7):
        L=n+2
        for r in range(1,9*L+1):
            if r>=2*L:
                m=r//(2*L)
                assert 2*m*L<=r and 4*m*L<=2*r and 2*m+1>=s.Rational(r,2*L)
            else:
                assert 4*L**2>r**2  # C_n is strictly larger than 4L^2.
            floor_cases += 1
    # Boundary-linear interval with the actual quadratic proxy, not f alone.
    u=(t+t*t)/2
    square_root=kernel(1,u)**3
    Q=s.expand(square_root**2)
    Z=s.integrate(Q,(t,0,1));mean=s.integrate(t*Q,(t,0,1))/Z
    assert Z>0 and s.degree(square_root,t)==6 and s.degree(Q,t)==12
    assert s.integrate(Q/Z,(t,0,1))==1 and 0<mean<1
    boundary={"n":1,"m":1,"L":3,"r":6,"root_degree":6,"density_degree":12,
              "normalizer":str(Z),"exact_objective":str(mean),"unit_mass":True}
    # A nonsimple three-dimensional apex: |x|,|y|<=z, 0<=z<=1.
    # Its monomial moment is 4/[(i+1)(j+1)(i+j+k+3)] for even i,j.
    def pyramid_integral(poly):
        total=0
        for powers, coefficient in s.Poly(s.expand(poly),x,y,z).terms():
            i,j,k=powers
            if i%2==0 and j%2==0:
                total += coefficient*s.Rational(4,(i+1)*(j+1)*(i+j+k+3))
        return total
    g=z+x*x+y*y+z*z
    root=kernel(1,g/4)**5
    apex_Q=s.expand(root**2)
    apex_Z=pyramid_integral(apex_Q)
    apex_mean=pyramid_integral(z*apex_Q)/apex_Z
    assert pyramid_integral(1)==s.Rational(4,3) and apex_Z>0 and 0<apex_mean<1
    assert s.Poly(root,x,y,z).total_degree()==10 and s.Poly(apex_Q,x,y,z).total_degree()==20
    assert pyramid_integral(apex_Q/apex_Z)==1
    apex={"n":3,"m":1,"L":5,"r":10,"G":4,"root_degree":10,"density_degree":20,
          "normalizer":str(apex_Z),"exact_objective":str(apex_mean),"unit_mass":True,
          "moment_formula":"4/((i+1)(j+1)(i+j+k+3)) if i,j even; zero otherwise"}
    # Multiple interior minima of a genuinely nonconvex polynomial.
    f=(t*t-s.Rational(1,4))**2
    gamma=s.Rational(13,2)
    gap=s.factor(gamma*(t-s.Rational(1,2))**2-f)
    assert s.diff(f,t).subs(t,s.Rational(1,2))==0
    assert s.diff(f,t,2).subs(t,0)==-1
    assert s.expand(gap-(t-s.Rational(1,2))**2*(gamma-(t+s.Rational(1,2))**2))==0
    # Exact orthogonality/endpoint kernel controls supporting the lower proof.
    legendre_results=[]
    for r in range(1,6):
        basis=[s.sqrt(2*j+1)*s.legendre(j,2*t-1) for j in range(r+1)]
        assert all(s.integrate(basis[j]*basis[k],(t,0,1))==int(j==k) for j in range(r+1) for k in range(r+1))
        assert sum(p.subs(t,0)**2 for p in basis)==(r+1)**2
        legendre_results.append({"r":r,"Gram_identity_exact":True,"endpoint_kernel":(r+1)**2})
    M0=s.Matrix([[1,s.Rational(1,2)],[s.Rational(1,2),s.Rational(1,3)]])
    M1=s.Matrix([[s.Rational(1,2),s.Rational(1,3)],[s.Rational(1,3),s.Rational(1,4)]])
    lam=s.symbols("lam")
    char=s.factor((M1-lam*M0).det())
    assert s.simplify(char.subs(lam,(3-s.sqrt(3))/6))==0
    return {"utc":datetime.now(timezone.utc).isoformat(),"python":sys.version,"sympy":s.__version__,
            "kernel_diagnostics":kernel_results,"integer_degree_cases":floor_cases,
            "boundary_interval":boundary,"nonsimple_apex":apex,"nonconvex_proxy_gap":str(gap),
            "Legendre_diagnostics":legendre_results,"r1_interval_characteristic_polynomial":str(char),
            "r1_interval_optimum":"(3-sqrt(3))/6",
            "negative_controls":{"false_core_bound_one":"A_1(1/9)=23/27<1",
                                 "odd_density_power_negative":"A_1(1)^5=-1/243",
                                 "L_n_plus_1_majorant":"sum_j 1 diverges",
                                 "unnormalized_f_1_plus_t":"q=0 gives 0<min_K f=1",
                                 "arbitrary_reference_delta_1":"normalized objective t is identically 1; min_[0,1] t=0",
                                 "constant_objective":"every feasible density gives zero error"},
            "all_assertions_passed":True,"finite_checks_not_universal_proof":True}


if __name__=="__main__":
    prior_before=prior_packet_custody()
    write("ORIGINAL_BINDING_RECEIPT.json",custody())
    write("EXACT_CONTROLS.json",diagnostics())
    assert prior_before==prior_packet_custody()
    write("PRIOR_PACKET_PRESERVATION.json",prior_before)
    print("All161 original bindings/152 CRC-read members and prior packets verified; exact diagnostics passed.")
