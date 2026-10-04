from pathlib import Path
import datetime,hashlib,json
R=Path(__file__).resolve().parent;A=R.parent
checks=0
sha=lambda b:hashlib.sha256(b).hexdigest()
def check(v):
    global checks
    assert v;checks+=1
original=json.loads((A/'root_original_reproduction_receipt.json').read_text())
family=json.loads((A/'root_family_verification_receipt.json').read_text())
ours=json.loads((R/'FROZEN_PACKET_RECEIPT.json').read_text())
ours_files={x['path']:x for x in ours['snapshot_file_bindings']}
# Evaluate the underlying complete captures and identities, not just historical PASS fields.
check(original['check_count']==158 and len(original['checks'])==158)
check(original['binding_count']==48 and len(original['nested_bindings'])==48)
check(original['actual_author_checkpoint']==ours['author_checkpoint'] and original['author_files']==14)
for remote in original['remote_files']:
    expected=ours_files[remote['path']]
    check(remote['bytes']==expected['bytes'] and remote['sha256']==expected['sha256'] and remote['git_blob']==expected['git_blob_sha'])
for e in original['replays']:
    for stream in ['stdout','stderr']:
        data=(A/'root_original_streams'/(e['label']+'.'+stream)).read_bytes()
        check(len(data)==e[stream+'_bytes'] and sha(data)==e[stream+'_sha256'])
    check(e['exit']==0 and e['complete_output'].encode()==(A/'root_original_streams'/(e['label']+'.stdout')).read_bytes())
    check((A/'root_original_streams'/(e['label']+'.stdout')).read_bytes()==(R/'streams'/(('author_checks' if e['label']=='author' else 'historical_review')+'.stdout')).read_bytes())
check(family['check_count']==612 and len(family['checks'])==612)
check(len(family['replays'])==30 and family['full_driver_commands_independently_reexecuted']==28)
check(family['all_family_public_bindings']==34)
streams=[]
for e in family['replays']:
    for stream in ['stdout','stderr']:
        data=(A/'root_family_streams'/(e['label']+'.'+stream)).read_bytes()
        check(len(data)==e[stream+'_bytes'] and sha(data)==e[stream+'_sha256'])
    check(e['exit']==0)
    streams.append({'label':e['label'],'exit':e['exit'],'stdout_bytes':e['stdout_bytes'],'stdout_sha256':e['stdout_sha256'],'stderr_bytes':e['stderr_bytes'],'stderr_sha256':e['stderr_sha256']})
reproduction=json.loads((A/'variational_capacity_review/REPRODUCTION.json').read_text())
check(len(reproduction['commands'])==28)
for i,e in enumerate(reproduction['commands']):
    actual=(A/'root_family_streams'/('variational_capture_'+str(i)+'.stdout')).read_bytes()
    expected=(A/'variational_capacity_review'/e['stdout']['path']).read_bytes()
    check(actual==expected and sha(actual)==e['stdout']['sha256'] and len(actual)==e['stdout']['bytes'])
    check((A/'root_family_streams'/('variational_capture_'+str(i)+'.stderr')).read_bytes()==b'' and e['returncode']==0)
# CHECKS and new control claims are checked against complete JSON outputs.
new=json.loads((A/'root_family_streams/variational_capture_27.stdout').read_text())
check(new['assertions']==823 and len(new['negative_controls_rejected'])==7)
for parent_source in ['root_original_reproduction_receipt.json','root_family_verification_receipt.json','root_reproduce_frozen_packet.py','root_verify_family_evidence.py']:
    check((A/parent_source).is_file())
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS underlying whole capture identities independently inspected','assertions':checks,'root_original_receipt_check_count':158,'root_original_nested_bindings':48,'root_family_receipt_check_count':612,'root_family_complete_replays_checked':30,'variational_historical_commands_whole_compared':28,'root_source_read_in_full':['root_reproduce_frozen_packet.py','root_verify_family_evidence.py'],'root_receipt_hashes':{n:sha((A/n).read_bytes()) for n in ['root_original_reproduction_receipt.json','root_family_verification_receipt.json']},'streams':streams,'scope':'Post-independent-seal corroboration only. None of these historical PASS labels supplied the original analytical verdict or the independent live prepared gate.'}
(R/'ROOT_EVIDENCE_INSPECTION.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'assertions':checks,'whole_family_replays':30,'whole_variational_commands':28},indent=2))
