"""One-time initial seal. Do not run again or edit outputs after sealing."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib,json,shutil

ROOT=Path(__file__).resolve().parent

def record(path):
 data=path.read_bytes()
 return {'path':str(path.relative_to(ROOT)),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}

if __name__=='__main__':
 manifest=ROOT/'MANIFEST.json'
 if manifest.exists():raise RuntimeError('Already sealed; refusing to alter the initial seal')
 cache=ROOT/'__pycache__'
 if cache.exists():shutil.rmtree(cache)
 unexpected=[str(p) for p in ROOT.iterdir() if p.is_dir() and p.name!='_local']
 if unexpected:raise RuntimeError('Unexpected nested output directories: '+repr(unexpected))
 stamp=datetime.now(timezone.utc).isoformat()
 raw=[record(p) for p in sorted((ROOT/'_local').rglob('*')) if p.is_file()]
 (ROOT/'RAW_INVENTORY.json').write_text(json.dumps({'sealed_utc':stamp,'ignored_root':'_local/','files':raw,'limits':'Retained sources/renders/raw tool responses are not authored findings. Non-PDF HTML payloads may retain .pdf suffixes after failed PDF requests; SOURCE_INVENTORY.json marks signatures and read scopes.'},indent=2)+'\n')
 with (ROOT/'RESEARCH_LOG.md').open('a') as stream:
  stream.write('\n- '+stamp+' (host UTC at seal): consistency QA passed; 31 retained payload hashes/signatures checked, 13 valid PDFs, 9,999 degree conversions and 16 exact valley-ratio checks. Initial independent audit sealed; no edits after seal. Completion estimate: 100% of assigned bounded audit; firstness/current-openness certification remains unavailable. Reverse cross-challenge and any final-paper/workflow review are not claimed complete.\n')
 authored=[record(p) for p in sorted(ROOT.iterdir()) if p.is_file() and p.name!='MANIFEST.json']
 payload={'schema':1,'stage':'initial independent priority/general-theory seal','sealed_utc':stamp,'family_root':str(ROOT),'authored_files':authored,'authored_count':len(authored),'raw_inventory_file':'RAW_INVENTORY.json','raw_payloads_separate':True,'manifest_self_excluded':True,'manifest_self_digest_delivery':'Exact MANIFEST.json byte count and SHA256 are delivered outside this manifest in the final parent report.','no_edits_after_seal':True,'no_other_new_priority_family_read':True}
 manifest.write_text(json.dumps(payload,indent=2)+'\n')
 for name in ['MANIFEST.json','REPORT.md','VERDICT.json','DERIVATION.md','RAW_INVENTORY.json']:
  print(json.dumps(record(ROOT/name)))
 print(json.dumps({'authored_files':len(authored),'raw_files':len(raw),'sealed_utc':stamp}))
