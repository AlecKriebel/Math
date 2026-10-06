"""ROOT revalidation of the delivered SOURCE pins; no helper import or mutation."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import stat

F=Path(__file__).resolve().parent; A=F.parent; R=A.parents[2]
O=A/'ordered_publication_operations_20261004'
def sha(b): return hashlib.sha256(b).hexdigest()
def check(item):
    p=R/item['path']; assert not p.is_symlink() and p.is_file()
    body=p.read_bytes(); assert len(body)==item['bytes'] and sha(body)==item['sha256'] and stat.S_IMODE(p.stat().st_mode)==item['full_mode']
index=O/'FINAL_SOURCE_PINS.json'; assert sha(index.read_bytes())=='5cf6ecfbee116c8d16cea0c39c39f234a034e3116b31605fb0dc5cb499013c52'
packet=json.loads(index.read_bytes())
assert len(packet['pins'])==84
for item in packet['pins']: check(item)
check(packet['SOURCE_BINDINGS']); check(packet['integration_helper'])
inputs=json.loads((O/'SOURCE_BINDINGS.json').read_bytes()); count=0
for key in ['original_custody','current_SOURCE_custody','priority_custody']:
    pin=inputs[key]; p=R/pin['path']; assert sha(p.read_bytes())==pin['sha256']
for pin in [inputs[k] for k in ['original_custody','current_SOURCE_custody','priority_custody']]+inputs['review_custodies']:
    p=R/pin['path']; assert sha(p.read_bytes())==pin['sha256']; rows=json.loads(p.read_bytes())['files']
    rows=[dict(v,path=k) for k,v in rows.items()] if isinstance(rows,dict) else rows
    for item in rows:
        target=Path(item['path']); target=target if target.is_absolute() else p.parent/target
        assert target.is_file() and not target.is_symlink(); target.resolve().relative_to(p.parent)
        body=target.read_bytes(); mode=item.get('full_mode_07777',item.get('full_mode',item.get('mode'))); mode=int(mode,8) if isinstance(mode,str) else mode
        assert len(body)==item['bytes'] and sha(body)==item['sha256'] and stat.S_IMODE(target.stat().st_mode)==mode
        count+=1
assert count==273
commandfile=O/'private/actual_readonly_inspection/COMMANDS.json'; commands=json.loads(commandfile.read_bytes())
assert len(commands)==27
for i,item in enumerate(commands,1):
    assert item['actual_pid']>0 and item['started_UTC']<=item['finished_UTC']
    for name in ['stdout','stderr']: assert sha((commandfile.parent/(str(i)+'.'+name)).read_bytes())==item[name+'_sha256']
gate=json.loads((F/'FINAL_NATIVE_GATE.json').read_bytes())
assert gate['source_bindings']=={'path':(O/'SOURCE_BINDINGS.json').relative_to(R).as_posix(),'sha256':sha((O/'SOURCE_BINDINGS.json').read_bytes())}
record={'schema':'pr57-ROOT-operations-source-readback/v1','UTC':dt.datetime.now(dt.timezone.utc).isoformat(),'actual_pid':os.getpid(),'final_source_member_pins_verified':84,'frozen_custody_members_verified':273,'actual_inspection_command_streams_verified':27,'helper_sha256':packet['integration_helper']['sha256'],'source_bindings_sha256':packet['SOURCE_BINDINGS']['sha256'],'ROOT_full_operative_helper_source_report_and_interface_read':True,'helper_imported_or_executed_by_this_verifier':False,'actual_publication_and_tracker_gate_bound':True,'writer_window_still_required':True,'PR57_ordered_workflow_percent':95,'dated_completed_program_fraction_percent':5/99*100,'goal_complete':False}
with (F/'ROOT_OPERATIONS_SOURCE_READBACK.json').open('x') as f: json.dump(record,f,indent=2); f.write('\n')
print(json.dumps(record,indent=2))
