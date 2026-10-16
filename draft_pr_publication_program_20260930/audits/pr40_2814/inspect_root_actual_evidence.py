#!/usr/bin/env python3
"""Independent root inspection of exact original and actual PR40 evidence.

No candidate research/helper execution. Writes only the new root inspection.
"""
import datetime as dt
import hashlib
import json
from pathlib import Path, PurePosixPath

A=Path(__file__).resolve().parent
SHA=lambda b:hashlib.sha256(b).hexdigest()

def need(value, message):
    if not value: raise ValueError(message)

def object_pairs(items):
    result={}
    for key,value in items:
        need(key not in result,'Duplicate JSON key '+key);result[key]=value
    return result

def parse(data): return json.loads(data,object_pairs_hook=object_pairs)

def data(path):
    need(path.is_file() and not path.is_symlink(),'Nonregular input')
    need(all(not p.is_symlink() for p in path.parents),'Symlink ancestor')
    return path.read_bytes()

def pin(path):
    raw=data(path);return {'path':path.relative_to(A).as_posix(),'size':len(raw),'sha256':SHA(raw)}

def check_row(root,row):
    n=row['path'];p=PurePosixPath(n)
    need(type(n) is str and n and not p.is_absolute() and '..' not in p.parts and p.as_posix()==n,'Unsafe row path')
    size=row['size'] if 'size' in row else row['bytes'];need(type(size) is int and size>=0,'Exact integer size required')
    raw=data(root/n);need(len(raw)==size and SHA(raw)==row['sha256'],'Full row byte mismatch '+n);return raw

def closure(root,self_name,rows,exclude=()):
    seen=set();json_count=0
    for row in rows:
        n=row['path'];need(n not in seen and n!=self_name,'Duplicate or root-self row');seen.add(n)
        raw=check_row(root,row)
        if n.endswith('.json'):parse(raw);json_count+=1
    actual=set()
    for p in root.rglob('*'):
        n=p.relative_to(root).as_posix()
        if PurePosixPath(n).parts[0] in exclude:continue
        need(not p.is_symlink(),'Symlink in authored closure')
        if p.is_file():actual.add(n)
        else:need(p.is_dir(),'Special file')
    need(actual==seen|{self_name},'Exact authored closure mismatch')
    return {'members':len(seen),'full_JSON_members_parsed':json_count}

def main():
    snapshot=parse(data(A/'snapshot_manifest.json'))
    need(SHA(data(A/'snapshot_manifest.json'))=='781f7df1f6a2e3d8e5041b555097f1765a44c1e2080c034971fd802d65e332d5','Exact source snapshot')
    need(snapshot['head']=='163e34d566d6cbaee3a2a8fdc6394fbb9e49a539' and snapshot['pr']==40 and snapshot['problem']=='2814','Exact original identity')
    need(len(snapshot['files'])==13 and len(snapshot['changed_paths'])==14,'Original13/14')
    for row in snapshot['files']:
        raw=check_row(A/'source_snapshot',row)
        need(row['mode']=='100644' and hashlib.sha1(('blob '+str(len(raw))+'\0').encode()+raw).hexdigest()==row['git_blob'],'Original mode/blob')
    need({p.relative_to(A/'source_snapshot').as_posix() for p in (A/'source_snapshot').rglob('*') if p.is_file()}=={r['path'] for r in snapshot['files']},'Original exact closure')
    diff=data(A/'pr_input/diff.patch');need(len(diff)==snapshot['diff_bytes']==67441 and SHA(diff)==snapshot['diff_sha256'],'Full14-path diff')
    primary_raw=data(A/'primary_scope_family/FIRST_PARTY_MANIFEST.json');primary=parse(primary_raw)
    need(SHA(primary_raw)=='adaa4da7629209ddba020851c54e4a2098147983c26acb7f2dbbfc159dda5d42','Exact primary family')
    primary_counts=closure(A/'primary_scope_family','FIRST_PARTY_MANIFEST.json',primary['files'],('foreign_cache','ignored_tmp'))
    geometry_raw=data(A/'geodesic_geometry_family/ARTIFACT_MANIFEST.json');geometry=parse(geometry_raw)
    need(SHA(geometry_raw)=='120735e12d3ed8673a918d114f4a01300ba6b1ab5a8b09a290659d1e61aafc75','Exact geometry family')
    geometry_counts=closure(A/'geodesic_geometry_family','ARTIFACT_MANIFEST.json',geometry['members'],('primary',))
    need(primary_counts['members']==97 and geometry_counts['members']==38,'All135 authored family members')
    foreign=parse(data(A/'geodesic_geometry_family/FOREIGN_PRIMARY_INVENTORY.json'))
    for row in foreign['members']:check_row(A/'geodesic_geometry_family',row)
    need(len(foreign['members'])==17,'Exact17 geometry foreign objects')
    original_capture=parse(data(A/'root_original_actual_capture/CAPTURE.json'))
    need(original_capture['status']=='PASS' and type(original_capture['returncode']) is int and original_capture['returncode']==0 and original_capture['attempted'] is True,'Actual original run')
    need(original_capture['program']['sha256']==SHA(data(A/'primary_scope_family/audit_original.py')),'Original actual source remains exact')
    original_streams={name:check_row(A/'root_original_actual_capture',original_capture[name]) for name in ('stdout','stderr')}
    need(not original_streams['stderr'],'Original actual stderr empty')
    result=parse(data(A/'root_original_actual_capture/results/RESULT.json'))
    need(result['status']=='PASS' and result['raw_corpus']['sql_open_mode']=='ro','Original actual report/SQLmode')
    need(parse(original_streams['stdout'])=={'status':'PASS','checks':5,'original_files':13,'sql_rows':15458,'negative_controls':5},'Whole original actual stdout')
    need(result['raw_corpus']['size']+result['raw_corpus']['reports_size']==149266659 and result['raw_corpus']['sql_rows_all_verified']==15458,'Full actual corpus/SQL counts')
    need(len(result['actual_budget_negative_controls'])==5 and all(r['rejected'] is True for r in result['actual_budget_negative_controls']),'Five actual budget controls')
    selected=parse(data(A/'root_original_actual_capture/results/SELECTED_COMPLETE_SOURCE_PAIRS.json'))
    need(len(selected)==2,'Complete selected pair count')
    for row,n,p in zip(selected,('source_record.json','duplicate_record.json'),('prior_report.json','duplicate_prior_report.json')):
        need(json.dumps(row['raw_problem'],sort_keys=True)==json.dumps(parse(data(A/'source_snapshot'/n)),sort_keys=True),'Full source type-sensitive equality')
        need(json.dumps(row['raw_report'],sort_keys=True)==json.dumps(parse(data(A/'source_snapshot'/p)),sort_keys=True),'Full prior type-sensitive equality')
    need(selected[0]['raw_report'] is None and selected[0]['raw_report_key_present'] is False and selected[0]['sql_fallback_report']=={},'Raw absent/null distinct fromSQLfallback')
    need(type(selected[1]['raw_report']) is dict and bool(selected[1]['raw_report']),'Complete duplicate prior present')
    family_capture=parse(data(A/'root_family_actual_capture/ROOT_ACTUAL_CAPTURE.json'))
    need(family_capture['status']=='PASS' and len(family_capture['actual_runs'])==5,'Five actual family runs')
    outputs={}
    for row in family_capture['actual_runs']:
        need(row['actual_execution'] is True and row['completed'] is True and type(row['returncode']) is int and row['returncode']==0 and type(row['pid']) is int,'Genuine actual family launch')
        source=data(A/'root_family_actual_capture'/row['label']/'prelaunch_source.py')
        need(len(source)==row['program_size'] and SHA(source)==row['program_sha256'],'Full actual prelaunch source')
        stdout=check_row(A/'root_family_actual_capture',row['stdout']);stderr=check_row(A/'root_family_actual_capture',row['stderr'])
        need(not stderr,'Clean full family stderr');outputs[row['label']]=parse(stdout)
    need(outputs['geometry_exact_controls_direct']['status']=='PASS','Exact geometric mechanism controls')
    need(outputs['geometry_manifest_controls']['status']=='PASS' and len(outputs['geometry_manifest_controls']['cases'])==12,'12 actual geometry closure controls')
    controls=parse(data(A/'root_family_actual_capture/primary_manifest_controls/RESULT.json'))
    need(len(controls['controls'])==7,'Primary7 actual closure controls')
    for row in controls['controls']:
        need(type(row['returncode']) is int and row['returncode']==row['expected_returncode'] and row['matched_expected'] is True,'Expected actual primary control outcome')
        for name,filename in [('stdout','ACTUAL_STDOUT.bin'),('stderr','ACTUAL_STDERR.bin')]:
            raw=data(A/'root_family_actual_capture/primary_manifest_controls/complete_control_streams'/row['label']/filename)
            need(len(raw)==row[name]['size'] and SHA(raw)==row[name]['sha256'],'Complete actual finite-control stream')
    refs=[]
    for folder in ('root_original_actual_capture','root_family_actual_capture'):
        for p in sorted((A/folder).rglob('*')):
            need(not p.is_symlink(),'Actual retention symlink')
            if p.is_file():
                refs.append(pin(p))
                if p.suffix=='.json':parse(data(p))
    outcome={'utc':dt.datetime.now(dt.timezone.utc).isoformat(),'status':'PASS','head':snapshot['head'],'base':snapshot['base'],
      'original_file_count':13,'changed_diff_path_count':14,'closed_authored_member_count':135,'closed_families':{'primary_scope_family':primary_counts,'geodesic_geometry_family':geometry_counts},
      'primary_manifest_sha256':SHA(primary_raw),'geometry_manifest_sha256':SHA(geometry_raw),'full_actual_capture_members':refs,
      'original_actual_capture':original_capture,'complete_original_actual_result':result,'actual_family_capture':family_capture,'complete_family_outputs':outputs,
      'root_full_actual_sources_streams_objects_checked':True,'source_statement_scope_valid':True,
      'scientific_status':'UNSOLVED_SOURCE_HOLD_VALID_PARTIAL','full_problem_solved':False,'original_substantive_attempts':0,'turn_limit':5,'new_substantive_attempts':0,'audit_turns':0,
      'limitations':'Independent full-byte/type/provenance inspection of actual finite evidence. Semantic scientific assessment is separately in ROOT_PARTIAL_SCOPE_CERTIFICATE. Geometry12 finite-fixture roots were deleted by reviewed producer; exact constructors/full outputs retained. Original helperSQLmode isro, notimmutable/query_only. No research helper executed by this inspector.'}
    target=A/'ROOT_ACTUAL_EVIDENCE_INSPECTION.json';need(not target.exists(),'Preserve earlier inspection')
    target.write_text(json.dumps(outcome,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'status':'PASS','inspection_sha256':SHA(data(target)),'original':13,'closed_authored':135,'actual_family_runs':5,'retained_capture_members':len(refs)}))

if __name__=='__main__':main()
