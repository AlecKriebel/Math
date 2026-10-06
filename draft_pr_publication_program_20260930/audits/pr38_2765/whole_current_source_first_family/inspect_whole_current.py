#!/usr/bin/env python3
"""Independent read-only exact closure and complete receipt audit.

Writes only this audit family. Finite byte/provenance checks are not mathematics.
No imports of candidate helpers, execution of candidate tools, or shared writes.
"""
import ast
from collections import Counter
import datetime
import hashlib
import json
from pathlib import Path, PurePosixPath
import sqlite3
import subprocess

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
REPO = AUDIT.parents[2]
CANDIDATE = AUDIT / 'reviewed_candidate'
SUPPORT = AUDIT / 'root_closed_families_actual_reproduction_support'
EXPECTED_MANIFEST = '054b156eb6d44903eadeffeda2012a23c68db530b514294830cc0f45c7b93912'
sha = lambda b: hashlib.sha256(b).hexdigest()
load = lambda p: json.loads(p.read_bytes())
errors, reads = [], []
def require(condition, message):
    if not condition: errors.append(message)
def read(p, role):
    b = p.read_bytes()
    reads.append({'path': str(p.relative_to(REPO)) if p.is_relative_to(REPO) else str(p),
                  'bytes': len(b), 'sha256': sha(b), 'role': role})
    return b
def safe(name):
    p = PurePosixPath(name)
    return not p.is_absolute() and '..' not in p.parts and name == p.as_posix() and bool(p.parts)
def exact_members(root, entries, excluded, role):
    names = [x['path'] for x in entries]
    require(len(set(names)) == len(names), role + ': duplicate paths')
    require(all(safe(x) for x in names), role + ': unsafe path')
    found = []
    for p in sorted(root.rglob('*')):
        rel = p.relative_to(root).as_posix()
        if any(rel == e or (e.endswith('/') and rel.startswith(e)) for e in excluded): continue
        require(not p.is_symlink(), role + ': symlink ' + rel)
        if p.is_file(): found.append(rel)
    require(set(found) == set(names), role + ': exact closure missing=' + str(sorted(set(names)-set(found))) + ' extra=' + str(sorted(set(found)-set(names))))
    for row in entries:
        p = root/row['path']
        if not p.is_file(): continue
        b = read(p, role)
        require(len(b) == row.get('bytes', row.get('size')) and sha(b) == row['sha256'], role + ': byte mismatch ' + row['path'])
    return len(names)

manifest_bytes = read(CANDIDATE/'MANIFEST.json', 'current_self_manifest')
manifest = json.loads(manifest_bytes)
require(sha(manifest_bytes) == EXPECTED_MANIFEST, 'candidate manifest unexpected')
require(manifest['self_excluded'] == ['MANIFEST.json'], 'candidate nonexact self exclusion')
candidate_count = exact_members(CANDIDATE, manifest['files'], ['MANIFEST.json'], 'whole_current_member')
require(candidate_count == manifest['files_count'] == 1499, 'candidate member count')

dependency = load(CANDIDATE/'CURRENT_PROOF_DEPENDENCIES.json')
require(dependency['dependency_anchor_repository_relative'] == str(AUDIT.relative_to(REPO)), 'dependency anchor')
dep_names = [x['path'] for x in dependency['files']]
require(len(dep_names) == len(set(dep_names)) == 1472, 'dependency exact names/count')
for row in dependency['files']:
    name = row['path']
    require(safe(name), 'unsafe dependency '+name)
    # Retained actual control inputs are first-party evidence, even where their
    # historical relative names contain ignoredtmp. No basename exclusion.
    require(not name.startswith(('tmp/','ignoredtmp/')), 'live scratch/cache dependency '+name)
    require(Path(name).suffix not in ['.pdf','.sqlite'], 'foreign primary dependency '+name)
    p = AUDIT/name
    require(p.is_file() and not p.is_symlink(), 'missing/nonregular dependency '+name)
    if p.is_file():
        b = read(p, 'qualified_current_dependency')
        require(len(b) == row['bytes'] and sha(b) == row['sha256'], 'dependency byte mismatch '+name)

support_manifest = load(SUPPORT/'ROOT_SUPPORT_MANIFEST.json')
support_count = exact_members(SUPPORT, support_manifest['files'], ['ROOT_SUPPORT_MANIFEST.json'], 'retained_actual_root_support')
require(support_count == 1269, 'support count')
pins = load(AUDIT/'root_replay_execution_revision/INPUT_PINS.json')
families = []
for name, info in pins['families'].items():
    count = exact_members(AUDIT/name, info['members'], [info['manifest_name'], info['cache_prefix']+'/'], 'closed_family:'+name)
    b = read(AUDIT/name/info['manifest_name'], 'closed_self_manifest')
    require(sha(b) == info['manifest']['sha256'] and len(b) == info['manifest']['size'], 'closed manifest mismatch '+name)
    families.append({'name':name,'count':count,'manifest_sha256':sha(b)})
require(sum(x['count'] for x in families) == 169, 'closed authored member count')

inspection = load(AUDIT/'ROOT_ACTUAL_REPLAY_INSPECTION.json')
bad_map = {x['path']: x for x in inspection['exact_malformed_negative_inputs']}
require(len(bad_map) == 12, 'exact malformed qualification count')
valid, malformed, python_asts = {}, [], 0
for root, label in [(CANDIDATE,'candidate'),(SUPPORT,'support')]:
    n = 0
    for p in sorted(root.rglob('*.json')):
        b = p.read_bytes()
        try:
            json.loads(b); n += 1
        except (ValueError, UnicodeError) as exc:
            if root == SUPPORT: rel = p.relative_to(SUPPORT).as_posix()
            else:
                prefix = 'root_verification/evidence/root_closed_families_actual_reproduction_support/'
                cp = p.relative_to(CANDIDATE).as_posix()
                require(cp.startswith(prefix), 'unexpected candidate malformed JSON '+cp)
                rel = cp[len(prefix):]
            row = bad_map.get(rel)
            require(row is not None and len(b) == row['size'] and sha(b) == row['sha256'], 'unqualified malformed JSON '+rel)
            if row:
                if '/nested_manifest_extra/' in rel:
                    expected = b'Actual nested same-basename extra-file control.\n'
                    provenance = 'literal reconstructed_controls.py nested_manifest_extra definition'
                else:
                    base = (AUDIT/'current_measure_family/bonahon_access_followup.json').read_bytes()
                    expected = bytes([base[0]^1])+base[1:]
                    provenance = 'exact one-byte XOR of closed bonahon_access_followup.json'
                require(b == expected, 'malformed control provenance mismatch '+rel)
                malformed.append({'root':label,'path':rel,'bytes':len(b),'sha256':sha(b),'parse_error':str(exc),'provenance':provenance})
    valid[label] = n
    for p in sorted(root.rglob('*.py')):
        try: ast.parse(p.read_bytes()); python_asts += 1
        except (SyntaxError, ValueError) as exc: errors.append('invalid python AST '+str(p)+' '+str(exc))
require(len(malformed) == 24, 'candidate/support malformed sets not each12')
dependency_valid,dependency_malformed=0,[]
for row in dependency['files']:
    p=AUDIT/row['path']
    if p.suffix!='.json':continue
    try:json.loads(p.read_bytes());dependency_valid+=1
    except (ValueError,UnicodeError) as exc:
        require(p.is_relative_to(SUPPORT),'unexpected malformed dependency JSON '+row['path'])
        rel=p.relative_to(SUPPORT).as_posix()
        require(rel in bad_map and sha(p.read_bytes())==bad_map[rel]['sha256'],'unqualified dependency malformed JSON '+row['path'])
        dependency_malformed.append(rel)
require(set(dependency_malformed)==set(bad_map),'dependency malformed exact set')
valid['dependency_members']=dependency_valid
for p in CANDIDATE.rglob('*.jsonl'):
    for i,line in enumerate(p.read_bytes().splitlines()):
        if line:json.loads(line)

receipt = load(AUDIT/'ROOT_CLOSED_FAMILIES_ACTUAL_REPRODUCTION.json')
def resolve(ref):
    p = Path(ref)
    return p if p.is_absolute() else AUDIT/p
stream_checks, source_checks, stdin_checks = [], [], []
for label, rows in [('outer',receipt['actual_outer_program_runs']),('nested',receipt['actual_nested_program_runs']),('administrative',receipt['actual_administrative_command_runs'])]:
    for i,row in enumerate(rows):
        for channel in ['stdout','stderr']:
            ref = row[channel]
            p = resolve(ref['path']); b = read(p, 'actual_'+label+'_'+channel)
            require(len(b) == ref['size'] and sha(b) == ref['sha256'], 'actual stream mismatch '+label+str(i)+channel)
            stream_checks.append({'kind':label,'index':i,'channel':channel,'path':str(p.relative_to(AUDIT)),'bytes':len(b),'sha256':sha(b),'exit_code':row['exit_code']})
        require(row['launch_attempted'] and row['actual_execution'] and row['completed'], 'unexecuted/incomplete actual row '+label+str(i))
        require(row['stdio_capture']['kind'] == 'complete_child_streams', 'actual incomplete streams '+label+str(i))
        script = row.get('script') or row.get('prelaunch_source')
        if script:
            p = resolve(script.get('retained_full_source') or script['path']); b = read(p, 'actual_'+label+'_source')
            require(len(b) == script['size'] and sha(b) == script['sha256'], 'actual script mismatch '+label+str(i))
            source_checks.append({'kind':label,'index':i,'sha256':sha(b),'bytes':len(b)})
        if 'stdin' in row:
            ref = row['stdin']; b = read(resolve(ref['path']), 'actual_'+label+'_stdin')
            require(len(b) == ref['size'] and sha(b) == ref['sha256'], 'actual stdin mismatch '+str(i))
            git_blob = hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
            require(resolve(row['stdout']['path']).read_bytes() == (git_blob+'\n').encode(), 'complete stdin git-blob output mismatch '+str(i))
            stdin_checks.append({'index':i,'sha256':sha(b),'git_blob':git_blob,'bytes':len(b)})
require([len(receipt[k]) for k in ['actual_outer_program_runs','actual_nested_program_runs','actual_administrative_command_runs']] == [12,108,2], 'actual run counts')
require(len(stdin_checks) == 16, 'original stdin count')
originals = []
for record in receipt['original_replays']:
    original = AUDIT/'source_snapshot'/('verification.json' if record['assertions'] == 30 else 'review/independent_results.json')
    a = resolve(record['actual_stdout']['path']).read_bytes()
    b = resolve(record['generated_receipt']['path']).read_bytes()
    old = original.read_bytes()
    require(a == b == old and json.loads(a) == json.loads(b) == json.loads(old), 'whole original replay byte/full JSON mismatch')
    originals.append({'assertions':record['assertions'],'whole_byte_equal':a==b==old,'whole_json_equal':json.loads(a)==json.loads(b)==json.loads(old),'sha256':sha(a)})

policy = receipt['comparison_exclusion_policy']
clock_keys = set(policy['clock_keys'])
actual_prefix = policy['single_private_path_prefix']['actual']
saved_prefix = policy['single_private_path_prefix']['saved']
def normalized(x):
    if isinstance(x,dict): return {k:normalized(v) for k,v in x.items() if k not in clock_keys}
    if isinstance(x,list): return [normalized(v) for v in x]
    if isinstance(x,str): return x.replace(actual_prefix,saved_prefix)
    return x
def differences(a,b,path='$'):
    if type(a) is not type(b): return [{'path':path,'actual':a,'saved':b}]
    if isinstance(a,dict):
        out=[]
        for key in sorted(set(a)|set(b)):
            if key not in a or key not in b:out.append({'path':path+'/'+key,'actual':a.get(key),'saved':b.get(key)})
            else:out.extend(differences(a[key],b[key],path+'/'+key))
        return out
    if isinstance(a,list):
        if len(a)!=len(b):return [{'path':path,'actual':a,'saved':b}]
        return sum((differences(aa,bb,path+'/'+str(i)) for i,(aa,bb) in enumerate(zip(a,b))),[])
    return [] if a==b else [{'path':path,'actual':a,'saved':b}]
qualified=[]
for row in receipt['full_structured_receipt_comparisons']:
    ab=read(resolve(row['actual']['path']),'whole_compared_actual_JSON')
    sb=read(resolve(row['saved']['path']),'whole_compared_saved_JSON')
    for b,ref in [(ab,row['actual']),(sb,row['saved'])]:
        require(sha(b)==ref['sha256'] and len(b)==ref['size'],'structured receipt ref '+row['label'])
    actual,saved=json.loads(ab),json.loads(sb)
    ds=differences(normalized(actual),normalized(saved))
    require({x['path']:x for x in ds}=={x['path']:x for x in row['full_JSON_differences']},'complete structured differences '+row['label'])
    require(row['complete_JSON_BYTE_equal']==(ab==sb),'whole receipt byte flag '+row['label'])
    require(row['equal_after_explicit_clock_and_private_path_exclusions']==(not ds),'whole receipt normalized flag '+row['label'])
    require(set(row['precise_qualifications'])=={x['path'] for x in ds},'exact qualified residual paths '+row['label'])
    for path,q in row['precise_qualifications'].items():
        require(q['difference']==next(x for x in ds if x['path']==path),'qualified residual values '+path)
        if 'actual_complete_stream' in q:
            refs=[q['actual_complete_stream'],q['saved_complete_stream']]
            bodies=[]
            for ref in refs:
                b=read(resolve(ref['path']),'whole_qualified_residual_stream')
                require(len(b)==ref['size'] and sha(b)==ref['sha256'],'qualified stream pin '+path)
                bodies.append(b)
            require(bodies[0].replace(actual_prefix.encode(),saved_prefix.encode())==bodies[1],'qualified full-stream path transport '+path)
        else:
            require(row['label']=='primary_full_dated_current_metadata' and path in ['$/state.json/bytes','$/state.json/sha256','$/history_target/sha256'],'unrecognized native qualification '+path)
            p=resolve(q['current_input_manifest']['path'])
            require(sha(p.read_bytes())==q['current_input_manifest']['sha256'],'native qualification current preimage pin '+path)
    qualified.append({'label':row['label'],'whole_BYTE_equal':ab==sb,'complete_JSON_equal_after_clock_and_path':not ds,'qualified_residuals':ds})

preimages = load(AUDIT/'ROOT_CURRENT_INPUT_PREIMAGES.json')
for row in preimages['files']:
    b = read(REPO/row['path'], 'dated_live_native_preimage')
    require(len(b) == row['size'] and sha(b) == row['sha256'], 'dated live13 preimage mismatch '+row['path'])
require(len(preimages['files']) == 13, 'preimage count')
queue=load(CANDIDATE/'CURRENT_QUEUE_PATCH.json')
qb=(CANDIDATE/'queue_proposal/QUEUE_PREIMAGE.md').read_bytes()
qa=(CANDIDATE/'queue_proposal/QUEUE_PROSPECTIVE.md').read_bytes()
require(sha(qb)==queue['whole_queue_preimage_sha256'] and sha(qa)==queue['whole_queue_prospective_sha256'],'queue whole pins')
before=queue['row_before'].encode();after=queue['row_prospective'].encode()
require(qb.count(before)==1 and qa==qb.replace(before,after,1),'queue only exact named row bytes')
fields_before=before.decode().split('|');fields_after=after.decode().split('|')
names=queue['header_names'];allowed={names.index(k)+1 for k in ['Status','Turns','Findings']}
require(len(names)==12 and len(fields_before)==len(fields_after)==14,'queue12 schema')
require(all(a==b for i,(a,b) in enumerate(zip(fields_before,fields_after)) if i not in allowed),'queue unrelated field modification')
require(fields_before[names.index('Status')+1].strip()=='queued' and fields_after[names.index('Status')+1].strip()=='unsolved','queue status')
require(fields_before[names.index('Turns')+1].strip()=='0/5' and fields_after[names.index('Turns')+1].strip()=='2/5','queue turns')
require((REPO/'unsolved_math_prioritization/QUEUE.md').read_bytes()==qb,'live queue preimage unchanged')

snapshot = load(AUDIT/'snapshot_manifest.json')
git_checks=[]
for row in snapshot['files']:
    p = 'unsolved_math_prioritization/attempts/2765/'+row['path']
    completed = subprocess.run(['git','show',snapshot['head']+':'+p],cwd=REPO,capture_output=True)
    b = read(CANDIDATE/'original_archive'/row['path'], 'exact_original_archive')
    require(completed.returncode == 0 and completed.stdout == b, 'original git/archived bytes '+p)
    require(sha(b) == row['sha256'] and len(b) == row['size'], 'original pin mismatch '+p)
    git_checks.append({'path':p,'sha256':sha(b),'whole_git_BYTE_equal':completed.stdout==b})
diff = subprocess.run(['git','diff',snapshot['base'],snapshot['head']],cwd=REPO,capture_output=True)
require(diff.returncode == 0 and diff.stdout == (CANDIDATE/'original_diff.patch').read_bytes(), 'full original17 diff mismatch')
require(subprocess.run(['git','diff','--name-only',snapshot['base'],snapshot['head']],cwd=REPO,capture_output=True).stdout.decode().splitlines() == snapshot['changed_paths'], 'original17 changed paths')

raw={}
for name,row in pins['corpus']['files'].items():
    b=read(REPO/'unsolved_math_prioritization/cache'/name,'foreign_raw_corpus_readonly')
    require(sha(b)==row['sha256'] and len(b)==row['bytes'],'raw corpus pin '+name)
    raw[name]=json.loads(b)
counts=Counter(p['problem_number'] for p in raw['problems.json'])
expected={}
reports=raw['research_results.json']
for p in raw['problems.json']:
    payload=dict(p)
    ambiguous=counts[p['problem_number']]>1 and p['problem_number'] in reports
    if ambiguous:payload['_ambiguous_report']=True
    expected[str(p['id'])]=(payload,{} if ambiguous else reports.get(p['problem_number'],{}))
db=REPO/'unsolved_math_prioritization/cache/catalog.sqlite'
connection=sqlite3.connect(db.as_uri()+'?mode=ro&immutable=1',uri=True)
connection.execute('PRAGMA query_only=ON')
require(connection.execute('SELECT revision FROM metadata').fetchall()==[(pins['corpus']['revision'],)],'SQL revision')
sql_seen=set()
for key,payload,prior in connection.execute('SELECT key,payload,report FROM records ORDER BY key'):
    require(key not in sql_seen and (json.loads(payload),json.loads(prior))==expected.get(key),'whole SQL joined record '+key)
    sql_seen.add(key)
connection.close()
require(sql_seen==set(expected) and len(sql_seen)==15458,'whole SQL row set')
require(expected['2765'][0]==load(CANDIDATE/'source_record.json'),'whole flat source')
require('KP-2.17' not in reports and (CANDIDATE/'prior_report.json').read_bytes()==b'null\n' and load(CANDIDATE/'native_importer_prior_fallback.json')=={},'prior null/fallback qualification')

report={'recorded_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS' if not errors else 'FAIL','errors':errors,'candidate_manifest_sha256':sha(manifest_bytes),'candidate_members_plus_self':[candidate_count,1],'current_dependency_count':len(dep_names),'support_member_count':support_count,'closed_families':families,'entire_byte_reads':reads,'valid_JSON_counts':valid,'exact_malformed_negative_inputs':malformed,'python_AST_count':python_asts,'actual_run_counts':{'outer':12,'nested':108,'administrative':2},'complete_actual_stream_checks':stream_checks,'complete_actual_source_checks':source_checks,'complete_original_stdin_checks':stdin_checks,'whole_original30_72_replay_checks':originals,'full_structured_comparisons_independently_checked':qualified,'live_native_preimages_checked':len(preimages['files']),'original16_git_BYTE_checks':git_checks,'original17_diff_BYTE_equal':diff.stdout==(CANDIDATE/'original_diff.patch').read_bytes(),'full_raw_and_SQL_importer_join_checked':{'raw_problems':len(raw['problems.json']),'raw_reports':len(reports),'SQL_records':len(sql_seen),'mode':'ro+immutable+query_only'},'scope':'Every complete current/dependency/support byte traversed and recorded; complete JSON objects parsed except exactly pinned mutation inputs with raw provenance. Human semantic reading ledger is separate. No all-metric mathematical proof is supplied by these finite provenance checks. No candidate tool executed and no shared state changed.'}
(HERE/'WHOLE_CURRENT_COVERAGE.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ['entire_byte_reads','complete_actual_stream_checks','complete_actual_source_checks','complete_original_stdin_checks','original16_git_BYTE_checks','exact_malformed_negative_inputs']},indent=2))
