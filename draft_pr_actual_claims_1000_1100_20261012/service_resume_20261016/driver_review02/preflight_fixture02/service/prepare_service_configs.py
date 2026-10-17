"""Read-only package/metadata preflight; writes only this new service folder."""
from pathlib import Path
import json,hashlib,datetime,subprocess
D=Path(__file__).resolve().parent.parent; R=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text())
def need(c,s):
 if not c:raise RuntimeError(s)
def identity(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
registry={r['pr']:r for r in read(D/'CLAIM_REGISTRY.json')['records']};state=read(D/'STATE.json')
manifest_paths={1033:'publication/zenodo-deposit.json',1034:'publication/zenodo-deposit.json',1037:'preprint/zenodo-deposit.json',1041:'preprint_v1_0/zenodo-deposit.json',1047:'preprint_v1_0/zenodo-deposit.json',1052:'publication/zenodo-deposit.json',1064:'preprint_v1_0/publication/zenodo-deposit.json',1071:'publication/zenodo-deposit.json',1080:'preprint_v1_0/deposit_metadata.json',1085:'preprint_v1_0/zenodo-deposit.json',1094:'preprint_v1_0/zenodo-deposit.json',1097:'preprint_v1_0/zenodo-deposit.json',1098:'preprint_v1_0/publication/zenodo-deposit.json'}
expected={
1033:[(81135,'9d10b9dbfd7540cdd6e5dd298c079c6834bc3c404d3494dd4e485dd654ca1e56'),(341341,'889e7f50364adafff6211e5edbdeea7845ef26e3822430ec4e1f26dc8f3a54d8')],
1034:[(132958,'3a3f2a9e4bbd002217fca218f963957245b767e4a782e80b917031a3ef2d250f'),(1899507,'55448cdcfb582cf2869f8b421f2141ed1d03d30a528e112df4935499280004d1')],
1037:[(124384,'d5909d26fa9d5777fffa77dd0b76a0f9d9334395fa995e90a2fc2ad002cc62c4'),(1041495,'cf9ca0625bd17bedfe7b78c90cb9e444fd11950b537da0677fa69407561241e2')],
1041:[(108357,'3ba83c50a4a2369a70897ee165a43f56324aa31574cf9c199e664174cbce0449'),(680672,'cd20964fe478365bd9c2db9b6cd8f6032aea0168073e7da21149865ec2f6d34c')],
1047:[(72363,'1ce63633a68179f5e9296fee9493632c4d6272918b8a42172eb382fbb0e0532d'),(1471927,'17e307809e960172f59e7430386c2f1c75784edb7fc394d16e15e210b7885eee')],
1052:[(58570,'e2be83ab3c334c8352f1c6a256c6038b59ed834d3beaa50ed7602f3c24f292a6'),(1681157,'0bb83d60cc0454870282dc251e1f459bced13165634933d0b5bf853b172b6a6d')],
1064:[(74898,'67f07f64a5b06c9a4372c285ed438e735fb780d8477b25652bea4f7f6c72e072'),(658533,'d1646f1c72d8ef64cfa07f0d66ba2c2e4b1523b030a494578e90362919af6355')],
1071:[(93113,'33b90a4d846db58ea93efd453c13455fbeb3a29dcaa3e4cc49a68c0a8ebdff5b'),(3101130,'4e4a1b20c2da7f5a6e686256f7f8d7bba9c8db71e21f316f99da63285f7b0191')],
1080:[(84937,'2337d141a8985f73a942f97e23727fe8e9e7857a653ff154fa2a76d5c90b27ed'),(18251309,'e19b72601d899d4f1c732d23ad821fad75d52dd2382b18491ef80419ca85899a')],
1085:[(97501,'464de043ac6b723f3bd5c03dddb6efd1c0bfeb05b5209bb532006580b7aedc2d'),(592060,'f986ce010bfa91509497c17eed8369e80955cd1f4f44f2d81692112cab307a66')],
1094:[(69486,'a1e2da77dd739bcc7ddc4dd8ba916c99010450e4224ae7a52d01d34c98960e72'),(1864645,'21de02dcdc08c6cd804ccf6345ede97edbfe734469dcdd83ff3b7a65c3c20f02')],
1097:[(77187,'6ae840e0b2e1df73b204c2c293c3fbcfa39206654e775a75261515c693a6187d'),(5658794,'94280d71c41617198e96f1f4b4aca043ff86c3feda3109e0af9a1a18e1db651d')],
1098:[(83409,'52d4355533f5095be83c8799bd148e9927e5c4bef8c2f6a00d534303f0b7ee5c'),(798999,'a9606c07600ca9ac60f36f5165c8c09ff3e0c0b42e83e50d006df6f1ee2723fe')]}
configs=[]
for n,relative in manifest_paths.items():
 a=next((D/'audits').glob('pr'+str(n)+'_*'));m=a/relative;data=read(m);sealpath=D/state.get('current_final_authorities',{}).get(str(n),str((a/'FINAL_SEAL.json').relative_to(D)));seal=read(sealpath)
 need(seal.get('publication_ready',seal.get('immutable_ready')) is True,'Final ready seal '+str(n))
 count=seal.get('whole_reviews_completed',seal.get('fresh_whole_package_reviews'));need(count>=2,'Two complete reviews '+str(n))
 issues=seal.get('actionable_issues')
 if n==1098:
  issues=read(a/'ROOT_WHOLE_PACKAGE_REVIEW_02.json')['actionable_P0_P1_P2_P3']
  need(seal['all_actionable_findings_resolved'] is True,'1098 final resolution')
 need(issues==0 or issues==[] or issues==dict.fromkeys(['P0','P1','P2','P3'],0),'Zero issues '+str(n))
 need(set(data)=={'metadata','files'} and len(data['files'])==2,'Native manifest shape '+str(n));files=[]
 for i,f in enumerate(data['files']):
  need(set(f)<={'path','name'} and 'path'in f,'Native file shape '+str(n));p=(m.parent/f['path']).resolve();v=identity(p);need((v['bytes'],v['sha256'])==expected[n][i],'Reviewed asset changed '+str(n));files.append({'path':str(p.relative_to(D)),'name':f.get('name',p.name),**v})
 row=registry[n];url='https://github.com/AlecKriebel/Math/pull/'+str(n)
 notes=(data['metadata']['title']+'. Accepted scope: '+row['asserted_result']+' Limits: '+row.get('remaining_scope','')+' Prior results and proof dependencies are credited in the paper. Historical novelty and worldwide current openness remain unestablished. Extensive AI use; unrefereed; '+str(count)+' fresh complete AI package reviews, latest zero actionable issues; no conventional human peer review or formal certification. Proof and verification: '+url)
 config={'pr':n,'problem_id':str(row['problem_id']),'head':row['head_oid'],'audit_folder':str(a.relative_to(D)),'manifest':str(m.relative_to(D)),'manifest_identity':identity(m),'metadata_sha256':hashlib.sha256(json.dumps(data['metadata'],sort_keys=True,separators=(',',':')).encode()).hexdigest(),'final_seal':str(sealpath.relative_to(D)),'final_seal_identity':identity(sealpath),'fresh_complete_reviews':count,'files':files,'title':data['metadata']['title'],'accepted_scope':row['asserted_result'],'limitations':row.get('remaining_scope',''),'tracker_original_problem':'Catalogue problem '+str(row['problem_id'])+'; original formulation/proof provenance: '+url,'tracker_notes':notes,'pr_title':'Accept '+str(row['problem_id'])+': '+data['metadata']['title'],'historical_scope':'All old local pending/hold/status fields remain exact dated history. New external receipt after prior PR1032 completes governs service progress.'}
 need(len(config['pr_title'])<=256,'PR title too long');(R/f'PR{n}_SERVICE_CONFIG.json').write_text(json.dumps(config,indent=2)+'\n');configs.append({'pr':n,'manifest':config['manifest'],'files':files,'fresh_complete_reviews':count})
(R/'READY_PACKAGE_PREFLIGHT.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS_13_NATIVE_INPUTS_MATCH_REVIEWED_CURRENT_PDF_ARCHIVE_BYTES','records':configs,'scope':'Read-only identity and final-seal accounting preflight. No new mathematical review, compile/render, external upload, tracker or PR mutation.'},indent=2)+'\n')
print(json.dumps({'status':'PASS','packages':len(configs),'assets_rehashed':26}))
