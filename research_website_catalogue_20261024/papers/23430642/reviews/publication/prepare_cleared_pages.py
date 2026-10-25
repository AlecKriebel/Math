from pathlib import Path
import hashlib,json,datetime,shutil
R=Path(__file__).resolve().parents[4]
S=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
clearance_rel='verification/root-clearance-game-seshadri-20261025.json'
clearance_path=R/clearance_rel
clearance=json.loads(clearance_path.read_text()); assert clearance['status']=='PASS' and clearance['disposition_by']=='root'
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
preflight={'utc':now,'completion_percent':80,'root_clearance_sha256':sha(clearance_path),'shared_before':{},'papers':{}}
for rel in ['scripts/render_page.py','scripts/published_assets.py','scripts/verify_live.py']:
 preflight['shared_before'][str(R/rel)]=sha(R/rel)
for rel in ['research/research.css']:
 preflight['shared_before'][str(S/rel)]=sha(S/rel)
for decision in clearance['papers']:
 rid=decision['record_id'];P=R/'papers'/rid;D=P/'reviews/publication'
 c=json.loads((D/'publication.json').read_text()); receipt=json.loads((P/'sources/receipt.json').read_text())
 assert decision['status']=='PASS' and c['doi']=='10.5281/zenodo.'+rid
 assert sha(P/'sources/receipt.json')==decision['source_receipt_sha256']
 assert sha(P/'sources'/decision['pdf_filename'])==decision['pdf_sha256']
 assert sha(P/'sources'/decision['supplement_filename'])==decision['supplement_sha256']
 reviews={}
 for kind,v in decision['reviews'].items():
  assert sha(P/v['report'])==v['report_sha256']
  assert sha(P/v['verdict_file'])==v['verdict_sha256']
  verdict=json.loads((P/v['verdict_file']).read_text())
  reviews[kind]={'report':v['report'],'sha256':v['report_sha256'],'verdict_file':v['verdict_file'],'verdict_sha256':v['verdict_sha256'],'verdict':verdict,'root_disposition':v['status']}
 for asset in receipt['files']:
  raw=(P/'sources'/asset['name']).read_bytes()
  assert len(raw)==asset['bytes'] and hashlib.sha256(raw).hexdigest()==asset['sha256'] and 'md5:'+hashlib.md5(raw).hexdigest()==asset['zenodo_checksum']
 shutil.copyfile(D/'publication.json',P/'publication.json')
 gate={'record_id':rid,'status':'PASS','disposition_by':'root','created_utc':now,'approved_scope':decision['approved_scope'],'root_clearance':clearance['authorization'],'root_clearance_file':clearance_rel,'root_clearance_sha256':sha(clearance_path),'root_clearance_record':decision,'pdf_sha256':decision['pdf_sha256'],'supplement_sha256':decision['supplement_sha256'],'publication_sha256':sha(P/'publication.json'),'source_receipt_sha256':decision['source_receipt_sha256'],'source_files':receipt['files'],'reviews':reviews,'scope_gate_resolution':'The frozen scope-only material retains its original independent scope boundary. Root read all final reports and the full manuscript, then issued the separately bound scientific clearance. No source or scientific review was rewritten.','source_repair':False,'human_peer_review':False,'formal_machine_verification':False,'follow_up':None}
 (P/'promotion.json').write_text(json.dumps(gate,ensure_ascii=False,indent=2)+'\n')
 preflight['papers'][rid]={'publication_sha256':sha(P/'publication.json'),'promotion_sha256':sha(P/'promotion.json'),'all_original_assets_md5_size_sha256':'PASS','all_review_bindings':'PASS'}
 with (D/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+now+' — 80%: explicit root clearance checked against current source bytes and all three final report/verdict hashes. Wrote final publication data and promotion gate; ready for local rendering. No deployment or external record changes.\n')
(R/'papers/23430642/reviews/publication/preflight.json').write_text(json.dumps(preflight,indent=2)+'\n')
print(json.dumps(preflight,indent=2))
