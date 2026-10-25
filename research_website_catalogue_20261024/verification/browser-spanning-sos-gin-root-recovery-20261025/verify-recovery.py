from pathlib import Path
import json,hashlib,subprocess
from datetime import datetime,timezone
P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024'); E=Path(__file__).parent
B=P/'verification/browser-spanning-sos-gin-sol-20261025'
def bind(p):
 b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def verify(base,rows):
 for x in rows:
  p=Path(x['path']);p=p if p.is_absolute()else base/p
  b=bind(p)
  if any(b[k]!=x[k] for k in ('bytes','sha256')):raise RuntimeError('Changed '+str(p))
 return len(rows)
counts={}
counts['interrupted_owned']=verify(B,json.loads((B/'INTERRUPTED_MANIFEST.json').read_text())['files'])
R=B/'reconnection-finish-20261025'
counts['additive_reconnection_owned']=verify(R,json.loads((R/'FINAL_MANIFEST.json').read_text())['files'])
counts['fresh_504_era_originals']=verify(B,json.loads((B/'preservation-before.json').read_text())['files'])
triples=[('23181280','aggregate-root-dependent-spanning-tree-cost','root_dependent_spanning_trees.pdf'),('23181280','aggregate-root-dependent-spanning-tree-cost','root_dependent_spanning_trees_support.zip'),('23442760','quadratic-sos-density-bounds-convex-bodies','Convex_Body_SOS_Density_Note_v1.0.pdf'),('23442760','quadratic-sos-density-bounds-convex-bodies','Convex_Body_SOS_Density_Verification_v1.0.zip'),('23395703','seven-hyperplane-generic-initial-degree-bound','seven_plane_gin.pdf'),('23395703','seven-hyperplane-generic-initial-degree-bound','verification-package.zip')]
rows=[]
for i,slug,name in triples:
 paths=[Path('/Users/alec/Downloads')/name,P/'papers'/i/'sources'/name,Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public/research')/slug/name]
 vals=[bind(p) for p in paths]
 if len({(x['bytes'],x['sha256']) for x in vals})!=1:raise RuntimeError('Download mismatch '+name)
 rows.append({'record':i,'filename':name,'download_source_site':vals,'three_way_exact':True})
site=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=site,text=True).strip()
if head!='dcc259dbd4fd4285a65374e20ae65281fa30e852':raise RuntimeError('Release changed')
public=len([p for p in (site/'public').rglob('*') if p.is_file()])
if public!=504:raise RuntimeError('Public count differs')
result={'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS_EXACT_FILE_IDENTITY_AND_ORIGINAL_PRESERVATION','counts':counts,'downloads':rows,'site_head':head,'public_files':public,'ui_claim':'Actual screenshot/AX evidence and root tool actions; filesystem checks do not independently prove browser interaction.'}
if '--record' in __import__('sys').argv:
 out=E/'CUSTODY_DOWNLOAD_RESULT.json'
 if out.exists():raise RuntimeError('Immutable receipt already exists')
 out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':result['status'],'counts':counts,'actual_downloads':len(rows),'public_files':public}))
