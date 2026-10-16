#!/usr/bin/env python3
"""PROPOSED UNEXECUTED SOURCE. ROOT alone may run after full personal reading.

This source authors six genuine dated prerequisite records only when explicitly
run by ROOT. It does not import, compile or run the production builder/operator,
mathematical helpers, closer or verifier, and grants no future acceptance.
"""
from pathlib import Path, PurePosixPath
import argparse, datetime as dt, hashlib, json, math, os, re, stat, subprocess, sys, traceback

R = Path('/Users/alec/Documents/Math')
# Explicit audit anchor: this draft lives in a new nested preparation folder.
A = R / 'draft_pr_publication_program_20260930/audits/pr49_30000703'
S = A / 'current_preparation_family'
F = A / 'current_source_adversary_family'
B = A.parent / 'pr45_9900007'
PM = '4324c2a69762752b42b159b141a629b55a6dda5351817afff12e4f2d0950e4cd'
FM = '53a1e404afcfd79aae8d222c682dde55dea009917e8ad0d7917a634a62876e30'
BUILDER = '023d21b553245153db874ce97a2b68e8e16272c9c467c819235c7e71413b9bd5'
OPERATOR = '28cc4387b850820200831f8a80410edb60808e69464e6895b71b4efa37ff76f0'
REPORT = 'b1691a83631b4ccf1d35cbf96498c5875fec8c1fcf8d42c44c0a10db44563510'
VERDICT = 'a1833d72b89bd5246e4e9547dc86d8fdaef4aea485f4f2cc9286b9640e3b13f0'
FIXED = '0c590341de2af06f969a990579fc7f88d0ef775e602330033225c39e10c7598f'
CAP_OPERATOR = 'c1ae969ccbbc48ed6fb486e96184da94329291a46b27d2b891ecb87185c909ec'
FLAGS = ['original16_complete17_path_diff_helpers_results_metadata_fully_read',
         'exact_unrestricted_arc_reflection_and_derivative_scope_checked',
         'raw_all15458_SQL_report_ABSENT_literal_empty_fallback_null_marker_fully_read',
         'actual_ROOT33_Git_and_three_literal_replays_fully_read',
         'both_closed_independent_mathematical_family_reports_fully_read',
         'credited2007_known_target_no_project_novelty_accepted',
         'operative_source_history_and_full_journal_proof_qualifications_fully_read',
         'new_source_adversary_closed_clean_complete_report_personally_read']
FIVE = ['ROOT_CURRENT_KNOWN_RESULT_SCOPE_CERTIFICATE.md', 'ROOT_PRIMARY_READ_LEDGER.json',
        'ROOT_SCIENCE_CARD.json', 'ROOT_CURRENT_INPUT_PREIMAGES.json', 'ROOT_EVIDENCE_BINDINGS.json']

def need(x, message):
    if not x: raise ValueError(message)

def stamp(): return dt.datetime.now(dt.timezone.utc).isoformat()
def sha(b): return hashlib.sha256(b).hexdigest()
def encode(v): return (json.dumps(v, indent=2, ensure_ascii=False, allow_nan=False)+'\n').encode()

def relative(s):
    need(type(s) is str and s and s != '.' and '\\' not in s and '\0' not in s, 'Relative path text')
    p = PurePosixPath(s)
    need(not p.is_absolute() and p.as_posix() == s and not set(p.parts)&{'.','..','.git','__pycache__'}, 'Canonical relative path')
    return s

def raw(p):
    need(not p.is_symlink() and all(not q.is_symlink() for q in p.parents) and stat.S_ISREG(p.stat().st_mode), 'Regular nonsymlink file')
    return p.read_bytes()

def load(p):
    def pairs(items):
        d = {}
        for k, v in items: need(k not in d, 'Duplicate JSON key'); d[k] = v
        return d
    def number(s):
        f = float(s); need(math.isfinite(f), 'Finite JSON float'); return f
    def bad(s): raise ValueError('Nonfinite JSON constant')
    return json.loads(raw(p), object_pairs_hook=pairs, parse_float=number, parse_constant=bad)

def clock(s):
    need(type(s) is str, 'UTC text'); t = dt.datetime.fromisoformat(s.replace('Z','+00:00'))
    need(t.tzinfo is not None and t.utcoffset() == dt.timedelta(0), 'Aware UTC'); return t

def ref(p, mode=False):
    b = raw(p); r = dict(path=relative(p.relative_to(R).as_posix()), bytes=len(b), sha256=sha(b))
    if mode: r['full_mode'] = stat.S_IMODE(p.stat().st_mode)
    return r

def typed_row(r, mode=False):
    need(type(r) is dict and set(r) == ({'path','bytes','sha256','full_mode'} if mode else {'path','bytes','sha256'}), 'Exact row schema')
    relative(r['path']); need(type(r['bytes']) is int and r['bytes'] >= 0 and type(r['sha256']) is str and re.fullmatch('[0-9a-f]{64}',r['sha256']), 'Typed size/SHA')
    if mode: need(type(r['full_mode']) is int and 0 <= r['full_mode'] < 4096, 'Typed full mode')

def check(r, mode=True):
    typed_row(r, mode); q = ref(R/r['path'], mode); need(q == r, 'Complete body/full mode binding changed'); return q

def write(p, v):
    b = v if type(v) is bytes else encode(v)
    with p.open('xb') as h: h.write(b); h.flush(); os.fsync(h.fileno())
    return ref(p)

def closure(root, selfname, schema, digest, count, directory_count):
    need(sha(raw(root/selfname)) == digest, 'Pinned self manifest')
    m = load(root/selfname)
    need(m['schema'] == schema and m['self_excluded'] == [selfname] and type(m['files_count']) is int and m['files_count'] == len(m['files']) == count, 'Exact self-only closure schema')
    owned = []; names = set()
    for r in m['files']:
        typed_row(r, True); need(r['path'] not in names and r['full_mode'] == 0o444, 'Unique closed full0444 member'); names.add(r['path'])
        owned.append(check(dict(r, path=root.relative_to(R).as_posix()+'/'+r['path'])))
    files = set(); dirs = {'.':stat.S_IMODE(root.stat().st_mode)}
    need(root.is_dir() and not root.is_symlink() and all(not q.is_symlink() for q in root.parents), 'Nonsymlink closure root')
    for p in root.rglob('*'):
        need(not p.is_symlink(), 'No closure symlinks'); n = relative(p.relative_to(root).as_posix()); mode = p.stat().st_mode
        if stat.S_ISREG(mode): files.add(n)
        else: need(stat.S_ISDIR(mode), 'No special members'); dirs[n] = stat.S_IMODE(mode)
    expected = {'.'}|{str(p) for n in names for p in PurePosixPath(n).parents if str(p) != '.'}
    need(files == names|{selfname} and set(dirs) == expected, 'Exact files/ancestor topology')
    manifest_dirs = {}
    for r in m['directories']:
        need(type(r) is dict and set(r) == {'path','full_mode'} and type(r['full_mode']) is int and 0 <= r['full_mode'] < 4096, 'Typed directory row')
        need(r['path'] == '.' or relative(r['path']), 'Directory path'); need(r['path'] not in manifest_dirs, 'Unique directories'); manifest_dirs[r['path']] = r['full_mode']
    need(dirs == manifest_dirs and len(dirs) == directory_count and stat.S_IMODE((root/selfname).stat().st_mode) == 0o444, 'Exact directory modes/self full0444')
    return m, owned

def cap4(name, pid, target, option, value, manifest_sha, closing_pid, count, ndirs, status):
    d = B/name; need({p.name for p in d.iterdir()} == {'CAPTURE.json','prelaunch_operator.py','stdout.bin','stderr.bin'}, 'Exact CAP4 topology')
    c = load(d/'CAPTURE.json')
    need(c['schema'] == 'root-explicit-command-capture/v1' and c['actual_execution'] is True and c['completed'] is True and type(c['pid']) is int and c['pid'] == pid and type(c['exit_code']) is int and c['exit_code'] == 0 and c['operator_unchanged'] is True and c['stdin_supplied'] is False and type(c['expected_exit_code']) is int and c['expected_exit_code'] == 0 and c['status'] == 'PASS' and 'operator_error' not in c, 'Actual successful child identity')
    need(c['argv'] == ['/usr/bin/python3','-B',str(target),option,value] and c['cwd'] == str(R), 'Exact causal role argv/cwd')
    need(c['operator_sha256'] == CAP_OPERATOR == sha(raw(d/'prelaunch_operator.py')), 'Complete operator prelaunch source')
    need(clock(c['started_utc']) < clock(c['finished_utc']) <= dt.datetime.now(dt.timezone.utc), 'Actual capture times')
    for k in ['stdout','stderr']:
        r = c[k]; typed_row(r); need(r['path'] == k+'.bin', 'Local split stream'); b = raw(d/r['path'])
        need(len(b) == r['bytes'] and sha(b) == r['sha256'], 'Complete stream body/typed size')
    need(c['stderr']['bytes'] == 0, 'Actual success empty stderr'); o = load(d/'stdout.bin')
    need(o['status'] == status and type(o['actual_closing_pid']) is int and o['actual_closing_pid'] == closing_pid and o['manifest_sha256'] == manifest_sha and type(o['files_count']) is int and o['files_count'] == count and type(o['directories_count']) is int and o['directories_count'] == ndirs, 'Entire printed role result binds exact manifest/PID/count')
    if option == '--expected-manifest-sha256': need(type(o['actual_readback_pid']) is int and o['actual_readback_pid'] == pid and type(o['readback_writes']) is int and o['readback_writes'] == 0, 'Distinct read-only child')
    return dict(complete_capture=c, complete_members=[ref(p, True) for p in sorted(d.iterdir())], complete_stdout_object=o, captured_operator_source_only=True, child_target_current_closure_binding=ref(target,True))

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--execute',action='store_true'); parser.add_argument('--root-personal-reading-confirmed',action='store_true')
    args = parser.parse_args()
    need(args.execute and args.root_personal_reading_confirmed and not sys.flags.optimize and os.environ.get('PYTHONOPTIMIZE','') in ('','0'), 'Explicit ROOT execution and complete personal reading required')
    need(Path.cwd() == R, 'Repository cwd required')
    for n in FIVE+['ROOT_NEW_SOURCE_ADVERSARY_RECORD.json','root_current_prerequisite_Git_actual_captures']:
        need(not (A/n).exists() and not (A/n).is_symlink(), 'Never overwrite a genuine prerequisite or retained capture')
    need(not (A/'reviewed_candidate').exists() and not (A/'reviewed_candidate').is_symlink(), 'No existing current candidate')
    source_path = Path(__file__).absolute(); source_body = raw(source_path)
    prep, source_owned = closure(S,'PREPARATION_MANIFEST.json','pr49-current-source-only-closure/v1',PM,119,19)
    need(sha(raw(S/'prepare_current_packet.py')) == BUILDER and sha(raw(S/'capture_root_builder_operation.py')) == OPERATOR, 'Exact unexecuted production text')
    # Compare the literal FLAGS line as text, without parsing/importing production.
    flag_line = next(line for line in raw(S/'prepare_current_packet.py').decode().splitlines() if line.startswith('FLAGS='))
    need(flag_line == 'FLAGS='+repr(FLAGS).replace(', ',','), 'Exact eight production reading flags')
    m, owned = closure(F,'MANIFEST.json','pr49-current-source-adversary-self-only-closure/v1',FM,74,11)
    need(sha(raw(F/'REPORT.md')) == REPORT and sha(raw(F/'VERDICT.json')) == VERDICT and sha(raw(F/'FIXED_READ_RESULT.json')) == FIXED, 'Exact full report/verdict/fixed ledger')
    v = load(F/'VERDICT.json'); fixed = load(F/'FIXED_READ_RESULT.json'); final = load(F/'FINAL_SOURCE_READ_RESULT.json')
    need(v['verdict'] == 'PASS_CURRENT_SOURCE_WITH_EXPLICIT_BOUNDED_QUALIFICATIONS' and v['mandatory_corrections'] == [] and v['future_acceptance_approved'] is False and v['did_author_current_SOURCE'] is False and v['current_SOURCE_preparer_was_different_reviewer'] is True and v['new_whole_current_review_gate'] == 'PENDING', 'Bounded different SOURCE review')
    need(v['status'] == 'already_solved' and v['credit'] == 'Kraus, Roth and Ruscheweyh (2007)' and v['full_2007_journal_proof_independently_certified'] is False and v['separate_original_source_response_count'] is None, 'Known-result qualifications')
    need(fixed['schema'] == 'pr49-current-source-adversary-fixed-read/v1' and fixed['status'] == 'PASS_COMPLETE_CURRENT_SOURCE_AND_FIXED_FIRST_PARTY_INSPECTION' and type(fixed['fixed_files']) is int and fixed['fixed_files'] == 1184 and type(fixed['source_files']) is int and fixed['source_files'] == 119, 'Complete fixed/read ledger')
    external = []; names = set()
    for r in fixed['checked_body_mode_rows']:
        typed_row(r,True); need(r['path'] not in names, 'Unique fixed rows'); names.add(r['path']); external.append(check(r))
    need(len(external) == 1312, 'Entire 1312 unique fixed rows')
    normalized_final = []
    for r in final['full_report_verdict_closer_verifier_operator_bindings']:
        typed_row(r,True); need((R/r['path']).parent == F and r['full_mode'] == 420, 'Historical own preclosure mode retained')
        q = ref(R/r['path'],True); need(all(q[k] == r[k] for k in ['path','bytes','sha256']) and q['full_mode'] == 292, 'Normalize separate actual postclosure own full0444'); normalized_final.append(q)
    need(len(normalized_final) == 5, 'Entire five final historical own bindings')
    captures = [
        cap4('root_pr49_current_source_closure_actual_capture',1200,S/'close_source_preparation.py','--expected-report-sha256','40b49e6a3c5c26cc7da6afc297b36c2402e727487a42d81b6630f18e15a0411b',PM,1200,119,19,'PASS_ROOT_SOURCE_SELF_ONLY_CLOSURE'),
        cap4('root_pr49_current_source_closed_readback_actual_capture',1444,S/'verify_source_preparation_readonly.py','--expected-manifest-sha256',PM,PM,1200,119,19,'PASS_SEPARATE_ROOT_SOURCE_READONLY_READBACK'),
        cap4('root_pr49_current_source_adversary_closure_actual_capture',31633,F/'close_current_source_adversary.py','--expected-report-sha256',REPORT,FM,31633,74,11,'PASS_ROOT_CURRENT_SOURCE_ADVERSARY_SELF_ONLY_CLOSURE'),
        cap4('root_pr49_current_source_adversary_closed_readback_actual_capture',32273,F/'verify_current_source_adversary_readonly.py','--expected-manifest-sha256',FM,FM,31633,74,11,'PASS_SEPARATE_ROOT_CURRENT_SOURCE_ADVERSARY_READONLY_READBACK')]
    for i, manifest in [(0,prep),(2,m)]:
        c = captures[i]['complete_capture']; d = captures[i+1]['complete_capture']
        need(type(manifest['actual_closing_pid']) is int and manifest['actual_closing_pid'] == c['pid'] and clock(c['started_utc']) <= clock(manifest['created_utc']) <= clock(c['finished_utc']) < clock(d['started_utc']), 'True original closure and separate postexit readback chronology')
    limits = load(F/'SCOPE_AND_LIMITS_RESULT.json'); closepre = limits['ROOT_source_closer_prelaunch']; check(closepre)
    need(raw(R/closepre['path']) == raw(S/'close_source_preparation.py'), 'Preserved actual ROOT SOURCE closer prelaunch equals closed source')
    # Historical ledger and own preclosure rows remain literal; normalized rows are additional observations.
    G = A/'root_current_prerequisite_Git_actual_captures'; G.mkdir(exist_ok=False); commands = []
    native = {'unsolved_math_prioritization/'+n for n in ['QUEUE.md','state.json','history.jsonl','catalog.json','assessments.json','queue.py','policy.json','manifest.json','cache/problems.json','cache/research_results.json','cache/catalog.sqlite','review_v2/related_target_groups.json']}
    native.add('draft_pr_publication_program_20260930/inventory.json')
    native4 = ['unsolved_math_prioritization/QUEUE.md','unsolved_math_prioritization/state.json','unsolved_math_prioritization/history.jsonl','draft_pr_publication_program_20260930/inventory.json']
    head = None
    def git(argv):
        allowed = [['git','branch','--show-current'],['git','rev-parse','HEAD']]
        if head is not None: allowed += [['git','show',head+':'+n] for n in native4]
        need(argv in allowed, 'Exact read-only whitelist')
        d = G/str(len(commands)); d.mkdir(exist_ok=False)
        write(d/'PRELAUNCH_OPERATOR.py',source_body)
        pre = dict(schema='pr49-root-prerequisite-readonly-git-prelaunch/v1',argv=argv,cwd=str(R),operator_pid=os.getpid(),parent_pid=os.getppid(),created_utc=stamp(),source=None,source_unchanged=None,operator_source=ref(d/'PRELAUNCH_OPERATOR.py'),operator_sha256=sha(source_body))
        write(d/'PRELAUNCH.json',pre)
        c = dict(pre,schema='pr49-root-prerequisite-readonly-git-actual/v1',started_utc=stamp(),actual_execution=False,completed=False,pid=None,exit_code=None,stdin_supplied=False)
        try:
            with (d/'stdout.bin').open('xb') as out,(d/'stderr.bin').open('xb') as err:
                child = subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=out,stderr=err,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0')); c.update(actual_execution=True,pid=child.pid)
                try: c['exit_code'] = child.wait(timeout=60); c['completed'] = True
                except BaseException: child.kill(); c['exit_code'] = child.wait(); raise
        except BaseException: c['failure'] = traceback.format_exc(); raise
        finally:
            c['finished_utc'] = stamp()
            for k in ['stdout','stderr']:
                if (d/(k+'.bin')).exists(): b = raw(d/(k+'.bin')); c[k] = dict(path=k+'.bin',bytes=len(b),sha256=sha(b))
            try: c['operator_unchanged'] = raw(source_path) == source_body
            except BaseException: c['operator_unchanged'] = False; c['operator_read_failure'] = traceback.format_exc()
            write(d/'CAPTURE.json',c); commands.append(c)
        need(c['actual_execution'] is True and c['completed'] is True and type(c['exit_code']) is int and c['exit_code'] == 0 and c['operator_unchanged'] is True and not raw(d/'stderr.bin'), 'Successful complete actual readonly Git')
        return raw(d/'stdout.bin')
    need(git(['git','branch','--show-current']) == b'main\n','Actual main before reading')
    head = git(['git','rev-parse','HEAD']).decode().strip(); need(re.fullmatch('[0-9a-f]{40}',head), 'Actual current HEAD')
    files = [ref(R/n,True) for n in sorted(native)]; need(len(files) == 13, 'Exact thirteen live bodies/full modes')
    for n in native4: need(git(['git','show',head+':'+n]) == raw(R/n), 'Native4 live equals committed main')
    for r in files: check(r)
    need(git(['git','branch','--show-current']) == b'main\n' and git(['git','rev-parse','HEAD']).decode().strip() == head, 'Main/HEAD stable after all reads')
    for r in external+owned+source_owned+normalized_final: check(r)
    for capture in captures:
        for r in capture['complete_members']: check(r)
    check(closepre)
    closure(S,'PREPARATION_MANIFEST.json','pr49-current-source-only-closure/v1',PM,119,19)
    closure(F,'MANIFEST.json','pr49-current-source-adversary-self-only-closure/v1',FM,74,11)
    need(sha(raw(S/'PREPARATION_MANIFEST.json')) == PM and sha(raw(F/'MANIFEST.json')) == FM and raw(source_path) == source_body, 'Self/production review/author unchanged')
    record = dict(schema='pr49-root-new-source-adversary-record/v1',approved_by_root=True,complete_report_personally_read=True,new_different_source_adversary=True,closed_clean=True,mandatory_corrections=[],created_utc=stamp(),
        preparation_manifest_sha256=PM,builder_sha256=BUILDER,operator_sha256=OPERATOR,manifest=ref(F/'MANIFEST.json'),report=ref(F/'REPORT.md'),members=[{k:r[k] for k in ['path','bytes','sha256']} for r in owned],
        completed_closing_capture=ref(B/'root_pr49_current_source_adversary_closure_actual_capture/CAPTURE.json'),completed_postexit_readback_capture=ref(B/'root_pr49_current_source_adversary_closed_readback_actual_capture/CAPTURE.json'),
        complete_VERDICT_object=v,complete_source_adversary_manifest_object=m,complete_fixed_read_ledger_object=fixed,normalized_complete_owned_body_mode_rows=owned,individual_complete_external_bindings=external,
        complete_final_read_object=final,normalized_postclosure_final_own_rows=normalized_final,complete_actual_SOURCE_and_adversary_closure_readback_captures=captures,ROOT_SOURCE_closer_prelaunch_binding=closepre,
        all74_closed_members_full_bytes_modes_read=True,all1312_external_complete_bytes_modes_read=True,actual_postexit_capture_chronology_checked=True,production_import_compile_execution=False,new_whole_current_gate='PENDING',future_acceptance_approved=False,
        independence_qualification='Different current SOURCE reviewer reused the closed boundary mathematical review and inherited context; not a new blind mathematics review. SOURCE preparer reused the different hyperbolic context. ROOT personally read the entire bounded report/verdict/helpers and reconciled optional CAP4/type/path limits; actual captures here receive stricter causal role checks. Four historical reviewer failures remain literal, with corrected distinct versions. No historical PASS becomes whole-current or future acceptance.',
        source_only_author_provenance=dict(path=source_path.relative_to(R).as_posix(),sha256=sha(source_body),actual_pid=os.getpid(),actual_parent_pid=os.getppid()),
        historical_own420_rows_preserved_current292_rows_separate=True,CAP4_captured_prelaunch_scope='Operator source only; target sources are independently bound to current closed members. No invented target-at-launch snapshot.',raw_or_SQL_or_foreign_source_bodies_copied=False)
    record_ref = write(A/'ROOT_NEW_SOURCE_ADVERSARY_RECORD.json',record)
    scope = '''# ROOT PR49 exact known-result acceptance

ROOT_SCOPE_ACCEPTED_EXACT_KNOWN_RESULT_ONLY

PR49 / 30000703 / OWR-1460-009
Original head: 036a5ed59bee5ed79f08349290481584610f1456
GitHub base and actual merge base: c6975ca76f9f667f1250ba403d0e6da2aafe14d0
Status: already_solved
Original turns: 0/5; new: 0; audit: 0
Full exact target verified: true
Novelty: false
Credit: Kraus, Roth and Ruscheweyh (2007)
Imported journal proof independently certified: false
NEW whole-current review: PENDING
Paper/new DOI/tracker: false

The ordinary unrestricted Schwarz-Pick distortion limit1 at boundary point1 is equivalent to local holomorphic circle reflection across an open arc containing1, with unimodular boundary values and finite positive oriented derivative. This credits the exact known target and supplies no project discovery. It implies local conformality, not global injectivity, a finite Blaschke product, whole-circle continuation, derivative equal1, or a radial/angular-only characterization. Neighboring Problem2 is outside scope.

The full2007 journal proof is imported, not independently certified. ROOT's primary browser text reads are distinct from the closed mathematical reviewers' authenticated PDF/pixel inspections. No exhaustive priority or absence-of-newer-literature assertion is made. Original16 and operative11 science/helper/results/plain integer source/admin null/turn/sourcechecksum bytes remain literal. Upstream report key ABSENT, SQLite importer fallback{}, and original administrative null are distinct. Original0/5,new0,audit0 have no invented original source-response field. Historical runtime/PASS/pending claims are dated, with no current runtime certification. Extensive AI use; unrefereed, no human peer review claimed.

This certificate approves the credited known scope for administrative preparation only. The actual postexit current freeze still needs a NEW whole-current source-first adversary and ROOT's complete reconciliation. Later integration requires a fresh13/main/foreign-work check and independently reviewed acceptance source; these dated prerequisites grant no future merge/native/publication authority.
'''.encode()
    scope_ref = write(A/'ROOT_CURRENT_KNOWN_RESULT_SCOPE_CERTIFICATE.md',scope)
    common = dict(approved_by_root=True,operative_preparation_directory='current_preparation_family',created_utc=stamp(),preparation_manifest_sha256=PM,source_qualification_sha256=sha(raw(S/'SOURCE_PRECISION_QUALIFICATIONS.md')))
    evidence = dict(common,schema='pr49-root-evidence-bindings/v1',manifest=ref(A/'root_original_actual_reproduction/MANIFEST.json'),summary=ref(A/'root_original_actual_reproduction/ROOT_CURRENT_REPRODUCTION_SUMMARY.json'),proof_notes=ref(A/'ROOT_MATHEMATICAL_REVIEW.md'),raw_audit=ref(A/'ROOT_COMPLETE_RAW_SQL_AUDIT.json'),source_adversary=record_ref,future_acceptance_approved=False)
    evidence_ref = write(A/'ROOT_EVIDENCE_BINDINGS.json',evidence)
    reading = dict(common,schema='pr49-root-primary-read-ledger/v1',reading_completed=True,root_flags={f:True for f in FLAGS},scope_certificate_sha256=scope_ref['sha256'],evidence_bindings_sha256=evidence_ref['sha256'],future_acceptance_approved=False,
        reading_notes='ROOT personally read original16 science and complete17-path diff, full literal helpers/results/plain source/admin null/object turns and metadata; both closed independent mathematical reports/proofs; ROOT33 actual Git and three69/duplicate69/187 literal replays with duplicate not independent; complete raw15458 derived audit with ABSENT/SQL{} versus original null; and current production source/history/global qualifications as text. ROOT read the entire newly closed bounded SOURCE report/verdict/helpers and reconciled all74 payloads,1312 unique fixed/read ledger rows, separate original/current mode observations and all four true SOURCE/adversary closing/readback CAP4 sources/argv/streams/PIDs/UTC. The exact known unrestricted reflection criterion is credited to Kraus,Roth,Ruscheweyh2007; complete journal proof is imported, not independently certified. NEW whole-current acceptance remains pending.')
    write(A/'ROOT_PRIMARY_READ_LEDGER.json',reading)
    science = dict(common,schema='pr49-root-science-card/v1',scope_certificate_sha256=scope_ref['sha256'],evidence_bindings_sha256=evidence_ref['sha256'],status='already_solved',exact_known_target_verified=True,full_problem_solved=True,full_target_prior_result_verified=True,project_solved=False,novelty_claimed=False,credit='Kraus, Roth and Ruscheweyh (2007)',full_2007_journal_proof_independently_certified=False,original_substantive_attempts=0,turn_limit=5,new_substantive_attempts=0,audit_turns=0,paper_created=False,new_DOI_created=False,tracker_row_created=False,current_model=None,current_reasoning_effort=None,current_deadline_utc=None,current_verdict=None,new_whole_current_gate='PENDING',future_acceptance_approved=False,
        strongest_verified_result='The exact unrestricted limit at1 is equivalent to local holomorphic circle reflection, with unimodular arc values, positive finite oriented derivative and local conformality; credited prior theorem, no project novelty.',remaining_current_gap='NEW whole-current adversary of actual postexit packet, ROOT full reconciliation and later fresh13/main integration authority; full2007 journal proof remains imported.')
    write(A/'ROOT_SCIENCE_CARD.json',science)
    for r in files: check(r)
    write(A/'ROOT_CURRENT_INPUT_PREIMAGES.json',dict(schema='pr49-root-fresh13-input-preimages/v1',approved_by_root=True,created_utc=stamp(),reason='ROOT read all13 full live bodies and complete mode bits in place, checked native4 against captured committed main and rechecked every body/mode/main/HEAD after reading. Dated current-freeze authority only; fresh checks are needed again before later integration.',current_head=head,files=files,operative_preparation_directory='current_preparation_family'))
    print(json.dumps(dict(status='PASS_GENUINE_ROOT_CURRENT_FREEZE_PREREQUISITES_ONLY',actual_pid=os.getpid(),actual_parent_pid=os.getppid(),current_head=head,source_members=74,source_external_bindings=1312,complete_source_record=ref(A/'ROOT_NEW_SOURCE_ADVERSARY_RECORD.json'),five_actual_prerequisites=[ref(A/n) for n in FIVE],actual_readonly_Git_children=len(commands),new_whole_current_gate='PENDING',future_acceptance_approved=False),indent=2))

if __name__ == '__main__': main()
