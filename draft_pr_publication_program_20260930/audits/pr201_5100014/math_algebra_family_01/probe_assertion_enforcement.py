"""Intentionally false checks; all verdicts verified by explicit exceptions."""
import ast,sys,json
from pathlib import Path
from collections import Counter
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]/'pr200_5100007'/'math_algebra_family_01'/'runtime_packages'))
import mpmath as mp
src=HERE.parent/'original_submitted_head/independent_review/independent_check.py'
tree=ast.parse(src.read_text())
selected=ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ('ck','close')],type_ignores=[])
ns={'C':Counter(),'D':Counter(),'maxerr':mp.mpf(0),'mp':mp}
exec(compile(selected,str(src),'exec'),ns)
results={}
for name,call in [('original_exact_false',lambda:ns['ck']('deliberately false',False)),('original_numeric_false',lambda:ns['close']('deliberately false',mp.mpf(0),mp.mpf(1)))]:
    try:call()
    except AssertionError:results[name]='rejected'
    else:results[name]='accepted'
def need(c,m):
    if not c:raise RuntimeError(m)
try:need(False,'deliberate new-check failure')
except RuntimeError:results['new_explicit_false']='rejected'
else:raise RuntimeError('explicit exception disabled')
want='accepted' if sys.flags.optimize else 'rejected'
need(results['original_exact_false']==want and results['original_numeric_false']==want,'original assertion behavior unexpected')
print(json.dumps({'optimization':sys.flags.optimize,'probe_outcomes':results,'status':'PASS','interpretation':'PASS means expected enforcement behavior was observed, never that the deliberately false mathematical checks passed.'},indent=2))
