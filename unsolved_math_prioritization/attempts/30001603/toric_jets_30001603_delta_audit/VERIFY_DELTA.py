#!/usr/bin/env python3
"""Read-only independent correction revalidation and full mathematical replay.
Usage: python -B VERIFY_DELTA.py [original_packet corrected_release original_audit]
Requires the previously bound audit plus Python3 and SymPy1.14.0. No network.
"""
from pathlib import Path
import ast, contextlib, difflib, hashlib, io, json, subprocess, sys

OLD_MANIFEST='5ae79fd9ca09fc095a33d7acfa27818377163c1eb2161977ff172cf641420616'
OLD_PROOF='76d197a8fc07f7e3796d67a24308531aa315b0aa03a69f3a2122c3bdf7f77b68'
NEW_MANIFEST='670f3a5365201fdcda372dbd6037aefb062cda2a7dd3537522a19c4a5204fe55'
NEW_PROOF='1ae5a43cbf52ba23c3b39a99a4d5c4c376305edb375a0b343da935e8328210ed'
RELEASE='506886489cb3eba4235fa555b4d3fb6c5b46dcb8d2b6b577576f8419e2b17a9e'
BINDING='57555649b4d5b980e55ac55cb02cf6f48b1a276eddb4c54212d84b15156cef1d'
AUDIT='efd9065e283904c34c9f3c863e85b159945186e504c6c3657d5a2547078935d1'
INDEPENDENT_CODE='65a036d7000e89423557d5039c858087467a5115102629b1c5ba73aeba472719'
CHECKS=[]
def ck(ok,label):
 if not ok:raise AssertionError(label)
 CHECKS.append(label)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def unique(pairs):
 r={}
 for k,v in pairs:
  if k in r:raise ValueError('duplicate JSON key')
  r[k]=v
 return r
def js(p):return json.loads(p.read_text(),object_pairs_hook=unique)
def files(root):return {p.relative_to(root).as_posix():(p.stat().st_size,sha(p)) for p in root.rglob('*') if p.is_file()}
def validate_manifest(root,manifest,anchor):
 ck(sha(root/manifest)==anchor,'external manifest anchor '+manifest)
 m=js(root/manifest);rows=m['files'];expected={r['path'] for r in rows}|{manifest}
 actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
 ck(actual==expected and len(rows)==len(expected)-1,'exact manifest membership '+manifest)
 ck(not any(p.is_symlink() for p in root.rglob('*')),'no linked members '+manifest)
 for r in rows:
  p=root/r['path'];ck(p.stat().st_size==r['bytes'] and sha(p)==r['sha256'],'bound member '+r['path'])
 return m

def main():
 parent=Path(__file__).resolve().parent.parent
 if len(sys.argv)==4:old,release,audit=map(Path,sys.argv[1:])
 elif len(sys.argv)==1:old=parent/'toric_jets_30001603';release=parent/'toric_jets_30001603_corrected_release';audit=parent/'toric_jets_30001603_independent_audit'
 else:raise SystemExit(__doc__)
 new=release/'packet';controls=release/'controls'
 before=[files(p) for p in [old,release,audit]]
 validate_manifest(old,'MANIFEST.json',OLD_MANIFEST)
 validate_manifest(audit,'MANIFEST.json',AUDIT)
 validate_manifest(release,'RELEASE_MANIFEST.json',RELEASE)
 validate_manifest(new,'MANIFEST.json',NEW_MANIFEST)
 ck(sha(old/'PROOF.md')==OLD_PROOF and sha(new/'PROOF.md')==NEW_PROOF,'old and new proof anchors')
 ck(sha(controls/'CORRECTION_BINDING.json')==BINDING,'correction-binding anchor')
 bind=js(controls/'CORRECTION_BINDING.json')
 ck(sha(audit/'CORRECTIONS.md')==bind['correction_map']['sha256'],'original correction map binding')
 ck(sha(audit/'AUDIT.md')==bind['review_input']['sha256'],'original complete audit binding')
 expected_names={p.name for p in old.iterdir()};changed=[];diff=''
 for name in sorted(expected_names):
  a=(old/name).read_bytes();b=(new/name).read_bytes()
  if a!=b:changed.append(name)
  diff+=''.join(difflib.unified_diff(a.decode().splitlines(keepends=True),b.decode().splitlines(keepends=True),fromfile='original/'+name,tofile='corrected/'+name))
 ck(diff.encode()==(controls/'CORRECTION.diff').read_bytes(),'complete unified diff independently reproduced')
 ck(len(changed)==9 and 'CHECK_PACKET.py' not in changed,'exactly nine changed files; packet checker unchanged')
 for r in bind['files']:
  for label,p in [('old',old/r['path']),('new',new/r['path'])]:ck(p.stat().st_size==r[label]['bytes'] and sha(p)==r[label]['sha256'],'correction binding '+label+' '+r['path'])
  ck(r['changed']==(r['path'] in changed),'changed flag '+r['path'])
 ol=(old/'PROOF.md').read_text().splitlines();nl=(new/'PROOF.md').read_text().splitlines()
 ck(len(ol)==len(nl) and {i+1 for i,(a,b) in enumerate(zip(ol,nl)) if a!=b}=={3,117,119,121},'only four requested proof lines changed')
 ck('their polygon coordinates agree' in nl[2] and 'synthetic polygon-coordinate sign error' in nl[116] and nl[118]=='## 6. Source agreement and attribution boundary' and 'both give (-1,-2)' in nl[120] and 'only as a deliberate synthetic negative control' in nl[120],'all four proof replacements are source-correct')
 for filename,lines in [('README.md',{16}),('APPROACH_LOG.md',{9}),('SOURCE_GATE.md',{21,23})]:
  a=(old/filename).read_text().splitlines();b=(new/filename).read_text().splitlines()
  ck(len(a)==len(b) and {i+1 for i,(q,r) in enumerate(zip(a,b)) if q!=r}==lines,'only requested prose lines changed '+filename)
 ck('incorrectly alleged a journal typo' in (new/'SOURCE_GATE.md').read_text(),'historical source error attributed to original packet')
 a=js(old/'SOURCES.json');b=js(new/'SOURCES.json')
 for q,r in zip(a['sources'],b['sources']):
  if q['title']=='Toric vector bundles and parliaments of polytopes, published 2018 offprint':
   ck(r['inspection']=='Bibliography and Examples4.2/5.3 inspected in text; printed pages7728 and7732 image-inspected. The e1-e2 vertex (-1,-2) agrees with arXiv v3 and the filtration-derived data.','corrected journal inspection text')
   q['inspection']=r['inspection']
 ck(a==b,'all scholarly metadata unchanged except required inspection text')
 a=js(old/'STATUS.json');b=js(new/'STATUS.json');a['limits'][2]=b['limits'][2]
 ck(a==b and b['limits'][2]=='The inspected journal and arXiv v3 coordinate agree; a synthetic sign-flip test is not a source discrepancy.','only required status-limit correction')
 a=js(old/'RESULTS.json');b=js(new/'RESULTS.json');a.pop('publication_typo_control')
 ck(b.pop('synthetic_polygon_sign_control')=='Synthetic (-1,2) rejected; source-consistent (-1,-2) satisfies the e1-e2 second-ray bound','new generated synthetic-control metadata')
 ck(a==b and a['assertions']==79,'all mathematical results and 79 author assertions unchanged')
 mapping={'correct vertex respects second ray':'source vertex respects second ray','published sign typo violates filtration':'synthetic sign flip violates filtration','publication_typo_control':'synthetic_polygon_sign_control','(-1,2) rejected; (-1,-2) satisfies the e1-e2 second-ray bound':'Synthetic (-1,2) rejected; source-consistent (-1,-2) satisfies the e1-e2 second-ray bound'}
 count=[]
 class Normalize(ast.NodeTransformer):
  def visit_Constant(self,n):
   if isinstance(n.value,str) and n.value in mapping:count.append(n.value);n.value=mapping[n.value]
   return n
 ta=Normalize().visit(ast.parse((old/'VERIFY.py').read_text()));tb=ast.parse((new/'VERIFY.py').read_text())
 ck(len(count)==4 and set(count)==set(mapping) and ast.dump(ta)==ast.dump(tb),'author verifier AST differs only in four descriptive strings')
 for name in ['VERIFY.py','RESULTS.json']:
  ck('publication_typo_control' not in (new/name).read_text(),'old false output key removed '+name)
 forbidden=['The journal PDF has a local polygon-coordinate sign typo','The published polygon sign error is identified','The journal\'s printed p.7728 gives (-1,2)','Printed polygon sign typo recorded.','the published polygon typo','The published p.7728 displays (-1,2)','The published polygon sign typo is corrected']
 ck(not any(q in p.read_text() for p in new.iterdir() for q in forbidden),'no old affirmative false allegation in current packet')
 rr=subprocess.run([sys.executable,'-B',str(new/'CHECK_PACKET.py')],capture_output=True,check=True)
 ck(not rr.stderr and rr.stdout==(controls/'REPLAY_OUTPUT.json').read_bytes(),'corrected packet and three integrity controls replay exactly')
 rr=subprocess.run([sys.executable,'-B',str(controls/'VALIDATE_CORRECTION.py'),str(old)],capture_output=True,check=True)
 ck(not rr.stderr and rr.stdout==(controls/'CORRECTION_VALIDATION.json').read_bytes(),'author correction validator exact output reproduced')
 ck(sha(audit/'INDEPENDENT_VERIFY.py')==INDEPENDENT_CODE,'prior independent verifier exact source binding')
 source=(audit/'INDEPENDENT_VERIFY.py').read_text()
 # Rebind external anchors and status metadata in memory only. Mathematical code is unchanged.
 replacements={OLD_MANIFEST:NEW_MANIFEST,OLD_PROOF:NEW_PROOF,'PASS_MATHEMATICS_SOURCE_CORRECTION_REQUIRED':'PASS','Both inspected PDFs print (-1,-2). The author packet falsely labels the synthetic sign flip (-1,2) as a published typo.':'Both inspected PDFs print (-1,-2). The corrected packet agrees and identifies (-1,2) only as a synthetic negative control.'}
 for a,b in replacements.items():ck(source.count(a)==1,'one metadata rebind '+a[:28]);source=source.replace(a,b)
 namespace={'__name__':'independent_corrected_replay','__file__':str(audit/'INDEPENDENT_VERIFY.py')}
 exec(compile(source,'<bound independent corrected replay>','exec'),namespace)
 saved=sys.argv;sys.argv=['independent_corrected_replay',str(new)];capture=io.StringIO()
 try:
  with contextlib.redirect_stdout(capture):namespace['main']()
 finally:sys.argv=saved
 independent=json.loads(capture.getvalue())
 ck(independent['result']=='PASS' and independent['independent_assertions']==60 and len(independent['independent_corruption_controls'])==8,'all 60 independent checks and eight corruption controls pass on corrected packet')
 ck(independent['section_system']=={'component_total_degree_bounds':[5,3,5],'constraints':88,'nullity':12,'rank':40,'unknowns':52},'independent exhaustive polynomial system unchanged')
 ck([files(p) for p in [old,release,audit]]==before,'original packet, original audit, and corrected release all preserved')
 print(json.dumps({'schema':'toric-jets-independent-delta-verification-v1','result':'PASS','disposition':'already_solved','author_turns_used':1,'author_turn_limit':5,'corrected_packet_manifest_sha256':NEW_MANIFEST,'corrected_proof_sha256':NEW_PROOF,'corrected_release_manifest_sha256':RELEASE,'correction_binding_sha256':BINDING,'original_audit_manifest_sha256':AUDIT,'delta_assertions':len(CHECKS),'checks':CHECKS,'changed_files':changed,'full_diff_bytes':len(diff.encode()),'no_unrelated_math_edits':True,'source_description_correction_complete':True,'independent_replay':independent,'scope':'Acceptance applies only to these exact corrected bytes. Source conclusions require the bound original full audit and this delta report; finite tests alone do not certify source prose or geometric nefness.'},indent=2,sort_keys=True))
if __name__=='__main__':main()
