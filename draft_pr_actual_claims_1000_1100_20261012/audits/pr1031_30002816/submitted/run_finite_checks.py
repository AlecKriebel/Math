#!/usr/bin/env python3
"""Replay the preserved independent exact checker without writing sealed inputs."""
from copy import deepcopy
from fractions import Fraction
from pathlib import Path
import hashlib,json,os,subprocess,sys,tempfile

def need(ok,message):
 if not ok:raise RuntimeError(message)
def same(a,b):
 if type(a) is not type(b):return False
 if type(b) is dict:return set(a)==set(b) and all(same(a[k],v) for k,v in b.items())
 if type(b) is list:return len(a)==len(b) and all(same(x,y) for x,y in zip(a,b))
 return a==b
sha=lambda b:hashlib.sha256(b).hexdigest()
ROOT=Path(__file__).resolve().parent
PUBLIC_PINS_SHA256='ceac31e462fed3af808df075a236de5663e9a7602ea800f02549de0961079a47'
POSITIVES={"arithmetic":"integer pairs and exact rational parsing","columns":225,"general_projector":{"independent_real_variables":24,"nonzero_coordinate_polynomials":495,"polynomial_terms_after_cancellation":11760,"verified_exterior_coordinates":495},"gram_diagonal":{"1":15,"2":210},"mixed_minors":9,"phi_trace":True,"python_optimization":0,"q_pure_trace":True,"rank":225,"readonly":None,"status":"PASS"}
EXPECTED_MUTATIONS=[('global_orientation_sign','COORDINATE_MISMATCH: column 0'),('missing_quarter_normalization','COORDINATE_MISMATCH: column 0'),('conjugate_projector_imaginary_sign','COORDINATE_MISMATCH: column 16'),('drop_real_offdiagonal','COORDINATE_MISMATCH: column 15'),('corrupt_pure_diagonal','COORDINATE_MISMATCH: column 0'),('corrupt_mixed_diagonal','COORDINATE_MISMATCH: column 2'),('swap_hermitian_basis_label','HERMITIAN_BASIS_ORDER'),('reverse_complex_orientation_label','REAL_BASIS_ORDER'),('bivector_basis_permutation','COMPLEX_BASIS_ORDER'),('duplicate_exterior_entry','ENTRY_ORDER_OR_DUPLICATE'),('invalid_exact_denominator','ENTRY_VALUE_PARSE'),('wrong_hermitian_gram_norm','GRAM_METADATA'),('missing_inverse_norm_factor','INVERSE_METADATA'),('missing_embedding_column','COLUMN_COUNT'),('unexpected_schema_field','SCHEMA_KEYS')]
def mutations(original):
    def fresh():
        return deepcopy(original)
    out = []
    obj = fresh()
    for col in obj["columns"]:
        for entry in col["entries"]:
            entry[1] = str(-Fraction(entry[1]))
    out.append(("global_orientation_sign", obj, "COORDINATE_MISMATCH"))
    obj = fresh()
    for col in obj["columns"]:
        for entry in col["entries"]:
            entry[1] = str(4*Fraction(entry[1]))
    out.append(("missing_quarter_normalization", obj, "COORDINATE_MISMATCH"))
    obj = fresh()
    for col in obj["columns"]:
        if col["label"][0] == "imag":
            for entry in col["entries"]:
                entry[1] = str(-Fraction(entry[1]))
    out.append(("conjugate_projector_imaginary_sign", obj, "COORDINATE_MISMATCH"))
    obj = fresh()
    obj["columns"][15]["entries"] = []
    out.append(("drop_real_offdiagonal", obj, "COORDINATE_MISMATCH"))
    obj = fresh()
    obj["columns"][0]["entries"][0][1] = "1/2"
    out.append(("corrupt_pure_diagonal", obj, "COORDINATE_MISMATCH"))
    obj = fresh()
    obj["columns"][2]["entries"][0][1] = "-1"
    out.append(("corrupt_mixed_diagonal", obj, "COORDINATE_MISMATCH"))
    obj = fresh()
    obj["columns"][16]["label"][0] = "real"
    out.append(("swap_hermitian_basis_label", obj, "HERMITIAN_BASIS_ORDER"))
    obj = fresh()
    obj["real_basis_order"][0], obj["real_basis_order"][1] = obj["real_basis_order"][1], obj["real_basis_order"][0]
    out.append(("reverse_complex_orientation_label", obj, "REAL_BASIS_ORDER"))
    obj = fresh()
    obj["complex_bivector_pairs_0based"][0], obj["complex_bivector_pairs_0based"][1] = obj["complex_bivector_pairs_0based"][1], obj["complex_bivector_pairs_0based"][0]
    out.append(("bivector_basis_permutation", obj, "COMPLEX_BASIS_ORDER"))
    obj = fresh()
    obj["columns"][0]["entries"].append(deepcopy(obj["columns"][0]["entries"][0]))
    out.append(("duplicate_exterior_entry", obj, "ENTRY_ORDER_OR_DUPLICATE"))
    obj = fresh()
    obj["columns"][0]["entries"][0][1] = "1/0"
    out.append(("invalid_exact_denominator", obj, "ENTRY_VALUE_PARSE"))
    obj = fresh()
    obj["gram_diagonal"][15] = 1
    out.append(("wrong_hermitian_gram_norm", obj, "GRAM_METADATA"))
    obj = fresh()
    obj["inverse_on_image"] = "A^T"
    out.append(("missing_inverse_norm_factor", obj, "INVERSE_METADATA"))
    obj = fresh()
    obj["columns"].pop()
    out.append(("missing_embedding_column", obj, "COLUMN_COUNT"))
    obj = fresh()
    obj["unreviewed_extra"] = True
    out.append(("unexpected_schema_field", obj, "SCHEMA_KEYS"))
    return out

def main():
 need(len(sys.argv)==1,'no extra arguments')
 need(os.getuid()==os.geteuid()==1000,'UID=EUID=1000')
 need(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode,'-I -S -B required')
 raw=(ROOT/'PUBLIC_INPUT_PINS.json').read_bytes();need(sha(raw)==PUBLIC_PINS_SHA256,'public input pins changed')
 pins=json.loads(raw)['files'];before={}
 for n,pin in pins.items():
  b=(ROOT/n).read_bytes();need(same(dict(bytes=len(b),sha256=sha(b)),pin),'public input changed');before[n]=b
 checker=ROOT/'current/audit_exact_embedding.py';certificate=ROOT/'current/EMBEDDING_CERTIFICATE.json'
 original=json.loads(before['current/EMBEDDING_CERTIFICATE.json']);mutants=mutations(original)
 need(len(mutants)==15 and [v[0] for v in mutants]==[v[0] for v in EXPECTED_MUTATIONS],'exact mutation identities')
 mode=[] if sys.flags.optimize==0 else ['-'+'O'*sys.flags.optimize]
 cases=[]
 def run(identity,path,expected_exit,expected,category):
  command=[sys.executable,'-I','-S','-B',*mode,str(checker),'--certificate',str(path)]
  r=subprocess.run(command,cwd=ROOT,env=dict(PATH=os.defpath,HOME='/tmp',TMPDIR='/tmp',LC_ALL='C'),capture_output=True,timeout=120)
  wanted=(json.dumps(expected,sort_keys=True)+'\n').encode()
  need(type(r.returncode) is int and r.returncode==expected_exit,'exact exit '+identity)
  need(r.stderr==b'' and r.stdout==wanted,'complete raw output '+identity)
  need(same(json.loads(r.stdout),expected),'recursive exact output types '+identity)
  cases.append(dict(identity=identity,category=category,exit_code=r.returncode,expected_exit=expected_exit,stdout=r.stdout.decode(),stderr=r.stderr.decode(),stdout_sha256=sha(r.stdout),stderr_sha256=sha(r.stderr),reason='exact coordinate checks passed' if expected_exit==0 else expected['error'],complete_raw_output_equal=True,exact_types=True))
 positive=deepcopy(POSITIVES);positive['python_optimization']=sys.flags.optimize
 run('independent_complete_embedding',certificate,0,positive,'positive')
 with tempfile.TemporaryDirectory(prefix='grassmann-exact-mutants-') as td:
  for index,((identity,obj,prefix),(_,reason)) in enumerate(zip(mutants,EXPECTED_MUTATIONS)):
   need(reason.startswith(prefix),'rejection class contract')
   path=Path(td)/(identity+'.json');path.write_text(json.dumps(obj,sort_keys=True)+'\n')
   need(obj!=original,'mutation actually changes certificate')
   run(identity,path,1,{'status':'FAIL','error':reason},'coordinate_matrix_mutants' if index<6 else 'certificate_schema_and_metadata_mutants')
 need(all((ROOT/n).read_bytes()==b for n,b in before.items()),'public inputs changed')
 need(len(cases)==16 and sum(c['expected_exit']==0 for c in cases)==1,'exact nonempty cases')
 print(json.dumps(dict(status='passed',schema=1,problem_id=30002816,python_optimize=sys.flags.optimize,uid=os.getuid(),euid=os.geteuid(),positive_checker_runs=1,expected_mutant_rejections=15,rejection_categories={'coordinate_matrix_mutants':6,'certificate_schema_and_metadata_mutants':9},cases=cases,public_input_count=len(pins),whole_public_input_unchanged=True,writing_author_generator='NOT_RUN',external_theorem_reproved=False),indent=2,sort_keys=True))
if __name__=='__main__':
 try:main()
 except (RuntimeError,ValueError,TypeError,KeyError,OSError,subprocess.TimeoutExpired) as exc:
  print('REJECT: exact finite suite: '+str(exc),file=sys.stderr);sys.exit(1)
