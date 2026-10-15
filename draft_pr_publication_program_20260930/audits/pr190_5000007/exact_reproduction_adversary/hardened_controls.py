"""Audit-owned AST guard repair on private copies; not a change to submissions."""
from pathlib import Path
from datetime import datetime,UTC
import ast,hashlib,json,subprocess
HERE=Path(__file__).resolve().parent
ORIG=HERE.parent/'original_submission/files/unsolved_math_prioritization/attempts/5000007'
OUT=HERE/'private/hardened_runs';OUT.mkdir(exist_ok=True)
DEST=HERE/'private/hardened';DEST.mkdir(exist_ok=True)
PYTHON='/opt/homebrew/opt/python@3.14/bin/python3.14'
sha=lambda x:hashlib.sha256(x).hexdigest()
class Harden(ast.NodeTransformer):
    def visit_Assert(self,node):
        msg=node.msg or ast.Constant(value='audit-hardened validation guard failed')
        return ast.copy_location(ast.If(test=ast.UnaryOp(op=ast.Not(),operand=node.test),body=[ast.Raise(exc=ast.Call(func=ast.Name(id='AssertionError',ctx=ast.Load()),args=[msg],keywords=[]),cause=None)],orelse=[]),node)
def repair(text): return ast.unparse(ast.fix_missing_locations(Harden().visit(ast.parse(text))))+'\n'
cert=(ORIG/'check_certificate.py').read_text();half=(ORIG/'check_half_turn.py').read_text()
variants=[('baseline_certificate','check_certificate.py',cert),('baseline_half_turn','check_half_turn.py',half),('false_guard','check_certificate.py',cert.replace('def check():','def check():\n    assert False, "deliberate false audit guard"')),('wrong_squared_length','check_certificate.py',cert.replace('K(F(307,2),F(137,2))','K(F(309,2),F(137,2))')),('wrong_geometry','check_certificate.py',cert.replace('C=K(F(-1,2),F(1,2))','C=K(F(-1,2),F(1,3))')),('wrong_source_ray','check_certificate.py',cert.replace('physical_ray=polys[-1][10]-end','physical_ray=polys[-1][10]-end\n    source_ray=physical_ray')),('empty_edge_geometry','check_half_turn.py',half.replace('edge_squared=4*ip*ip','edge_squared=K()'))]
results=[]
for name,fn,text in variants:
    d=DEST/name;d.mkdir(exist_ok=True)
    sources={}
    for filename,original in [('check_certificate.py',cert),('check_half_turn.py',half)]:
        before=text if filename==fn else original;after=repair(before);(d/filename).write_text(after)
        sources[filename]={'input_sha256':sha(before.encode()),'hardened_sha256':sha(after.encode())}
    for optimize in [False,True]:
        label=name+('_optimized' if optimize else '_normal')
        code='import sys,runpy;sys.path.insert(0,'+repr(str(d))+');runpy.run_path('+repr(str(d/fn))+',run_name="__main__")'
        argv=[PYTHON,'-E','-S','-B','-P']+(['-O'] if optimize else [])+['-c',code]
        start=datetime.now(UTC).isoformat();r=subprocess.run(argv,capture_output=True);end=datetime.now(UTC).isoformat()
        record={'label':label,'argv':argv,'start_utc':start,'end_utc':end,'sources':sources,'returncode':r.returncode,'stdout_sha256':sha(r.stdout),'stderr_sha256':sha(r.stderr)}
        for stream,data in [('stdout',r.stdout),('stderr',r.stderr)]: (OUT/(label+'.'+stream)).write_bytes(data)
        (OUT/(label+'.json')).write_text(json.dumps(record,indent=2)+'\n')
        results.append({'label':label,'returncode':r.returncode,'stdout_sha256':sha(r.stdout),'stderr_tail':r.stderr.decode(errors='replace').splitlines()[-1:]})
(HERE/'HARDENED_CONTROL_SUMMARY.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
