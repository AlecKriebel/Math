"""Read-only custody/consistency verification; no atlas/program rerun."""
from pathlib import Path
import hashlib,json
O=Path(__file__).resolve().parent
def load(n):return json.loads((O/n).read_text())
def bind(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return dict(bytes=p.stat().st_size,sha256=h.hexdigest())
def need(c,msg):
 if not c:raise RuntimeError(msg)
b=load('BEFORE_BINDINGS.json')['files']
for p,spec in b.items():need(bind(Path(p))==spec,'Original changed: '+p)
for entry in load('READ_LEDGER.json')['reads']:
 need(bind(Path(entry['path']))['sha256']==entry['sha256'],'Read source changed')
r=load('RECONCILIATION.json');v=load('VERDICT.json')
need(r['published_row']['raw_id']==137124,'Wrong rawcase')
need(r['all_eleven_edges_and_heads_match'] and len(r['source_mixed_edges'])==11,'Graph binding')
need(all(r['negative_controls'].values()),'Negativecontrol')
need(r['exact_bound_article']==v['exactboundarticle_sha256']=='e49e72c09183679f04362afe37917e410f0b8b6fe5dc98f423a0b642dce78cf4','Article binding')
need(r['exact_bound_archive']==v['exactboundarchive_sha256']=='477c160057f7a729215dfd37960063d283ddbedcf95396a8239a9fd22e94ac62','Archive binding')
need(v['disposition']=='CENTRAL_IMPORTED_FINITE_PROOF_GAP_REMAINS' and v['bypass_found'] is False,'Disposition')
for k in ['publication_authority','rendered','live','native','originals_modified']:need(v[k] is False,'Authority gate')
for k in ['root_adoption','followup','canonical','AA']:need(v[k] is None,'Null gate')
need((O/'.gitignore').read_text()=='cache/\n','Privatecacheignore')
if (O/'FINAL_MANIFEST.json').exists():
 m=load('FINAL_MANIFEST.json')
 for name,spec in m['owned_bindings'].items():need(bind(O/name)==spec,'Owned changed: '+name)
 need({str(p.relative_to(O)) for p in O.rglob('*') if p.is_file()}==set(m['owned_bindings'])|{'FINAL_MANIFEST.json','FINAL_SEAL.json'},'Unexpected/missingfile')
 need(bind(O/'FINAL_MANIFEST.json')==load('FINAL_SEAL.json')['manifest_binding'],'Seal mismatch')
print(json.dumps(dict(status='PASS_READ_ONLY_RECONCILIATION_CUSTODY',preserved_original_bindings=len(b),
 owned_sealed=(O/'FINAL_SEAL.json').exists(),source_programs_or_atlas_rerun=False,writes=False),indent=2))
