"""Enumerate only this family's outputs. No glob exclusions except explicit files."""
from pathlib import Path
import datetime,hashlib,json
b=Path(__file__).resolve().parent
manifest=b/'OWNERSHIP_MANIFEST.json'
foreign={
 'foreign_primary/original_owr_2020_6.pdf':'Official EMS original; foreign primary PDF',
 'foreign_primary/jkp_arxiv_2103.16430v2.pdf':'Johnston–Kabluchko–Prochno author manuscript; foreign primary PDF',
 'foreign_primary/original_mfo_candidate_url.pdf':'Official MFO original at candidate URL; foreign primary PDF',
 'foreign_primary/publisher_metadata.html':'IMPAN primary publication metadata and abstract; foreign HTML',
 'foreign_primary/jkp_render-02.png':'Rendered foreign primary manuscript p2',
 'foreign_primary/jkp_render-03.png':'Rendered foreign primary manuscript p3',
 'foreign_primary/jkp_render-04.png':'Rendered foreign primary manuscript p4',
 'foreign_primary/owr_p413.png':'Rendered foreign primary original p413',
}
first=[];excluded=[]
for p in sorted(b.rglob('*')):
 if not p.is_file() or p==manifest:continue
 name=str(p.relative_to(b));raw=p.read_bytes()
 row={'path':name,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
 if name in foreign:row['reason']=foreign[name];excluded.append(row)
 else:first.append(row)
if set(foreign)!={x['path'] for x in excluded}:raise RuntimeError('Foreign inventory mismatch')
record={'schema':'compactness-source-exact-family-ownership/v1','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'family_root':str(b),'first_party_files':first,'foreign_individually_excluded':excluded,'self_manifest_files':[{'path':'OWNERSHIP_MANIFEST.json','role':'Exact ownership self-manifest; cryptographic self-hash is necessarily omitted, external final tool hash records bytes'}],'excluded_directories':[],'parent_or_sibling_files_claimed':[],'ownership_scope':'These files only, inside this new compactness_source_family. Foreign source full bodies and derived renders are evidence, not first-party mathematical text. No original candidate artifact is copied into the family as our mathematical writing.','single_file_limit_bytes':100*1024*1024}
manifest.write_text(json.dumps(record,indent=2)+'\n')
allfiles=[x for x in b.rglob('*') if x.is_file()]
if len(allfiles)!=len(first)+len(excluded)+1:raise RuntimeError('Inventory closure mismatch')
if any(p.stat().st_size>=100*1024*1024 for p in allfiles):raise RuntimeError('Single-file limit')
print(json.dumps({'first_party':len(first),'foreign':len(excluded),'self_manifests':1,'exact_total_files':len(allfiles),'manifest_sha256':hashlib.sha256(manifest.read_bytes()).hexdigest(),'max_bytes':max(p.stat().st_size for p in allfiles)},indent=2))
