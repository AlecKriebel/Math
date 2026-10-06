"""Seal effective V2 metadata; never write V1."""
from pathlib import Path
import json,datetime,hashlib,os
B=Path(__file__).resolve().parent
def h(p):
 d=p.read_bytes();return {'bytes':len(d),'sha256':hashlib.sha256(d).hexdigest()}
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
validation=json.loads((B/'_private/effective_packet_validation.stdout').read_text())
assert validation['V1_immutable_verified'] and validation['effective_assertion_replacement_verified']
with (B/'RESEARCH_LOG.md').open('a') as f:
 f.write(f'- {now}: Correction checkpoint4. Read-only validator checked17 sealed V1 public files,48 V1 private custody files, existing source pins, all effective V2 assertions/JSON, and the zero-flow optional-versus-mandatory boundary check. V1 immutable history verified. Effective corrected packet sealed100%; pending parent fresh adjudication, inherited mathematical gate100%, priority0%, original2/5, extra central proof routes0.\n')
seal={'UTC':now,'operator_PID':os.getpid(),'effective_version':'corrected_v2','history':'Sealed V1 preserved immutable.','validation_receipt':{'relative_path':'_private/effective_packet_validation.stdout',**h(B/'_private/effective_packet_validation.stdout')},'validation':validation,'source_bodies':'Pinned existing V1 private source PDF/text; only relevant re-extraction in V2 private custody.','authority':'No human-referee, novelty, publication or closure authority.','manifest_rule':'PUBLIC_MANIFEST.json excludes itself; includes SEAL and PRIVATE_CUSTODY_MANIFEST. V2 private manifest also lists external immutable source/body pins separately.'}
(B/'SEAL.json').write_text(json.dumps(seal,indent=2)+'\n')
ledger=json.loads((B/'CORRECTION_LEDGER.json').read_text())
private={'UTC':now,'files':[{'private_relative_path':str(p.relative_to(B)),**h(p)} for p in sorted((B/'_private').iterdir()) if p.is_file()],'immutable_V1_relevant_source_pins':ledger['source_pins'][:2],'custody':'Raw primary extraction private; public material consists of first-party evidence and metadata.'}
(B/'PRIVATE_CUSTODY_MANIFEST.json').write_text(json.dumps(private,indent=2)+'\n')
public={'UTC':now,'effective_version':'corrected_v2','files':[{'relative_path':p.name,**h(p)} for p in sorted(B.iterdir()) if p.is_file() and p.name!='PUBLIC_MANIFEST.json'],'self_excluded':'PUBLIC_MANIFEST.json','V1_immutable_bindings':'V1_IMMUTABLE_BINDINGS.json','private_inventory':'PRIVATE_CUSTODY_MANIFEST.json'}
(B/'PUBLIC_MANIFEST.json').write_text(json.dumps(public,indent=2)+'\n')
print(json.dumps({'UTC':now,'operator_PID':os.getpid(),'effective_version':'corrected_v2','public_manifest':h(B/'PUBLIC_MANIFEST.json'),'report':h(B/'REPORT.md'),'verdict':h(B/'VERDICT.json'),'novelty_matrix':h(B/'NOVELTY_MATRIX.json'),'correction_ledger':h(B/'CORRECTION_LEDGER.json')}))
