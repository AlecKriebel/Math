#!/usr/bin/env python3
"""One administrative raw-data freeze; never import, parse or run production code."""
from pathlib import Path
import datetime
import difflib
import hashlib
import json
import os
import stat

P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
OWN=P/'verification/gram-thompson-d4-production-prepare-v4-sol-20261117'
BASE=P/'verification/gram-thompson-d4-production-prepare-v3-sol-20261117'
PAYLOAD=['release_overlay.py','PLAN.json','SOURCE.diff','PLAN.diff','INPUT_PINS.json',
         'prepare_inert_source.py','freeze_packet.py','READ_LEDGER.json','RESEARCH_LOG.md','REPORT.md']
TERMINALS=['FINAL.json','MANIFEST.json','SEAL.json']
PINS={'release_overlay.py':(115802,'fa1d71b99d3494fe22eeca4599ee3b195fc1c6ed91d83807f86d9ade1ff2515b'),
      'PLAN.json':(14213,'26c8f9548c1d51225e806278f32023a6de43d0c6bcc2152b6e828ad6ce310caa'),
      'SOURCE.diff':(4590,'c7d13ec28c7f5d59a0c56afe26062773e1fc081869df2fca213ab86e936f3979'),
      'PLAN.diff':(2111,'81a7552d0a46b6b91bff780240dffe4876e7fbb7e5010729e138919ab306b84d')}

def need(value,reason):
    if not value:
        raise RuntimeError(reason)

def read(path):
    need(not any(p.is_symlink() for p in (path,*path.parents)),'no symbolic raw-data paths')
    first=path.stat()
    need(stat.S_ISREG(first.st_mode),'ordinary whole raw file')
    raw=path.read_bytes()
    last=path.stat()
    need((first.st_dev,first.st_ino,first.st_mode,first.st_size,first.st_mtime_ns,first.st_ctime_ns)==
         (last.st_dev,last.st_ino,last.st_mode,last.st_size,last.st_mtime_ns,last.st_ctime_ns) and len(raw)==first.st_size,'stable whole raw read')
    return raw

def pin(path):
    raw=read(path)
    return {'bytes':len(raw),'SHA256':hashlib.sha256(raw).hexdigest(),'mode':format(stat.S_IMODE(path.stat().st_mode),'04o')}

def write_new(name,value):
    raw=(json.dumps(value,indent=2,sort_keys=True)+'\n').encode()
    fd=os.open(OWN/name,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o644)
    try:
        os.fchmod(fd,0o644)
        offset=0
        while offset<len(raw):
            count=os.write(fd,raw[offset:])
            need(count>0,'complete new terminal write')
            offset+=count
        os.fsync(fd)
    finally:
        os.close(fd)

need(Path(__file__).absolute()==OWN/'freeze_packet.py','exact administrative freeze path')
need({p.name for p in OWN.iterdir()}==set(PAYLOAD),'exact ten payload files only')
for name,(size,digest) in PINS.items():
    need(pin(OWN/name)=={'bytes':size,'SHA256':digest,'mode':'0644'},'exact personally fully read artifact')
inputs=json.loads(read(OWN/'INPUT_PINS.json'))
need(inputs['before']==inputs['after'] and inputs['whole_fixed_inputs_identical'] is True,'initial complete fixed-input equality')
observed=set()
for root_name in inputs['roots']:
    root=Path(root_name)
    observed.add(str(root))
    if root.is_dir():
        observed.update(str(p) for p in root.rglob('*'))
need(observed=={row['path'] for row in inputs['after']},'same complete fixed namespaces at freeze')
for row in inputs['after']:
    path=Path(row['path'])
    info=path.stat()
    need((info.st_dev,info.st_ino,format(stat.S_IMODE(info.st_mode),'04o'),info.st_mtime_ns,info.st_ctime_ns)==
         (row['device'],row['inode'],row['mode'],row['mtime_ns'],row['ctime_ns']),'same fixed input identity/mode/times at freeze')
    if row['kind']=='file':
        need(pin(path)=={k:row[k] for k in ('bytes','SHA256','mode')},'same complete fixed file bytes at freeze')
    else:
        need(stat.S_ISDIR(info.st_mode) and row['empty']==(not any(path.iterdir())),'same ordinary fixed directory topology')
old_source=read(BASE/'release_overlay.py')
source=old_source
for row in inputs['exact_source_byte_replacements']:
    old,new=row['old'].encode(),row['new'].encode()
    need(source.count(old)==1,'exact single authorized source replacement')
    source=source.replace(old,new,1)
need(source==read(OWN/'release_overlay.py'),'all other V3 source bytes unchanged')
old_plan=read(BASE/'PLAN.json')
plan=old_plan.replace(b'production-prepare-v3-sol-20261117',b'production-prepare-v4-sol-20261117',1)
plan=plan.replace(b'"Math_remote_root_sibling_directories": 159,',b'"Math_remote_root_sibling_directories": 148,\n  "Math_remote_protected_nonprogramme_entries": 159,',1)
plan=plan.replace(b'preserve its159 sibling directory and docs tree OIDs.',b'preserve all159 protected non-programme root entries (148 directory siblings and11 root files), including the docs tree, with exact name/mode/type/OID maps.',1)
need(plan==read(OWN/'PLAN.json'),'all other V3 PLAN bytes unchanged')
for name,old,new,unit in [('SOURCE.diff',old_source,source,'release_overlay.py'),('PLAN.diff',old_plan,plan,'PLAN.json')]:
    expected=''.join(difflib.unified_diff(old.decode().splitlines(keepends=True),new.decode().splitlines(keepends=True),fromfile='V3/'+unit,tofile='V4/'+unit)).encode()
    need(expected==read(OWN/name),'complete actual V3-to-V4 raw diff')
for name in PAYLOAD:
    need(pin(OWN/name)['mode']=='0644','all inert payload modes0644')
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
final={'schema':'inert-production-source-v4-final-v1','UTC':now,'scope':str(OWN),
       'status':'SOURCE_PREPARED_PENDING_INDEPENDENT_FULL_STATIC_AND_ROOT_ACTUAL_READ',
       'completion_percent_assigned_source_preparation':100,
       'source':pin(OWN/'release_overlay.py'),'PLAN':pin(OWN/'PLAN.json'),
       'source_lines':1709,'PLAN_lines':232,'directory_siblings':148,
       'protected_nonprogramme_entries':159,'protected_root_files':11,
       'all_other_V3_source_and_PLAN_bytes_unchanged':True,'fixed_inputs_unchanged_through_freeze':True,
       'V3_all_modes_UNFIT_and_assembler_V1_one_exit1_history_preserved':True,
       'all_release_helper_modes_default_import_AST_compile_help_test':0,
       'Git_network_W_RUNTIME_ignore_global_Sheet_primary_scientific_install_deploy_contact_actions':0,
       'source_preparation_only':True,'publication_or_future_action_authority':False,
       'AA':None,'redirect':None,'follow_up':None}
write_new('FINAL.json',final)
names=sorted(PAYLOAD+TERMINALS)
manifest={'schema':'finite-inert-source-v4-manifest-v1','scope':str(OWN),'file_count':len(names),
          'child_directory_count':0,'root_mode':format(stat.S_IMODE(OWN.stat().st_mode),'04o'),
          'entries':[{'path':name,'kind':'file',**pin(OWN/name)} if name not in ('MANIFEST.json','SEAL.json') else
                     {'path':name,'kind':'file','mode':'0644','content_hash_exclusion':'Acyclic terminal; actual complete external bytes/SHA256 reported to root, not this marker.'} for name in names],
          'terminal_content_hash_exclusions_exact':['MANIFEST.json','SEAL.json'],
          'source_preparation_only':True,'publication_or_future_action_authority':False}
write_new('MANIFEST.json',manifest)
seal={'schema':'acyclic-inert-source-v4-seal-v1','scope':str(OWN),'UTC':now,
      'file_count':len(names),'child_directory_count':0,'exact_names':names,
      'FINAL':pin(OWN/'FINAL.json'),'MANIFEST':pin(OWN/'MANIFEST.json'),
      'source':pin(OWN/'release_overlay.py'),'PLAN':pin(OWN/'PLAN.json'),
      'own_actual_external_pin_reported_to_root':True,'publication_or_future_action_authority':False}
write_new('SEAL.json',seal)
need({p.name for p in OWN.iterdir()}==set(names),'exact final finite namespace')
for name in names:
    need(pin(OWN/name)['mode']=='0644','all final files ordinary0644')
fd=os.open(OWN,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
try:
    os.fsync(fd)
finally:
    os.close(fd)
print(json.dumps({'status':final['status'],'files':len(names),'child_directories':0,
                  'terminal_pins':{name:pin(OWN/name) for name in TERMINALS},
                  'source':pin(OWN/'release_overlay.py'),'PLAN':pin(OWN/'PLAN.json'),
                  'publication_or_future_action_authority':False},sort_keys=True))
