#!/usr/bin/env python3
"""SOURCE ONLY. ROOT may freeze an absent PR46 packet after genuine source reading.

This program performs administrative copying and read-only Git queries. It never
imports, compiles or executes any candidate or family mathematical helper. It
never changes native inputs, canonical attempts, Git/index, a remote or people.
Actual attempts, failures and complete streams remain in the audit-local tmp.
"""
import argparse
import ctypes
import datetime as dt
import hashlib
import json
import math
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import sys
import traceback

HEAD = 'a39d178b10f75fb127058b08e0d0002b3ae97f8a'
BASE = 'c6975ca76f9f667f1250ba403d0e6da2aafe14d0'
MERGE_BASE = BASE
SCIENCE = 'a0d374da6984537cd9902e2e790177791739bdc32ea820b74830a6b50241ea6c'
GATE = 'PENDING_NEW_WHOLE_CURRENT_SOURCE_FIRST_ADVERSARY'
FLAGS = ['original13_complete14_path_diff_helpers_results_metadata_fully_read', 'operative_OWR668669_v1Theorem2_Section22_v2Example1_Lemma9_Theorem3_fully_read', 'every_degree_all_periods_RP1_full2dplus1_ordinary_real_open_proof_accepted', 'whole_raw_SQL_prior_presence_or_null_and_literal_empty_fallback_fully_read', 'unchanged_author51_and_independent848_actual_reproductions_fully_read', 'both_closed_independent_math_families_fully_read', 'scoped_original_closure_family_exclusions_first_party_topology_checked', 'known_Kozhasov_Kummer_preprint_credit_no_discovery_scope_accepted', 'new_source_adversary_closed_clean_complete_report_personally_read']
HEADER = ['Rank', 'ID / code', 'Problem', 'EV', 'Impact (/10)', 'Difficulty',
          'Proposed', 'Status', 'Turns', 'Chat', 'Findings', 'DOI']
NATIVE = {'unsolved_math_prioritization/' + name for name in [
    'QUEUE.md', 'state.json', 'history.jsonl', 'catalog.json', 'assessments.json',
    'queue.py', 'policy.json', 'manifest.json', 'cache/problems.json',
    'cache/research_results.json', 'cache/catalog.sqlite',
    'review_v2/related_target_groups.json']}
NATIVE.add('draft_pr_publication_program_20260930/inventory.json')
IMMUTABLE = ['SOURCE_STATUS.md', 'verification.json', 'verify.py', 'source_record.json', 'turns.json', 'provenance.json', 'independent_review/independent_checks.py', 'independent_review/independent_results.json']

def require(value, message):
    if not value:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def encode(value):
    return (json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + '\n').encode()


def equal(a, b):
    # Serialized scalar tokens distinguish integers, booleans and nulls.
    return json.dumps(a, sort_keys=True, ensure_ascii=False, allow_nan=False,
                      separators=(',', ':')) == json.dumps(
        b, sort_keys=True, ensure_ascii=False, allow_nan=False, separators=(',', ':'))


def hex64(value):
    return type(value) is str and re.fullmatch('[0-9a-f]{64}', value) is not None


def utc():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def clock(value):
    require(type(value) is str, 'Explicit aware UTC timestamp required')
    parsed = dt.datetime.fromisoformat(value[:-1] + '+00:00' if value.endswith('Z') else value)
    require(parsed.tzinfo is not None and parsed.utcoffset() == dt.timedelta(0), 'UTC required')
    return parsed


def load(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, 'Duplicate JSON key: ' + key)
            result[key] = value
        return result
    def constant(value):
        raise ValueError('Invalid JSON constant: ' + value)
    def floating(value):
        result = float(value)
        require(math.isfinite(result), 'Nonfinite JSON number')
        return result
    return json.loads(raw, object_pairs_hook=pairs, parse_constant=constant, parse_float=floating)


def structured(name, raw):
    if name.endswith('.json'):
        load(raw)
    elif name.endswith('.jsonl'):
        for line in raw.splitlines():
            require(line.strip(), 'Blank JSONL row rejected')
            load(line)


def relative(value):
    require(type(value) is str and value and '\\' not in value and '\0' not in value, 'POSIX relative path required')
    path = PurePosixPath(value)
    require(not path.is_absolute() and path.as_posix() == value and
            not {'.', '..', '.git', '__pycache__'}.intersection(path.parts), 'Unsafe path: ' + value)
    return value


def regular(path):
    require(not path.is_symlink() and all(not p.is_symlink() for p in path.parents),
            'Symlink path rejected: ' + str(path))
    require(stat.S_ISREG(path.stat().st_mode), 'Regular file required: ' + str(path))
    return path.read_bytes()


def inventory(root):
    require(root.is_dir() and not root.is_symlink() and
            all(not p.is_symlink() for p in root.parents), 'Regular directory required')
    files, directories = set(), set()
    for path in root.rglob('*'):
        require(not path.is_symlink(), 'Symlink member rejected')
        name = relative(path.relative_to(root).as_posix())
        mode = path.stat().st_mode
        if stat.S_ISREG(mode):
            files.add(name)
        else:
            require(stat.S_ISDIR(mode), 'Special member rejected')
            directories.add(name)
    expected = {p.as_posix() for name in files for p in PurePosixPath(name).parents
                if p.as_posix() != '.'}
    require(directories == expected, 'Extra/empty directory rejected')
    return files


def rows(items):
    require(type(items) is list, 'Rows must be a list')
    names = set()
    for item in items:
        require(type(item) is dict and set(item) == {'path', 'bytes', 'sha256'},
                'Exact path/bytes/SHA row required')
        name = relative(item['path'])
        require(name not in names, 'Duplicate row path')
        names.add(name)
        require(type(item['bytes']) is int and item['bytes'] >= 0 and hex64(item['sha256']),
                'Typed bytes/SHA required')
    return names


def publish_absent(source, destination):
    require(sys.platform == 'darwin', 'Reviewed macOS exclusive publication required')
    libc = ctypes.CDLL(None, use_errno=True)
    rename = libc.renamex_np
    rename.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_uint]
    rename.restype = ctypes.c_int
    # RENAME_EXCL is 0x00000004 on macOS; never use replacement rename.
    if rename(os.fsencode(source), os.fsencode(destination), 4) != 0:
        number = ctypes.get_errno()
        raise OSError(number, os.strerror(number), str(destination))


def build(args, script, audit, repo, attempt):
    destination=audit/'reviewed_candidate'
    require(not destination.exists() and not destination.is_symlink(), 'Never overwrite a candidate')
    dependencies, outputs, commands={}, {}, []
    def bind(name, role, expected=None):
        name=relative(name); raw=regular(audit/name)
        # Arbitrary archived streams are literal bytes, including empty failed .json.
        row={'path':name,'bytes':len(raw),'sha256':sha(raw),'roles':[role]}
        require(expected is None or row['sha256']==expected, 'Pinned input changed: '+name)
        if name in dependencies:
            old=dependencies[name]
            require(all(old[k]==row[k] for k in ['path','bytes','sha256']), 'Repeated dependency changed')
            row['roles']=sorted(set(old['roles']+row['roles']))
        dependencies[name]=row
        return raw
    def checked(row, role):
        rows([row]); raw=bind(row['path'],role,row['sha256'])
        require(len(raw)==row['bytes'], 'Pinned byte count changed')
        return raw
    def git(*argv):
        require(argv and argv[0] in {'branch','rev-parse','show','ls-tree','diff'}, 'Read-only Git only')
        require(argv[0]!='branch' or argv[1:]==('--show-current',), 'Read-only branch query only')
        directory=attempt/'git'; directory.mkdir(exist_ok=True); index=len(commands)
        rec={'argv':['git',*argv],'cwd':str(repo),'started_utc':utc(),'actual_execution':False,
          'completed':False,'pid':None,'exit_code':None,'stdin_supplied':False}; commands.append(rec)
        try:
            with (directory/(str(index)+'.stdout')).open('xb') as out, (directory/(str(index)+'.stderr')).open('xb') as err:
                child=subprocess.Popen(rec['argv'],cwd=repo,stdin=subprocess.DEVNULL,stdout=out,stderr=err,
                  env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'))
                rec.update(actual_execution=True,pid=child.pid)
                try: rec['exit_code']=child.wait(timeout=60); rec['completed']=True
                except BaseException: child.kill(); rec['exit_code']=child.wait(); raise
        except BaseException: rec['failure']=traceback.format_exc(); raise
        finally:
            rec['finished_utc']=utc()
            for channel in ['stdout','stderr']:
                path=directory/(str(index)+'.'+channel)
                if path.exists():
                    raw=regular(path); rec[channel]={'path':path.relative_to(attempt).as_posix(),'bytes':len(raw),'sha256':sha(raw)}
            (attempt/'GIT_COMMANDS.json').write_bytes(encode(commands))
        require(rec['completed'] is True and type(rec['exit_code']) is int and rec['exit_code']==0, 'Actual read-only Git failed; retained')
        require(not regular(directory/(str(index)+'.stderr')), 'Unexpected Git stderr; retained')
        return regular(directory/(str(index)+'.stdout'))
    prep_raw=bind('current_preparation_family_v2/PREPARATION_MANIFEST.json','closed_source_preparation')
    prep=load(prep_raw)
    require(prep['schema']=='PR46_CURRENT_SOURCE_ONLY_CLOSURE_v2' and prep['status']=='CLOSED_SOURCE_ONLY_CURRENT_PREPARATION'
      and prep['self_excluded']==['PREPARATION_MANIFEST.json'] and type(prep['files_count']) is int
      and prep['files_count']==len(prep['files']), 'Closed SOURCE-only preparation required')
    names=rows(prep['files'])
    require(inventory(script.parent)==names|{'PREPARATION_MANIFEST.json'}, 'Exact SOURCE closure changed')
    for row in prep['files']:
        require(stat.S_IMODE((script.parent/row['path']).stat().st_mode)==0o444, 'SOURCE member full0444 required')
        outputs['build/source_preparation/'+row['path']]=checked(dict(row,path='current_preparation_family_v2/'+row['path']), 'reviewed_SOURCE_preparation')
    require(stat.S_IMODE((script.parent/'PREPARATION_MANIFEST.json').stat().st_mode)==0o444, 'SOURCE manifest full0444 required')
    outputs['build/source_preparation/PREPARATION_MANIFEST.json']=prep_raw
    pins=load(bind('current_preparation_family_v2/STATIC_INPUT_BINDINGS.json','fixed_input_contract'))
    require(pins['schema']=='PR46_FIXED_CURRENT_SOURCE_INPUTS_v1' and pins['status']=='SOURCE_ONLY_ROOT_PREREQUISITES_PENDING', 'SOURCE-only fixed input status required')
    require(git('branch','--show-current').strip()==b'main','Stay on main')
    for row in pins['superseded_v1_closed_source_rows']:
        checked(row,'dated_superseded_V1_source_mistaken_chronology_attribution_only')
    original_preparation_raw=checked(pins['original_preparation_manifest'],'original_scoped_preparation_manifest')
    original_preparation=load(original_preparation_raw)
    require(original_preparation['schema']=='pr46-original-preparation-self-only-manifest/v1'
      and original_preparation['self_excluded']==['ORIGINAL_PREPARATION_MANIFEST.json']
      and original_preparation['files_count']==318 and len(original_preparation['files'])==318, 'Original scoped318+self required')
    owned={r['path'] for r in original_preparation['files']}
    require(owned=={r['path'] for r in pins['original_preparation_members']}, 'Exact original preparation rows required')
    actual_owned=set(original_preparation['authorship_root_files'])
    for root in original_preparation['authorship_directory_roots']:
        actual_owned|={root+'/'+name for name in inventory(audit/root)}
    require(actual_owned==owned,'Scoped original authorship changed; sibling audit efforts excluded')
    for row in pins['original_preparation_members']:
        body=checked(row,'original_scoped_first_party_preparation')
        require(stat.S_IMODE((audit/row['path']).stat().st_mode)==0o444,'Original preparation full0444 changed')
        outputs['original_preparation_archive/'+row['path']]=body
    outputs['original_preparation_archive/ORIGINAL_PREPARATION_MANIFEST.json']=original_preparation_raw
    for row in pins['original_separate_closure_capture']:
        outputs['original_preparation_archive/'+row['path']]=checked(row,'separately_completed_original_closure_capture')
    for row in pins['genuine_closed_ROOT_evidence_fixed_rows']:
        outputs['root_fixed_evidence_archive/'+row['path']]=checked(row,'genuine_completed_first_party_ROOT_evidence')
    snapshot_raw=checked(pins['snapshot_manifest'],'original13_snapshot'); snapshot=load(snapshot_raw)
    require(snapshot['schema']=='pr46-original-source-snapshot/v1' and snapshot['head']==HEAD
      and snapshot['github_base']==BASE and snapshot['merge_base']==MERGE_BASE
      and snapshot['original_files']==13 and len(snapshot['files'])==13,'Exact original13 snapshot required')
    original={}
    for row in snapshot['files']:
        name=relative(row['relative_path']); native='unsolved_math_prioritization/attempts/30004438/'+name
        require(name not in original and type(row['bytes']) is int and row['bytes']>=0 and hex64(row['sha256'])
          and row['git_mode']=='100644' and row['snapshot_mode']=='0444' and row['path']==native
          and type(row['git_object']) is str and re.fullmatch('[0-9a-f]{40}',row['git_object']), 'Exact original Git body required')
        raw=bind('source_snapshot/'+name,'immutable_original13',row['sha256'])
        require(len(raw)==row['bytes'] and stat.S_IMODE((audit/'source_snapshot'/name).stat().st_mode)==0o444,'Original full bytes/mode changed')
        require(git('show',HEAD+':'+native)==raw and git('ls-tree',HEAD,'--',native).decode().strip()
          =='100644 blob '+row['git_object']+'\t'+native,'Original Git body/blob/mode differs')
        original[name]=raw
    require(inventory(audit/'source_snapshot')==set(original) and sha(original['SOURCE_STATUS.md'])==SCIENCE,'Complete original science required')
    tree=git('ls-tree','-r','-z',HEAD,'--','unsolved_math_prioritization/attempts/30004438/').decode().split('\0')
    require({entry.split('\t',1)[1] for entry in tree if entry}=={'unsolved_math_prioritization/attempts/30004438/'+n for n in original},'Complete original Git tree required')
    metadata=load(checked(pins['original_metadata'],'original_PR_metadata'))
    require(metadata['head']==HEAD and metadata['github_base']==BASE and metadata['merge_base']==MERGE_BASE
      and metadata['changed_files']==14 and git('rev-parse',BASE)==(BASE+'\n').encode(),'Original identities differ')
    diff=checked(metadata['full_diff'],'whole_original14_path_diff')
    require(len(diff)==89103 and sha(diff)=='944d6ac424b3e6fa6d4ccf163e6b381352072589528a3a5a29b146454e458209'
      and git('diff','--no-ext-diff','--no-textconv','--binary',MERGE_BASE,HEAD,'--')==diff
      and git('diff','--name-only',MERGE_BASE,HEAD).decode().splitlines()==[r['path'] for r in metadata['all_changed_paths']], 'Whole original14-path diff required')
    ledger=load(original['turns.json']); saved=load(original['verification.json']); independent=load(original['independent_review/independent_results.json'])
    require(type(ledger) is dict and ledger['problem_id']==30004438 and type(ledger['substantive_turns_used']) is int
      and ledger['substantive_turns_used']==0 and type(ledger['source_verification_responses']) is int
      and ledger['source_verification_responses']==1 and type(ledger['turn_limit']) is int and ledger['turn_limit']==5
      and ledger['outcome']=='known_result_source_correction' and ledger['recommended_status']=='already_solved','Original object ledger0/5 + one source response required')
    for receipt,count in [(saved,51),(independent,848)]:
        require(type(receipt['passed']) is int and receipt['passed']==count and type(receipt['failed']) is int
          and receipt['failed']==0 and type(receipt['checks']) is dict and len(receipt['checks'])==count
          and all(value=='PASS' for value in receipt['checks'].values()),'Complete literal saved receipt required; ROOT replay separate')
    source=load(original['source_record.json'])
    require(type(source) is dict and type(source['id']) is int and source['id']==30004438
      and source['problem_number']=='OWR-17475-003' and 'problem' not in source,'Plain raw original source object required')
    family_pins={}
    for family, info in pins['families'].items():
        require(family in {'projective_algebra_family','complex_dynamics_family'},'Exact independent family identities required')
        member_names=rows(info['members']); separate_names=rows(info['separate_excluded_closure'])
        manifest_name=relative(info['manifest']['path'])
        require(not member_names.intersection(separate_names) and inventory(audit/family)==member_names|separate_names|{manifest_name},'Exact family topology required')
        actual_dirs={p.relative_to(audit/family).as_posix() for p in (audit/family).rglob('*') if p.is_dir()}
        require(actual_dirs==set(info['directories'])==set(info['directory_modes'])
          and all(stat.S_IMODE((audit/family/n).stat().st_mode)==mode for n,mode in info['directory_modes'].items()),'Exact independent family directory topology/modes required')
        manifest_raw=checked(dict(info['manifest'],path=family+'/'+manifest_name),'independent_family_self_manifest')
        manifest=load(manifest_raw); family_pins[family]=sha(manifest_raw)
        require({r['path'] for r in manifest['files']}==member_names and manifest['files_count']==len(member_names),'Exact family closed member rows required')
        require(manifest['self_excluded']==info['manifest_self_excluded'],'Preserve exact dated family exclusions')
        outputs['family_evidence/'+family+'/'+manifest_name]=manifest_raw
        for row in info['members']+info['separate_excluded_closure']:
            body=checked(dict(row,path=family+'/'+row['path']),'independent_authored_member' if row['path'] in member_names else 'separate_completed_family_closure_capture')
            require(stat.S_IMODE((audit/family/row['path']).stat().st_mode)==0o444,'Independent family full0444 required')
            outputs['family_evidence/'+family+'/'+row['path']]=body
    require(set(family_pins)=={'projective_algebra_family','complex_dynamics_family'},'Both independent families required')
    algebra=load(bind('projective_algebra_family/verdict.json','algebra_full_known_result_determination'))
    complex_manifest=load(bind('complex_dynamics_family/COMPLEX_DYNAMICS_MANIFEST.json','complex_full_known_result_determination'))
    complex_report=bind('complex_dynamics_family/COMPLEX_DYNAMICS_AUDIT.md','complete_complex_audit_report').decode()
    require(algebra['verdict']=='PASS_MATHEMATICAL_EXACT_TARGET_KNOWN_RESULT'
      and algebra['recommended_research_disposition']=='already_solved' and algebra['candidate_comparison']['mandatory_mathematical_corrections']==[]
      and algebra['mathematical_gap_remaining'] is None and algebra['acceptance_approval'] is None
      and complex_manifest['mathematical_claim_verified'] is True and complex_manifest['acceptance_verdict'] is None
      and 'Exact mathematical claim verified. No mandatory correction' in complex_report,'Closed mathematical reports confer no acceptance')

    future={}
    for name,option in [('ROOT_CURRENT_KNOWN_RESULT_SCOPE_CERTIFICATE.md','root_scope_certificate_sha256'),
      ('ROOT_PRIMARY_READ_LEDGER.json','root_read_ledger_sha256'),('ROOT_SCIENCE_CARD.json','root_science_card_sha256'),
      ('ROOT_CURRENT_INPUT_PREIMAGES.json','root_current_input_manifest_sha256'),('ROOT_EVIDENCE_BINDINGS.json','root_evidence_bindings_sha256')]:
        future[name]=bind(name,'genuine_separate_ROOT_prerequisite',getattr(args,option))
    evidence=load(future['ROOT_EVIDENCE_BINDINGS.json'])
    require(set(evidence)=={'schema','approved_by_root','created_utc','notes','manifest','proof_notes','summary','raw_audit','source_adversary','operative_preparation_directory'}
      and evidence['operative_preparation_directory']=='current_preparation_family_v2' and evidence['schema']=='PR46_ROOT_EVIDENCE_BINDINGS_v1' and evidence['approved_by_root'] is True
      and type(evidence['notes']) is str and len(evidence['notes'].strip())>=40
      and clock(prep['utc'])<=clock(evidence['created_utc'])<=dt.datetime.now(dt.timezone.utc),'Genuine actual ROOT evidence required; drafts rejected')
    require(evidence['manifest']['path']=='root_original_actual_reproduction_v2/MANIFEST.json'
      and evidence['proof_notes']['path']=='ROOT_MATHEMATICAL_REVIEW.md'
      and evidence['summary']['path']=='root_original_actual_reproduction_v2/ROOT_CURRENT_REPRODUCTION_SUMMARY.json'
      and evidence['raw_audit']['path']=='ROOT_COMPLETE_RAW_SQL_AUDIT.json','Exact ROOT evidence anchors required')
    reproduction_raw=checked(evidence['manifest'],'genuine_ROOT_reproduction_manifest'); reproduction=load(reproduction_raw)
    require(reproduction['schema']=='pr46-root-complete-reproduction-self-only-closure/v1'
      and reproduction['self_excluded']==['MANIFEST.json'] and type(reproduction['files_count']) is int
      and reproduction['files_count']==len(reproduction['files'])==37
      and reproduction['future_acceptance_approved'] is False and reproduction['foreign_primary_raw_SQL_cache_bodies_copied'] is False,'Genuine ROOT self-only reproduction required')
    reproduction_rows=[]
    for row in reproduction['files']:
        require(type(row) is dict and set(row)=={'path','bytes','sha256','full_mode'} and row['full_mode']=='0444','Exact ROOT full0444 row required')
        reproduction_rows.append({k:row[k] for k in ['path','bytes','sha256']})
    actual_names=rows(reproduction_rows)
    require(inventory(audit/'root_original_actual_reproduction_v2')==actual_names|{'MANIFEST.json'},'ROOT evidence closure topology changed')
    outputs['root_evidence/root_original_actual_reproduction_v2/MANIFEST.json']=reproduction_raw
    for row in reproduction_rows:
        require(stat.S_IMODE((audit/'root_original_actual_reproduction_v2'/row['path']).stat().st_mode)==0o444,'Actual ROOT evidence full0444 changed')
        outputs['root_evidence/root_original_actual_reproduction_v2/'+row['path']]=checked(dict(row,path='root_original_actual_reproduction_v2/'+row['path']),'complete_genuine_ROOT_reproduction_member')
    summary=load(checked(evidence['summary'],'ROOT_entire_actual_reproduction_summary'))
    require(summary['schema']=='pr46-root-current-complete-reproduction-summary/v1'
      and summary['status']=='PASS_ROOT_COMPLETED_FIRST_PARTY_REPRODUCTION'
      and equal(summary['entire_author_result'],saved) and equal(summary['entire_historical_independent_result'],independent)
      and equal(summary['complete_original_turns'],ledger) and summary['future_acceptance_approved'] is False
      and summary['source_record_schema']=='plain_raw_problem_object' and summary['source_record_wrapper_claimed'] is False
      and summary['selected_prior_key_present'] is False and equal(summary['selected_prior_fallback'],{})
      and summary['historical_failure_preserved'] is True and summary['foreign_primary_SQL_raw_cache_body_copy'] is False,'Complete actual ROOT results/ledger required')
    require(bind('root_original_actual_reproduction_v2/author/verification.json','actual_ROOT_author_receipt')==original['verification.json']
      and bind('root_original_actual_reproduction_v2/historical_independent/independent_results.json','actual_ROOT_independent_receipt')==original['independent_review/independent_results.json'],'Actual complete ROOT receipts byte-exact required')
    for key,number in [('original_substantive_attempts',0),('source_verification_responses',1),('new_substantive_attempts',0),('audit_turns',0)]:
        require(type(summary[key]) is int and summary[key]==number,'Typed actual ROOT accounting required')
    require(type(summary['complete_helper_captures']) is list and len(summary['complete_helper_captures'])==2,'Exactly both genuine unchanged helper captures required')
    for cap in summary['complete_helper_captures']:
        require(cap['schema']=='pr46-root-unchanged-helper-actual-capture/v1' and cap['actual_execution'] is True
          and cap['completed'] is True and type(cap['pid']) is int and cap['pid']>0 and type(cap['exit_code']) is int
          and cap['exit_code']==0 and cap['stdin_supplied'] is False and cap['source_unchanged'] is True
          and cap['operator_pid']==62514 and cap['cwd']==str(repo)
          and clock(cap['started_utc'])<=clock(cap['finished_utc'])<=dt.datetime.now(dt.timezone.utc),'Genuine complete ROOT helper child capture required')
        for key in ['source','copied_source','stdout','stderr']:
            row=dict(cap[key]); anchor=audit.relative_to(repo).as_posix()+'/'
            require(row['path'].startswith(anchor),'Exact repository-anchored ROOT reference required')
            row['path']=row['path'][len(anchor):]; checked(row,'genuine_actual_ROOT_helper_'+key)
    raw_audit=load(checked(evidence['raw_audit'],'ROOT_complete_inplace_raw_SQL_audit'))
    require(raw_audit['schema']=='pr46-root-in-place-complete-raw-sql-audit/v1'
      and raw_audit['status']=='PASS_FULL_RAW_PRIOR_SQL_AND_ORIGINAL_PLAIN_SOURCE'
      and type(raw_audit['full_raw_and_prior_bytes']) is int and raw_audit['full_raw_and_prior_bytes']==149266659
      and type(raw_audit['all_SQL_rows']) is int and raw_audit['all_SQL_rows']==15458
      and len(raw_audit['complete_row_bindings'])==15458 and raw_audit['complete_saved_source_equals_raw_selected'] is True
      and raw_audit['selected_prior_key_present'] is False and equal(raw_audit['selected_prior_fallback'],{})
      and raw_audit['raw_null_present'] is False and raw_audit['raw_or_SQL_or_foreign_source_bodies_copied'] is False
      and equal(raw_audit['original_native_selected_read']['complete_selected_problem'],source)
      and equal(raw_audit['original_native_selected_read']['complete_selected_prior_report'],{}),'Actual raw prior absence distinguished from null and saved{}')
    outputs['root_evidence/ROOT_COMPLETE_RAW_SQL_AUDIT.json']=bind(evidence['raw_audit']['path'],'literal_ROOT_raw_audit')
    notes=checked(evidence['proof_notes'],'ROOT_completed_full_mathematical_and_source_review')
    require(notes.decode().strip() and not notes.decode().lstrip().startswith('# DRAFT'),'Actual ROOT mathematical review required')
    outputs['root_evidence/ROOT_MATHEMATICAL_REVIEW.md']=notes
    adversary_record_raw=checked(evidence['source_adversary'],'ROOT_separate_actual_new_source_adversary_record')
    adversary_record=load(adversary_record_raw)
    require(adversary_record['schema']=='PR46_ROOT_NEW_SOURCE_ADVERSARY_RECORD_v1'
      and adversary_record['approved_by_root'] is True and adversary_record['complete_report_personally_read'] is True
      and adversary_record['new_different_source_adversary'] is True and adversary_record['closed_clean'] is True
      and adversary_record['mandatory_corrections']==[] and adversary_record['preparation_manifest_sha256']==sha(prep_raw)
      and adversary_record['builder_sha256']==sha(regular(script))
      and adversary_record['operator_sha256']==sha(regular(script.parent/'capture_root_builder_operation.py'))
      and clock(prep['utc'])<=clock(adversary_record['created_utc'])<=dt.datetime.now(dt.timezone.utc),'New SOURCE adversary approval never inherited from old reports')
    source_adversary_manifest_raw=checked(adversary_record['manifest'],'new_SOURCE_adversary_closed_manifest')
    source_adversary_manifest=load(source_adversary_manifest_raw)
    source_adversary_root=PurePosixPath(adversary_record['manifest']['path']).parent.as_posix()
    source_adversary_self=PurePosixPath(adversary_record['manifest']['path']).name
    require(source_adversary_manifest['self_excluded']==[source_adversary_self]
      and type(source_adversary_manifest['files_count']) is int
      and source_adversary_manifest['files_count']==len(source_adversary_manifest['files']),'New SOURCE adversary must be truly self-only closed')
    new_member_rows=[]
    for row in source_adversary_manifest['files']:
        require(type(row) is dict and set(row) in ({'path','bytes','sha256'},{'path','bytes','sha256','full_mode'}),'Typed new reviewer member required')
        if 'full_mode' in row: require(row['full_mode'] in ('0444',0o444),'New reviewer member full0444 required')
        new_member_rows.append({k:row[k] for k in ['path','bytes','sha256']})
    require(inventory(audit/source_adversary_root)==rows(new_member_rows)|{source_adversary_self},'Exact new reviewer own topology required')
    require(equal(adversary_record['members'],[dict(row,path=source_adversary_root+'/'+row['path']) for row in new_member_rows]),'ROOT standalone reviewer member list must equal real closure')
    checked(adversary_record['report'],'new_SOURCE_adversary_complete_report')
    require(adversary_record['report']['path'] in {r['path'] for r in adversary_record['members']},'Complete new report must belong to closed reviewer')
    outputs['new_source_adversary_evidence/'+adversary_record['manifest']['path']]=source_adversary_manifest_raw
    for row in adversary_record['members']:
        body=checked(row,'individual_new_SOURCE_adversary_closed_dependency')
        require(stat.S_IMODE((audit/row['path']).stat().st_mode)==0o444,'New source reviewer full0444 required')
        outputs['new_source_adversary_evidence/'+row['path']]=body
    outputs['root_approval/ROOT_NEW_SOURCE_ADVERSARY_RECORD.json']=adversary_record_raw
    certificate=future['ROOT_CURRENT_KNOWN_RESULT_SCOPE_CERTIFICATE.md'].decode()
    require(certificate.splitlines()[0]=='# ROOT PR46 exact known-result acceptance'
      and certificate.splitlines().count('ROOT_SCOPE_ACCEPTED_EXACT_KNOWN_RESULT_ONLY')==1 and 'DRAFT' not in certificate,'Actual ROOT known-result certificate required')
    for literal in ['PR46 / 30004438 / OWR-17475-003',HEAD,BASE,'Status: already_solved',
      'Original turns: 0/5; source-verification responses: 1; new: 0; audit: 0','Full exact target verified: true',
      'Novelty: false','Khazhgali Kozhasov','Mario Kummer','2020 preprint','NEW whole-current review: PENDING','Paper/new DOI/tracker: false']:
        require(literal in certificate,'Missing literal actual ROOT scope: '+literal)
    reading=load(future['ROOT_PRIMARY_READ_LEDGER.json']); science=load(future['ROOT_SCIENCE_CARD.json'])
    qualification=bind('current_preparation_family_v2/SOURCE_PRECISION_QUALIFICATIONS.md','global_current_qualification')
    for obj,schema in [(reading,'PR46_ROOT_PRIMARY_READ_LEDGER_v1'),(science,'PR46_ROOT_SCIENCE_CARD_v1')]:
        require(obj['operative_preparation_directory']=='current_preparation_family_v2' and obj['schema']==schema and obj['reading_completed'] is True and equal(obj['root_flags'],{flag:True for flag in FLAGS})
          and type(obj['reading_notes']) is str and len(obj['reading_notes'].strip())>=40
          and clock(prep['utc'])<=clock(obj['created_utc'])<=dt.datetime.now(dt.timezone.utc),'Completed actual ROOT full reading required')
        require(obj['scope_certificate_sha256']==args.root_scope_certificate_sha256 and obj['preparation_manifest_sha256']==sha(prep_raw)
          and obj['source_qualification_sha256']==sha(qualification) and obj['evidence_bindings_sha256']==args.root_evidence_bindings_sha256
          and equal(obj['family_manifest_sha256'],family_pins),'ROOT actual evidence pins differ')
        for key,number in [('original_substantive_attempts',0),('original_source_verification_responses',1),('new_substantive_attempts',0),('audit_turns',0)]:
            require(type(obj[key]) is int and obj[key]==number,'Typed source-only accounting required')
    require(science['status']=='already_solved' and science['exact_known_target_verified'] is True and science['full_problem_solved'] is True
      and science['full_target_prior_result_verified'] is True and science['project_solved'] is False
      and science['novelty_claimed'] is False and type(science['turn_limit']) is int and science['turn_limit']==5
      and science['existing_result_credit']==['Khazhgali Kozhasov','Mario Kummer'] and science['source_publication_kind']=='preprint'
      and all(science[k] is False for k in ['paper_created','new_DOI_created','tracker_row_created'])
      and science['read_ledger_sha256']==args.root_read_ledger_sha256 and science['current_input_manifest_sha256']==args.root_current_input_manifest_sha256
      and science['new_whole_current_gate']=='PENDING' and all(science[k] is None for k in ['current_model','current_reasoning_effort','current_deadline_utc','current_verdict']), 'Only exact credited known-result acceptance with unknown current runtime')
    current=load(future['ROOT_CURRENT_INPUT_PREIMAGES.json'])
    require(set(current)=={'schema','approved_by_root','created_utc','reason','current_head','files','operative_preparation_directory'}
      and current['operative_preparation_directory']=='current_preparation_family_v2' and current['schema']=='PR46_ROOT_FRESH13_INPUT_PREIMAGES_v1' and current['approved_by_root'] is True
      and type(current['reason']) is str and len(current['reason'].strip())>=40
      and clock(prep['utc'])<=clock(current['created_utc'])<=dt.datetime.now(dt.timezone.utc)
      and type(current['current_head']) is str and re.fullmatch('[0-9a-f]{40}',current['current_head'])
      and type(current['files']) is list and len(current['files'])==13,'Genuine ROOT fresh13/currentHEAD authority required')
    native_rows=[]
    for row in current['files']:
        require(type(row) is dict and set(row)=={'path','bytes','sha256','full_mode'}
          and type(row['full_mode']) is int and 0<=row['full_mode']<0o10000,'Exact typed full native mode required')
        native_rows.append({k:row[k] for k in ['path','bytes','sha256']})
    require(rows(native_rows)==NATIVE,'Exactly all13 native paths required')
    def validate_native():
        require(git('branch','--show-current').strip()==b'main' and git('rev-parse','HEAD').decode().strip()==current['current_head'],'Approved actual main HEAD changed')
        for row in current['files']:
            path=repo/row['path']; body=regular(path)
            require(len(body)==row['bytes'] and sha(body)==row['sha256'] and stat.S_IMODE(path.stat().st_mode)==row['full_mode'],'Actual native bytes/full modes changed')
            structured(row['path'],body)
    validate_native()
    # Complete first-party procedural Git stdout of native4 is allowed; no raw cache bodies are copied.
    native4=['unsolved_math_prioritization/QUEUE.md','unsolved_math_prioritization/state.json',
      'unsolved_math_prioritization/history.jsonl','draft_pr_publication_program_20260930/inventory.json']
    for native in native4:
        require(git('show',current['current_head']+':'+native)==regular(repo/native),'Dated native4 committed body differs from approved current live bytes')
        git('ls-tree',current['current_head'],'--',native)
    outer_name=relative(os.environ.get('PR46_ROOT_OUTER_CAPTURE',''))
    require(re.fullmatch(r'tmp/root_pr46_current_v2_outer_[0-9]{8}T[0-9]{6}\.[0-9]{6}Z',outer_name),'Genuine outer prelaunch required')
    outer_raw=bind(outer_name+'/OPERATION_PRELAUNCH.json','actual_ROOT_outer_prelaunch'); outer=load(outer_raw)
    require(outer['schema']=='PR46_ROOT_BUILDER_PRELAUNCH_v2' and type(outer['operator_pid']) is int and outer['operator_pid']==os.getppid()
      and outer['builder_sha256']==sha(regular(script)) and outer['operator_sha256']==sha(regular(script.parent/'capture_root_builder_operation.py'))
      and outer['argv']==['/usr/bin/python3','-B',str(script),*sys.argv[1:]] and outer['cwd']==str(repo)
      and clock(outer['started_utc'])<=dt.datetime.now(dt.timezone.utc),'Actual outer parent/source/argv/cwd differ')
    for name,expected in [('PRELAUNCH_BUILDER_SOURCE.py',outer['builder_sha256']),('PRELAUNCH_OPERATOR.py',outer['operator_sha256'])]:
        outputs['build/root_outer_prelaunch/'+name]=bind(outer_name+'/'+name,'actual_prelaunch_source',expected)
    outputs['build/root_outer_prelaunch/OPERATION_PRELAUNCH.json']=outer_raw
    outputs['CURRENT_EXECUTION_REFERENCE.json']=encode({'audit_relative_outer_capture':outer_name,'outer_parent_pid':os.getppid(),
      'audit_relative_inner_attempt':attempt.relative_to(audit).as_posix(),'actual_builder_pid':os.getpid(),
      'outer_prelaunch_sha256':sha(outer_raw),'complete_outer_capture_written_only_after_child_exit':True,
      'final_inner_GIT_COMMANDS_written_incrementally_by_builder_before_exit':True,
      'frozen_inner_command_copy_is_prepublication_prefix':True,
      'outer_operator_does_not_write_inner_GIT_COMMANDS':True,
      'ROOT_final_original_inner_commands_inspection_required_AFTER_child_exit':True,'ROOT_must_read_final_actual_outer_and_inner_at_original_paths':True,
      'already_complete_outer_receipt_or_whole_PASS_certified':False})
    queue=regular(repo/'unsolved_math_prioritization/QUEUE.md'); lines=queue.splitlines(keepends=True)
    require(sum(line.startswith(b'|') and [v.strip() for v in line.decode().split('|')[1:-1]]==HEADER for line in lines)==1,'Unique named queue header required')
    hits=[(line,line.decode().split('|')) for line in lines if line.startswith(b'|') and len(line.decode().split('|'))==len(HEADER)+2
      and line.decode().split('|')[2].strip()=='30004438 / OWR-17475-003']
    require(len(hits)==1,'Exact unique target queue row required'); before,fields=hits[0]
    indexes={name:HEADER.index(name)+1 for name in HEADER}
    require(fields[indexes['Status']].strip()=='queued' and fields[indexes['Turns']].strip()=='0/5','Expected queued0/5 preimage required')
    finding='Credited existing Kozhasov-Kummer2020 preprint result: every d>=2 admits a nonempty ordinary real-open subset of full ambient dimension2d+1 with every complex projective periodic point real at all periods. Original0/5; one source-verification response; new0; audit0. No discovery/journal/paper/new DOI/tracker claim. NEW whole-current review PENDING.'
    after_fields=list(fields)
    for name,value in [('Status','already_solved'),('Turns','0/5'),('Findings',finding)]: after_fields[indexes[name]]=' '+value+' '
    allowed={indexes[name] for name in ['Status','Turns','Findings']}
    require(all(left==right for index,(left,right) in enumerate(zip(fields,after_fields)) if index not in allowed),'Other target columns/Chat/DOI must remain byte-exact')
    after='|'.join(after_fields).encode(); prospective=b''.join(after if line==before else line for line in lines)
    notice=b'Historical literal body follows. Model/reasoning/deadline, access/PDF hashes, review PASS and publication-state prose are dated attributions. Read SOURCE_PRECISION_QUALIFICATIONS.md with every presentation. NEW whole-current review PENDING.\n\n'
    overview=bind('current_preparation_family_v2/CURRENT_OVERVIEW.md','current_overview')
    outputs.update({'original_archive/'+name:body for name,body in original.items()})
    outputs.update({name:original[name] for name in IMMUTABLE})
    outputs.update({'README.md':overview+b'\n'+qualification,'PR_DRAFT.md':overview+b'\n'+qualification,
      'pr_body.md':overview+b'\n'+qualification,'CURRENT_CONTEXT.md':overview+b'\n'+qualification,
      'CURRENT_SOURCE_STATUS_CONTEXT.md':qualification+b'\n'+notice+original['SOURCE_STATUS.md'],
      'independent_review/REVIEW.md':qualification+b'\n'+notice+original['independent_review/REVIEW.md'],
      'SOURCE_PRECISION_QUALIFICATIONS.md':qualification,'HISTORICAL_ORIGINAL_NOTICE.md':notice,
      'original_snapshot_manifest.json':snapshot_raw,'original_diff.patch':diff,
      'queue_proposal/QUEUE_PREIMAGE.md':queue,'queue_proposal/QUEUE_PROSPECTIVE.md':prospective})
    for native in native4:
        body=regular(repo/native)
        label=native.replace('/','__')
        outputs['native4_proposal/preimage/'+label]=body
        outputs['native4_proposal/prospective/'+label]=prospective if native.endswith('/QUEUE.md') else body
    outputs['native4_proposal/PROPOSAL_SCOPE.json']=encode({'phase':'PENDING_NATIVE_ACCEPTANCE_LOCAL_PROPOSAL_ONLY',
      'QUEUE_named_changes':['Status','Turns','Findings'],'selected_id':30004438,'state_history_inventory_prospective':'UNCHANGED_BYTE_EXACT',
      'native_acceptance_requires_later_ROOT_saved_full_plan_and_fresh13_currentHEAD':True,'prior_native_state_or_history_rewritten':False})
    outputs.update({'root_approval/'+name:body for name,body in future.items()})
    common={'id':30004438,'problem_number':'OWR-17475-003','status':'already_solved','exact_known_target_verified_by_ROOT':True,
      'full_problem_solved':True,'full_target_prior_result_verified':True,'project_solved':False,'campaign_new_discovery':False,'novelty_claimed':False,
      'existing_result_credit':['Khazhgali Kozhasov','Mario Kummer'],'source_publication_kind':'2020 preprint',
      'current_model':None,'current_reasoning_effort':None,'current_deadline_utc':None,'current_verdict':None,
      'current_gate':GATE,'original_substantive_attempts':0,'original_source_verification_responses':1,
      'substantive_attempt_limit':5,'new_substantive_attempts':0,'audit_turns':0,
      'historical_runtime_certified':False,'historical_verdict_transferred':False,'human_peer_review_claimed':False,
      'formal_certification_claimed':False,'paper_created':False,'new_DOI_created':False,'tracker_row_created':False,
      'global_qualification':'SOURCE_PRECISION_QUALIFICATIONS.md','exact_mathematical_gap_remaining':None,
      'exact_remaining_publication_gap':'NEW whole-current source-first adversary and ROOT final reconciliation/integration',
      'journal_publication_certified':False,'fresh_PDF_bytes_or_pixels_authenticated':False}
    for name in ['status.json','readiness.json','independent_review/verdict.json','independent_review/review_summary.json']:
        outputs[name]=encode(common)
    outputs['CURRENT_QUEUE_PATCH.json']=encode({'phase':'Local prospective proposal only; no native write','id':30004438,
      'allowed_named_changes':['Status','Turns','Findings'],'whole_preimage_sha256':sha(queue),
      'whole_prospective_sha256':sha(prospective),'row_before':before.decode(),'row_prospective':after.decode(),
      'all_other_rows_and_columns_Chat_DOI_byte_preserved':True})
    outputs['CURRENT_PRECISION_RECEIPT.json']=encode({'original13_archive_byte_exact':True,'original_object_ledger_preserved':True,
      'plain_raw_source_record_preserved':True,'actual_ROOT_entire_author51_and_independent848_receipts_exact':True,
      'finite_controls_do_not_prove_all_degree_all_period_scope':True,'historical_PDF_hashes_are_attribution_only':True,
      'fresh_primary_operative_text_reading_does_not_authenticate_legacy_PDF_hashes_or_pixels':True,
      'global_ordinary_real_open_full_ambient_all_period_RP1_credit_qualifications':True,
      'native13_actual_live_checked_before_after_native4_dated_full_Git_stdout_copied':True,
      'native4_frozen_past_never_approves_future_merge':True,'foreign_raw_SQLite_cache_PDF_OCR_pixels_headers_cookies_never_copied':True,
      'source_and_current_whole_reviews_are_different_gates':True,'NEW_whole_current_gate':'PENDING'})
    outputs['RESEARCH_LOG.md']=(utc()+' — Actual administrative freeze; publication workflow75%; known-target source audit accepted by genuine ROOT reading; new-discovery credit0%. Status already_solved; original0/5, source responses1, new0, audit0. NEW whole-current review PENDING. No paper/new DOI/tracker.\n').encode()
    def validate_dependencies():
        for row in dependencies.values():
            body=regular(audit/row['path'])
            require(len(body)==row['bytes'] and sha(body)==row['sha256'],'Dependency changed')
    validate_dependencies(); validate_native()
    require(regular(repo/'unsolved_math_prioritization/QUEUE.md')==queue,'Queue changed before staging')
    outputs['CURRENT_DEPENDENCIES.json']=encode({'anchor_repository_relative':audit.relative_to(repo).as_posix(),
      'resolution':'repository_root / anchor_repository_relative / files.path; never scratch',
      'files':sorted(dependencies.values(),key=lambda row:row['path']),'current_native13':current['files'],
      'current_main_head':current['current_head'],'native4_dated_Git_stdout_is_first_party_procedural_evidence':True,
      'stable9_live_required_by_later_whole_review':True,'fresh13_new_authority_required_again_before_final_acceptance':True,
      'foreign_original_PDF_hashes_are_attributed_unautheticated_records_only':True})
    trees=[]
    for previous in sorted((audit/'tmp').glob('root_pr46_current_v2_build_*')):
        require(previous.is_dir() and not previous.is_symlink(),'Regular retained actual attempt required')
        previous_files=[]; previous_dirs=[]
        for path in sorted(previous.rglob('*')):
            require(not path.is_symlink(),'Retained attempt symlink rejected'); name=relative(path.relative_to(previous).as_posix())
            if stat.S_ISREG(path.stat().st_mode):
                body=regular(path); previous_files.append({'path':name,'bytes':len(body),'sha256':sha(body)})
                if previous==attempt: outputs['build/actual_attempt_prepublication_prefix/'+name]=body
            else: require(path.is_dir(),'Retained special member rejected'); previous_dirs.append(name)
        trees.append({'audit_relative_directory':previous.relative_to(audit).as_posix(),'files':previous_files,
          'directories':previous_dirs,'all_original_members_preserved_at_original_audit_path':True,
          'current_attempt_listing_is_prepublication_prefix':previous==attempt,'positive_packet_claimed':False})
    outputs['build/RETAINED_ACTUAL_ATTEMPT_TREES.json']=encode(trees)
    stage=attempt/'stage'; stage.mkdir(exist_ok=False)
    for name,body in sorted(outputs.items()):
        path=stage/relative(name); path.parent.mkdir(parents=True,exist_ok=True)
        # Never reinterpret arbitrary original .json failure streams as valid JSON.
        with path.open('xb') as handle: handle.write(body); handle.flush(); os.fsync(handle.fileno())
        path.chmod(0o444)
    require(inventory(stage/'original_archive')==set(original),'Complete exact original13 archive required')
    for name,body in original.items(): require(regular(stage/'original_archive'/name)==body,'Original archive bytes changed')
    for name in IMMUTABLE: require(regular(stage/name)==original[name],'Immutable science/code/source/results/ledger changed')
    members=[{'path':name,'bytes':len(regular(stage/name)),'sha256':sha(regular(stage/name))} for name in sorted(inventory(stage))]
    manifest={'schema':'PR46_STRICT_CURRENT_PACKET_v1','self_excluded':['MANIFEST.json'],'files_count':len(members),'files':members,
      'current_gate':GATE,'status':'already_solved','full_problem_solved':True,'campaign_new_discovery':False,'novelty_claimed':False,
      'original_substantive_attempts':0,'original_source_verification_responses':1,'new_substantive_attempts':0,'audit_turns':0,'full_permission_mode':'0444'}
    with (stage/'MANIFEST.json').open('xb') as handle: handle.write(encode(manifest)); handle.flush(); os.fsync(handle.fileno())
    (stage/'MANIFEST.json').chmod(0o444)
    require(inventory(stage)=={r['path'] for r in members}|{'MANIFEST.json'},'Exact self-only packet closure required')
    for row in members:
        path=stage/row['path']; body=regular(path)
        require(len(body)==row['bytes'] and sha(body)==row['sha256'] and stat.S_IMODE(path.stat().st_mode)==0o444,'Staged full bytes/full0444 changed')
    require(stat.S_IMODE((stage/'MANIFEST.json').stat().st_mode)==0o444,'Manifest full0444 required')
    validate_dependencies(); validate_native()
    require(regular(repo/'unsolved_math_prioritization/QUEUE.md')==queue,'Queue changed after staging')
    require(not destination.exists() and not destination.is_symlink(),'Candidate appeared; retain stage')
    publish_absent(stage,destination)
    print(json.dumps({'status':'ACTUAL_CURRENT_FREEZE_NEW_WHOLE_GATE_PENDING','destination':str(destination),
      'manifest_sha256':sha(regular(destination/'MANIFEST.json')),'full_problem_solved':True,'campaign_new_discovery':False,
      'original_attempts':'0/5','source_verification_responses':1,'new_attempts':0,'audit_turns':0,'native_writes':0,'current_whole_verdict':None},indent=2))


def main():
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument('--execute',action='store_true')
    for name in ['root-scope-certificate','root-read-ledger','root-science-card','root-current-input-manifest','root-evidence-bindings']:
        parser.add_argument('--'+name+'-sha256',required=True)
    args=parser.parse_args()
    require(args.execute and all(hex64(v) for k,v in vars(args).items() if k.endswith('sha256')),'Explicit ROOT execution/five actual prerequisite SHA pins required')
    require(not sys.flags.optimize and os.environ.get('PYTHONOPTIMIZE','') in ('','0'),'No optimization may suppress guards')
    script=Path(__file__).absolute(); regular(script)
    require(script.parent.name=='current_preparation_family_v2' and script.parent.parent.name=='pr46_30004438','Exact PR46 anchor required')
    audit=script.parent.parent; repo=audit.parents[2]
    require(repo==Path('/Users/alec/Documents/Math'),'Exact repository root required')
    (audit/'tmp').mkdir(exist_ok=True); require(not (audit/'tmp').is_symlink(),'Regular audit-local tmp required')
    attempt=audit/'tmp'/('root_pr46_current_v2_build_'+dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ'))
    attempt.mkdir(exist_ok=False); (attempt/'PRELAUNCH_BUILDER_SOURCE.py').write_bytes(regular(script))
    (attempt/'INVOCATION.json').write_bytes(encode({'argv':sys.argv,'cwd':str(Path.cwd()),'pid':os.getpid(),
      'parent_pid':os.getppid(),'utc':utc(),'source_sha256':sha(regular(script)),'administrative_only':True}))
    try: build(args,script,audit,repo,attempt)
    except BaseException:
        error=traceback.format_exc(); (attempt/'BUILD_FAILURE.json').write_bytes(encode({'utc':utc(),
          'status':'FAILED_ACTUAL_BUILD_PRESERVED','traceback':error,'current_positive_verdict':False}))
        print(error,file=sys.stderr); raise
if __name__=='__main__': main()
