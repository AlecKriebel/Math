#!/usr/bin/env python3
"""Independent read-only PR110 preservation/custody audit; outputs only here.

No queue execution, service request, export or Git mutation. Actual Git object
reads are bounded, journaled, killed and reaped on failure. This program does
not load the prepared native/action sources to obtain their conclusions.
"""
import argparse, base64, collections, csv, datetime, difflib, hashlib, io, json
import os, pathlib, selectors, signal, sqlite3, stat, subprocess, sys, time
A=pathlib.Path('/Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr85_30001203/isolated_main_integration_20261005/checkout/draft_pr_publication_program_20260930/audits/pr110_5100032')
C=A.parents[2]; W=A/'actual_native_candidate_adversary_20261006'
PACKET=A/'native_actual_input_preparation_20261006/root_fresh_native_preflight_20261006/EXECUTION_INPUTS.json'
PACKET_SHA='d9eb646c1dd70e891cc44bcaa5de2b62fc0c5a6eabdf2d487a148c3d3cc02281'
PHASE=A/'native_acceptance_merge_preparation_20261006'
PHASE_SHA='be4b56c47af3965bba42c4652375f85e74ef02a9658c2e27b27ef45b66766ec3'
K='5100032'; PREFIX='unsolved_math_prioritization/attempts/'+K+'/'
HEAD='3d159f0a00d0bd7ff8d558d6fbc75af5094f7a35'
NAMES=['queue.py','manifest.json','policy.json','catalog.json','assessments.json','state.json','history.jsonl','assessment_history.jsonl','ranking.csv','summary.json','SHORTLIST.md','QUEUE.md']
DERIVED=set(NAMES)-{'queue.py','manifest.json','policy.json','SHORTLIST.md'}
checks=0; journal=[]
def check(ok,message):
    global checks
    checks+=1
    if not ok:raise RuntimeError(message)
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def stamp(s):return datetime.datetime.fromisoformat(s.replace('Z','+00:00'))
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(b):return {'bytes':len(b),'sha256':sha(b)}
def canon(x):return (json.dumps(x,sort_keys=True,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode()
def ordered(x):
    if isinstance(x,dict):return ('dict',[(k,ordered(v)) for k,v in x.items()])
    if isinstance(x,list):return ('list',[ordered(v) for v in x])
    return (type(x).__name__,json.dumps(x,ensure_ascii=False,allow_nan=False))
def obj(b):
    def pairs(items):
        d={}
        for k,v in items:check(k not in d,'Duplicate JSON key');d[k]=v
        return d
    def bad(s):raise ValueError('Nonfinite JSON '+s)
    return json.loads(b,object_pairs_hook=pairs,parse_constant=bad)
def regular(path,expected=None,retain=True,cap=256*1024*1024):
    path=pathlib.Path(path);check(path.is_absolute() and '..' not in path.parts,'Absolute nonescaping path')
    for parent in [path,*path.parents]:check(not parent.is_symlink(),'Symlink audit input')
    fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW)
    try:
        st=os.fstat(fd);check(stat.S_ISREG(st.st_mode) and st.st_nlink==1 and st.st_size<=cap,'Regular unique-link bounded input')
        h=hashlib.sha256();count=0;parts=[]
        while True:
            b=os.read(fd,1024*1024)
            if not b:break
            count+=len(b);check(count<=cap,'Read grew beyond cap');h.update(b)
            if retain:parts.append(b)
        end=os.fstat(fd);check((st.st_ino,st.st_dev,st.st_size,st.st_mtime_ns)==(end.st_ino,end.st_dev,end.st_size,end.st_mtime_ns) and count==end.st_size,'Input changed during full read')
        actual={'bytes':count,'sha256':h.hexdigest()}
        if expected is not None:check(actual=={k:expected[k] for k in ['bytes','sha256']},'Full file pin drift '+str(path))
        return b''.join(parts) if retain else actual
    finally:os.close(fd)
def audit(spec):return regular(A/spec['path'],spec,cap=8*1024*1024)
def save(name,value):
    target=W/name;check(not target.exists(),'Unique independent output')
    with target.open('xb') as f:f.write(canon(value));f.flush();os.fsync(f.fileno())
def git_blob(p,name):
    rt=p['runtime'];env=dict(rt['python_environment']);env.update(GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL='/dev/null',GIT_CONFIG_SYSTEM='/dev/null',GIT_OPTIONAL_LOCKS='0',GIT_NO_REPLACE_OBJECTS='1',GIT_TERMINAL_PROMPT='0')
    argv=[rt['binaries']['git']['resolved_absolute_path'],'-c','core.fsmonitor=false','-c','core.hooksPath=/dev/null','-c','credential.helper=','show',p['main_parent']+':unsolved_math_prioritization/'+name]
    started=now();mono=time.monotonic();proc=subprocess.Popen(argv,cwd=C,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
    sel=selectors.DefaultSelector();out=bytearray();err=bytearray();reason=None
    for label,s in [('stdout',proc.stdout),('stderr',proc.stderr)]:os.set_blocking(s.fileno(),False);sel.register(s,selectors.EVENT_READ,label)
    try:
        while sel.get_map() or proc.poll() is None:
            if time.monotonic()-mono>30:reason='deadline';raise RuntimeError(reason)
            for key,_ in sel.select(.1):
                b=os.read(key.fileobj.fileno(),65536)
                if not b:sel.unregister(key.fileobj);continue
                buf=out if key.data=='stdout' else err;buf.extend(b)
                if len(buf)>(32*1024*1024 if key.data=='stdout' else 65536):reason='stream_cap';raise RuntimeError(reason)
        proc.wait(timeout=3)
    except BaseException:
        try:os.killpg(proc.pid,signal.SIGKILL)
        except ProcessLookupError:pass
        proc.wait(timeout=3);raise
    finally:
        sel.close();proc.stdout.close();proc.stderr.close()
        journal.append({'actual_PID':proc.pid,'argv':argv,'cwd':str(C),'environment_sha256':sha(canon(env)),'UTC_start':started,'UTC_end':now(),'exit_code':proc.returncode,'reaped':proc.returncode is not None,'termination_reason':reason,'full_observed_stdout':pin(bytes(out)),'full_observed_stderr':pin(bytes(err)),'immutable_body_source':p['main_parent']+':unsolved_math_prioritization/'+name})
    check(proc.returncode==0 and not err,'Successful genuine Git object read');return bytes(out)
def prepare(p):
    check(sha(regular(PACKET))==PACKET_SHA and regular(PACKET)==canon(p),'Exact canonical actual packet')
    check(p['main_parent']=='f9f840d21305bdc353d151abe8dd5c51b6a27dd6' and p['identity']['original_head']==HEAD,'Packet identity/current parent')
    check(p['identity']['literal_status']=='claimed_solved' and p['identity']['turns_used']==2 and p['identity']['new_central_proof_search_turns']==0,'Honest effort')
    check(len(p['input_files'])==182 and len({s['path'] for s in p['input_files']})==182,'Exact unique input registry')
    for s in p['input_files']:audit(s)
    for s in p['program_files'].values():audit(s)
    manifest=obj(regular(PHASE/'OUTPUT_MANIFEST.json'));seal=obj(regular(PHASE/'SEAL_RECEIPT.json'))
    check(pin(regular(PHASE/'OUTPUT_MANIFEST.json'))==seal['manifest_pin'],'Phase seal/manifest')
    check(manifest['file_count']==11 and len(manifest['files'])==11,'Complete sealed phase source')
    for s in manifest['files']:regular(PHASE/s['path'],s)
    check(sha(regular(PHASE/'native_acceptance_actions.py'))==PHASE_SHA,'Exact executing phase source')
    original=obj(audit(p['original']['manifest']));check(original['file_count']==17 and original['original_budget']=='2/5' and original['original_head']==HEAD,'Original manifest')
    for s in original['files']:
        b=audit(p['original']['files'][s['relative_path']]);check(pin(b)=={k:s[k] for k in ['bytes','sha256']},'Original full body');check(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==s['git_blob_oid'],'Original Git object identity')
    source=audit(p['original']['files']['source_record.json']);prior=audit(p['original']['files']['prior_imported_report.json'])
    check(bool(obj(prior)) and len(prior)==2977,'Nonempty original prior')
    check(sha(obj(source)['statement'].encode())==p['identity']['statement_hash'],'Complete target wording hash')
    check(sha(json.dumps([obj(source),obj(prior)],sort_keys=True).encode())==p['identity']['review_hash'],'Exact full sourcepair hash')
    cache=p['source_cache'];regular(cache['absolute_path'],cache['pin'],retain=False)
    for suffix in ['-wal','-shm','-journal']:check(not os.path.lexists(cache['absolute_path']+suffix),'No SQL writer sidecar')
    db=sqlite3.connect('file:'+cache['absolute_path']+'?mode=ro&immutable=1',uri=True)
    try:
        check(db.execute('SELECT revision FROM metadata').fetchone()==(p['identity']['dataset_revision'],),'SQL revision')
        check(db.execute('SELECT count(*) FROM records').fetchone()[0]==15458,'SQL count')
        row=db.execute('SELECT payload,report FROM records WHERE key=?',(K,)).fetchone();check(obj(row[0])==obj(source) and obj(row[1])==obj(prior),'SQL complete sourcepair equals immutable original')
    finally:db.close()
    for name,s in p['raw_source_pins'].items():regular(pathlib.Path(cache['absolute_path']).parent/name,s,retain=False)
    pub=obj(audit(p['publication_receipt']));sheet=obj(audit(p['sheet_receipt']))
    check(pub['published'] is True and pub['DOI']=='10.5281/zenodo.23191247','Actual published record identity')
    check(sheet['DOI']==pub['DOI'] and sheet['range']=="'Math Puzzles'!A32:D32" and sheet['values'][2]=='https://doi.org/'+pub['DOI'],'Actual tracker target')
    check(len(pub['logical_readbacks'])==33,'All thirty-three publication bodies')
    for name,s in p['package']['logical_inventory'].items():check(audit(s)==audit(pub['logical_readbacks'][name]['body']),'Actual complete published logical body')
    for role,r in sheet['processes'].items():
        raw=obj(audit(r['stdout']));check(r['exit_code']==0 and r['reaped'] and r['termination_reason'] is None,'Actual successful GWS envelope')
        if role in ['readback','independent_readback']:check(raw['values']==[sheet['values']] and raw['range']==sheet['range'],'Actual full tracker row readback')
    before={name:git_blob(p,name) for name in NAMES}
    for name,b in before.items():check(pin(b)=={k:p['native_baseline'][name][k] for k in ['bytes','sha256']},'Full immutable native baseline')
    baseline=obj(before['catalog.json']);target=next(r for r in baseline if r['id']==K)
    check(target['local_status']=='queued' and target['turns_used']==0 and K not in obj(before['state.json']),'Genuine queued zero-turn baseline')
    return before
def csv_rows(body):
    text=body.decode();lines=text.splitlines(keepends=True);reader=csv.reader(io.StringIO(text,newline=''),strict=True);rows=[];start=0
    for fields in reader:
        end=reader.line_num;rows.append((fields,''.join(lines[start:end]).encode()));start=end
    check(start==len(lines),'Independent CSV physical span coverage');return rows
def actual(p,before,candidate):
    # Filled only for genuine supplied output; never creates a candidate or gate.
    r=obj(regular(candidate/'CANDIDATE_RECEIPT.json'));check(r['schema']=='pr110-actual-private-native-candidate/v1' and r['packet_sha256']==PACKET_SHA,'Actual candidate identity')
    check(candidate==A/'native_execution_programs_v1/workspaces'/('candidate_'+PACKET_SHA[:16]),'Exact exclusive candidate')
    check(r['main_parent']==p['main_parent'] and r['original_head']==HEAD and not r['native_export_executed'] and r['Git_mutations']==0 and r['service_writes']==0,'Private-only actual candidate')
    check(regular(candidate/'EXECUTION_INPUTS.json')==regular(PACKET),'Staged immutable actual packet')
    for name,s in p['program_files'].items():check(regular(candidate/name)==audit(s),'Staged exact four sources')
    control_b=regular(candidate/'WORKER_CONTROL.json');control=obj(control_b);worker=obj(regular(candidate/'WORKER_RESULT.json'))
    check(worker['outcome']=='success' and worker['native_assess_call_attempted'] is True and worker['native_assess_completed'] is True,'Literal native assess completed')
    check(worker['actual_worker_PID']==r['native_assess_actual_PID'] and worker['control_sha256']==sha(control_b) and worker['validated_control']==control,'Actual worker/control correspondence')
    check(control['resources']==p['resources'] and control['fixture'] is False and set(control['pre_assess_pins'])==set(NAMES)|{'assessment.json'},'Complete genuine thirteen-preimage worker control')
    oldstates=obj(before['state.json']);oldass=obj(before['assessments.json']);overlay=p['assessment_overlay']
    after={name:regular(candidate/'private_native_backend'/name,worker['output_pins'][name]) for name in NAMES}
    event=obj(regular(candidate/'offer'/PREFIX/'IMPORT_BASELINE.json'))
    check(event['at']==p['import_UTC'] and event['event']=='dated_import_of_authenticated_author_count' and event['turns_used']==2 and event['status']=='claimed_solved' and event['original_structured_ledger_present'] is False and event['new_central_proof_search_turns']==0,'One honest dated two-turn import event')
    expected_state={**oldstates,K:event};expected_hist=before['history.jsonl']+json.dumps(event,ensure_ascii=False).encode()+b'\n'
    for name in NAMES:
        pre=before[name]
        if name=='state.json':pre=(json.dumps(expected_state,ensure_ascii=False,indent=2)+'\n').encode()
        if name=='history.jsonl':pre=expected_hist
        check(control['pre_assess_pins'][name]==pin(pre),'Actual pre-assess full pin independently derived '+name)
    check(control['pre_assess_pins']['assessment.json']==pin(canon({**oldass[K],**overlay})),'Exact reviewed metadata-only assessment input')
    for name in ['queue.py','manifest.json','policy.json']:check(after[name]==before[name],'Immutable native runtime input')
    newstates=obj(after['state.json']);check(ordered(newstates)==ordered(expected_state),'All state objects and key order preserved, with one import')
    check(after['history.jsonl']==expected_hist,'Full history prefix and exactly one honest import')
    newass=obj(after['assessments.json']);check(list(newass)==list(oldass),'All assessment outer key order')
    for key in oldass:
        if key!=K:check(ordered(newass[key])==ordered(oldass[key]),'Unrelated assessment full object/key order')
    expected={**oldass[K],**overlay};check(canon({k:v for k,v in newass[K].items() if k!='reviewed_at'})==canon({k:v for k,v in expected.items() if k!='reviewed_at'}),'Target changes only reviewed descriptive metadata')
    check(stamp(worker['UTC_start'])<=stamp(newass[K]['reviewed_at'])<=stamp(worker['UTC_end']),'Actual assessment timestamp lies inside worker')
    suffix=after['assessment_history.jsonl'][len(before['assessment_history.jsonl']):]
    check(after['assessment_history.jsonl'].startswith(before['assessment_history.jsonl']) and len(suffix.splitlines())==1 and obj(suffix)=={'id':K,**newass[K]},'Full assessment history prefix and exactly one current target event')
    offered={x['path']:regular(candidate/'offer'/x['path'],x['after']) for x in r['affected_paths']}
    check(len(offered)==len(r['affected_paths']) and len(offered)<=256,'Unique complete offered path set')
    found={str(f.relative_to(candidate/'offer')) for f in (candidate/'offer').rglob('*') if f.is_file()};check(found==set(offered),'No missing or extra offer member')
    for name,s in p['attempt_offer_sources'].items():check(offered[name]==audit(s),'Every authenticated source offer preserved exactly')
    generated=['IMPORT_BASELINE.json','HISTORICAL_DESK_ASSESSMENT.json','assessment.json','PUBLICATION_EVIDENCE.json','ACCEPTANCE_EVIDENCE.json','README.md','RESEARCH_LOG.md']
    check(set(offered)==set(p['attempt_offer_sources'])|{'unsolved_math_prioritization/'+n for n in DERIVED if after[n]!=before[n]}|{PREFIX+n for n in generated},'Exact reviewed target/generated/eight-global offer')
    oldcat=obj(before['catalog.json']);newcat=obj(offered['unsolved_math_prioritization/catalog.json']);check([x['id'] for x in oldcat]==[x['id'] for x in newcat],'All catalog physical list positions')
    generated_cat=obj(after['catalog.json']);generated_map={x['id']:x for x in generated_cat};check(len(generated_map)==len(generated_cat)==len(oldcat) and set(generated_map)=={x['id'] for x in oldcat},'Actual native regeneration complete identity set')
    explained=[]
    for old in oldcat:
        g=generated_map[old['id']]
        if old['id']==K:continue
        changed={key for key in set(old)|set(g) if key not in old or key not in g or ordered(old[key])!=ordered(g[key])}
        check(changed<={'rank','local_status','turns_used','eligible'},'Native regeneration did not change unrelated scores/source/metadata')
        if changed-{'rank'}:
            st=newstates.get(old['id'],{});assessment=newass.get(old['id'],{})
            if old['present']:
                default='queued' if assessment.get('decision')=='candidate' else 'deferred' if assessment.get('decision') in ['defer','exclude'] else 'unreviewed'
                if default=='queued' and old['holds']:default='unreviewed'
                if assessment.get('resolution')=='already_solved' and assessment.get('review_hash')==old['review_hash']:default='already_solved'
                status=st.get('status',default);turns=st.get('turns_used',0)
            else:status=st.get('status',old['local_status']);turns=old['turns_used']
            eligible=bool(old['present'] and not old['holds'] and status in ['queued','unreviewed','ready'] and turns<5)
            check(g['local_status']==status and type(g['turns_used']) is int and g['turns_used']==turns and g['eligible'] is eligible,'Each restored unrelated projection drift has an exact native explanation')
            explained.append({'id':old['id'],'fields':sorted(changed),'baseline_preserved':True})
    check(r['unrelated_projection_drift_restored']==explained,'Every reported unrelated projection restoration independently reproduced')
    for x,y in zip(oldcat,newcat):
        if x['id']!=K:check(ordered(x)==ordered(y),'Full unrelated catalog object/key/score/rank preservation')
        else:
            allowed={'local_status','turns_used','eligible','rank','desk_note'}
            check(ordered({k:v for k,v in x.items() if k not in allowed})==ordered({k:v for k,v in y.items() if k not in allowed}),'Target source/score/holds/metadata preserved')
            check(list(x)==list(y) and y['local_status']=='claimed_solved' and y['turns_used']==2 and y['eligible'] is False and y['rank'] is None and y['desk_note']==overlay['note'],'Target scoped native projection')
    oldcsv=csv_rows(before['ranking.csv']);newcsv=csv_rows(offered['unsolved_math_prioritization/ranking.csv']);check(len(oldcsv)==len(newcsv) and oldcsv[0]==newcsv[0],'CSV header/count')
    columns=oldcsv[0][0];idcol=columns.index('id');target_count=0
    for old,new in zip(oldcsv[1:],newcsv[1:]):
        check(old[0][idcol]==new[0][idcol],'All physical CSV row positions')
        if old[0][idcol]!=K:check(old[1]==new[1],'Every unrelated CSV physical byte')
        else:
            target_count+=1;d0=dict(zip(columns,old[0]));d1=dict(zip(columns,new[0]));allowed={'local_status','turns_used','eligible','rank','desk_note'}
            check({k:v for k,v in d0.items() if k not in allowed}=={k:v for k,v in d1.items() if k not in allowed},'Target CSV scores/source fields retained')
            check(d1['local_status']=='claimed_solved' and d1['turns_used']=='2' and d1['eligible']=='False' and d1['rank']=='' and d1['desk_note']==overlay['note'],'Target CSV projection')
    check(target_count==1,'Exactly one target CSV row')
    oldqueue=before['QUEUE.md'].splitlines(keepends=True);newqueue=offered['unsolved_math_prioritization/QUEUE.md'].splitlines(keepends=True);check(len(oldqueue)==len(newqueue),'Full campaign line count')
    qchanges=[]
    for i,(old,new) in enumerate(zip(oldqueue,newqueue)):
        if old==new:continue
        qchanges.append(i);cells0=old.decode().split('|');cells1=new.decode().split('|');check(cells0[2].strip()==K+' / AMR-050-0032','Only target campaign row')
        check([v for j,v in enumerate(cells0) if j not in {8,9,11,12}]==[v for j,v in enumerate(cells1) if j not in {8,9,11,12}],'Campaign separate scores/rank/fields preserved')
        check(cells1[8].strip()=='claimed_solved' and cells1[9].strip()=='2/5' and cells1[11].strip()==p['campaign_note'] and cells1[12].strip()=='https://doi.org/10.5281/zenodo.23191247','Exact reviewed campaign delta')
    check(len(qchanges)==1,'Exactly one campaign line changed')
    check('unsolved_math_prioritization/SHORTLIST.md' not in offered,'Old SHORTLIST is not exported')
    oldsummary=obj(before['summary.json']);summary=obj(offered['unsolved_math_prioritization/summary.json'])
    check(list(summary)==list(oldsummary),'Summary top-level key order')
    for k in oldsummary:
        if k not in {'records','eligible','assessed','holds'}:check(ordered(summary[k])==ordered(oldsummary[k]),'Unrelated summary metadata retained')
    check(summary['records']==15458 and summary['assessed']==len(newass) and summary['eligible']==sum(x['eligible'] for x in newcat) and summary['holds']==dict(collections.Counter(h.split(':')[0] for x in newcat for h in x['holds'])),'Scoped summary derived from offered full catalog')
    # Independently reconstruct complete representation, including genuine binary additions.
    diff=[]
    for row in r['affected_paths']:
        name=row['path'];body=offered[name];old=before.get(name.removeprefix('unsolved_math_prioritization/')) if name in {'unsolved_math_prioritization/'+n for n in NAMES} else None
        check(row['before']==(None if old is None else pin(old)),'Every offered committed preimage pin')
        try:oldlines=[] if old is None else old.decode().splitlines(keepends=True);newlines=body.decode().splitlines(keepends=True)
        except UnicodeDecodeError:
            check(old is None,'Only new binary additions');diff.append(('Complete new binary addition '+name+' '+json.dumps(pin(body),sort_keys=True)+'\n'+base64.b64encode(body).decode()+'\n').encode());continue
        for line in difflib.unified_diff(oldlines,newlines,fromfile='/dev/null' if old is None else 'a/'+name,tofile='b/'+name):
            if not line.endswith('\n'):line+='\n\\ No newline at end of file\n'
            diff.append(line.encode())
    expected_diff=b''.join(diff);check(regular(candidate/'DIFF.txt',r['DIFF_pin'])==expected_diff and len(expected_diff)<=1024*1024,'Full untruncated DIFF independently reconstructed')
    return {'candidate_receipt_pin':pin(regular(candidate/'CANDIDATE_RECEIPT.json')),'DIFF_pin':pin(expected_diff),'offered_files':len(offered),'unrelated_catalog_records_preserved':len(oldcat)-1,'unrelated_assessments_preserved':len(oldass)-1,'unrelated_physical_CSV_rows_preserved':len(oldcsv)-2,'native_process_and_outer_custody':'Requires separately supplied actual outer receipt and independent final audit'}
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--candidate',type=pathlib.Path);parser.add_argument('--label',required=True);args=parser.parse_args();started=now()
    try:
        p=obj(regular(PACKET));before=prepare(p);result={'preparatory_full_inputs_and_baseline_authenticated':True,'candidate_audited':False,'execution_clearance':False}
        if args.candidate:result.update(actual(p,before,args.candidate));result['candidate_audited']=True
        result.update(schema='pr110-independent-actual-candidate-reproduction/v1',UTC_start=started,UTC_end=now(),actual_reviewer_PID=os.getpid(),checks=checks,packet_sha256=PACKET_SHA,action_source_sha256=PHASE_SHA,verification_source_pin=pin(pathlib.Path(__file__).read_bytes()),Git_mutations=0,native_assess_calls=0,service_calls=0)
        save(args.label+'_RESULT.json',result)
    finally:save(args.label+'_GIT_READ_JOURNAL.json',{'actual_reviewer_PID':os.getpid(),'UTC':now(),'processes':journal})
    print(json.dumps(result))
if __name__=='__main__':main()
