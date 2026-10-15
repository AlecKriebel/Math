#!/usr/bin/env python3
"""Bind review candidate to exact local artifacts and live eligible PR head."""
import argparse,hashlib,json,subprocess
from datetime import datetime,timezone
from pathlib import Path
HERE=Path(__file__).resolve().parent;A=HERE.parent;R=HERE.parents[3]
HEAD='330a544a53b9e3e01bb0ed70817a5f4a79cc6a0a'
def run(args):return subprocess.run(args,cwd=R,check=True,text=True,capture_output=True).stdout

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--revision',type=int,default=1);args=ap.parse_args()
 target=json.loads(run(['gh','pr','view','905','--repo','AlecKriebel/Math','--json','headRefOid,state,isDraft,url']))
 if target['headRefOid']!=HEAD or target['state']!='OPEN' or not target['isDraft']:raise RuntimeError('Live draft differs from reviewed eligible candidate')
 text=run(['gh','api','repos/AlecKriebel/Math/contents/unsolved_math_prioritization/QUEUE.md?ref='+HEAD,'-H','Accept: application/vnd.github.raw+json'])
 rows=[line for line in text.splitlines() if len(line.split('|'))>9 and line.split('|')[2].strip().startswith('30000717 /')]
 if len(rows)!=1 or rows[0].split('|')[8].strip()!='claimed_solved':raise RuntimeError('Exact claimed_solved gate failed')
 names=['note.tex','output/pdf/note.pdf','robinson-tangency-source-verification-v1.0.zip','zenodo-deposit.json','README.md','verify_package.py','requirements.txt','build_package.py']
 files={}
 for name in names:
  p=HERE/name
  if not p.is_file() or p.is_symlink():raise RuntimeError('Missing/nonregular candidate '+name)
  files[name]={'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 record={'utc':datetime.now(timezone.utc).isoformat(),'pr':905,'problem_id':'30000717','candidate_revision':args.revision,'reviewed_head':HEAD,'live_status':'OPEN draft claimed_solved','original_candidate_turns':'1/5 preserved','files':files,'package_manifest_sha256':json.loads((HERE/'PACKAGE_BUILD.json').read_text())['manifest_sha256'],'mathematical_gates':'PASS no universal proof gap for either explicit reading','priority':'Bounded audit; classical ingredients credited; first priority not asserted','next_gate':'Fresh sequential full-package adversarial reviews; not yet accepted for publication'}
 p=HERE/'PREPUBLICATION_FREEZE.json'
 if p.exists():raise RuntimeError('Preserve previous freeze before writing a new revision')
 p.write_text(json.dumps(record,indent=2)+'\n');(A/'PR_PREFLIGHT.json').write_text(json.dumps(target,indent=2)+'\n');print(json.dumps(record,indent=2))
if __name__=='__main__':main()
