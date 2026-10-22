#!/usr/bin/env python3
"""Independent review harness. Private paths and raw bodies stay in private_tmp."""
import copy, datetime, hashlib, importlib.util, io, json, os
from pathlib import Path
import shutil, stat, struct, subprocess, sys, time, traceback, zipfile, zlib

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
SUPPLIED = BASE / 'publication_tools_01'
TMP = HERE / 'private_tmp'
TMP.mkdir(exist_ok=True)
PIN = 'f17b0c2cf4fafdd586560c13ed5ab9dcffa87790b297558ada36da0da59ec999'
TOOL_PIN = 'a5b5ab7a3b0397e1d21bd70d3637ef1e200a7eba50419c0052e357b46a0e1d9c'
MAN_PIN = '179b1a05f8fb8f3243a171e8a3a584423ee75f373cfbf6280a7c7d7636a59310'
SOURCE_PIN = '1d677ef16697e1e294f9f86800c10fe3189270cf2d9771a75d7c4e64954c0d1c'
PY = sys.executable
def stamp(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b): return hashlib.sha256(b).hexdigest()
def pin(b): return dict(bytes=len(b), sha256=sha(b))
def dump(obj): return (json.dumps(obj, indent=2, sort_keys=True)+'\n').encode()
def write(path, raw):
    with path.open('xb') as f:
        f.write(raw); f.flush(); os.fsync(f.fileno())
def save(name, obj): write(HERE/name, dump(obj))
RESULTS=[]
def result(name, ok, detail=None):
    row=dict(name=name, passed=bool(ok), detail=detail, timestamp_utc=stamp())
    with (HERE/'TEST_RESULTS.jsonl').open('a') as f:
        f.write(json.dumps(row, sort_keys=True)+'\n'); f.flush(); os.fsync(f.fileno())
    RESULTS.append(row)
    if not ok: print('FAIL',name,detail,flush=True)
    return ok
def expect_raise(name, fn):
    try: fn()
    except Exception as e: return result(name,True,dict(type=type(e).__name__,reason=str(e)))
    return result(name,False,'accepted')
SEQ=0
def process(name, command, *, cwd=TMP, environment=None, timeout=120):
    global SEQ
    SEQ+=1; stem=TMP/('invocation-%03d'%SEQ)
    started=stamp(); mono=time.monotonic_ns(); p=None; expired=False
    try:
        p=subprocess.Popen(command,cwd=cwd,env=environment,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        launched=stamp()
        try: out,err=p.communicate(timeout=timeout)
        except subprocess.TimeoutExpired: expired=True;p.kill();out,err=p.communicate()
        meta=dict(name=name,started_utc=started,launched_utc=launched,ended_utc=stamp(),elapsed_ns=time.monotonic_ns()-mono,pid=p.pid,returncode=p.returncode,timeout=expired,stdout=pin(out),stderr=pin(err))
    except OSError as e:
        out=b'';err=(type(e).__name__+': '+str(e)).encode()
        meta=dict(name=name,started_utc=started,ended_utc=stamp(),elapsed_ns=time.monotonic_ns()-mono,pid=None,returncode=None,timeout=False,launch_error=type(e).__name__,stdout=pin(out),stderr=pin(err))
    # Persist actual raw evidence before interpreting or asserting any outcome.
    write(Path(str(stem)+'.stdout.bin'),out)
    write(Path(str(stem)+'.stderr.bin'),err)
    write(Path(str(stem)+'.json'),dump(meta))
    with (HERE/'PROCESS_INDEX.jsonl').open('a') as f:
        f.write(json.dumps(dict(receipt=stem.name,**meta),sort_keys=True)+'\n'); f.flush(); os.fsync(f.fileno())
    return meta,out,err
def cli(name,args,*,mode=0,environment=None,accepted=True,contains=None,tool=None):
    cmd=[PY,'-I','-S','-B']+(['-O'] if mode else [])+[str(tool or SUPPLIED/'portable.py'),*map(str,args)]
    meta,out,err=process(name,cmd,environment=environment,timeout=180)
    try: decoded=json.loads(out)
    except Exception: decoded=None
    ok=meta['returncode']==(0 if accepted else 1) and err==b'' and isinstance(decoded,dict) and decoded.get('status')==('PASS' if accepted else 'REJECTED')
    if contains is not None: ok=ok and contains in out.decode(errors='replace')
    result(name,ok,dict(receipt='invocation-%03d'%SEQ,returncode=meta['returncode'],status=decoded.get('status') if decoded else None,reason=decoded.get('reason') if decoded else None))
    return decoded,meta,out,err
def authenticate():
    rows=[]
    for rel,n,h in [('SAFE_MANIFEST.json',4062,MAN_PIN),('portable.py',49920,TOOL_PIN),('verification/package_index.json',4095,PIN)]:
        b=(SUPPLIED/rel).read_bytes();rows.append(dict(path=rel,**pin(b),passed=len(b)==n and sha(b)==h))
    safe=json.loads((SUPPLIED/'SAFE_MANIFEST.json').read_bytes())
    for row in safe['files']:
        b=(SUPPLIED/row['path']).read_bytes();rows.append(dict(path=row['path'],**pin(b),passed=pin(b)=={k:row[k] for k in ('bytes','sha256')}))
    raw=(BASE/'SOURCE_MANIFEST.json').read_bytes()
    rows.append(dict(path='original-manifest',**pin(raw),passed=len(raw)==4654 and sha(raw)==SOURCE_PIN))
    src=json.loads(raw)
    for label,root in [('original-source',BASE/'source'),('portable-source',SUPPLIED/'verification/source')]:
        for row in src['files']:
            b=(root/row['path']).read_bytes();blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
            rows.append(dict(path=label+'/'+row['path'],**pin(b),git_blob=blob,passed=pin(b)=={k:row[k] for k in ('bytes','sha256')} and blob==row['git_blob']))
    idx=json.loads((SUPPLIED/'verification/package_index.json').read_bytes())
    for row in idx['files']:
        b=(SUPPLIED/'verification'/row['path']).read_bytes();rows.append(dict(path='indexed/'+row['path'],**pin(b),passed=pin(b)=={k:row[k] for k in ('bytes','sha256')}))
    save('AUTHENTICATION.json',dict(timestamp_utc=stamp(),checks=rows,all_pass=all(r['passed'] for r in rows),safe_rows=len(safe['files']),source_rows=len(src['files']),source_bytes=sum(r['bytes'] for r in src['files']),indexed_files=len(idx['files'])+1))
    if not all(r['passed'] for r in rows): raise RuntimeError('authentication failed')
def independent_zip(blobs, *, suffix=b'', mode=stat.S_IFREG|0o644, date=(2026,10,16), trailing_deflate=b''):
    # Independent raw record construction: no ZipFile writer or tool helper.
    local=bytearray();central=bytearray();td=((date[0]-1980)<<9)|(date[1]<<5)|date[2]
    for i,name in enumerate(sorted(blobs)):
        raw=blobs[name];nameb=name.encode('ascii'); c=zlib.compressobj(9,zlib.DEFLATED,-15);compressed=c.compress(raw)+c.flush()
        if i==0: compressed+=trailing_deflate
        crc=zlib.crc32(raw)&0xffffffff;offset=len(local)
        local.extend(struct.pack('<I5H3I2H',0x04034b50,20,0,8,0,td,crc,len(compressed),len(raw),len(nameb),0));local.extend(nameb);local.extend(compressed)
        central.extend(struct.pack('<I6H3I5H2I',0x02014b50,0x0314,20,0,8,0,td,crc,len(compressed),len(raw),len(nameb),0,0,0,0,mode<<16,offset));central.extend(nameb)
    return bytes(local+central+struct.pack('<I4H2IH',0x06054b50,0,0,len(blobs),len(blobs),len(central),len(local),0))+suffix
def tree(root,blobs):
    root.mkdir()
    for name,raw in blobs.items():
        p=root/name;p.parent.mkdir(exist_ok=True,parents=True);p.write_bytes(raw)
def indexed(blobs,schema='post-lie-30005737-verification-v1'):
    obj=dict(schema=schema,problem_id='30005737',files=[dict(path=n,**pin(b)) for n,b in sorted(blobs.items())])
    return dump(obj)
def fixture_current(portable):
    outer={k:portable[k] for k in ('portable.py','metadata.json','zenodo-deposit.json','note.tex')}
    outer.update({'verification/'+n:b for n,b in portable.items()})
    outer['CURRENT_PUBLICATION.json']=(SUPPLIED/'CURRENT_LAYOUT_TEMPLATE.json').read_bytes()
    outer['post-lie-note.pdf']=b'%PDF-1.7\nNOT ACTUAL PAPER; HEADER ONLY FIXTURE\n'
    outer['post-lie-verification.zip']=independent_zip(portable)
    outer['CURRENT_PUBLICATION_MANIFEST.json']=indexed(outer,'post-lie-30005737-current-publication-v1')
    return outer
def reindex_current(outer, *, regenerate_zip=True):
    p={n[13:]:b for n,b in outer.items() if n.startswith('verification/') and n!='verification/package_index.json'}
    p['package_index.json']=indexed(p)
    outer.update({'verification/'+n:b for n,b in p.items()})
    if regenerate_zip:outer['post-lie-verification.zip']=independent_zip(p)
    outer.pop('CURRENT_PUBLICATION_MANIFEST.json',None)
    outer['CURRENT_PUBLICATION_MANIFEST.json']=indexed(outer,'post-lie-30005737-current-publication-v1')
    return outer
def checkpoint(pct,text):
    with (HERE/'RESEARCH_LOG.md').open('a') as f:f.write('- '+stamp()+' — '+str(pct)+'%: '+text+'\n')

def main():
    authenticate()
    spec=importlib.util.spec_from_file_location('independent_subject',SUPPLIED/'portable.py'); m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    portable={str(p.relative_to(SUPPLIED/'verification')):p.read_bytes() for p in (SUPPLIED/'verification').rglob('*') if p.is_file()}
    baseline=TMP/'portable';tree(baseline,portable)
    subject=baseline/'portable.py'
    result('independent_raw_zip_matches_tool_writer', independent_zip(portable)==m.deterministic_zip(portable),pin(independent_zip(portable)))
    # Actual CLI positives and no-execution behavior.
    a,_,_,_=cli('verify_only_actual',['verify',PIN,'--root',baseline,'--verify-only'],tool=subject)
    result('verify_only_exact_label_and_zero_replay',a is not None and a['replay']==dict(status='NOT_RUN',archival_code_executed=False,label='VERIFY_ONLY_BYTE_AUTHENTICATION_NO_ARCHIVAL_EXECUTION'))
    cli('verify_only_receipt_rejected',['verify',PIN,'--root',baseline,'--verify-only','--receipt-dir',TMP/'forbidden-verify-receipt'],tool=subject,accepted=False)
    result('verify_only_created_no_receipt',not (TMP/'forbidden-verify-receipt').exists())
    for mode in (0,1):
        rec=TMP/('replay-%d'%mode)
        value,_,_,_=cli('verify_default_replay_%d'%mode,['verify',PIN,'--root',baseline,'--receipt-dir',rec],mode=mode,tool=subject)
        if value:
            events=value.get('replay',{}).get('launcher',{}).get('events',[])
            result('replay_independent_receipt_schedule_%d'%mode,len(events)==8 and [e['measured_flags']['optimize'] for e in events]==[0,1,0,0,0,1,1,1] and all(e['original_execution_began']==(e['kind']!='corrupt') for e in events))
            for e in events:
                stem=rec/'processes'/e['raw_receipt_stem']
                actual=json.loads(Path(str(stem)+'.json').read_bytes())
                result('raw_receipt_%d_%s'%(mode,e['raw_receipt_stem']),pin(Path(str(stem)+'.stdout.bin').read_bytes())==actual['stdout'] and pin(Path(str(stem)+'.stderr.bin').read_bytes())==actual['stderr'] and actual['started_utc']<=actual['ended_utc'] and isinstance(actual['returncode'],int))
    outdir=TMP/'build';outdir.mkdir()
    built,_,_,_=cli('build_default_replays',['build',PIN,outdir/'post-lie-verification.zip','--root',baseline,'--receipt-dir',TMP/'replay-build'],tool=subject)
    if built:result('build_raw_independent_byte_reconstruction',(outdir/'post-lie-verification.zip').read_bytes()==independent_zip(portable))
    cli('build_never_overwrites',['build',PIN,outdir/'post-lie-verification.zip','--root',baseline,'--receipt-dir',TMP/'must-not-replay'],tool=subject,accepted=False)
    result('build_overwrite_fails_before_replay',not (TMP/'must-not-replay').exists())
    current=fixture_current(portable); curroot=TMP/'NOT_ACTUAL_PAPER_current';tree(curroot,current);cpin=sha(current['CURRENT_PUBLICATION_MANIFEST.json'])
    value,_,_,_=cli('current_verify_only',['current',cpin,'--root',curroot,'--verify-only'],tool=subject)
    result('current_header_only_scope',value and value['pdf_validation']=='HEADER_ONLY' and value['visual_qa']=='SEPARATE_REVIEW_REQUIRED')
    cli('current_default_replay',['current',cpin,'--root',curroot,'--receipt-dir',TMP/'current-replay'],tool=subject)
    cli('current_optimized_replay',['current',cpin,'--root',curroot,'--receipt-dir',TMP/'current-replay-o'],tool=subject,mode=1)
    checkpoint(45,'Authenticated positives, real normal/optimized original replay, build, current and independent raw ZIP reconstruction exercised. Paper fixture remains HEADER ONLY and NOT ACTUAL PAPER.')
    # Strict JSON and typed inventory direct challenges, independent of pin failure.
    for name,b in [('duplicate',b'{"x":1,"x":2}'),('nested_duplicate',b'{"x":{"a":1,"a":2}}'),('nan',b'{"x":NaN}'),('infinity',b'[Infinity]'),('overflow',b'[1e400]')]:
        expect_raise('json_'+name,lambda b=b:m.strict_json(b))
    for val in [True,False,1.0,-1,256*1024*1024+1,'0',None]:
        expect_raise('typed_bytes_'+repr(val),lambda val=val:m.pin_row(dict(path='x',bytes=val,sha256='0'*64)))
    for names in [['x','X'],['a','a/b'],['A/x','a/y'],['a//b'],['../a'],['/a'],['./a'],['a\\b']]:
        expect_raise('path_inventory_'+repr(names),lambda names=names:m.rows_map([dict(path=n,bytes=0,sha256='0'*64) for n in names]))
    malformed=TMP/'malformed';tree(malformed,portable)
    def index_case(name,raw):
        (malformed/'package_index.json').write_bytes(raw)
        cli(name,['verify',sha(raw),'--root',malformed,'--verify-only'],tool=subject,accepted=False)
        (malformed/'package_index.json').write_bytes(portable['package_index.json'])
    idx=json.loads(portable['package_index.json'])
    raw=portable['package_index.json'].replace(b'"problem_id": "30005737"',b'"problem_id": "30005737", "problem_id": "30005737"')
    index_case('cli_duplicate_key_reindexed',raw)
    for val in [True,0.0,1e100]:
        obj=copy.deepcopy(idx);obj['files'][0]['bytes']=val;index_case('cli_bytes_type_'+repr(val),dump(obj))
    for val in [True,30005737]:
        obj=copy.deepcopy(idx);obj['problem_id']=val;index_case('cli_id_type_'+repr(val),dump(obj))
    (malformed/'empty').mkdir();cli('cli_unlisted_empty_directory',['verify',PIN,'--root',malformed,'--verify-only'],tool=subject,accepted=False);(malformed/'empty').rmdir()
    (malformed/'unlisted').write_bytes(b'x');cli('cli_unlisted_regular_file',['verify',PIN,'--root',malformed,'--verify-only'],tool=subject,accepted=False);(malformed/'unlisted').unlink()
    old=(malformed/'metadata.json').read_bytes();(malformed/'metadata.json').unlink();(malformed/'metadata.json').symlink_to(baseline/'metadata.json')
    cli('cli_symlink_member',['verify',PIN,'--root',malformed,'--verify-only'],tool=subject,accepted=False);(malformed/'metadata.json').unlink();(malformed/'metadata.json').write_bytes(old)
    symlink=TMP/'symlink-root';symlink.symlink_to(baseline,target_is_directory=True)
    cli('cli_symlink_root',['verify',PIN,'--root',symlink,'--verify-only'],tool=subject,accepted=False)
    # Actual output/receipt preflight, including case-insensitive APFS physical aliases.
    cli('receipt_existing_directory',['verify',PIN,'--root',baseline,'--receipt-dir',outdir],tool=subject,accepted=False)
    cli('receipt_inside_indexed_root',['verify',PIN,'--root',baseline,'--receipt-dir',baseline/'new-receipts'],tool=subject,accepted=False)
    cli('build_inside_indexed_root',['build',PIN,baseline/'post-lie-verification.zip','--root',baseline,'--receipt-dir',TMP/'must-not-build-inside'],tool=subject,accepted=False)
    cli('build_wrong_exact_name',['build',PIN,outdir/'wrong.zip','--root',baseline],tool=subject,accepted=False)
    (TMP/'outside-link').symlink_to(outdir,target_is_directory=True)
    cli('receipt_symlink_parent',['verify',PIN,'--root',baseline,'--receipt-dir',TMP/'outside-link'/'receipt'],tool=subject,accepted=False)
    alias=baseline.with_name(baseline.name.upper())
    same=alias.exists() and os.path.samefile(alias,baseline)
    result('physical_case_alias_capability',same)
    if same:
        cli('receipt_physical_case_alias',['verify',PIN,'--root',baseline,'--receipt-dir',alias/'case-receipt'],tool=subject,accepted=False,contains='physical device/inode')
        cli('build_physical_case_alias',['build',PIN,alias/'post-lie-verification.zip','--root',baseline],tool=subject,accepted=False,contains='physical device/inode')
    # Internally coherent, reindexed metadata deviations must still fail fixed guards.
    metaroot=TMP/'metadata-current';tree(metaroot,current)
    def current_case(name,outer):
        outer=reindex_current(outer)
        for n,b in outer.items():(metaroot/n).write_bytes(b)
        cli(name,['current',sha(outer['CURRENT_PUBLICATION_MANIFEST.json']),'--root',metaroot,'--verify-only'],tool=subject,accepted=False)
    for key,val in [('title','Different title'),('publication_date','2026-10-17'),('version','2.0.0'),('license','cc0-1.0'),('access_right','closed'),('publication_type','article'),('creators',[dict(name='Kriebel, Alec',affiliation='Other',orcid='0009-0001-9320-500X')])]:
        outer=dict(current);meta=json.loads(outer['metadata.json']);meta[key]=val;deposit=json.loads(outer['zenodo-deposit.json']);deposit['metadata']=meta
        for prefix in ('','verification/'):
            outer[prefix+'metadata.json']=dump(meta);outer[prefix+'zenodo-deposit.json']=dump(deposit)
        current_case('current_fixed_identity_'+key,outer)
    outer=dict(current);d=json.loads(outer['zenodo-deposit.json']);d['files'][0]['path']='other.pdf'
    outer['zenodo-deposit.json']=outer['verification/zenodo-deposit.json']=dump(d);current_case('current_exact_two_assets',outer)
    outer=dict(current);outer['note.tex']+=b'\ncopy mismatch\n';current_case('current_outer_inner_copy_mismatch',outer)
    # Actual current-mode strict archive rejection with coherent external manifest.
    for name,z in [('prefix',b'x'+independent_zip(portable)),('trailer',independent_zip(portable,suffix=b'x')),('unused_deflate',independent_zip(portable,trailing_deflate=b'JUNK')),('concatenated_deflate',independent_zip(portable,trailing_deflate=zlib.compress(b'other'))),('wrong_mode',independent_zip(portable,mode=stat.S_IFREG|0o444)),('wrong_date',independent_zip(portable,date=(2026,10,15)))]:
        outer=dict(current);outer['post-lie-verification.zip']=z;outer=reindex_current(outer,regenerate_zip=False)
        for n,b in outer.items():(metaroot/n).write_bytes(b)
        cli('current_zip_'+name,['current',sha(outer['CURRENT_PUBLICATION_MANIFEST.json']),'--root',metaroot,'--verify-only'],tool=subject,accepted=False)
    original={p.name:p.read_bytes() for p in (BASE/'source/authored').iterdir() if p.is_file() and p.name!='AUDIT_VOLUME_TOPOLOGY.md'}
    result('original_nine_member_zip_exact_validation',m.zip_payloads((BASE/'source/AUTHOR_CANDIDATE.zip').read_bytes(),original)==original)
    expect_raise('original_zip_unused_deflate_representation',lambda:m.zip_payloads(independent_zip(original,date=(2026,10,16),trailing_deflate=b'x'),original))
    checkpoint(65,'Adversarial JSON, closed tree, metadata, raw ZIP and output/receipt safety tests completed; proceeding to hostile startup and native first-pass ordering.')
    # Capability control: unisolated original checker startup hook emits frozen
    # output and exits before checker code. Reviewed tool must resist this.
    hostile=TMP/'hostile';hostile.mkdir();marker=hostile/'hook-ran';expected=(BASE/'source/authored/CHECK_RESULTS.json').read_bytes()
    hook="import os\nfrom pathlib import Path\nPath(os.environ['REVIEW_HOOK_MARKER']).write_bytes(b'HOOK')\nos.write(1,Path(os.environ['REVIEW_FROZEN_OUTPUT']).read_bytes())\nos._exit(0)\n"
    (hostile/'sitecustomize.py').write_text(hook)
    env=dict(os.environ,PYTHONPATH=str(hostile),PYTHONOPTIMIZE='2',REVIEW_HOOK_MARKER=str(marker),REVIEW_FROZEN_OUTPUT=str(BASE/'source/authored/CHECK_RESULTS.json'))
    meta,out,err=process('hostile_positive_capability_control',[PY,str(BASE/'source/authored/check_algebra.py')],environment=env)
    result('hostile_hook_capability_proven',meta['returncode']==0 and out==expected and err==b'' and marker.read_bytes()==b'HOOK')
    marker.unlink()
    for mode in (0,1):
        hostile_env=dict(env,__PYVENV_LAUNCHER__=PY)
        value,_,_,_=cli('hostile_environment_replay_%d'%mode,['verify',PIN,'--root',baseline,'--receipt-dir',TMP/('hostile-replay-%d'%mode)],mode=mode,environment=hostile_env,tool=subject)
        result('hostile_hook_did_not_run_%d'%mode,not marker.exists())
        if value:
            ev=value.get('replay',{}).get('launcher',{}).get('events',[])
            result('hostile_actual_optimization_%d'%mode,[e['measured_flags']['optimize'] for e in ev]==[0,1,0,0,0,1,1,1] and all(e['process']['environment_policy']=='PYTHON variables and __PYVENV_LAUNCHER__ removed' for e in ev))
    # Native actual complete input checks; no raw corpus copies.
    workspace=BASE.parents[2]
    native=[workspace/'unsolved_math_prioritization/catalog.json',workspace/'unsolved_math_prioritization/cache/problems.json',workspace/'unsolved_math_prioritization/cache/research_results.json']
    nativeargs=['--catalog',native[0],'--problems',native[1],'--reports',native[2]]
    for mode in (0,1):
        value,_,_,_=cli('source_only_actual_%d'%mode,['source-only',*nativeargs],mode=mode,tool=subject)
    cli('primary_unlisted_text_files_rejected',['source-only',*nativeargs,'--primary-dir',BASE/'private_sources'],tool=subject,accepted=False)
        # Actual primary directory contains text extracts and should be rejected;
        # strict positive primary path is constructed separately below.
    primary=TMP/'primary';primary.mkdir()
    for name in m.PRIMARY_PINS:os.link(BASE/'private_sources'/name,primary/name)
    value,_,_,_=cli('source_only_complete_native_and_primary',['source-only',*nativeargs,'--primary-dir',primary],tool=subject)
    if value:result('native_exact_pair_statement_absence',value.get('canonical_pair')==dict(bytes=3524,sha256='b27d5dbb0f92c0ab330bf44891ec4467f7d8c593cef610196cbd82d4cc6d5298') and value.get('statement')==dict(bytes=183,sha256='a8224e60e73ef6f78e8af57e836e4cc5246a0b1cd12d1af10393d8fd0104149e') and value.get('target_report')=='ABSENT')
    # Independent instrumentation tests order on actual complete corpora.
    events=[];oldpin=m.stream_pin;oldparse=m.strict_json
    def trackpin(path,*args):
        events.append('pin-start:'+path.name);v=oldpin(path,*args);events.append('pin-done:'+path.name);return v
    def trackparse(raw):events.append('parse');return oldparse(raw)
    m.stream_pin=trackpin;m.strict_json=trackparse
    try:
        value=m.source_only(native)
        result('native_all_three_complete_before_first_parse',events[:7]==['pin-start:catalog.json','pin-done:catalog.json','pin-start:problems.json','pin-done:problems.json','pin-start:research_results.json','pin-done:research_results.json','parse'],events)
    finally:m.stream_pin=oldpin;m.strict_json=oldparse
    bad=TMP/'bad-native.json';bad.write_bytes(b'{bad')
    for i in range(3):
        vals=list(native);vals[i]=bad;events=[];m.stream_pin=trackpin;m.strict_json=trackparse
        try:
            try:m.source_only(vals)
            except Exception as e:result('native_bad_corpus_%d_no_parse'%i,'parse' not in events,dict(events=events,reason=str(e)))
            else:result('native_bad_corpus_%d_no_parse'%i,False,'accepted')
        finally:m.stream_pin=oldpin;m.strict_json=oldparse
        cli('source_only_bad_corpus_actual_%d'%i,['source-only','--catalog',vals[0],'--problems',vals[1],'--reports',vals[2]],tool=subject,accepted=False)
    # Native/primary output-parent guard applies even when otherwise unindexed.
    cli('receipt_inside_native_parent',['verify',PIN,'--root',baseline,*nativeargs,'--receipt-dir',native[0].parent/'review-forbidden-receipt'],tool=subject,accepted=False)
    cli('build_inside_native_parent',['build',PIN,native[0].parent/'post-lie-verification.zip','--root',baseline,*nativeargs],tool=subject,accepted=False)
    cli('receipt_inside_primary',['verify',PIN,'--root',baseline,'--primary-dir',primary,'--receipt-dir',primary/'forbidden'],tool=subject,accepted=False)
    cli('build_inside_primary',['build',PIN,primary/'post-lie-verification.zip','--root',baseline,'--primary-dir',primary],tool=subject,accepted=False)
    checkpoint(90,'Independent runtime, hostile capability control, native complete-before-parse ordering, exact pair/statement and optional primary inventory tests completed. Awaiting final issue disposition and public manifest.')
    save('SUMMARY.json',dict(timestamp_utc=stamp(),tests=len(RESULTS),passed=sum(r['passed'] for r in RESULTS),failed=sum(not r['passed'] for r in RESULTS),processes=SEQ,tool_sha256=TOOL_PIN,original_effort='1/5',scope='Independent format/CLI/runtime audit only; no mathematics, priority or actual paper acceptance'))
    print(json.dumps(dict(tests=len(RESULTS),passed=sum(r['passed'] for r in RESULTS),failed=sum(not r['passed'] for r in RESULTS),processes=SEQ)),flush=True)

if __name__=='__main__':
    try:main()
    except BaseException:
        failure=traceback.format_exc()
        with (HERE/'HARNESS_FAILURES.txt').open('a') as f:f.write(stamp()+'\n'+failure+'\n')
        print(failure,flush=True);raise
