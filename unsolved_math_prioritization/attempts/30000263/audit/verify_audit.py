#!/usr/bin/env python3
"""Independent finite checks and authenticated optional-input replay.

The analytic audit, not finite samples, establishes the stated partial results.
No author checker is imported. No network operations or source writes occur.
"""
import argparse
from decimal import Decimal as Dec, localcontext
from fractions import Fraction as Rat
import hashlib
import io
import json
import math
from pathlib import Path
import random
import sys
import zipfile

ROOT = Path(__file__).resolve().parent
AUTHOR_HASH = "e2f02d9bcc751e0551ccde2a32ab3ff701e2355b0394aeb24c56b96adb44a14e"
AUTHOR_BYTES = 33182
REVIEW_HASH = "41dce0de0472889e89c4936d3356ad2b0e568c1368a3cff52261db747b141f38"
CORPORA = [
    ("catalog", 21735099, 15458, "891938878f1e395de77f6829d5d5d13cb5d5393f85efaa7941fb14bd3e3d7566"),
    ("problems", 68931837, 15458, "04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf"),
    ("reports", 80334822, 6701, "8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b"),
]
FILES = {
    "README.md", "AUDIT_REPORT.md", "MANDATORY_CORRECTIONS.md", "RESEARCH_LOG.md",
    "verify_audit.py", "audit_controls.py", "pack_audit.py", "INDEPENDENT_RESULTS.json",
    "INPUT_SOURCE_CHECKS.json", "AUTHOR_REPLAY_RESULTS.json", "PUBLIC_SOURCE_REVIEW.json",
    "PRIOR_ARTIFACT_REVIEW.json", "AUDIT_CONTROL_RESULTS.json",
}


def need(ok, why):
    if not ok:
        raise ValueError(why)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def unique(pairs):
    ans = {}
    for key, val in pairs:
        need(key not in ans, "duplicate JSON key")
        ans[key] = val
    return ans


def reject_constant(word):
    raise ValueError("nonfinite JSON constant: " + word)


def decode(data):
    return json.loads(data, object_pairs_hook=unique, parse_constant=reject_constant)


def read(name):
    return decode((ROOT / name).read_bytes())


def manifest():
    actual = list(ROOT.iterdir())
    need(all(p.is_file() and not p.is_symlink() for p in actual), "unexpected directory or symlink")
    need({p.name for p in actual} == FILES | {"MANIFEST.json"}, "package allowlist mismatch")
    m = read("MANIFEST.json")
    need(m["schema"] == 1 and set(m["files"]) == FILES, "manifest allowlist mismatch")
    for name in sorted(FILES):
        raw = (ROOT / name).read_bytes()
        need(m["files"][name] == {"bytes": len(raw), "sha256": digest(raw)}, "manifest mismatch: " + name)
    # Parse every JSON payload, including evidence the mathematical runner does not consume.
    for name in sorted(FILES):
        if name.endswith(".json"):
            read(name)


def line_values(points, weights):
    n = len(points)
    need(n == len(weights) and len(set(points)) == n, "invalid line inputs")
    pot, force = [Rat(0) for _ in points], [Rat(0) for _ in points]
    denom = Rat(0)
    # An unordered-pair implementation, independent of the author's row implementation.
    for i in range(n):
        for j in range(i + 1, n):
            d = points[j] - points[i]
            r = abs(d)
            pot[i] += weights[j] / r
            pot[j] += weights[i] / r
            force[i] -= weights[j] * d / r**3
            force[j] += weights[i] * d / r**3
            denom += (weights[i]**2 + weights[j]**2) / r**2
    g = [-2 * a * f for a, f in zip(weights, force)]
    numerator = sum(t*t for t in pot) + max((abs(t) for t in g), default=Rat(0))
    return pot, force, denom, numerator


def energy(points, weights):
    return sum((weights[i] * weights[j] * abs(points[i] - points[j])
                for i in range(len(points)) for j in range(i+1, len(points))), Rat(0))


def exact_line_checks():
    rng = random.Random(80630000263)
    line_count = 0
    for n in range(2, 11):
        for sample in range(31):
            x = sorted(Rat(v, 7) for v in rng.sample(range(-70, 71), n))
            u = [Rat(rng.randint(-13, 13), rng.randint(1, 9)) for _ in x]
            p, f, d, num = line_values(x, u)
            virial = sum((u[i] * x[i]**3 * f[i] - Rat(3, 2) * u[i] * x[i]**2 * p[i]
                          for i in range(n)), Rat(0))
            need(2*virial + energy(x, u) == 0, "cubic identity")
            w = u[:-1] + [-sum(u[:-1])]
            cumulative = Rat(0)
            gap_energy = Rat(0)
            for i in range(n - 1):
                cumulative += w[i]
                gap_energy -= (x[i+1] - x[i])*cumulative*cumulative
            need(energy(x, w) == gap_energy, "distance-prefix identity")
            need(gap_energy < 0 or all(t == 0 for t in w), "strictness")
            for a in (x[0]-Rat(2, 3), x[-1]+Rat(5, 4), (x[0]+x[1])/2):
                radius = [abs(z-a) for z in x]
                y = [a+1/(z-a) for z in x]
                v = [u[i]/radius[i] for i in range(n)]
                py, fy, _, _ = line_values(y, v)
                for i in range(n):
                    need(py[i] == radius[i]*p[i], "Kelvin line potential")
                    need(fy[i] == radius[i]*(x[i]-a)*p[i] - radius[i]**3*f[i], "Kelvin line full force")
                lifted = [u[i]/radius[i]**2 for i in range(n)]
                need(energy(y, v) == energy(x, lifted), "Kelvin line energy")
            need(sum(-2*u[i]*f[i] for i in range(n)) == 0, "translation force identity")
            line_count += 1

    support_count = 0
    support_one_count = 0
    support_zero_count = 0
    for n in range(2, 12):
        for s in range(n + 1):
            for repeat in range(4):
                x = sorted(Rat(v, 11) for v in rng.sample(range(-100, 101), n))
                active = sorted(rng.sample(range(n), s))
                u = [Rat(0) for _ in x]
                for i in active:
                    u[i] = Rat(rng.choice([-9,-5,-1,1,3,8]), rng.randint(1, 9))
                p, _, d, num = line_values(x, u)
                if s == 0:
                    need(d == num == 0, "empty support")
                    support_zero_count += 1
                elif s == 1:
                    need(num == d and d > 0, "support one exact equality")
                    need(any(p[i] != 0 for i in range(n) if i not in active), "support one zero exclusion")
                    support_one_count += 1
                else:
                    _, _, ds, ns = line_values([x[i] for i in active], [u[i] for i in active])
                    q = sum(p[i]**2 for i in range(n) if i not in active)
                    c = 1 + 4*(2*s-1)*(n-s)
                    need(num == ns+q, "support numerator decomposition")
                    need(d <= c*ds+2*q, "support denominator bound")
                    # Use the exactly computed constant for this active configuration.
                    cs = ns/ds
                    need(num >= min(cs/c, Rat(1, 2))*d, "support constant transfer")
                support_count += 1

    # A finite non-site Kelvin center with zero transformed total charge.
    x = [Rat(0), Rat(1)]
    u = [Rat(1), Rat(-4)]
    a = Rat(1, 3)
    need(sum(u[i]/(x[i]-a)**2 for i in range(2)) == 0, "zero-total center example")
    # This example is not a zero-system configuration.
    return {"rational_line_configurations": line_count, "line_kelvin_centers": 3*line_count,
            "rational_support_configurations": support_count, "support_one_cases": support_one_count,
            "support_zero_cases": support_zero_count, "explicit_finite_kelvin_center_checks": 1}


def decimal_geometry():
    rng = random.Random(20261005806)
    count = 0
    largest = Dec(0)
    with localcontext() as ctx:
        ctx.prec = 80
        def vals(x, u):
            p = [Dec(0) for _ in x]
            f = [[Dec(0)]*3 for _ in x]
            for i in range(len(x)):
                for j in range(i+1, len(x)):
                    delta = [x[i][k]-x[j][k] for k in range(3)]
                    r = sum(z*z for z in delta).sqrt()
                    need(r > 0, "decimal collision")
                    p[i] += u[j]/r
                    p[j] += u[i]/r
                    for k in range(3):
                        f[i][k] += u[j]*delta[k]/r**3
                        f[j][k] -= u[i]*delta[k]/r**3
            return p, f
        for n in range(2, 9):
            for sample in range(9):
                raw = rng.sample([(a,b,c) for a in range(-3,4) for b in range(-3,4)
                                  for c in range(-3,4)], n)
                x = [[Dec(z) for z in row] for row in raw]
                u = [Dec(rng.randint(-11, 11))/Dec(7) for _ in x]
                center = [Dec(1)/3, Dec(2)/5, Dec(-3)/7]
                a = [[x[i][k]-center[k] for k in range(3)] for i in range(n)]
                r2 = [sum(z*z for z in row) for row in a]
                rad = [z.sqrt() for z in r2]
                y = [[center[k]+a[i][k]/r2[i] for k in range(3)] for i in range(n)]
                v = [u[i]/rad[i] for i in range(n)]
                p,f = vals(x,u)
                py,fy = vals(y,v)
                for i in range(n):
                    reflected = [f[i][k]-2*a[i][k]*sum(a[i][h]*f[i][h] for h in range(3))/r2[i]
                                 for k in range(3)]
                    tests = [(py[i],rad[i]*p[i])]
                    tests += [(fy[i][k],rad[i]*a[i][k]*p[i]+rad[i]**3*reflected[k]) for k in range(3)]
                    for actual,expected in tests:
                        err = abs(actual-expected)/(1+abs(expected))
                        largest = max(largest,err)
                        need(err < Dec('1e-65'), "decimal full Kelvin identity")
                count += 1
    return {"decimal_3d_kelvin_configurations": count, "precision_digits": 80,
            "relative_error_tolerance": "1e-65", "max_scaled_error": str(largest),
            "status": "FINITE_HIGH_PRECISION_CHECK_NOT_A_GENERAL_PROOF"}


def exact_counterexamples():
    x = [(Rat(1),Rat(0),Rat(0)), (Rat(-3,5),Rat(4,5),Rat(0)),
         (Rat(-3,5),Rat(-4,5),Rat(0)), (Rat(0),Rat(0),Rat(1,2)),
         (Rat(0),Rat(0),Rat(-1,2)), (Rat(0),Rat(1,4),Rat(0))]
    w = [Rat(3,8),Rat(5,16),Rat(5,16)]
    radii = [sum(z*z for z in row) for row in x]
    need(sum(w)==1 and min(w)>0, "ball weights")
    need(all(sum(w[i]*x[i][k] for i in range(3)) == 0 for k in range(3)), "ball center")
    need(radii == [1,1,1,Rat(1,4),Rat(1,4),Rat(1,16)], "ball contact certificate")
    # The determinant of differences to points 2,3,4 is nonzero.
    a,b,c = [[x[i][k]-x[0][k] for k in range(3)] for i in (1,2,3)]
    det = a[0]*(b[1]*c[2]-b[2]*c[1])-a[1]*(b[0]*c[2]-b[2]*c[0])+a[2]*(b[0]*c[1]-b[1]*c[0])
    need(det == Rat(32,25), "ball affine dimension determinant")
    for center in [(Rat(2,3),Rat(-3,5),Rat(7,11)), (Rat(0),Rat(0),Rat(0))]:
        need(sum(w[i]*sum((x[i][k]-center[k])**2 for k in range(3)) for i in range(3))
             == 1+sum(z*z for z in center), "weighted squared radius identity")
    # Multiply the complex weights by sqrt(2): W2=1-i, W3=2i.
    def mul(a,b):
        return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
    c2=mul((Rat(-1,2),Rat(1,2)),(Rat(1),Rat(-1)))
    c3=mul((Rat(-1,2),Rat(0)),(Rat(0),Rat(2)))
    need(tuple(c2[k]+c3[k] for k in (0,1)) == (0,0), "complex premise")
    need((1,1) != (0,0), "complex conclusion fails")
    return {"minimum_ball_boundary_count": 3, "affine_dimension": 3,
            "affine_determinant": str(det), "complex_local_counterexample": "VERIFIED_LOCAL_ONLY"}


def compute_math():
    return {"line_and_support": exact_line_checks(), "kelvin_3d": decimal_geometry(),
            "counterexamples": exact_counterexamples()}


def replay_numeric(z):
    data=decode(z.read("NUMERIC_RESULTS.json"))
    summary=decode(z.read("NUMERIC_SUMMARY.json"))
    need(data['status']=='FINITE_EXPLORATION_NOT_A_PROOF', "numeric scope")
    need(data['seed']==30000263 and len(data['rows'])==24, "numeric metadata")
    families={}
    objective_error=0.0
    ratio_error=0.0
    for row in data['rows']:
        p, dim = row['p'], row['dimension']
        x,u=row['positions'],row['charges']
        need((p,dim) in {(6,2),(6,3),(7,3),(8,3)}, "numeric family")
        need(len(x)==len(u)==p and all(len(a)==dim for a in x), "numeric shape")
        need(all(math.isfinite(a) for a in u) and all(math.isfinite(a) for b in x for a in b), "nonfinite numeric values")
        pot=[0.0]*p; grad=[[0.0]*dim for _ in x]; denom=0.0; separation=math.inf
        for i in range(p):
            for j in range(i+1,p):
                delta=[x[i][k]-x[j][k] for k in range(dim)]
                r=math.sqrt(math.fsum(t*t for t in delta))
                need(r>0 and math.isfinite(r), "numeric collision")
                separation=min(separation,r)
                pot[i]+=u[j]/r; pot[j]+=u[i]/r
                denom+=(u[i]*u[i]+u[j]*u[j])/(r*r)
                for k in range(dim):
                    term=-2*u[i]*u[j]*delta[k]/(r*r*r)
                    grad[i][k]+=term; grad[j][k]-=term
        need(denom>0 and math.isfinite(denom), "numeric denominator")
        pp=math.fsum(t*t for t in pot)
        ratio=(pp+max(abs(t) for v in grad for t in v))/denom
        objective=pp/denom+math.fsum(t*t for v in grad for t in v)/(denom*denom)
        need(math.isclose(ratio,row['ratio_coordinate'],rel_tol=1e-10,abs_tol=1e-12), "stored ratio")
        need(math.isclose(objective,row['smooth_objective'],rel_tol=1e-9,abs_tol=1e-12), "stored objective")
        need(math.isclose(separation,row['min_separation'],rel_tol=1e-12,abs_tol=1e-12), "stored separation")
        need(math.isclose(math.fsum(a*a for a in u),1,abs_tol=1e-12), "charge gauge")
        need(x[0]==[0.0]*dim and x[1]==[1.0]+[0.0]*(dim-1), "position gauge")
        need(1<=row['nfev']<=500 and row['optimizer_status'] in {0,1,2,3,4}, "optimizer flags")
        key=f'p={p},dimension={dim}'
        family=families.setdefault(key,{'rows':[],'minimum':math.inf,'budget_exhaustions':0})
        need(row['start'] not in family['rows'] and 0<=row['start']<6, "duplicate start")
        family['rows'].append(row['start']); family['minimum']=min(family['minimum'],ratio)
        if row['optimizer_status']==0:
            need(row['nfev']==500, "premature budget status")
            family['budget_exhaustions']+=1
        objective_error=max(objective_error,abs(objective-row['smooth_objective']))
        ratio_error=max(ratio_error,abs(ratio-row['ratio_coordinate']))
    need(len(families)==4 and len(summary['families'])==4, "family coverage")
    for entry in summary['families']:
        f=families[f"p={entry['p']},dimension={entry['dimension']}"]
        need(len(f['rows'])==entry['starts']==6, "summary start count")
        need(f['budget_exhaustions']==entry['evaluation_budget_exhaustions'], "summary budget count")
        need(math.isclose(f['minimum'],entry['minimum_observed_ratio_not_bound'],rel_tol=1e-10), "summary minimum")
    need(summary['all_p_strict_positive_bound_proved'] is False, "numerical proof overclaim")
    return {'status':'PASS_FINITE_REPLAY_NOT_PROOF','rows':24,'families':families,
            'max_absolute_objective_error':objective_error,'max_absolute_ratio_error':ratio_error}


def author_input(path):
    raw=path.read_bytes()
    need(len(raw)==AUTHOR_BYTES and digest(raw)==AUTHOR_HASH, "author ZIP authentication")
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        names=z.namelist()
        need(len(names)==14 and len(set(names))==14, "author ZIP entry count")
        need(all('/' not in n and '\\' not in n and n not in {'.','..'} for n in names), "unsafe author ZIP path")
        m=decode(z.read('MANIFEST.json'))
        need(set(m['files'])==set(names)-{'MANIFEST.json'}, "author manifest names")
        for name in m['files']:
            data=z.read(name)
            need(m['files'][name]=={'bytes':len(data),'sha256':digest(data)}, "author internal manifest")
        return replay_numeric(z)


def external_corpora(paths):
    loaded={}
    for (role,size,count,sha),path in zip(CORPORA,paths):
        raw=path.read_bytes()
        need(len(raw)==size and digest(raw)==sha,"corpus authentication: "+role)
        val=decode(raw);need(len(val)==count,"corpus count: "+role);loaded[role]=val
    records=[r for r in loaded['problems'] if r.get('id')==30000263]
    need(len(records)==1,"unique target record")
    record=records[0]
    need(record['problem_number']=='OWR-1050-014',"target number")
    need(record['problem_number'] not in loaded['reports'],"missing-report convention")
    need(sum(str(r.get('id'))=='30000263' for r in loaded['catalog'])==1,"catalog target uniqueness")
    val=[record,loaded['reports'].get(record['problem_number'],{})]
    need(digest(json.dumps(val,sort_keys=True).encode())==REVIEW_HASH,"complete record review")
    return 'PASS_FULL_INPUT_BYTES_COUNTS_AND_COMPLETE_REVIEW'


def source_inputs(directory):
    meta=read('INPUT_SOURCE_CHECKS.json')
    name_by_tail={'46004':'owr2005_29.pdf','AIHPC_2006__23_5_629_0.pdf':'xu2006.pdf',
                  '2101.10023':'chen2021.pdf','barhi-5.pdf':'lan_lu.pdf','66.pdf':'chen2021_journal.pdf'}
    for s in meta['fresh_pdf_retrievals']:
        name=name_by_tail[s['url'].rsplit('/',1)[-1]]
        raw=(directory/name).read_bytes()
        need(raw.startswith(b'%PDF-') and len(raw)==s['bytes'] and digest(raw)==s['sha256'], "source PDF: "+name)
    return 'PASS_FIVE_PDF_BYTE_PINS'


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--author-zip',type=Path)
    ap.add_argument('--corpora',type=Path,nargs=3)
    ap.add_argument('--source-dir',type=Path)
    args=ap.parse_args()
    manifest()
    result=read('INDEPENDENT_RESULTS.json')
    need(result['verdict']=='ACCEPT_PARTIAL_RESULTS_NO_GENERAL_RESOLUTION',"audit verdict")
    need(result['mandatory_correction_count']==0,"mandatory correction count")
    need(result['author_zip']=={'bytes':AUTHOR_BYTES,'sha256':AUTHOR_HASH},"audit author pin")
    controls=read('AUDIT_CONTROL_RESULTS.json')
    need(controls['status']=='PASS' and controls['case_count']==len(controls['cases'])==26,"recorded control coverage")
    expected_cases={'relocated_clean_with_supplied_inputs','changed_bytes','missing_file','extra_file',
                    'symlink','wrong_verdict','wrong_math_count','duplicate_json_key','nonfinite_json',
                    'empty_manifest','author_zip_bit_flip','full_corpus_bit_flip','source_pdf_bit_flip'}
    need({(r['case'],r['optimized']) for r in controls['cases']}==
         {(c,mode) for c in expected_cases for mode in (False,True)},"recorded control identities")
    for row in controls['cases']:
        expected='PASS' if row['case']=='relocated_clean_with_supplied_inputs' else 'FAIL'
        need(row['expected']==row['observed']==expected,"recorded control result")
    math_result=compute_math()
    need(result['math_checks']==math_result,"independent mathematical replay")
    sources=read('INPUT_SOURCE_CHECKS.json')
    need(sources['input_checks']['target_review_sha256']==REVIEW_HASH,"stored complete review")
    need(sources['all_five_fresh_pdf_pins_match'] is True,"fresh PDF pin flag")
    need(len(sources['fresh_pdf_retrievals'])==5 and all(s['author_pin_match'] is True for s in sources['fresh_pdf_retrievals']),"fresh source count")
    for role,size,count,sha in CORPORA:
        need(sources['input_checks'][role]=={'bytes':size,'count':count,'sha256':sha},"stored corpus pin")
    ext={'author_zip':'NOT_PROVIDED','corpora':'NOT_PROVIDED','source_pdfs':'NOT_PROVIDED'}
    if args.author_zip:
        ext['author_zip']=author_input(args.author_zip)
        saved=result['numeric_replay']
        actual=ext['author_zip']
        need(saved['status']==actual['status'] and saved['rows']==actual['rows'],"stored numeric replay scope")
        need(set(saved['families'])==set(actual['families']),"stored numeric replay families")
        for key,family in actual['families'].items():
            old=saved['families'][key]
            need(old['rows']==family['rows'] and old['budget_exhaustions']==family['budget_exhaustions'],"stored numeric replay metadata")
            need(math.isclose(old['minimum'],family['minimum'],rel_tol=1e-10,abs_tol=1e-12),"stored numeric replay minimum")
    if args.corpora:
        ext['corpora']=external_corpora(args.corpora)
    if args.source_dir:
        ext['source_pdfs']=source_inputs(args.source_dir)
    print(json.dumps({'status':'PASS_PARTIAL_AUDIT_CHECKS_NOT_GENERAL_CONJECTURE',
                      'optimized_python':not __debug__,'external':ext,'math_checks':math_result},sort_keys=True))


if __name__=='__main__':
    try:
        main()
    except Exception as exc:
        print('FAIL: '+str(exc),file=sys.stderr)
        sys.exit(1)
