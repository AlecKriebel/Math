"""Read back actual provider metadata before or after original-head integration."""
from pathlib import Path
import datetime,hashlib,importlib.util,json,sys
A=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('scope170',A/'prepare_scoped_merge.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
TITLE='[claimed_solved] 30003480: Gram-locus obstruction; qualified contemporary publication'
def main():
 m.require(len(sys.argv)==2 and sys.argv[1] in ['accepted','merged'],'Choose exact metadata phase')
 merged=sys.argv[1]=='merged';body=A/('PR_BODY_MERGED.md' if merged else 'PR_BODY_ACCEPTED.md')
 pr=m.api('pulls/170')
 m.require(pr['title']==TITLE and pr['body']==body.read_text() and pr['head']['sha']==m.ORIGINAL and not pr['draft'],'Actual PR title/body/original head differs')
 if merged:
  acceptance=json.loads((A/'MERGE_AND_NATIVE_ACCEPTANCE.json').read_text())
  m.require(pr['merged'] and pr['state']=='closed' and pr['merge_commit_sha']==acceptance['merge_commit'],'Actual provider merge differs')
 else:m.require(not pr['merged'] and pr['state']=='open','Original PR no longer open')
 receipt={'UTC':datetime.datetime.now(datetime.UTC).isoformat(),'status':'ACTUAL_MERGED_PR_METADATA_READBACK_ACCEPTED' if merged else 'ACTUAL_READY_ORIGINAL_HEAD_PR_METADATA_READBACK_ACCEPTED','PR':170,'title':TITLE,'original_head':pr['head']['sha'],'GitHub_PR_state':'MERGED' if merged else 'OPEN_READY','body_sha256':hashlib.sha256(body.read_bytes()).hexdigest(),'draft':pr['draft'],'merge_commit':pr['merge_commit_sha'] if merged else None,'body_and_title_exact':True}
 m.save(A/('PR_METADATA_MERGED_ACCEPTANCE.json' if merged else 'PR_METADATA_ACCEPTANCE.json'),receipt)
 print(json.dumps(receipt))
if __name__=='__main__':main()
