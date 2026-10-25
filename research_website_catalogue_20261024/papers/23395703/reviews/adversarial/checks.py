"""Independent SymPy/rational audit; no supplied program is imported or executed.

Reconstructs ambient differentiation, exact sections, flat lattice and syzygies;
independently checks the literal deposited certificate data and finite scopes.
Writes only this new adversarial namespace and refuses evidence overwrite.
"""
from pathlib import Path, PurePosixPath
from hashlib import sha256
from datetime import datetime, timezone
from itertools import combinations
import json
import stat
import sys
import zipfile
import sympy as s

HERE=Path(__file__).resolve().parent
SOURCE=HERE.parents[1]/"sources"
ROOT=HERE.parents[3]
x,y,z,w=s.symbols("x y z w")
a,b,c=s.symbols("a b c")
AMBIENT=(x,y,z,w)
ROWS=[(1,0,0,0),(0,1,0,0),(1,-1,0,0),(1,-2,0,0),(0,0,1,0),(0,0,0,1),(1,0,1,1)]
FACTORS=[sum(q*v for q,v in zip(row,AMBIENT)) for row in ROWS]
Q=s.prod(FACTORS)
POLARS=[s.diff(Q,v).expand() for v in AMBIENT]


def h(data):return sha256(data).hexdigest()


def write(name,value):
    path=HERE/name
    if path.exists():raise RuntimeError("Refusing evidence overwrite: "+name)
    path.write_text(json.dumps(value,indent=2,ensure_ascii=False)+"\n")


def mons(n,d):
    if n==1:return [(d,)]
    return [(j,)+tail for j in range(d,-1,-1) for tail in mons(n-1,d-j)]


def monomial(powers,variables):return s.prod(v**k for v,k in zip(variables,powers))


def restricted(forms):
    return [p.subs(dict(zip(AMBIENT,forms)),simultaneous=True).expand() for p in POLARS]


def macaulay(polars,variables,degree,grevlex=False):
    powers=mons(len(variables),degree)
    if grevlex:powers.sort(key=lambda e:tuple(-v for v in reversed(e)),reverse=True)
    columns=[monomial(e,variables) for e in powers]
    multipliers=[monomial(e,variables) for e in mons(len(variables),degree-6)]
    rows=[]
    for p in polars:
        for multiplier in multipliers:
            poly=s.Poly(p*multiplier,*variables)
            rows.append([poly.coeff_monomial(term) for term in columns])
    return s.Matrix(rows),powers


def rank_record(matrix,powers):
    _,columns=matrix.rref();_,rows=matrix.T.rref()
    determinant=matrix.extract(rows,columns).det()
    left=matrix.T.nullspace()
    assert determinant!=0 and len(left)==matrix.rows-len(columns)
    assert all(matrix.T*vector==s.zeros(matrix.cols,1) for vector in left)
    return {"rows":matrix.rows,"columns":matrix.cols,"rank":len(columns),
            "quotient_dimension":matrix.cols-len(columns),"monomials":powers,
            "nonzero_minor_rows":list(rows),"nonzero_minor_columns":list(columns),
            "minor_determinant":str(determinant),"complete_left_kernel":[list(map(str,v)) for v in left]}


def decode(records,variables):
    return s.expand(sum(s.Rational(row["coefficient"])*monomial(row["exponents"],variables) for row in records))


def custody():
    seal_bytes=(SOURCE/"SOURCE_READY_SEAL.json").read_bytes()
    manifest_bytes=(SOURCE/"SOURCE_READY_MANIFEST.json").read_bytes()
    assert h(seal_bytes)=="71125e7f4f982d19951983c9c94e3f528b9b137feb367cd83de689d1013ec933"
    assert h(manifest_bytes)=="c99057222a53f393bc00b87fbb18cb086767771efd632c76d20c42f90ff6fbfe"
    manifest=json.loads(manifest_bytes)
    assert manifest["file_count"]==len(manifest["files"])==88
    bindings=[]
    for item in manifest["files"]:
        data=(SOURCE/item["path"]).read_bytes()
        actual={"path":item["path"],"bytes":len(data),"sha256":h(data)}
        assert actual==item
        bindings.append(actual)
    assert (SOURCE/"seven_plane_gin.tex").read_bytes()==(SOURCE/"published-source/seven_plane_gin.tex").read_bytes()
    members=[]
    with zipfile.ZipFile(SOURCE/"verification-package.zip") as archive:
        entries=archive.infolist()
        assert len(entries)==78 and len({e.filename for e in entries})==78
        for entry in entries:
            name=PurePosixPath(entry.filename)
            assert not name.is_absolute() and ".." not in name.parts and "\\" not in entry.filename
            assert not entry.is_dir() and not stat.S_ISLNK(entry.external_attr>>16)
            data=archive.read(entry)
            assert data==(SOURCE/"published-source"/entry.filename).read_bytes()
            members.append({"member":entry.filename,"bytes":len(data),"sha256":h(data),
                            "CRC32":f"{entry.CRC:08x}","CRC_read_pass":True,"equals_frozen_extracted_original":True})
    record=json.loads((SOURCE/"record.raw.json").read_text())
    assert "version" not in record["metadata"]
    return {"utc":datetime.now(timezone.utc).isoformat(),"status":"ALL_88_ORIGINAL_BINDINGS_AND_78_MEMBERS_AUTHENTICATED",
            "source_ready_manifest_sha256":h(manifest_bytes),"source_ready_seal_sha256":h(seal_bytes),
            "bindings":bindings,"archive_members":members,"separate_and_embedded_TeX_identical":True,
            "record_id":record["id"],"version_field_present":False,"version":None,
            "publication_date":record["metadata"]["publication_date"],"created":record["created"],
            "updated":record["updated"],"original_source_code_executed":False,"original_bytes_mutated":False}


def prior_custody():
    targets=[("papers/23074543/reviews/adversarial","289a69d2eb79c2f907b584bf3eb34e16d5e7e04a98669e4052ac87ccfaf49aa7"),
             ("verification/cfh-independent-code-audit-sol-20261025","08df6760943ae91c7fb4f22b5bc6952aea2325bc87ae1b1623a47af5dbdb984f"),
             ("papers/23442760/reviews/adversarial","97745de4ecdbbfd9cdd465150871285f42a484668e12f88ea4852b48e33e5518")]
    results=[]
    for relative,expected in targets:
        directory=ROOT/relative;seal_bytes=(directory/"FINAL_SEAL.json").read_bytes()
        assert h(seal_bytes)==expected
        seal=json.loads(seal_bytes);manifest_bytes=(directory/seal["manifest"]).read_bytes()
        assert h(manifest_bytes)==seal["manifest_sha256"]
        files=json.loads(manifest_bytes)["files"]
        if isinstance(files,dict):files=[{"path":name,**item} for name,item in files.items()]
        for item in files:
            data=(directory/item["path"]).read_bytes()
            assert len(data)==item["bytes"] and h(data)==item["sha256"]
        results.append({"directory":str(directory),"seal_sha256":expected,"owned_files_verified":len(files),
                        "read_scope":"Bytes only; prior opinions not consumed."})
    return results


def diagnostics():
    assert s.expand(sum(v*p for v,p in zip(AMBIENT,POLARS))-7*Q)==0
    ambient_rows=s.Matrix(ROWS);assert ambient_rows.rank()==4
    flats=set()
    for i,j in combinations(range(7),2):
        pair=ambient_rows[[i,j],:]
        assert pair.rank()==2
        closure=tuple(k for k in range(7) if pair.col_join(ambient_rows[[k],:]).rank()==2)
        flats.add(closure)
    assert len(flats)==16 and sorted(map(len,flats))==[2]*15+[4]
    assert (0,1,2,3) in flats
    circuits=[]
    for size in range(2,6):
        for subset in combinations(range(7),size):
            if ambient_rows[list(subset),:].rank()<size and all(ambient_rows[list(part),:].rank()==size-1 for part in combinations(subset,size-1)):
                circuits.append(subset)
    expected=set(combinations(range(4),3))|{(0,4,5,6)}|{tuple(sorted((*pair,4,5,6))) for pair in combinations((1,2,3),2)}
    assert set(circuits)==expected
    C0=s.Matrix([[1,0,0,0],[0,1,0,0],[2,3,1,0],[7,11,3,1]])
    assert C0.det()==1
    T=(a,b,c,a+2*b+3*c);U=(a,b,2*a+3*b,7*a+11*b)
    p3=restricted(T);p2=restricted(U)
    assert [p.subs(c,2*a+3*b).expand() for p in p3]==p2
    factor_rows=[s.Poly(f.subs(dict(zip(AMBIENT,U)),simultaneous=True),a,b) for f in FACTORS]
    vectors=[(p.coeff_monomial(a),p.coeff_monomial(b)) for p in factor_rows]
    determinants=[{"pair":[i,j],"determinant":str(s.det(s.Matrix([vectors[i],vectors[j]])))} for i,j in combinations(range(7),2)]
    assert all(s.Rational(item["determinant"])!=0 for item in determinants)
    records=[]
    for variables,polars,degrees in [((a,b,c),p3,(6,7)),((a,b),p2,(6,7,8,9))]:
        for degree in degrees:
            matrix,powers=macaulay(polars,variables,degree)
            records.append({"variables":len(variables),"degree":degree,**rank_record(matrix,powers)})
    assert [row["rank"] for row in records]==[4,12,4,7,9,10]
    displayed=[11*a,11*b,-73*(2*a+3*b),25*(7*a+11*b)]
    assert s.expand(sum(u*f for u,f in zip(displayed,p2)))==0
    # Inspect and check actual deposited certificate data by a distinct engine.
    cert_path=SOURCE/"published-source/audits/exact_reproduction_audit_01/EXACT_CERTIFICATE.json"
    cert=json.loads(cert_path.read_text())
    assert decode(cert["ambient_polynomial"],AMBIENT)==s.expand(Q)
    for key,expected_polars,variables in [("ambient_polars",POLARS,AMBIENT),("ternary_polars",p3,(a,b,c)),("binary_polars",p2,(a,b))]:
        assert [decode(poly,variables) for poly in cert[key]]==expected_polars
    for row in cert["ternary_Macaulay"]+cert["binary_Macaulay"]:
        variables,polars=((a,b,c),p3) if row["variables"]==3 else ((a,b),p2)
        matrix,powers=macaulay(polars,variables,row["degree"])
        assert powers==[tuple(e) for e in row["monomial_order"]]
        assert matrix==s.Matrix([[s.Rational(v) for v in r] for r in row["matrix"]])
        assert matrix.extract(row["rank_minor_rows"],row["rank_minor_columns"]).det()==s.Rational(row["rank_minor_determinant"])!=0
        left=[s.Matrix([s.Rational(q) for q in vector]) for vector in row["left_kernel_basis"]]
        assert len(left)==matrix.rows-row["rank"] and all(matrix.T*v==s.zeros(matrix.cols,1) for v in left)
        assert not left or s.Matrix.hstack(*left).rank()==len(left)
    HB=s.Matrix([[decode(entry,(a,b)) for entry in row] for row in cert["binary_Hilbert_Burch"]["matrix"]])
    assert (s.Matrix(1,4,p2)*HB).applyfunc(s.expand)==s.zeros(1,3)
    common=s.Rational(cert["binary_Hilbert_Burch"]["signed_maximal_minors_equal_polars_times"])
    for i in range(4):
        minor=s.expand((-1)**i*HB[[j for j in range(4) if j!=i],:].det())
        assert s.expand(minor-common*p2[i])==0
        assert minor==decode(cert["binary_Hilbert_Burch"]["signed_maximal_minors"][i],(a,b))
    assert [max(s.Poly(HB[i,j],a,b).total_degree() for i in range(4)) for j in range(3)]==[1,2,3]
    # Verify deposited binary Groebner data, including all S-pairs, using SymPy.
    orth_path=SOURCE/"published-source/audits/exact_reproduction_audit_01/ORTHOGONAL_CERTIFICATE.json"
    orth=json.loads(orth_path.read_text());C4=s.Matrix(orth["GL4_control_matrix"])
    assert C4.det()==-2
    C2=[sum(C4[i,j]*v for j,v in enumerate((a,b))) for i in range(4)]
    C2polars=restricted(C2)
    gb=[decode(poly,(a,b)) for poly in orth["exact_binary_Groebner"]["basis"]]
    leads=[s.Poly(poly,a,b).terms(order="grevlex")[0][0] for poly in gb]
    assert [list(e) for e in leads]==orth["exact_binary_Groebner"]["leading_exponents"]
    reps=orth["exact_binary_Groebner"]["representations_in_ambient_polar_generators"]
    for poly,coefficients in zip(gb,reps):
        assert s.expand(poly-sum(decode(coef,(a,b))*f for coef,f in zip(coefficients,C2polars)))==0
    assert all(s.reduced(f,gb,a,b,order="grevlex")[1]==0 for f in C2polars)
    pairs=0
    for i,j in combinations(range(len(gb)),2):
        ei,ci=s.Poly(gb[i],a,b).terms(order="grevlex")[0]
        ej,cj=s.Poly(gb[j],a,b).terms(order="grevlex")[0]
        lcm=tuple(max(p,q) for p,q in zip(ei,ej))
        S=monomial(tuple(p-q for p,q in zip(lcm,ei)),(a,b))*gb[i]/ci-monomial(tuple(p-q for p,q in zip(lcm,ej)),(a,b))*gb[j]/cj
        assert s.reduced(s.expand(S),gb,a,b,order="grevlex")[1]==0
        pairs+=1
    assert pairs==orth["exact_binary_Groebner"]["Buchberger_pairs_checked"]
    # Excluded-case and distinction controls.
    after_restriction=[s.diff(Q.subs(dict(zip(AMBIENT,T)),simultaneous=True),v).expand() for v in (a,b,c)]
    def constant_rank(polys,variables):
        powers=mons(len(variables),6)
        return s.Matrix([[s.Poly(p,*variables).coeff_monomial(monomial(e,variables)) for e in powers] for p in polys]).rank()
    assert constant_rank(p3,(a,b,c))==4 and constant_rank(after_restriction,(a,b,c))==3
    assert all(s.Poly(p,a,b,c).coeff_monomial(a**6)==0 for p in p3)
    bad=restricted((a,b,c,2*a+3*c));badmatrix,_=macaulay(bad,(a,b,c),7)
    assert badmatrix.rank()==11
    edge=(a,b,2*a+3*b,s.Rational(11,2)*a+9*b)
    edgepolars=restricted(edge)
    assert s.expand(sum(u*f for u,f in zip([edge[0],edge[1],-6*edge[2],2*edge[3]],edgepolars)))==0
    assert macaulay(edgepolars,(a,b),7)[0].rank()==7
    edgefactors=[f.subs(dict(zip(AMBIENT,edge)),simultaneous=True).expand() for f in FACTORS]
    edgevectors=[(s.Poly(f,a,b).coeff_monomial(a),s.Poly(f,a,b).coeff_monomial(b)) for f in edgefactors]
    assert all(s.det(s.Matrix([u,v]))!=0 for u,v in combinations(edgevectors,2))
    t=s.symbols("t")
    numerator=1-4*t**6+t**7+t**8+t**9
    assert numerator.subs(t,1)==s.diff(numerator,t).subs(t,1)==0
    hf=s.series(numerator/(1-t)**2,t,0,10).removeO().expand()
    assert [hf.coeff(t,j) for j in (6,7,8)]==[3,1,0]
    return {"utc":datetime.now(timezone.utc).isoformat(),"python":sys.version,"sympy":s.__version__,
            "field":"Q; exact identities and nonzero integer/rational certificates remain valid in all characteristic0 fields",
            "ambient_rank":4,"rank2_flats":[list(flat) for flat in sorted(flats)],"matroid_circuits":[list(C) for C in circuits],
            "unique_multiplicity4_flat":[0,1,2,3],"parallel_connection_circuit_formula_exact":True,
            "C0_determinant":1,"all21_binary_pair_determinants":determinants,"Macaulay_certificates":records,
            "displayed_binary_syzygy_exact":True,"actual_deposited_certificate_polynomials_matrices_minors_and_full_left_kernels_verified":True,
            "Hilbert_Burch_matrix":[list(map(str,HB.row(i))) for i in range(4)],"Hilbert_Burch_common_minor_factor":str(common),
            "all4_Hilbert_Burch_minors_and_syzygy_columns_verified":True,
            "deposited_binary_Groebner_representations_and_all_S_pairs_verified":pairs,
            "binary_Hilbert_values_6_7_8":[3,1,0],"ternary_Hilbert_values_5_6_7":[21,24,24],"multiplication_kernel_values_6_7":[0,1],
            "negative_controls":{"restricted_ambient_vs_ternary_Jacobian_degree6_ranks":[4,3],
                                 "favorable_section_not_a_gin_certificate":"Raw ternary coordinate degree6 span has no a^6 coefficient, while characteristic0 gin must contain its first-variable sixth power.",
                                 "X_Z_W_dependence_bad_ternary_degree7_rank":11,
                                 "trace_t_coefficient_zero_still_unique_binary_linear_syzygy":True,
                                 "characteristic7":"Euler becomes a nonzero linear polar syzygy; no extension claimed.",
                                 "characteristic2":"x-2y=x, so seven distinct factors fail."},
            "all_assertions_pass":True,"finite_coordinates_do_not_establish_genericity_or_full_gin":True,
            "supplied_programs_executed":False}


if __name__=="__main__":
    before=prior_custody()
    write("ORIGINAL_BINDING_RECEIPT.json",custody())
    write("EXACT_CONTROLS.json",diagnostics())
    assert before==prior_custody()
    write("PRIOR_PACKET_PRESERVATION.json",before)
    print("Exact rational reconstruction, deposited certificate data,88 bindings/78 members and three prior packets verified.")
