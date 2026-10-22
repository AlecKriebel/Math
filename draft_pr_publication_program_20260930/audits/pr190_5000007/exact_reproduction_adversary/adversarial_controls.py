"""Private-copy mutations. Never changes submission; saves argv/time/streams/hashes."""
from pathlib import Path
from datetime import datetime, UTC
import hashlib,json,subprocess,sys
HERE=Path(__file__).resolve().parent
ORIG=HERE.parent/'original_submission/files/unsolved_math_prioritization/attempts/5000007'
PYTHON='/opt/homebrew/opt/python@3.14/bin/python3.14'
PRIV=HERE/'private/mutations';PRIV.mkdir(parents=True,exist_ok=True)
OUT=HERE/'private/control_runs';OUT.mkdir(exist_ok=True)
sha=lambda b:hashlib.sha256(b).hexdigest()
cert=(ORIG/'check_certificate.py').read_text()
half=(ORIG/'check_half_turn.py').read_text()
tests=(ORIG/'test_reconstruction.py').read_text()
variants=[
 ('certificate_false_guard','check_certificate.py',cert.replace('def check():','def check():\n    assert False, "deliberate false audit guard"')),
 ('certificate_wrong_squared_length','check_certificate.py',cert.replace('K(F(307,2),F(137,2))','K(F(309,2),F(137,2))')),
 ('certificate_wrong_geometry','check_certificate.py',cert.replace('C=K(F(-1,2),F(1,2))','C=K(F(-1,2),F(1,3))')),
 ('certificate_wrong_source_ray','check_certificate.py',cert.replace('physical_ray=polys[-1][10]-end','physical_ray=polys[-1][10]-end\n    source_ray=physical_ray')),
 ('half_turn_false_guard','check_half_turn.py',half.replace('phi=K(1,1)/2','assert False, "deliberate false audit guard"\nphi=K(1,1)/2')),
 ('half_turn_empty_edge_geometry','check_half_turn.py',half.replace('edge_squared=4*ip*ip','edge_squared=K()')),
 ('unittest_false_test','test_reconstruction.py',tests.replace('class Arithmetic(unittest.TestCase):','class Arithmetic(unittest.TestCase):\n    def test_deliberate_false(self): self.assertTrue(False)')),
]
records=[]
for name,filename,body in variants:
    d=PRIV/name;d.mkdir(exist_ok=True)
    for fn,txt in [('check_certificate.py',cert),('check_half_turn.py',half),('test_reconstruction.py',tests)]:
        (d/fn).write_text(body if fn==filename else txt)
    for optimized in [False,True]:
        mode='optimized' if optimized else 'normal';label=name+'_'+mode
        launcher='import sys,runpy;sys.path.insert(0,'+repr(str(d))+');runpy.run_path('+repr(str(d/filename))+',run_name="__main__")'
        argv=[PYTHON,'-E','-S','-B','-P']+(['-O'] if optimized else [])+['-c',launcher]
        start=datetime.now(UTC).isoformat();r=subprocess.run(argv,capture_output=True);end=datetime.now(UTC).isoformat()
        record={'label':label,'argv':argv,'start_utc':start,'end_utc':end,'returncode':r.returncode,'source_sha256':sha(body.encode()),'sources':{fn:sha((d/fn).read_bytes()) for fn in ['check_certificate.py','check_half_turn.py','test_reconstruction.py']},'stdout_sha256':sha(r.stdout),'stderr_sha256':sha(r.stderr),'stdout_bytes':len(r.stdout),'stderr_bytes':len(r.stderr)}
        for stream,data in [('stdout',r.stdout),('stderr',r.stderr)]: (OUT/(label+'.'+stream)).write_bytes(data)
        (OUT/(label+'.json')).write_text(json.dumps(record,indent=2)+'\n')
        summary={'label':label,'returncode':r.returncode,'stdout_sha256':sha(r.stdout),'stderr_tail':r.stderr.decode(errors='replace').splitlines()[-1:]}
        try:
            o=json.loads(r.stdout);summary['output_length']=o.get('squared_length');summary['output_edge_count']=o.get('edge_count');summary['output_source_difference']=o.get('fuchs_beta_minus_alpha')
        except Exception:pass
        records.append(summary)
# Audit-owned guard controls: unlike Python assert, require must survive -O.
owned=(HERE/'independent_exact.py').read_text()
for name,body in [('owned_false_guard',owned.replace("if __name__=='__main__':","if __name__=='__main__':\n    require(False,'deliberate audit-owned false guard')")),('owned_wrong_length',owned.replace('(307+137*SQRT5)/2','(309+137*SQRT5)/2'))]:
    p=PRIV/(name+'.py');p.write_text(body)
    for optimized in [False,True]:
        mode='optimized' if optimized else 'normal';label=name+'_'+mode
        argv=[PYTHON,'-E','-S','-B','-P']+(['-O'] if optimized else [])+[str(p)]
        start=datetime.now(UTC).isoformat();r=subprocess.run(argv,capture_output=True);end=datetime.now(UTC).isoformat()
        record={'label':label,'argv':argv,'start_utc':start,'end_utc':end,'returncode':r.returncode,'source_sha256':sha(p.read_bytes()),'stdout_sha256':sha(r.stdout),'stderr_sha256':sha(r.stderr)}
        for stream,data in [('stdout',r.stdout),('stderr',r.stderr)]: (OUT/(label+'.'+stream)).write_bytes(data)
        (OUT/(label+'.json')).write_text(json.dumps(record,indent=2)+'\n')
        records.append({'label':label,'returncode':r.returncode,'stderr_tail':r.stderr.decode(errors='replace').splitlines()[-1:]})
(HERE/'CONTROL_SUMMARY.json').write_text(json.dumps(records,indent=2)+'\n')
print(json.dumps(records,indent=2))
