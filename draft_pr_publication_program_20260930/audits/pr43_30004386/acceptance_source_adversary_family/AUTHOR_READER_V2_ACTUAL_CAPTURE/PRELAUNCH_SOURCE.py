"""Preserve failed own reader; qualify archived invalid drafting sources explicitly."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os
H=Path(__file__).resolve().parent
p=H/'inspect_all_inputs.py';raw=p.read_bytes();s=raw.decode()
old="raw=(S/z['path']).read_bytes();tree=ast.parse(raw,filename=z['path'])\n            ast_records.append({'path':z['path'],'bytes':len(raw),'sha256':sha(raw),'parse_only_no_code_object':True,'functions':[n.name for n in ast.walk(tree) if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))]})"
new="""raw=(S/z['path']).read_bytes()
            try:tree=ast.parse(raw,filename=z['path'])
            except SyntaxError as error:
                demand(z['path'].startswith('preserved_') and z['path'].endswith('/integrate_reviewed_partial.py'),'Only explicitly archived invalid drafting literals may fail AST parsing')
                ast_records.append({'path':z['path'],'bytes':len(raw),'sha256':sha(raw),'archived_invalid_drafting_literal':True,'syntax_error':str(error),'no_bytecode_or_execution':True})
            else:ast_records.append({'path':z['path'],'bytes':len(raw),'sha256':sha(raw),'parse_only_no_code_object':True,'functions':[n.name for n in ast.walk(tree) if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))]})"""
assert s.count(old)==1
s=s.replace(old,new).replace("n='git_'+str(len(git_records)+1)","n='v2_git_'+str(len(git_records)+1)")
target=H/'inspect_all_inputs_v2.py'
with target.open('x') as f:f.write(s)
record={'schema':'PR43_SOURCE_ADVERSARY_OWN_READER_REPAIR_v1','utc':dt.datetime.now(dt.timezone.utc).isoformat(),'actual_pid':os.getpid(),'failed_source_sha256':hashlib.sha256(raw).hexdigest(),'new_source_sha256':hashlib.sha256(s.encode()).hexdigest(),'old_source_preserved':p.read_bytes()==raw,'reason':'Own initial AST loop incorrectly required archived historically invalid drafting sources to parse. Their invalid newline literals were already disclosed in the frozen preparation; qualified separately, not production defects. Full failed actual capture remains.','proposed_sources_executed':False}
(H/'OWN_READER_REPAIR.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record,indent=2))
