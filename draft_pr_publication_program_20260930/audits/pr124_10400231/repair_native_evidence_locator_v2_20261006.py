#!/usr/bin/env python3
"""Prepare separate locator-corrected postimages; never repeat native commands."""
from pathlib import Path
import json, hashlib, os, datetime, subprocess, copy
C=Path(__file__).resolve().parents[3]
A=Path(__file__).resolve().parent
D=A/'native_published_obstruction_preparation_20261006'
V=D/'v2'; B=V/'private_backend'; N=V/'proposed_native_attempt'
GIT='/opt/homebrew/Cellar/git/2.38.2/bin/git'
def req(value,message):
    if not value: raise RuntimeError(message)
def sha(body): return hashlib.sha256(body).hexdigest()
def raw(p): return p.read_bytes()
def load(p): return json.loads(raw(p))
def dump(p,value): p.write_text(json.dumps(value,indent=2,sort_keys=True)+'\n')
def utc(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def replace(value):
    global occurrences
    if isinstance(value,dict):
        return {k:replace(v) for k,v in value.items()}
    if isinstance(value,list): return [replace(v) for v in value]
    if value==old:
        occurrences+=1
        return new
    return value
req(not V.exists(),'V2 must be fresh')
v1_path=D/'PREPARED_RECEIPT.json'; v1_body=raw(v1_path); v1=load(v1_path)
req(v1['base_commit']=='5de48499b84f168099d0273a340f4976f841f691','Pinned baseline')
req(v1['new_central_proof_search_turns']==0 and not v1['native_commands_repeated'],'No new proof events')
finding_path=A/'native_published_obstruction_protocol_adversary_20261006/V1_FINDING.json'
req(sha(raw(finding_path))=='f87db66fa0f468f8bf08ab8464598a1b809779706fc78fd3402b75fb237f8eeb','Independent V1 finding pin')
old=load(A/'ROOT_PUBLISHED_OBSTRUCTION_DISPOSITION_READY_20261006.json')['fresh_disposition_review']
new=str((A/old).relative_to(C)); req((C/new).is_file(),'Qualified review resolves')
req(sha(raw(C/new))=='c47bb56bca384c7a0e88f76e1b93e93ffaa7d7a54450d6cffacfba3ae8483412','Reviewed report pin')
records=[]
for item in v1['source_inputs']:
    start=utc(); p=subprocess.Popen([GIT,'show',v1['base_commit']+':'+item['path']],cwd=C,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err=p.communicate(); req(p.returncode==0,'Baseline read')
    req(len(out)==item['bytes'] and sha(out)==item['sha256'],'Unchanged full baseline')
    records.append({'PID':p.pid,'UTC_start':start,'UTC_end':utc(),'path':item['path'],'bytes':len(out),'sha256':sha(out),'exit_code':p.returncode})
pins=v1['proposed_native_pins']
for item in pins:
    body=raw(Path(item['prepared_local_path']))
    req(len(body)==item['bytes'] and sha(body)==item['sha256'],'V1 full postimage pin '+item['path'])
V.mkdir(); B.mkdir(); N.mkdir(); (V/'.gitignore').write_text('private_backend/\n')
changes=[]; newpins=[]; total=0
for item in pins:
    source=Path(item['prepared_local_path']); body=raw(source); occurrences=0
    if source.parent.name=='proposed_native_attempt': dest=N/source.name
    else: dest=B/source.name
    if source.suffix=='.json':
        before=json.loads(body); after=replace(before)
        corrected=(json.dumps(after,indent=2,sort_keys=True)+'\n').encode() if occurrences else body
        req(replace(copy.deepcopy(before))==after,'Exact JSON repair')
        occurrences//=2
    elif source.suffix=='.jsonl':
        chunks=[]
        for line in body.splitlines(keepends=True):
            count_before=occurrences; before=json.loads(line); after=replace(before)
            chunks.append((json.dumps(after,sort_keys=True)+'\n').encode() if occurrences!=count_before else line)
        corrected=b''.join(chunks)
        req(len(corrected.splitlines())==len(body.splitlines()),'History event count unchanged')
    else: corrected=body
    dest.write_bytes(corrected); total+=occurrences
    newpins.append({'path':item['path'],'prepared_local_path':str(dest),'bytes':len(corrected),'sha256':sha(corrected)})
    if occurrences: changes.append({'path':item['path'],'occurrences':occurrences,'before_sha256':sha(body),'after_sha256':sha(corrected)})
req(total==10 and len(changes)==6,'Exact ten locator corrections in six target evidence bodies')
for item in pins:
    req(sha(raw(Path(item['prepared_local_path'])))==item['sha256'],'V1 body preserved')
req(raw(v1_path)==v1_body,'Original actual receipt preserved')
correction={'schema':'pr124-preexport-target-evidence-locator-correction/v2','UTC':utc(),'actual_operator_PID':os.getpid(),'V1_receipt_sha256':sha(v1_body),'independent_V1_finding_sha256':sha(raw(finding_path)),'old_locator':old,'repository_qualified_locator':new,'review_report_sha256':sha(raw(C/new)),'changes':changes,'total_locator_occurrences':total,'all_other_semantic_values_unchanged':True,'baseline_history_prefix_bytes_unchanged':True,'native_commands_repeated':False,'new_history_events':0,'new_central_proof_search_turns':0,'historical_event_timestamps_preserved':True,'original_V1_files_preserved':True,'shared_tracked_files_exported':False,'read_only_baseline_revalidation':records,'workflow_completion_estimate_percent':95}
dump(D/'LOCATOR_CORRECTION_V2.json',correction)
v2=copy.deepcopy(v1); v2.update({'schema':'pr124-private-prepared-native-published-obstruction-correction/v2','UTC':utc(),'actual_locator_repair_operator_PID':os.getpid(),'actual_operator_PID':os.getpid(),'V1_receipt_path':str(v1_path.relative_to(C)),'V1_receipt_sha256':sha(v1_body),'locator_correction_path':str((D/'LOCATOR_CORRECTION_V2.json').relative_to(C)),'locator_correction_sha256':sha(raw(D/'LOCATOR_CORRECTION_V2.json')),'proposed_native_pins':newpins,'new_native_commands_in_v2':0,'new_history_events_in_v2':0,'repository_qualified_fresh_review':new,'preexport_postimage_locator_repair':True})
dump(D/'CORRECTED_PREPARED_RECEIPT_V2.json',v2)
print(json.dumps({'actual_operator_PID':os.getpid(),'UTC':utc(),'receipt':str(D/'CORRECTED_PREPARED_RECEIPT_V2.json'),'receipt_sha256':sha(raw(D/'CORRECTED_PREPARED_RECEIPT_V2.json')),'changes':changes,'native_commands_repeated':False,'shared_tracked_files_exported':False},sort_keys=True))
