#!/usr/bin/env python3
from pathlib import Path
import subprocess,tempfile,json,hashlib,datetime
here=Path(__file__).resolve().parent
source=(here/'boundary_controls.py').read_text()
changes=[
('hw_wrong_orders','[[0,4,0],[4,0,0],[1,1,1]]','[[0,2,0],[2,0,0],[1,1,1]]'),
('twist_wrong_epimorphism','character=s.Matrix([1,k,0,0])','character=s.Matrix([1,0,0,0])'),
('seifert_bad_antisymmetric_entry','[[a,b],[b-1,d]]','[[a,b],[b-2,d]]'),
('wrong_branched_cover_matrix','P=V+V.T','P=V-V.T')]
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'mutants':[]}
with tempfile.TemporaryDirectory(prefix='boundary_mutants_',dir=here/'private_replay') as tmp:
    for name,old,new in changes:
        assert source.count(old)==1
        folder=Path(tmp)/name;folder.mkdir();p=folder/'boundary_controls.py';p.write_text(source.replace(old,new))
        r=subprocess.run(['/usr/bin/python3',str(p)],cwd=folder,text=True,capture_output=True)
        assert r.returncode!=0 and 'AssertionError:' in r.stderr,(name,r.stdout,r.stderr)
        out['mutants'].append({'name':name,'program_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr,'rejected':True})
out['rejected']=len(out['mutants']);out['scope']='Actual rejected algebraic presentation mutants; not a test of all knots or geometric lifting/existence.'
(here/'BOUNDARY_MUTATION_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'rejected':out['rejected']}))
