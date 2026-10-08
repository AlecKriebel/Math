#!/usr/bin/env python3
"""Externally authenticate this harness too; full baseline plus fail-closed tests."""
import copy,hashlib,json,os,re,shutil,stat,subprocess,sys,tempfile
from pathlib import Path
sha=lambda b:hashlib.sha256(b).hexdigest()
def need(ok,message):
    if not ok:raise ValueError(message)
def thaw(root):
    for p in root.rglob('*'):
        if p.is_dir() and not p.is_symlink():p.chmod(0o755)
        elif p.is_file() and not p.is_symlink() and p.stat().st_nlink==1:p.chmod(0o644)
    root.chmod(0o755)
def freeze(root):
    for p in root.iterdir():
        if p.is_file() and not p.is_symlink() and p.stat().st_nlink==1:p.chmod(0o444)
        elif p.is_dir() and not p.is_symlink():p.chmod(0o555)
    root.chmod(0o555)
def main():
    need(len(sys.argv)==5,'packet, before, after, externally trusted bootstrap SHA-256 required')
    root,before,after=[Path(os.path.abspath(x)) for x in sys.argv[1:4]];bp=sys.argv[4]
    need(os.getuid()==os.geteuid()==1000,'UID=EUID=1000');need(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode,'-I -S -B')
    bootstrap=(root/'BOOTSTRAP.py').read_bytes();need(sha(bootstrap)==bp,'external bootstrap pin')
    code=bootstrap.decode();mp=re.search("MANIFEST_SHA256 = '([0-9a-f]{64})'",code).group(1);vp=re.search("VERIFIER_SHA256 = '([0-9a-f]{64})'",code).group(1)
    verifier=(root/'verify_publication.py').read_bytes();need(sha(verifier)==vp,'verifier pin');need(sha((root/'PUBLICATION_MANIFEST.json').read_bytes())==mp,'manifest pin')
    ns={'__name__':'authenticated_test_target'};exec(compile(verifier,'<authenticated-test-target>','exec'),ns)
    initial=ns['integrity'](root,before,after,mp,bp);snapshot=initial[0];physical=ns['readonly'](root,before,after)
    mode=[] if sys.flags.optimize==0 else ['-'+'O'*sys.flags.optimize]
    env=dict(PATH=os.defpath,HOME='/tmp',TMPDIR='/tmp',LC_ALL='C')
    baseline=subprocess.run([sys.executable,'-I','-S','-B',*mode,str(root/'BOOTSTRAP.py'),str(root),str(before),str(after)],cwd=root,env=env,capture_output=True,timeout=1800)
    need(baseline.returncode==0 and baseline.stderr==b'','full baseline rejected')
    result=ns['parse'](baseline.stdout);need(result['whole_delivery_unchanged'] is True,'baseline integrity')
    # Baseline output is retained completely, not merely reduced to its status or counts.
    for item in result['replays']:
        tag=item['script'].removesuffix('.py');ns['compare_output'](item['script'],item['stdout'].encode(),item['stderr'].encode(),snapshot[tag+'.reference.stdout'],snapshot[tag+'.reference.stderr'])
    integrity_rows=[]
    def check_fixture(label,mutation):
        with tempfile.TemporaryDirectory(prefix='fast-bump-negative-') as temp:
            td=Path(temp);fixture=td/'packet';shutil.copytree(root,fixture);thaw(fixture)
            b=td/'before.md';a=td/'after.md';b.write_bytes(initial[1]);a.write_bytes(initial[2]);mutation(fixture,b,a);freeze(fixture);b.chmod(0o444);a.chmod(0o444)
            try:
                run=subprocess.run([sys.executable,'-I','-S','-B',*mode,str(root/'BOOTSTRAP.py'),str(fixture),str(b),str(a)],cwd=root,env=env,capture_output=True,timeout=20)
                need(run.returncode==1 and run.stdout==b'' and run.stderr in (b'REJECT: bootstrap integrity validation failed\n',b'REJECT: strict publication validation failed\n'),'integrity negative was not rejected: '+label)
                integrity_rows.append(dict(control=label,exit_code=run.returncode,stdout=run.stdout.decode(),stderr=run.stderr.decode()))
            finally:thaw(fixture)
    def modify(name,content):return lambda p,b,a:(p/name).write_bytes(content)
    def delete(name):return lambda p,b,a:(p/name).unlink()
    check_fixture('changed acceptance',modify('ACCEPTANCE.json',b'{}\n'))
    check_fixture('changed proof text',modify('SCOPE_AUDIT.md',b'altered proof\n'))
    check_fixture('changed source metadata',modify('SOURCE_METADATA.json',b'{}\n'))
    check_fixture('changed preparation receipt',modify('HARDENING_REPLAY.json',b'{}\n'))
    check_fixture('changed reference stdout',modify('check_reduction.reference.stdout',b'{"status":"PASS"}\n'))
    check_fixture('changed reference stderr',modify('check_reduction.reference.stderr',b'hidden failure\n'))
    check_fixture('changed mathematical code',modify('independent_controls.py',b'print("PASS")\n'))
    check_fixture('changed verifier',modify('verify_publication.py',b'print("PASS")\n'))
    check_fixture('changed manifest',modify('PUBLICATION_MANIFEST.json',b'{}\n'))
    check_fixture('changed bootstrap',modify('BOOTSTRAP.py',b'print("PASS")\n'))
    check_fixture('missing member',delete('ACCEPTANCE.md'))
    check_fixture('extra member',modify('EXTRA.txt',b'unlisted\n'))
    check_fixture('extra directory',lambda p,b,a:(p/'__pycache__').mkdir())
    def link(p,b,a):
        (p/'ACCEPTANCE.md').unlink();(p/'ACCEPTANCE.md').symlink_to(root/'ACCEPTANCE.md')
    check_fixture('linked member',link)
    def hardlink(p,b,a):
        os.link(p/'ACCEPTANCE.md',p.parent/'outside-hardlink')
    check_fixture('hardlinked member',hardlink)
    def fifo(p,b,a):
        (p/'ACCEPTANCE.md').unlink();os.mkfifo(p/'ACCEPTANCE.md')
    check_fixture('special member',fifo)
    check_fixture('actual before queue mismatch',lambda p,b,a:b.write_bytes(initial[1]+b'\n'))
    check_fixture('actual after queue mismatch',lambda p,b,a:a.write_bytes(initial[2]+b'\n'))
    # Resealing an altered member cannot replace the fixed externally pinned manifest.
    def reseal(p,b,a):
        f=p/'ACCEPTANCE.json';f.write_bytes(b'{}\n');m=json.loads((p/'PUBLICATION_MANIFEST.json').read_bytes())
        for row in m['files']:
            if row['path']==f.name:row.update(bytes=f.stat().st_size,sha256=sha(f.read_bytes()))
        (p/'PUBLICATION_MANIFEST.json').write_text(json.dumps(m))
    check_fixture('forged replacement manifest',reseal)
    semantic=[]
    def reject(label,f):
        try:f()
        except (ValueError,TypeError,KeyError,json.JSONDecodeError) as e:
            semantic.append(dict(control=label,rejected=True,error=str(e)));return
        raise ValueError('semantic negative accepted: '+label)
    for label,raw in [('duplicate keys',b'{"a":1,"a":2}'),('NaN',b'{"x":NaN}'),('Infinity',b'{"x":Infinity}'),('negative Infinity',b'{"x":-Infinity}'),('float overflow',b'{"x":1e9999}'),('trailing content',b'{} true'),('malformed JSON',b'{')]:reject(label,lambda raw=raw:ns['parse'](raw))
    manifest=ns['parse'](snapshot['PUBLICATION_MANIFEST.json'])
    def bad_manifest(label,change):
        obj=copy.deepcopy(manifest);change(obj);reject(label,lambda:ns['validate_manifest'](obj,snapshot))
    bad_manifest('manifest schema bool',lambda m:m.update(schema=True))
    bad_manifest('manifest schema float',lambda m:m.update(schema=1.0))
    bad_manifest('problem identifier bool',lambda m:m.update(problem_id=True))
    bad_manifest('unknown manifest key',lambda m:m.update(unexpected=1))
    bad_manifest('missing manifest key',lambda m:m.pop('schema'))
    bad_manifest('files wrong type',lambda m:m.update(files={}))
    bad_manifest('missing manifest member',lambda m:m['files'].pop())
    bad_manifest('duplicate manifest member',lambda m:m['files'].__setitem__(0,copy.deepcopy(m['files'][1])))
    for label,value in [('boolean bytes',True),('float bytes',1.0),('negative bytes',-1),('huge bytes',10**30),('string bytes','1')]:bad_manifest(label,lambda m,value=value:m['files'][0].update(bytes=value))
    for label,value in [('traversal path','../outside'),('absolute path','/tmp/outside'),('nonstring path',1),('manifest self reference','PUBLICATION_MANIFEST.json'),('bootstrap self reference','BOOTSTRAP.py'),('malformed digest','z'*64)]:
        key='sha256' if label=='malformed digest' else 'path';bad_manifest(label,lambda m,key=key,value=value:m['files'][0].update({key:value}))
    acceptance=ns['parse'](snapshot['ACCEPTANCE.json'])
    for key,value in [('unconditional_original_acceptance',True),('regular_only_exclusion_certified',True),('faithful_action_only_exclusion_certified',True),('question109_certified',True),('novelty_claim',True),('journal_acceptance_established',True),('indexing_action_faithfulness_required',True),('top_group_replaced_by_permutation_image',True),('base_support','unrestricted'),('new_proof_search_attempts',False),('queue_status','already_solved'),('queue_turns','5/5'),('schema',True),('credited_author','new discovery')]:
        obj=copy.deepcopy(acceptance);obj[key]=value;reject('acceptance '+key,lambda obj=obj:ns['validate_acceptance'](obj))
    obj=copy.deepcopy(acceptance);obj['extra']=0;reject('extra acceptance field',lambda:ns['validate_acceptance'](obj))
    obj=copy.deepcopy(ns['EXPECTED_QUEUE']);obj['changed_split_column']=10;reject('queue binding wrong column',lambda:ns['validate_queue_binding'](obj))
    b,a=initial[1:3]
    reject('queue unrelated line alteration',lambda:ns['validate_queue_delta'](b,a+b'\n'))
    reject('queue literal header alteration',lambda:ns['validate_queue_delta'](b,b'x'+a[1:]))
    lines=a.splitlines(keepends=True);i=next(i for i,l in enumerate(lines) if b'| 30003846 / OWR-16167-016 |' in l)
    for col,value in [(8,b' already_solved '),(9,b' 1/5 '),(10,b' changed notes '),(12,b' https://example.org/new '),(1,b' 9999 ')]:
        changed=list(lines);cells=changed[i].split(b'|');cells[col]=value;changed[i]=b'|'.join(cells);bad=b''.join(changed);reject('queue forbidden column '+str(col),lambda bad=bad:ns['validate_queue_delta'](b,bad))
    s='independent_controls.py';out=snapshot['independent_controls.reference.stdout'];err=snapshot['independent_controls.reference.stderr']
    def output_bad(label,mutated,stderr=err):reject(label,lambda:ns['compare_output'](s,mutated,stderr,out,err))
    for label,change in [('PASS-only stdout',b'{"status":"PASS"}\n'),('changed count',out.replace(b'"total_replayed_swaps": 48150',b'"total_replayed_swaps": 48151')),('boolean count',out.replace(b'"total_replayed_swaps": 48150',b'"total_replayed_swaps": true')),('float count',out.replace(b'"total_replayed_swaps": 48150',b'"total_replayed_swaps": 48150.0')),('changed output formatting',out.replace(b'  "status"',b'    "status"')),('extra stdout',out+b'PASS\n')]:output_bad(label,change)
    output_bad('nonempty stderr',out,b'warning\n')
    for label,val in [('negative elapsed',b'-1.0'),('integer elapsed',b'1'),('string elapsed',b'"1.0"'),('boolean elapsed',b'true'),('NaN elapsed',b'NaN'),('overflow elapsed',b'1e9999')]:output_bad(label,re.sub(rb'(?m)^(  "elapsed_seconds": )[^,]+,',lambda m:m[1]+val+b',',out))
    output_bad('duplicate elapsed',out.replace(b'  "elapsed_seconds":',b'  "elapsed_seconds": 1.0,\n  "elapsed_seconds":'))
    changed=re.sub(rb'(?m)^(  "elapsed_seconds": )[^,]+,',rb'\g<1>123.0,',out);ns['compare_output'](s,changed,err,out,err)
    # Hostile environment/site variables and cwd shadow files must not enter isolated subprocesses.
    with tempfile.TemporaryDirectory(prefix='fast-bump-hostile-') as temp:
        td=Path(temp);sentinel=td/'TRIGGERED';evil="from pathlib import Path\nPath("+repr(str(sentinel))+").write_text('bad')\nraise RuntimeError('hostile import')\n"
        for n in ['sitecustomize.py','usercustomize.py','json.py','hashlib.py','check_combinatorics.py']:(td/n).write_text(evil)
        hostile=dict(env,PYTHONPATH=str(td),PYTHONSTARTUP=str(td/'sitecustomize.py'),PYTHONHOME=str(td),PYTHONINSPECT='1',PYTHONDONTWRITEBYTECODE='0')
        probe="import sys,hashlib,json; print(json.dumps({'isolated':sys.flags.isolated,'no_site':sys.flags.no_site,'no_bytecode':sys.dont_write_bytecode,'optimization':sys.flags.optimize},sort_keys=True))"
        h=subprocess.run([sys.executable,'-I','-S','-B',*mode,'-c',probe],cwd=td,env=hostile,capture_output=True,timeout=20)
        need(h.returncode==0 and h.stderr==b'' and not sentinel.exists(),'hostile startup imported')
        hostile_record=dict(exit_code=h.returncode,stdout=h.stdout.decode(),stderr=h.stderr.decode(),sentinel_created=False,scope='Interpreter startup isolation only; full computational baseline separately replayed above')
    need(ns['integrity'](root,before,after,mp,bp)==initial,'original delivery changed')
    print(json.dumps(dict(schema=1,problem_id=30003846,status='PASS',uid=os.getuid(),euid=os.geteuid(),optimization=sys.flags.optimize,manifest_sha256=mp,bootstrap_sha256=bp,physical_denials=physical,baseline=dict(exit_code=baseline.returncode,stdout=baseline.stdout.decode(),stderr=baseline.stderr.decode()),integrity_negative_controls=integrity_rows,semantic_negative_controls=semantic,elapsed_only_positive_control=True,hostile_startup=hostile_record,whole_delivery_unchanged=True),sort_keys=True))
if __name__=='__main__':
    try:main()
    except (ValueError,OSError,TypeError,KeyError,subprocess.TimeoutExpired) as e:
        print('REJECT: mutation harness failed: '+type(e).__name__+': '+str(e),file=sys.stderr);sys.exit(1)
