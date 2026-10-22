#!/usr/bin/env python3
"""Truthfully repair the eligible PR's live description; no acceptance/merge."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,subprocess
P=Path(__file__).resolve().parent
A=P/'audits/pr909_30001345'
ROOT=P.parent
HEAD='d186dea31791cd3e8acf6829e0b65d01849623b8'
def run(args):return subprocess.run(args,cwd=ROOT,text=True,capture_output=True,check=True).stdout
def require(x,label):
 if not x:raise RuntimeError(label)
def main():
 before=json.loads(run(['gh','pr','view','909','--repo','AlecKriebel/Math','--json','number,state,isDraft,headRefOid,baseRefName,title,body,url']))
 require(before['state']=='OPEN' and before['isDraft'] is True and before['headRefOid']==HEAD and before['baseRefName']=='main','Live eligible draft/head changed')
 run(['git','fetch','--no-write-fetch-head','origin',HEAD])
 queue=run(['git','show',HEAD+':unsolved_math_prioritization/QUEUE.md'])
 rows=[l for l in queue.splitlines() if l.startswith('|') and len(l.split('|'))>8 and l.split('|')[2].strip().split(' / ')[0]=='30001345']
 require(len(rows)==1 and rows[0].split('|')[8].strip()=='claimed_solved','Immutable-head status not exactly claimed_solved')
 receipt=A/'PR_DESCRIPTION_REPAIR.json'
 require(not receipt.exists(),'Repair already recorded; inspect instead of repeating')
 (A/'PR_DESCRIPTION_BEFORE_REPAIR.json').write_text(json.dumps(before,indent=2)+'\n')
 body='''## Result and exact scope

The original28-file packet at d186dea31791cd3e8acf6829e0b65d01849623b8 proves an explicit reduced flat multibranch delta-constant family with finite simultaneous normalization and a common transverse ball. Its ordinary-nine central point has delta36 and rough K(K+D)=7; every sufficiently small nonzero complex fiber has twelve ordinary triples with summed delta36 and summed rough12. The original classical Fermat extension gives rough excess n²−4 for every integer n>=3, by the written structural argument rather than a finite test range.

This is a negative answer only to the unrestricted literal **summed** reading of Borodzik's2009 Oberwolfach rough-invariant Questions2–3 (printed2446–2447). The question does not literally display a sum; the following fixed-ball discussion supports that reading. It is not a marked-section result and does not settle the explicitly unibranched parametric Conjecture3.8 in the2014 published paper. No unstated author intention is asserted.

## Priority repair

The geometry and deformation method are classical. De Jong–van Straten1998, Definition4.2 and Example6.6 (pp476,503–504), use the exact nine-line/twelve-triple configuration in the delta-constant picture-deformation framework. Plamenevskaya–Starkston2023, Definition2.7 and Example8.7 (pp1109,1194), explicitly provide the simultaneous-normalization setting and constant-term scaling to a pencil. Borodzik2014 p578 already uses contraction to an ordinary multiple point and its rough value r−2. The complete corollary bridge and all local hypotheses have now been checked. The all-n Fermat geometry is also classical, as in Hirzebruch1983 p119.

A proposed note therefore presents an **explicitly attributed classical corollary and formulation clarification**, with no construction/method novelty, first-priority, or present-openness claim. The inspected sources did not establish an earlier literal statement of the exact7-to12 rough-M comparison; that gap establishes neither firstness nor a claim that the1998 paper already stated this theorem. The scoped mathematics is valid; its exact historical-priority status remains bounded by the documented searches.

Primary sources: [2009 report](https://doi.org/10.4171/OWR/2009/43), [Borodzik2014](https://doi.org/10.18910/50809), [de Jong–van Straten1998](https://doi.org/10.1215/S0012-7094-98-09513-8), [Plamenevskaya–Starkston2023](https://doi.org/10.2140/gt.2023.27.1083), [Hirzebruch1983](https://doi.org/10.1007/978-1-4757-9286-7_7).

## Verification and publication status

Four separate construction, invariant, computation and source/model audit families passed the exact scoped theorem. Two distinct deep priority audits and a fresh independent disposition adversary identified the prior construction/method and the limits above. A four-page note and supporting archive are being prepared for the required sequential fresh full-package adversarial reviews; this description update does not imply final acceptance, merge or publication.

All28 historical files, original packet manifest a8376fa67c497c4b31522364ac87163cdd6f5ec42961893981c44f0d95f0ee02, and original proof561b189c2091eaeccccf89fdd933b2300ec676a871d7229ebfaf8c806962fe8b remain unchanged. The historical recovery label is **1 verified/5; earlier attempt count unavailable**; no complete earlier author-search history is invented and audits add no author proof-search turn.

Release replay uses a separate externally anchored closed-inventory verifier and isolated nonoptimized checker execution, while preserving the historical guards/results. Exact computations supplement the analytic proof and do not certify priority or universal analytic claims by sampling. Raw third-party bodies are excluded. AI tools have been used extensively in research, verification, adversarial review and writing. Independent AI-assisted review is not independent human or journal peer review. The proposed preprint is unrefereed.
'''
 title='30001345: attributed multibranch rough-M counterexample; claimed_solved'
 path=A/'PR_DESCRIPTION_CORRECTED.md';path.write_text(body)
 run(['gh','pr','edit','909','--repo','AlecKriebel/Math','--title',title,'--body-file',str(path)])
 after=json.loads(run(['gh','pr','view','909','--repo','AlecKriebel/Math','--json','state,isDraft,headRefOid,baseRefName,title,body,url']))
 require(after['body']==body and after['title']==title and after['headRefOid']==HEAD and after['state']=='OPEN' and after['isDraft'] is True,'Exact live readback failed')
 data={'utc':datetime.now(timezone.utc).isoformat(),'pr':909,'original_head':HEAD,'eligibility_status':'claimed_solved','queue_row':rows[0],'previous_body_sha256':hashlib.sha256(before['body'].encode()).hexdigest(),'corrected_body_sha256':hashlib.sha256(body.encode()).hexdigest(),'corrected_title':title,'exact_live_readback':True,'head_unchanged':True,'no_math_or_original_packet_changed':True,'acceptance_merge_publication_performed':False}
 receipt.write_text(json.dumps(data,indent=2)+'\n');print(json.dumps(data,indent=2))
if __name__=='__main__':main()
