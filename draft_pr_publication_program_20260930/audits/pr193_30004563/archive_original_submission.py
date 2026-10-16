"""Archive immutable submitted PR193 blobs as read-only research data; never run them."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import base64,datetime,hashlib,importlib.util,json
A=Path(__file__).resolve().parent;P=A.parent.parent
HEAD='b9a399eeac816dbb8f0e50e81b498c26e5acef81';NATIVE='unsolved_math_prioritization/attempts/30004563/'
def main():
 s=importlib.util.spec_from_file_location('native193_archive',P/'audits/pr190_5000007/prepare_final_scoped_merge.py');h=importlib.util.module_from_spec(s);s.loader.exec_module(h);h.m.TREE_CACHE_PATH=A/'ARCHIVE_IMMUTABLE_TREE_CACHE.json'
 pr=h.api('pulls/193');h.require(pr['head']['sha']==HEAD and pr['state']=='open' and pr['draft'] and not pr['merged'],'Original PR head/state changed')
 co=h.api('git/commits/'+HEAD);found=h.lookup(co['tree']['sha'],NATIVE.rstrip('/'));h.require(found and found[1]=='tree','Original attempt tree missing')
 rows=h.api('git/trees/'+found[2]+'?recursive=1')['tree'];blobs=[x for x in rows if x['type']=='blob'];h.require(0<len(blobs)<200,'Unexpected original inventory')
 def fetch(x):
  rel=x['path'];h.require(not Path(rel).is_absolute() and '..' not in Path(rel).parts,'Unsafe original data path')
  j=h.api('git/blobs/'+x['sha']);b=base64.b64decode(j['content']);h.require(hashlib.sha1(b'blob '+str(len(b)).encode()+bytes([0])+b).hexdigest()==x['sha'],'Git blob data mismatch')
  dest=A/'original_submission/files'/NATIVE/rel;dest.parent.mkdir(parents=True,exist_ok=True)
  with dest.open('xb') as f:f.write(b)
  dest.chmod(0o444);return {'path':NATIVE+rel,'mode':x['mode'],'git_blob':x['sha'],'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
 with ThreadPoolExecutor(max_workers=6) as ex:files=sorted(ex.map(fetch,blobs),key=lambda x:x['path'])
 stamp=datetime.datetime.now(datetime.UTC).isoformat();manifest={'UTC':stamp,'PR':193,'problem_id':30004563,'original_head':HEAD,'original_commit_tree':co['tree']['sha'],'original_commit_parents':[x['sha'] for x in co['parents']],'title':pr['title'],'files':files}
 target=A/'ORIGINAL_FILE_MANIFEST.json'
 with target.open('x') as f:json.dump(manifest,f,indent=2);f.write('\n')
 target.chmod(0o444)
 status={'UTC':stamp,'PR':193,'problem_id':30004563,'original_head':HEAD,'original_QUEUE_status':'claimed_solved','original_effort':'2/5','status':'ORIGINAL_SUBMISSION_PRESERVED_EXACT_TARGET_AND_COUNTEREXAMPLE_UNREVIEWED','case_percent':5,'mathematical_clearance':False,'priority_clearance':False,'publication_ready':False,'actual_Zenodo_published':False,'actual_tracker_updated':False,'actual_original_PR_merged':False,'fully_completed_count':40,'published_count':24,'goal_complete':False,'remaining_required_steps':'Define exact original conjecture and hypotheses; adversarial source-first mathematical audits and independent reproduction; priority then whole-package reviews and actual publication/disposition as warranted.'}
 with (A/'CURRENT_CASE_STATUS.json').open('x') as f:json.dump(status,f,indent=2);f.write('\n')
 with (A/'RESEARCH_LOG.md').open('a') as f:f.write(stamp+' — PR193 workflow5%: immutable original claimed_solved2/5 submission archived as read-only exact blobs. Mathematical/priority/publication clearance0%; target claim unreviewed. Prior PR191 actually complete,40completed/24published. Broader goal active.\n')
 last=h.api('pulls/193');h.require(last['head']['sha']==HEAD and last['state']=='open' and last['draft'] and not last['merged'],'Current PR changed during archival; immutable archived head retained')
 print(json.dumps({'PR':193,'original_head':HEAD,'parents':manifest['original_commit_parents'],'files':files}))
if __name__=='__main__':main()

