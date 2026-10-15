"""Pure exact V4 GH parser fragment. Synthetic text only; no private file read."""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import ast,datetime,hashlib,importlib.util,json,os,re
D=Path(__file__).resolve().parent;S=D.parent/'native_publication_integration_plan_20261006/corrected_v4'
spec=importlib.util.spec_from_file_location('guards',S/'v3_guards.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
tree=ast.parse((S/'v3_guards.py').read_text());function=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='verify_private_runtime_configuration')
branch=next(n for n in ast.walk(function) if isinstance(n,ast.If) and ast.unparse(n.test)=="path.name == 'config.yml'")
fragment=ast.Module(body=branch.body,type_ignores=[]);code=compile(fragment,str(S/'v3_guards.py'),'exec')
cases=[('empty_LF_followed_by_regular_field',b'http_unix_socket:\neditor: synthetic-value\n',False),('empty_space_LF_followed_by_regular_field',b'http_unix_socket: \neditor: synthetic-value\n',False),('empty_tab_CRLF_followed_by_regular_field',b'http_unix_socket:\t\r\neditor: synthetic-value\r\n',False),('empty_terminal_field',b'http_unix_socket:\n',True),('ordinary_no_socket_no_alias',b'editor: synthetic-value\n',True),('active_socket_inline',b'http_unix_socket: /tmp/synthetic-only.sock\n',False),('active_external_alias',b"aliases:\n  synthetic: '!echo synthetic-only'\n",False)]
results=[]
for name,text,expected_accept in cases:
    try:exec(code,{'data':text,'require':g.require,'re':re});accepted=True;error=None
    except ValueError as e:accepted=False;error=str(e)
    if accepted!=expected_accept:raise RuntimeError('Unexpected parser challenge result: '+name)
    results.append({'name':name,'accepted':accepted,'expected_source_behavior':expected_accept,'legitimate_empty_field_false_positive':name.startswith('empty_') and not name.startswith('empty_terminal'),'error':error,'synthetic_text_sha256':hashlib.sha256(text).hexdigest()})
socket_pattern=next(n.args[0].value for n in ast.walk(branch) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=='search' and isinstance(n.args[0],ast.Constant) and 'http_unix_socket' in n.args[0].value)
match=re.search(socket_pattern,cases[0][1].decode())
if match is None or '\n' not in match.group():raise RuntimeError('False positive did not cross newline')
result={'schema':'pr108-frozen-V4-F10-independent-source-counterexample/v1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'PID':os.getpid(),'optimized':not __debug__,'reproduced':True,'exact_source_branch_start_line':branch.lineno,'socket_pattern':socket_pattern,'fragment_AST_sha256':hashlib.sha256(ast.dump(fragment,include_attributes=False).encode()).hexdigest(),'false_positive_match_lines':len(match.group().splitlines()),'cases':results,'private_configuration_body_reads':0,'actual_config_gate_files_created':0,'native_resource_services_or_Git_calls':0}
(D/('F10_OPTIMIZED_COUNTEREXAMPLE.json' if not __debug__ else 'F10_NORMAL_COUNTEREXAMPLE.json')).write_bytes(g.canonical(result))
print(json.dumps({k:v for k,v in result.items() if k!='cases'},sort_keys=True))
