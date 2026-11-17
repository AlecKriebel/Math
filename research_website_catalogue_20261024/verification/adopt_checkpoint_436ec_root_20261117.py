"""Authenticate the frozen native145/Fano checkpoint as inert data only."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib
import json
import stat

P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
R=P/'verification/checkpoint-native145-fanoINITIAL-20261117'
OUT=P/'verification/root-checkpoint-436ec-adoption-20261117.json'
assert not OUT.exists()
pins={'FINAL.json':(652,'55433d6be51dd2e4df839ddf683444a49344b11a674bb4eccc0231f8a5ecd24b'),
      'MANIFEST.json':(12054,'be29ecf5626dd46ebfb8a7f2125232882dc3d11c1a33d71ebe2da6b722c22726'),
      'REPORT.md':(1895,'d6ac4dd49e01c9a1ab2a30fd3ea059af7acfec2ed0afd4c1e80575601b8532ec'),
      'FINAL_CHECKS.json':(1529,'7ab8da188e35e0d3ed967336703ae01688ad08f7558d658fc8086d56528a935e')}
sha=lambda b:hashlib.sha256(b).hexdigest()
for n,v in pins.items():
 b=(R/n).read_bytes();assert (len(b),sha(b))==v,n
m=json.loads((R/'MANIFEST.json').read_bytes())
files={p.relative_to(R).as_posix() for p in R.rglob('*') if p.is_file()}
assert len(files)==m['regular_files']==54 and not any(p.is_dir() for p in R.rglob('*'))
assert stat.S_IMODE(R.stat().st_mode)==int(m['root_mode'],8)
excluded=set(m['exact_existing_terminal_recursive_hash_exclusions'])
assert excluded=={'MANIFEST.json','FINAL.json'} and not m['other_exclusions']
assert len(m['payload_files'])==52 and {r['path'] for r in m['payload_files']}|excluded==files
for r in m['payload_files']:
 p=R/r['path'];s=p.lstat();assert stat.S_ISREG(s.st_mode)
 b=p.read_bytes();assert (len(b),sha(b),stat.S_IMODE(s.st_mode))==(r['bytes'],r['SHA256'],int(r['mode'],8)),r['path']
 assert (not b)==r['empty'] and any(x.startswith('.') for x in Path(r['path']).parts)==r['hidden']
for n,mode in m['terminal_modes'].items():assert stat.S_IMODE((R/n).stat().st_mode)==int(mode,8)
c=json.loads((R/'FINAL_CHECKS.json').read_bytes());f=json.loads((R/'FINAL.json').read_bytes())
assert c['commit']==f['commit']=='436ec422f9ae291a365b9ff2814cb88bc15db8f3'
assert c['parent']==f['parent']=='bbfb7abf5c56e3f8d090e125784ff357138076fb'
assert c['tree']==f['tree']=='e8fd14aa219dd4a807215ab2b67e829ab0d61f96'
assert c['changed_paths']==146 and c['durable_closures']==72 and c['key_files']==201
assert c['all159siblings_docs_exact'] and c['native_and_public_whole_guards_equal']
runs=json.loads((R/'RUNS.json').read_bytes());assert len(runs)==6 and all(x['exit_code']==0 for x in runs)
assert [c['fano_INITIAL_physical_files'],c['fano_committed_files'],c['fano_actual_ignored_PNGs']]==[18,13,5]
assert c['scientific_and_native_reviewed']==145 and c['remaining']==58
record={'UTC':datetime.now(timezone.utc).isoformat(),'status':'ACCEPTED_SCOPED_CHECKPOINT',
        'commit':c['commit'],'parent':c['parent'],'tree':c['tree'],'packet_files':54,
        'all_payload_bytes_individual_declared_modes_terminal_controls_exact':True,
        'full_actual_FINAL_REPORT_FINAL_CHECKS_and_six_RUNS_personally_read':True,
        'all_six_runs_exit0':True,'changed_paths':146,'durable_closures':72,'keys':201,
        'all159siblings_docs_and_nativeM_W_public_unchanged_in_checkpoint':True,
        'root172_INITIAL18physical13committed5actualignored_hashbound':True,
        'root172_scientific_continuation_now_authorized':True,'scientific_and_native_reviewed':145,
        'programme_complete':False,'controls':{n:{'bytes':s,'SHA256':h} for n,(s,h) in pins.items()}}
OUT.write_text(json.dumps(record,indent=2)+'\n')
b=OUT.read_bytes();print(json.dumps({'files_authenticated':54,'bytes':len(b),'SHA256':sha(b),'path':str(OUT)}))
