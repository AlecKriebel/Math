"""Finalize the bounded review; no external mutations."""
from pathlib import Path
import collections,datetime as dt,hashlib,json,os,re,subprocess,sys
Q=Path(__file__).resolve().parent;R=Q.parent.parent;REPO=R.parent
def now():return dt.datetime.now(dt.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def save(rel,obj):
 p=Q/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,indent=2)+'\n')
def require(ok,msg):
 if not ok:raise RuntimeError(msg)
initial=json.loads((Q/'private/initial_live_wire.json').read_text())['data']['repository']
query='query { repository(owner:"AlecKriebel",name:"Math") {'+' '.join(f'p{n}:pullRequest(number:{n}){{number title body state isDraft mergedAt updatedAt headRefOid baseRefOid mergeCommit{{oid}}}}' for n in range(628,672))+'} }'
wire=subprocess.run(['gh','api','--hostname','github.com','graphql','--input','-'],input=json.dumps({'query':query}).encode(),cwd=REPO,capture_output=True,check=True).stdout;(Q/'private/final_live_wire.json').write_bytes(wire);live=json.loads(wire);require('errors' not in live,'final provider error');changed=[]
for n in range(628,672):
 delta=[k for k in live['data']['repository'][f'p{n}'] if live['data']['repository'][f'p{n}'][k]!=initial[f'p{n}'][k]]
 if delta:changed.append(dict(pr=n,fields=delta))
canonical_changed=[]
for n in range(628,672):
 name=f'PR{n:04d}_DISPOSITION.json'
 if (R/name).read_bytes()!=(Q/'private/inputs'/name).read_bytes():canonical_changed.append(n)
statebytes=(R/'STATE.json').read_bytes();state=json.loads(statebytes);(Q/'private/final_STATE.json').write_bytes(statebytes);inventorybytes=(R/'rest_inventory.json').read_bytes();inventory=json.loads(inventorybytes);(Q/'private/final_rest_inventory.json').write_bytes(inventorybytes)
current=R/'COVERAGE_SNAPSHOT.json';b=current.read_bytes();(Q/'private/final_COVERAGE_SNAPSHOT.json').write_bytes(b)
save('final_live_recheck.json',dict(at=now(),count=44,live_wire_sha256=sha(wire),changed_processed_prs=changed,changed_canonical_dispositions=canonical_changed,initial_next_pr=json.loads((Q/'private/inputs/STATE.json').read_text())['next_pr'],final_next_pr=state['next_pr'],final_last_completely_processed=state['last_completely_processed_pr'],final_highest_observed=state['highest_observed_pr'],final_inventory_highest=inventory['highest_pr'],final_state_sha256=sha(statebytes),final_inventory_sha256=sha(inventorybytes),scope='Dated start/end comparison only; later canonical cursor progress is legitimate and outside bounded range.'))
require(not changed and not canonical_changed,'root reconciliation required')
initialmanifest=json.loads((Q/'INPUT_MANIFEST.json').read_text());rechecked=[];mutable=[]
for entry in initialmanifest['files']:
 src=Path(entry['source']);current_digest=sha(src.read_bytes());same=current_digest==entry['sha256']
 rechecked.append(dict(path=entry['path'],captured_sha256=entry['sha256'],source_current_sha256=current_digest,unchanged=same))
 if not same:mutable.append(entry['source'])
save('final_input_recheck.json',dict(at=now(),files=rechecked,source_changes=mutable,scope='Captured receipts never updated to follow canonical advancement. Changed global STATE/journal/inventory/coverage may be legitimate; individual processed dispositions and sealed review evidence must remain bound.'))
allowed={str(R/x) for x in ['STATE.json','dispositions.jsonl','rest_inventory.json','COVERAGE_SNAPSHOT.json']};require(set(mutable)<=allowed,'sealed review or scoped source changed')
# Independent semantic distinctions, based on actual full metadata and full publication texts read.
save('semantic_dedup_assessment.json',dict(at=now(),fresh_ledger=dict(rows=178,columns=4,pr662_unique_row=94,pr628_exact_identity_rows=[],pr630_exact_identity_rows=[]),ledger_hurwitz_lead=dict(row=13,record=23124601,reason='Fixed positive Artin words in Wajnryb A5 quotient and strict Hurwitz equivalence; no arithmetic Hurwitz-space descent bound.'),captured_account=dict(total_unique=197,positive_control=23174283,independent_identity_search_no_628_630=True,fresh_authenticated_account_fetch=False,scope='Both captured complete authenticated account files agree byte for byte; receipt/count/identity independently checked. Account-universe completeness is bounded by root capture, not newly certified.'),pr628_distinct_account_leads=[dict(record=23444093,reason='Long prime/unit graph clique equality.'),dict(record=23430927,reason='Positive surface boundary-twist factorizations.'),dict(record=23124601,reason='Wajnryb Artin A5 positive words.'),dict(record=22729355,reason='Hurwitz-stable Turing matrices, unrelated use of Hurwitz.')],pr630_distinct_account_lead=dict(record=23441167,reason='Polynomial multipliers of differentiation-hypercyclic entire functions; no IM shared value or prescribed higher derivative implication.'),pr662_identity='Original2306086/AMR0226086/Hayman-Lingham6.86; real-coefficient normalized schlicht functions; qualitative strict fixed nonreal pre-Schwarzian bound, uniform in f and on compact nonreal sets; real-diameter4 sharp; original expression at0 zero.',no_stronger_claim='Neither DOI description, complete paper/source, controlling scope nor own QUEUE row claims explicit upper gap, sharp numerical radius, general extremizers/full variability, certified numerical proof, firstness or present openness.',source_limits=['Jenkins1960 and Aleksandrov-Popova1973 original-source overlap unresolved in existing public package.','No new scientific proof/priority certification is supplied by this coverage review.','Explicit nonclaimed rows were skipped entirely after binding; their proof/audit bodies were not used to elevate scope.']))
assess=json.loads((Q/'per_pr_assessments.json').read_text())
for a in assess:
 n=a['pr']
 if n==628:a.update(outcome='RETAIN_PRIORITY_HOLD',reason='Two materially distinct fresh family reports plus root acceptance bind exact target.13+47 seal payloads verified;36originals unchanged;full15-J certificate replay agrees after execution UTC only; custody restoration disclosed. No new mechanism/full-target novelty clearance established.',evidence=['hold_custody_checks.json','fresh_primary_source_receipts.json'])
 elif n==630:a.update(outcome='RETAIN_PRIORITY_HOLD',reason='Source-first71-file seal and root replays bind exact literal universal claim.28originals unchanged;2009 quadratic B=2b directly meets target at a=0,k=2;independent normal/optimized controls reproduce. Refinement firstness and stronger restrictions remain unclaimed.',evidence=['hold_custody_checks.json','fresh_primary_source_receipts.json'])
 elif n==662:a.update(outcome='RETAIN_EXISTING_PUBLICATION_SKIP',reason='Actual merge first-parent46path scope, all24immutable originals and merged paper/source/scope agree with freshpublic DOI23384924/PDF/ZIP101members100positivepayloads and uniquefreshGWSrow94. No newpublication or quantitative radius claim.',evidence=['publication_integrity_checks.json','special_662_comparison_check.json','ledger_fresh_receipt.json'])
 else:a.update(outcome='SKIP_ENTIRELY_EXPLICIT_NONCLAIMED',reason='Exactly one own added QUEUE row matches problem ID and complete pinned own-attempt scope. Explicit status governs; no body-driven elevation or substantive science review.',evidence=['pinned_scope_checks.json','pinned_blob_values.json'])
save('per_pr_assessments.json',assess)
log=json.loads((Q/'RESEARCH_LOG.json').read_text());log.append(dict(at=now(),completion_estimate_percent=95,event='Final live44metadata and processed dispositions unchanged. Fresh public source scope and semantic duplicate leads reconciled; writing bounded findings and final seal.'));save('RESEARCH_LOG.json',log)
print(json.dumps(dict(changed_processed_prs=changed,changed_dispositions=canonical_changed,changed_global_sources=mutable,final_next_pr=state['next_pr'],final_highest=inventory['highest_pr'])))
