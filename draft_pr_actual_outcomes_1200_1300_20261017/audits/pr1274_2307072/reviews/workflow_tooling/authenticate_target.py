#!/usr/bin/env python3
"""Authenticate the real target's six-file snapshots and editorial output spans.

This checks retained bytes and declared schema, never mathematical validity or
the absent historical audit input/removed text. All guards survive -O/-OO.
"""
from pathlib import Path
import hashlib,json,re,runpy
FAMILY=Path(__file__).resolve().parent
AUDIT=FAMILY.parents[1]

def need(condition,message):
    if not condition:raise RuntimeError(message)
def sha(data):return hashlib.sha256(data).hexdigest()
def binding(path):
    data=path.read_bytes();return {'bytes':len(data),'sha256':sha(data)}
def partition(intervals,total,label):
    cursor=0
    for start,end in sorted(intervals):
        need(type(start) is int and type(end) is int and start==cursor and start<=end<=total,'Nonpartition '+label)
        cursor=end
    need(cursor==total,'Incomplete partition '+label)

def main():
    verifier=runpy.run_path(str(AUDIT/'publication/verification/verify.py'))
    snapshot=json.loads((AUDIT/'SUBMITTED_SNAPSHOT.json').read_text())
    verifier['authenticate_snapshot'](AUDIT/'submitted',snapshot)
    need(snapshot['parents']==['4b27092a448d53b61408355ce44ec38d103a1ce4'],'Original parent differs')
    for name in verifier['NAMES']:
        need((AUDIT/'submitted'/name).read_bytes()==(AUDIT/'current_edition'/name).read_bytes(),'Preserved edition drift '+name)
    editorial=json.loads((AUDIT/'submitted/EDITORIAL_MAP.json').read_text())
    need(editorial['schema']==1 and editorial['problem_id']==2307072,'Editorial target/schema differs')
    need(editorial['offset_unit']=='zero-based UTF-8 bytes; half-open intervals','Editorial units differ')
    need(editorial['removed_text_included'] is False,'Unexpected historical removed text declaration')
    need({item['artifact'] for item in editorial['artifacts']}=={'PROOF.md','AUDIT.md'} and len(editorial['artifacts'])==2,'Editorial artifacts differ')
    results=[]
    for artifact in editorial['artifacts']:
        name=artifact['artifact'];body=(AUDIT/'submitted'/name).read_bytes();record=artifact['output']
        need(record=={'path':name,**binding(AUDIT/'submitted'/name)},'Editorial output binding differs '+name)
        inputs=[];outputs=[];operations=artifact['operations'];unchanged=artifact['unchanged_ranges']
        for item in operations:
            before=(item['input_start'],item['input_end']);after=(item['output_start'],item['output_end'])
            replacement=item['replacement_utf8'].encode()
            need(item['removed_bytes']==before[1]-before[0] and re.fullmatch('[0-9a-f]{64}',item['removed_sha256']) is not None,'Malformed removed-span receipt')
            need(body[after[0]:after[1]]==replacement and sha(replacement)==item['replacement_sha256'],'Replacement output differs '+name)
            inputs.append(before);outputs.append(after)
        for item in unchanged:
            before=(item['input_start'],item['input_end']);after=(item['output_start'],item['output_end']);data=body[after[0]:after[1]]
            need(item['bytes']==before[1]-before[0]==after[1]-after[0]==len(data),'Unchanged output length differs '+name)
            need(sha(data)==item['sha256'],'Unchanged output digest differs '+name)
            inputs.append(before);outputs.append(after)
        partition(inputs,artifact['input']['bytes'],name+' input declarations')
        partition(outputs,len(body),name+' retained output')
        for item in artifact.get('protected_mathematical_regions',[]):
            data=body[item['output_start']:item['output_end']]
            need(item['byte_identical'] is True and item['bytes']==len(data)==item['input_end']-item['input_start'] and sha(data)==item['sha256'],'Protected retained output differs '+name)
        input_available=artifact['input']=={'bytes':len(body),'sha256':sha(body)}
        if artifact.get('byte_identical') is True:need(input_available and not operations,'Claimed full byte identity unsupported '+name)
        results.append({'artifact':name,'replacement_spans':len(operations),'unchanged_output_spans':len(unchanged),'protected_output_spans':len(artifact.get('protected_mathematical_regions',[])),'input_and_output_declarations_partitioned':True,'historical_input_body_reauthenticated':input_available,'output_sha256':sha(body)})
    print(json.dumps({'status':'PASS','pr':1274,'problem_id':2307072,'original_head':snapshot['head'],'original_single_parent':snapshot['parents'][0],'original_files':6,'current_files':6,'preserved_original_files_exact':True,'git_blob_sha1_fields_authenticated':6,'public_manifest_nonself_members':5,'editorial_output_checks':results,'limits':'Retained snapshots/output spans and declarations only. Absent pre-editorial AUDIT input and removed spans cannot be reauthenticated. No mathematical, priority, source-inspection, publication or actual full-package review clearance.'},sort_keys=True))
if __name__=='__main__':main()
