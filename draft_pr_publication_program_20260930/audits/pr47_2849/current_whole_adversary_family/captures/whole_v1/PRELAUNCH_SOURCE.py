"""Independent read-only whole frozen-packet/native/raw reconciliation; no production import."""
from pathlib import Path, PurePosixPath
import collections, datetime as dt, hashlib, json, math, os, stat, sqlite3, subprocess, sys, traceback
F=Path(__file__).absolute().parent; A=F.parent; R=A.parents[2]; C=A/'reviewed_candidate'
assert __debug__ and not sys.flags.optimize
checks=0; readrows={}; nodecounts=collections.Counter(); commands=[]
def need(v,n):
    global checks
    if not v: raise AssertionError(n)
    checks+=1
def sha(b): return hashlib.sha256(b).hexdigest()
def enc(o): return (json.dumps(o,indent=2,allow_nan=False)+'\n').encode()
def utc(): return dt.datetime.now(dt.timezone.utc).isoformat()
def time(v):
    need(type(v) is str,'time string'); t=dt.datetime.fromisoformat(v.replace('Z','+00:00'))
    need(t.tzinfo is not None and t.utcoffset()==dt.timedelta(0),'aware UTC'); return t
def equal(a,b):
    if type(a) is not type(b): return False
    if type(a) is dict: return a.keys()==b.keys() and all(equal(a[k],b[k]) for k in a)
    if type(a) is list: return len(a)==len(b) and all(equal(x,y) for x,y in zip(a,b))
    return a==b
def parse(b):
    def pairs(items):
        o={}
        for k,v in items: need(k not in o,'duplicate JSON'); o[k]=v
        return o
    def floating(v):
        f=float(v); need(math.isfinite(f),'finite floating'); return f
    def bad(v): raise ValueError(v)
    return json.loads(b,object_pairs_hook=pairs,parse_constant=bad,parse_float=floating)
def visit(o):
    nodecounts[type(o).__name__]+=1
    if type(o) is dict:
        for k,v in o.items(): need(type(k) is str,'JSON key string'); visit(v)
    elif type(o) is list:
        for v in o: visit(v)
    else: need(type(o) in [str,int,float,bool,type(None)],'JSON scalar type')
def path(n):
    need(type(n) is str and n and '\\' not in n and '\0' not in n,'POSIX string')
    p=PurePosixPath(n); need(not p.is_absolute() and str(p)==n and not {'.','..','.git','__pycache__'}.intersection(p.parts),'canonical safe path'); return n
def read(p):
    need(not p.is_symlink() and all(not q.is_symlink() for q in p.parents) and stat.S_ISREG(p.stat().st_mode),'regular nonsymlink body')
    b=p.read_bytes(); row={'path':str(p),'bytes':len(b),'sha256':sha(b),'full_mode':stat.S_IMODE(p.stat().st_mode)}
    if str(p) in readrows: need(equal(readrows[str(p)],row),'repeated full body/mode unchanged')
    readrows[str(p)]=row; return b
def jsonread(p):
    o=parse(read(p)); visit(o); return o
def bind(root,row,full=False):
    need(type(row) is dict and type(row['bytes']) is int and row['bytes']>=0 and type(row['sha256']) is str and len(row['sha256'])==64,'typed row'); p=root/path(row['path']); b=read(p)
    need(len(b)==row['bytes'] and sha(b)==row['sha256'],'complete pinned bytes')
    if full:
        mode=row['full_mode']; need(type(mode) is int and 0<=mode<4096 and stat.S_IMODE(p.stat().st_mode)==mode,'fullmode typed')
    return b
def topo(root):
    need(root.is_dir() and not root.is_symlink() and all(not q.is_symlink() for q in root.parents),'regular root'); fs=set(); ds=set()
    for p in root.rglob('*'):
        need(not p.is_symlink(),'no member symlink'); n=path(p.relative_to(root).as_posix()); mode=p.stat().st_mode
        if stat.S_ISREG(mode): fs.add(n)
        else: need(stat.S_ISDIR(mode),'no special member'); ds.add(n)
    need(ds=={str(q) for n in fs for q in PurePosixPath(n).parents if str(q)!='.'},'exact noempty parent topology')
    return fs,ds
def closure(root,name,pin,count,dirs):
    body=read(root/name); need(sha(body)==pin,'closed manifest pin'); m=parse(body); visit(m)
    need(len(m['files'])==count,'closed count')
    fs,ds=topo(root); need(fs=={r['path'] for r in m['files']}|{name} and len(ds)==dirs,'self-only family topology')
    for row in m['files']: bind(root,row); need(stat.S_IMODE((root/row['path']).stat().st_mode)==0o444,'full0444 member')
    need(stat.S_IMODE((root/name).stat().st_mode)==0o444,'full0444 self')
    return m
def git(argv):
    d=F/'private_git'/str(len(commands)); d.mkdir(parents=True,exist_ok=False)
    (d/'PRELAUNCH_OPERATOR.py').write_bytes(Path(__file__).read_bytes())
    rec={'argv':['git',*argv],'cwd':str(R),'operator_pid':os.getpid(),'started_utc':utc(),'source':None,'source_unchanged':None,'actual_execution':False,'completed':False,'pid':None,'exit_code':None,'stdin_supplied':False}
    (d/'PRELAUNCH.json').write_bytes(enc(rec))
    try:
        with (d/'stdout.bin').open('xb') as out,(d/'stderr.bin').open('xb') as err:
            child=subprocess.Popen(rec['argv'],cwd=R,stdin=subprocess.DEVNULL,stdout=out,stderr=err,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0')); rec.update(actual_execution=True,pid=child.pid)
            try: rec['exit_code']=child.wait(timeout=60); rec['completed']=True
            except BaseException: child.kill(); rec['exit_code']=child.wait(); raise
    except BaseException: rec['failure']=traceback.format_exc(); raise
    finally:
        rec['finished_utc']=utc()
        for k in ['stdout','stderr']:
            p=d/(k+'.bin')
            if p.exists(): b=p.read_bytes(); rec[k]={'path':p.relative_to(F).as_posix(),'bytes':len(b),'sha256':sha(b)}
        (d/'CAPTURE.json').write_bytes(enc(rec)); commands.append(rec)
    need(rec['completed'] is True and type(rec['exit_code']) is int and rec['exit_code']==0 and (d/'stderr.bin').read_bytes()==b'','actual read-only Git complete')
    return (d/'stdout.bin').read_bytes()
m=closure(C,'MANIFEST.json','a7d1acc9dbbf8cd5435d0bebd8f6b1a540ecb0f2aea8d0c616c46bc5bf6b4ea5',1328,282)
need(m['self_excluded']==['MANIFEST.json'] and m['status']=='unsolved' and m['full_problem_solved'] is False and m['novelty_claimed'] is False,'current scope')
for row in m['files']:
    p=C/row['path']
    if p.suffix=='.json': jsonread(p)
dep=jsonread(C/'CURRENT_DEPENDENCIES.json'); need(dep['anchor']=='repository_root' and len(dep['files'])==1422,'repo root 1422 deps')
for row in dep['files']: bind(R,row,True)
prep=closure(A/'current_preparation_family_v2','PREPARATION_MANIFEST.json','da314f40d628606f8e80cc198c3ab4a94b71554e929f70c63fce31cc195def10',139,16)
ar=jsonread(A/'ROOT_NEW_SOURCE_ADVERSARY_RECORD.json')
reviewroot=A/Path(ar['manifest']['path']).parent
sourcead=closure(reviewroot,Path(ar['manifest']['path']).name,ar['manifest']['sha256'],263,len(jsonread(reviewroot/Path(ar['manifest']['path']).name)['directories']))
pins=jsonread(A/'current_preparation_family_v2/STATIC_INPUT_BINDINGS.json')
for group,info in pins['groups'].items():
    mr=info['manifest']; mb=bind(R,mr,True); old=parse(mb); visit(old); root=(R/mr['path']).parent
    for row in info['members']: bind(R,row,True)
    if group=='original':
        fs=set(info['authorship_root_files']); ds=set()
        for dn in info['authorship_directory_roots']:
            sub,subdirs=topo(A/dn); fs|={dn+'/'+n for n in sub}; ds|={dn}|{dn+'/'+n for n in subdirs}
        need(fs=={str(PurePosixPath(r['path']).relative_to(root.relative_to(R))) for r in info['members']} and len(ds)==55 and len(old['files'])==301,'original scoped301/55')
    else:
        expected=(143,23) if group=='cover_algebra_family' else (71,15)
        closure(root,Path(mr['path']).name,mr['sha256'],*expected)
    for row in info['directories']: need(stat.S_IMODE((root/row['path']).stat().st_mode)==row['full_mode'],'exact family directorymode')
for row in pins['separate_original_and_ROOT_actual_captures']: bind(R,row,True)
repair=jsonread(A/'current_preparation_family_v2/SOURCE_V1_REPAIR_BINDINGS.json')
for group,info in repair['closed_groups'].items():
    mr=info['manifest']; old=jsonread(R/mr['path']); closure((R/mr['path']).parent,Path(mr['path']).name,mr['sha256'],len(old['files']),len(info['directories']))
for key in ['complete_fixed_member_reads','external_ROOT_closure_and_readback_members','qualified_current_packet_exports']:
    for row in repair[key]: bind(R,row,True)
rootfixed=jsonread(A/'current_preparation_family_v2/ROOT_FIXED_EVIDENCE.json')
closure(A/'root_original_actual_reproduction','MANIFEST.json','71109d8643eeff305b9e8200e2e7be0e62e79ad1cc7ad8a22b4456f5a108d278',219,46)
for key in ['members','separate_actual_closure_members']:
    for row in rootfixed[key]: bind(R,row,True)
snap=jsonread(A/'snapshot_manifest.json'); original={}; head=snap['head']; base=snap['merge_base']
for row in snap['files']:
    n=row['relative_path']; b=read(A/'source_snapshot'/n); original[n]=b
    need(b==read(C/'original_archive'/n),'every original archive byte')
    need(git(['show',head+':'+row['path']])==b,'new complete Git body')
    need(git(['ls-tree',head,'--',row['path']]).decode().strip()=='100644 blob '+row['git_object']+'\t'+row['path'],'new Git blob/mode')
need(len(original)==16 and topo(C/'original_archive')[0]==set(original),'exact16 archive')
immutable=['verify.py','verification.json','source_checksums.json','source_record.json','turns.json','prior_report.json','review/independent_checks.py','review/independent_results.json','review/submitted_verify.py','review/submitted_results.json']
for n in immutable: need(read(C/n)==original[n],'ten operative immutable')
diff=read(C/'original_diff.patch'); need(git(['diff','--no-ext-diff','--no-textconv','--binary',base,head,'--'])==diff and len(diff)==59460 and sha(diff)=='17a6b488f85b54d22af865a5e0c9644b016211c3c985bd352631b46632dedc27','entire17 original diff')
meta=jsonread(A/'original_pr_metadata.json'); need(git(['diff','--name-only',base,head]).decode().splitlines()==[r['path'] for r in meta['all_changed_paths']],'all17 paths')
tree=git(['ls-tree','-r','-z',head,'--','unsolved_math_prioritization/attempts/2849/']).decode().split('\0')
need({v.split('\t')[1] for v in tree if v}=={r['path'] for r in snap['files']},'full scientific tree')
for n in ['status.json','readiness.json','review/verdict.json','review/review_summary.json']:
    o=jsonread(C/n)
    for k,v in {'status':'unsolved','original_substantive_attempts':1,'turn_limit':5,'new_substantive_attempts':0,'audit_turns':0,'full_problem_solved':False,'novelty_claimed':False,'universal_normal_vanishing_false':True,'realized_example_instanton_rank_computed':False,'current_verdict':None,'current_model':None,'current_reasoning_effort':None,'current_deadline_utc':None,'paper_created':False,'new_DOI_created':False,'tracker_row_created':False,'old_review_PASS_transferred':False}.items():need(equal(o[k],v),'typed global status '+k)
ledger=parse(original['turns.json']); need(type(ledger) is dict and type(ledger['count']) is int and ledger['count']==1 and len(ledger['attempts'])==1,'one original object turn')
for n in ['README.md','PR_DRAFT.md','pr_body.md','CURRENT_CONTEXT.md','CURRENT_REVIEW_CONTEXT.md','OBSTRUCTION.md','REALIZED_DEGENERACY_PROOF.md','SOURCE_PROVENANCE_CORRECTION.md','SOURCE_PRECISION_QUALIFICATIONS.md']:
    b=read(C/n).decode(); need('Sivek' in b and 'Zentner' in b and 'Proposition6.1' in b and 'UNSOLVED' in b and 'not a counterexample' in b and 'not computed' in b,'globally qualified scientific copy '+n)
native4=['unsolved_math_prioritization/QUEUE.md','unsolved_math_prioritization/state.json','unsolved_math_prioritization/history.jsonl','draft_pr_publication_program_20260930/inventory.json']
fresh=jsonread(A/'ROOT_CURRENT_INPUT_PREIMAGES.json'); need(fresh['current_head']==dep['current_main_head'],'dated HEAD binding')
dated=fresh['current_head']; proposals={}
for n in native4:
    label=n.replace('/','__'); pre=read(C/'native4_proposal/preimage'/label); after=read(C/'native4_proposal/prospective'/label); proposals[n]=(pre,after)
    need(git(['show',dated+':'+n])==pre,'dated committed native4 fullbody'); git(['ls-tree',dated,'--',n])
    if not n.endswith('QUEUE.md'): need(after==pre,'state history inventory unchanged')
pre,after=proposals[native4[0]]; beforelines=pre.splitlines(keepends=True); afterlines=after.splitlines(keepends=True)
need(len(beforelines)==len(afterlines),'queue same line count'); hits=[]
for i,(x,y) in enumerate(zip(beforelines,afterlines)):
    if x!=y: hits.append((i,x,y))
need(len(hits)==1,'onlyone target row change'); old,new=hits[0][1:]; xs=old.decode().split('|'); ys=new.decode().split('|')
need(xs[2].strip()=='2849 / KP-3.51' and xs[8].strip()=='queued' and xs[9].strip()=='0/5' and ys[8].strip()=='unsolved' and ys[9].strip()=='1/5','exacttargetnamedcells')
need(all(x==y for i,(x,y) in enumerate(zip(xs,ys)) if i not in {8,9,11}),'everyothercellChatDOI')
stable9=[r for r in fresh['files'] if r['path'] not in native4]; need(len(stable9)==9,'stable9count')
for row in stable9: bind(R,row,True)
live_head=git(['rev-parse','HEAD']).decode().strip(); need(git(['branch','--show-current']).strip()==b'main','live main')
# The completed ORIGINAL final inner/outer records are read only after exit.
ref=jsonread(C/'CURRENT_EXECUTION_REFERENCE.json'); outer=A/ref['audit_relative_outer_capture']; inner=A/ref['audit_relative_inner_attempt']
out=jsonread(outer/'CAPTURE.json'); prelaunch=jsonread(outer/'OPERATION_PRELAUNCH.json')
need(out['operator_pid']==53866 and out['pid']==53867 and out['completed'] is True and type(out['exit_code']) is int and out['exit_code']==0,'genuine actualcurrent PIDs/exit')
need(time(out['started_utc'])<=time(out['finished_utc'])<time(utc()),'current alreadyexited chronology')
for n,key,originaln in [('PRELAUNCH_BUILDER_SOURCE.py','builder_sha256','prepare_current_packet.py'),('PRELAUNCH_OPERATOR.py','operator_sha256','capture_root_builder_operation.py')]:
    b=read(outer/n); need(sha(b)==out[key] and b==read(A/'current_preparation_family_v2'/originaln),'exact current prelaunchsource')
for k in ['stdout','stderr']: bind(outer,out[k]); need(k!='stderr' or read(outer/out[k]['path'])==b'','actualsuccess fullstderr')
need(equal(prelaunch['argv'],out['argv']) and prelaunch['operator_pid']==out['operator_pid'],'outerprelaunch binding')
final=jsonread(inner/'GIT_COMMANDS.json'); prefix=jsonread(C/'build/actual_attempt_prepublication_prefix/GIT_COMMANDS.json')
need(len(final)==49 and len(prefix)==47 and equal(final[:47],prefix),'honest47prefix of49final')
inv=jsonread(inner/'INVOCATION.json'); need(inv['pid']==53867 and inv['parent_pid']==53866,'realinnerinvocation')
for cmd in final:
    need(cmd['actual_execution'] is True and cmd['completed'] is True and type(cmd['exit_code']) is int and cmd['exit_code']==0 and type(cmd['pid']) is int and cmd['pid']>0 and cmd['stdin_supplied'] is False,'final49actualcomplete')
    need(time(out['started_utc'])<=time(cmd['started_utc'])<=time(cmd['finished_utc'])<=time(out['finished_utc']),'final49UTCbounds')
    for k in ['stdout','stderr']: bind(inner,cmd[k]); need(k!='stderr' or read(inner/cmd[k]['path'])==b'','whole49stderr')
need(len({cmd['pid'] for cmd in final})==49,'49uniqueactualchildren')
inspection=jsonread(A/'ROOT_ACTUAL_CURRENT_FREEZE_INSPECTION.json')
need(inspection['verification_pid']==56799 and equal(inspection['complete_actual_outer_capture'],out) and equal(inspection['complete_final_original_inner_commands'],final),'distinctROOTfinalreconciliation')
failure=inspection['retained_initial_ROOT_inspector_failure']; need(failure['actual_pid']==56454 and 'full_problem_solved' in failure['reason'],'honestretainedinitialROOTfailure')
# Full in-place raw importer validation, saving no foreign body.
cache=R/'unsolved_math_prioritization/cache'; rb=read(cache/'problems.json'); pb=read(cache/'research_results.json'); raw=parse(rb); prior=parse(pb)
need(len(rb)+len(pb)==149266659 and len(raw)==15458 and len(prior)==6701,'fullraw/prior149M')
byid={str(z['id']):z for z in raw}; counts=collections.Counter(z['problem_number'] for z in raw); need(len(byid)==15458,'allunique15458ids')
conn=sqlite3.connect('file:'+str(cache/'catalog.sqlite')+'?mode=ro&immutable=1',uri=True); conn.execute('PRAGMA query_only=ON'); need(conn.execute('PRAGMA query_only').fetchone()==(1,),'readonlyimmutableSQL')
rowbindings=[]; seen=set()
for key,payload,report in conn.execute('SELECT key,payload,report FROM records ORDER BY key'):
    need(key not in seen,'uniqueSQL'); seen.add(key); expected=dict(byid[key]); code=expected['problem_number']; ambiguous=counts[code]>1 and code in prior
    if ambiguous: expected['_ambiguous_report']=True
    expected_report={} if ambiguous else prior.get(code,{})
    need(equal(parse(payload),expected) and equal(parse(report),expected_report),'entire SQL payload/report typed equality')
    rowbindings.append({'key':key,'payload_sha256':sha(payload.encode()),'report_sha256':sha(report.encode()),'complete_payload_recursive_type_equal':True,'complete_report_recursive_type_equal':True,'prior_key_present':code in prior,'ambiguous_code':ambiguous})
conn.close(); need(seen==set(byid),'allSQLrows covered')
rawcert=jsonread(A/'ROOT_COMPLETE_RAW_SQL_AUDIT.json'); need(equal(rowbindings,rawcert['complete_row_bindings']),'allROOT15458derivedrows exact')
need(equal(byid['2849'],parse(original['source_record.json'])) and 'KP-3.51' not in prior and original['prior_report.json']==b'null\n','plainrecord/null/absence')
need(rawcert['selected_prior_key_present'] is False and equal(rawcert['selected_prior_fallback'],{}) and rawcert['literal_original_prior_file_value'] is None,'null/{}fallback distinct')
for row in stable9: bind(R,row,True)
result={'schema':'pr47-whole-independent-complete-frozen-readback/v1','actual_pid':os.getpid(),'utc':utc(),'status':'PASS','assertions':checks,'unique_complete_body_reads':len(readrows),'unique_complete_body_bytes':sum(r['bytes'] for r in readrows.values()),'complete_read_bindings':sorted(readrows.values(),key=lambda r:r['path']),'JSON_node_counts':dict(nodecounts),'packet_payload_count':1328,'packet_relative_directories':282,'dependencies_count':1422,'all_original_archive_count':16,'immutable_operative_count':10,'complete_new_readonly_Git_captures':commands,'complete_actual_current_outer':out,'complete_original_final_inner_commands':final,'complete_ROOT_actual_freeze_inspection':inspection,'frozen_prefix47_final49':True,'native4_proposals_bound':True,'stable9_live_match':True,'dated_head':dated,'observed_live_head':live_head,'live_head_is_dated_head':live_head==dated,'all_raw_prior_bytes':len(rb)+len(pb),'all_SQL_rows':len(rowbindings),'all_15458_row_bindings':rowbindings,'foreign_raw_SQL_PDF_body_copy':False,'full_target_solved':False,'future_acceptance_approved':False,'new_fresh13_HEAD_needed_before_acceptance':True}
(F/'WHOLE_READBACK.json').write_bytes(enc(result))
print(json.dumps({k:result[k] for k in ['status','actual_pid','assertions','unique_complete_body_reads','unique_complete_body_bytes','all_raw_prior_bytes','all_SQL_rows','live_head_is_dated_head','future_acceptance_approved']}))
