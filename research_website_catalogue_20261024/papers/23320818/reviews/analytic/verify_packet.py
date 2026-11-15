#!/usr/bin/env python3
"""Read-only packet/native/primary custody and independent exact replay.
Does not rerun the source wrapper's temporary-writing full programme; its two
already completed full receipts are checked separately, with current guards.
"""
from pathlib import Path,PurePosixPath
import hashlib,json,runpy,subprocess,sys
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
def need(t,s):
 if not t:raise RuntimeError(s)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rerun(file,*flags):
 r=subprocess.run([sys.executable,'-B',*flags,str(HERE/file)],capture_output=True,text=True,check=True)
 need(not r.stderr,'unexpected stderr '+file);return json.loads(r.stdout)
def main():
 need(len(sys.argv)==1,'No arguments accepted')
 seal=json.loads((HERE/'FINAL_SEAL.json').read_text());need(sha(HERE/'FINAL_MANIFEST.json')==seal['manifest_sha256'],'final manifest seal')
 m=json.loads((HERE/'FINAL_MANIFEST.json').read_text());names=set()
 for row in m['files']:
  name=row['path'];q=PurePosixPath(name);p=HERE/name
  need(str(q)==name and not q.is_absolute() and '..' not in q.parts and name not in names,'safe unique owned path');names.add(name)
  need(p.is_file() and not p.is_symlink() and p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],'owned bytes changed '+name)
 exclude=lambda p:p.is_relative_to(HERE/'cache/deps') or p.is_relative_to(HERE/'cache/tmp')
 actual={p.relative_to(HERE).as_posix() for p in HERE.rglob('*') if p.is_file() and not exclude(p)}
 need(actual==names|{'FINAL_MANIFEST.json','FINAL_SEAL.json'},'owned file set changed')
 inputs=json.loads((HERE/'INPUT_BINDINGS.json').read_text())['files']
 for name,w in inputs.items():
  p=Path(name);need(p.is_file() and p.stat().st_size==w['bytes'] and sha(p)==w['sha256'],'external original changed '+name)
 native=rerun('verify_source_custody.py');need(native==json.loads((HERE/'SOURCE_CUSTODY.json').read_text()),'native replay changed')
 normal=rerun('independent_verify.py');optimized=rerun('independent_verify.py','-O')
 need(normal==json.loads((HERE/'INDEPENDENT_NORMAL.json').read_text()) and optimized==json.loads((HERE/'INDEPENDENT_OPTIMIZED.json').read_text()),'independent exact replay changed')
 n=dict(normal);o=dict(optimized);n.pop('optimized');o.pop('optimized');need(n==o,'normal optimized exact outcomes differ')
 full=(HERE/'FULL_REPLAY_NORMAL.json').read_bytes();need(full==(HERE/'FULL_REPLAY_OPTIMIZED.json').read_bytes() and hashlib.sha256(full).hexdigest()=='8e46c0fdb6a61ca4ec1be99573e3e2aa97fa3507afb1fc64beae5f36d3503ce8','stored actual full receipts differ')
 receipt=json.loads(full);need(receipt['status']=='PASS' and receipt['profile']=='full' and receipt['dependencies']=={'mpmath':'1.3.0','sympy':'1.14.0'} and receipt['history_and_payloads_unchanged'] is True and receipt['finite_checks_replace_analytic_proof'] is False,'full receipt scope changed')
 need(receipt['independent_symbolic']['actual_intended_rejection_executions']==32 and receipt['explicit_guard_rejection_controls']==13,'full rejection evidence changed')
 driver=runpy.run_path(str(ROOT/'sources/published-source/verification/run_verification.py'))
 need(driver['check_manifest']()==35 and driver['check_history']()==receipt['history'] and driver['check_code_origins']()==4 and driver['guard_self_checks']()==13,'current source manifests/history/guards changed')
 need((HERE/'.gitignore').read_text()=='/cache/deps/\n/cache/tmp/\n','dependency-only ignore missing')
 print(json.dumps({'assessment':'SEALED_ANALYTIC_REVIEW_CUSTODY_AND_EXACT_REPLAY_SUPPORTED','owned_files':len(names),'external_original_bindings':len(inputs),'original_ZIP_payloads_preserved':native['original_ZIP_payloads_compared'],'native_source_files':native['native_total_files'],'exact_independent_controls':normal['exact_checks'],'false_generic_identities_rejected':normal['false_identities_rejected'],'stored_full_source_profiles_normal_and_optimized_identical':True,'full_source_reexecution_performed_by_this_packet_verifier':False,'current_source_manifest_payloads':35,'current_source_guard_rejections':13,'mathematical_proof_replaced_by_computation':False,'publication_authority':False},sort_keys=True,indent=2))
if __name__=='__main__':main()
