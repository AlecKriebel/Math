"""Run only extracted ck definitions on deliberately false controls."""
from pathlib import Path
from collections import Counter
import ast,json,os,sys
A=Path(__file__).resolve().parent
O=A/'original_head_authentication_20261006/original_attempt'
D=A/'repaired_diagnostics_v1'
results=[]
for label,path,kind in [('original_author',O/'verify.py','author'),
    ('original_independent',O/'review/independent_checks.py','independent'),
    ('effective_author',D/'verify.py','author'),('effective_independent',D/'independent_checks.py','independent')]:
    functions=[node for node in ast.parse(path.read_text()).body if isinstance(node,ast.FunctionDef) and node.name=='ck']
    if len(functions)!=1:raise ValueError('Unique ck definition')
    namespace={'count':0,'C':Counter()}
    exec(compile(ast.Module(body=functions,type_ignores=[]),str(path)+':guard-only','exec'),namespace)
    try:
        namespace['ck'](False) if kind=='author' else namespace['ck']('deliberately_false',False)
    except (AssertionError,ValueError) as error:
        raised=type(error).__name__
    else:raised=None
    expected='ValueError' if label.startswith('effective') else ('AssertionError' if __debug__ else None)
    if raised!=expected:raise ValueError('False guard control unexpected: '+label)
    results.append({'label':label,'false_control_exception':raised,'expected':expected,'false_claim_accepted':raised is None})
print(json.dumps({'actual_PID':os.getpid(),'optimized':not __debug__,'status':'PASS','results':results,
    'original_optimized_guards_cleared':False,'effective_guards_reject_false_claims':True},indent=2,sort_keys=True))
