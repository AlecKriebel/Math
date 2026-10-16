#!/usr/bin/env python3
"""Source-only PR40 administrative packet builder; explicit root execution only.

No research-code execution/import, SQL query, subprocess, Git or shared/native
mutation. Current publication is one absent-only Darwin exclusive rename.
"""
import argparse
import ctypes
import datetime as dt
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import sys

HEAD = '163e34d566d6cbaee3a2a8fdc6394fbb9e49a539'
BASE = 'c6975ca76f9f667f1250ba403d0e6da2aafe14d0'
SCOPE = 'c8f4ff0c373073e313de3c9ead16937117134d384560dbacfb499e1333561ac4'
READ = '0a2da801b4f214435be7fea1ec55b5d47124bc6bcadcafd8b16a9d76839a1bd6'
GUARD = 'b7ddba101a11683a1aa6a5a32eee8b1d4897fc1d2f66acf1bdc5898e26935b5e'
QUAL = '27ff1255b44c35cb8ace695d80e575441c4aa9de418bb68026ec7fba9c59bd35'
NATIVE = {'unsolved_math_prioritization/'+name for name in (
    'QUEUE.md','state.json','history.jsonl','catalog.json','assessments.json',
    'queue.py','policy.json','manifest.json','cache/problems.json',
    'cache/research_results.json','cache/catalog.sqlite','review_v2/related_target_groups.json')}
NATIVE.add('draft_pr_publication_program_20260930/inventory.json')


def need(condition, message):
    if not condition: raise ValueError(message)


def sha(data): return hashlib.sha256(data).hexdigest()
def encoded(value): return (json.dumps(value,indent=2,ensure_ascii=False)+'\n').encode()


def unique(items):
    result={}
    for key,value in items:
        need(key not in result,'Duplicate JSON key '+key);result[key]=value
    return result


def parse(data):
    return json.loads(data,object_pairs_hook=unique,
        parse_constant=lambda value: (_ for _ in ()).throw(ValueError('Nonfinite JSON '+value)))


def relative(value):
    need(type(value) is str and value and '\\' not in value,'Invalid path')
    p=PurePosixPath(value)
    need(not p.is_absolute() and str(p)==value and all(c not in ('','.', '..') for c in value.split('/')),'Unsafe/noncanonical path')
    need(not {'.git','__pycache__'}.intersection(p.parts),'Unreviewed path capability')
    return value


def data(path):
    need(path.is_file() and not path.is_symlink(),'Missing/nonregular input '+str(path))
    need(all(not p.is_symlink() for p in path.parents),'Symlink ancestor')
    return path.read_bytes()


def value(obj,key,kind,expected):
    need(type(obj) is dict and key in obj and type(obj[key]) is kind and obj[key]==expected,'Required field/type/value: '+key)


def rows(items,size_key='size'):
    need(type(items) is list,'Rows must be a list');names=set()
    for row in items:
        need(type(row) is dict and {'path',size_key,'sha256'}<=set(row),'Incomplete row')
        name=relative(row['path']);need(name not in names,'Duplicate row '+name);names.add(name)
        need(type(row[size_key]) is int and row[size_key]>=0,'Size must be integer, not bool')
        need(type(row['sha256']) is str and re.fullmatch('[0-9a-f]{64}',row['sha256']) is not None,'Invalid SHA256')
    return names


def inventory(root,excluded=()):
    files,dirs=set(),set()
    need(root.is_dir() and not root.is_symlink(),'Invalid inventory root')
    for p in root.rglob('*'):
        name=p.relative_to(root).as_posix()
        if PurePosixPath(name).parts[0] in excluded: continue
        need(not p.is_symlink(),'Symlink in first-party closure '+name)
        if p.is_file(): files.add(relative(name))
        else: need(p.is_dir(),'Special member');dirs.add(relative(name))
    return files,dirs


def exclusive_publish(stage,destination):
    need(sys.platform=='darwin','Reviewed exclusive rename requires Darwin')
    rename=ctypes.CDLL(None,use_errno=True).renamex_np
    rename.argtypes=[ctypes.c_char_p,ctypes.c_char_p,ctypes.c_uint];rename.restype=ctypes.c_int
    if rename(os.fsencode(stage),os.fsencode(destination),0x00000004)!=0:
        error=ctypes.get_errno();raise OSError(error,os.strerror(error),str(destination))


def main():
    cli=argparse.ArgumentParser(description=__doc__);cli.add_argument('--execute',action='store_true')
    for label in ('root-guard','root-preimage','science-card','sql-qualification'):
        cli.add_argument('--'+label+'-json',required=True);cli.add_argument('--'+label+'-sha256',required=True)
    args=cli.parse_args();need(args.execute,'Static preparation; root must explicitly execute after source review')
    need(sys.platform=='darwin','Darwin-only reviewed publication capability')
    script=Path(__file__).resolve();A=script.parent.parent;repo=A.parents[2]
    need(script.parent.name=='current_preparation_family' and A.name=='pr40_2814','Exact owned audit anchor')
    C=A/'reviewed_candidate';need(not os.path.lexists(C),'Current destination must be absent')
    dependencies={};payloads={}

    def bind(name,expected=None,size=None):
        name=relative(name);raw=data(A/name)
        need(expected is None or sha(raw)==expected,'Input SHA drift '+name)
        need(size is None or len(raw)==size,'Input size drift '+name)
        row={'path':name,'bytes':len(raw),'sha256':sha(raw)}
        need(name not in dependencies or dependencies[name]==row,'Input changed during binding')
        dependencies[name]=row;payloads[name]=raw;return raw

    def supplied(label):
        name=getattr(args,label+'_json');digest=getattr(args,label+'_sha256')
        need(re.fullmatch('[0-9a-f]{64}',digest) is not None,'Explicit whole SHA required')
        path=Path(name)
        if path.is_absolute():name=path.relative_to(A).as_posix()
        return name,bind(name,digest)

    prep=parse(bind('current_preparation_family/PREPARATION_MANIFEST.json'))
    value(prep,'excluded',list,['PREPARATION_MANIFEST.json']);names=rows(prep['files'])
    need(inventory(script.parent)==(names|{'PREPARATION_MANIFEST.json'},set()),'Preparation exact recursive closure')
    for r in prep['files']:bind('current_preparation_family/'+r['path'],r['sha256'],r['size'])
    pins=parse(bind('current_preparation_family/INPUT_PINS.json'))
    rows(pins['fixed_inputs']);rows(pins['actual_capture_members'])
    for r in pins['fixed_inputs']:bind(r['path'],r['sha256'],r['size'])
    expected_families={'primary_scope_family':(97,'FIRST_PARTY_MANIFEST.json',['foreign_cache','ignored_tmp']),
        'geodesic_geometry_family':(38,'ARTIFACT_MANIFEST.json',['primary']),
        'root_audit_SQL_qualification_family':(5,'FIRST_PARTY_MANIFEST.json',[])}
    need(set(pins['families'])==set(expected_families),'Exact two closed families plus SQL qualification')
    for family,info in pins['families'].items():
        names=rows(info['members']);files,dirs=inventory(A/family,info['excluded_root_directories'])
        count,self_name,excluded=expected_families[family]
        need(len(names)==count and info['manifest_name']==self_name and info['excluded_root_directories']==excluded,'Family scope/exclusions differ')
        need(info['directories']==sorted(set(info['directories'])),'Unique ordered directory paths required')
        need(files==names|{info['manifest_name']} and dirs==set(info['directories']),'Exact family recursive closure '+family)
        bind(family+'/'+info['manifest_name'],info['manifest_sha256'])
        for r in info['members']:bind(family+'/'+r['path'],r['sha256'],r['size'])
    need(set(pins['capture_closures'])=={'root_original_actual_capture','root_family_actual_capture'},'Exact capture roots required')
    for folder,info in pins['capture_closures'].items():
        names=rows(info['members']);need(inventory(A/folder)==(names,set(info['directories'])),'Exact actual capture recursive closure')
        for r in info['members']:bind(folder+'/'+r['path'],r['sha256'],r['size'])
    need(set(pins['foreign_inventory'])=={'primary_scope_family/foreign_cache','geodesic_geometry_family/primary'},'Exact rooted foreign inventory prefixes')
    for prefix,info in pins['foreign_inventory'].items():
        names=rows(info['members']);need(inventory(A/prefix)==(names,set(info['directories'])),'Exact foreign inventory drift')
        for r in info['members']:
            raw=data(A/prefix/r['path']);need(len(raw)==r['size'] and sha(raw)==r['sha256'],'Foreign byte drift')
        # Foreign bytes are checked and discarded; never bind/copy them as first-party.
    guard_name,guard_raw=supplied('root_guard');need(sha(guard_raw)==GUARD,'Exact actual root inspection required');guard=parse(guard_raw)
    for k,t,v in [('status',str,'PASS'),('head',str,HEAD),('base',str,BASE),('original_file_count',int,13),('changed_diff_path_count',int,14),
        ('closed_authored_member_count',int,135),('original_substantive_attempts',int,0),('turn_limit',int,5),('new_substantive_attempts',int,0),
        ('audit_turns',int,0),('root_full_actual_sources_streams_objects_checked',bool,True),('source_statement_scope_valid',bool,True),
        ('scientific_status',str,'UNSOLVED_SOURCE_HOLD_VALID_PARTIAL'),('full_problem_solved',bool,False)]:value(guard,k,t,v)
    need(guard['full_actual_capture_members']==pins['actual_capture_members'],'Whole actual capture row bindings differ')
    qualification_name,qualification_raw=supplied('sql_qualification')
    need(sha(qualification_raw)==QUAL,'Exact adjacent qualification BINDINGS required')
    qualification=parse(qualification_raw);value(qualification,'closed_family_modified',bool,False)
    for group in ('source_and_actual_root_receipts','actual_root_complete_streams'):
        rows(qualification[group])
        for r in qualification[group]:bind(r['path'],r['sha256'],r['size'])
    qualification_checks=parse(payloads['root_audit_SQL_qualification_family/SOURCE_READ_CHECKS.json'])
    value(qualification_checks,'actual_result_value',str,'ro')
    value(qualification_checks,'immutable_option_set_by_source',bool,False)
    value(qualification_checks,'query_only_PRAGMA_set_by_source',bool,False)
    scope=bind('ROOT_PARTIAL_SCOPE_CERTIFICATE.md',SCOPE);ledger=parse(bind('ROOT_PRIMARY_READ_LEDGER.json',READ))
    for k,t,v in [('reading_completed',bool,True),('source_first_independence_claimed',bool,False),('actual_SQL_mode_of_original_helper',str,'ro'),
        ('scope_certificate_sha256',str,SCOPE),('original_substantive_attempts',int,0),('turn_limit',int,5),('new_substantive_attempts',int,0),
        ('audit_turns',int,0),('full_problem_solved_by_project',bool,False),('novelty_claimed',bool,False)]:value(ledger,k,t,v)
    preimage_name,preimage_raw=supplied('root_preimage');preimage=parse(preimage_raw)
    value(preimage,'approved_by_root',bool,True)
    need('reason' in preimage and type(preimage['reason']) is str and re.search(r'20\d\d-\d\d-\d\d',preimage['reason']),'Dated root authorization reason required')
    need('current_head' in preimage and type(preimage['current_head']) is str and re.fullmatch('[0-9a-f]{40}',preimage['current_head']),'Actual root-declared current HEAD required')
    need(rows(preimage['files'])==NATIVE and len(preimage['files'])==13,'Exactly thirteen complete native preimages')

    def native_check():
        for r in preimage['files']:
            raw=data(repo/r['path']);need(len(raw)==r['size'] and sha(raw)==r['sha256'],'Native preimage changed')
        state=parse(data(repo/'unsolved_math_prioritization/state.json'))
        need(type(state) is dict and not {'2814','20001896'}.intersection(state),'No fabricated target native state')
        history=[parse(line) for line in data(repo/'unsolved_math_prioritization/history.jsonl').splitlines() if line.strip()]
        need(all(type(e) is dict and str(e.get('id')) not in {'2814','20001896'} for e in history),'No fabricated target native event')
    native_check()
    card_name,card_raw=supplied('science_card');card=parse(card_raw)
    for k,t,v in [('status',str,'UNSOLVED'),('full_problem_solved',bool,False),('partial_valid',bool,True),('novelty_claimed',bool,False),
        ('original_substantive_attempts',int,0),('turn_limit',int,5),('new_substantive_attempts',int,0),('audit_attempts_added',int,0),
        ('current_model',type(None),None),('current_reasoning_effort',type(None),None),('current_deadline_utc',type(None),None),
        ('new_whole_current_gate',str,'PENDING'),('scope_certificate_sha256',str,SCOPE),('read_ledger_sha256',str,READ),
        ('root_actual_guard_sha256',str,GUARD)]:value(card,k,t,v)
    snapshot=parse(payloads['snapshot_manifest.json']);original={}
    rows(snapshot['files']);need(len(snapshot['files'])==13 and len(snapshot['changed_paths'])==14,'Original13/14 preserved')
    for r in snapshot['files']:
        raw=bind('source_snapshot/'+r['path'],r['sha256'],r['size']);original[r['path']]=raw
        need(r['mode']=='100644' and hashlib.sha1(('blob '+str(len(raw))+'\0').encode()+raw).hexdigest()==r['git_blob'],'Original declared mode/blob differs')
    need(inventory(A/'source_snapshot')==(set(original),{'review'}),'Exact original recursive inventory')
    turns=parse(original['turns.json'])
    need(set(turns)=={'id','substantive_attempts','count','reason'},'No hidden or extra ledger fields')
    for k,t,v in [('id',int,2814),('count',int,0),('substantive_attempts',list,[])]:value(turns,k,t,v)
    need(type(turns['reason']) is str and parse(original['prior_report.json']) is None,'Empty ledger/literal null prior')
    selected=parse(payloads['root_original_actual_capture/results/SELECTED_COMPLETE_SOURCE_PAIRS.json'])
    need(type(selected) is list and len(selected)==2,'Two full selected records')
    for r,n,p in zip(selected,('source_record.json','duplicate_record.json'),('prior_report.json','duplicate_prior_report.json')):
        need(json.dumps(r['raw_problem'],sort_keys=True)==json.dumps(parse(original[n]),sort_keys=True),'Whole source object drift')
        need(json.dumps(r['raw_report'],sort_keys=True)==json.dumps(parse(original[p]),sort_keys=True),'Whole prior object drift')
    value(selected[0],'raw_report_key_present',bool,False);value(selected[0],'raw_report',type(None),None);value(selected[0],'sql_fallback_report',dict,{})
    need(type(selected[1]['raw_report']) is dict and selected[1]['raw_report'],'Duplicate full prior preserved, same budget0')
    result=parse(payloads['root_original_actual_capture/results/RESULT.json'])
    need(json.dumps(guard['complete_original_actual_result'],sort_keys=True)==json.dumps(result,sort_keys=True),'Whole actual result differs')
    value(result['raw_corpus'],'sql_open_mode',str,'ro')
    need(result['raw_corpus']['size']+result['raw_corpus']['reports_size']==149266659 and type(result['raw_corpus']['sql_rows_all_verified']) is int and result['raw_corpus']['sql_rows_all_verified']==15458,'Actual full corpus/SQL provenance')

    now=dt.datetime.now(dt.timezone.utc).isoformat();outputs=dict(original)
    outputs.update({'original_archive/'+n:b for n,b in original.items()})
    for n,b in payloads.items():
        if n.startswith(('primary_scope_family/','geodesic_geometry_family/','root_audit_SQL_qualification_family/')):outputs['family_evidence/'+n]=b
        elif n not in {'snapshot_manifest.json','pr_input/metadata.json','pr_input/diff.patch'} and not n.startswith('source_snapshot/'):
            outputs['root_verification/'+n]=b
    for n in ('snapshot_manifest.json','pr_input/metadata.json','pr_input/diff.patch'):outputs['original_archive/'+n]=payloads[n]
    overview=(script.parent/'CURRENT_OVERVIEW_TEMPLATE.md').read_bytes()
    outputs['CURRENT_OVERVIEW.md']=overview;outputs['CURRENT_PARTIAL_SCOPE_CERTIFICATE.md']=scope
    common={k:card[k] for k in ('status','full_problem_solved','partial_valid','novelty_claimed','original_substantive_attempts','turn_limit',
        'new_substantive_attempts','audit_attempts_added','current_model','current_reasoning_effort','current_deadline_utc','new_whole_current_gate')}
    common.update(id=2814,duplicate_id=20001896,source_hold=True,original_head=HEAD,original_base=BASE,root_actual_guard_sha256=GUARD,
        root_science_card_sha256=sha(card_raw),root_current_preimage_sha256=sha(preimage_raw),root_current_head=preimage['current_head'],
        original_SOURCE_STATUS_sha256=sha(original['SOURCE_STATUS.md']),verification_attempts_added=0,current_verdict=None,
        historical_verdict_transferred=False,current_gate='pending_NEW_whole_current_packet_source_first_adversary')
    for n in ('status.json','attempt.json','current_readiness.json','acceptance.json','review/current_verdict.json'):outputs[n]=encoded(common)
    outputs['CURRENT_RESEARCH_LOG.md']=(now+' — Administrative packet frozen; preparation100%, new whole-current/integration pending. Valid source-status partial, target UNSOLVED/source hold0/5; new0/audit0. No project theorem/novelty or recursively certified external proof claimed. No shared/native/Git/remote mutation.\n').encode()
    outputs['CURRENT_PROOF_DEPENDENCIES.json']=encoded({'utc':now,'dependency_anchor_repository_relative':A.relative_to(repo).as_posix(),
        'resolution_rule':'Resolve files.path against repository_root/dependency_anchor_repository_relative; repository_preimages paths against repository_root.',
        'closed_authored_members':135,'closed_authored_members_including_two_manifests':137,'qualification_members_including_manifest':6,
        'actual_capture_members':42,'files':sorted(dependencies.values(),key=lambda r:r['path']),
        'repository_preimages':preimage['files'],'foreign_primary_inventory':pins['foreign_inventory'],
        'foreign_blobs_copied':False,'current_gate':common['current_gate']})
    outputs['CURRENT_BUILD_RECEIPT.json']=encoded({'utc':now,'actual_administrative_freeze':True,'original13_root_and_archive_bytes_exact':True,
        'SOURCE_STATUS_unchanged':True,'original_verification_program_exists':False,'generated_original_program_outputs_claimed':False,
        'root_actual_guard_sha256':GUARD,'root_science_card_sha256':sha(card_raw),'root_current_preimage_sha256':sha(preimage_raw),
        'current_head_verified_by_builder':False,'current_head_qualification':'Root-declared pinned preimage; root independently rechecks live HEAD at capture/integration.',
        'new_substantive_attempts':0,'audit_attempts_added':0,'research_helpers_executed':False,'SQL_queries_executed':False,'shared_writes':False,'new_whole_current_gate':'PENDING'})
    native_check()
    for n,r in dependencies.items():need(data(A/n)==payloads[n],'Input changed before freeze')
    stage=A/('reviewed_candidate.preparation_'+dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ'))
    stage.mkdir(exist_ok=False)
    try:
        for n,raw in sorted(outputs.items()):
            p=stage/relative(n);p.parent.mkdir(parents=True,exist_ok=True)
            with p.open('xb') as f:f.write(raw)
            p.chmod(0o444)
        files,dirs=inventory(stage)
        entries=[{'path':n,'bytes':len(data(stage/n)),'sha256':sha(data(stage/n)),'mode':'0444'} for n in sorted(files)]
        manifest={'schema':'strict_self_excluded_recursive_current_packet_v1','utc':now,'self_excluded':['MANIFEST.json'],
            'files_count':len(entries),'files':entries,'directories':sorted(dirs),'current_gate':common['current_gate']}
        with (stage/'MANIFEST.json').open('xb') as f:f.write(encoded(manifest))
        (stage/'MANIFEST.json').chmod(0o444)
        need(inventory(stage)==(files|{'MANIFEST.json'},dirs),'Current exact recursive root-self closure')
        for n in files|{'MANIFEST.json'}:need((stage/n).stat().st_mode&0o777==0o444,'Current file not444')
        for n,raw in outputs.items():need(data(stage/n)==raw,'Staged full byte drift')
        native_check()
        for n in dependencies:need(data(A/n)==payloads[n],'Input changed at publication')
        exclusive_publish(stage,C)
    except BaseException:
        # The complete stage remains. Do not delete or overwrite evidence on failure.
        raise
    print(json.dumps({'status':'CURRENT_PACKET_FROZEN_NEW_WHOLE_GATE_PENDING','destination':str(C),'members':len(entries),
        'manifest_sha256':sha(data(C/'MANIFEST.json')),'new_substantive_attempts':0,'audit_attempts_added':0,'shared_writes':False}))


if __name__=='__main__':main()
