"""Authenticate the complete bounded independent transport review before use."""
from pathlib import Path
import datetime,hashlib,json
A=Path(__file__).resolve().parent
D=A/'zenodo_transport_adversary'
def require(c,m):
 if not c:raise RuntimeError(m)
def pin(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def main():
 seal=json.loads((D/'FINAL_SEAL.json').read_text())
 allow=json.loads((D/'PUBLIC_ALLOWLIST.json').read_text())['allowlisted_files']
 require(set(allow)==set(seal['files'])|{'FINAL_SEAL.json'},'Incomplete independent final seal')
 require({p.name for p in D.iterdir() if p.is_file()}==set(allow),'Uninventoried audit file')
 require(pin(D/'FINAL_SEAL.json')['sha256']=='3f2cb5bf3973b2707b1798f893048e070f193818568a5aa865a0542665f66e21','Independent seal changed')
 for name,v in seal['files'].items():
  p=D/name;require(pin(p)=={k:v[k] for k in ['bytes','sha256']},'Audit file changed: '+name)
 for name in allow:require((D/name).stat().st_mode&0o777==0o444,'Audit not sealed: '+name)
 inputs=json.loads((D/'PINNED_INPUTS.json').read_text())
 for name,v in inputs['inputs'].items():require(pin(Path(name))==v,'Audited input changed: '+name)
 cross=json.loads((D/'CROSS_MODE_VERIFICATION.json').read_text())
 require(cross['all_controls_pass'] and cross['control_outcomes_identical'] and cross['semantic_checks_identical'],'Cross-mode controls failed')
 require(cross['ordinary_controls']==cross['optimized_controls']==106 and cross['accepted_controls']==11 and cross['rejected_controls']==95,'Unexpected controls')
 for name in ['ordinary_network_attempts','optimized_network_attempts','ordinary_private_reads','optimized_private_reads']:require(cross[name]==[],'Independent scope exceeded')
 verdict=json.loads((D/'VERDICT.json').read_text())
 require(verdict['verdict']=='PASS_FOR_PRECISELY_THIS_FROZEN_TRANSPORT_ALLOWANCE' and verdict['necessary_fixes']==[],'Transport repair remains')
 require(verdict['draft_id']==23318851 and verdict['guard_identity']==pin(A/'zenodo_exact_description_guard.py'),'Wrong draft or guard')
 science=json.loads((A/'ROOT_PUBLICATION_GATE.json').read_text())
 require(science['status']=='READY_FOR_AUTHORIZED_PUBLICATION' and science['human_authorized_qualified_publication'] and science['fresh_seal_first_review_clean'],'Scientific publication gate absent')
 result={'UTC':datetime.datetime.now(datetime.UTC).isoformat(),'status':'EXACT_HTML_DESCRIPTION_TRANSPORT_GUARD_INDEPENDENTLY_VERIFIED','PR':170,'draft_id':23318851,'guard_identity':verdict['guard_identity'],'independent_final_seal':pin(D/'FINAL_SEAL.json'),'independent_report':pin(D/'REVIEW.md'),'authenticated_owned_artifacts':len(allow),'authenticated_inputs':len(inputs['inputs']),'ordinary_controls':106,'optimized_controls':106,'accepted_baselines':11,'rejected_false_variants':95,'scope':'Only exact entire frozen description with both n>=3 and n>=4 serialized as n&gt;=3 and n&gt;=4 once each. All remaining tags, text, submitted metadata, files and original kit checks remain exact. Existing original kit representation allowances are unchanged.','frozen_metadata':pin(A/'publication_package_v2/metadata.json'),'deposit_manifest':pin(A/'zenodo-deposit.v2.json'),'scientific_gate':pin(A/'ROOT_PUBLICATION_GATE.json'),'original_kit_files':science['kit_files'],'upload_files':{n:science['files'][n] for n in science['upload_files']},'no_candidate_or_kit_changes':True,'no_duplicate_draft_authorized':True,'publication_authorization':'Prior direct human instruction; independent transport review supplies verification, not authorization.','actual_published':False}
 p=A/'ROOT_PUBLICATION_TRANSPORT_GATE.json';require(not p.exists(),'Transport gate already exists')
 p.write_text(json.dumps(result,indent=2)+'\n');p.chmod(0o444)
 for name in ['zenodo_exact_description_guard.py','test_zenodo_description_guard.py','ROOT_ZENODO_DESCRIPTION_GUARD_CONTROLS.json','ZENODO_HTML_REPRESENTATION_DIAGNOSTIC.json']:(A/name).chmod(0o444)
 print(json.dumps({'status':result['status'],'gate':pin(p),'artifacts':len(allow),'inputs':len(inputs['inputs']),'draft_id':23318851}))
if __name__=='__main__':main()
