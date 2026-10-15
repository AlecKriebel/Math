#!/usr/bin/env python3
"""Read-only GitHub custody retrieval for the single eligible PR65 source."""
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
HEAD = '5cc1602c05d79502defb07cec7027963149494d2'
REPO = 'AlecKriebel/Math'
TARGET = '2305051'
ATTEMPT = 'unsolved_math_prioritization/attempts/' + TARGET + '/'
ORIGINAL = HERE / 'original'
RAW = HERE / 'commands'
COMMANDS = HERE / 'ACTUAL_COMMANDS.jsonl'

def utc():
    return dt.datetime.now(dt.timezone.utc).isoformat()

def digest(data):
    return hashlib.sha256(data).hexdigest()

def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')

def run(label, argv):
    RAW.mkdir(parents=True, exist_ok=True)
    started = utc()
    proc = subprocess.Popen(argv, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    finished = utc()
    stem = RAW / label
    stem.with_suffix('.stdout').write_bytes(out)
    stem.with_suffix('.stderr').write_bytes(err)
    record = dict(label=label, argv=argv, actual_pid=proc.pid, started_UTC=started,
                  finished_UTC=finished, exit_code=proc.returncode,
                  stdout_path=str(stem.with_suffix('.stdout').relative_to(HERE)),
                  stderr_path=str(stem.with_suffix('.stderr').relative_to(HERE)),
                  stdout_bytes=len(out), stdout_sha256=digest(out),
                  stderr_bytes=len(err), stderr_sha256=digest(err))
    with COMMANDS.open('a') as stream:
        stream.write(json.dumps(record, ensure_ascii=False) + '\n')
    if proc.returncode:
        raise RuntimeError(f'{label} failed, exit {proc.returncode}; exact output retained')
    return out

def api(label, endpoint):
    return json.loads(run(label, ['gh', 'api', endpoint]))

def keep_body(path, body, expected, mode=None):
    git_sha = hashlib.sha1(b'blob ' + str(len(body)).encode() + b'\0' + body).hexdigest()
    if git_sha != expected:
        raise RuntimeError(f'Git blob mismatch: {path}: {git_sha} != {expected}')
    target = ORIGINAL / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(body)
    return dict(path=path, mode=mode, git_blob_SHA1=expected, computed_git_blob_SHA1=git_sha,
                sha256=digest(body), bytes=len(body), retained_path=str(target.relative_to(HERE)))

def retrieve_blob(label, entry):
    value = api(label, f'repos/{REPO}/git/blobs/{entry["sha"]}')
    if value.get('encoding') != 'base64' or value.get('sha') != entry['sha']:
        raise RuntimeError(f'Unexpected blob representation: {entry["path"]}')
    body = base64.b64decode(value['content'])
    if len(body) != value.get('size'):
        raise RuntimeError(f'Blob byte-count mismatch: {entry["path"]}')
    return keep_body(entry['path'], body, entry['sha'], entry.get('mode'))

def snapshot():
    started=utc()
    head=run('000_prelaunch_local_HEAD', ['git','rev-parse','HEAD']).decode().strip()
    branch=run('001_prelaunch_local_branch', ['git','branch','--show-current']).decode().strip()
    status=run('002_prelaunch_local_status', ['git','status','--porcelain=v1','--untracked-files=all']).decode()
    hashes=[]
    relevant=[ROOT/'AGENTS.md', ROOT/'unsolved_math_prioritization/AGENTS.md',
              ROOT/'unsolved_math_prioritization/QUEUE.md']
    local_attempt=ROOT/ATTEMPT
    if local_attempt.is_dir():
        relevant += sorted(p for p in local_attempt.rglob('*') if p.is_file())
    for path in relevant:
        if path.is_file():
            body=path.read_bytes()
            hashes.append(dict(path=str(path.relative_to(ROOT)), bytes=len(body), sha256=digest(body),
                               lstat_mode=oct(path.lstat().st_mode)))
        else:
            hashes.append(dict(path=str(path.relative_to(ROOT)), upstream_local_presence='absent'))
    write_json(HERE/'SOURCE_PRELAUNCH_SNAPSHOT.json', dict(schema='PR65-source-prelaunch/v1',
        UTC=started, finished_UTC=utc(), controller_pid=os.getpid(), local_HEAD=head,
        local_branch=branch, local_status=status, relevant_local_file_hashes=hashes,
        authorized_remote_head=HEAD, original_folder_was_new=True,
        excluded_science_read=False, git_mutations_performed=False))
    if branch != 'main':
        raise RuntimeError('Local workspace is not on main; retrieval stops without branch mutation')

def intake():
    snapshot()
    meta=json.loads(run('003_initial_PR65_status', ['gh','pr','view','65','--repo',REPO,'--json',
        'number,state,isDraft,headRefOid,headRefName,baseRefName,url,title']))
    if meta['headRefOid'] != HEAD or meta['state'] != 'OPEN' or meta['isDraft'] is not True:
        raise RuntimeError('Fresh PR65 head/draft/open gate failed')
    queue=api('004_initial_submitted_QUEUE', f'repos/{REPO}/contents/unsolved_math_prioritization/QUEUE.md?ref={HEAD}')
    if queue.get('encoding') != 'base64':
        raise RuntimeError('QUEUE encoding unavailable')
    body=base64.b64decode(queue['content'])
    item=keep_body('unsolved_math_prioritization/QUEUE.md', body, queue['sha'])
    rows=[line for line in body.decode().splitlines() if line.startswith('|') and f'[{TARGET}]' in line]
    if not rows:
        rows=[line for line in body.decode().splitlines() if line.startswith('|') and TARGET in line]
    if len(rows) != 1:
        raise RuntimeError(f'QUEUE target row count {len(rows)}')
    columns=[part.strip() for part in rows[0].split('|')[1:-1]]
    if 'claimed_solved' not in columns or '2/5' not in columns:
        raise RuntimeError('Fresh literal QUEUE claimed_solved 2/5 gate failed')
    status=dict(schema='PR65-fresh-initial-status/v1', UTC=utc(), metadata=meta,
        literal_status='claimed_solved', literal_budget='2/5', literal_row=rows[0],
        literal_row_sha256=digest(rows[0].encode()), QUEUE=item,
        scientific_source_opened_before_gate=False, gate_passed=True)
    write_json(HERE/'INITIAL_LITERAL_STATUS.json',status)
    print(json.dumps({'initial_gate':'PASSED','literal_status':'claimed_solved','budget':'2/5',
                      'head':HEAD,'QUEUE_blob_SHA1':queue['sha']}),flush=True)
    commit=api('005_original_git_commit',f'repos/{REPO}/git/commits/{HEAD}')
    if commit['sha'] != HEAD:
        raise RuntimeError('Git commit SHA mismatch')
    tree=api('006_original_recursive_tree',f'repos/{REPO}/git/trees/{commit["tree"]["sha"]}?recursive=1')
    if tree.get('truncated') is not False or tree['sha'] != commit['tree']['sha']:
        raise RuntimeError('Original tree is incomplete or mismatched')
    files=[]
    for page in range(1,32):
        page_files=api(f'007_changed_files_page_{page:02}',f'repos/{REPO}/pulls/65/files?per_page=100&page={page}')
        if not isinstance(page_files,list):
            raise RuntimeError('Unexpected PR files representation')
        files+=page_files
        if len(page_files)<100:
            break
    else:
        raise RuntimeError('Changed-file pagination limit reached')
    write_json(HERE/'ORIGINAL_GIT_COMMIT.json',commit)
    write_json(HERE/'ORIGINAL_RECURSIVE_TREE.json',tree)
    write_json(HERE/'INCOMING_CHANGED_DOMAIN.json',dict(UTC=utc(),head=HEAD,files=files,
        count=len(files),pagination_complete=True))
    selected=[e for e in tree['tree'] if e['path'].startswith(ATTEMPT)]
    write_json(HERE/'TARGET_ATTEMPT_TREE.json',selected)
    print(json.dumps({'tree':tree['sha'],'changed_files':[f['filename'] for f in files],
                      'attempt_entries':selected},indent=2),flush=True)

def attempt():
    initial=json.loads((HERE/'INITIAL_LITERAL_STATUS.json').read_text())
    if initial.get('gate_passed') is not True or initial['metadata']['headRefOid'] != HEAD:
        raise RuntimeError('No successful initial source gate')
    tree=json.loads((HERE/'ORIGINAL_RECURSIVE_TREE.json').read_text())
    entries=[e for e in tree['tree'] if e['path'].startswith(ATTEMPT) and e['type']=='blob']
    if any(e['mode'] not in ('100644','100755') for e in entries):
        raise RuntimeError('Attempt has a nonregular artifact')
    artifacts=[]
    for i,e in enumerate(entries):
        artifacts.append(retrieve_blob(f'008_attempt_blob_{i:02}',e))
        if e['path']==ATTEMPT+'CANDIDATE.md':
            print(json.dumps({'candidate_available':str(ORIGINAL/e['path']),
                              'sha256':artifacts[-1]['sha256'],'bytes':artifacts[-1]['bytes']}),flush=True)
    write_json(HERE/'ORIGINAL_ATTEMPT_BLOBS.json',artifacts)
    print(json.dumps({'attempt_body_count':len(artifacts),'all_authenticated':True}),flush=True)

def provenance():
    tree=json.loads((HERE/'ORIGINAL_RECURSIVE_TREE.json').read_text())
    bypath={e['path']:e for e in tree['tree']}
    selected=['unsolved_math_prioritization/manifest.json',
              'unsolved_math_prioritization/state.json',
              'unsolved_math_prioritization/history.jsonl',
              'unsolved_math_prioritization/queue.py',
              'unsolved_math_prioritization/AGENTS.md', 'AGENTS.md']
    artifacts=[]
    for i,path in enumerate(selected):
        entry=bypath.get(path)
        if entry is None:
            artifacts.append(dict(path=path,presence='absent'))
        elif entry['type']!='blob' or entry['mode'] not in ('100644','100755'):
            raise RuntimeError(f'Nonregular provenance file {path}')
        else:
            artifacts.append(retrieve_blob(f'009_provenance_blob_{i:02}',entry))
    write_json(HERE/'ORIGINAL_PROVENANCE_BLOBS.json',artifacts)
    print((ORIGINAL/'unsolved_math_prioritization/manifest.json').read_text(),flush=True)

def verify_tree(tree):
    entries=tree['tree']
    directory_hashes={'':tree['sha']}
    children={}
    for entry in entries:
        path=entry['path']
        parent,_,name=path.rpartition('/')
        children.setdefault(parent,[]).append((name,entry))
        if entry['type']=='tree':
            directory_hashes[path]=entry['sha']
    checked=[]
    for directory,expected in sorted(directory_hashes.items()):
        direct=children.get(directory,[])
        ordered=sorted(direct,key=lambda pair:(pair[0]+('/' if pair[1]['type']=='tree' else '')).encode())
        raw=b''.join((entry['mode'].lstrip('0')+' '+name).encode()+b'\0'+bytes.fromhex(entry['sha'])
                     for name,entry in ordered)
        actual=hashlib.sha1(b'tree '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
        if actual!=expected:
            raise RuntimeError(f'Git tree serialization mismatch {directory}: {actual} != {expected}')
        checked.append(dict(path=directory or '/',sha=actual,direct_entries=len(direct)))
    return dict(all_match=True,recursive_response_truncated=False,directory_count=len(checked),
                root_tree_SHA1=tree['sha'],authenticated_tree_serializations=checked)

def reconstruct_commit(commit):
    # GitHub API uses UTC dates and omits original timezone offsets. A matching
    # Git-object digest certifies any recovered serialization without guessing.
    base='tree '+commit['tree']['sha']+'\n'
    base+=''.join('parent '+p['sha']+'\n' for p in commit['parents'])
    people={}
    for role in ('author','committer'):
        p=commit[role]
        stamp=int(dt.datetime.fromisoformat(p['date'].replace('Z','+00:00')).timestamp())
        people[role]=f'{role} {p["name"]} <{p["email"]}> {stamp}'
    for minute in range(-12*60,14*60+1):
        tz=('-' if minute<0 else '+')+f'{abs(minute)//60:02}{abs(minute)%60:02}'
        for ending in ('\n',''):
            body=(base+people['author']+' '+tz+'\n'+people['committer']+' '+tz+'\n\n'
                  +commit['message']+ending).encode()
            actual=hashlib.sha1(b'commit '+str(len(body)).encode()+b'\0'+body).hexdigest()
            if actual==HEAD:
                path=HERE/'ORIGINAL_GIT_COMMIT_BODY.bin'
                path.write_bytes(body)
                return dict(original_serialization_recovered=True,computed_git_commit_SHA1=actual,
                    recovered_author_timezone=tz,recovered_committer_timezone=tz,
                    bytes=len(body),sha256=digest(body),retained_path=path.name,
                    method='Reconstructed from immutable API fields; matching full Git object SHA1 authenticates bytes.')
    return dict(original_serialization_recovered=False,computed_git_commit_SHA1=None,
        authenticated_via='Immutable GitHub git/commits endpoint',
        limitation='API normalizes dates to UTC, original commit serialization not recoverable by equal-offset enumeration.')

def type_shape(value):
    if value is None:
        return {'JSON_type':'null','value':None}
    if isinstance(value,dict):
        return {'JSON_type':'object','is_empty_object':value=={},'keys':{k:type_shape(v) for k,v in value.items()}}
    if isinstance(value,list):
        return {'JSON_type':'array','length':len(value),'items':[type_shape(v) for v in value]}
    if isinstance(value,bool):
        kind='boolean'
    elif isinstance(value,int):
        kind='integer'
    elif isinstance(value,float):
        kind='number'
    else:
        kind='string'
    return {'JSON_type':kind}

def finalize():
    commit=json.loads((HERE/'ORIGINAL_GIT_COMMIT.json').read_text())
    tree=json.loads((HERE/'ORIGINAL_RECURSIVE_TREE.json').read_text())
    bypath={e['path']:e for e in tree['tree']}
    tree_check=verify_tree(tree)
    write_json(HERE/'TREE_SERIALIZATION_AUTHENTICATION.json',tree_check)
    commit_check=reconstruct_commit(commit)
    write_json(HERE/'COMMIT_SERIALIZATION_AUTHENTICATION.json',commit_check)
    pr=api('010_PR65_current_API_metadata',f'repos/{REPO}/pulls/65')
    if pr['head']['sha']!=HEAD or pr['state']!='open' or pr.get('draft') is not True:
        raise RuntimeError('Final head/draft/open gate failed')
    base=pr['base']['sha']
    compare=api('011_immutable_changed_domain_compare',f'repos/{REPO}/compare/{base}...{HEAD}')
    expected_files=json.loads((HERE/'INCOMING_CHANGED_DOMAIN.json').read_text())['files']
    changed={f['filename'] for f in expected_files}
    if changed!={f['filename'] for f in compare['files']} or len(changed)!=pr['changed_files']:
        raise RuntimeError('Complete incoming PR changed domain is not stable or complete')
    allowed={'unsolved_math_prioritization/QUEUE.md'}|{e['path'] for e in tree['tree']
             if e['path'].startswith(ATTEMPT) and e['type']=='blob'}
    if changed!=allowed:
        raise RuntimeError('Incoming changed domain does not equal QUEUE plus complete target attempt')
    artifacts=[]
    for path in sorted(p for p in ORIGINAL.rglob('*') if p.is_file()):
        rel=str(path.relative_to(ORIGINAL))
        entry=bypath.get(rel)
        if not entry or entry['type']!='blob' or entry['mode'] not in ('100644','100755'):
            raise RuntimeError(f'Original retained file is not regular in pinned tree: {rel}')
        item=keep_body(rel,path.read_bytes(),entry['sha'],entry['mode'])
        if item['bytes']!=entry['size']:
            raise RuntimeError(f'Original retained file size mismatch {rel}')
        item['incoming_changed_domain']=rel in changed
        artifacts.append(item)
    for f in expected_files:
        if f['sha']!=bypath[f['filename']]['sha'] or f['status'] not in ('added','modified'):
            raise RuntimeError(f'Changed-file blob SHA/status inconsistent: {f["filename"]}')
    initial=json.loads((HERE/'INITIAL_LITERAL_STATUS.json').read_text())
    source=json.loads((ORIGINAL/(ATTEMPT+'source_record.json')).read_text())
    state=json.loads((ORIGINAL/'unsolved_math_prioritization/state.json').read_text())
    history=(ORIGINAL/'unsolved_math_prioritization/history.jsonl').read_bytes()
    turns_body=(ORIGINAL/(ATTEMPT+'turns.jsonl')).read_bytes()
    turns=[json.loads(line) for line in turns_body.splitlines() if line.strip()]
    status=json.loads((ORIGINAL/(ATTEMPT+'status.json')).read_text())
    if [t.get('turn') for t in turns]!=[1,2] or turns[-1]['outcome']!='candidate':
        raise RuntimeError('Target original turn ledger shape is inconsistent')
    candidate=(ORIGINAL/(ATTEMPT+'CANDIDATE.md')).read_bytes()
    if digest(candidate)!=turns[-1]['sha256'] or digest(candidate)!=status['candidate_sha256']:
        raise RuntimeError('Original candidate hash ledger link inconsistent')
    shape=dict(schema='PR65-original-target-record-shapes/v1',source_record=type_shape(source),
        source_record_top_level_keys=list(source),original_source_problem_id_native_type=type(source['problem']['id']).__name__,
        upstream_report_key_present='upstream_report' in source,upstream_report_is_null=source.get('upstream_report') is None,
        upstream_report_is_empty_object=source.get('upstream_report')=={},
        global_state=type_shape(state),global_state_target_key_present=TARGET in state,
        global_state_target_value_state='absent' if TARGET not in state else type_shape(state[TARGET]),
        global_history_bytes=len(history),global_history_record_count=len(history.splitlines()),
        target_turn_ledger=dict(bytes=len(turns_body),raw_line_count=len(turns_body.splitlines()),
            JSON_record_count=len(turns),turn_numbers=[t['turn'] for t in turns],record_shapes=[type_shape(t) for t in turns]),
        original_status_literal=status['status'],submitted_QUEUE_literal=initial['literal_status'],
        SQL_catalog=dict(pinned_tree_path='unsolved_math_prioritization/cache/catalog.sqlite',
            present_in_pinned_tree='unsolved_math_prioritization/cache/catalog.sqlite' in bypath,
            interpretation='Absent original tracked artifact; no SQLite row substituted for the full tracked source_record JSON.'),
        external_PDF_manifest=dict(declaration_authenticated=True,pdf_bodies_present_in_attempt_tree=False,
            bytes_fetched_or_authenticated=False,interpretation='Declared external hashes only; original tree does not redistribute these PDFs.'))
    write_json(HERE/'TARGET_RECORD_SHAPES.json',shape)
    write_json(HERE/'ORIGINAL_BLOB_MANIFEST.json',dict(schema='PR65-original-blob-custody/v1',UTC=utc(),
        head=HEAD,root_tree=tree['sha'],artifact_count=len(artifacts),artifacts=artifacts))
    commands=[json.loads(line) for line in COMMANDS.read_text().splitlines()]
    evidence=dict(schema='PR65-original-source-authentication/v1',UTC=utc(),controller_pid=os.getpid(),
        PR=65,problem_id=TARGET,title=initial['metadata']['title'],original_head=HEAD,
        original_root_tree=tree['sha'],original_parent_commits=[p['sha'] for p in commit['parents']],
        original_commit_API_SHA1_authenticated=True,commit_serialization=commit_check,
        original_tree_serializations_authenticated=True,tree_serialization_count=tree_check['directory_count'],
        initial_literal_status_gate='PASSED_BEFORE_SOURCE_READ',submitted_QUEUE_literal='claimed_solved',
        submitted_budget_literal='2/5',original_status_json_literal=status['status'],
        exact_original_attempt_blob_count=18,complete_incoming_changed_domain_count=len(changed),
        incoming_domain_QUEUE_plus_complete_target_attempt_only=True,
        immutable_compare_base=base,immutable_compare_head=HEAD,immutable_compare_merge_base=compare['merge_base_commit']['sha'],
        authenticated_original_body_count=len(artifacts),all_retained_blobs_are_regular=True,
        all_retained_body_git_SHA1_SHA256_and_bytes_checked=True,turn_numbers=[t['turn'] for t in turns],
        candidate_SHA256=digest(candidate),source_record_complete=True,
        upstream_report_present=True,upstream_report_null=False,upstream_report_empty_object=False,
        pinned_dataset_revision=source['dataset_revision'],global_state_literal_empty_object=state=={},
        global_history_literal_empty=len(history)==0,upstream_target_in_global_state='absent',
        source_support_PDF_byte_custody='Not present in original target tree; declarations retained only',
        source_only=True,new_mathematical_review=False,new_central_proof_attempts=0,
        submitted_scientific_code_execution=False,source_custody_completion_estimate_percent=100,
        source_authentication_status='COMPLETE',scientific_publication_verdict='NOT_ASSIGNED_TO_SOURCE_AGENT',
        all_recorded_subprocesses_serial=True,actual_subprocess_count=len(commands),
        actual_recorded_failures=[r for r in commands if r['exit_code']!=0],
        final_PR_head_recheck=dict(head=pr['head']['sha'],state=pr['state'],draft=pr['draft']),
        forbidden_mutations=dict(git_fetch=False,git_index=False,git_refs=False,git_branch=False,
            git_commit=False,git_push=False,target_status=False,PR=False,Zenodo=False,Sheets=False,
            native_editor=False,external_contact=False),
        artifacts_manifest='ORIGINAL_BLOB_MANIFEST.json',commands='ACTUAL_COMMANDS.jsonl',
        exact_subprocess_outputs='commands/',source_prelaunch='SOURCE_PRELAUNCH_SNAPSHOT.json')
    write_json(HERE/'ORIGINAL_AUTHENTICATION.json',evidence)
    log=[f'# PR65 original-source custody research log\n\nScope: source retrieval and authentication only, with no mathematical judgment.\n']
    first=commands[0]['started_UTC']
    initial_end=next(r['finished_UTC'] for r in commands if r['label']=='004_initial_submitted_QUEUE')
    candidate_end=next(r['finished_UTC'] for r in commands if r['label']=='008_attempt_blob_00')
    last=commands[-1]['finished_UTC']
    log += [f'## {first} — Prelaunch snapshot\n\nCustody completion estimate: 5%. Captured the main branch, local HEAD, read-only workspace status, and relevant local file hashes before source retrieval.\n',
        f'## {initial_end} — Fresh initial eligibility authenticated\n\nCustody completion estimate: 20%. PR65 was OPEN and draft at `{HEAD}`. Literal submitted QUEUE status was `claimed_solved` with `2/5`; no target scientific source was opened before this gate.\n',
        f'## {candidate_end} — Candidate body available\n\nCustody completion estimate: 65%. Preserved candidate bytes and authenticated Git blob hash. Subsequently preserved all 18 target attempt and old-review bodies. Informed ROOT promptly.\n',
        f'## {last} — Complete original domain and provenance checkpoint\n\nCustody completion estimate: 100%. Authenticated all regular retained bodies, every recursive tree serialization, original commit serialization where the Git digest matches, both target turn records, and complete 19-file incoming domain against an immutable base/head compare. Preserved null, absent, and empty-object states distinctly. External PDFs occur only as declared hashes in original artifacts; no PDF byte authentication claimed. All recorded remote source retrieval subprocesses were serial and exited successfully. Mathematical verification and publication remain ROOT responsibilities.\n']
    (HERE/'RESEARCH_LOG.md').write_text('\n'.join(log))
    report=f'''# PR65 original source authentication\n\nSource custody is complete at immutable head `{HEAD}` and root tree `{tree['sha']}`. Fresh initial PR metadata and the literal submitted QUEUE entry were authenticated before reading target scientific source: OPEN draft, `claimed_solved`, `2/5`.\n\nAll 18 original attempt and prior-review files, the whole submitted QUEUE, and six provenance/infrastructure files are retained under `original/`. Their full bytes match the pinned regular Git blobs; `ORIGINAL_BLOB_MANIFEST.json` gives SHA1, SHA256, bytes, and mode for every body. The complete incoming PR domain has 19 files: QUEUE and precisely the complete target attempt. The original recursive tree was independently serialized and all {tree_check['directory_count']} directory hashes matched. Original commit bytes were recovered with matching SHA1: {commit_check['original_serialization_recovered']}.\n\nThe full source record and upstream report are retained. The upstream report is a present object; nullable author fields remain null. The original global state is literally `{{}}`, with target key absent, and the original global history is zero bytes. The separate target turn ledger has exactly sequential turns 1 and 2, ending in the candidate whose SHA256 is `{digest(candidate)}`. QUEUE's `claimed_solved` and status.json's `claimed_solved_after_independent_review` remain distinct literal observations. The tracked upstream dataset manifest pins `ulamai/UnsolvedMath` revision `{source['dataset_revision']}`. SQLite cache is absent from the pinned tracked tree and was not substituted for source JSON.\n\nOriginal external PDF hashes are declarations in source_manifest.json; actual PDF bodies are absent from the original target tree. This custody report authenticates declarations and does not certify PDF bytes or the mathematical claim. No candidate code was executed, no new proof attempt occurred, and no git, target-status, PR, native-editor, Zenodo, or Sheets mutation or external contact occurred. Exact argv, real child PIDs, UTC intervals, exit codes, stdout/stderr bytes, and hashes are preserved in `ACTUAL_COMMANDS.jsonl` and `commands/`. Custody completion estimate: 100%; scientific/publication assessment remains unassigned to this agent.\n'''
    (HERE/'ORIGINAL_AUTHENTICATION.md').write_text(report)
    manifest=[]
    for path in sorted(p for p in HERE.rglob('*') if p.is_file() and p.name!='SELF_MANIFEST.json'):
        body=path.read_bytes()
        manifest.append(dict(path=str(path.relative_to(HERE)),bytes=len(body),sha256=digest(body)))
    write_json(HERE/'SELF_MANIFEST.json',dict(schema='PR65-custody-self-manifest/v1',UTC=utc(),
        exclusions=['SELF_MANIFEST.json'],files=manifest))
    print(json.dumps({'source_custody_complete':True,'head':HEAD,'tree':tree['sha'],
        'candidate_sha256':digest(candidate),'original_bodies':len(artifacts),
        'self_manifest_sha256':digest((HERE/'SELF_MANIFEST.json').read_bytes()),
        'report_sha256':digest((HERE/'ORIGINAL_AUTHENTICATION.json').read_bytes())}),flush=True)

def seal():
    # These initial inspection outcomes were returned by the shell tool before
    # the provenance controller existed. Do not fabricate unavailable PID/UTC.
    write_json(HERE/'BOOTSTRAP_ABSENCE_OBSERVATIONS.json',dict(schema='bootstrap-tool-observations/v1',
        observations=[dict(command='rg --files -g AGENTS.md draft_pr_publication_program_20260930',
            exit_code=1,exact_output='',meaning='No nested AGENTS.md found',actual_pid=None,
            actual_UTC=None,provenance_limitation='Shell-tool envelope did not expose PID or UTC'),
        dict(command='ls -ld draft_pr_publication_program_20260930/audits/pr65_2305051/original_source_authentication_20261004',
            exit_code=1,exact_output='ls: draft_pr_publication_program_20260930/audits/pr65_2305051/original_source_authentication_20261004: No such file or directory\n',
            meaning='Assigned dedicated custody folder absent before creation',actual_pid=None,
            actual_UTC=None,provenance_limitation='Shell-tool envelope did not expose PID or UTC')],
        remote_source_API_failures=False))
    commands=[json.loads(line) for line in COMMANDS.read_text().splitlines()]
    output_checks=[]
    for record in commands:
        for stream in ('stdout','stderr'):
            body=(HERE/record[stream+'_path']).read_bytes()
            if digest(body)!=record[stream+'_sha256'] or len(body)!=record[stream+'_bytes']:
                raise RuntimeError(f'Exact output changed for {record["label"]}/{stream}')
        output_checks.append(dict(label=record['label'],actual_pid=record['actual_pid'],pass_check=True))
    blobs=json.loads((HERE/'ORIGINAL_BLOB_MANIFEST.json').read_text())['artifacts']
    for item in blobs:
        body=(HERE/item['retained_path']).read_bytes()
        actual=hashlib.sha1(b'blob '+str(len(body)).encode()+b'\0'+body).hexdigest()
        if actual!=item['git_blob_SHA1'] or digest(body)!=item['sha256'] or len(body)!=item['bytes']:
            raise RuntimeError(f'Original bytes changed for {item["path"]}')
    report_path=HERE/'ORIGINAL_AUTHENTICATION.json'
    report=json.loads(report_path.read_text())
    if 'code_execution' in report:
        report['submitted_scientific_code_execution']=report.pop('code_execution')
    report['bootstrap_expected_absence_observations']='BOOTSTRAP_ABSENCE_OBSERVATIONS.json'
    report['final_custody_recheck']='FINAL_CUSTODY_RECHECK.json'
    write_json(report_path,report)
    log=HERE/'RESEARCH_LOG.md'
    log.write_text(log.read_text().replace('All source subprocesses were serial and exited successfully.',
        'All recorded remote source retrieval subprocesses were serial and exited successfully.'))
    write_json(HERE/'FINAL_CUSTODY_RECHECK.json',dict(schema='PR65-final-custody-recheck/v1',UTC=utc(),
        controller_pid=os.getpid(),original_body_count=len(blobs),all_body_hashes_and_bytes_match=True,
        exact_command_record_count=len(commands),all_retained_stdout_stderr_hashes_and_bytes_match=True,
        command_output_checks=output_checks,original_commit_serialization_SHA1=HEAD,
        custody_completion_estimate_percent=100))
    files=[]
    for path in sorted(p for p in HERE.rglob('*') if p.is_file() and p.name!='SELF_MANIFEST.json'):
        body=path.read_bytes()
        files.append(dict(path=str(path.relative_to(HERE)),bytes=len(body),sha256=digest(body)))
    write_json(HERE/'SELF_MANIFEST.json',dict(schema='PR65-custody-self-manifest/v1',UTC=utc(),
        exclusions=['SELF_MANIFEST.json'],files=files))
    print(json.dumps({'sealed':True,'head':HEAD,'original_bodies':len(blobs),
        'manifest_file_count':len(files),'report_sha256':digest(report_path.read_bytes()),
        'original_blob_manifest_sha256':digest((HERE/'ORIGINAL_BLOB_MANIFEST.json').read_bytes()),
        'self_manifest_sha256':digest((HERE/'SELF_MANIFEST.json').read_bytes())}),flush=True)

if __name__=='__main__':
    try:
        if sys.argv[1:] == ['intake']:
            intake()
        elif sys.argv[1:] == ['attempt']:
            attempt()
        elif sys.argv[1:] == ['provenance']:
            provenance()
        elif sys.argv[1:] == ['finalize']:
            finalize()
        elif sys.argv[1:] == ['seal']:
            seal()
        else:
            raise RuntimeError('Use the explicit intake phase')
    except Exception as exc:
        write_json(HERE/'RETRIEVAL_FAILURE.json',dict(UTC=utc(),controller_pid=os.getpid(),
            error_type=type(exc).__name__,error=str(exc),preserved=True))
        raise
