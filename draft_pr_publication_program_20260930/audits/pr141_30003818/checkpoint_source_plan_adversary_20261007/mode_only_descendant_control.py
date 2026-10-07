"""Evaluate only the isolated side-effect-free final readback predicate."""
from pathlib import Path
import ast, datetime, hashlib, json, os
A=Path('/Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr85_30001203/isolated_main_integration_20261005/checkout/draft_pr_publication_program_20260930/audits/pr141_30003818')
S=A/'checkpoint_preparation_20261007/scoped_audit_checkpoint_publish.py'
O=A/'checkpoint_source_plan_adversary_20261007'
source=S.read_bytes()
if hashlib.sha256(source).hexdigest()!='19ef8deeb6503256646af94edc69ad14d0715066e9008e68645b960f413ee431':raise RuntimeError('source changed')
tree=ast.parse(source)
publish=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='publish')
calls=[n for n in ast.walk(publish) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='require' and len(n.args)==2 and isinstance(n.args[1],ast.Constant) and n.args[1].value=='published full body changed']
if len(calls)!=1:raise RuntimeError('unique final body predicate')
expr=calls[0].args[0]
if {n.id for n in ast.walk(expr) if isinstance(n,ast.Name)}!={'len','z','m','digest'}:raise RuntimeError('unexpected expression')
code=compile(ast.Expression(expr),'<isolated pure readback predicate>','eval')
body=b'unchanged audited body\n'
member={'post':{'bytes':len(body),'mode':420,'sha256':hashlib.sha256(body).hexdigest()}}
def accepted(value):return eval(code,{'__builtins__':{},'len':len,'digest':lambda b:hashlib.sha256(b).hexdigest(),'z':value,'m':member})
cases=[]
for remote_mode in ['100644','100755','120000']:
    observed={'mode':remote_mode,'kind':'blob','body':body}
    got=accepted(observed['body'])
    if not got:raise RuntimeError('expected body predicate accepts identical body')
    cases.append({'observed_mode':remote_mode,'same_body':True,'actual_final_source_predicate_accepts':got,'required_mode_matches':remote_mode=='100644'})
if accepted(body+b'x') or accepted(b'changed audited body!!\n'):raise RuntimeError('negative body control did not reject')
out={'schema':'pr141-isolated-readback-mode-counterexample/v1','actual_reviewer_PID':os.getpid(),'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_sha256':hashlib.sha256(source).hexdigest(),'source_line':calls[0].lineno,'isolated_expression':ast.unparse(expr),'identical_body_modes':cases,'two_changed_body_negative_controls_reject':True,'mode_only_descendant_false_accept_demonstrated':True,'operator_module_imported':False,'candidate_publish_main_or_any_writer_called':False,'Git_repository_or_remote_action':False,'scope':'Only the side-effect-free Boolean expression is compiled and evaluated; no operator function runs.'}
(O/'MODE_ONLY_DESCENDANT_CONTROL.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps({'actual_PID':os.getpid(),'mode_only_false_accept':True,'writer_called':False}))
