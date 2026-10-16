#!/usr/bin/env python3
"""PR66 pinned source custody; executes no submitted scientific code."""
import base64
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path('/Users/alec/Documents/Math')
HERE = Path(__file__).resolve().parent
HEAD = '78f4a7fadac0fd24e147a617956cb409eb6a579e'
REPO = 'AlecKriebel/Math'
PR = 66
TARGET = '10400033'
ATTEMPT = 'unsolved_math_prioritization/attempts/' + TARGET + '/'
ORIGINAL = HERE / 'original'
COMMANDS = HERE / 'ACTUAL_COMMANDS.jsonl'

def utc():
    return dt.datetime.now(dt.timezone.utc).isoformat()

def sha256(body):
    return hashlib.sha256(body).hexdigest()

def git_digest(kind, body):
    return hashlib.sha1(kind.encode() + b' ' + str(len(body)).encode() + b'\0' + body).hexdigest()

def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')

def log(message, percent):
    with (HERE/'RESEARCH_LOG.md').open('a') as out:
        out.write(f'\n## {utc()} — Custody checkpoint\n\nCompletion estimate: {percent}%. {message}\n')

def run(label, argv, required=True):
    (HERE/'commands').mkdir(exist_ok=True)
    if (HERE/'commands'/f'{label}.stdout').exists():
        original_label=label
        retry=1
        while (HERE/'commands'/f'{label}.stdout').exists():
            label=f'{original_label}_retry_{retry}'
            retry+=1
    start = utc()
    proc = subprocess.Popen(argv, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    end = utc()
    record = dict(label=label, argv=argv, actual_pid=proc.pid, cwd=str(ROOT),
        started_UTC=start, finished_UTC=end, exit_code=proc.returncode)
    for name, body in [('stdout',out),('stderr',err)]:
        path = HERE/'commands'/f'{label}.{name}'
        path.write_bytes(body)
        record.update({name+'_path':str(path.relative_to(HERE)),name+'_bytes':len(body),name+'_sha256':sha256(body)})
    with COMMANDS.open('a') as stream:
        stream.write(json.dumps(record, ensure_ascii=False)+'\n')
    if proc.returncode and required:
        raise RuntimeError(f'{label} failed; retained exact stdout and stderr')
    return out, proc.returncode

def api(label, endpoint):
    out, _ = run(label, ['gh','api',endpoint])
    return json.loads(out)

def keep(path, body, expected, mode=None):
    actual = git_digest('blob',body)
    if actual != expected:
        raise RuntimeError(f'Blob digest mismatch for {path}')
    dest = ORIGINAL/path
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and dest.read_bytes()!=body:
        raise RuntimeError(f'Immutable retained input differs: {path}')
    dest.write_bytes(body)
    return dict(path=path,mode=mode,git_blob_SHA1=expected,computed_git_blob_SHA1=actual,
        bytes=len(body),sha256=sha256(body),retained_path=str(dest.relative_to(HERE)))

def blob(label, entry):
    value = api(label,f'repos/{REPO}/git/blobs/{entry["sha"]}')
    if value.get('encoding')!='base64' or value.get('sha')!=entry['sha']:
        raise RuntimeError(f'Unexpected immutable blob response: {entry["path"]}')
    body = base64.b64decode(value['content'],validate=False)
    if len(body)!=value['size'] or len(body)!=entry['size']:
        raise RuntimeError(f'Byte count mismatch: {entry["path"]}')
    return keep(entry['path'],body,entry['sha'],entry['mode'])

def read_json(name):
    return json.loads((HERE/name).read_text())

def intake():
    if (HERE/'INITIAL_LITERAL_STATUS.json').exists():
        raise RuntimeError('Initial gate already recorded; do not overwrite')
    if not (HERE/'RESEARCH_LOG.md').exists():
        (HERE/'RESEARCH_LOG.md').write_text('# PR66 source custody research log\n\nSource retrieval and authentication only; mathematical verdict remains ROOT.\n')
    local_head, _ = run('000_local_HEAD',['git','rev-parse','HEAD'])
    branch, _ = run('001_local_branch',['git','branch','--show-current'])
    status, _ = run('002_scoped_status',['git','status','--porcelain=v1','--untracked-files=no','--',
        'AGENTS.md','unsolved_math_prioritization/AGENTS.md','unsolved_math_prioritization/QUEUE.md',ATTEMPT])
    snapshot = []
    local_paths = [ROOT/'AGENTS.md',ROOT/'unsolved_math_prioritization/AGENTS.md',ROOT/'unsolved_math_prioritization/QUEUE.md']
    if (ROOT/ATTEMPT).is_dir():
        local_paths += sorted(p for p in (ROOT/ATTEMPT).rglob('*') if p.is_file())
    for path in local_paths:
        item = dict(path=str(path.relative_to(ROOT)),presence='present' if path.is_file() else 'absent')
        if path.is_file():
            body=path.read_bytes()
            item.update(bytes=len(body),sha256=sha256(body),lstat_mode=oct(path.lstat().st_mode))
        snapshot.append(item)
    write_json(HERE/'SOURCE_PRELAUNCH_SNAPSHOT.json',dict(UTC=utc(),controller_pid=os.getpid(),
        local_HEAD=local_head.decode().strip(),branch=branch.decode().strip(),scoped_tracked_status=status.decode(),
        scoped_status_only=True,local_file_hashes=snapshot,science_contents_opened=False))
    if branch.decode().strip()!='main':
        raise RuntimeError('Not main; no branch changes authorized')
    log('Captured main, HEAD, scoped tracked status, and hashes of relevant local inputs. Target scientific bodies were not opened.',5)
    meta_out,_=run('003_fresh_PR66_metadata',['gh','pr','view',str(PR),'--repo',REPO,'--json',
        'number,state,isDraft,headRefOid,headRefName,baseRefName,url,title'])
    meta=json.loads(meta_out)
    if meta['number']!=PR or meta['state']!='OPEN' or meta['isDraft'] is not True or meta['headRefOid']!=HEAD or meta['headRefName']!='dot/math-10400033' or meta['baseRefName']!='main':
        raise RuntimeError('Fresh exact draft/open/head/branch gate failed')
    queue=api('004_fresh_submitted_QUEUE',f'repos/{REPO}/contents/unsolved_math_prioritization/QUEUE.md?ref={HEAD}')
    if queue.get('encoding')!='base64':
        raise RuntimeError('QUEUE has no complete base64 body')
    body=base64.b64decode(queue['content'])
    item=keep('unsolved_math_prioritization/QUEUE.md',body,queue['sha'])
    rows=[s for s in body.decode().splitlines() if s.startswith('|') and any(
        c.strip().split(' / ',1)[0]==TARGET for c in s.split('|')[1:-1])]
    if len(rows)!=1:
        raise RuntimeError(f'QUEUE target row count is {len(rows)}')
    columns=[part.strip() for part in rows[0].split('|')[1:-1]]
    if 'claimed_solved' not in columns or '1/5' not in columns:
        raise RuntimeError('Fresh QUEUE literal claimed_solved 1/5 gate failed')
    write_json(HERE/'INITIAL_LITERAL_STATUS.json',dict(UTC=utc(),metadata=meta,gate_passed=True,
        literal_status='claimed_solved',literal_budget='1/5',literal_row=rows[0],
        literal_row_sha256=sha256(rows[0].encode()),QUEUE=item,scientific_source_opened_before_gate=False))
    log('Fresh GitHub PR66 was OPEN draft at the required head and branch. The pinned complete QUEUE contains literal claimed_solved and 1/5. The science read gate passed.',20)
    commit=api('005_original_git_commit',f'repos/{REPO}/git/commits/{HEAD}')
    if commit['sha']!=HEAD:
        raise RuntimeError('Original commit API SHA mismatch')
    tree=api('006_original_recursive_tree',f'repos/{REPO}/git/trees/{commit["tree"]["sha"]}?recursive=1')
    if tree.get('truncated') is not False or tree['sha']!=commit['tree']['sha']:
        raise RuntimeError('Original recursive tree missing or truncated')
    files=[]
    page=1
    while True:
        batch=api(f'007_changed_files_page_{page:03}',f'repos/{REPO}/pulls/{PR}/files?per_page=100&page={page}')
        if not isinstance(batch,list):
            raise RuntimeError('Unexpected PR changed files representation')
        files.extend(batch)
        if len(batch)<100:
            break
        page+=1
        if page>100:
            raise RuntimeError('Unexpected pagination size; no completeness assertion')
    write_json(HERE/'ORIGINAL_GIT_COMMIT.json',commit)
    write_json(HERE/'ORIGINAL_RECURSIVE_TREE.json',tree)
    write_json(HERE/'INCOMING_CHANGED_DOMAIN.json',dict(UTC=utc(),head=HEAD,files=files,count=len(files),pagination_complete=True))
    entries=[e for e in tree['tree'] if e['path'].startswith(ATTEMPT)]
    write_json(HERE/'TARGET_ATTEMPT_TREE.json',entries)
    print(json.dumps({'gate':'PASSED','head':HEAD,'tree':tree['sha'],'attempt_entries':entries,'changed_count':len(files)},indent=2),flush=True)

def attempt():
    gate=read_json('INITIAL_LITERAL_STATUS.json')
    if gate.get('gate_passed') is not True or gate['metadata']['headRefOid']!=HEAD:
        raise RuntimeError('No successful gate for this head')
    entries=[e for e in read_json('TARGET_ATTEMPT_TREE.json') if e['type']=='blob']
    if not entries or any(e['mode'] not in ('100644','100755') for e in entries):
        raise RuntimeError('No regular complete attempt tree')
    ordered=sorted(entries,key=lambda e:(0 if e['path'].endswith('/CANDIDATE.md') else 1 if e['path'].endswith('/source_record.json') else 2,e['path']))
    artifacts=[blob(f'008_attempt_blob_{i:03}',e) for i,e in enumerate(ordered)]
    write_json(HERE/'ORIGINAL_ATTEMPT_BLOBS.json',artifacts)
    log(f'Authenticated and preserved all {len(artifacts)} target attempt bodies, including CANDIDATE.md and complete source_record.json. Source authentication remains distinct from mathematical judgment.',65)
    print(json.dumps({'all_original_attempt_bodies_authenticated':True,'artifact_count':len(artifacts),'artifacts':artifacts},indent=2),flush=True)

def provenance():
    tree=read_json('ORIGINAL_RECURSIVE_TREE.json')
    bypath={e['path']:e for e in tree['tree']}
    selected=['AGENTS.md','unsolved_math_prioritization/AGENTS.md','unsolved_math_prioritization/attempts/AGENTS.md','unsolved_math_prioritization/manifest.json',
        'unsolved_math_prioritization/state.json','unsolved_math_prioritization/history.jsonl','unsolved_math_prioritization/queue.py']
    artifacts=[]
    for i,path in enumerate(selected):
        entry=bypath.get(path)
        if entry is None:
            artifacts.append(dict(path=path,presence='absent'))
        elif entry['type']!='blob' or entry['mode'] not in ('100644','100755'):
            raise RuntimeError(f'Nonregular provenance file: {path}')
        else:
            artifacts.append(blob(f'009_provenance_blob_{i:03}',entry))
    write_json(HERE/'ORIGINAL_PROVENANCE_BLOBS.json',artifacts)
    log('Preserved tracked source manifest, instruction bodies, state/history, and queue implementation where present; absence remains a distinct recorded state.',80)
    print(json.dumps({'provenance':artifacts},indent=2),flush=True)

def tree_check(tree):
    directories={'':tree['sha']}
    children={}
    for e in tree['tree']:
        parent,_,name=e['path'].rpartition('/')
        children.setdefault(parent,[]).append((name,e))
        if e['type']=='tree':
            directories[e['path']]=e['sha']
    checked=[]
    for directory,expected in sorted(directories.items()):
        direct=children.get(directory,[])
        ordered=sorted(direct,key=lambda x:(x[0]+('/' if x[1]['type']=='tree' else '')).encode())
        body=b''.join((e['mode'].lstrip('0')+' '+name).encode()+b'\0'+bytes.fromhex(e['sha']) for name,e in ordered)
        actual=git_digest('tree',body)
        if actual!=expected:
            raise RuntimeError(f'Tree serialization mismatch: {directory}')
        checked.append(dict(path=directory or '/',git_tree_SHA1=actual,serialized_bytes=len(body),sha256=sha256(body),direct_entry_count=len(direct)))
    return dict(all_match=True,root_tree_SHA1=tree['sha'],directory_count=len(checked),directories=checked)

def commit_check(commit):
    body,code=run('010_local_exact_commit_body',['git','cat-file','commit',HEAD],required=False)
    if code==0:
        if git_digest('commit',body)!=HEAD:
            raise RuntimeError('Local raw commit digest mismatch')
        method='Read-only git cat-file of existing local exact commit object; full Git digest matched.'
        recovered=True
    else:
        recovered=False
        base='tree '+commit['tree']['sha']+'\n'+''.join('parent '+p['sha']+'\n' for p in commit['parents'])
        people={}
        for role in ('author','committer'):
            p=commit[role]
            stamp=int(dt.datetime.fromisoformat(p['date'].replace('Z','+00:00')).timestamp())
            people[role]=f'{role} {p["name"]} <{p["email"]}> {stamp}'
        for minute in range(-12*60,14*60+1):
            tz=('-' if minute<0 else '+')+f'{abs(minute)//60:02}{abs(minute)%60:02}'
            for ending in ('\n',''):
                candidate=(base+people['author']+' '+tz+'\n'+people['committer']+' '+tz+'\n\n'+commit['message']+ending).encode()
                if git_digest('commit',candidate)==HEAD:
                    body=candidate
                    recovered=True
                    method='API-field reconstruction with timezone enumeration; full original Git digest matched.'
                    break
            if recovered:
                break
    if recovered:
        dest=HERE/'ORIGINAL_GIT_COMMIT_BODY.bin'
        dest.write_bytes(body)
        return dict(original_serialization_recovered=True,computed_git_commit_SHA1=git_digest('commit',body),
            bytes=len(body),sha256=sha256(body),retained_path=dest.name,method=method)
    return dict(original_serialization_recovered=False,computed_git_commit_SHA1=None,
        authenticated_via='Pinned immutable GitHub git/commits JSON; root tree independently authenticated.',
        limitation='Raw object absent locally; API normalizes timestamps and may omit headers. Equal-offset candidate enumeration did not match; exact commit bytes are not claimed.')

def type_shape(value):
    if value is None:
        return dict(JSON_type='null',value=None)
    if isinstance(value,dict):
        return dict(JSON_type='object',is_empty_object=value=={},keys={k:type_shape(v) for k,v in value.items()})
    if isinstance(value,list):
        return dict(JSON_type='array',length=len(value),items=[type_shape(v) for v in value])
    if isinstance(value,bool):
        kind='boolean'
    elif isinstance(value,int):
        kind='integer'
    elif isinstance(value,float):
        kind='number'
    else:
        kind='string'
    return dict(JSON_type=kind,value=value)

def field_state(obj,key):
    return dict(presence='absent') if key not in obj else dict(presence='present',shape=type_shape(obj[key]))

def inspect():
    selected=['source_record.json','status.json','turns.jsonl','source_manifest.json']
    for name in selected:
        body=(ORIGINAL/(ATTEMPT+name)).read_bytes()
        print(json.dumps({'path':ATTEMPT+name,'bytes':len(body),'sha256':sha256(body),'body':body.decode()},ensure_ascii=False),flush=True)
    print(json.dumps({'path':'unsolved_math_prioritization/manifest.json',
        'body':(ORIGINAL/'unsolved_math_prioritization/manifest.json').read_text()},ensure_ascii=False),flush=True)

def supplement():
    # Retain new, genuinely instrumented replays; do not claim they supply the
    # unavailable PID or UTC for the earlier shell-tool inspection.
    reference='draft_pr_publication_program_20260930/audits/pr65_2305051/original_source_authentication_20261004/retrieve_original.py'
    ref_body,_=run('013_algorithm_reference_replay',['cat',reference])
    intake_path='draft_pr_publication_program_20260930/ordered_intake_20261004/after_PR65/INTAKE_AFTER_PR65.json'
    intake_body,_=run('014_parent_intake_reference_replay',['cat',intake_path])
    remote_body,_=run('015_remote_identity_replay',['git','remote','-v'])
    observations=[
        dict(requested_shell_command="pwd; git branch --show-current; rg --files draft_pr_publication_program_20260930 | rg 'retrieve_original.py$|INTAKE_AFTER_PR65.json$|pr66'",
            tool_chunk_id='750a8f',exit_code=0,tool_output_state='Full combined tool output remains in conversation history; not transplanted from PR65.',
            purpose='Read-only discovery and branch observation'),
        dict(requested_shell_command='cat '+reference,tool_chunk_id='754749',exit_code=0,
            output_retention='Initial body in tool conversation history; subsequent fully instrumented body retained as commands/013_algorithm_reference_replay.stdout.',
            subsequent_body_bytes=len(ref_body),subsequent_body_sha256=sha256(ref_body),
            purpose='Read-only algorithm reference, with all PR66 predicates and file counts independently derived'),
        dict(requested_shell_command='cat '+intake_path,tool_chunk_id='b02065',exit_code=0,
            output_retention='Initial body in tool conversation history; subsequent fully instrumented body retained as commands/014_parent_intake_reference_replay.stdout.',
            subsequent_body_bytes=len(intake_body),subsequent_body_sha256=sha256(intake_body),purpose='Parent eligibility observation reference only'),
        dict(requested_shell_command='git remote -v',tool_chunk_id='ba5a89',exit_code=0,
            observed_combined_output='origin\thttps://github.com/AlecKriebel/Math.git (fetch)\norigin\thttps://github.com/AlecKriebel/Math.git (push)\n',
            subsequent_body_sha256=sha256(remote_body),purpose='Read-only remote identity'),
        dict(requested_shell_command='rg \'10400033\' '+str((ORIGINAL/'unsolved_math_prioritization/QUEUE.md').relative_to(ROOT)),
            tool_chunk_id='e31a99',exit_code=0,
            observed_combined_output=read_json('INITIAL_LITERAL_STATUS.json')['literal_row']+'\n',
            purpose='Diagnose literal row parser after unsuccessful initial gate; no scientific body read')]
    for item in observations:
        item.update(cwd=str(ROOT),actual_shell_argv=None,actual_child_PID=None,actual_UTC=None,
            limitation='Shell-tool envelope did not expose child argv/PID/UTC or separate stdout/stderr. None are fabricated; later replays remain distinct executions.')
        if 'observed_combined_output' in item:
            encoded=item['observed_combined_output'].encode()
            item.update(observed_combined_bytes=len(encoded),observed_combined_sha256=sha256(encoded))
    write_json(HERE/'BOOTSTRAP_TOOL_OBSERVATIONS.json',dict(UTC=utc(),schema='PR66-own-bootstrap-observations/v1',
        observations=observations,bootstrap_facts_transplanted_from_other_PR=False,
        controller_launch_envelope_limitation='The Python custody phase processes were launched by exec_command. Its shell PID/argv and UTC are not exposed. The custody controller records its own PID in snapshots, failures, or final results; all its spawned children have complete exact execution records.',
        science_hash_only_before_gate='Prelaunch local files were read as raw bytes for hashes; no decoded scientific contents were inspected before the successful fresh gate.'))
    report_path=HERE/'ORIGINAL_AUTHENTICATION.json'
    report=read_json(report_path.name)
    records=[json.loads(line) for line in COMMANDS.read_text().splitlines()]
    source=json.loads((ORIGINAL/(ATTEMPT+'source_record.json')).read_text())
    status=json.loads((ORIGINAL/(ATTEMPT+'status.json')).read_text())
    review=(ORIGINAL/(ATTEMPT+'review/REVIEW.md')).read_bytes()
    if status.get('review_sha256')!=sha256(review):
        raise RuntimeError('Original status review digest differs from retained original review')
    declared=json.loads((ORIGINAL/(ATTEMPT+'source_manifest.json')).read_text())
    pdf_tree_entries=[e['path'] for e in read_json('TARGET_ATTEMPT_TREE.json') if e['type']=='blob' and e['path'].lower().endswith('.pdf')]
    report.update(actual_subprocess_count=len(records),actual_recorded_failures=[r for r in records if r['exit_code']!=0],
        source_record_native_prior_report_key='prior_upstream_report',
        source_record_native_prior_report_presence='present' if 'prior_upstream_report' in source else 'absent',
        original_review_sha256=sha256(review),original_status_review_digest_matched=True,
        external_PDF_custody=dict(declaration_count=len(declared.get('pdfs',[])),
            source_pdfs_redistributed=field_state(declared,'source_pdfs_redistributed'),
            PDF_blob_paths_in_target_tree=pdf_tree_entries,external_PDF_bodies_fetched=False,external_PDF_byte_hashes_authenticated=False,
            interpretation='Original source_manifest.json declarations authenticated; no external PDF byte custody claimed.'))
    write_json(report_path,report)
    failure=read_json('RETRIEVAL_FAILURE.json') if (HERE/'RETRIEVAL_FAILURE.json').exists() else None
    if failure:
        log(f'Retained initial gate-parser failure at {failure["UTC"]}: {failure["error"]}. The literal native-ID row parser was corrected, a fresh metadata/QUEUE gate rerun succeeded, and no scientific body was decoded before success.',100)
    log('Final supplement preserves honest bootstrap metadata gaps separately from fully instrumented child command executions. Status-to-candidate, ledger candidate-event, and status-to-original-review digest links match. External PDF declarations are authenticated without claiming downloaded PDF bytes.',100)
    md=HERE/'ORIGINAL_AUTHENTICATION.md'
    md.write_text(md.read_text()+f'\nThe native prior-report key is `prior_upstream_report` (present object); `upstream_report` is absent. The original ledger has three JSON events, all with `turn: 1`; `status.json` reports `turns_used: 1`. These event and substantive-turn counts remain distinct. The status review hash matches original `review/REVIEW.md` SHA256 `{sha256(review)}`. The external PDF manifest has {len(declared.get("pdfs",[]))} declarations and no target PDF blobs. An initial literal-row parser failure was preserved and followed by a successful fresh gate; see RETRIEVAL_FAILURE.json and RESEARCH_LOG.md.\n')
    seal()
    print(json.dumps({'tree_serialization_count':report['tree_serializations'],
        'commit_serialization':report['commit_serialization'],'original_turn_events':report['original_turn_numbers'],
        'actual_subprocess_count':len(records),'native_prior_report':'prior_upstream_report'},indent=2),flush=True)

def finalize():
    commit=read_json('ORIGINAL_GIT_COMMIT.json')
    tree=read_json('ORIGINAL_RECURSIVE_TREE.json')
    bypath={e['path']:e for e in tree['tree']}
    checked=tree_check(tree)
    write_json(HERE/'TREE_SERIALIZATION_AUTHENTICATION.json',checked)
    commit_auth=commit_check(commit)
    write_json(HERE/'COMMIT_SERIALIZATION_AUTHENTICATION.json',commit_auth)
    pr=api('011_final_PR66_metadata',f'repos/{REPO}/pulls/{PR}')
    if pr['head']['sha']!=HEAD or pr['state']!='open' or pr.get('draft') is not True:
        raise RuntimeError('Final PR66 draft/open/head gate failed')
    compare=api('012_immutable_changed_domain_compare',f'repos/{REPO}/compare/{pr["base"]["sha"]}...{HEAD}')
    incoming=read_json('INCOMING_CHANGED_DOMAIN.json')['files']
    paths=[f['filename'] for f in incoming]
    if len(paths)!=len(set(paths)) or set(paths)!={f['filename'] for f in compare['files']} or len(paths)!=pr['changed_files']:
        raise RuntimeError('Complete changed domain mismatch')
    attempt_paths={e['path'] for e in tree['tree'] if e['path'].startswith(ATTEMPT) and e['type']=='blob'}
    expected={'unsolved_math_prioritization/QUEUE.md'}|attempt_paths
    if set(paths)!=expected:
        raise RuntimeError('Changed domain is not precisely QUEUE plus complete target attempt; preserve for escalation')
    artifacts=[]
    for path in sorted(p for p in ORIGINAL.rglob('*') if p.is_file()):
        rel=str(path.relative_to(ORIGINAL))
        entry=bypath.get(rel)
        if not entry or entry['type']!='blob' or entry['mode'] not in ('100644','100755'):
            raise RuntimeError(f'Retained input is not regular: {rel}')
        item=keep(rel,path.read_bytes(),entry['sha'],entry['mode'])
        if item['bytes']!=entry['size']:
            raise RuntimeError(f'Retained byte count mismatch: {rel}')
        item['incoming_changed_domain']=rel in paths
        artifacts.append(item)
    for f in incoming:
        if f['status'] not in ('added','modified') or f['sha']!=bypath[f['filename']]['sha']:
            raise RuntimeError(f'Changed blob mismatch: {f["filename"]}')
    gate=read_json('INITIAL_LITERAL_STATUS.json')
    queue_artifact=next(a for a in artifacts if a['path']=='unsolved_math_prioritization/QUEUE.md')
    if queue_artifact['sha256']!=gate['QUEUE']['sha256']:
        raise RuntimeError('Initial QUEUE changed')
    source=json.loads((ORIGINAL/(ATTEMPT+'source_record.json')).read_text())
    status=json.loads((ORIGINAL/(ATTEMPT+'status.json')).read_text())
    turns_body=(ORIGINAL/(ATTEMPT+'turns.jsonl')).read_bytes()
    turns=[json.loads(line) for line in turns_body.splitlines() if line.strip()]
    candidate=(ORIGINAL/(ATTEMPT+'CANDIDATE.md')).read_bytes()
    ledger_hashes=[]
    for i,turn in enumerate(turns):
        if 'candidate_sha256' in turn:
            if turn['candidate_sha256']!=sha256(candidate):
                raise RuntimeError('Turn-event candidate digest does not match retained candidate')
            ledger_hashes.append(dict(record_index=i,turn=turn.get('turn'),field='candidate_sha256',
                recorded_sha256=turn['candidate_sha256'],matches_candidate=True))
    if 'candidate_sha256' in status and status['candidate_sha256']!=sha256(candidate):
        raise RuntimeError('Status candidate digest does not match retained candidate')
    state_path=ORIGINAL/'unsolved_math_prioritization/state.json'
    state=json.loads(state_path.read_text()) if state_path.exists() else None
    history_path=ORIGINAL/'unsolved_math_prioritization/history.jsonl'
    history=history_path.read_bytes() if history_path.exists() else None
    source_report_keys=[key for key in source if 'report' in key]
    shapes=dict(UTC=utc(),source_record=type_shape(source),source_report_keys=source_report_keys,
        source_reports={key:field_state(source,key) for key in source_report_keys},
        prior_upstream_report=field_state(source,'prior_upstream_report'),upstream_report=field_state(source,'upstream_report'),
        original_status=type_shape(status),turn_ledger=dict(bytes=len(turns_body),raw_line_count=len(turns_body.splitlines()),
            JSON_record_count=len(turns),records=turns,record_shapes=[type_shape(t) for t in turns],candidate_hash_links=ledger_hashes),
        status_candidate_hash=field_state(status,'candidate_sha256'),
        global_state=dict(presence='present' if state_path.exists() else 'absent',shape=type_shape(state) if state_path.exists() else None,
            target=field_state(state,TARGET) if isinstance(state,dict) else dict(applicability='not an object')),
        global_history=dict(presence='present' if history is not None else 'absent',bytes=len(history) if history is not None else None,
            is_literal_empty=history==b'' if history is not None else None),
        SQLite_cache_presence='present' if 'unsolved_math_prioritization/cache/catalog.sqlite' in bypath else 'absent',
        target_prior_report=dict(native_report_keys=source_report_keys,reports={key:field_state(source,key) for key in source_report_keys},
            attempt_review_paths=sorted(p for p in attempt_paths if '/review/' in p or '/reviews/' in p)))
    write_json(HERE/'TARGET_RECORD_SHAPES.json',shapes)
    write_json(HERE/'ORIGINAL_BLOB_MANIFEST.json',dict(UTC=utc(),head=HEAD,root_tree=tree['sha'],artifact_count=len(artifacts),artifacts=artifacts))
    commands=[json.loads(line) for line in COMMANDS.read_text().splitlines()]
    evidence=dict(UTC=utc(),controller_pid=os.getpid(),PR=PR,problem_id=TARGET,original_head=HEAD,
        original_tree=tree['sha'],original_parent_commits=[p['sha'] for p in commit['parents']],
        initial_source_gate='PASSED_BEFORE_SCIENCE_READ',submitted_QUEUE_literal='claimed_solved',submitted_budget_literal='1/5',
        exact_attempt_blob_count=len(attempt_paths),complete_changed_domain_count=len(paths),QUEUE_plus_complete_attempt_only=True,
        immutable_compare_base=pr['base']['sha'],immutable_compare_merge_base=compare['merge_base_commit']['sha'],
        authenticated_original_body_count=len(artifacts),all_retained_blobs_regular=True,
        all_body_git_SHA1_SHA256_bytes_and_modes_checked=True,tree_serializations=checked['directory_count'],commit_serialization=commit_auth,
        original_status_literal=status.get('status'),original_turn_numbers=[t.get('turn') for t in turns],
        original_turns_used=field_state(status,'turns_used'),original_turn_event_count=len(turns),
        source_report_native_keys=source_report_keys,source_dataset_revision=field_state(source,'dataset_revision'),
        candidate_digest_ledger_links=ledger_hashes,
        source_record_complete=True,candidate_sha256=sha256(candidate),typed_states_preserved=True,
        original_attempt_manifest='ORIGINAL_ATTEMPT_BLOBS.json',blob_manifest='ORIGINAL_BLOB_MANIFEST.json',
        record_shapes='TARGET_RECORD_SHAPES.json',command_ledger='ACTUAL_COMMANDS.jsonl',exact_command_outputs='commands/',
        actual_subprocess_count=len(commands),actual_recorded_failures=[r for r in commands if r['exit_code']!=0],
        bootstrap_observations='BOOTSTRAP_TOOL_OBSERVATIONS.json',
        recovered_gate_controller_failure='RETRIEVAL_FAILURE.json' if (HERE/'RETRIEVAL_FAILURE.json').exists() else None,
        execution_record_limitation='Pre-controller shell-tool inspection exposed no actual child argv/PID or UTC and combined stdout/stderr only. These gaps are stated in BOOTSTRAP_TOOL_OBSERVATIONS.json; no unavailable custody metadata was fabricated.',
        scope='Source custody only',new_mathematical_review=False,new_central_proof_attempts=0,submitted_scientific_code_execution=False,
        source_custody_completion_estimate_percent=100,source_authentication_status='COMPLETE',
        forbidden_mutations=dict(git_fetch=False,git_index=False,git_refs=False,git_branch=False,git_commit=False,git_push=False,
            target_status=False,PR=False,Zenodo=False,Sheets=False,native_editor=False,external_contact=False),
        final_PR_head_recheck=dict(head=pr['head']['sha'],state=pr['state'],draft=pr['draft']),
        scientific_publication_verdict='NOT_ASSIGNED_TO_SOURCE_AGENT')
    write_json(HERE/'ORIGINAL_AUTHENTICATION.json',evidence)
    log(f'Complete source custody: all {len(artifacts)} retained bodies and the {len(paths)}-file incoming domain authenticated; all {checked["directory_count"]} recursive tree serializations match. Original commit serialization recovered: {commit_auth["original_serialization_recovered"]}. Exact original turn/status and typed source states preserved. No scientific code executed or new proof turn.',100)
    report=f'''# PR66 original source authentication\n\nCustody complete at head `{HEAD}` and root tree `{tree['sha']}`. Fresh initial gate authenticated OPEN draft, required branch, literal QUEUE `claimed_solved`, and original budget `1/5` before opening the scientific source.\n\nAll {len(attempt_paths)} original attempt bodies, full QUEUE, and tracked provenance inputs are retained under `original/`. The manifest records each path, regular Git mode, blob SHA1, full byte SHA256, and byte count. The complete incoming domain has {len(paths)} files and is exactly QUEUE plus the target attempt; it matches both paginated PR files and an immutable base/head compare. All {checked['directory_count']} recursive Git tree serializations matched. Exact original commit serialization recovered with matching full Git digest: {commit_auth['original_serialization_recovered']}.\n\nCANDIDATE.md SHA256: `{sha256(candidate)}`. The complete source_record.json includes the original target prior report. TARGET_RECORD_SHAPES.json preserves source, report, status, ledger, absent, null, and empty states without substituting a SQLite cache row or inferring scientific conclusions. Exact original turn numbers: `{[t.get('turn') for t in turns]}`; original status literal: `{status.get('status')}`.\n\nACTUAL_COMMANDS.jsonl records actual argv, PID, cwd, UTC interval, exit status, and exact retained stdout/stderr with byte hashes for every custody-controller child. Bootstrap shell-tool observations precede this controller and have only tool-exposed metadata; their unavailable PID/UTC is explicitly recorded separately rather than invented. Immutable API JSON is original evidence; reconstructed Git bodies are claimed only when the original digest matches. External-document declarations, if present, do not imply external byte authentication.\n\nNo submitted scientific code was executed; no mathematical review or new proof turn was performed. No Git/index/ref/native/PR/Zenodo/Sheets/editor mutation or external human contact occurred. Custody completion estimate: 100%. Mathematical verdict remains ROOT.\n'''
    (HERE/'ORIGINAL_AUTHENTICATION.md').write_text(report)
    seal()

def seal():
    records=[json.loads(line) for line in COMMANDS.read_text().splitlines()]
    for record in records:
        for name in ('stdout','stderr'):
            body=(HERE/record[name+'_path']).read_bytes()
            if sha256(body)!=record[name+'_sha256'] or len(body)!=record[name+'_bytes']:
                raise RuntimeError(f'Output custody recheck failed: {record["label"]}')
    artifacts=read_json('ORIGINAL_BLOB_MANIFEST.json')['artifacts']
    for item in artifacts:
        body=(HERE/item['retained_path']).read_bytes()
        if git_digest('blob',body)!=item['git_blob_SHA1'] or sha256(body)!=item['sha256'] or len(body)!=item['bytes']:
            raise RuntimeError(f'Body custody recheck failed: {item["path"]}')
    write_json(HERE/'FINAL_CUSTODY_RECHECK.json',dict(UTC=utc(),controller_pid=os.getpid(),
        authenticated_body_count=len(artifacts),actual_command_record_count=len(records),all_body_and_output_hashes_match=True,custody_completion_percent=100))
    files=[]
    for path in sorted(p for p in HERE.rglob('*') if p.is_file() and p.name!='SELF_MANIFEST.json'):
        body=path.read_bytes()
        files.append(dict(path=str(path.relative_to(HERE)),bytes=len(body),sha256=sha256(body)))
    write_json(HERE/'SELF_MANIFEST.json',dict(UTC=utc(),exclusions=['SELF_MANIFEST.json'],files=files))
    print(json.dumps({'sealed':True,'head':HEAD,'original_body_count':len(artifacts),
        'candidate_sha256':read_json('ORIGINAL_AUTHENTICATION.json')['candidate_sha256'],
        'report_sha256':sha256((HERE/'ORIGINAL_AUTHENTICATION.json').read_bytes()),
        'self_manifest_sha256':sha256((HERE/'SELF_MANIFEST.json').read_bytes())}),flush=True)

if __name__=='__main__':
    try:
        phases={'intake':intake,'attempt':attempt,'provenance':provenance,'inspect':inspect,'supplement':supplement,'finalize':finalize,'seal':seal}
        if len(sys.argv)!=2 or sys.argv[1] not in phases:
            raise RuntimeError('Use an explicit custody phase')
        phases[sys.argv[1]]()
    except Exception as exc:
        write_json(HERE/'RETRIEVAL_FAILURE.json',dict(UTC=utc(),controller_pid=os.getpid(),type=type(exc).__name__,error=str(exc)))
        raise
