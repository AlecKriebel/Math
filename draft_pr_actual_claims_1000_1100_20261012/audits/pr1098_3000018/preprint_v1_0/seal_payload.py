"""One-time authoring helper; regeneration after edits requires new reviews."""
from pathlib import Path
import hashlib,json,sys
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'code'))
from common import archive_bytes
def record(p):
    b=p.read_bytes()
    return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def save(name,obj):
    (ROOT/name).write_text(json.dumps(obj,sort_keys=True,indent=2)+'\n')
save('ARTIFACT_BINDINGS.json',{'paper.pdf':record(ROOT/'paper.pdf')})
exclude={'paper.pdf','pr1098_support_v1_0.zip','MANIFEST.json','DEPOSIT_BINDING.json',
 'prepare_assets.py','seal_payload.py','validate_preparation.py','PREPARATION_REPORT.md',
 'OUTPUT_PINS.json','PREPARATION_SEAL.json','RESEARCH_LOG.md'}
paths=[p for p in sorted(ROOT.rglob('*')) if p.is_file() and str(p.relative_to(ROOT)) not in exclude
       and 'validation' not in p.relative_to(ROOT).parts and '__pycache__' not in p.parts]
save('MANIFEST.json',{'schema_version':1,'entries':[{'path':str(p.relative_to(ROOT)),**record(p)} for p in paths],
 'external_artifacts':['paper.pdf','pr1098_support_v1_0.zip'],
 'hash_cycle_policy':'PDF bound inside payload; ZIP closed bytes reconstructed exactly. Outer deposit binding outside ZIP binds PDF, ZIP and native manifest.'})
(ROOT/'pr1098_support_v1_0.zip').write_bytes(archive_bytes())
save('DEPOSIT_BINDING.json',{'schema_version':1,'artifacts':{name:record(ROOT/name) for name in
 ['paper.pdf','pr1098_support_v1_0.zip','publication/zenodo-deposit.json']},
 'metadata_sha256':record(ROOT/'metadata.json')['sha256'],
 'checkpoint_date_utc':'2026-10-16','publication_ready':False,'published':False,'services_held_after_pr':1032})
print(json.dumps({'payload_members':len(paths),'pdf':record(ROOT/'paper.pdf'),'zip':record(ROOT/'pr1098_support_v1_0.zip')}))
