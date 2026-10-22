#!/usr/bin/env python3
"""Independent actual CLI checks in the one owned disposable extraction."""
from pathlib import Path
import subprocess,sys,json,hashlib,os,datetime
H=Path(__file__).resolve().parent;S=H/'scratch';K=S/'clean_check/verification_kit';P=H.parents[1]/'preprint_v1_0'
rows=[]
def need(ok,msg):
    if not ok:raise RuntimeError(msg)
def pins():return {p.relative_to(K).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in K.rglob('*') if p.is_file()}
initial=pins();outside=S/'independent-outside';outside.mkdir(exist_ok=True)
sentinel=outside/'sentinel';sentinel.write_text('Independent protected sentinel\n');senthash=hashlib.sha256(sentinel.read_bytes()).hexdigest()
for opt in [False,True]:
    prefix=[sys.executable,'-I','-B']+(['-O'] if opt else [])
    def call(label,args,pass_expected=False,script='verify.py',root=K,needle=None):
        argv=prefix+[str(root/script)]+[str(x) for x in args]
        r=subprocess.run(argv,capture_output=True,text=True,timeout=120)
        row={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'label':label,'optimized':opt,'argv':argv,'returncode':r.returncode,'stdout':r.stdout,'stderr':r.stderr}
        rows.append(row)
        with (H/'INDEPENDENT_SEMANTIC_RECEIPTS.jsonl').open('a') as f:f.write(json.dumps(row)+'\n')
        need((r.returncode==0)==pass_expected,label+' exit')
        if needle:need(needle in r.stderr,label+' reason')
        return r
    call('optional-absent-default',[],True)
    call('required-absent',['--require-binding'],needle='external binding required')
    call('explicit-missing',['--binding',outside/'absent-binding'],needle='input missing')
    adj=K.parent/'EXTERNAL_BINDING.json'
    for label,body,needle in [('malformed-present','{broken','JSONDecodeError'),('wrong-present',json.dumps({'manifest_sha256':'0'*64}),'external manifest binding mismatch')]:
        adj.write_text(body);call(label,[],needle=needle);adj.unlink()
    leaf=outside/'binding-link';leaf.symlink_to(P/'EXTERNAL_BINDING.json')
    call('binding-leaf-symlink',['--binding',leaf],needle='input symlink rejected');leaf.unlink()
    ancestor=outside/'binding-parent';ancestor.symlink_to(P,target_is_directory=True)
    call('binding-ancestor-symlink',['--binding',ancestor/'EXTERNAL_BINDING.json'],needle='input symlink rejected');ancestor.unlink()
    for artifact in ['pdf','archive']:
        call('corrupt-bound-'+artifact,['--binding',P/'EXTERNAL_BINDING.json','--'+artifact,sentinel],needle='bound artifact mismatch')
    # Bootstrap leaf symlinks must be rejected before parsing their invalid target.
    bad=outside/'invalid-json';bad.write_text('{not-json')
    for name in ['ALLOWLIST.json','MANIFEST.json']:
        path=K/name;original=path.read_bytes();path.unlink();path.symlink_to(bad)
        call('preparse-bootstrap-'+name,[],needle='symlink')
        path.unlink();path.write_bytes(original)
    bad.unlink()
    alias=K.with_name(K.name.swapcase());need(alias.samefile(K),'Actual case-alias premise unavailable')
    for label,dest,root in [
        ('case-root',alias/'independent-new.zip',K),
        ('case-nested',alias/'originals/independent-new.zip',K),
        ('case-two-missing-ancestors',alias/'missing-one/missing-two/independent-new.zip',K),
        ('case-reverse-root',K/'independent-new.zip',alias),
        ('case-reverse-two-missing',K/'missing-one/missing-two/independent-new.zip',alias),
        ('raw-dotdot-case',alias/'originals/../independent-new.zip',K)]:
        call(label,['--output',dest],script='build_archive.py',root=root,needle='archive')
        need(not dest.exists(),label+' created output')
    need(not (K/'missing-one').exists(),'Missing ancestors created')
    link=outside/'ancestor-link';link.symlink_to(outside,target_is_directory=True)
    call('unresolved-symlink-dotdot',['--output',link/'../new.zip'],script='build_archive.py',needle='symlink');link.unlink()
    hard=outside/'hardlink.zip';os.link(K/'preprint.tex',hard)
    call('hardlink-to-source',['--output',hard],script='build_archive.py',needle='fresh');hard.unlink()
    call('existing-external-sentinel',['--output',sentinel],script='build_archive.py',needle='fresh')
    dest=outside.with_name(outside.name.swapcase())/('positive-O.zip' if opt else 'positive.zip')
    need(dest.parent.samefile(outside),'Actual outside case premise')
    call('positive-external-case',['--output',dest],True,'build_archive.py')
    need(hashlib.sha256(dest.read_bytes()).hexdigest()==hashlib.sha256((P/'verification_kit.zip').read_bytes()).hexdigest(),'Independent rebuild bytes')
    dest.unlink();need(pins()==initial,'Owned extraction changed')
    need(hashlib.sha256(sentinel.read_bytes()).hexdigest()==senthash,'Sentinel changed')
(H/'INDEPENDENT_SEMANTIC_RESULTS.json').write_text(json.dumps({'status':'PASS','actual_commands':len(rows),'physical_alias_available':True,'all_kit_input_hashes_unchanged':len(initial),'sentinel_unchanged':True,'both_python_modes':True},indent=2)+'\n')
print('PASS',len(rows))
