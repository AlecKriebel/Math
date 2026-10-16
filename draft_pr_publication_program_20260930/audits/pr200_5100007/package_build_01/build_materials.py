"""Build portable PR200 verification sources. No dependency/runtime redistribution."""
from pathlib import Path
import ast,hashlib,json,shutil
A=Path(__file__).resolve().parent.parent;P=A/'publication_package_v1';M=P/'materials';M.mkdir(exist_ok=True)
def write(rel,text):
 f=M/rel;f.parent.mkdir(parents=True,exist_ok=True);f.write_text(text)
parser='''import argparse
_parser=argparse.ArgumentParser()
_parser.add_argument('--output-dir',default='replay-results')
_parser.add_argument('--self-test-failure',action='store_true')
_args=_parser.parse_args()
ROOT=Path(_args.output_dir).resolve()
ROOT.mkdir(parents=True,exist_ok=True)
if _args.self_test_failure:
    raise RuntimeError('deliberate explicit-guard failure')
'''
src=(A/'math_algebra_family_01/exact_certificates.py').read_text()
src=src.replace('sys.path.insert(0,str(Path(__file__).resolve().parent/"runtime_packages"))\n','')
src=src.replace('ROOT=Path(__file__).resolve().parent',parser)
write('verification/exact_certificates.py',src)
class ExplicitChecks(ast.NodeTransformer):
 def visit_Assert(self,node):
  msg=ast.Constant('parity check failed at source-audit line '+str(node.lineno)+': '+ast.unparse(node.test))
  return ast.copy_location(ast.If(test=ast.UnaryOp(op=ast.Not(),operand=node.test),body=[ast.Raise(exc=ast.Call(func=ast.Name(id='RuntimeError',ctx=ast.Load()),args=[msg],keywords=[]),cause=None)],orelse=[]),node)
src=(A/'parity_extension_adversary_01/check.py').read_text();src=src.replace('sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "math_algebra_family_01/runtime_packages"))\n','')
src=ast.unparse(ast.fix_missing_locations(ExplicitChecks().visit(ast.parse(src))))+'\n'
src=src.replace('mp.mp.dps = 100','mp.mp.dps = 100\n'+parser)
src=src.replace("Path(__file__).with_name('CHECK_RESULTS.json')","ROOT / 'parity_controls_results.json'")
write('verification/parity_controls.py','"""Portable adaptation of the independently authored parity audit; explicit guards survive -O.\nNo novel independence claim is made for this package adaptation.\n"""\n'+src)
write('verification/requirements.txt','sympy==1.14.0\nmpmath==1.3.0\n')
for origin,target in [('math_algebra_family_01/exact_certificates.json','expected/exact_certificates.json'),('parity_extension_adversary_01/CHECK_RESULTS.json','expected/parity_controls_results.json')]:
 f=M/target;f.parent.mkdir(exist_ok=True);shutil.copyfile(A/origin,f)
files={
 'ROOT_EDITORIAL_PRIORITY_DECISION_01.md':'provenance/EDITORIAL_SCOPE.md',
 'priority_root_01/ROOT_OBSERVED_CHRONOLOGY_01.json':'provenance/OBSERVED_CHRONOLOGY.json',
 'original_submitted_head/PROOF.md':'history/ORIGINAL_POSITIVE_PROOF_20261001.md',
 'parity_extension_adversary_01/DERIVATION.md':'proofs/PARITY_DERIVATION_20261016.md',
 'priority_exact_history_01/REPORT.md':'priority/exact_history_report.md',
 'priority_exact_history_01/SOURCE_LEDGER.md':'priority/exact_history_sources.md',
 'priority_exact_history_01/QUERY_LOG.md':'priority/exact_history_queries.md',
 'priority_general_theorems_01/REPORT.md':'priority/general_theorems_report.md',
 'priority_general_theorems_01/SEARCH_LOG.md':'priority/general_theorems_searches.md',
 'priority_classical_elliptic_01/REPORT.md':'priority/classical_report.md',
 'priority_classical_elliptic_01/SOURCE_IMPLICATION_LEDGER.md':'priority/classical_sources.md',
 'priority_classical_elliptic_01/QUERY_LOG.md':'priority/classical_queries.md',
 'priority_classical_elliptic_01/TECHNICAL_ADDENDUM.md':'priority/classical_implications.md'}
origins={}
for source,target in files.items():
 f=M/target;f.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(A/source,f);b=f.read_bytes();origins[target]={'source_repository_path':'draft_pr_publication_program_20260930/audits/pr200_5100007/'+source,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'copy':'unaltered historical/audit text; relative local paths in it describe original audit environment, not portable replay commands'}
write('SOURCE_ORIGINS.json',json.dumps(origins,indent=2)+'\n')
print(json.dumps({'portable_verifiers':2,'selected_authored_evidence':len(files),'thirdparty_fulltexts_or_dependencies_copied':False}))
