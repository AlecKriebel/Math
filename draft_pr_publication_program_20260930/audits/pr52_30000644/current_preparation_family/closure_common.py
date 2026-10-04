"""Only this bounded private SOURCE packet and its read-only input bindings."""
from pathlib import Path
from datetime import datetime
import hashlib,json,stat

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
SELF='SELF_MANIFEST.json'
COUNTER=[0]
def require(test,message):
    if not test:raise AssertionError(message)
    COUNTER[0]+=1
def sha(body):return hashlib.sha256(body).hexdigest()
def bind(p,relative=False,mode=None):
    p=Path(p);st=p.lstat()
    require(stat.S_ISREG(st.st_mode) and not p.is_symlink() and st.st_nlink==1,'single regular file '+str(p))
    b=p.read_bytes()
    return {'path':p.relative_to(HERE).as_posix() if relative else str(p),
            'bytes':len(b),'sha256':sha(b),'mode':mode or format(stat.S_IMODE(st.st_mode),'04o')}
def load(p):return json.loads(Path(p).read_bytes())
def external():
    evidence=load(HERE/'EXTERNAL_BINDINGS.json')
    names=[r['path'] for r in evidence['files']]
    require(names==sorted(set(names)),'unique sorted in-place external rows')
    for row in evidence['files']:
        require(bind(Path(row['path']))==row,'complete external body and full mode '+row['path'])
    family_counts=[]
    for f in evidence['closed_families']:
        home=Path(f['path']);manifest=load(home/SELF)
        require(bind(home/SELF)==f['manifest'],'exact actual closed manifest')
        require(manifest['schema']==f['schema'],'literal predecessor schema')
        records=manifest['files'] if f['schema']=='pr52-divergence-shear-self-closure-v1' else manifest['file_bindings']
        full=[]
        for row in records:
            p=Path(row['path'])
            if not p.is_absolute():p=home/p
            observed=bind(p)
            require(observed['bytes']==row['bytes'] and observed['sha256']==row['sha256'],'literal closed payload body')
            mode=format(row['mode'],'04o') if isinstance(row['mode'],int) else row['mode']
            require(observed['mode']==mode,'literal closed payload full mode')
            full.append(str(p))
        actual=sorted(str(p) for p in home.rglob('*') if p.is_file())
        require(actual==sorted(full+[str(home/SELF)]),'whole predecessor exact file set')
        dirs=[home]+sorted(p for p in home.rglob('*') if p.is_dir())
        actual_dirs=[{'path':str(p),'mode':format(stat.S_IMODE(p.stat().st_mode),'04o')} for p in dirs]
        require(actual_dirs==f['directories'],'whole predecessor directory set and full modes')
        require(len(full)==f['payload_files'],'whole predecessor count')
        family_counts.append(len(full))
    require(family_counts==[194,27,25],'exact three predecessor payload counts')
    caps=evidence['actual_ROOT_captures']
    require(len(caps)==6 and len({c['path'] for c in caps})==6,'six distinct actual ROOT CAP4s')
    for c in caps:
        home=Path(c['path']);cap=load(home/'CAPTURE.json')
        require(cap['schema']=='root-explicit-command-capture/v1','literal CAP4 schema')
        require(cap['actual_execution'] is True and cap['completed'] is True and cap['exit_code']==0 and cap['status']=='PASS','actual ROOT successful completion')
        require(cap['pid']==c['actual_pid'] and cap['pid']>0,'literal actual PID')
        require(cap['argv']==c['argv'] and cap['cwd']=='/Users/alec/Documents/Math','literal argv/cwd')
        require(cap['operator_unchanged'] is True,'actual operator unchanged')
        require(sha((home/'prelaunch_operator.py').read_bytes())==cap['operator_sha256'],'complete prelaunch ROOT operator')
        for stream in ('stdout','stderr'):
            b=(home/(stream+'.bin')).read_bytes()
            require(len(b)==cap[stream]['bytes'] and sha(b)==cap[stream]['sha256'],'complete actual ROOT '+stream)
        require((home/'stderr.bin').read_bytes()==b'','complete empty ROOT stderr')
        require(load(home/'stdout.bin')==c['stdout_typed'],'entire ROOT stdout values/types')
        require(datetime.fromisoformat(cap['started_utc'])<=datetime.fromisoformat(cap['finished_utc']),'actual ROOT chronological interval')
        require(bind(Path(cap['argv'][2]))==c['invoked_source'],'whole actual invoked source')
    for i in range(0,6,2):
        closer=load(Path(caps[i]['path'])/'CAPTURE.json')
        reader=load(Path(caps[i+1]['path'])/'CAPTURE.json')
        require(datetime.fromisoformat(closer['finished_utc'])<datetime.fromisoformat(reader['started_utc']),'separate reader after closer exit')
    return len(evidence['files'])
def science():
    value=load(HERE/'SCIENCE_INDEX.json')
    require(value['original_head']=='d40d2dae4cff2a5e5a1e12e9a2f8bc3987431c1a','original head')
    require(len(value['original_archive'])==19 and len(value['operative'])==20,'lean science count')
    for row in value['original_archive']:
        p=HERE/row['path'];b=p.read_bytes()
        observed=bind(p,True)
        for k in ('bytes','sha256'):require(observed[k]==row[k],'complete original archive')
        require(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==row['git_blob_sha1'],'original full Git blob')
    archive=HERE/'original_head_archive';current=HERE/'current_science'
    require(sorted(p.relative_to(archive).as_posix() for p in archive.rglob('*') if p.is_file())==[r['relative_path'] for r in value['original_archive']],'whole original archive set')
    require(sorted(p.relative_to(current).as_posix() for p in current.rglob('*') if p.is_file())==[r['relative_path'] for r in value['operative']],'whole operative set')
    for row in value['operative']:
        p=HERE/row['path'];observed=bind(p,True)
        for k in ('bytes','sha256'):require(observed[k]==row[k],'complete operative science')
        original=archive/row['relative_path']
        if row['change']=='retained_literal':require(p.read_bytes()==original.read_bytes(),'retained literal body')
    for name in ('KNOWN_THEOREM.md','review/KNOWN_THEOREM.md'):
        a=(archive/name).read_text();c=(current/name).read_text()
        marker='## 1. Statement and conventions'
        require(marker in a and c[c.index(marker):]==a[a.index(marker):],'entire mathematical proof unchanged')
    source=load(current/'source_record.json');old=load(archive/'source_record.json')
    for k in ('id','problem_number','statement','original_statement','clean_statement'):
        require(source[k]==old[k] and type(source[k]) is type(old[k]),'exact literal problem scope/type')
    require(source['status']=='already_solved','operative source status corrected')
    turns=load(current/'turns.json');attempt=load(current/'attempt.json')
    require(turns['substantive_search_attempts']==0 and len(turns['validation_activities'])==1,'literal zero search plus one validation')
    require(attempt['substantive_attempts_used']==0 and attempt['substantive_attempt_limit']==5,'literal 0/5')
    require((current/'prior_report.json').read_bytes()==b'null\n','literal original absence display retained')
    quals=load(current/'GLOBAL_QUALIFICATIONS.json')
    require(quals['raw_prior_key_present'] is False and quals['selected_sql_report_text']=='{}' and quals['selected_sql_report_is_SQL_NULL'] is False,'exact absent/raw SQL distinction')
    require(quals['original_prior_report_decoded'] is None and quals['original_response_count_supplied'] is False,'no invented original count')
    require(quals['new_independent_mathematical_family'] is False and quals['ROOT_acceptance_authority'] is False,'reused source preparer only')
    return 39
def builder_capture():
    home=HERE/'builder_capture';cap=load(home/'CAPTURE.json')
    require(cap['exit_code']==0 and cap['source_unchanged_after'] is True and cap['operator_unchanged_after'] is True,'actual private builder success')
    require(cap['argv']==['/usr/bin/python3','-B',str(HERE/'build_current.py')],'literal builder argv')
    require(cap['cwd']==str(HERE) and cap['child_pid']>0,'literal builder cwd/actual PID')
    require(datetime.fromisoformat(cap['utc_start'])<=datetime.fromisoformat(cap['utc_end']),'builder actual UTC interval')
    require((home/'prelaunch_build_current.py').read_bytes()==(HERE/'build_current.py').read_bytes(),'complete builder prelaunch source')
    require((home/'prelaunch_operator.py').read_bytes()==(HERE/'capture_builder.py').read_bytes(),'complete private operator')
    for stream in ('stdout','stderr'):
        body=(home/(stream+'.bin')).read_bytes()
        require(cap[stream]=={'bytes':len(body),'sha256':sha(body)},'complete private '+stream)
    require((home/'stderr.bin').read_bytes()==b'','empty private builder stderr')
    require(load(home/'stdout.bin')==load(HERE/'PREPARATION_READBACK.json'),'typed actual builder full stdout')
    return cap
def inspect(closed):
    index=load(HERE/'INDEX.json');ready=load(HERE/'READY.json')
    require(index['schema']=='pr52-current-lean-index/v1' and index['future_authority'] is False,'literal current index scope')
    rows=index['files'];names=[r['path'] for r in rows]
    require(names==sorted(set(names)),'unique sorted fixed payload')
    expected=names+['INDEX.json','READY.json']+([SELF] if closed else [])
    actual=sorted(p.relative_to(HERE).as_posix() for p in HERE.rglob('*') if p.is_file())
    require(actual==sorted(expected),'entire current packet exact file set')
    for row in rows:require(bind(HERE/row['path'],True)==row,'whole frozen current payload')
    require(ready['index']==bind(HERE/'INDEX.json',True),'literal whole current index binding')
    for p in HERE.rglob('*'):
        require(not p.is_symlink(),'no current symlinks')
        if p.is_file():require(stat.S_IMODE(p.stat().st_mode)==0o444,'whole current full file modes')
    dirs=[HERE]+sorted(p for p in HERE.rglob('*') if p.is_dir())
    require([{'path':'.' if p==HERE else p.relative_to(HERE).as_posix(),'mode':format(stat.S_IMODE(p.stat().st_mode),'04o')} for p in dirs]==index['directories'],'whole current dirs and full modes')
    require(all(stat.S_IMODE(p.stat().st_mode)==0o555 for p in dirs),'current directories full 0555')
    require(ready['ROOT_closure_performed'] is False and ready['SELF_manifest_absent_when_prepared'] is True,'honest current SOURCE-only preparation')
    count=external();science_count=science();cap=builder_capture()
    verdict=load(HERE/'VERDICT.json')
    require(verdict['new_independent_mathematical_verdict'] is False and verdict['ROOT_approval'] is False and verdict['native_acceptance'] is False,'no new verdict/approval')
    require(verdict['recommended_status']=='already_solved' and verdict['new_paper'] is False,'credited prior result treatment')
    return {'schema':'pr52-current-lean-inspection-v1','status':'PASS_SOURCE_PREPARATION_ONLY',
            'science_files':science_count,'fixed_payload_files_without_self':len(names)+2,
            'external_full_body_rows':count,'actual_builder_child_pid':cap['child_pid'],
            'ROOT_or_native_authority':False,'closed':closed}
