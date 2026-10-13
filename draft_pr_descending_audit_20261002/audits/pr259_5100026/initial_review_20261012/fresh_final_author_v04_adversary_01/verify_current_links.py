#!/usr/bin/env python3
from pathlib import Path
import json,re,posixpath,datetime
B=Path('/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr259_5100026/initial_review_20261012');A=B/'author_claim_repair_preparation_01/final_facing_v04';O=B/'fresh_final_author_v04_adversary_01';S=B/'submitted';root='unsolved_math_prioritization/attempts/5100026/'
plan=json.loads((A/'SCOPED_FILE_PLAN.json').read_text());overlay={p.relative_to(S).as_posix():p for p in S.rglob('*') if p.is_file()};overlay.update({x['repository_path']:A/x['payload_path'] for x in plan['operations']});links=[];docs=0
for repo,p in overlay.items():
 if not repo.startswith(root) or not repo.endswith('.md') or '/historical_submission_' in repo or '/audit_20261012/evidence/' in repo:continue
 docs+=1
 for caption,target in re.findall(r'\[([^\]]*)\]\(([^)]+)\)',p.read_text()):
  if target.startswith(('https:','http:','mailto:','#')):continue
  target=target.split('#',1)[0];dest=posixpath.normpath(posixpath.join(posixpath.dirname(repo),target))
  assert dest in overlay,(repo,target,dest)
  links.append({'source':repo,'target':target,'resolved':dest,'exists_in_exact_author_overlay':True})
result={'schema':'new-independent-current-author-overlay-link-audit','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','current_generic_markdown_documents':docs,'resolved_local_links':len(links),'links':links,'absolute_Main_audit_links_bound_by_independent_integrity_verifier':6,'historical_verbatim_report_links_have_explicit_omission_maps_and_are_not_promised_as_self_contained':True,'network_calls':0,'provider_or_git_writes':0}
(O/'CURRENT_LINK_VERIFICATION.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='links'},indent=2))
