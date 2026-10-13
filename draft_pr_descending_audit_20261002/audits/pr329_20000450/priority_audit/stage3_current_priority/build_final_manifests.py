"""Own namespace manifest generator; no Git/network/source mutation."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
S=Path(__file__).resolve().parent;N=S.parent
def pin(p,base=None):
 assert not p.is_symlink()
 b=p.read_bytes();return {'path':str(p.relative_to(base)) if base else str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'mode_decimal':p.stat().st_mode&0o777}
def write(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
public=['PRIORITY_REPORT.md','MORTON_PRIOR_COMPARISON.md','VERDURE_PRIOR_COMPARISON.md','GAPS_AND_LIMITS.md','VERSION_CHRONOLOGY.md','SOURCE_INVENTORY.json','SEARCH_INVENTORY.json','READING_LEDGER.json','README_PUBLIC.md','verify_prior_parameter_comparison.py','verify_public_package.py']
if __import__('sys').argv[1:]!=['whole-only']:
 write(S/'PUBLIC_MANIFEST.json',{'schema':'pr329-public-priority-manifest-v1','generated_actual_utc':datetime.now(timezone.utc).isoformat(),'self_seal':False,'publication_authorization':False,'priority_firstness_certified':False,'payloads':[pin(S/x,S) for x in public],'export_rule':'Only these11filenames and thismanifest; no private namespace/raw sources/transcription/imported reports.'})
if __name__=='__main__' and __import__('sys').argv[1:]==['public-only']:
 print(json.dumps(pin(S/'PUBLIC_MANIFEST.json',S)));raise SystemExit(0)
ex={'stage3_current_priority/WHOLE_NAMESPACE_MANIFEST.json','stage3_current_priority/private_evidence/final_whole_replay001/stdout','stage3_current_priority/private_evidence/final_whole_replay001/stderr','stage3_current_priority/private_evidence/final_whole_replay001/receipt.json'}
external={}
for p in [N/'SOURCE_ONLY_FREEZE.json',N/'stage2_candidate_exposure/FIRST_CANDIDATE_FREEZE.json']:
 x=json.loads(p.read_text())
 for r in x.get('external_pins',x.get('authorized_external_source_pins',[])):external[r['path']]=r
index=json.loads((S/'private_evidence/original_attempt_reads/INDEX.json').read_text())
for r in index['records']:
 p=Path(r['argv'][1]);v=pin(p);assert v['sha256']==r['input_sha256'] and v['bytes']==r['input_bytes'] and v['mode_decimal']==r['input_mode'];external[str(p)]=v
for name in ['imported_report','imported_payload']:
 r=json.loads((S/'private_evidence'/name/'receipt.json').read_text());p=Path(r['argv'][1]);v=pin(p)
 assert v['sha256']==r['stdout_sha256'] and v['bytes']==r['stdout_bytes'];external[str(p)]=v
payloads=[pin(p,N) for p in sorted(N.rglob('*')) if p.is_file() and str(p.relative_to(N)) not in ex]
write(S/'WHOLE_NAMESPACE_MANIFEST.json',{'schema':'pr329-whole-priority-manifest-v1','generated_actual_utc':datetime.now(timezone.utc).isoformat(),'self_seal':False,'publication_authorization':False,'closure_authorization_received':False,'priority_firstness_certified':False,'payloads':payloads,'external_pins':list(external.values()),'excluded_exact_paths':sorted(ex),'exclusion_reason':'Self-reference and the3actualownfinalnative-replayoutput/receiptfilesonly. No genericdirectoryorfuturesealallowance.','early_freezes_preserved':['3f82ef0a12c729bf5ebebad8dcaf7622b3c0a714fc4d0d59229a5f23fc43356c','4229772cf8b5b3540dbdf2d9c13781d6109e24d1744c0a0981c6cc8f0ea07f16'],'public_manifest_pin':pin(S/'PUBLIC_MANIFEST.json',S),'status':'Held unsealed for external full reading/native replay; no publication clearance.'})
print(json.dumps({'payload_count':len(payloads),'external_count':len(external),'public_manifest':pin(S/'PUBLIC_MANIFEST.json',S),'whole_manifest':pin(S/'WHOLE_NAMESPACE_MANIFEST.json',S)},indent=2))
