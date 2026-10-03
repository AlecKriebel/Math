#!/usr/bin/env python3
"""Proposed PR41 administrative freeze. Root alone executes after source review.

No helper imports/execution, scientific search, network, Git mutation or native
write. Copied evidence is readonly; a NEW entire-current review stays pending.
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
import subprocess
import sys
import traceback

HEAD='292b95ca601f166e6d246e609cf7ed5ca5653e25'
BASE='c6975ca76f9f667f1250ba403d0e6da2aafe14d0'
SNAPSHOT='feef9bf6433c165296d3cdea883ceb74440048e17ff87f03ef636a99338cb3e6'
PROOF='464af6d259f9275ca9f0056567f5301bc228465fa0ddaf2faece0920cab6bd7c'
GATE='pending_NEW_whole_current_packet_source_first_adversary'
FLAGS=['original_mathematical_body_fully_read','operative_primary_definitions_and_target_fully_read',
       'imported_source_proof_qualifications_fully_read_and_accepted','full_raw_SQL_and_present_prior_actual_evidence_fully_read',
       'unchanged_original_helper_actual_reproductions_fully_read','both_closed_independent_families_fully_read',
       'closed_input_manifests_and_retained_evidence_exactly_checked','scoped_scientific_conclusions_accepted']
IMMUTABLE=['PROOF.md','verify.py','verification.json','source_record.json','prior_report.json','source_provenance.json','turns.json',
           'review/independent_checks.py','review/independent_results.json','review/review_summary.json']
HEADER=['Rank','ID / code','Problem','EV','Impact (/10)','Difficulty','Proposed','Status','Turns','Chat','Findings','DOI']
NATIVE={'unsolved_math_prioritization/'+x for x in ['QUEUE.md','state.json','history.jsonl','catalog.json','assessments.json','queue.py','policy.json','manifest.json','cache/problems.json','cache/research_results.json','cache/catalog.sqlite','review_v2/related_target_groups.json']}|{'draft_pr_publication_program_20260930/inventory.json'}


def require(value,message):
    if not value:raise ValueError(message)


def sha(data):return hashlib.sha256(data).hexdigest()
def encode(value):return (json.dumps(value,indent=2,ensure_ascii=False)+'\n').encode()
def canonical(value):return json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(',',':'))
def equal(a,b):return canonical(a)==canonical(b)
def hex64(value):return type(value) is str and re.fullmatch('[0-9a-f]{64}',value) is not None


def utc(value):
    require(type(value) is str and value,'Explicit ISO UTC clock required')
    parsed=dt.datetime.fromisoformat(value[:-1]+'+00:00' if value.endswith('Z') else value)
    require(parsed.tzinfo is not None and parsed.utcoffset()==dt.timedelta(0),'Aware UTC clock required')
    return parsed


def load(data):
    def pairs(items):
        value={}
        for key,item in items:
            require(key not in value,'Duplicate JSON key: '+key);value[key]=item
        return value
    def constant(value):raise ValueError('Non-JSON numeric constant: '+value)
    def floating(value):
        result=float(value);require(math.isfinite(result),'Nonfinite decoded JSON number')
        return result
    return json.loads(data,object_pairs_hook=pairs,parse_constant=constant,parse_float=floating)


def relative(value):
    require(type(value) is str and value and '\\' not in value,'Nonempty POSIX path required')
    path=PurePosixPath(value)
    require(not path.is_absolute() and path.as_posix()==value and not {'.','..','.git','__pycache__'}.intersection(path.parts),'Unsafe/noncanonical path: '+value)
    return value


def inventory(root):
    values=set();directories=set()
    require(root.is_dir() and not root.is_symlink(),'Regular root directory required')
    for path in root.rglob('*'):
        require(not path.is_symlink(),'Symlink rejected: '+str(path))
        if path.is_file():values.add(relative(path.relative_to(root).as_posix()))
        else:
            require(path.is_dir(),'Nonregular member')
            directories.add(relative(path.relative_to(root).as_posix()))
    expected={parent.as_posix() for value in values for parent in PurePosixPath(value).parents if parent.as_posix()!='.'}
    require(directories==expected,'Extra empty directory rejected: '+str(sorted(directories-expected)))
    return values


def validate_rows(rows):
    require(type(rows) is list,'Named rows must be a list');names=set()
    for row in rows:
        require(type(row) is dict and set(row)=={'path','bytes','sha256'},'Exact path/bytes/SHA row required')
        name=relative(row['path']);require(name not in names,'Duplicate path row');names.add(name)
        require(type(row['bytes']) is int and row['bytes']>=0 and hex64(row['sha256']),'Typed nonnegative bytes and lowercase SHA required')
    return names


def publish_absent(source,target):
    require(sys.platform=='darwin','Reviewed macOS exclusive rename required')
    libc=ctypes.CDLL(None,use_errno=True);call=libc.renamex_np
    call.argtypes=[ctypes.c_char_p,ctypes.c_char_p,ctypes.c_uint];call.restype=ctypes.c_int
    if call(os.fsencode(source),os.fsencode(target),4)!=0:
        number=ctypes.get_errno();raise OSError(number,os.strerror(number),str(target))


def arguments():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--execute',action='store_true')
    for name in ['root-scope-certificate','root-read-ledger','root-science-card','root-current-input-manifest']:
        parser.add_argument('--'+name+'-sha256',required=True)
    return parser.parse_args()


def execute(args,script,audit,repo,attempt):
    require(not sys.flags.optimize,'Do not disable assertions')
    destination=audit/'reviewed_candidate';require(not destination.exists() and not destination.is_symlink(),'Existing candidate must never be overwritten')
    dependencies,outputs,commands={},{},[];now=dt.datetime.now(dt.timezone.utc).isoformat()
    def bind(name,role,expected=None):
        name=relative(name);path=audit/name
        require(path.is_file() and not path.is_symlink() and all(not p.is_symlink() for p in path.parents),'Regular nonsymlink input required: '+name)
        data=path.read_bytes();row={'path':name,'bytes':len(data),'sha256':sha(data),'role':role}
        require(expected is None or row['sha256']==expected,'Approved input changed: '+name)
        if name in dependencies:
            previous=dependencies[name]
            require(all(equal(previous[key],row[key]) for key in ['path','bytes','sha256']),'Input changed during build')
            roles=previous['role'] if type(previous['role']) is list else [previous['role']]
            row['role']=sorted(set(roles+[role]))
        dependencies[name]=row;return data
    def git(*argv):
        require(argv[0] in {'branch','rev-parse','show','ls-tree','diff'},'Readonly Git only')
        require(argv[0]!='branch' or argv[1:]==('--show-current',),'Readonly branch query only')
        index=len(commands);directory=attempt/'git';directory.mkdir(exist_ok=True)
        row={'argv':['git',*argv],'cwd':str(repo),'started_utc':dt.datetime.now(dt.timezone.utc).isoformat(),
             'launch_attempted':False,'actual_execution':False,'completed':False,'exit_code':None,'stdin_supplied':False,'retention_errors':[]}
        commands.append(row);error=tb=process=None;called=False
        def retain(channel,data,available):
            path=directory/(str(index)+'.'+channel)
            try:path.write_bytes(data)
            except OSError as caught:
                row['retention_errors'].append(str(caught));path=attempt/'retention_fallback'/(str(index)+'.'+channel)
                try:path.parent.mkdir(exist_ok=True);path.write_bytes(data)
                except BaseException:
                    sys.stderr.buffer.write(data);raise
            row[channel]={'path':path.relative_to(attempt).as_posix(),'bytes':len(data),'sha256':sha(data),'available':available}
        def save():(attempt/'GIT_COMMANDS.json').write_bytes(encode(commands))
        try:
            for channel in ['stdout','stderr']:retain(channel,b'',False)
            row['stdio_kind']='prelaunch_empty_placeholder';save();require(not row['retention_errors'],'Prelaunch retention failed')
            row['launch_attempted']=True;save()
            try:
                called=True;process=subprocess.run(row['argv'],cwd=repo,stdin=subprocess.DEVNULL,capture_output=True,timeout=180,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'))
                row.update(actual_execution=True,completed=True,exit_code=process.returncode,stdio_kind='complete_child_streams');values={'stdout':process.stdout,'stderr':process.stderr}
            except subprocess.TimeoutExpired as caught:
                error,tb=caught,caught.__traceback__;row.update(actual_execution=True,stdio_kind='partial_timeout');values={'stdout':caught.stdout,'stderr':caught.stderr}
            except OSError as caught:
                error,tb=caught,caught.__traceback__;row['stdio_kind']='no_child_launched';values={'stdout':None,'stderr':None}
            for channel,value in values.items():retain(channel,value.encode() if isinstance(value,str) else value or b'',value is not None)
        except BaseException as caught:
            if not called:row['launch_attempted']=False
            if error is None:error,tb=caught,caught.__traceback__
            else:row['retention_errors'].append('Secondary retention: '+str(caught))
        finally:
            row['ended_utc']=dt.datetime.now(dt.timezone.utc).isoformat()
            if error:row['failure']={'type':type(error).__name__,'message':str(error)}
            try:save()
            except BaseException as caught:
                row['retention_errors'].append('Ledger retention: '+str(caught));print(json.dumps(row),file=sys.stderr)
                if error is None:error,tb=caught,caught.__traceback__
        if error:raise error.with_traceback(tb)
        require(not row['retention_errors'] and process.returncode==0,'Readonly Git or retention failed; actual evidence retained')
        return process.stdout

    preparation_raw=bind('current_preparation_family/PREPARATION_MANIFEST.json','closed_builder_preparation');preparation=load(preparation_raw)
    require(type(preparation) is dict and preparation['status']=='CLOSED_SOURCE_ONLY_CURRENT_PREPARATION','Closed SOURCE-ONLY preparation required')
    require(preparation['excluded']==['PREPARATION_MANIFEST.json'],'Only exact root preparation self excluded')
    prepared=[]
    for row in preparation['files']:
        require(set(row)=={'path','size','sha256'} and type(row['size']) is int and row['size']>=0 and hex64(row['sha256']),'Typed preparation row')
        name=relative(row['path']);require(name not in prepared,'Duplicate preparation path');prepared.append(name)
        raw=bind('current_preparation_family/'+name,'reviewed_proposed_source',row['sha256']);require(len(raw)==row['size'],'Preparation size changed')
        outputs['build/'+name]=raw
    require(inventory(script.parent)==set(prepared)|{'PREPARATION_MANIFEST.json'},'Exact recursive preparation closure required')
    outputs['build/PREPARATION_MANIFEST.json']=preparation_raw
    pins=load(bind('current_preparation_family/INPUT_PINS.json','exact_original_and_closed_input_contract'))
    require(pins['status']=='SOURCE_ONLY_FIXED_INPUTS_FUTURE_ROOT_PREREQUISITES_PENDING' and pins['current_or_future_root_verdict_claimed'] is False,'No preparation verdict transfer')
    for row in pins['auxiliary']:
        raw=bind(row['path'],'frozen_original_auxiliary',row['sha256']);require(len(raw)==row['bytes'],'Auxiliary size differs')
    snapshot_raw=bind('snapshot_manifest.json','exact_original16_snapshot',SNAPSHOT);snapshot=load(snapshot_raw)
    require(snapshot['head']==HEAD and snapshot['base']==BASE and len(snapshot['files'])==16 and len(snapshot['changed_paths'])==17,'Original16/17 head/base required')
    original={}
    require(git('branch','--show-current').strip()==b'main','Stay on main')
    for row in snapshot['files']:
        name=relative(row['path']);require(name not in original and type(row['size']) is int and row['size']>=0,'Unique typed original row')
        data=bind('source_snapshot/'+name,'unchanged_original16_source',row['sha256']);require(len(data)==row['size'],'Original size differs')
        target=snapshot['prefix']+name
        require(git('show',HEAD+':'+target)==data and git('ls-tree',HEAD,'--',target).decode().strip()==row['mode']+' blob '+row['git_blob']+'\t'+target,'Original native bytes/mode/blob differ')
        original[name]=data
    require(inventory(audit/'source_snapshot')==set(original) and sha(original['PROOF.md'])==PROOF,'Original complete archive/PROOF unchanged')
    diff=bind('pr_input/diff.patch','whole_original17_path_diff',pins['diff_sha256']);require(len(diff)==201709 and git('diff',BASE,HEAD)==diff and git('diff','--name-only',BASE,HEAD).decode().splitlines()==snapshot['changed_paths'],'Full original diff differs')
    problem,prior,history=[load(original[x]) for x in ['source_record.json','prior_report.json','turns.json']]
    old=load(original['attempt.json']);require(type(old['substantive_attempts_used']) is int and old['substantive_attempts_used']==2 and type(old['substantive_attempt_limit']) is int and old['substantive_attempt_limit']==5 and [x['turn'] for x in history]==[1,2],'Original local2/5 required')
    require(all(type(x['turn']) is int for x in history) and old['full_original_resolution_claimed'] is False and old['novel_result_claimed'] is False,'No new original solution/novelty')
    require(canonical(problem)==pins['whole_source_JSON'] and canonical(prior)==pins['whole_prior_JSON'] and prior,'Whole original source/PRESENT prior content and types differ')

    # Pins describe every authored and every individually bound foreign input.
    # Foreign primary bodies remain dependencies only, never copied outputs.
    require(set(pins['families'])=={'primary_scope_family','network_tail_measure_family'},'Two closed independent families required')
    for family,info in pins['families'].items():
        manifest_name=family+'/'+info['manifest']['path'];raw=bind(manifest_name,'exact_closed_family_manifest',info['manifest']['sha256'])
        require(len(raw)==info['manifest']['bytes'],'Family manifest size differs');outputs['family_evidence/'+manifest_name]=raw
        authored=validate_rows(info['members']);foreign_names=validate_rows(info['foreign_members'])
        require(not authored.intersection(foreign_names) and len(authored)==info['first_party_count'] and len(foreign_names)==info['foreign_count'],'Disjoint individually bound family classes required')
        all_rows=info['members']+info['foreign_members'];names=validate_rows(all_rows)
        require(inventory(audit/family)==names|{info['manifest']['path']},'Exact family recursive closure differs')
        for row in all_rows:
            foreign=row['path'] in foreign_names;raw=bind(family+'/'+row['path'],'foreign_primary_hash_only' if foreign else 'closed_independent_first_party',row['sha256'])
            require(len(raw)==row['bytes'],'Closed family member size differs')
            if not foreign:outputs['family_evidence/'+family+'/'+row['path']]=raw
    qualification=bind(pins['qualification']['path'],'current_ancillary_source_qualification',pins['qualification']['sha256'])

    # Both actual root closures are pinned to existing genuine complete captures.
    root_objects={}
    for label,info in pins['root_support'].items():
        prefix=info['directory'];raw=bind(prefix+'/MANIFEST.json','root_actual_exact_retention_manifest',info['manifest_sha256']);manifest=load(raw)
        require(manifest['self_excluded']==['MANIFEST.json'] and type(manifest['files_count']) is int and manifest['files_count']==info['member_count'],'Root actual manifest shape/count differs')
        require(equal(manifest['files'],info['members']),'Root actual named rows/types differ');names=validate_rows(manifest['files'])
        require(inventory(audit/prefix)==names|{'MANIFEST.json'},'Exact root support closure differs');outputs['root_verification/'+prefix+'/MANIFEST.json']=raw
        for row in manifest['files']:
            raw=bind(prefix+'/'+row['path'],'actual_root_retained_source_stream_result',row['sha256']);require(len(raw)==row['bytes'],'Root actual retained size differs')
            outputs['root_verification/'+prefix+'/'+row['path']]=raw
        root_objects[label]=load((audit/prefix/info['receipt']).read_bytes())
    for row in pins['root_sources']:
        raw=bind(row['path'],'actual_root_reproduction_source',row['sha256']);require(len(raw)==row['bytes'],'Root source size differs');outputs['root_verification/'+row['path']]=raw
    root=root_objects['original'];families=root_objects['families']
    for obj in [root,families]:
        require(obj['status']=='PASS' and type(obj['original_substantive_attempts']) is int and obj['original_substantive_attempts']==2,'Genuine original2 actual root PASS required')
        require(all(type(obj[x]) is int and obj[x]==0 for x in ['new_substantive_attempts','audit_turns']),'Typed root new0/audit0 required')
        require(len(obj['actual_outer_runs'])==3,'Three complete actual outer runs required')
        for run in obj['actual_outer_runs']:
            require(run['actual_execution'] is True and run['completed'] is True and type(run['exit_code']) is int and run['exit_code']==0 and type(run['pid']) is int and run['pid']>0,'Actual completed PID/exit0 required')
            require(run['stdin_supplied'] is False,'These approved actual producers supplied no stdin')
            require(utc(run['started_utc'])<=utc(run['finished_utc']),'Ordered actual UTC clocks required')
            require(type(run['argv']) is list and run['argv'] and all(type(x) is str and x for x in run['argv']) and type(run['cwd']) is str and run['cwd'],'Complete actual argv/cwd required')
            streams=[run[channel] for channel in ['stdout','stderr']]
            require(len(validate_rows(streams))==2,'Distinct fully retained actual channels required')
            prefix=pins['root_support']['original' if obj is root else 'families']['directory']
            for stream in streams:
                retained=bind(prefix+'/'+stream['path'],'complete_actual_root_stream',stream['sha256'])
                require(len(retained)==stream['bytes'],'Actual retained channel size differs')
    require(type(root['author_assertions']) is int and root['author_assertions']==211 and type(root['original_independent_assertions']) is int and root['original_independent_assertions']==3809,'Actual original211/3809 required')
    require(root['whole_saved_and_actual_JSON_objects_equal'] is True and root['original16_byte_unchanged'] is True and root['native13_and_main_unchanged'] is True and root['full_problem_solved'] is False,'Root scoped unchanged actual reproduction required')
    data=load((audit/'root_original_actual_reproduction/original_data/RESULT.json').read_bytes())
    require(data['status']=='PASS_READONLY_ORIGINAL_DATA' and equal(data['original16'],snapshot['files']),'Actual full original-data reproduction required')
    require(data['actual_prior_PRESENT_nonempty'] is True and data['source_prior_whole_raw_snapshot_equal'] is True,'Genuine whole PRESENT prior; no fallback')
    require(all(type(data[k]) is int and data[k]==v for k,v in [('raw_corpus_bytes',149266659),('raw_problem_count',15458),('raw_report_count',6701),('all_SQL_rows_verified',15458),('full17_path_diff_bytes',201709)]),'Fullraw/allSQL/diff counts required')
    require(data['SQL_configuration']=='mode=ro&immutable=1; PRAGMA query_only=ON verified1' and data['full_diff_sha256']==sha(diff),'Readonly SQL and exact full diff required')
    for name,count,actual_path in [('verification.json',211,'author_private/verification.json'),('review/independent_results.json',3809,'original_independent_private/review/independent_results.json')]:
        actual_raw=(audit/'root_original_actual_reproduction'/actual_path).read_bytes();actual=load(actual_raw);saved=load(original[name])
        require(actual_raw==original[name] and equal(actual,saved) and type(actual['passed']) is int and actual['passed']==count and type(actual['failed']) is int and actual['failed']==0 and len(actual['checks'])==count,'Whole actual/saved FILE bytes and JSON differ')
    require(type(families['primary_finite_checks']) is int and families['primary_finite_checks']==1326 and type(families['network_measure_checks']) is int and families['network_measure_checks']==122 and families['network_result_whole_saved_actual_equal'] is True,'Genuine own finite1326/122 required')
    for saved_path,actual_path in pins['family_result_pairs']:
        require(equal(load((audit/saved_path).read_bytes()),load((audit/actual_path).read_bytes())),'Whole actual/saved independent result differs')

    # Future root-authored prerequisites: no draft/null/false truth flags accepted.
    fixed={'root_scope_certificate':'ROOT_PARTIAL_SCOPE_CERTIFICATE.md','root_read_ledger':'ROOT_PRIMARY_READ_LEDGER.json',
           'root_science_card':'ROOT_SCIENCE_CARD.json','root_current_input_manifest':'ROOT_CURRENT_INPUT_PREIMAGES.json'}
    future={key:bind(name,'genuine_root_prerequisite',getattr(args,key+'_sha256')) for key,name in fixed.items()}
    ledger,card,current=[load(future[x]) for x in ['root_read_ledger','root_science_card','root_current_input_manifest']]
    require(ledger['reading_completed'] is True and ledger['scope_certificate_sha256']==args.root_scope_certificate_sha256 and ledger['proof_qualifications_sha256']==pins['qualification']['sha256'] and ledger['actual_replay_manifest_sha256']==pins['root_support']['original']['manifest_sha256'],'Root reading chain required')
    require(all(type(ledger[k]) is int and ledger[k]==v for k,v in [('original_substantive_attempts',2),('new_substantive_attempts',0),('audit_turns',0)]),'Root reading accounting required')
    require(card['status']=='UNSOLVED' and card['partial_valid'] is True and card['full_problem_solved'] is False and card['novelty_claimed'] is False,'Genuine root scoped science required')
    require(all(type(card[k]) is int and card[k]==v for k,v in [('original_substantive_attempts',2),('turn_limit',5),('new_substantive_attempts',0),('audit_turns',0)]),'Typed science accounting required')
    require(all(card[k] is None for k in ['current_model','current_reasoning_effort','current_deadline_utc','current_verdict']) and card['new_whole_current_gate']=='PENDING','Present current nulls and NEW gate required')
    require(type(card['root_flags']) is dict and set(card['root_flags'])==set(FLAGS) and all(card['root_flags'][x] is True for x in FLAGS),'Eight genuine typed root scientific-reading flags required')
    for key,value in [('scope_certificate_sha256',args.root_scope_certificate_sha256),('read_ledger_sha256',args.root_read_ledger_sha256),('proof_qualifications_sha256',pins['qualification']['sha256']),('actual_replay_receipt_sha256',pins['root_support']['original']['receipt_sha256']),('actual_replay_manifest_sha256',pins['root_support']['original']['manifest_sha256']),('actual_family_replay_manifest_sha256',pins['root_support']['families']['manifest_sha256']),('current_input_manifest_sha256',args.root_current_input_manifest_sha256)]:
        require(hex64(card[key]) and card[key]==value,'Science card pin differs: '+key)
    require(current['approved_by_root'] is True and type(current['reason']) is str and current['reason'].strip() and type(current['current_head']) is str and re.fullmatch('[0-9a-f]{40}',current['current_head']),'Explicit fresh root current inputs required')
    require(current['reason'].strip().lower() not in {'yes','approved','pass','ok','root'},'Substantive fresh-input approval reason required')
    require(utc(current['created_utc'])<=utc(now),'Fresh input UTC may not be future dated')
    require(validate_rows(current['files'])==NATIVE and len(current['files'])==13 and equal(current['files'],root['input_preimages']),'Fresh native13 bytes must match dated actual preimages')
    def validate_native():
        for row in current['files']:
            path=repo/relative(row['path']);require(path.is_file() and not path.is_symlink() and all(not x.is_symlink() for x in path.parents),'Regular native input required')
            raw=path.read_bytes();require(len(raw)==row['bytes'] and sha(raw)==row['sha256'],'Native preimage changed; preserve attempt')
        require(git('rev-parse','HEAD').decode().strip()==current['current_head'],'Fresh explicitly approved HEAD changed')
    validate_native()
    # The dated replay HEAD is preserved; fresh HEAD may include routine audit
    # checkpoint commits. It is never silently forced equal to head_before.
    require('9700035' not in load((repo/'unsolved_math_prioritization/state.json').read_bytes()),'Fresh native target state must remain absent')
    require(not any(str(load(x)['id'])=='9700035' for x in (repo/'unsolved_math_prioritization/history.jsonl').read_bytes().splitlines() if x),'Fresh native target history must remain absent')

    queue=(repo/'unsolved_math_prioritization/QUEUE.md').read_bytes();lines=queue.splitlines(keepends=True)
    header=next(x.decode() for x in lines if x.startswith(b'| Rank |'))
    require([x.strip() for x in header.split('|')[1:-1]]==HEADER,'Exact twelve named queue columns required')
    matches=[x for x in lines if x.startswith(b'|') and len(x.decode().split('|'))==14 and x.decode().split('|')[2].strip()=='9700035 / AMR-096-0035']
    require(len(matches)==1,'Unique full queue target preimage required');before=matches[0];fields=before.decode().split('|');after_fields=list(fields)
    indexes={name:index+1 for index,name in enumerate(HEADER)}
    require(fields[indexes['Status']].strip()=='queued' and fields[indexes['Turns']].strip()=='0/5','Native queued0/5 differs from authored2/5')
    finding='Qualified SIRSN partial: interior law and full law only under t^4 P(D>t)->0; indexed target UNSOLVED. Source proof qualifications retained. NEW whole-current review PENDING; original2/5, new0.'
    for name,value in [('Status','unsolved'),('Turns','2/5'),('Findings',finding)]:after_fields[indexes[name]]=' '+value+' '
    require(all(a==b for i,(a,b) in enumerate(zip(fields,after_fields)) if i not in {indexes[x] for x in ['Status','Turns','Findings']}),'Only named Status/Turns/Findings proposal allowed')
    after='|'.join(after_fields).encode();prospective=b''.join(after if x==before else x for x in lines)

    summary=('PR41 / AMR-096-0035: full indexed target UNSOLVED; scoped partial.\n\n'
             'The span is the union of all prescribed pair routes, including exterior excursions. The unconditional interior expected-length law and full-length lower bound are valid; the full law requires the explicit additional t^4 P(D>t)->0 condition (finite fourth moment suffices). This argument does not close the expected exterior-length gap from the ordinary axioms. A full SIRSN supplies finite major-road intensity p(1); a weak SIRSN does not automatically do so. The published question permits sufficient extra assumptions; this is not a general SIRSN solution or a priority certificate.\n\n'
             'Original16, main PROOF, all code, full saved results, source/prior/provenance and two turns are exact archives. The imported prior is PRESENT and its Steiner wording is historical, corrected by current interpretation. Root actually reproduced211/3809 original checks and1326/122 family controls, and checked full149MB/all15458 SQL joins. Finite checks supplement primary analytic reading. The credited Kahn model moment import requires the exact joint-event/T_n/time-tail/slow-length qualifications appended below; it is independent of the main conditional theorem.\n\n'
             'Current NEW whole-source-first review is PENDING; all embedded historical PASS/model/reasoning/deadline labels are archival. Current model/reasoning/deadline/verdict remain present nulls. Original2/5, new0/audit0. No paper, DOI, tracker, shared/native/Git/remote mutation or outside contact.\n')
    context=('\nCURRENT_PROOF_DEPENDENCIES paths resolve against repository_root/'+audit.relative_to(repo).as_posix()+', including after canonical copying. Private scratch is never an anchor. All copied members and saved outputs are0444; old file writers need separately reviewed fresh code-only directories and new result files. Foreign primary PDF/text/render/HTML/cache bodies are individually hash-bound but not copied. The full retained root130+15 first-party closures are copied, including archival original helper inputs. A fresh whole-current source-first review is required before promotion; no old PASS transfers. The queue patch is local prospective named-column data only.\n')
    notice=b'Historical source/review text follows as an exact archival body; its prior PASS is not a current whole-packet verdict. The appended source qualifications govern current ancillary applicability.\n\n'
    outputs.update({'original_archive/'+name:raw for name,raw in original.items()});outputs.update({name:original[name] for name in IMMUTABLE})
    outputs.update({'README.md':summary.encode()+context.encode()+b'\n'+qualification,'CURRENT_CONTEXT.md':summary.encode()+context.encode(),
                    'SOURCE_AUDIT.md':summary.encode()+notice+original['SOURCE_AUDIT.md']+b'\n\n'+qualification,
                    'review/REVIEW.md':notice+original['review/REVIEW.md']+b'\n\n'+qualification,
                    'pr_body.md':summary.encode()+b'\n'+qualification,'SOURCE_PROOF_QUALIFICATIONS.md':qualification,
                    'CURRENT_AUDIT_SCOPE.md':summary.encode()+context.encode(),'HISTORICAL_ORIGINAL_NOTICE.md':notice+context.encode(),
                    'CURRENT_PARTIAL_SCOPE_CERTIFICATE.md':future['root_scope_certificate'],'primary_evidence/ROOT_PRIMARY_READ_LEDGER.json':future['root_read_ledger'],
                    'root_verification/ROOT_SCIENCE_CARD.json':future['root_science_card'],'root_verification/ROOT_CURRENT_INPUT_PREIMAGES.json':future['root_current_input_manifest'],
                    'original_diff.patch':diff,'original_pr_metadata.json':(audit/'pr_input/metadata.json').read_bytes(),'original_snapshot_manifest.json':snapshot_raw,
                    'queue_proposal/QUEUE_PREIMAGE.md':queue,'queue_proposal/QUEUE_PROSPECTIVE.md':prospective})
    common={'id':'9700035','problem_number':'AMR-096-0035','status':'unsolved_scoped_conditional_partial_pending_NEW_whole_gate','full_problem_solved':False,'novelty_claimed':False,'current_gate':GATE,'current_verdict':None,
            'current_model':None,'current_reasoning_effort':None,'current_deadline_utc':None,'original_substantive_attempts':2,'substantive_attempt_limit':5,'new_substantive_attempts':0,'audit_turns':0,
            'historical_model_reasoning_deadline_archival_only':True,'historical_verdict_transferred':False,'canonical_historical_events_inferred':False,
            'exact_remaining_gap':'Prove o(k) expected total exterior route-union length from ordinary SIRSN axioms, without assuming the sufficient fourth-order tail.'}
    for name in ['attempt.json','status.json','readiness.json','review/verdict.json']:outputs[name]=encode(common)
    outputs['CURRENT_ANCILLARY_CORRECTION_RECEIPT.json']=encode({'qualification_sha256':sha(qualification),'current_append_targets':['README.md','SOURCE_AUDIT.md','review/REVIEW.md','pr_body.md'],'exact_note_appended':True,'historical_source_audit_and_review_byte_exact_in_archive':True,'original_main_math_and_all16_unchanged':True,'source_import_repair_not_new_attempt':True,'current_gate':GATE})
    outputs['CURRENT_QUEUE_PATCH.json']=encode({'id':'9700035','phase':'Prospective named-only local proposal; no shared write','header_names':HEADER,'column_count':12,'allowed_named_changes':['Status','Turns','Findings'],'whole_preimage_sha256':sha(queue),'whole_prospective_sha256':sha(prospective),'row_before':before.decode(),'row_prospective':after.decode(),'all_unrelated_bytes_Chat_DOI_preserved':True})
    outputs['CURRENT_SOURCE_SERIALIZATION_RECEIPT.json']=encode({'whole_source_and_PRESENT_prior_types_contents_exact':True,'original_source_sha256':sha(original['source_record.json']),'original_prior_sha256':sha(original['prior_report.json']),'imported_Steiner_description_archival_only':True,'source_records_not_rewritten':True,'comparison':'type-sensitive whole JSON encoding plus independent whole-byte pins'})
    for row in dependencies.values():
        raw=(audit/row['path']).read_bytes();require(len(raw)==row['bytes'] and sha(raw)==row['sha256'],'Dependency changed before freeze')
    require((repo/'unsolved_math_prioritization/QUEUE.md').read_bytes()==queue,'Queue changed before freeze');validate_native()
    outputs['CURRENT_PROOF_DEPENDENCIES.json']=encode({'dependency_anchor_repository_relative':audit.relative_to(repo).as_posix(),'resolution_rule':'repository_root / dependency_anchor_repository_relative / files.path; never private scratch','files':sorted(dependencies.values(),key=lambda x:x['path']),'foreign_hash_dependencies_are_not_copied':True})
    outputs['CURRENT_BUILD_RECEIPT.json']=encode({'utc':now,'kind':'Actual administrative freeze; no research helper execution','original_head':HEAD,'original_base':BASE,'dated_actual_replay_head':root['head_before'],'fresh_root_approved_head':current['current_head'],'original_archive_count':16,'original_diff_path_count':17,'original_main_math_CODE_saved_receipts_source_prior_turns_BYTE_exact':True,'only_current_ancillary_presentation_qualified':True,'root_original_retained_members':130,'root_family_retained_members':15,'current_gate':GATE,'new_substantive_attempts':0,'audit_turns':0,'shared_native_Git_remote_writes':0})
    outputs['RESEARCH_LOG.md']=(now+' — administrative current freeze prepared; workflow75%, discovery0% (unconditional target UNSOLVED). Original2/5,new0/audit0. Current ancillary source presentation qualified, main math unchanged. NEW entire-current source-first review PENDING; no paper/DOI/tracker or live mutation.\n').encode()
    for name in inventory(attempt):outputs['build/actual_builder_attempt/'+name]=(attempt/name).read_bytes()
    stage=attempt/'stage';stage.mkdir(exist_ok=False)
    try:
        for name,raw in sorted(outputs.items()):
            path=stage/relative(name);path.parent.mkdir(parents=True,exist_ok=True)
            with path.open('xb') as handle:handle.write(raw)
            path.chmod(0o444)
        require(inventory(stage/'original_archive')==set(original),'Exact original archive16 required')
        for name,raw in original.items():require((stage/'original_archive'/name).read_bytes()==raw,'Archive differs')
        for name in IMMUTABLE:require((stage/name).read_bytes()==original[name],'Current immutable mathematical/source evidence differs')
        rows=[{'path':name,'bytes':len((stage/name).read_bytes()),'sha256':sha((stage/name).read_bytes()),'mode':'0444'} for name in sorted(inventory(stage))]
        manifest={'schema':'PR41_STRICT_CURRENT_PACKET_v1','self_excluded':['MANIFEST.json'],'files_count':len(rows),'files':rows,'current_gate':GATE}
        with (stage/'MANIFEST.json').open('xb') as handle:handle.write(encode(manifest))
        (stage/'MANIFEST.json').chmod(0o444);require(inventory(stage)=={x['path'] for x in rows}|{'MANIFEST.json'},'Exact self-only current closure required')
        for row in rows:
            path=stage/row['path'];raw=path.read_bytes();require(len(raw)==row['bytes'] and sha(raw)==row['sha256'] and path.stat().st_mode&0o777==0o444,'Current staged bytes/mode differ')
        require(not destination.exists() and not destination.is_symlink(),'Destination appeared; preserve stage');publish_absent(stage,destination)
    except BaseException:
        try:(stage/'BUILD_FAILURE.json').write_bytes(encode({'utc':dt.datetime.now(dt.timezone.utc).isoformat(),'traceback':traceback.format_exc(),'failed_stage_preserved':True}))
        except BaseException:print('Secondary stage failure retention failed; original error preserved',file=sys.stderr)
        raise
    print(json.dumps({'status':'CURRENT_PACKET_FROZEN_NEW_WHOLE_GATE_PENDING','destination':str(destination),'members':len(rows),'manifest_sha256':sha((destination/'MANIFEST.json').read_bytes()),'full_target':'UNSOLVED','original_attempts':'2/5','new_substantive_attempts':0,'audit_turns':0,'shared_writes':0},indent=2))


def main():
    args=arguments();require(args.execute,'Static source only; root explicit --execute required')
    require(all(hex64(v) for k,v in vars(args).items() if k.endswith('sha256')),'Explicit genuine root SHA pins required')
    script=Path(__file__).resolve();require(script.parent.name=='current_preparation_family' and script.parent.parent.name=='pr41_9700035','Exact PR41 audit anchor required')
    audit=script.parent.parent;repo=audit.parents[2];(audit/'tmp').mkdir(exist_ok=True)
    attempt=audit/'tmp'/('root_pr41_current_build_'+dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ'));attempt.mkdir(exist_ok=False)
    try:
        (attempt/'PRELAUNCH_BUILDER_SOURCE.py').write_bytes(script.read_bytes())
        (attempt/'BUILDER_INVOCATION.json').write_bytes(encode({'argv':sys.argv,'cwd':str(Path.cwd()),'source_path':script.relative_to(audit).as_posix(),'source_sha256':sha(script.read_bytes()),'created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'scratch_is_dependency_anchor':False}))
        execute(args,script,audit,repo,attempt)
    except BaseException:
        error=traceback.format_exc()
        try:(attempt/'BUILD_ATTEMPT_FAILURE.json').write_bytes(encode({'status':'FAILED_BUILD_PRESERVED','traceback':error,'new_substantive_attempts':0,'audit_turns':0}))
        except BaseException:print('Secondary attempt retention failed; original error preserved',file=sys.stderr)
        print(error,file=sys.stderr);raise


if __name__=='__main__':main()
