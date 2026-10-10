#!/usr/bin/env python3
"""Real subprocess negative controls using an external trusted bootstrap copy.
This tests the verifier, not the underlying universal mathematical proofs.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

def need(ok,message):
    if not ok: raise RuntimeError(message)
def sha(raw): return hashlib.sha256(raw).hexdigest()
def dump(path,obj): path.write_text(json.dumps(obj,indent=2)+'\n')
def rebind(root):
    path=root/'PUBLICATION_MANIFEST.json';m=json.loads(path.read_text())
    for row in m['files']:
        f=root/row['path']
        if f.is_file(): row.update(bytes=f.stat().st_size,sha256=sha(f.read_bytes()))
    dump(path,m); return sha(path.read_bytes())
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--packet',type=Path,required=True);p.add_argument('--expected-manifest',required=True);a=p.parse_args();source=a.packet.absolute()
    cases=['changed proof old pin','changed proof rebound outer','missing file','extra file','extra directory','malformed manifest','duplicate manifest key','boolean problem id','float rank','solved status','false source scope','wrong frozen anchor','duplicate inventory path','traversal path','absolute path','boolean byte count','float byte count','malformed digest','wrong mode','symlink member','symlink directory','symlink manifest','symlink root','symlink wrapper','changed wrapper','changed wrapper rebound outer','changed bootstrap','changed bootstrap rebound outer','changed hardening patch rebound outer','changed hardened manifest rebound outer','duplicate inner JSON rebound outer','nonfinite JSON rebound outer','duplicate outer JSON rebound outer']
    results=[]
    with tempfile.TemporaryDirectory(prefix='lattice-external-bootstrap-controls-') as td:
        t=Path(td);cwd=t/'unrelated';cwd.mkdir();launcher=t/'TRUSTED_BOOTSTRAP.py';shutil.copyfile(source/'BOOTSTRAP.py',launcher)
        original_launcher_sha=sha(launcher.read_bytes())
        for label,flags in [('normal',[]),('O',['-O']),('OO',['-OO'])]:
            env={k:v for k,v in os.environ.items() if not k.startswith('PYTHON')};env['PYTHONDONTWRITEBYTECODE']='1'
            def invoke(root,pin):
                need(sha(launcher.read_bytes())==original_launcher_sha,'Trusted launcher changed')
                return subprocess.run([sys.executable,'-I','-B',*flags,str(launcher),'--packet',str(root),'--expected-manifest',pin,'--check-only'],cwd=cwd,env=env,capture_output=True,timeout=60)
            cp=invoke(source,a.expected_manifest);need(cp.returncode==0,'Positive bootstrap failed: '+cp.stderr.decode())
            results.append({'mode':label,'case':'baseline external bootstrap','outcome':'PASS'})
            for index,name in enumerate(cases):
                root=t/(label+'-'+str(index));shutil.copytree(source,root);pin=a.expected_manifest;mf=root/'PUBLICATION_MANIFEST.json';m=json.loads(mf.read_text())
                if name.startswith('changed proof'):
                    (root/'original/REPORT.md').write_text('Corrupted proof\n')
                    if name.endswith('outer'):pin=rebind(root)
                elif name=='missing file':(root/'original/REPORT.md').unlink()
                elif name=='extra file':(root/'unexpected.json').write_text('{}\n')
                elif name=='extra directory':(root/'unexpected').mkdir()
                elif name=='malformed manifest':mf.write_text('{');pin=sha(mf.read_bytes())
                elif name=='duplicate manifest key':mf.write_text(mf.read_text().replace('"rank": 996,','"rank": 0, "rank": 996,',1));pin=sha(mf.read_bytes())
                elif name in ['boolean problem id','float rank','solved status','false source scope','wrong frozen anchor']:
                    if name=='boolean problem id':m['problem_id']=True
                    elif name=='float rank':m['rank']=996.0
                    elif name=='solved status':m['status']='claimed_solved'
                    elif name=='false source scope':m['source_files_redistributed']=True
                    else:m['frozen_manifest_anchors']['original']='0'*64
                    dump(mf,m);pin=sha(mf.read_bytes())
                elif name in ['duplicate inventory path','traversal path','absolute path','boolean byte count','float byte count','malformed digest','wrong mode']:
                    if name=='duplicate inventory path':m['files'].append(dict(m['files'][0]))
                    elif name=='traversal path':m['files'][0]['path']='../outside.json'
                    elif name=='absolute path':m['files'][0]['path']='/outside.json'
                    elif name=='boolean byte count':m['files'][0]['bytes']=True
                    elif name=='float byte count':m['files'][0]['bytes']=float(m['files'][0]['bytes'])
                    elif name=='malformed digest':m['files'][0]['sha256']='z'*64
                    else:m['files'][0]['mode']='0755'
                    dump(mf,m);pin=sha(mf.read_bytes())
                elif name in ['symlink member','symlink manifest','symlink wrapper']:
                    rel={'symlink member':'original/REPORT.md','symlink manifest':'PUBLICATION_MANIFEST.json','symlink wrapper':'VERIFY_PUBLICATION.py'}[name]
                    f=root/rel;outside=t/(label+'-outside-'+str(index));shutil.copyfile(f,outside);f.unlink();f.symlink_to(outside)
                elif name=='symlink directory':
                    f=root/'original';outside=t/(label+'-outside-dir');f.rename(outside);f.symlink_to(outside,target_is_directory=True)
                elif name=='symlink root':
                    alias=t/(label+'-root-alias');alias.symlink_to(root,target_is_directory=True);root=alias
                elif name.startswith('changed wrapper'):
                    (root/'VERIFY_PUBLICATION.py').write_text('raise SystemExit(0)\n')
                    if name.endswith('outer'):pin=rebind(root)
                elif name.startswith('changed bootstrap'):
                    (root/'BOOTSTRAP.py').write_text('raise SystemExit(0)\n')
                    if name.endswith('outer'):pin=rebind(root)
                elif name=='changed hardening patch rebound outer':
                    f=root/'independent_audit/VALIDATION_HARDENING.patch';f.write_bytes(f.read_bytes()+b'\n');pin=rebind(root)
                elif name=='changed hardened manifest rebound outer':
                    f=root/'hardened/MANIFEST.json';v=json.loads(f.read_text());v['schema']=True;dump(f,v);pin=rebind(root)
                elif name=='duplicate inner JSON rebound outer':
                    f=root/'hardened/CLAIMS.json';f.write_text(f.read_text().replace('"route_count": 5,','"route_count": 0, "route_count": 5,',1));pin=rebind(root)
                elif name=='nonfinite JSON rebound outer':
                    f=root/'MUTATION_RESULTS.json';f.write_text('{"not_finite": NaN}\n');pin=rebind(root)
                elif name=='duplicate outer JSON rebound outer':
                    f=root/'MUTATION_RESULTS.json';f.write_text('{"key": 0, "key": 1}\n');pin=rebind(root)
                cp=invoke(root,pin)
                need(cp.returncode!=0,'Mutation accepted: '+label+' '+name)
                results.append({'mode':label,'case':name,'outcome':'REJECT'})
    result={'status':'PASS','external_bootstrap':True,'modes':['normal','O','OO'],'positive_bootstrap_runs':3,'hostile_rejections':3*len(cases),'external_trust_boundary_controls':0,'results':results,'limits':'Recomputed outer pins test structure and frozen anchors. Arbitrarily authorized replacement metadata is not a falsified proof. No general proof verifier or trust without externally authenticated code is claimed.'}
    print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':main()
