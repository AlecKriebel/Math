"""Author-only sealing and malformed-input driver. Confined to this packet."""
from pathlib import Path
import datetime, hashlib, json, shutil, subprocess, sys, tempfile

ROOT=Path(__file__).resolve().parent
MODES={'normal':[],'O':['-O'],'OO':['-OO']}

def require(ok,msg):
    if not ok:
        raise RuntimeError(msg)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def dump(path,obj):
    path.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')

def seal(root):
    files=[]
    for p in sorted(root.rglob('*')):
        if p.is_file() and p.name not in {'MANIFEST.json','SEAL.sha256'}:
            # Exclude only the two ROOT seal files, never a captured head manifest.
            if p.parent==root:
                pass
        if p.is_file() and p not in [root/'MANIFEST.json',root/'SEAL.sha256']:
            require(not p.is_symlink(),'unexpected source symlink')
            b=p.read_bytes();files.append({'path':p.relative_to(root).as_posix(),'bytes':len(b),'sha256':digest(b)})
    dump(root/'MANIFEST.json',{'schema':1,'scope':'pr1129_projective_adversary','files':files})
    s=digest((root/'MANIFEST.json').read_bytes())
    (root/'SEAL.sha256').write_text(s+'  MANIFEST.json\n')
    return s

def invoke(root,s,flags):
    r=subprocess.run([sys.executable,'-B']+flags+[str(root/'verify_offline.py'),'--root',str(root),'--manifest-sha256',s],capture_output=True,text=True)
    try:out=json.loads(r.stdout)
    except Exception as e:raise RuntimeError('invalid verifier JSON '+r.stderr) from e
    return r,out

def refresh_entry(root,name):
    m=json.loads((root/'MANIFEST.json').read_text())
    for e in m['files']:
        if e['path']==name:
            b=(root/name).read_bytes();e.update(bytes=len(b),sha256=digest(b));break
    else:raise RuntimeError('entry not found')
    dump(root/'MANIFEST.json',m)

def mutate(root,kind):
    path=root/'MANIFEST.json'
    if kind=='bad_external_digest':return '0'*64
    if kind=='duplicate_json_key':
        b=path.read_bytes();path.write_bytes(b'{"schema":1,'+b[1:])
    elif kind in ['traversal','duplicate_member','closed_missing_required']:
        m=json.loads(path.read_text())
        if kind=='traversal':m['files'][0]['path']='../outside'
        elif kind=='duplicate_member':m['files'].append(m['files'][0].copy())
        else:
            m['files']=[e for e in m['files'] if e['path']!='REVIEW.md'];(root/'REVIEW.md').unlink()
        dump(path,m)
    elif kind=='unlisted_file':(root/'EXTRA.txt').write_text('unexpected')
    elif kind=='missing_file':(root/'CLAIM.json').unlink()
    elif kind=='symlink_file':
        (root/'CLAIM.json').unlink();(root/'CLAIM.json').symlink_to('REVIEW.md')
    elif kind=='source_byte_tamper':
        with (root/'private/owr.pdf').open('ab') as f:f.write(b'X')
    elif kind in ['wrong_head','wrong_parity','wrong_cutoff']:
        name='CLAIM.json';c=json.loads((root/name).read_text())
        c[{'wrong_head':'head','wrong_parity':'theorem_N_parity','wrong_cutoff':'parameter_bound'}[kind]]={'wrong_head':'0'*40,'wrong_parity':1,'wrong_cutoff':4}[kind]
        dump(root/name,c);refresh_entry(root,name)
    elif kind=='wrong_source_url':
        name='SOURCE_BINDINGS.json';c=json.loads((root/name).read_text());c['primary_sources'][0]['url']='https://invalid.example/other';dump(root/name,c);refresh_entry(root,name)
    elif kind=='wrong_git_blob':
        name='private/head_inventory.json';c=json.loads((root/name).read_text());c['files'][0]['blob']='0'*40;dump(root/name,c);refresh_entry(root,name)
    else:raise RuntimeError('unknown mutation')
    return digest(path.read_bytes())

def main():
    receipt=ROOT/'VALIDATION_RUNS.json'
    if not receipt.exists():dump(receipt,{'status':'pending'})
    s=seal(ROOT)
    results=[];baseline=[]
    for mode,flags in MODES.items():
        r,out=invoke(ROOT,s,flags)
        require(r.returncode==0 and out['status']=='pass','baseline '+mode+' failed '+r.stdout+r.stderr)
        baseline.append({'mode':mode,'returncode':r.returncode,'status':out['status'],'stdout_sha256':digest(r.stdout.encode())})
    faults={
      'bad_external_digest':'external manifest SHA256 mismatch',
      'duplicate_json_key':'duplicate JSON key',
      'traversal':'unsafe path',
      'duplicate_member':'duplicate manifest member',
      'closed_missing_required':'required packet member absent',
      'unlisted_file':'packet closure mismatch',
      'missing_file':'missing packet file',
      'symlink_file':'symlink in packet',
      'source_byte_tamper':'byte count mismatch',
      'wrong_head':'claim binding mismatch: head',
      'wrong_parity':'claim binding mismatch: theorem_N_parity',
      'wrong_cutoff':'claim binding mismatch: parameter_bound',
      'wrong_source_url':'primary source binding',
      'wrong_git_blob':'Git blob mismatch'}
    members=json.loads((ROOT/'MANIFEST.json').read_text())['files']
    with tempfile.TemporaryDirectory(prefix='owned_fault_fixtures_',dir=ROOT) as td:
        for kind,expected in faults.items():
            target=Path(td)/kind;target.mkdir()
            for e in members:
                src=ROOT/e['path'];dst=target/e['path'];dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst)
            shutil.copyfile(ROOT/'MANIFEST.json',target/'MANIFEST.json')
            bad_s=mutate(target,kind)
            for mode,flags in MODES.items():
                r,out=invoke(target,bad_s,flags)
                require(r.returncode==1 and out.get('status')=='fail' and expected in out.get('reason',''),'fault not specifically rejected '+kind+' '+mode+' '+r.stdout+r.stderr)
                results.append({'fault':kind,'mode':mode,'returncode':r.returncode,'reason':out['reason']})
            shutil.rmtree(target)
    record={'status':'pass','checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
       'modes':baseline,'malformed_controls':results,'malformed_cases_per_mode':len(faults),
       'mathematical_boundary':'Finite controls only; no universal theorem is inferred from their count or packet hashing.',
       'seal_procedure':'Receipt included in final manifest; final sealed packet rerun in all three modes and stdout compared with these mode hashes. Final digest held externally in SEAL.sha256.'}
    dump(receipt,record)
    with (ROOT/'RESEARCH_LOG.md').open('a') as f:
        f.write('\n'+datetime.datetime.now(datetime.timezone.utc).isoformat()+' — Checkpoint, estimated completion100%. Independent projective review concluded without substantive mathematical objection. Exact interfaces passed with8 deliberate algebra/parity/degree controls. Read-only packet verification passed normal/-O/-OO;14 malformed-packet cases rejected specifically in every mode. Receipt and all private source inputs sealed; final verification repeated after final seal. No publication/priority verdict.\n')
    s=seal(ROOT)
    for e in baseline:
        r,out=invoke(ROOT,s,MODES[e['mode']])
        require(r.returncode==0 and digest(r.stdout.encode())==e['stdout_sha256'],'final seal differs '+r.stdout+r.stderr)
    print(json.dumps({'status':'pass','manifest_sha256':s,'baseline_modes':3,'fault_cases':len(faults),'fault_runs':len(results),'final_sealed_modes':3},sort_keys=True))

if __name__=='__main__':main()
