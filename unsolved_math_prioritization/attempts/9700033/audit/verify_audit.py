#!/usr/bin/env python3
"""Verify the audit against a separately held external manifest hash. Not a proof assistant."""
import hashlib,json,pathlib,stat,subprocess,sys

def require(condition,message):
    if not condition:raise ValueError(message)
def digest(raw):return hashlib.sha256(raw).hexdigest()
def read_json(raw):
    def unique(items):
        result={}
        for key,value in items:
            require(key not in result,'duplicate JSON key: '+key)
            result[key]=value
        return result
    return json.loads(raw,object_pairs_hook=unique)
def main():
    require(len(sys.argv)==3,'usage: verify_audit.py EXTERNAL_MANIFEST EXPECTED_SHA256')
    root=pathlib.Path(__file__).absolute().parent
    require(not root.is_symlink(),'symlink audit root')
    manifest_path=pathlib.Path(sys.argv[1]);require(not manifest_path.is_symlink(),'symlink external manifest')
    raw=manifest_path.read_bytes();require(digest(raw)==sys.argv[2],'external manifest SHA-256 differs from supplied trust pin')
    m=read_json(raw);require(m['problem_id']==9700033,'wrong problem ID');require(m['result']=='UNSOLVED_SCOPED_PARTIAL_ACCEPT_CORRECTED','wrong decision')
    entries=m['files'];actual=set();allowed_dirs=set()
    for name in entries:
        p=pathlib.PurePosixPath(name)
        require(not p.is_absolute() and '..' not in p.parts and '\\' not in name,'unsafe manifest name')
        allowed_dirs.update(x.as_posix() for x in p.parents if x.as_posix()!='.')
    for p in root.rglob('*'):
        require(not p.is_symlink(),'symlink audit member')
        rel=p.relative_to(root).as_posix()
        if p.is_dir():require(rel in allowed_dirs,'unexpected directory')
        else:require(p.is_file(),'special node');actual.add(rel)
    require(actual==set(entries),'audit inventory differs from external manifest')
    for name,e in entries.items():
        b=(root/name).read_bytes();require(len(b)==e['bytes'] and digest(b)==e['sha256'],'audit byte mismatch: '+name)
        if name.endswith('.json'):read_json(b)
    accepted=read_json((root/'ACCEPTANCE.json').read_bytes())
    require(accepted['status']=='ACCEPT_CORRECTED_SCOPED_PARTIAL','wrong exact acceptance status')
    for name,e in accepted['corrected_files'].items():
        b=(root/'corrected'/name).read_bytes();require(len(b)==e['bytes'] and digest(b)==e['sha256'],'acceptance binding: '+name)
    b=(root/'MEASURABILITY_CORRECTION.patch').read_bytes();require(digest(b)==accepted['patch']['sha256'] and len(b)==accepted['patch']['bytes'],'patch acceptance binding')
    executions=[]
    for directory in ['original','corrected']:
        for options in [[],['-O']]:
            p=subprocess.run([sys.executable,'-I','-B',*options,str(root/directory/'verify.py')],cwd=root.parent,capture_output=True,text=True,timeout=40)
            require(p.returncode==0,'package verifier failed: '+directory)
            answer=read_json(p.stdout);require(answer['status']=='PASS','package did not pass')
            executions.append({'package':directory,'optimized':bool(options),'result':answer})
    print(json.dumps({'status':'PASS','problem_id':9700033,'files_bound':len(entries),'manifest_sha256':digest(raw),'exact_acceptance_sha256':digest((root/'ACCEPTANCE.json').read_bytes()),'executions':executions,'limits':'Integrity and finite diagnostics only; mathematical acceptance is independent AI review, not formal proof.'},sort_keys=True))
if __name__=='__main__':
    try:main()
    except (ValueError,KeyError,TypeError,OSError,json.JSONDecodeError,subprocess.SubprocessError) as exc:
        print('FAIL: '+str(exc),file=sys.stderr);sys.exit(1)
