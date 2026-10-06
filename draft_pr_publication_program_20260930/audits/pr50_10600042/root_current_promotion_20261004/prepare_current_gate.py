"""Bind the current eligible PR to its original sources and fixed reviewed package."""
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import zipfile

if sys.flags.optimize:
    raise RuntimeError('Optimized assertions forbidden')
own=Path(__file__).resolve().parent
a50=own.parent
program=a50.parents[1]
repo=program.parent
head='7260315f8b8b193020c09d4ef6df9d943a3a13ff'
def sha(b): return hashlib.sha256(b).hexdigest()
def must(ok,msg):
    if not ok: raise RuntimeError(msg)
def git(*args):
    p=subprocess.run(['git','--no-replace-objects',*args],cwd=repo,capture_output=True)
    must(p.returncode==0,p.stderr.decode(errors='replace'))
    return p.stdout
pr_raw=(program/'audits/pr45_9900007/root_pr50_current_head_and_status_20261004_actual_capture/stdout.bin').read_bytes()
pr=json.loads(pr_raw)
must(pr['state']=='OPEN' and pr['isDraft'] is True and pr['headRefOid']==head and pr['baseRefName']=='main','PR is not the checked current draft')
q=git('show',head+':unsolved_math_prioritization/QUEUE.md')
rows=[r for r in q.decode().splitlines() if '| 10600042 /' in r]
must(len(rows)==1 and rows[0].split('|')[8].strip()=='claimed_solved' and rows[0].split('|')[9].strip()=='1/5','Not eligible at exact head')
manifest=json.loads((a50/'ORIGINAL_MANIFEST.json').read_bytes())
must(manifest['head']==head and manifest['files_count']==15,'Original source manifest differs')
originals=[]
for item in manifest['files']:
    blob=git('show',head+':'+item['original_git_path'])
    local=(a50/'original'/item['path']).read_bytes()
    must(blob==local and len(blob)==item['bytes'] and sha(blob)==item['sha256'],'Original source body drift: '+item['path'])
    originals.append({'path':item['original_git_path'],'bytes':len(blob),'sha256':sha(blob),'git_blob_sha1':item['git_blob_sha1']})
pins={
 'even_strand_markov.tex':'cd141a55da2241764d4fbbe8a145d8d4be29370803e24704e645c60cf8f2d0dc',
 'even_strand_markov.pdf':'ea3e6f6b647de0acd71219a2840ee515fe6548f7d4dbba828558b7fb0e01624e',
 'even-strand-markov-verification-v1.zip':'2b519b4ba59ccd2e5ed9c88a79aa96d273481b45bb18b6a1ecc6fcbd0381a48d',
 'zenodo-deposit.json':'4636f8b65dc2906097967a3fa963b0ae0fc652d645e2a5bcf17558c6f7493b82'}
package=a50/'publication_package_v1'
for name,h in pins.items(): must(sha((package/name).read_bytes())==h,'Final publication drift: '+name)
members=['LICENSE-CODE.txt','LICENSE-TEXT.md','README.md','SHA256SUMS','SOURCE_QUALIFICATIONS.md','VERIFICATION_RECORD.json','build_verification_zip.py','even_strand_markov.tex','expected_results.json','verify_even_calculus.py']
with zipfile.ZipFile(package/'even-strand-markov-verification-v1.zip') as z:
    must(z.namelist()==members and z.testzip() is None,'ZIP topology or CRC')
    for name in members: must(z.read(name)==(package/name).read_bytes(),'Archived member differs: '+name)
reviews=[]
for family in ['preprint_v1_adversary_family','preprint_v1_second_adversary_family','submission_final_adversary_family']:
    path=a50/family/'VERDICT.json'
    body=path.read_bytes(); v=json.loads(body)
    if family=='preprint_v1_adversary_family':
        must(v['mathematical_review']=='PASS_NO_MANDATORY_ISSUES_FOUND' and v['editorial_scope_review']=='PASS_NO_MANDATORY_ISSUES_FOUND' and v['mandatory_issues']==[] and v['unresolved_proof_gaps_within_stated_scope']==[],'First historical review not clean')
        status=v['mathematical_review']
    else:
        status=v['status']
        must(status.startswith('PASS'),'Historical package verdict not PASS')
    reviews.append({'path':path.relative_to(repo).as_posix(),'sha256':sha(body),'status':status})
final=json.loads((a50/'submission_final_adversary_family/VERDICT.json').read_bytes())
must(final['final_artifact_sha256']==pins and final['mandatory_corrections']==[],'Final historical reviewed artifacts differ')
deposit=json.loads((package/'zenodo-deposit.json').read_bytes())
must(set(deposit)=={'metadata','files'} and deposit['metadata']['creators']==[{'name':'Kriebel, Alec','orcid':'0009-0001-9320-500X'}],'Metadata/creator differs')
must(deposit['files']==[{'path':'even_strand_markov.pdf','name':'even_strand_markov.pdf'},{'path':'even-strand-markov-verification-v1.zip','name':'even-strand-markov-verification-v1.zip'}],'Upload pair differs')
record={'schema':'pr50-current-preparation-binding/v1','UTC':dt.datetime.now(dt.timezone.utc).isoformat(),'actual_pid':os.getpid(),
 'status':'PASS_CURRENT_ELIGIBLE_HEAD_AND_UNCHANGED_FIXED_PACKAGE','head':head,'problem_id':'10600042','PR':50,
 'exact_submitted_status':'claimed_solved','original_budget':'1/5','new_central_attempts':0,
 'fresh_PR_readback_sha256':sha(pr_raw),'exact_head_queue_sha256':sha(q),'exact_target_queue_row':rows[0],
 'all_fifteen_originals_fresh_exact_head_reconciled':originals,'publication_pins':pins,'historical_three_package_reviews':reviews,
 'root_all_four_final_pdf_pages_personally_viewed_again':True,'new_current_promotion_adversary_pending':True,
 'concrete_1996_Nencka_priority_lead_under_investigation':True,
 'current_publication_approval':False,'DOI':None,'tracker_written':False,'merge_completed':False,
 'mathematical_review_estimate_percent':95,'PR50_full_workflow_percent':0,'whole_goal_complete':False}
(own/'CURRENT_PREPARATION_BINDING.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2))
