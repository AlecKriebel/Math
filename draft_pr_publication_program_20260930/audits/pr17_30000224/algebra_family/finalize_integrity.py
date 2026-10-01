#!/usr/bin/env python3
"""Validate immutable receipts, then bind final family artifacts and sources."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import subprocess
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
EVIDENCE=HERE/'evidence'
SOURCE=HERE.parent/'source_snapshot'
FROZEN='dae2b77074945443e1b91c92f641ff9feff12235'
digest=lambda path:hashlib.sha256(path.read_bytes()).hexdigest()
seal=json.loads((EVIDENCE/'first_pass_seal.json').read_text())
for name,expected in seal['hashes'].items():
    assert digest(HERE/name)==expected, ('sealed artifact changed',name)
manifest=json.loads((HERE.parent/'snapshot_manifest.json').read_text())
assert manifest['head']==FROZEN
byname={row['path']:row for row in manifest['files']}
source_records=[]
for path in sorted(SOURCE.iterdir()):
    if not path.is_file():
        continue
    # Leave historical conclusions unopened even after the independent seal.
    if path.name in ('REVIEW.md','review_summary.json'):
        continue
    expected=byname[path.name]
    assert digest(path)==expected['sha256']
    spec=FROZEN+':unsolved_math_prioritization/attempts/30000224/'+path.name
    run=subprocess.run(['git','cat-file','blob',spec],cwd=ROOT,capture_output=True)
    assert run.returncode==0, (path.name,run.stderr.decode())
    assert hashlib.sha256(run.stdout).hexdigest()==expected['sha256']
    source_records.append({'path':str(path.relative_to(ROOT)),
                           'sha256':expected['sha256'],'git_blob':expected['git_blob'],
                           'frozen_commit_bytes_match':True})
author=json.loads((EVIDENCE/'author_reproduction.json').read_text())
assert author['exit_code']==0 and author['receipt']['assertions']==135
assert author['receipt_matches_frozen'] and author['frozen_files_unchanged']
probes=json.loads((EVIDENCE/'exact_probe_results.json').read_text())
assert probes['status']=='passed' and probes['assertions']==10351
assert probes['script_sha256']==digest(HERE/'exact_probes.py')
mutations=json.loads((EVIDENCE/'author_mutation_results.json').read_text())
assert len(mutations['records'])==5
assert all(r['failure_detected'] and not r['receipt_written'] for r in mutations['records'])
receipt=json.loads((EVIDENCE/'primary_source_receipts.json').read_text())
for source in receipt['records']:
    assert source['status']=='retrieved'
    assert digest(HERE/source['pdf'])==source['pdf_sha256']
    assert digest(HERE/source['text'])==source['text_sha256']
branch=subprocess.run(['git','branch','--show-current'],cwd=ROOT,capture_output=True,text=True,check=True).stdout.strip()
assert branch=='main', branch
now=datetime.now(timezone.utc).isoformat()
verdict={'completed_at_utc':now,'audit_completion_percent':100,
         'target':'30000224 / OWR-824-008','pr':17,'frozen_head':FROZEN,
         'verdict':'pass: algebraic partial obstructions; geometry conclusions conditional',
         'fatal_findings':[],
         'actionable_clarifications':['retain unrestricted original ideal scope',
                                     'label all Koszul depths/projective dimensions at m',
                                     'keep positive defect distinct from nonpositive criterion',
                                     'geometry acceptance requires its separate independent family',
                                     'generic length one excluded without homogeneity; do not extend length-two bound'],
         'strongest_verified':['no binomial CM thickening over any characteristic-zero K',
                               'H1_m(A)=K(-1) and not seminormal at vertex',
                               'Koszul depth H1=0, Z1=3, B1=1, Z2=2; pdim Z2=2 at m',
                               '2025 source-ideal shortcut fails under all generator padding',
                               'q-contained algebra reduction forces symbolic power and homogeneity'],
         'exact_gap':'non-binomial a-primary b with nonzero nilpotent q; homogeneous length>=3 only conditional on geometry; unrestricted nonhomogeneous class unresolved',
         'original_problem_status':'unsolved / partial-stalled','original_attempts_used':4,
         'original_attempt_budget':5,'new_attempt_consumed':False,
         'new_priority_claim':False,'paper_or_deposit_created':False,
         'author_assertions_reproduced':135,'new_exact_probe_assertions':10351,
         'new_probe_groups':len(probes['records']),'author_mutations_rejected':5,
         'independence_seal':str((EVIDENCE/'first_pass_seal.json').relative_to(HERE)),
         'historical_and_other_family_conclusions_read':False,
         'git_branch':branch,'git_mutations_by_family':False,
         'canonical_or_environment_mutations_by_family':False,'external_contacts':False}
(HERE/'VERDICT.json').write_text(json.dumps(verdict,indent=2)+'\n')
with (HERE/'RESEARCH_LOG.md').open('a') as log:
    log.write('\n- '+now+' — 100% algebra audit complete. Independent sealed artifacts\n'
              '  remain unchanged, all frozen snapshot bytes match their exact PR-head Git\n'
              '  objects, author135 reproduction and 10,351 distinct exact probes pass,\n'
              '  all five author mutations are rejected, and nine primary-source loci pass.\n'
              '  Relevant PDF pages were rendered and visually inspected. Final verdict:\n'
              '  algebraic partial results pass; geometric conclusions conditional. Original\n'
              '  arbitrary-ideal question remains unsolved with 4/5 original attempts; no new\n'
              '  attempt, publication, deposit, priority claim, or mutation outside this\n'
              '  folder. Main branch retained. No external contacts.\n')
visual_pages=['hass_theorem-02.png','hass_theorem-03.png','hass_sd-22.png',
              'mss_criteria-16.png','mss_criteria-17.png','mss_seminormal-14.png',
              'sw_target-08.png','owr_target-44.png','es_laurent-13.png','es_laurent-14.png']
visual={'checked_at_utc':now,'method':'rendered with pdftoppm; inspected using view_image',
        'pages':[{'path':'tmp/pdfs/'+p,'sha256':digest(HERE/'tmp'/'pdfs'/p)} for p in visual_pages]}
(EVIDENCE/'visual_inspection.json').write_text(json.dumps(visual,indent=2)+'\n')
artifact_records=[]
for path in sorted(HERE.rglob('*')):
    if path.is_file() and 'tmp' not in path.relative_to(HERE).parts and path.name!='HASH_LEDGER.json':
        artifact_records.append({'path':str(path.relative_to(HERE)),'sha256':digest(path),'bytes':path.stat().st_size})
ledger={'completed_at_utc':now,'frozen_head':FROZEN,
        'first_pass_seal_valid':True,'frozen_commit_bytes_match':True,
        'self_hash_policy':'ledger excludes its own hash to avoid circularity',
        'source_snapshot':source_records,'family_artifacts':artifact_records,
        'primary_downloads':receipt['records'],'visual_page_records':visual['pages']}
(HERE/'HASH_LEDGER.json').write_text(json.dumps(ledger,indent=2)+'\n')
print(json.dumps({'verdict':verdict['verdict'],'completion_percent':100,
                  'first_pass_seal_valid':True,'frozen_files_matched':len(source_records),
                  'artifact_hashes':len(artifact_records),'main_branch_retained':branch=='main'},indent=2))
