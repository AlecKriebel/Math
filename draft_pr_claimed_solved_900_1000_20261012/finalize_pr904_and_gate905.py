from pathlib import Path
import json,subprocess,hashlib,tarfile,io,re
from datetime import datetime,timezone
P=Path(__file__).resolve().parent; R=P.parent; A=P/'audits/pr904_30000347'; now=datetime.now(timezone.utc).isoformat()
def run(args): return subprocess.run(args,cwd=R,check=True,text=True,capture_output=True).stdout
receipt=json.loads((A/'NATIVE_PUBLICATION_RECEIPT.json').read_text()); sha=receipt['commit']
q=run(['git','show',sha+':unsolved_math_prioritization/QUEUE.md'])
lines=[line for line in q.splitlines() if re.match(r'^\|\s*\d+\s*\|\s*30000347\s*/',line)]
assert len(lines)==1 and lines[0].split('|')[8].strip()=='preprint_published' and '10.5281/zenodo.23331258' in lines[0]
st=json.loads(run(['git','show',sha+':unsolved_math_prioritization/state.json'])); assert st['30000347']['status']=='preprint_published' and st['30000347']['doi']=='10.5281/zenodo.23331258'
record={'utc':now,'pr':904,'problem_id':'30000347','outcome':'accepted_merged_preprint_published','original_pr_head':'d67d11bcb7d1e730daf9be7555c75950d3484b5d','merge_commit':'703e129726dd1110f1780aabbaba7d0d78f42728','doi':'10.5281/zenodo.23331258','record_url':'https://zenodo.org/records/23331258','tracker_range':"'Math Puzzles'!A68:D68",'native_ledger_commit':sha,'native_ledger_readback_confirmed':True,'original_turns_preserved':'1/5','priority_limit':'No first-priority assertion; classical ingredients explicitly credited','AI_and_peer_review':'Extensive AI assistance; unrefereed; no independent human peer review asserted'}
(A/'PUBLICATION_RECORD.json').write_text(json.dumps(record,indent=2)+'\n')
body='''The claimed solution is accepted and published after independent mathematical, source/model, computational and bounded priority audits. The unit-cost undirected three-terminal shortest-path blocking decision problem is NP-complete even when all original pairwise terminal distances are three; finite-distance and exact three-to-four variants are also established.

Preprint: **NP-completeness of three-terminal shortest-path blocking**, version 1.0, Alec Kriebel. DOI: [10.5281/zenodo.23331258](https://doi.org/10.5281/zenodo.23331258). The [Zenodo record](https://zenodo.org/records/23331258) includes the four-page note and its reproducible source/verification archive.

Three sequential full-package adversarial reviews were completed. A missing pair of promised citation-evidence records was repaired after the second review; the third review found no required repairs. Classical subdivision and spoke-attachment ingredients are credited to Poljak and Khachiyan et al. The bounded priority audit does not establish or assert first priority.

AI tools were used extensively in proof development and verification. The note is unrefereed; independent human or journal peer review is not claimed. Publication metadata and uploaded bytes were verified. The DOI was recorded and read back in the requested Math Puzzles tracker, row 68. The original candidate's 1/5 proof-attempt count is preserved.

Accepted immutable PR head: `d67d11bcb7d1e730daf9be7555c75950d3484b5d`. Audit and publication receipts: `draft_pr_claimed_solved_900_1000_20261012/audits/pr904_30000347/`.
'''
(A/'PR_PUBLISHED_BODY.md').write_text(body)
run(['gh','pr','edit','904','--repo','AlecKriebel/Math','--title','30000347: accepted three-terminal BSP NP-completeness and published preprint','--body-file',str(A/'PR_PUBLISHED_BODY.md')])
(A/'PR_PUBLISHED_METADATA.json').write_text(run(['gh','pr','view','904','--repo','AlecKriebel/Math','--json','number,title,body,state,mergedAt,mergeCommit,url']))
# Eligibility is resolved before any mathematical snapshot/read for the next PR.
r=json.loads(run(['gh','pr','view','905','--repo','AlecKriebel/Math','--json','number,title,state,isDraft,headRefOid,headRefName,url']))
content=run(['gh','api','repos/AlecKriebel/Math/contents/unsolved_math_prioritization/QUEUE.md?ref='+r['headRefOid'],'-H','Accept: application/vnd.github.raw+json'])
rows=[line for line in content.splitlines() if re.match(r'^\|\s*\d+\s*\|\s*30000717\s*/',line)]
assert len(rows)==1
r.update(problem_id='30000717',status=rows[0].split('|')[8].strip(),queue_row_sha256=hashlib.sha256(rows[0].encode()).hexdigest(),gate_utc=now)
r['eligible']=r['state']=='OPEN' and r['isDraft'] and r['status']=='claimed_solved'
B=P/'audits/pr905_30000717'; B.mkdir(parents=True,exist_ok=True); (B/'ELIGIBILITY_GATE.json').write_text(json.dumps(r,indent=2)+'\n')
if r['eligible']:
    run(['git','fetch','--no-write-fetch-head','origin',r['headRefOid']])
    out=B/'original'; out.mkdir(exist_ok=True)
    blob=subprocess.run(['git','archive',r['headRefOid'],'unsolved_math_prioritization/attempts/30000717'],cwd=R,check=True,capture_output=True).stdout
    with tarfile.open(fileobj=io.BytesIO(blob)) as tf: tf.extractall(out,filter='data')
    files={p.relative_to(out).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(out.rglob('*')) if p.is_file()}
    (B/'ORIGINAL_SNAPSHOT.json').write_text(json.dumps({'utc':now,'head':r['headRefOid'],'files':files},indent=2)+'\n')
    (B/'GATED_QUEUE_ROW.md').write_text(rows[0]+'\n')
state=json.loads((P/'CURRENT_STATE.json').read_text()); state.update(utc=now,active_pr=905 if r['eligible'] else None,active_problem_id='30000717' if r['eligible'] else None,completed_prs=[904],completed_results=[record],publication='PR904_published_tracker_and_ledger_verified',phase='PR905_independent_math_audit' if r['eligible'] else 'continue_status_gating',shard_completion_estimate_percent=100/12)
for key in ['mathematics_gates','priority_gate','fresh_full_package_reviews','candidate_revision','original_pr_head']: state.pop(key,None)
(P/'CURRENT_STATE.json').write_text(json.dumps(state,indent=2)+'\n')
readme=(P/'README.md').read_text().replace('No paper is accepted yet.','PR #904 is accepted, merged and published: [10.5281/zenodo.23331258](https://doi.org/10.5281/zenodo.23331258), tracker row 68. Its audited publication record is preserved in `audits/pr904_30000347/`.')
(P/'README.md').write_text(readme)
for dest in [P/'RESEARCH_LOG.md',A/'RESEARCH_LOG.md']:
    with dest.open('a') as f: f.write('\n## '+now+' — #904 completed; #905 eligibility rechecked\n\n#904 accepted and merged, exact reviewed Zenodo metadata and files published under DOI 10.5281/zenodo.23331258; tracker row 68 confirmed. Native publication ledger pushed and independently read back at '+sha+'. PR title/body updated to the factual published outcome. No other status or target processed. #905 live gate: '+str(r['eligible'])+'; exact proposed status '+r['status']+'.\n\nCompletion estimate: 100% of #904; 8.33% of 12 initially eligible shard dispositions/publications.\n')
inv=json.loads((P/'inventory.json').read_text())
for x in inv:
    if x['number']==904: x.update(disposition='accepted_merged_preprint_published',doi=record['doi'],tracker_range=record['tracker_range'])
(P/'inventory.json').write_text(json.dumps(inv,indent=2)+'\n')
print(json.dumps({'PR904':record,'PR905_gate':r},indent=2))
