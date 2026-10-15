#!/usr/bin/env python3
"""Read/bind all authorized sealed payloads, parse every JSON and raw run.

This is a reviewer custody check, not acceptance by delegated label.
Writes only its adjacent owned binding/interpretation record.
"""
from pathlib import Path
import datetime,hashlib,json

HERE=Path(__file__).resolve().parent
CASE=HERE.parents[1]
HEAD='3242c84e06db7e99012c7fe581adde5c3f89fc89'

def require(value,message):
    if not value:raise ValueError(message)

def bind(path):
    require(path.is_file() and not path.is_symlink(),'unsafe/missing file '+str(path))
    b=path.read_bytes()
    return {'path':str(path.relative_to(CASE)),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}

def run_records(value,label,answer):
    if isinstance(value,dict):
        if 'returncode' in value and 'stdout' in value and 'stderr' in value:
            stdout=value['stdout'];parsed=None
            if isinstance(stdout,str) and stdout.strip():
                try:parsed=json.loads(stdout)
                except json.JSONDecodeError:parsed={'not_one_JSON_value':True}
            answer.append({'input':label,'name':value.get('name',value.get('case',value.get('mutant'))),
               'returncode':value['returncode'],'optimization':value.get('inherited_PYTHONOPTIMIZE',value.get('optimized')),
               'stdout_status':parsed.get('status',parsed.get('verdict')) if isinstance(parsed,dict) else None,
               'stdout_bytes':len(stdout.encode()) if isinstance(stdout,str) else None,
               'stdout_sha256':hashlib.sha256(stdout.encode()).hexdigest() if isinstance(stdout,str) else None,
               'stderr':value['stderr'],'expected_rejection':value.get('expected_rejection'),
               'command':value.get('command'),'expected_error':value.get('expected_error_substring',value.get('expected_error'))})
        for key,item in value.items():
            if key not in ('stdout','stderr'):run_records(item,label+'/'+key,answer)
    elif isinstance(value,list):
        for i,item in enumerate(value):run_records(item,label+'/'+str(i),answer)

def main():
    rows=[];families=[];runs=[];json_fields=[]
    for folder in ['verification_repair','reviews/whole_math_adversary','reviews/geometry_scope','reviews/spectral_adversary','reviews/reproduction']:
        root=CASE/folder;seal=root/'PUBLIC_FILES.json';manifest=json.loads(seal.read_bytes())
        require(manifest['pr']==445 and str(manifest['problem_id'])=='30002737' and manifest['frozen_head']==HEAD,'identity '+folder)
        rows.append(bind(seal))
        for item in manifest['files']:
            rel=item.get('review_relative_path',item['path'])
            require(not Path(rel).is_absolute() and '..' not in Path(rel).parts,'path '+rel)
            file=root/rel;row=bind(file)
            require(row['bytes']==item['bytes'] and row['sha256']==item['sha256'],'broken seal '+str(file))
            rows.append(row)
            if file.suffix=='.json':
                value=json.loads(file.read_bytes())
                json_fields.append({'path':row['path'],'keys':list(value) if isinstance(value,dict) else None})
                run_records(value,row['path'],runs)
        result=json.loads((root/'RESULT.json').read_bytes())
        counts={k:result[k] for k in ('blocking_findings','required_repairs','central_mathematical_gaps')}
        require(all(type(v) is int for v in counts.values()),'count types '+folder)
        families.append({'folder':folder,'payloads':len(manifest['files']),**counts})
    for name in ['SOURCE_RECEIPT.json','pr_metadata.json','REPAIR_INTEGRATION.md','ROOT_MATHEMATICAL_RECONSTRUCTION.md','ROOT_SOURCE_READBACK.json','ROOT_PRIMARY_SOURCE_RECEIPT.json','ROOT_FACTOR_SOURCE_RECEIPT.json','ROOT_REPAIR_REPLAY.json']:
        path=CASE/name;rows.append(bind(path))
        if path.suffix=='.json':run_records(json.loads(path.read_bytes()),name,runs)
    initial=bind(HERE/'INITIAL_RECONSTRUCTION.md')
    require(initial['sha256']=='81ec5bf6eded3a9fc117a23bc8c5ae0b8fd1d350eb3dc8a06b948c4850d325b3','independent checkpoint changed')
    rows.append(initial)
    result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pr':445,'problem_id':30002737,'frozen_head':HEAD,
        'reviewer':'/root/pr445_whole_math_adversary2','families':families,'all_seals_match':True,
        'initial_checkpoint_unchanged':True,'all_listed_payload_bytes_loaded':True,'all_JSON_payloads_parsed':True,
        'records':rows,'raw_subprocess_interpretation':runs,'JSON_payload_keys':json_fields,
        'scope':'Integrity/structured evidence inspection only; full mathematical and code conclusions in REPORT.md'}
    (HERE/'EXPOSED_INPUT_BINDINGS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'families':families,'bound_records':len(rows),'raw_run_entries':len(runs)},indent=2))

if __name__=='__main__':main()
