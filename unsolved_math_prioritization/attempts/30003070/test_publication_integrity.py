#!/usr/bin/env python3
"""Relocated positive and negative controls; never modify the original publication."""
import hashlib,json,os,shutil,subprocess,sys,tempfile
from pathlib import Path
BASE=Path(__file__).resolve().parent
def require(ok,message):
    if not ok:raise RuntimeError(message)
def snapshot(p):
    return {x.relative_to(p).as_posix():hashlib.sha256(x.read_bytes()).hexdigest() for x in p.rglob('*') if x.is_file()}
def rebind(p):
    m=json.loads((p/'MANIFEST.json').read_text())
    for e in m['files']:
        b=(p/e['path']).read_bytes();e['bytes']=len(b);e['sha256']=hashlib.sha256(b).hexdigest()
    b=(json.dumps(m,indent=2)+'\n').encode();(p/'MANIFEST.json').write_bytes(b)
    (p/'MANIFEST.sha256').write_text(hashlib.sha256(b).hexdigest()+'  MANIFEST.json\n')
def main():
    modes=[('normal',[],{}),('optimized',['-O'],{}),('doubly_optimized',['-OO'],{}),('environment_optimized',[],{'PYTHONOPTIMIZE':'2'})]
    cases=['changed_author_proof','changed_audit','missing_scope','extra_file','extra_directory','symlink','manifest_binding','duplicate_manifest_path','unsafe_manifest_path','frozen_manifest_rebound','status_rebound','root_sequence_claim_rebound','wrong_turns_rebound']
    before=snapshot(BASE);out=[];controls=[]
    env={k:v for k,v in os.environ.items() if k!='PYTHONOPTIMIZE'}
    with tempfile.TemporaryDirectory(prefix='plabic-publication-controls-') as temp:
        temp=Path(temp);relocated=temp/'relocated';shutil.copytree(BASE,relocated);copied=snapshot(relocated)
        for mode,flags,extra in modes:
            cmd=[sys.executable,'-B',*flags,str(relocated/'verify_publication.py')]
            r=subprocess.run(cmd,cwd='/',capture_output=True,env={**env,**extra})
            require(r.returncode==0 and not r.stderr,'positive replay failed: '+mode+' '+r.stderr.decode())
            out.append(r.stdout)
            sentinel='import runpy; d=runpy.run_path('+repr(str(relocated/'verify_publication.py'))+'); d["require"](False,"runtime sentinel")'
            r=subprocess.run([sys.executable,'-B',*flags,'-c',sentinel],cwd='/',capture_output=True,env={**env,**extra})
            require(r.returncode!=0 and b'runtime sentinel' in r.stderr,'optimized false requirement accepted')
            for case in cases:
                p=temp/(mode+'-'+case);shutil.copytree(BASE,p)
                if case=='changed_author_proof':
                    f=p/'author/MATHEMATICS.md';f.write_bytes(f.read_bytes()+b'changed')
                elif case=='changed_audit':
                    f=p/'audit/AUDIT.md';f.write_bytes(f.read_bytes()+b'changed')
                elif case=='missing_scope':(p/'PUBLICATION_SCOPE.md').unlink()
                elif case=='extra_file':(p/'unexpected.txt').write_text('extra')
                elif case=='extra_directory':(p/'unexpected').mkdir()
                elif case=='symlink':
                    f=p/'author/README.md';f.unlink();f.symlink_to('MATHEMATICS.md')
                elif case=='manifest_binding':
                    f=p/'MANIFEST.json';f.write_bytes(f.read_bytes()+b' ')
                elif case in ('duplicate_manifest_path','unsafe_manifest_path'):
                    f=p/'MANIFEST.json';m=json.loads(f.read_text())
                    if case=='duplicate_manifest_path':m['files'].append(dict(m['files'][0]))
                    else:m['files'][0]['path']='../escape'
                    b=json.dumps(m).encode();f.write_bytes(b);(p/'MANIFEST.sha256').write_text(hashlib.sha256(b).hexdigest()+'  MANIFEST.json\n')
                elif case=='frozen_manifest_rebound':
                    f=p/'audit/MANIFEST.json';f.write_bytes(f.read_bytes()+b' ');rebind(p)
                else:
                    f=p/'release_status.json';s=json.loads(f.read_text())
                    if case=='status_rebound':s['status']='solved'
                    elif case=='root_sequence_claim_rebound':s['cube_embedding_constructs_root_sequence']=True
                    elif case=='wrong_turns_rebound':s['turns']='4/5'
                    f.write_text(json.dumps(s));rebind(p)
                r=subprocess.run([sys.executable,'-B',*flags,str(p/'verify_publication.py')],cwd='/',capture_output=True,env={**env,**extra})
                require(r.returncode!=0,'accepted negative control: '+mode+'/'+case)
                controls.append({'mode':mode,'case':case,'rejected':True})
        require(all(x==out[0] for x in out),'optimization changed output bytes')
        require(snapshot(relocated)==copied,'portable replay changed copied files')
    require(snapshot(BASE)==before,'controls changed original publication')
    print(json.dumps({'status':'PASS','portable_replay':json.loads(out[0]),'optimization_modes':[m[0] for m in modes],'false_runtime_requirements_rejected':4,'publication_corruptions_per_mode':len(cases),'publication_corruptions_total':len(controls),'negative_controls':controls,'unchanged_original_and_relocated_trees':True},indent=2,sort_keys=True))
if __name__=='__main__':main()
