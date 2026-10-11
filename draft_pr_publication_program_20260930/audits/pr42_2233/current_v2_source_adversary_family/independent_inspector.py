"""Independent byte reader and own finite predicates; never load foreign code.

Only this directory is writable. Git calls are a fixed read-only list, captured.
Candidate builders and mathematical helpers are never imported/run/compiled.
"""
import ctypes
import datetime as dt
import difflib
import hashlib
import json
import math
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import sys

F = Path(__file__).resolve().parent
A = F.parent
R = A.parents[2]
P = A / 'current_preparation_family_v2'
BINDINGS, CHECKS, JSON_READS, SOURCE_READS, GIT = {}, {}, {}, {}, []

def H(raw): return hashlib.sha256(raw).hexdigest()
def encode(v): return (json.dumps(v, indent=2, ensure_ascii=False)+'\n').encode()
def demand(v, label):
    if not v: raise ValueError(label)
def ck(label, v):
    demand(v, label)
    CHECKS[label] = 'PASS'
def strict(raw):
    def pairs(items):
        out = {}
        for key, value in items:
            demand(key not in out, 'duplicate JSON key')
            out[key] = value
        return out
    def constant(v): raise ValueError('invalid JSON number '+v)
    def floating(v):
        x = float(v)
        demand(math.isfinite(x), 'nonfinite JSON float')
        return x
    return json.loads(raw, object_pairs_hook=pairs, parse_constant=constant, parse_float=floating)
def types(v):
    stack, counts = [v], {}
    while stack:
        x = stack.pop(); key = type(x).__name__
        counts[key] = counts.get(key, 0)+1
        if type(x) is dict: stack.extend(x.values())
        elif type(x) is list: stack.extend(x)
    return counts
def equal(a, b):
    return json.dumps(a,sort_keys=True,separators=(',',':')) == json.dumps(b,sort_keys=True,separators=(',',':'))
def safe(s):
    demand(type(s) is str and s and '\\' not in s, 'relative path type')
    p = PurePosixPath(s)
    demand(not p.is_absolute() and p.as_posix()==s and not {'.','..','.git','__pycache__'}.intersection(p.parts),'unsafe path')
    return s
def rowset(items):
    demand(type(items) is list,'rows list')
    names=set()
    for row in items:
        demand(type(row) is dict and set(row)=={'path','bytes','sha256'},'exact row shape')
        name=safe(row['path'])
        demand(name not in names,'duplicate row')
        names.add(name)
        demand(type(row['bytes']) is int and row['bytes']>=0 and type(row['sha256']) is str and re.fullmatch('[0-9a-f]{64}',row['sha256']) is not None,'typed row')
    return names
def tree(root, empty_allowed=False):
    demand(root.is_dir() and not root.is_symlink(),'regular root')
    files, dirs=set(),set()
    for p in root.rglob('*'):
        demand(not p.is_symlink(),'symlink rejected')
        name=safe(p.relative_to(root).as_posix())
        if p.is_file(): files.add(name)
        else:
            demand(p.is_dir(),'special member rejected'); dirs.add(name)
    expected={x.as_posix() for n in files for x in PurePosixPath(n).parents if x.as_posix()!='.'}
    if not empty_allowed: demand(dirs==expected,'empty extra rejected')
    return files,dirs
def read(p, role):
    demand(p.is_file() and not p.is_symlink() and all(not q.is_symlink() for q in p.parents),'regular file required '+str(p))
    # Full bytes are read into memory, never copied to this audit.
    raw=p.read_bytes(); name=p.relative_to(R).as_posix()
    row=dict(path=name,bytes=len(raw),sha256=H(raw),roles=[role])
    if name in BINDINGS:
        old=BINDINGS[name]
        demand(all(row[k]==old[k] for k in ['path','bytes','sha256']),'input changed on repeated read')
        row['roles']=sorted(set(old['roles']+row['roles']))
    BINDINGS[name]=row
    if p.suffix in {'.json','.jsonl'} and name.startswith(A.relative_to(R).as_posix()+'/'):
        value=[strict(line) for line in raw.splitlines()] if p.suffix=='.jsonl' else strict(raw)
        JSON_READS[name]=dict(path=name,bytes=len(raw),sha256=H(raw),type_counts=types(value),all_values_visited=True)
    if p.suffix in {'.py','.md','.patch'}:
        text=raw.decode('utf-8')
        SOURCE_READS[name]=dict(path=name,bytes=len(raw),sha256=H(raw),lines=len(text.splitlines()),full_UTF8_read=True,semantic_scope='Full text bytes, separately reviewed critical builder/contracts/proofs; no imported code execution or AST compilation.')
    return raw
def bind(root,row,role):
    raw=read(root/safe(row['path']),role)
    ck('binding:'+str((root/row['path']).relative_to(R)),type(row['bytes']) is int and len(raw)==row['bytes'] and H(raw)==row['sha256'])
    return raw
def J(p,role='full strict JSON read'): return strict(read(p,role))
def git(*argv):
    demand(argv[0] in {'branch','rev-parse','show','ls-tree','diff'},'fixed read-only Git')
    demand(argv[0]!='branch' or argv[1:]==('--show-current',),'read-only branch')
    d=F/'READONLY_GIT';d.mkdir(exist_ok=True);i=len(GIT)
    rec=dict(argv=['git',*argv],cwd=str(R),started_utc=dt.datetime.now(dt.timezone.utc).isoformat(),pid=None,actual_execution=False,completed=False,exit_code=None,stdin_supplied=False)
    GIT.append(rec)
    try:
        with (d/(str(i)+'.stdout')).open('xb') as out,(d/(str(i)+'.stderr')).open('xb') as err:
            child=subprocess.Popen(rec['argv'],cwd=R,stdin=subprocess.DEVNULL,stdout=out,stderr=err,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'))
            rec.update(pid=child.pid,actual_execution=True)
            try: rec['exit_code']=child.wait(timeout=45);rec['completed']=True
            except BaseException: child.kill();rec['exit_code']=child.wait();raise
    finally:
        rec['finished_utc']=dt.datetime.now(dt.timezone.utc).isoformat()
        for c in ['stdout','stderr']:
            p=d/(str(i)+'.'+c)
            if p.exists():
                raw=p.read_bytes();rec[c]=dict(path=p.relative_to(F).as_posix(),bytes=len(raw),sha256=H(raw),classification='own forensic capture; embedded original code/text is attributed foreign evidence')
        (F/'GIT_COMMANDS.json').write_bytes(encode(GIT))
    demand(rec['completed'] is True and rec['exit_code']==0,'actual read-only Git failed')
    return (d/(str(i)+'.stdout')).read_bytes()
def reject(label,fn):
    try: fn()
    except (ValueError,TypeError,KeyError,json.JSONDecodeError): CHECKS[label]='PASS_REJECTED'
    else: raise ValueError('failed negative control '+label)

requested={'PREPARATION_MANIFEST.json':'c77fbc8effa07391977ed49a161001625f81bdcf1f0e647537fdae441d0b2071','prepare_current_packet.py':'ec426a4207c57645fe33b58b7f67acb20c45da455bf9d959077ff6f191d76a76','REPAIR_INPUT_PINS.json':'cb6138cca003898fb15742a070a72719c0edb645b8054ea110cd4fd1a9ee8ac2','SOURCE_REPAIR_DELTA.patch':'304f08bf36700b860390d57b7c49df72e0b91881b123fb131ee9cd8f2862242c','INPUT_PINS.json':'54c0aa6f06615a0ff6c106f9025a8b4ac788da09f3dfb8c242bc669fa76684f3','SOURCE_PRECISION_QUALIFICATIONS.md':'3529898445960cde70381bf99ea8287ec88a1003d8ca1cb4c3e0d088abdee570'}
for n,h in requested.items(): ck('exact_requested_pin:'+n,H(read(P/n,'operative closed repaired source'))==h)
prep=J(P/'PREPARATION_MANIFEST.json');files,dirs=tree(P)
ck('v2_exact33_plus_self',files==rowset(prep['files'])|{'PREPARATION_MANIFEST.json'} and prep['files_count']==len(prep['files'])==33)
for row in prep['files']: bind(P,row,'operative closed preparation member')
repair=J(P/'REPAIR_INPUT_PINS.json');prior_counts={}
for info in repair['prior_closed_evidence']:
    root=A/safe(info['directory']);manifest=strict(bind(root,info['manifest'],'unchanged prior closed manifest'))
    f,d=tree(root,True);normalized=[{k:x[k] for k in ['path','bytes','sha256']} for x in manifest['files']]
    ck('exact_prior_tree:'+root.name,f==rowset(normalized)|{info['manifest']['path']} and d==set(info['directories']) and manifest['files_count']==len(normalized)==info['files_count'])
    if 'directories' in manifest:
        ck('exact_prior_four_empty_controls',manifest['directories']==info['directories'] and manifest['explicitly_retained_own_empty_finite_control_directories']==info['intentional_empty_directories'] and len(info['intentional_empty_directories'])==4)
    for row in normalized: bind(root,row,'foreign predecessor source/capture/failure individually excluded from this authorship')
    for row in manifest['files']:
        if 'permission_mode' in row: ck('prior_full_mode:'+row['path'],oct(stat.S_IMODE((root/row['path']).stat().st_mode))==row['permission_mode'])
    prior_counts[root.name]=len(normalized)
old=read(A/'current_preparation_family/prepare_current_packet.py','full old builder source')
new=read(P/'prepare_current_packet.py','full repaired builder source')
delta=''.join(difflib.unified_diff(old.decode().splitlines(keepends=True),new.decode().splitlines(keepends=True),fromfile='current_preparation_family/prepare_current_packet.py',tofile='current_preparation_family_v2/prepare_current_packet.py')).encode()
ck('entire_delta_exact',delta==read(P/'SOURCE_REPAIR_DELTA.patch','full independently recomputed source delta'))
ck('full_permission_guards_two',new.count(b'stat.S_IMODE(path.stat().st_mode) == 0o444')==1 and new.count(b"stat.S_IMODE((stage / 'MANIFEST.json').stat().st_mode) == 0o444")==1 and b'st_mode & 0o777' not in new)
for n in ['INPUT_PINS.json','SOURCE_PRECISION_QUALIFICATIONS.md','CURRENT_OVERVIEW.md','DRAFT_ROOT_READ_LEDGER.json','DRAFT_ROOT_SCIENCE_CARD.json','DRAFT_ROOT_CURRENT_INPUT_PREIMAGES.json']:
    ck('byte_unchanged:'+n,read(P/n,'unchanged v2 schema/science')==read(A/'current_preparation_family'/n,'unchanged v1 schema/science'))
pins=J(P/'INPUT_PINS.json');snapshot=strict(bind(A,pins['original_manifest'],'full original snapshot17 manifest'))
ck('original_exact17_diff18',len(snapshot['files'])==17 and len(snapshot['changed_paths'])==18 and snapshot['head']=='099ae5e4d06d8789214cfaaece87309c87e914f9' and snapshot['base']=='60292bed09f59236aa192cb17aa138f7b4750e1a')
ck('actual_main',git('branch','--show-current').strip()==b'main');head=git('rev-parse','HEAD').decode().strip()
original={}
for row in snapshot['files']:
    raw=bind(A/'source_snapshot_v2',dict(path=row['path'],bytes=row['size'],sha256=row['sha256']),'immutable original scientific archive')
    name='unsolved_math_prioritization/attempts/2233/'+row['path']
    ck('Git_original_bytes:'+row['path'],git('show',snapshot['head']+':'+name)==raw)
    ck('Git_original_mode_blob:'+row['path'],git('ls-tree',snapshot['head'],'--',name).decode().strip()==row['mode']+' blob '+row['git_blob']+'\t'+name)
    original[row['path']]=raw
ck('original_recursive17',tree(A/'source_snapshot_v2')[0]==set(original))
diff=read(A/'original_diff_v2.patch','complete original18-pathdiff')
ck('entire_original_diff',len(diff)==snapshot['diff_bytes'] and H(diff)==snapshot['diff_sha256'] and git('diff',snapshot['base'],snapshot['head'])==diff and git('diff','--name-only',snapshot['base'],snapshot['head']).decode().splitlines()==snapshot['changed_paths'])
ck('wrong_base_empty_retained',tree(A/'source_snapshot')[0]==set())
retained=0
for info in pins['retained_closures']:
    root=A/info['directory'];ck('retained_tree:'+root.name,tree(root)[0]==rowset(info['files']))
    for row in info['files']: bind(root,row,'full retained original actual/failure evidence')
    retained+=len(info['files'])
ck('retained104_aux14',retained==104 and len(pins['auxiliary'])==14)
for row in pins['auxiliary']: bind(A,row,'full retained original auxiliary source/log')
family_counts={};foreign_rows=[]
for family,info in pins['families'].items():
    root=A/family;manifest=strict(bind(root,info['manifest'],'closed original independent family manifest'))
    copied,foreign=rowset(info['copied_members']),rowset(info['foreign_members'])
    ck('foreign_disjoint:'+family,not copied.intersection(foreign))
    ck('family_tree:'+family,tree(root)[0]==copied|foreign|{info['manifest']['path']})
    for row in info['copied_members']: bind(root,row,'foreign original independent first-party evidence; excluded from own authorship')
    for row in info['foreign_members']:
        bind(root,row,'foreign primary/derivative individually excluded from candidate copying and own authorship')
        foreign_rows.append(dict(row,path=(root/row['path']).relative_to(R).as_posix()))
    if family=='literal_geometry_family':
        ck('literal_extract_explicitly_excluded','controls/primary_pdf_extract.stdout.txt' in foreign and 'controls/primary_pdf_extract.stdout.txt' not in copied and len(copied)==54 and len(foreign)==26)
    else:
        ck('exact41_copy5_foreign',len(copied)==41 and len(foreign)==5)
        for row in manifest['foreign_external_read_files_individually_pinned_and_excluded']:
            path=Path(row['path']);bind(R,dict(path=path.relative_to(R).as_posix(),bytes=row['bytes'],sha256=row['sha256']),'original exact family external dependency; excluded own authorship')
    family_counts[family]=dict(copied=len(copied),individually_excluded=len(foreign))
actual=J(A/'root_original_actual_reproduction_v2/RESULT.json','complete original typed genuine replay record')
saved=strict(original['check_results.json']);independent=strict(original['review/independent_results.json'])
ck('full_actual_author_objects',equal(actual['entire_current_author_result'],dict(saved,partial_sha256=H(original['PARTIAL.md']))) and equal(actual['entire_reviewed_author_result'],saved))
ck('all1263_independent_labels',equal(actual['entire_original_independent_result'],independent) and type(independent['passed']) is int and independent['passed']==len(independent['checks'])==1263 and independent['failed']==0 and all(type(x) is str and x=='PASS' for x in independent['checks'].values()))
ledger=[strict(line) for line in original['turns.jsonl'].splitlines()]
ck('whole_original_ledger',len(ledger)==2 and [row['turn'] for row in ledger]==[1,2] and all(type(row['turn']) is int for row in ledger) and equal(actual['whole_original_ledger'],ledger))
ck('whole_source_fallback',equal(strict(original['source_record.json']),J(A/'pinned_problem.json')) and J(A/'pinned_prior_report.json')=={} and actual['original_prior_raw_key_present'] is False and actual['prior_SQL_empty_object_is_fallback'] is True)
ck('original_execution_dimensions',actual['author_assertions']==18306 and actual['independent_assertions']==1263 and actual['whole_raw_bytes']==149266659 and actual['whole_SQL_rows']==15458)
ck('original2_new0_audit0_unsolved',all(type(actual[k]) is int and actual[k]==v for k,v in [('original_substantive_attempts',2),('new_substantive_attempts',0),('audit_turns',0)]) and actual['full_problem_solved'] is False)
for i,run in enumerate(actual['actual_outer_runs']):
    ck('actual_original_run_metadata:'+str(i),run['actual_execution'] is True and run['completed'] is True and type(run['pid']) is int and run['pid']>0 and type(run['exit_code']) is int and run['exit_code']==0 and run['stdin_supplied'] is False)
    for n in ['stdout','stderr','source','output_file']: bind(A/'root_original_actual_reproduction_v2',run[n],'full original actual '+n)
ck('header_only_math_change',original['review/PARTIAL.md'].replace(b'Separate adversarial review is pending.',b'Separate adversarial AI review passed; see [the report](review/REVIEW.md). This has not undergone human peer review.')==original['PARTIAL.md'])
old_sentence=b'The corresponding research-results entry is null, with only a dated OPEN-TRIAGE note embedded in the problem background.'
ck('one_prior_precision_sentence',original['SOURCE_AUDIT.md'].count(old_sentence)==1)
native=[]
for row in pins['native13_at_preparation']:
    raw=read(R/row['path'],'live native dated observation; never fresh ROOT approval')
    native.append(dict(path=row['path'],bytes=len(raw),sha256=H(raw),differs_from_preparation=len(raw)!=row['bytes'] or H(raw)!=row['sha256']))
ck('native13_exact_required_names',len(rowset(pins['native13_at_preparation']))==13 and set(J(P/'DRAFT_ROOT_CURRENT_INPUT_PREIMAGES.json')['required_paths'])=={r['path'] for r in native})
raw_prior=strict(read(R/'unsolved_math_prioritization/cache/research_results.json','whole current raw absence observation'))
ck('direct_raw_key_absent','EP-653' not in raw_prior)
for n in ['DRAFT_ROOT_READ_LEDGER.json','DRAFT_ROOT_SCIENCE_CARD.json']:
    d=J(P/n);ck('draft_false_eight_flags:'+n,d['reading_completed'] is False and len(d['root_flags'])==8 and all(v is False for v in d['root_flags'].values()) and not equal(d['root_flags'],{k:True for k in d['root_flags']}))
    ck('draft_null_approval_hashes:'+n,d['scope_certificate_sha256'] is None and d['preparation_manifest_sha256'] is None)
science=J(P/'DRAFT_ROOT_SCIENCE_CARD.json')
ck('draft_science_current_nulls',all(science[k] is None for k in ['current_model','current_reasoning_effort','current_deadline_utc','current_verdict']))
root_observations={}
for n in ['ROOT_CURRENT_PARTIAL_SCOPE_CERTIFICATE.md','ROOT_PRIMARY_READ_LEDGER.json','ROOT_SCIENCE_CARD.json','ROOT_CURRENT_INPUT_PREIMAGES.json']:
    p=A/n;root_observations[n]=dict(present=p.exists(),symlink=p.is_symlink())
    if p.is_file():
        raw=read(p,'dated actual ROOT prerequisite observation; no future attestation')
        root_observations[n].update(bytes=len(raw),sha256=H(raw))
candidate=A/'reviewed_candidate';ck('candidate_still_absent',not candidate.exists() and not candidate.is_symlink())
status=J(P/'SOURCE_STATUS.json')
ck('source_status_pending_nulls',status['NEW_whole_current_gate']=='PENDING' and status['future_whole_current_verdict'] is None and all(status[k] is None for k in ['current_model','current_reasoning_effort','current_deadline_utc']) and status['candidate_created'] is False)

# Own independently authored finite diagnostics, with no candidate function calls.
for i,bad in enumerate([b'{"x":1,"x":2}',b'NaN',b'Infinity',b'1e9999']): reject('strict_json_negative:'+str(i),lambda bad=bad:strict(bad))
ck('boolean_numeric_serialized_distinct',not equal(True,1) and not equal({'f':True},{'f':1}))
good=dict(path='n/f',bytes=0,sha256='a'*64)
for i,bad in enumerate([[dict(good,bytes=True)],[dict(good,bytes=-1)],[good,good],[dict(good,extra=0)],[dict(good,sha256='A'*64)]]): reject('rows_negative:'+str(i),lambda bad=bad:rowset(bad))
for i,bad in enumerate(['','/x','../x','./x','x//y','x/','x\\y','.git/x','__pycache__/x',True]): reject('path_negative:'+str(i),lambda bad=bad:safe(bad))
C=F/'FINITE_CONTROLS';C.mkdir(exist_ok=False);cases=[]
for mode in [0o444,0o1444,0o2444,0o4444,0o644,0o400]:
    p=C/('mode_'+format(mode,'04o'));p.write_bytes(b'Own finite predicate object; never candidate evidence.\n');p.chmod(mode)
    observed=p.stat().st_mode;full=stat.S_IMODE(observed)
    ck('actual_full_permission:'+oct(mode),full==mode and (full==0o444)==(mode==0o444))
    cases.append(dict(path=p.relative_to(F).as_posix(),requested=oct(mode),actual_st_mode=oct(observed),actual_permission=oct(full),exact_guard_accepts=full==0o444,old_guard_accepts=(observed&0o777)==0o444))
    p.chmod(0o444) # normalized after actual finite observation for this own closure
ck('exhaustive4096_permission_guard',sum(stat.S_IMODE(stat.S_IFREG|m)==0o444 for m in range(0o10000))==1)
valid=C/'valid';(valid/'nested').mkdir(parents=True);(valid/'nested/member').write_bytes(b'own exact control')
ck('valid_recursive_tree',tree(valid)[0]=={'nested/member'})
empty=C/'intentional_empty';(empty/'extra').mkdir(parents=True);reject('empty_tree_negative',lambda:tree(empty))
linkdir=C/'removed_symlink_control';linkdir.mkdir();link=linkdir/'link';link.symlink_to(valid/'nested/member');reject('symlink_negative',lambda:tree(linkdir));link.unlink()
fifodir=C/'removed_fifo_control';fifodir.mkdir();fifo=fifodir/'fifo';os.mkfifo(fifo);reject('special_negative',lambda:tree(fifodir));fifo.unlink()
ck('macOS_exclusive_environment',sys.platform=='darwin')
libc=ctypes.CDLL(None,use_errno=True);rename=libc.renamex_np;rename.argtypes=[ctypes.c_char_p,ctypes.c_char_p,ctypes.c_uint];rename.restype=ctypes.c_int
source=C/'failed_exclusive_stage';source.mkdir();(source/'member').write_bytes(b'own stage retained')
destination=C/'existing_destination';destination.mkdir();(destination/'sentinel').write_bytes(b'unchanged sentinel')
rv=rename(os.fsencode(source),os.fsencode(destination),4);err=ctypes.get_errno()
ck('exclusive_existing_rejected_preserved',rv==-1 and err==17 and (source/'member').read_bytes()==b'own stage retained' and (destination/'sentinel').read_bytes()==b'unchanged sentinel')
absent=C/'absent_destination';rv2=rename(os.fsencode(source),os.fsencode(absent),4)
ck('exclusive_absent_published_own',rv2==0 and not source.exists() and (absent/'member').read_bytes()==b'own stage retained')
# A second rejected stage is deliberately retained as failure-preservation evidence.
retained_stage=C/'retained_failed_stage';retained_stage.mkdir();(retained_stage/'member').write_bytes(b'own permanently retained rejected stage')
rv3=rename(os.fsencode(retained_stage),os.fsencode(destination),4);err3=ctypes.get_errno()
ck('second_failure_stage_retained',rv3==-1 and err3==17 and (retained_stage/'member').exists())
(F/'FINITE_RESULTS.json').write_bytes(encode(dict(cases=cases,exhaustive_full_permission_modes=4096,only_0444_accepted=True,finite_mode_objects_normalized_after_observation_to='0444',nonregular_control_objects_removed_after_recorded_negative_checks=True,removed_paths=[link.relative_to(F).as_posix(),fifo.relative_to(F).as_posix()],historical_or_builder_failures_removed=False,exclusive_existing_errno=err,second_failure_errno=err3,retained_failed_stage=retained_stage.relative_to(F).as_posix(),builder_or_helper_import_compile_execute=False)))

# Queue operation is reproduced only on an in-memory whole preimage.
header=['Rank','ID / code','Problem','EV','Impact (/10)','Difficulty','Proposed','Status','Turns','Chat','Findings','DOI']
queue=read(R/'unsolved_math_prioritization/QUEUE.md','whole queue proposal preimage only');lines=queue.splitlines(keepends=True)
headers=[x for x in lines if x.startswith(b'|') and [f.strip() for f in x.decode().split('|')[1:-1]]==header]
hits=[]
for line in lines:
    if line.startswith(b'|'):
        fields=line.decode().split('|')
        if len(fields)==len(header)+2 and fields[2].strip()=='2233 / EP-653':hits.append((line,fields))
ck('queue_unique_target_header',len(hits)==len(headers)==1);before,fields=hits[0];idx={k:header.index(k)+1 for k in header}
ck('queue_native_queued0of5',fields[idx['Status']].strip()=='queued' and fields[idx['Turns']].strip()=='0/5')
changed=list(fields)
for k,v in [('Status','unsolved'),('Turns','2/5'),('Findings','Scoped generic-gluing and line/circle obstructions verified; full EP-653 UNSOLVED. No novelty or best-known claim. NEW whole-current review PENDING; original2/5, new0.')]:changed[idx[k]]=' '+v+' '
after='|'.join(changed).encode();proposal=[after if line==before else line for line in lines]
ck('queue_only_three_named_fields',all(a==b for i,(a,b) in enumerate(zip(fields,changed)) if i not in {idx[k] for k in ['Status','Turns','Findings']}))
ck('queue_one_row_Chat_DOI_preserved',sum(a!=b for a,b in zip(lines,proposal))==1 and fields[idx['Chat']]==changed[idx['Chat']] and fields[idx['DOI']]==changed[idx['DOI']])
(F/'QUEUE_FINITE_RESULT.json').write_bytes(encode(dict(preimage_sha256=H(queue),prospective_sha256=H(b''.join(proposal)),row_before=before.decode(),row_prospective=after.decode(),native_writes=False)))
ck('observed_head_unchanged_during_inspection',git('rev-parse','HEAD').decode().strip()==head)
ck('final_no_candidate',not candidate.exists() and not candidate.is_symlink())
result=dict(schema='PR42_V2_INDEPENDENT_SOURCE_ONLY_INSPECTION_v1',utc=dt.datetime.now(dt.timezone.utc).isoformat(),status='COMPLETE_INDEPENDENT_SOURCE_BINDING_AND_FINITE_INSPECTION',checks_count=len(CHECKS),checks=CHECKS,foreign_external_inputs_individually_bound_and_excluded_from_authorship=sorted(BINDINGS.values(),key=lambda x:x['path']),individual_foreign_primary_derivatives=foreign_rows,closed_JSON_reads=sorted(JSON_READS.values(),key=lambda x:x['path']),source_text_reads=sorted(SOURCE_READS.values(),key=lambda x:x['path']),prior_closure_counts=prior_counts,original17=17,original_diff_paths=18,retained_ROOT_members=retained,family_counts=family_counts,current_main_HEAD_observed=head,native13_dated_observations=native,actual_ROOT_prerequisites_observed=root_observations,candidate_present=False,readonly_git_count=len(GIT),builder_or_mathematical_helper_import_compile_execute=False,no_future_ROOT_reading_or_execution_attestation=True,whole_current_verdict=None,NEW_whole_current_gate='PENDING',original_substantive_attempts=2,new_substantive_attempts=0,audit_turns=0,full_problem_solved=False,scope_limit='Byte-complete and strict JSON structural inspection plus own finite guards; no repeat original scientific replay, no repeat whole SQL join computation, no full external paper proof certification.')
(F/'INSPECTION_RESULT.json').write_bytes(encode(result))
print(json.dumps(dict(status=result['status'],checks=len(CHECKS),foreign_bound=len(BINDINGS),complete_closed_JSON=len(JSON_READS),complete_text_sources=len(SOURCE_READS),Git_readonly_commands=len(GIT),prior_closures=prior_counts,native_changed=[x['path'] for x in native if x['differs_from_preparation']],candidate_present=False,builder_or_helper_import_compile_execute=False,whole_current_verdict=None),indent=2))
