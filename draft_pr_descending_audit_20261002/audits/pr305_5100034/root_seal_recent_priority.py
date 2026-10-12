"""Close ROOT's bounded recent-priority evidence without granting final priority."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,stat
A=Path(__file__).resolve().parent
utc=lambda:datetime.now(timezone.utc).isoformat()
sha=lambda b:hashlib.sha256(b).hexdigest()
pin=lambda p:{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes()),'mode':format(p.stat().st_mode&0o777,'04o')}
# Third-party full web text is private reference custody, not a public artifact.
moves=[]
for i in range(1,5):
 p=A/('ROOT_PRIORITY_WEB_DISCOVERY_00'+str(i)+'.json');q=A/'root_priority_recent_private'/p.name
 assert p.is_file() and not q.exists();before=pin(p);p.rename(q);assert pin(q)==before
 moves.append({'from':p.name,'to':str(q.relative_to(A)),'pin':before})
provenance=json.loads((A/'ROOT_PRIORITY_CURRENT_PROVENANCE.json').read_text())
acquisition=json.loads((A/'ROOT_PRIORITY_RECENT_ACQUISITION.json').read_text())
assert acquisition['candidate']['commit']=='cc083024dbd00de06ad444cd4070f51f60d209eb'
assert acquisition['candidate']['author_date']=='2026-10-02T06:06:35Z'
for name,j in provenance['zenodo'].items():
 assert j['failure'] is None and j['updated']<'2026-10-02T06:06:35Z'
 f=next(f for f in j['files'] if f['key']=='main.pdf')
 assert f['size']==j['website_pdf']['bytes'] and f['checksum']=='md5:'+j['website_pdf']['md5']
 assert acquisition['sources'][name]['sha256']==j['website_pdf']['sha256']
files={}
for dirname in ['root_priority_recent_private','root_priority_current_private']:
 d=A/dirname
 for p in sorted(d.iterdir()):
  assert p.is_file() and not p.is_symlink();p.chmod(0o444);files[str(p.relative_to(A))]=pin(p)
 d.chmod(0o555)
j={'utc':utc(),'status':'PASS_ROOT_RECENT_ROUTE_CLOSED_NO_FINAL_PRIORITY_CLEARANCE','report':pin(A/'ROOT_PRIORITY_RECENT_COMPARISON.md'),'private_payload_count':len(files),'private_payloads':files,'private_directories_mode':'0555','relocated_tool_source_captures':moves,'root_full_primary_texts_read':['recent0021.txt complete6pages','recent0027.txt complete7pages; truncated combined output followed by bounded remaining section read','recent0014.txt complete9pages; truncated combined output followed by bounded beginning/middle reads'],'three_exact_public_record_pdf_descriptor_matches':True,'candidate_timestamp_from_exact_provider_commit':True,'independent_priority_families_still_active':True,'final_priority_clearance':False,'preprint_ready':False,'merge_clearance':False,'publication_clearance':False,'completion_estimates':{'mathematics':100,'priority':35,'workflow':35}}
(A/'ROOT_PRIORITY_RECENT_ROUTE_SEAL.json').write_text(json.dumps(j,indent=2)+'\n')
with (A/'RESEARCH_LOG.md').open('a') as f:f.write('\n## '+j['utc']+' — bounded recent-publication route closed\n\nThree complete primary texts and their exact published-PDF descriptor/date maps were inspected for E/M/C implications. Related methods and restricted results found, no full target theorem identified in these three texts. Current exact-ID repository/catalog observations remain explicitly bounded. Two independent literature routes remain active; no final priority or preprint/publication gate. Best guesses: mathematics100%; bounded priority35%; workflow35%. See ROOT_PRIORITY_RECENT_COMPARISON.md and native custody/seal.\n')
print(json.dumps({'utc':j['utc'],'status':j['status'],'private_payload_count':len(files),'report':j['report'],'seal':pin(A/'ROOT_PRIORITY_RECENT_ROUTE_SEAL.json'),'completion_estimates':j['completion_estimates']},indent=2))
