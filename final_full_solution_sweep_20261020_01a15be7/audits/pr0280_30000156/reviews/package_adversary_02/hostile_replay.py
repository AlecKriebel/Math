#!/usr/bin/env python3
"""Independent current-archive replay and malformed-input rejection checks."""
from pathlib import Path
import copy, hashlib, json, os, shutil, subprocess, sys, tempfile, time

BASE=Path(__file__).resolve().parent
TREE=BASE/'archive/birational-cycle-verification'
SCRATCH=BASE.parents[3]/'private/pr0280_package2'
# BASE.parents[3] is the effort root, and this directory is ignored source custody.
RUNTIMES=[Path('/Users/alec/Documents/Math/.venv/bin/python3.9'),
 Path('/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'),
 Path(shutil.which('python3'))]

def execute(exe,tree,optimized=False,extra=()):
    cmd=[str(exe),'-B']+(['-O'] if optimized else [])+['verify.py']+list(extra)
    began=time.time()
    r=subprocess.run(cmd,cwd=tree,capture_output=True,text=True,timeout=45)
    return {'command':cmd,'returncode':r.returncode,'stdout':r.stdout,'stderr':r.stderr,
            'elapsed_seconds':time.time()-began}

def main():
    SCRATCH.mkdir(parents=True,exist_ok=True)
    results={'runtimes':[],'normal_replays':[],'mutants':[]}
    for exe in RUNTIMES:
        results['runtimes'].append({'requested':str(exe),'resolved':str(exe.resolve()),
            'version':subprocess.check_output([str(exe),'--version'],text=True).strip()})
        for opt in [False,True]:
            r=execute(exe,TREE,opt); results['normal_replays'].append(r)
            if r['returncode']!=0:raise RuntimeError(r)
    mutations=[]
    def manifest_mutation(label,fun):mutations.append((label,fun,True,()))
    def tree_mutation(label,fun):mutations.append((label,fun,False,()))
    for label,val in [('true',True),('false',False),('float_one',1.0),('string_one','1'),('null',None),('two',2),('zero',0),('list',[])]:
        manifest_mutation('schema_'+label,lambda m,v=val:m.__setitem__('schema',v))
    manifest_mutation('schema_missing',lambda m:m.pop('schema'))
    manifest_mutation('schema_extra_key',lambda m:m.__setitem__('unexpected',1))
    manifest_mutation('duplicate_payload_path',lambda m:m['files'].append(copy.deepcopy(m['files'][0])))
    for label,val in [('absolute','/tmp/x'),('traversal','../x'),('noncanonical','a/./b'),('backslash','a\\b'),('dot','.'),('manifest','MANIFEST.json'),('empty',''),('nonstring',42)]:
        manifest_mutation('path_'+label,lambda m,v=val:m['files'][0].__setitem__('path',v))
    for label,val in [('true',True),('float',406.0),('negative',-1),('string','406'),('null',None)]:
        manifest_mutation('bytes_'+label,lambda m,v=val:m['files'][0].__setitem__('bytes',v))
    manifest_mutation('sha_wrong',lambda m:m['files'][0].__setitem__('sha256','0'*64))
    manifest_mutation('sha_wrongtype',lambda m:m['files'][0].__setitem__('sha256',None))
    manifest_mutation('entry_extra',lambda m:m['files'][0].__setitem__('unexpected',1))
    manifest_mutation('entry_missing',lambda m:m['files'][0].pop('bytes'))
    manifest_mutation('files_missing_payload',lambda m:m['files'].pop())
    manifest_mutation('files_wrongtype',lambda m:m.__setitem__('files',{}))
    tree_mutation('payload_append',lambda t:(t/'README.md').write_bytes((t/'README.md').read_bytes()+b'x'))
    tree_mutation('payload_deleted',lambda t:(t/'README.md').unlink())
    tree_mutation('payload_extra',lambda t:(t/'unexpected.txt').write_text('unexpected'))
    tree_mutation('manifest_bad_json',lambda t:(t/'MANIFEST.json').write_text('{'))
    def symlink_payload(t):
        p=t/'README.md';p.unlink();p.symlink_to(TREE/'README.md')
    tree_mutation('payload_symlink',symlink_payload)
    def symlink_manifest(t):
        p=t/'MANIFEST.json';p.unlink();p.symlink_to(TREE/'MANIFEST.json')
    tree_mutation('manifest_symlink',symlink_manifest)
    tree_mutation('extra_dir_symlink',lambda t:(t/'extra').symlink_to(TREE,target_is_directory=True))
    tree_mutation('extra_fifo',lambda t:os.mkfifo(t/'unexpected_fifo'))
    def altered_baseline_rehashed(t):
        p=t/'expected_checks.json';x=json.loads(p.read_text());x['exact_checks']+=1;p.write_text(json.dumps(x))
        q=t/'MANIFEST.json';m=json.loads(q.read_text());entry=next(v for v in m['files'] if v['path']=='expected_checks.json');entry['bytes']=p.stat().st_size;entry['sha256']=hashlib.sha256(p.read_bytes()).hexdigest();q.write_text(json.dumps(m))
    tree_mutation('rehash_bad_expected_result',altered_baseline_rehashed)
    mutations.append(('command_line_override',lambda t:None,False,('--skip',)))
    for label,mutate,is_manifest,extra in mutations:
        # Fresh independent extraction copy for every mutation and mode.
        for opt in [False,True]:
            with tempfile.TemporaryDirectory(prefix='hostile_',dir=SCRATCH) as d:
                tree=Path(d)/'tree';shutil.copytree(TREE,tree)
                if is_manifest:
                    p=tree/'MANIFEST.json';m=json.loads(p.read_text());mutate(m);p.write_text(json.dumps(m))
                else:mutate(tree)
                r=execute(RUNTIMES[0],tree,opt,extra)
                results['mutants'].append({'mutation':label,'optimized':opt,**r})
                if r['returncode']==0:raise RuntimeError('False acceptance '+label)
    results['summary']={'status':'PASS','normal_passes':len(results['normal_replays']),
        'distinct_negative_cases':len(mutations),'negative_rejections':len(results['mutants']),
        'scope':'Integrity assumes the externally bound ZIP hash; finite replay is not an infinite-prime proof.'}
    return results

if __name__=='__main__':print(json.dumps(main(),indent=2,sort_keys=True))
