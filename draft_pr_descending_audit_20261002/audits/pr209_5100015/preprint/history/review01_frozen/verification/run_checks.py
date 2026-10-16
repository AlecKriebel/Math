"""Offline isolated-copy replay; no archive, environment, network or repository mutation."""
from pathlib import Path
from datetime import datetime,timezone
from concurrent.futures import ThreadPoolExecutor
import argparse,hashlib,json,shutil,subprocess,sys
from integrity import verify
V=Path(__file__).resolve().parent
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output',required=True,help='New directory outside the verification tree')
parser.add_argument('--jobs',type=int,default=2,choices=[1,2,3])
args=parser.parse_args();OUT=Path(args.output).resolve()
assert not OUT.exists() and not OUT.is_relative_to(V) and not V.is_relative_to(OUT),'Output must be a new separate directory'
assert sys.dont_write_bytecode,'Run this harness with python -B'
OUT.mkdir(parents=True);before=verify()
cases=[
 ('author','original_submission/verify.py','original_submission','verification.json','original_submission/verification.json',[]),
 ('inherited','original_submission/independent_review/independent_check.py','original_submission',None,'root_reproductions/root_reproduction_01/inherited_review/stdout.txt',[]),
 ('root_geometry','scope_controls/root_exact_geometry.py',None,'root_reproduction_01/ROOT_EXACT_GEOMETRY.json','root_reproductions/root_reproduction_01/ROOT_EXACT_GEOMETRY.json',['utc']),
 ('source','audits/source_domain_adversary_01/independent_controls.py',None,'control_results.json','audits/source_domain_adversary_01/control_results.json',['created_utc']),
 ('physical','audits/physical_geometry_adversary_01/cartesian_check.py',None,'RESULTS.json','audits/physical_geometry_adversary_01/RESULTS.json',[]),
 ('meromorphic','audits/meromorphic_divisor_adversary_01/check_independent.py',None,'CHECK_RESULTS.json','audits/meromorphic_divisor_adversary_01/CHECK_RESULTS.json',['utc']),
 ('contemporary_comparison','audits/priority_author_updates_01/check_comparison.py',None,'COMPARISON_CHECK_RESULTS.json','audits/priority_author_updates_01/COMPARISON_CHECK_RESULTS.json',['created_utc']),
 ('classical_bridge','audits/priority_classical_general_01/bridge_verify.py',None,'bridge_results.json','audits/priority_classical_general_01/bridge_results.json',[]),
]
def run(case):
 name,script,copytree,outfile,expected,ignored=case;folder=OUT/name;folder.mkdir();source=V/script
 if copytree:
  shutil.copytree(V/copytree,folder/'inputs');program=folder/'inputs'/source.relative_to(V/copytree);work=program.parent
 else:
  program=folder/source.name;shutil.copyfile(source,program);work=folder
 if name=='root_geometry':(folder/'root_reproduction_01').mkdir()
 command=[sys.executable,'-B',str(program)]
 if name=='physical':command+=['--output',str(folder/'RESULTS.json'),'--dps','90']
 started=datetime.now(timezone.utc).isoformat()
 r=subprocess.run(command,cwd=work,capture_output=True,timeout=900)
 (folder/'stdout.txt').write_bytes(r.stdout);(folder/'stderr.txt').write_bytes(r.stderr)
 receipt=dict(name=name,started_utc=started,finished_utc=datetime.now(timezone.utc).isoformat(),returncode=r.returncode,source_program=script,program_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),copied_program_byte_identical=program.read_bytes()==source.read_bytes(),ignored_nonscientific_fields=ignored)
 try:
  assert r.returncode==0,'Checker failed; outputs retained'
  actual=json.loads((work/outfile).read_text()) if outfile else json.loads(r.stdout)
  want=json.loads((V/expected).read_text())
  for k in ignored:actual.pop(k,None);want.pop(k,None)
  assert actual==want,'Scientific result differs from frozen expected output'
  receipt.update(status='PASS',all_scientific_fields_identical=True)
 except Exception as exc:receipt.update(status='FAIL',error=str(exc))
 (folder/'REPLAY_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n');print(name,receipt['status'],flush=True);return receipt
with ThreadPoolExecutor(max_workers=args.jobs) as pool:results=list(pool.map(run,cases))
after=verify();assert before==after
receipt=dict(utc=datetime.now(timezone.utc).isoformat(),status='PASS' if all(x['status']=='PASS' for x in results) else 'FAIL',verified_frozen_files_before_after=before,scientific_programs=len(results),results=results,python=sys.version,limits='Finite exact and uncertified arbitrary-precision controls support written universal proofs. No network, installation or release operation. Copied outputs and failures remain in the requested directory; frozen inputs unchanged.')
(OUT/'REPRODUCTION.json').write_text(json.dumps(receipt,indent=2)+'\n');print(receipt['status']);sys.exit(0 if receipt['status']=='PASS' else 1)
