"""Offline closed-inventory and administrative receipt consistency verification.
Usage: python -I -S -B verify_packet.py ABS_PACKET MANIFEST_SHA CHECKER_SHA
No network calls, mathematical candidate execution, or writes.
"""
from pathlib import Path
import collections,hashlib,json,stat,sys

def need(v,m):
 if not v:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 need(len(sys.argv)==4,'Expected absolute packet and two external pins');root=Path(sys.argv[1]);need(root.is_absolute() and root.is_dir() and not root.is_symlink(),'Absolute nonsymlink packet')
 need(Path(__file__).resolve()==(root/'verify_packet.py').resolve(),'Executing checker belongs to packet')
 need(sha((root/'MANIFEST.json').read_bytes())==sys.argv[2],'External manifest pin');need(sha((root/'verify_packet.py').read_bytes())==sys.argv[3],'External checker pin')
 m=json.loads((root/'MANIFEST.json').read_text());need(m['schema']=='closed-admin-scope-packet-v1','Manifest schema');files=m['files']
 need(set(p.name for p in root.iterdir())==set(files)|{'MANIFEST.json','verify_packet.py'},'Closed file inventory')
 for p in root.iterdir():need(stat.S_ISREG(p.lstat().st_mode) and p.stat().st_nlink==1,'Regular unlinked packet file')
 for n,digest in files.items():need('/' not in n and '\\' not in n and sha((root/n).read_bytes())==digest,'Exact manifest member')
 def read(n):return json.loads((root/n).read_text())
 for n in ['ANTECEDENT_RECEIPT.json','CLOSURE_READBACK.json','NATIVE_SCOPE_READBACK.json','PUBLIC_RECORD_READBACK.json','FINAL_SCREEN_READBACK.json','DELIVERY_LOCAL_READBACK.json']:need(read(n)['result']=='PASS','Administrative receipt PASS: '+n)
 a=read('ANTECEDENT_RECEIPT.json');n=read('NATIVE_SCOPE_READBACK.json');c=read('CLOSURE_READBACK.json');f=read('FINAL_SCREEN_READBACK.json');p=read('PUBLIC_RECORD_READBACK.json');d=read('DELIVERY_LOCAL_READBACK.json');s=read('STATUS.json')
 need(a['original_files']==n['originals_confirmed_at_reviewed_head']==54 and a['original_bytes']==365960 and a['original_archive_members']==30,'Preserved original file/archive count')
 need(a['head']==c['head']=='cc45ec9dc93515593c3b2a228def86c3a562e13f' and a['comment_sha256']==c['comment_sha256'],'Reviewed closure identity')
 need(c['state']=='closed' and c['merged'] is False and c['draft'] is True,'Closed unmerged draft')
 need(n['commit']=='287ac5133f14ea223d7c32b0faa81820948ca7ba' and n['parent']=='010cf0f04d9824331f6fabc059202480daceb0bf','Native immutable commit identity')
 need(n['after_root_tree']==n['independently_rebuilt_root_tree']=='2fe751fb7ec0c10339d078a27ca9161b69b84973' and len(n['complete_changed_paths'])==8,'Complete eight-path Merkle result')
 need(n['own_original_budget']=='5/5' and n['own_DOI_blank'] is True and n['native_status']=='already_solved','Own outcome/budget/DOI')
 need(n['original_main_entries_present_unchanged']==0 and n['original_main_entries_absent_unchanged']==54 and p['includes_all_54_originals_as_audit_copies'] is True,'Precise native absence versus preserved audit copies')
 need(f['all_integer_numbers_queried_twice']==101 and f['fresh_exact_head_queue_bindings']==f['immutable_source_blobs_replayed']==89 and f['remaining_exact_claimed_solved']==[],'Complete final eligibility')
 need(f['excluded_open_drafts']=={'unsolved':80,'already_solved':9},'Exact excluded counts')
 need(f['merged']==[718,742,764,765,778,781,786,788,789] and f['closed_unmerged']==[734,767,799],'Final disposition lists')
 cap=read('FINAL_METADATA_CAPTURES.json');need(sha((root/'FINAL_METADATA_CAPTURES.json').read_bytes())==f['capture_receipt_sha256'],'Capture receipt pin')
 metas=[]
 for side in ['before','after']:
  rows=[];need(len(cap[side])==5,'Five complete metadata batches')
  for start,batch in zip(range(700,801,25),cap[side]):
   numbers=list(range(start,min(start+25,801)));need(set(batch['response'])=={'p'+str(i) for i in numbers},'Direct alias metadata coverage');rows.extend(batch['response']['p'+str(i)] for i in numbers)
  need([r['number'] for r in rows]==list(range(700,801)),'All 101 integer numbers');metas.append(rows)
 need(metas[0]==metas[1],'Stable before and after full metadata')
 open_rows=[r for r in metas[0] if r['state']=='OPEN' and r['isDraft']];need([r['number'] for r in open_rows]==[r['number'] for r in f['own_rows']],'Exactly every open draft own row screened')
 bindings={}
 for batch in cap['queue_bindings']:bindings.update(batch['response'])
 need(set(bindings)=={'q'+str(r['number']) for r in open_rows},'Exactly all 89 immutable-source bindings')
 for r in f['own_rows']:
  need(r['status']!='claimed_solved' and bindings['q'+str(r['number'])]['oid']==r['queue_blob_oid'],'Fresh source binding and exact noneligibility')
 need(dict(collections.Counter(r['status'] for r in f['own_rows']))==f['excluded_open_drafts'],'Own-row exact status counts')
 need(d['local_PDFs_independently_hashed']==9 and d['total_PDF_bytes']==638324 and d['new_external_mutations']==0,'Nine local PDF bindings')
 need(s['result']=='PASS' and s['remaining_actionable_administrative_issues']==[] and s['administrative_scope_completion_percent']==100 and s['mathematical_re_review_performed'] is False,'Final scoped administrative outcome')
 print(json.dumps({'result':'PASS','closed_files':len(files)+2,'scope':'Offline integrity and stored administrative consistency only; not formal mathematical verification','original_files':54,'native_changed_paths':8,'range_numbers':101,'excluded_drafts':89,'remaining_claimed_solved':0,'final_PDFs':9,'network_calls':0,'writes':0},sort_keys=True))
if __name__=='__main__':main()
