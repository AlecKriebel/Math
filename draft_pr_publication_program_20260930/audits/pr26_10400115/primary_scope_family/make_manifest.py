from pathlib import Path
import datetime, hashlib, json
P=Path(__file__).resolve().parent
M=P/'FIRST_PARTY_MANIFEST.json'
if M.exists():raise SystemExit('Preserve the sealed manifest; create a new version instead.')
entries=[]
for f in sorted(P.rglob('*')):
 if not f.is_file() or f==M or 'primary_sources' in f.relative_to(P).parts:continue
 entries.append({'path':str(f.relative_to(P)),'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()})
sources=[]
for f in sorted((P/'primary_sources').iterdir()):
 if f.is_file():sources.append({'path':str(f.relative_to(P)),'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()})
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Owned primary_scope_family audit outputs, copied historical repository scripts and their isolated reproduction receipts; excludes this manifest itself. Third-party downloaded primary texts and derivative renders have a separate source-evidence inventory, without claiming authorship.','self_excluded':'FIRST_PARTY_MANIFEST.json','first_party_files':entries,'first_party_file_count':len(entries),'third_party_source_evidence':sources,'source_render_caveat':'scherich_p2022_high.png is a preserved wrong-offset render of printed2023 from s-PDF, not Example3.11 evidence. The correct high-resolution Example3.11 render is scherich_s_p2022_high.png. Early p-PDF printed2022 render is scherich-16.png.','sealed_input_head':'762f5808268a85a5cb5373d3f7d60ad160b828f5','full_target_status':'Unsolved in this investigation; no target proof attempt added.'}
M.write_text(json.dumps(out,indent=2)+'\n')
assert all((P/x['path']).stat().st_size==x['bytes'] and hashlib.sha256((P/x['path']).read_bytes()).hexdigest()==x['sha256'] for x in entries+sources)
print(json.dumps({'manifest':str(M),'sha256':hashlib.sha256(M.read_bytes()).hexdigest(),'first_party_count':len(entries),'third_party_source_evidence_count':len(sources),'all_listed_hashes_pass':True},indent=2))
