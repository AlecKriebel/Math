"""Handwritten private source audit. Production is read as bytes/text only."""
from pathlib import Path, PurePosixPath
import ctypes, datetime as dt, hashlib, json, math, os, re, stat, subprocess, sys, traceback

F = Path(__file__).absolute().parent
A = F.parent
R = A.parents[2]
P = A / 'current_preparation_family'
CHECKS = []
READS = {}

def now(): return dt.datetime.now(dt.timezone.utc).isoformat()
def sha(body): return hashlib.sha256(body).hexdigest()
def emit(path, value): path.write_bytes((json.dumps(value, indent=2, sort_keys=True, allow_nan=False)+'\n').encode())
def check(value, label):
    if value is not True: raise ValueError(label)
    CHECKS.append(label)
def want_rejection(action, label):
    try: action()
    except (ValueError, TypeError, KeyError, OSError, json.JSONDecodeError): CHECKS.append(label); return
    raise ValueError('Expected rejection: '+label)
def plain(path):
    if path.is_symlink() or any(q.is_symlink() for q in path.parents) or not stat.S_ISREG(path.stat().st_mode): raise ValueError('Not regular nonsymlink')
    return path.read_bytes()
def path_token(token):
    if type(token) is not str or not token or '\\' in token or '\0' in token: raise ValueError('Bad relative token')
    q = PurePosixPath(token)
    if q.is_absolute() or q.as_posix()!=token or set(q.parts)&{'.','..','.git','__pycache__'}: raise ValueError('Noncanonical relative path')
    return token
def row_tokens(rows):
    if type(rows) is not list: raise ValueError('Not list')
    names=set()
    for row in rows:
        if type(row) is not dict or set(row)!={'path','bytes','sha256'}: raise ValueError('Wrong row keys')
        name=path_token(row['path'])
        if name in names: raise ValueError('Duplicate path')
        names.add(name)
        if type(row['bytes']) is not int or row['bytes']<0 or type(row['sha256']) is not str or re.fullmatch('[0-9a-f]{64}',row['sha256']) is None: raise ValueError('Wrong scalar type')
    return names
def parse(body):
    def object_pairs(items):
        result={}
        for key,value in items:
            if key in result: raise ValueError('Duplicate JSON key')
            result[key]=value
        return result
    def constants(value): raise ValueError('Nonfinite constant')
    def floats(value):
        q=float(value)
        if not math.isfinite(q): raise ValueError('Nonfinite float')
        return q
    return json.loads(body,object_pairs_hook=object_pairs,parse_constant=constants,parse_float=floats)
def exact(a,b): return json.dumps(a,sort_keys=True,allow_nan=False,separators=(',',':'))==json.dumps(b,sort_keys=True,allow_nan=False,separators=(',',':'))
def full_tree(root):
    if root.is_symlink() or any(q.is_symlink() for q in root.parents) or not root.is_dir(): raise ValueError('Bad root')
    files=set(); directories=set()
    for q in root.rglob('*'):
        if q.is_symlink(): raise ValueError('Symlink member')
        name=path_token(q.relative_to(root).as_posix()); mode=q.stat().st_mode
        if stat.S_ISREG(mode): files.add(name)
        elif stat.S_ISDIR(mode): directories.add(name)
        else: raise ValueError('Special member')
    implied={q.as_posix() for name in files for q in PurePosixPath(name).parents if q.as_posix()!='.'}
    if directories!=implied: raise ValueError('Empty/extra directory')
    return files, directories
def observe(row, anchor=A, role='first_party'):
    row_tokens([row]); path=anchor/row['path']; body=plain(path)
    check(len(body)==row['bytes'] and sha(body)==row['sha256'],'exact '+str(path.relative_to(R)))
    key=path.relative_to(R).as_posix()
    record={'path':key,'bytes':len(body),'sha256':sha(body),'full_mode':stat.S_IMODE(path.stat().st_mode),'roles':[role]}
    if key in READS: record['roles']=sorted(set(record['roles']+READS[key]['roles']))
    READS[key]=record
    return body
def self_manifest(root, manifest_name, expected_hash, count, allowed_extra=()):
    body=plain(root/manifest_name); check(sha(body)==expected_hash,'pinned manifest '+manifest_name)
    data=parse(body); source_rows=data['files']; normalized=[]
    for row in source_rows:
        normalized.append({k:row[k] for k in ['path','bytes','sha256']})
    names=row_tokens(normalized)
    check(type(data['files_count']) is int and data['files_count']==len(names)==count,'typed count '+manifest_name)
    files,dirs=full_tree(root)
    check(files==names|{manifest_name}|set(allowed_extra),'complete topology '+manifest_name)
    for row in normalized:
        observe(row,root,'closed_first_party_member')
        check(stat.S_IMODE((root/row['path']).stat().st_mode)==0o444,'full0444 '+str(root/row['path']))
    check(stat.S_IMODE((root/manifest_name).stat().st_mode)==0o444,'manifest full0444 '+manifest_name)
    return data,dirs
def git(argv):
    captures=F/'READ_ONLY_GIT_ACTUAL'; captures.mkdir(exist_ok=True); index=len(list(captures.glob('*.json')))
    record={'schema':'PR46_CURRENT_SOURCE_ADVERSARY_GIT_ACTUAL_v1','argv':['git',*argv],'cwd':str(R),'operator_pid':os.getpid(),'started_utc':now(),'actual_execution':False,'completed':False,'pid':None,'exit_code':None,'stdin_supplied':False,'production_executed':False}
    emit(captures/(str(index)+'.PRELAUNCH.json'),record)
    try:
        with (captures/(str(index)+'.stdout.bin')).open('xb') as out, (captures/(str(index)+'.stderr.bin')).open('xb') as err:
            child=subprocess.Popen(record['argv'],cwd=R,stdin=subprocess.DEVNULL,stdout=out,stderr=err,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'))
            record.update(actual_execution=True,pid=child.pid)
            try: record['exit_code']=child.wait(timeout=60); record['completed']=True
            except BaseException: child.kill(); record['exit_code']=child.wait(); raise
    except BaseException: record['failure']=traceback.format_exc(); raise
    finally:
        record['finished_utc']=now()
        for channel in ['stdout','stderr']:
            q=captures/(str(index)+'.'+channel+'.bin')
            if q.exists():
                b=plain(q); record[channel]={'path':q.name,'bytes':len(b),'sha256':sha(b)}
        emit(captures/(str(index)+'.CAPTURE.json'),record)
    check(record['actual_execution'] is True and record['completed'] is True and type(record['exit_code']) is int and record['exit_code']==0,'actual read-only Git completed')
    check(not plain(captures/(str(index)+'.stderr.bin')),'empty read-only Git stderr')
    return plain(captures/(str(index)+'.stdout.bin'))
def native_rows():
    names=['QUEUE.md','state.json','history.jsonl','catalog.json','assessments.json','queue.py','policy.json','manifest.json','cache/problems.json','cache/research_results.json','cache/catalog.sqlite','review_v2/related_target_groups.json']
    paths=['unsolved_math_prioritization/'+n for n in names]+['draft_pr_publication_program_20260930/inventory.json']
    records=[]
    for name in paths:
        q=R/name; body=plain(q); records.append({'path':name,'bytes':len(body),'sha256':sha(body),'full_mode':stat.S_IMODE(q.stat().st_mode)})
    return records
def toy_queue(body):
    header=['Rank','ID / code','Problem','EV','Impact (/10)','Difficulty','Proposed','Status','Turns','Chat','Findings','DOI']
    lines=body.splitlines(keepends=True)
    matching=[line for line in lines if line.startswith(b'|') and [c.strip() for c in line.decode().split('|')[1:-1]]==header]
    if len(matching)!=1: raise ValueError('Header not unique')
    rows=[(i,line,line.decode().split('|')) for i,line in enumerate(lines) if line.startswith(b'|') and len(line.decode().split('|'))==14 and line.decode().split('|')[2].strip()=='30004438 / OWR-17475-003']
    if len(rows)!=1: raise ValueError('Target not unique')
    i,before,parts=rows[0]
    if parts[8].strip()!='queued' or parts[9].strip()!='0/5': raise ValueError('Wrong preimage')
    after=list(parts)
    for column,value in [('Status','already_solved'),('Turns','0/5'),('Findings','PRIVATE TOY known-result credit; review pending')]: after[header.index(column)+1]=' '+value+' '
    changed={j for j,(a,b) in enumerate(zip(parts,after)) if a!=b}
    if not changed<={8,9,11}: raise ValueError('Unapproved column changed')
    output=list(lines); output[i]='|'.join(after).encode()
    if any(output[j]!=lines[j] for j in range(len(lines)) if j!=i): raise ValueError('Other row changed')
    return b''.join(output),parts,after
def exclusive(source,destination):
    if sys.platform!='darwin': raise ValueError('macOS required')
    lib=ctypes.CDLL(None,use_errno=True); rename=lib.renamex_np
    rename.argtypes=[ctypes.c_char_p,ctypes.c_char_p,ctypes.c_uint]; rename.restype=ctypes.c_int
    if rename(os.fsencode(source),os.fsencode(destination),4):
        error=ctypes.get_errno(); raise OSError(error,os.strerror(error))

def run():
    start=now(); before_native=native_rows(); before_head=git(['rev-parse','HEAD']).decode().strip()
    check(git(['branch','--show-current']).strip()==b'main','main before')
    source=plain(P/'prepare_current_packet.py'); operator=plain(P/'capture_root_builder_operation.py')
    check(sha(source)=='c44ebde1cd07f53dcfe13b51205777b6dea0776bd18fded15eb85d7c8e3c2c83','independent operative builder binding')
    check(sha(operator)=='852501ddca5804a931fbda3e176fb6518bf648387754dc2e5383acb5a6bdb830','independent operative operator binding')
    prep,prepdirs=self_manifest(P,'PREPARATION_MANIFEST.json','2f1ef9d9b0b4c9596110f5a66aa6d5095fdf611cc65f9aa367b208ca5ab6accc',60)
    check(prep['schema']=='PR46_CURRENT_SOURCE_ONLY_CLOSURE_v1' and prep['self_excluded']==['PREPARATION_MANIFEST.json'] and prep['status']=='CLOSED_SOURCE_ONLY_CURRENT_PREPARATION','SOURCE self-only status')
    check(set(prep['directories'])==prepdirs and prep['production_import_compile_or_execution'] is False and prep['ROOT_reading_or_approval'] is None,'SOURCE no transferred execution/approval')
    pins=parse(plain(P/'STATIC_INPUT_BINDINGS.json'))
    for field in ['snapshot_manifest','original_metadata','original_preparation_manifest']: observe(pins[field],role=field)
    original=parse(plain(A/pins['original_preparation_manifest']['path'])); owned=row_tokens([{k:row[k] for k in ['path','bytes','sha256']} for row in original['files']])
    check(len(owned)==318 and owned==row_tokens(pins['original_preparation_members']),'original exact scoped318 rows')
    actual=set(original['authorship_root_files'])
    for directory in original['authorship_directory_roots']: actual|={directory+'/'+n for n in full_tree(A/directory)[0]}
    check(actual==owned,'original scoped ownership excludes siblings')
    for row in pins['original_preparation_members']:
        observe(row,role='original_scoped_member'); check(stat.S_IMODE((A/row['path']).stat().st_mode)==0o444,'original scoped full0444')
    check(stat.S_IMODE((A/pins['original_preparation_manifest']['path']).stat().st_mode)==0o444,'original self full0444')
    for row in pins['original_separate_closure_capture']+pins['genuine_closed_ROOT_evidence_fixed_rows']: observe(row,role='completed_first_party_evidence')
    families={}
    for family,info in pins['families'].items():
        manifest,dirs=self_manifest(A/family,info['manifest']['path'],info['manifest']['sha256'],len(info['members']),row_tokens(info['separate_excluded_closure']))
        check(set(info['directories'])==dirs==set(info['directory_modes']),'family exact directory topology')
        check(all(type(m) is int and stat.S_IMODE((A/family/n).stat().st_mode)==m for n,m in info['directory_modes'].items()),'family exact directory modes')
        check(manifest['self_excluded']==info['manifest_self_excluded'],'family dated exact exclusions')
        for row in info['members']+info['separate_excluded_closure']: observe(row,A/family,'family_exact_member')
        families[family]={'manifest_sha256':info['manifest']['sha256'],'count':len(info['members']),'separate_excluded_count':len(info['separate_excluded_closure'])}
    root,rootdirs=self_manifest(A/'root_original_actual_reproduction_v2','MANIFEST.json','0fe84c88fabb16e1512d440f9f447ed56c9a29ea4c78a52075e6c323d51e2fc7',37)
    check(root['future_acceptance_approved'] is False,'ROOT reproduction has no future acceptance')
    closure=A/'current_preparation_closure_actual_capture'
    check(full_tree(closure)[0]=={'PRELAUNCH_SOURCE.py','PRELAUNCH.json','stdout.bin','stderr.bin','CAPTURE.json'},'actual separate source closure five-member topology')
    closure_capture=parse(plain(closure/'CAPTURE.json'))
    check(closure_capture['actual_execution'] is True and closure_capture['completed'] is True and type(closure_capture['exit_code']) is int and closure_capture['exit_code']==0,'actual source closure completed child')
    for channel in ['stdout','stderr']: observe(closure_capture[channel],closure,'source_closure_complete_stream')
    check(not plain(closure/'stderr.bin'),'source closure stderr empty')
    snapshot=parse(plain(A/pins['snapshot_manifest']['path'])); originals={}
    head='a39d178b10f75fb127058b08e0d0002b3ae97f8a'; base='c6975ca76f9f667f1250ba403d0e6da2aafe14d0'
    for row in snapshot['files']:
        name=path_token(row['relative_path']); body=plain(A/'source_snapshot'/name); originals[name]=body
        check(sha(body)==row['sha256'] and len(body)==row['bytes'] and stat.S_IMODE((A/'source_snapshot'/name).stat().st_mode)==0o444,'exact original13 source body')
        check(git(['show',head+':'+row['path']])==body,'original Git complete body')
        check(git(['ls-tree',head,'--',row['path']]).decode().strip()=='100644 blob '+row['git_object']+'\t'+row['path'],'original Git object mode')
    check(full_tree(A/'source_snapshot')[0]==set(originals) and len(originals)==13,'complete original13 topology')
    tree=git(['ls-tree','-r','-z',head,'--','unsolved_math_prioritization/attempts/30004438/']).decode()
    check({e.split('\t',1)[1] for e in tree.split('\0') if e}=={'unsolved_math_prioritization/attempts/30004438/'+n for n in originals},'full original Git tree')
    metadata=parse(plain(A/pins['original_metadata']['path'])); diff=observe(metadata['full_diff'],role='whole_original_diff')
    check(len(diff)==89103 and sha(diff)=='944d6ac424b3e6fa6d4ccf163e6b381352072589528a3a5a29b146454e458209' and git(['diff','--no-ext-diff','--no-textconv','--binary',base,head,'--'])==diff,'entire original14-path diff')
    check(git(['diff','--name-only',base,head]).decode().splitlines()==[r['path'] for r in metadata['all_changed_paths']] and len(metadata['all_changed_paths'])==14,'all14 original changed paths')
    ledger=parse(originals['turns.json']); raw_source=parse(originals['source_record.json'])
    check(type(ledger) is dict and type(ledger['substantive_turns_used']) is int and ledger['substantive_turns_used']==0 and type(ledger['source_verification_responses']) is int and ledger['source_verification_responses']==1 and type(ledger['turn_limit']) is int and ledger['turn_limit']==5,'object original turns0/5 response1')
    check(type(raw_source) is dict and type(raw_source['id']) is int and raw_source['id']==30004438 and 'problem' not in raw_source,'plain raw source record not wrapper')
    for name in ['DRAFT_ROOT_READ_LEDGER.json','DRAFT_ROOT_SCIENCE_CARD.json']:
        draft=parse(plain(P/name)); check(draft['reading_completed'] is False and len(draft['root_flags'])==9 and all(v is False for v in draft['root_flags'].values()) and draft['created_utc'] is None,'false/null reading draft')
    for name in ['DRAFT_ROOT_EVIDENCE_BINDINGS.json','DRAFT_ROOT_CURRENT_INPUT_PREIMAGES.json']:
        draft=parse(plain(P/name)); check(draft['approved_by_root'] is False and draft['created_utc'] is None,'false/null prerequisite draft')
    check(b'ROOT_SCOPE_ACCEPTED_EXACT_KNOWN_RESULT_ONLY' not in plain(P/'DRAFT_ROOT_CURRENT_KNOWN_RESULT_SCOPE_CERTIFICATE.md'),'draft no actual acceptance sentinel')
    # Independent adversarial boundary controls; production is never evaluated.
    good={'path':'one/member','bytes':0,'sha256':'a'*64}; check(row_tokens([good])=={'one/member'},'valid exact typed row')
    for token in ['', '.', '..', '/one', 'one/', 'one//member', 'one/./member', 'one/../member', '.git/one', 'one/__pycache__/member', 'one\\member', 'one\0member', 1, True, None]: want_rejection(lambda t=token:path_token(t),'reject private path '+repr(token))
    for bad in [None,{},[dict(good,bytes=True)],[dict(good,bytes=False)],[dict(good,bytes=0.0)],[dict(good,bytes=-1)],[dict(good,sha256='A'*64)],[dict(good,extra=0)],[good,good]]: want_rejection(lambda x=bad:row_tokens(x),'reject private row '+repr(bad))
    for body in ['{"a":1,"a":2}','{"a":{"b":1,"b":2}}','NaN','Infinity','-Infinity','1e309']: want_rejection(lambda b=body:parse(b),'reject JSON '+body)
    check(not exact(True,1) and not exact(False,0) and not exact(None,0),'serialized scalar type identity')
    for mode in range(4096): check((mode==0o444)==(mode in {292}),'full mode '+format(mode,'04o'))
    fixture=F/'PRIVATE_FIXTURES'; fixture.mkdir()
    os_observations=[]
    for mode in [0o444,0o1444,0o2444,0o4444,0o644,0o755,0o7777]:
        q=fixture/('mode_'+format(mode,'04o')); q.write_bytes(b'private mode fixture\n'); q.chmod(mode); got=stat.S_IMODE(q.stat().st_mode)
        check(got==mode and (got==0o444)==(mode==0o444),'actual private full mode '+format(mode,'04o'))
        os_observations.append({'name':q.name,'dated_full_mode':got,'accepted':got==0o444}); q.chmod(0o444)
    treefixture=fixture/'tree'; treefixture.mkdir(); (treefixture/'member').write_bytes(b'private topology member\n')
    check(full_tree(treefixture)[0]=={'member'},'valid private recursive closure')
    (treefixture/'empty').mkdir(); want_rejection(lambda:full_tree(treefixture),'actual empty directory rejection'); (treefixture/'empty').rmdir()
    (treefixture/'link').symlink_to('member'); want_rejection(lambda:full_tree(treefixture),'actual member symlink rejection'); (treefixture/'link').unlink()
    os.mkfifo(treefixture/'fifo'); want_rejection(lambda:full_tree(treefixture),'actual FIFO rejection'); (treefixture/'fifo').unlink()
    alias=fixture/'alias'; alias.symlink_to(treefixture,target_is_directory=True); want_rejection(lambda:full_tree(alias),'actual root symlink rejection'); alias.unlink()
    stage=fixture/'rename_stage'; stage.mkdir(); (stage/'member').write_bytes(b'private rename payload\n'); destination=fixture/'rename_absent'; exclusive(stage,destination)
    check(not stage.exists() and plain(destination/'member')==b'private rename payload\n','actual absent-only rename success')
    refused=fixture/'rename_refused_stage'; refused.mkdir(); (refused/'member').write_bytes(b'private refused payload\n'); sentinel=sha(plain(destination/'member'))
    want_rejection(lambda:exclusive(refused,destination),'actual exclusive rename existing refusal')
    check(sha(plain(destination/'member'))==sentinel and plain(refused/'member')==b'private refused payload\n','actual exclusive refusal retains both bodies')
    queue=plain(R/'unsolved_math_prioritization/QUEUE.md'); prospective,before,after=toy_queue(queue)
    check(all(before[i]==after[i] for i in range(len(before)) if i not in {8,9,11}),'native queue private named cells only')
    check(before[10]==after[10] and before[12]==after[12],'queue Chat DOI byte preservation')
    target=[line for line in queue.splitlines(keepends=True) if b'| 30004438 / OWR-17475-003 |' in line][0]
    want_rejection(lambda:toy_queue(queue+target),'duplicate target queue rejected')
    check(prospective!=queue and queue==plain(R/'unsolved_math_prioritization/QUEUE.md'),'private prospective never writes native queue')
    after_native=native_rows(); after_head=git(['rev-parse','HEAD']).decode().strip()
    check(git(['branch','--show-current']).strip()==b'main','main after')
    check(before_native==after_native and before_head==after_head,'native13 bytes/full modes/main HEAD unchanged before after')
    check(plain(P/'prepare_current_packet.py')==source and plain(P/'capture_root_builder_operation.py')==operator,'operative production bytes unchanged after private controls')
    result={'schema':'PR46_CURRENT_SOURCE_ADVERSARY_PRIVATE_AUDIT_v1','status':'PASS_SCOPED_PRIVATE_SOURCE_AUDIT','started_utc':start,'finished_utc':now(),'pid':os.getpid(),'parent_pid':os.getppid(),'assertions':len(CHECKS),'all_assertion_labels':CHECKS,'all4096_full_modes_tested':True,'production_import_compile_or_execution':False,'own_operations_only':True,'full_recursive_preparation_member_count':60,'preparation_manifest_sha256':sha(plain(P/'PREPARATION_MANIFEST.json')),'builder_sha256':sha(source),'operator_sha256':sha(operator),'source_closure_external_capture':closure_capture,'first_party_input_reads':sorted(READS.values(),key=lambda x:x['path']),'family_boundaries':families,'original_substantive_attempts':0,'original_source_verification_responses':1,'new_substantive_attempts':0,'audit_turns':0,'before_native13':before_native,'after_native13':after_native,'before_main_head':before_head,'after_main_head':after_head,'dated_actual_mode_observations':os_observations,'temporary_expected_rejection_symlink_fifo_empty_directory_removed_after_recording':True,'private_control_proves_production_runtime':False,'current_freeze_or_whole_acceptance_certified':False,'foreign_PDF_text_rawcache_SQL_access_headers_copied':False}
    emit(F/'PRIVATE_AUDIT_RESULTS.json',result)
    print(json.dumps({k:result[k] for k in ['status','assertions','all4096_full_modes_tested','production_import_compile_or_execution','preparation_manifest_sha256','builder_sha256','operator_sha256','current_freeze_or_whole_acceptance_certified']},sort_keys=True))

if __name__=='__main__': run()
