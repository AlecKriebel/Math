#!/usr/bin/env python3
"""Seal completed review evidence; refuses an incomplete mathematical replay."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,sys,platform
base=Path(__file__).parent
paper=base.parent.parent
now=datetime.now(timezone.utc).isoformat()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
log=(base/'full_replay.log').read_text()
assert log.rstrip().endswith('VERIFIED: certificate bundle mode=full')
assert 'VERIFIED: all exact mathematical gates (full)' in log
assert '"relations": 269730' in log and '"maximum_probe_port_count": 10' in log
commitment=json.loads((base/'full_replay_commitment.json').read_text())
assert commitment['reviews/compact_probe_clean_clone_gate/certificates/compact_only_semantic_replay.json']=='e0238102b9577c82bda683bbeb07f4e77cb183503aa0b5b8598b85a094711cae'
source=json.loads((base/'source_binding.json').read_text())
for asset in source['assets']:
 p=Path(asset['path']);assert sha(p)==asset['sha256'] and p.stat().st_size==asset['bytes']
fresh={}
for name in ['fresh_sharpness','fresh_supports','fresh_omega_symbolic','fresh_theta','fresh_cut_algebra','fresh_boundary_control','fresh_factor_control']:
 result=json.loads((base/(name+'.json')).read_text());assert result['status']=='PASS'
 fresh[name]={'program':name+'.py','program_sha256':sha(base/(name+'.py')),'result':name+'.json','result_sha256':sha(base/(name+'.json')),'scope':result.get('scope',result.get('method')),'check_count':result.get('check_count',result.get('count',len(result.get('checks',[]))))}
read=(base/'PROOF_REVIEW.md').read_text()
body='## Exact target and boundaries'+read.split('## Exact target and boundaries',1)[1]
body=body.replace('That finite dependency is being replayed.','That finite dependency passed the complete exact replay described above.')
body=body.replace('the full replay remains necessary for those links','the completed full replay supplies the separately checked graph-binding and exhaustive-universe links')
intro=f'''# Independent adversarial review — Zenodo 22089373 v1.1.7

**Verdict: PASS for the exact printed mathematical scope.** Completed {now}; review completion 100%. No substantive mathematical defect or unresolved load-bearing gap was identified. This disposition combines the complete written proof review, fresh independent controls, primary theorem-interface checks, and an exit-code-zero replay of every committed exact mathematical gate. It is an AI-assisted review, not journal peer review or proof-assistant certification.

The strongest reviewed conclusion is the paper's source-open containment classification and generic topology recovery modulo ordinary triangle redirection within its fixed simple binary STC level-2 strict-JC class, together with the explicit all-n weak-class Omega and Theta common-germ counterexample families. This does not assert equality of complete stochastic images, recovery against all weak competitors, boundary validity, optimal statistical reconstruction, universal failure of each non-STC topology, or priority.

## Identity and completed verification

- Main [Zenodo record](https://zenodo.org/records/22089373): 33 pages; SHA256 `ae01c6beba01da624bba7060e9f3adfce74a5e568e5808f4db168300d7873084`.
- Reader supplement: all seven pages; SHA256 `bffe44178c93bbcac2f8cfd70f4b6fc45c61723bac7007d1aad2284ad5be78d7`.
- Main source ZIP SHA256 `e01d8277ceccb3b44f741578217da74f0dd1e70adc5b39beb85d69e4f0a6b36a`.
- The [published companion bundle](https://zenodo.org/records/22064121) tar archive SHA256 is `ffcce5398c8be387d6d808620fc939490f31ac41fb48592e22608cf0e7b05db4`. All 14 public assets across the two records were size/MD5/SHA-bound, then rehashed unchanged after replay; the identical main/reader PDFs occur in both records.

`full_replay.log` records the completed command through `verifiers/run_gate.py full`, exit code 0. The final line is `VERIFIED: certificate bundle mode=full`; all 241 active payload files passed the final integrity gate. The generated `full_replay_commitment.json` was copied before the verifier's automatic temporary-directory cleanup, SHA256 `{sha(base/'full_replay_commitment.json')}`. Its capture receipt records the exact source and time. The run used Python {platform.python_version()}, mpmath1.3.0, networkx3.2.1 and sympy1.14.0. The initial executable-mode extraction failure and its archive-header-only correction in the private copy are disclosed below; no mathematical payload was repaired.

The replay regenerated the balanced-word palette (808,642 configurations and 379,742 valid reduced presentations), 77 endpoint tensors and 72 one-active tensors with no failures, the 10,826-raw/10,466-canonical n3 universe and its full directed-relation evidence, and the 192 raw theta2 presentations with their canonical transports. The separate n3 base referee checked 225 exact symbolic bodies. The n4 all-record audit covered 132 roots and 2,106 states with zero failures; its separate referee additionally checked 44 symbolic samples. These latter samples are not substituted for the all-record audit.

Direct-anchor closure passed all 62 anchors, 2,642 one-port and 18,224 two-port extensions, including exact transports and all 12 mutation tests. The all-family compact semantic replay passed 276 paths and **269,730 relations**, with maximum 10 ports; its nine mutation tests passed. The base-only n4 status deliberately says `probe_extension_status: UNRESOLVED`; the separate completed direct-anchor and all-family compact gates close that dependency. The strict common-triangle point/rank gate, Theta, Omega producer, independent Omega replay and exact core-rank readability gate all passed. This was one complete `full` run, not the separate two-pass `regenerate-all` release mode.

Fresh code written for this review supplies distinct controls:

| Evidence | Independently checked scope |
|---|---|
| `fresh_sharpness.py/json` | 265 exact Omega point, Fourier/probability, rank, rooting and nonisomorphism checks |
| `fresh_supports.py/json` | All 12 printed strong supports and 100 admissible rootings |
| `fresh_omega_symbolic.py/json` | 79 checks: 64 symbolic correspondence coordinates, exact core rank six and 14 Euler identities |
| `fresh_theta.py/json` | 210 checks: universal equations, quadratic-field common point, both determinants, strict physical root gauge, and five admissible rootings, two tree-child |
| `fresh_cut_algebra.py/json` | 25 independent cut-minor, elimination-identity and incidence-anchor controls |
| `fresh_boundary_control.py/json` | All three strict-point quartet ranks 16 versus excluded-boundary ranks 4 |
| `fresh_factor_control.py/json` | All 27 stored strict polynomial products and 309 factors checked by independent exact Bernstein arithmetic; separate full replay supplies graph binding |

Every manuscript/supplement page was read. No current sibling or dedicated historical reviewer conclusion was read before this disposition. Raw primary sources were shared for acquisition efficiency only. Incidental historical statuses in required manuscript/capsule/code metadata were not treated as proof. All original sources remained unchanged. No website, spreadsheet, Git, DOI or outreach action was taken. No follow-up question is proposed.

'''
(base/'REVIEW.md').write_text(intro+body)
with (base/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+now+' — 100%: Full mathematical replay and final authenticated payload integrity completed with exit code 0. Compact closure passed all 276 paths / 269,730 relations at maximum 10 ports, followed by mutation, triangle and both sharpness gates. Generated commitment retained; all 14 public asset hashes rechecked unchanged. Complete adversarial verdict PASS for exact printed scope; no substantive gap found. Standard import/access, AI/formal, no-whole-image-equality and no-priority limits retained. No publication or external mutation performed.\n')
artifacts={}
for p in sorted(base.iterdir()):
 if p.is_file() and p.name not in ['evidence.json','verdict.json']:
  artifacts[p.name]={'bytes':p.stat().st_size,'sha256':sha(p)}
evidence={'schema':'independent-review-evidence-v1','record_id':'22089373','completed_utc':now,'reviewer_role':'adversarial','post_replay_public_assets_unchanged':True,'public_assets':source['assets'],'fresh_controls':fresh,'full_replay':{'exit_code':0,'mode':'full','final_line':log.rstrip().splitlines()[-1],'log_sha256':sha(base/'full_replay.log'),'commitment_sha256':sha(base/'full_replay_commitment.json'),'generated_commitments':commitment,'source_code_unmodified':True,'original_assets_unmodified':True,'double_regenerate_all_run':False},'artifacts':artifacts}
(base/'evidence.json').write_text(json.dumps(evidence,indent=2)+'\n')
verdict={'schema':'independent-adversarial-review-v1','record_id':'22089373','inventory_row':53,'version':'1.1.7','reviewer_role':'adversarial','verdict':'PASS','completed_utc':now,'completion_percent':100,'paper_sha256':'ae01c6beba01da624bba7060e9f3adfce74a5e568e5808f4db168300d7873084','source_zip_sha256':'e01d8277ceccb3b44f741578217da74f0dd1e70adc5b39beb85d69e4f0a6b36a','main_pages_read':33,'additional_reader_pdfs':[{'filename':'Strong_Tree_Childness_Sharp_Level2_JC_supplement.pdf','pages_read':7,'sha256':'bffe44178c93bbcac2f8cfd70f4b6fc45c61723bac7007d1aad2284ad5be78d7'}],'companion_record_id':'22064121','companion_archive_sha256':'ffcce5398c8be387d6d808620fc939490f31ac41fb48592e22608cf0e7b05db4','public_asset_identity_verified':True,'public_assets':source['assets'],'mathematical_clearance_scope':'Theorem1.1 and Corollary1.2 for the defined simple binary, LSA-valid, one-step reticulation-preserving fixed-sd0 STC level-2 class with JC multipliers and inheritance probabilities strictly in (0,1), uniform root, source-relative regular open-image containment; generic topology recovery within that class modulo ordinary triangle redirection. Theorem1.3 Omega and Theorem9.3 Theta all-n>=4 weak-but-not-strong common-regular-germ families with dimensions 2n+1 and 2n respectively.','strongest_verified_result':'The complete printed containment/generic-identifiability theorem and both sharpness mechanisms survived independent proof review, fresh exact symbolic/combinatorial controls and complete authenticated full certificate replay.','substantive_defects':[],'exact_remaining_gap':None,'proof_mechanisms_verified':['Fixed-mixed-graph convention and all-admissible-rooting strong criterion','Primitive core/minimum repair and independent incoming-port reduction','Pointwise cut theorem with exact endpoint/minor dependencies','Full incidence fibre, physical local product chart and source-open localization','Semialgebraic finite-cover and marginal open-image argument','Decorated finite relation universes, graph-to-polynomial binding, strict signs and canonical transports','Fixed-full restoration and coherent one-/two-port reconstruction','Strict triangle common germ, contextual contraction and simultaneous physical gluing','Generic exceptional-set dimension argument','Omega/Theta exact full-germ rank mechanisms and cherry continuation'], 'fresh_controls':fresh,'published_replay':evidence['full_replay'],'runtime_adjustment':{'issue':'Safe extraction normalized executable file modes, causing initial integrity gate rejection before mathematics.','resolution':'Copied authenticated archive bytes into ignored private replay cache and restored archive-header executable bits there only.','receipt':'extraction-mode-receipt.json','mathematical_payload_repaired':False},'independence':{'sibling_review_conclusions_read':False,'dedicated_historical_reviewer_opinions_read':False,'incidental_exposure':'Historical status statements in required manuscript, capsule and code/certificate metadata. Prior tasks exposed distinct K3P/K2P editions, whose conclusions were not imported.','fresh_controls_before_supplied_mathematical_helpers':'Initial graph/Fourier/support and symbolic sharpness controls were written before opening the submitted mathematical helper implementations; later independent cut/factor/boundary/gauge checks are separately labelled.','strict_blind_human_review_claim':False},'primary_reference_receipt':'primary_interfaces.json','follow_up':None,'review_sha256':sha(base/'REVIEW.md'),'evidence_sha256':sha(base/'evidence.json'),'artifacts':artifacts,'limits':['AI-assisted mathematical review, not journal peer review or a proof-assistant formalization.','External primary papers checked at the relevant theorem interfaces, not reproved in full. The full BCR book body was unavailable; standard semialgebraic dimension/Tarski–Seidenberg and differential rank facts are accepted imports. Official Coste full-PDF fetch timed out; indexed author-source statements were visible.','One complete full replay was run; two-pass regenerate-all release regeneration was not run.','No equality of entire stochastic images, validity at boundary/negative JC multipliers, recovery against arbitrary weak competitors, higher-level or richer-model theorem, every-non-STC failure, finite-sample guarantee or priority claim.','No sibling conclusions were used; incidental required-support statuses and different-edition knowledge are disclosed.'],'mutations':{'original_sources':'unchanged','website':'none','spreadsheet':'none','git':'none','zenodo':'none','outreach':'none'}}
(base/'verdict.json').write_text(json.dumps(verdict,indent=2)+'\n')
print(json.dumps({'verdict':'PASS','review_sha256':sha(base/'REVIEW.md'),'verdict_sha256':sha(base/'verdict.json'),'evidence_sha256':sha(base/'evidence.json'),'full_log_sha256':sha(base/'full_replay.log')},indent=2))
