#!/usr/bin/env python3
"""Replay public-only geometry and exact semantic controls; no original-inventory claim."""
import argparse,ast,copy,hashlib,json,os,shutil,subprocess,sys,tempfile
from pathlib import Path

class AuditFailure(Exception): pass

def need(x,msg):
    if not x: raise AuditFailure(msg)

def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def inventory(root): return {p.name:{'bytes':p.stat().st_size,'sha256':digest(p),'mode':oct(p.stat().st_mode & 0o777)} for p in sorted(root.iterdir()) if p.is_file()}
def run(args,cwd):
    p=subprocess.run(args,cwd=cwd,text=True,capture_output=True)
    try: obj=json.loads(p.stdout)
    except json.JSONDecodeError: obj=None
    return {'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'result':obj}
def expect(r,status,code,error=None):
    need(r['exit_code']==code and r['stderr']=='','unexpected process result')
    need(isinstance(r['result'],dict) and r['result'].get('status')==status,'missing structured expected status')
    if error is not None: need(r['result'].get('error')==error,'wrong failure reason: '+str(r['result']))

def main():
    ap=argparse.ArgumentParser();ap.add_argument('public_author',type=Path);ap.add_argument('output',type=Path);a=ap.parse_args()
    root=a.public_author.resolve();before=inventory(root)
    need(os.getuid()==1000 and os.geteuid()==1000,'audit requires actual UID 1000')
    need(digest(root/'PUBLIC_MANIFEST.json')=='4e3fb58491159e8892d218a8aeec1dc95174bf8b7243472d51c96c8fea64d4a8','wrong public-author manifest pin')
    need(root.stat().st_mode & 0o222 == 0,'public-author directory has writable mode')
    ast_report={}
    for name in ('check_geometry.py',):
        tree=ast.parse((root/name).read_text());n=sum(isinstance(x,ast.Assert) for x in ast.walk(tree))
        need(n==0,'assert statement in native checker');ast_report[name]={'assert_nodes':n}
    receipt={'schema':'public-geometry-replay-v1','status':'RUNNING','scope':'public derivative only; not original private-packet integrity','uid':os.getuid(),'euid':os.geteuid(),'public_author_manifest_sha256':digest(root/'PUBLIC_MANIFEST.json'),'public_inventory_before':before,'ast_review':ast_report,'runs':[]}
    with tempfile.TemporaryDirectory(prefix='hexagon-audit-') as td:
        work=Path(td)
        for mode,flags in [('normal',[]),('O',['-O']),('OO',['-OO'])]:
            base=[sys.executable,'-I','-S','-B']+flags
            geometry=run(base+[str(root/'check_geometry.py'),'--readonly'],work);expect(geometry,'PASS',0)
            need(geometry['result']['uid']==1000 and geometry['result']['euid']==1000,'wrong runtime uid')
            need(len(geometry['result']['write_probes'])==2 and all(p['result']=='PermissionError' for p in geometry['result']['write_probes']),'write denial not established')
            independent=run(base+[str(Path(__file__).resolve().parent/'independent_geometry.py'),str(root)],work);expect(independent,'PASS',0)
            row={'mode':mode,'native_geometry':geometry,'independent_geometry':independent,'semantic_controls':[]}
            def geometry_control(name,script=None,fixtures=None,missing=False,expected=''):
                d=work/(mode+'_'+name);d.mkdir()
                (d/'check_geometry.py').write_text(script if script is not None else (root/'check_geometry.py').read_text())
                if not missing:(d/'fixtures.json').write_text(json.dumps(fixtures) if fixtures is not None else (root/'fixtures.json').read_text())
                args=base+[str(d/'check_geometry.py')]
                if missing:args+=['--fixtures','MISSING_FIXTURE.json']
                r=run(args,d);expect(r,'FAIL',2,expected)
                row['semantic_controls'].append({'case':name,'expected_error':expected,**r})
            orig=json.loads((root/'fixtures.json').read_text());src=(root/'check_geometry.py').read_text()
            geometry_control('missing_fixture',missing=True,expected='required fixture input missing: MISSING_FIXTURE.json')
            bad=copy.deepcopy(orig);bad['schema']=99
            geometry_control('invalid_schema',fixtures=bad,expected='unexpected fixture schema')
            bad=copy.deepcopy(orig);bad['point_sets']['boundary_blocker']=[[2,1]]
            geometry_control('boundary_blocker_moved_into_interior',fixtures=bad,expected='boundary fixture has an interior blocker')
            bad=copy.deepcopy(orig);bad['point_sets']['degenerate_six'][1]=[2,-1]
            geometry_control('weak_fixture_gains_corner',fixtures=bad,expected='weak-six fixture wrong')
            bad=copy.deepcopy(orig);bad['point_sets']['sparse_triples'][0][0]+=1
            geometry_control('destroy_one_intended_collinear_triple',fixtures=bad,expected='unexpected collinearity among sparse triples')
            old='return all(p in S or not in_closed_hull(p, poly) for p in P)';new='return all(p in S or not in_interior(p, poly) for p in P)'
            need(src.count(old)==1,'edge mutant anchor mismatch')
            geometry_control('ignore_closed_edge_blockers',script=src.replace(old,new),expected='closed edge blocker was ignored')
            old='q = min(candidates, key=lambda q:';need(src.count(old)==1,'ear mutant anchor mismatch')
            geometry_control('select_farthest_ear',script=src.replace(old,'q = max(candidates, key=lambda q:'),expected='nearest-ear conclusion failed')
            old='31*len(D)+30';need(src.count(old)==1,'threshold mutant anchor mismatch')
            geometry_control('wrong_slab_threshold',script=src.replace(old,'30*len(D)+30'),expected='slab threshold fixture wrong')
            receipt['runs'].append(row)
        after=inventory(root);need(before==after,'public files changed during replay')
        receipt['public_inventory_after']=after;receipt['public_author_unchanged']=True;receipt['status']='PASS'
        receipt['summary']={'native_geometry_passes':3,'independent_geometry_passes':3,'denied_write_probes':6,'semantic_control_rejections':24,'arbitrary_crashes_accepted':0}
        a.output.write_text(json.dumps(receipt,sort_keys=True,indent=2)+'\n')
        print(json.dumps(receipt['summary'],sort_keys=True))

if __name__=='__main__':
    try:main()
    except (AuditFailure,OSError,ValueError,TypeError,KeyError) as e:
        print(json.dumps({'status':'FAIL','error':str(e)},sort_keys=True));sys.exit(2)
