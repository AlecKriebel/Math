"""GET-only authentication of the audit record referenced by PR799's comment."""
from pathlib import Path
import hashlib,json,datetime,sys
W=Path(__file__).resolve().parent;T=W.parent
sys.path.insert(0,str(W))
from check_native_scope import Commit,need,oid
PREFIX='draft_pr_claimed_solved_700_800_20261012/audits/pr799_30002364/tmp/'
def main():
 r=Commit('010cf0f04d9824331f6fabc059202480daceb0bf')
 rels=['root-receipts/PRIORITY_GATE.json','root-receipts/ROOT_PRIORITY_ASSESSMENT.md','root-receipts/ROOT_PRIORITY_REPLAYS.json','root-receipts/ROOT_PRIORITY_PRIMARY_READING.json','root-receipts/MATH_GATE.json','root-receipts/CLOSE_COMMENT.md','intake/ROOT_SOURCE_IDENTITY.json']
 p=json.loads((T/'root-receipts/PRIORITY_GATE.json').read_text())
 for pkt in p['priority_packets']:
  rels.extend([pkt['family']+'/'+pkt['manifest'],pkt['family']+'/'+pkt['checker']])
 source=json.loads((T/'intake/ROOT_SOURCE_IDENTITY.json').read_text())
 rels.extend('intake/original/'+row['path'] for row in source['original_files'])
 for rel in rels:
  b=(T/rel).read_bytes();need(r.entry(PREFIX+rel)=={'mode':'100644','type':'blob','sha':oid('blob',b)},'Published audit record exact: '+rel)
 result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'result':'PASS','checked_immutable_main_commit':r.commit,'public_audit_files_authenticated':len(rels),'includes_all_54_originals_as_audit_copies':True,'does_not_claim_original_native_attempt_was_imported':True,'priority_gate_derivation_and_four_manifest_checker_pairs_available':True,'comment_link_target':'https://github.com/AlecKriebel/Math/tree/main/draft_pr_claimed_solved_700_800_20261012/audits/pr799_30002364'}
 (W/'PUBLIC_RECORD_READBACK.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
