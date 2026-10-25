#!/usr/bin/env python3
"""Bind this review to public bytes and retained/fresh primary provenance."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json

HERE=Path(__file__).resolve().parent
PAPER=HERE.parents[1]
SRC=PAPER/'sources'
PACKAGE=SRC/'published-source/dfc_stability_verification/dfc_stability_verification'
PRIMARY=HERE.parent/'scope/cache/primary-sources'
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def bind(path):
    return {'path':str(path),'bytes':path.stat().st_size,'sha256':sha(path)}
def write(name,value): (HERE/name).write_text(json.dumps(value,indent=2)+'\n')
def main():
    now=datetime.now(timezone.utc).isoformat()
    receipt=json.loads((SRC/'receipt.json').read_text())
    assets=[]
    for item in receipt['files']:
        p=SRC/item['name']; b=bind(p); b['md5']=hashlib.md5(p.read_bytes()).hexdigest()
        assert b['bytes']==item['bytes'] and b['sha256']==item['sha256'] and b['md5']==item['md5']
        b.update({'url':item['url'],'matches_fresh_receipt':True}); assets.append(b)
    assert sha(SRC/'record.json')==receipt['record_sha256']
    assert (PACKAGE/'paper.pdf').read_bytes()==(SRC/'dfc_stability.pdf').read_bytes()
    build=json.loads((PACKAGE/'BUILD_RECEIPT.json').read_text())
    assert sha(PACKAGE/'main.tex')==build['source_sha256']
    replay=json.loads((HERE/'replay-results.json').read_text())
    current={str(p.relative_to(PACKAGE)):sha(p) for p in sorted(PACKAGE.rglob('*')) if p.is_file()}
    assert current==replay['source_sha256']
    coverage={
      'nre-0910.5577v1.pdf':('Definition of continuous-time stability and full Section 3.2/Figure 2, including opposite Conjecture 3.4.','Exact generator/model definition; different conjecture direction.'),
      'owr-2010-48.pdf':('Complete Norros contribution, printed pages 2782–2783.','Fresh public historical stochastic-stability conjecture; unstable ODE distinction.'),
      'nre-2011-retained-authorproof.pdf':('Cover/internal date; Section 3.2, Figure 2, explanatory text and Conjecture 3.6, printed pp.10–12.','Same six-rate chain and later stability direction. Retained author proof, not final publisher body or fresh download.'),
      'meyn-tweedie-III.pdf':('Section 4.1, CD2 and Theorems 4.1–4.3, printed pp.528–530.','Nonexplosive right process, closed petite set and bounded V on set; constant drift does not assert population moments. Manuscript gives direct countable-state argument.'),
      'oguz-allerton-2012-retained.pdf':('Entire retained five-page paper, printed pp.915–919, including Section II/III protocol, Section IV operative proof and final rare-chunk conjecture.','Different Common Chunk kernel. No independent full reproof of its theorem is claimed or needed; it is not imported to prove DFC recurrence.'),
      'oguz-technical-report-2012.pdf':('Bibliographic/title and introduction/model context, especially Chapter 3.1 and neighboring overview.','Related fresh technical-report source only; not substituted for conference or later journal editions; not full-body review.'),
    }
    all_receipts=[]; receipt_bindings=[]
    for name in ('receipt-initial.json','receipt-second.json','receipt-third.json','receipt-retained.json'):
        rp=PRIMARY/name
        if rp.exists():
            receipt_bindings.append(bind(rp)); data=json.loads(rp.read_text())
            assert isinstance(data,list)
            all_receipts.extend(data)
    rows=[]
    for name,(read,used) in coverage.items():
        p=PRIMARY/name
        matching=[r for r in all_receipts if r.get('filename')==name and r.get('sha256')==sha(p)]
        assert matching,name
        rec=matching[-1]
        row=bind(p); row.update({'reading_coverage':read,'interface_used':used,'acquisition':rec})
        txt=p.with_suffix('.txt')
        if txt.exists(): row['text_extraction']=bind(txt)
        rows.append(row)
    write('primary-reading-ledger.json',{'created_utc':now,'raw_source_only':True,
        'sibling_findings_read':False,'sources':rows,'acquisition_receipt_bindings':receipt_bindings,
        'access_limits':'Final 2011 publisher PDF and final 2015 journal extension not inspected; retained 2011 author-proof and 2012 conference bytes are not newly publicly authenticated. No exhaustive priority/open-status certificate.'})
    with (HERE/'RESEARCH_LOG.md').open('a') as f:
        f.write('\n- 2026-10-25 02:45 UTC — 75%: Fresh rational controls completed successfully on 12,693 states before packaged helper reading. Read complete necessary TURN_4 mathematical proof and then selected current-proof controls. Incidental author completion/status sentences and README historical test summaries were encountered; no dedicated old judgment bodies were opened or used. Selected unmodified replays completed in isolation and matched their expected outputs, with the false protocol identity rejected.\n')
        f.write('- 2026-10-25 02:47 UTC — 95%: Completed full independent proof notes and reviewed exact primary interfaces, with explicit retained-versus-fresh provenance. No substantive gap found for the six-rate, fixed-real-positive-load theorem. Historical priority remains unestablished. All source hashes remain unchanged; report and final bindings prepared.\n')
        f.write(f'- {now} — 100%: Final analytic report, source/primary/control evidence bindings and scoped PASS verdict complete. Strongest result: exact model is nonexplosive, irreducible and positive recurrent for every fixed real lambda>0, with a unique stationary probability. No mathematical gap identified. No uniform-load, stationary moment, other-protocol, human-peer-review or novelty certification. No repair or publication action taken.\n')
    evidence_names=['REVIEW.md','RESEARCH_LOG.md','paper.txt','fresh_controls.py','fresh-control-results.json',
       'fresh-controls.stdout.txt','fresh-controls.stderr.txt','replay_selected.py','replay-results.json',
       'replay-driver.stdout.txt','replay-driver.stderr.txt','primary-reading-ledger.json','finalize_evidence.py']
    evidence_names += sorted(p.name for p in HERE.glob('replay-*.stdout.txt') if p.name!='replay-driver.stdout.txt')
    evidence_names += sorted(p.name for p in HERE.glob('replay-*.stderr.txt') if p.name!='replay-driver.stderr.txt')
    evidence={'created_utc':now,'record_id':'23524971','public_assets':assets,
              'source_receipt':bind(SRC/'receipt.json'),'record':bind(SRC/'record.json'),
              'reader_pdf_map':bind(SRC/'reader-pdf-map.json'),'embedded_pdf_identical':True,
              'main_tex':bind(PACKAGE/'main.tex'),'original_mathematical_proof':bind(PACKAGE/'original/TURN_4.md'),
              'build_receipt':bind(PACKAGE/'BUILD_RECEIPT.json'),
              'source_file_count':len(current),'all_source_files_unchanged':True,
              'artifacts':[bind(HERE/name) for name in evidence_names],
              'historical_assessment_bodies_used':False,'complete_package_reproduction_claimed':False}
    write('evidence.json',evidence)
    verdict={'record_id':'23524971','review_role':'independent analytic','completed_utc':now,
        'completion_percent':100,'verdict':'PASS','verdict_scope':'Exact mathematical Theorem 1; not publication clearance or novelty certification.',
        'title':'All-load stability of a deterministic-first-chunk file-sharing chain','version':'1.0','manuscript_date':'2026-10-20',
        'pdf_sha256':'bee5abffcfdb1ce8bc50f706480c81c4a80e8d609bec2a9d99c6aa4e9b805036',
        'zip_sha256':'38664f12e8d2e74fa46b3f11363a071ec100aad62ece713b578293a6593d9a0e',
        'exact_checked_claims':[
            'Six-state-increment CTMC on N0^4, exact equation (1) rates, independent uniform first-choice arrivals, permanent seed, invisible empty waiting rooms, immediate completed departures.',
            'Every fixed real lambda>0: nonexplosion, irreducibility, positive recurrence and unique stationary probability, from every finite initial state.',
            'Global rounded imbalance bound, reflected finite Poisson equation with terminal equation at R, monotone cutoff interfaces and exhaustive exterior drift bound LV<=-1.',
            'Localized continuous-time Dynkin hitting-time bound and finite-mean regeneration; no assumed stationary averaging or population moment.',
            'Small-load workload consequence lambda<1/2, exact source-version distinction and Common Chunk kernel nonidentity.'
        ],
        'strongest_verified_result':'For each fixed real lambda>0 the exact six-rate chain in equation (1) is nonexplosive, irreducible and positive recurrent, hence has one stationary probability; a single coercive Foster function and a finite-mean continuous-time regeneration argument establish the claim.',
        'substantive_defects':[], 'mathematical_gaps':[],
        'exact_remaining_gap':'No identified mathematical gap for the stated theorem. Independent human peer review/formal verification and comprehensive priority verification were not performed; retained primary edition and final-body access limits are preserved.',
        'scope_exclusions':['lambda=0 irreducibility','aggregate seed upload cap','visible waiting rooms or other protocols','uniform-in-lambda bound','finite stationary population moment','geometric ergodicity','quantitative delay bound','worldwide novelty or continuing-open status'],
        'fresh_controls':{'loads':['1/8','1','3'],'states':12693,'poisson_states':317,'outside_F_states':1062,'all_assertions_passed':True,'universal_proof':False},
        'published_replay':{'isolated':True,'unmodified':True,'positive_output_matches':4,'intentional_rejection':1,'complete_package_launcher_run':False,'source_files_unchanged':92},
        'independence':{'sibling_reports_read':False,'dedicated_historical_assessment_bodies_read':False,
                        'incidental_exposure':'TURN_4 author candidate/completion statements and README historical control/review summaries; not used to determine validity. Historical files hashed as opaque bytes by integrity/control programs.'},
        'report':bind(HERE/'REVIEW.md'),'evidence':bind(HERE/'evidence.json'),'research_log':bind(HERE/'RESEARCH_LOG.md'),
        'review_type':'AI review; not human peer review; no publication action or source repair.'}
    write('verdict.json',verdict)
    print(json.dumps({'report':bind(HERE/'REVIEW.md'),'verdict':bind(HERE/'verdict.json'),'evidence':bind(HERE/'evidence.json'),'verdict_status':'PASS','source_files_unchanged':len(current)},indent=2))
if __name__=='__main__': main()
