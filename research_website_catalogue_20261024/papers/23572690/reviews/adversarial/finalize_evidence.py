#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
HERE=Path(__file__).resolve().parent;PAPER=HERE.parents[1];SRC=PAPER/'sources'
PKG=SRC/'published-source/bv-generators-source-and-verification'
PRIMARY=HERE.parent/'scope/cache/primary-sources'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def bind(p):return {'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p)}
def write(name,obj):(HERE/name).write_text(json.dumps(obj,indent=2)+'\n')
def main():
    now=datetime.now(timezone.utc).isoformat();receipt=json.loads((SRC/'receipt.json').read_text())
    assets=[]
    for row in receipt['files']:
        p=SRC/row['name'];b=bind(p);b['md5']=hashlib.md5(p.read_bytes()).hexdigest()
        assert b['bytes']==row['bytes'] and b['sha256']==row['sha256'] and b['md5']==row['md5']
        b.update({'url':row['url'],'matches_fresh_public_receipt':True});assets.append(b)
    assert sha(SRC/'record.json')==receipt['record_sha256']
    assert (PKG/'paper.pdf').read_bytes()==(SRC/'bv-generators.pdf').read_bytes()
    replay=json.loads((HERE/'replay-results.json').read_text())
    current={str(p.relative_to(PKG)):sha(p) for p in sorted(PKG.rglob('*')) if p.is_file()}
    assert current==replay['source_sha256']
    custody={'record_id':'23572690','created_utc':now,'assets':assets,'record':bind(SRC/'record.json'),
        'acquisition_receipt':bind(SRC/'receipt.json'),'reader_pdf_map':bind(SRC/'reader-pdf-map.json'),
        'extraction_integrity':bind(SRC/'extraction-integrity.json'),'embedded_pdf_identical':True,
        'source_file_count':len(current),'source_sha256':current,'all_source_files_unchanged':True,
        'source_manifest':bind(PKG/'source-manifest.json'),
        'meaningfully_read_source_bodies':['main.tex','DEPENDENCIES.md','README.md','exact_checks.py','CHECK_RESULTS.json'],
        'excluded_opinion_body':'PRIORITY.md not read; its bytes hashed only for manifest custody.'}
    write('source-custody.json',custody)
    coverage={
       'lopes-solotar-published.pdf':('Publisher PDF','Proposition 2.1; complete Section 3 resolution/differentials; Proposition 3.9 proof and Corollary 3.11; Nakayama paragraph; Section 6.1 and Theorem 6.2.','Load-bearing resolution, quotient, higher vanishing, basis and derivation interfaces. Exactness is a published input; full contracting-homotopy/positive-characteristic/Virasoro analyses not independently reproved.'),
       'benkart-lopes-ondrus-v2.pdf':('Author manuscript arXiv v2, not publisher-final bytes','Lemma 2.13; Theorem 2.17 and characteristic-zero proof; Proposition 3.1 and proof; Theorem 4.9 and Lemma 4.11; Theorems 5.3/5.7 and proofs, Proposition 5.9 and proof, Theorem 5.13 and proof.','Load-bearing characteristic-zero arbitrary-field spanning, normalizers, scalar convention, localization and innerness.'),
       'owr-2023-46.pdf':('Publisher PDF','Complete Lopes–Solotar contribution, printed pp.2702–2703.','Exact original embedded-family question and generator convention; other general/Poisson questions kept separate.'),
       'kowalzig-krahmer-author.pdf':('Author-host manuscript','Application context and Theorem 1.7.','Semisimplicity restriction and ordinary cohomology versus twisted homology; background only, no import to the nonsemisimple classification.'),
       'herscovich-li-published.pdf':('Publisher PDF','Proposition 4.15 and complete proof, pp.1802–1803.','Earlier no-generator obstruction without square-zero for FK(3); distinct family.'),
       'bian-etal-v2.pdf':('Author preprint v2','Criterion 7.7 statement and relevant proof setup; Theorem 7.11 statement and scope.','Commuting odd-generator premise and truncated basic-cycle family; no full preprint theorem reproof claimed.'),
    }
    raw=[];receipts=[]
    for name in ['receipt-initial.json','receipt-second.json','receipt-third.json']:
        p=PRIMARY/name;receipts.append(bind(p));raw.extend(json.loads(p.read_text()))
    rows=[]
    for name,(edition,read,scope) in coverage.items():
        p=PRIMARY/name;b=bind(p)
        records=[r for r in raw if r.get('filename')==name and r.get('sha256')==b['sha256']]
        assert records,name
        b.update({'edition':edition,'reading_coverage':read,'interface':scope,'acquisition':records[-1],
                  'text_extraction':bind(p.with_suffix('.txt'))});rows.append(b)
    write('primary-reading-ledger.json',{'created_utc':now,'sources':rows,'receipt_bindings':receipts,
        'sibling_findings_read':False,'primary_sources_only':True,
        'limits':'Exact primary interfaces checked, not complete reconstruction of all cited articles or exhaustive historical novelty determination.'})
    with (HERE/'RESEARCH_LOG.md').open('a') as f:
        f.write('\n- 2026-10-25 02:52 UTC — 75%: Corrected fresh harness completed 631 exact assertions across twelve polynomials, including rational multiples and nonsplit repeated factors, normalized-bar comparisons, centrality primitives and embedded-zero signs. Only after that completion, read the packaged checker and ran it unmodified in isolation with ordinary and -OO flags; both outputs were byte-identical to CHECK_RESULTS.json. All twelve source hashes unchanged.\n')
        f.write('- 2026-10-25 02:53 UTC — 90%: Completed the manuscript proof/interface audit and exact primary theorem readings. No substantive defect found. All four nonzero-h equivalences, the separate embedded-zero case and the characteristic-zero field scope are supported. Author-manuscript versus publisher editions retained explicitly. No sibling findings or PRIORITY.md read.\n')
        f.write(f'- {now} — 100%: Sealed full report, source custody, primary/evidence bindings and scoped PASS verdict. Strongest result: ordinary canonical Hochschild BV/bracket generators exist exactly for squarefree nonzero h over any characteristic-zero field; repeated factors forbid every generator. No mathematical gap identified. No repair, publication action or historical priority certificate.\n')
    names=['REVIEW.md','RESEARCH_LOG.md','paper.txt','fresh_weyl_controls.py','fresh-control-results.json',
           'fresh-controls.stdout.txt','fresh-controls.stderr.txt','fresh-controls-attempt1.py',
           'fresh-controls-attempt1.stdout.txt','fresh-controls-attempt1.stderr.txt','replay_published.py',
           'replay-results.json','replay-driver.stdout.txt','replay-driver.stderr.txt','replay-ordinary.stdout.txt',
           'replay-ordinary.stderr.txt','replay-optimized.stdout.txt','replay-optimized.stderr.txt',
           'source-custody.json','primary-reading-ledger.json','finalize_evidence.py']
    evidence={'record_id':'23572690','created_utc':now,'objective':bind(PAPER.parents[1]/'GOAL.md'),
        'source_custody':bind(HERE/'source-custody.json'),'primary_ledger':bind(HERE/'primary-reading-ledger.json'),
        'artifacts':[bind(HERE/name) for name in names],'no_sibling_or_historical_opinions_used':True,
        'no_public_source_edits':True,'fresh_checks_before_helper_reading':True}
    write('evidence.json',evidence)
    verdict={'record_id':'23572690','role':'independent adversarial','completed_utc':now,'completion_percent':100,
        'verdict':'PASS','title':'BV generators for polynomial Weyl subalgebras','version':'1.0.0','publication_date':'2026-10-22',
        'pdf_sha256':'2c344b0baff06088f04f4468bd8f6365405e879f7004b169055aebedbdecd4e7',
        'zip_sha256':'a7ab72e55fd0952d363f78f92bc418b9f1331ccefb1f75eaea8dda32868601e6',
        'verdict_scope':'Exact ordinary-Hochschild characteristic-zero classification and separate literal embedded h=0 statement; not publication clearance, formal verification or novelty certification.',
        'exact_checked_claims':[
            'For every characteristic-zero field and nonzero h, squarefree h iff zero canonical Gerstenhaber bracket iff degree-minus-one bracket generator iff square-zero BV generator.',
            'Units included; nonmonic scalar multiples and repeated irreducibles over the base field require no splitting-field assumption.',
            'Canonical normalized-bar cup comparison [D_f] cup [E] = [f E(x)] in HH2=A/dA; correct right factors and constant/linear relation terms.',
            'c=[D_d] is a nonzero central annihilator with independent companion when d!=1; this forces every putative generator to vanish on HH1.',
            'Repeated-factor pair is cup-zero with nonzero commutator class [D_(h u_prime/u^2)], obstructing all generators without square-zero.',
            'Literal embedded h=0 is k[x] with negative-divergence BV generator; abstract h=0 two-generator algebra is a different polynomial plane.',
            'Nonconstant h yields the specified nonsemisimple Nakayama map; no unstated application of a semisimplicity theorem.'
        ],
        'strongest_verified_result':'For any characteristic-zero field and nonzero polynomial h, ordinary canonical HH*(A_h) has a BV or even bracket generator exactly when h is squarefree. Repeated factors forbid every generator. The separate embedded h=0 line has the stated negative-divergence BV operator.',
        'substantive_defects':[],'mathematical_gaps':[],
        'exact_remaining_gap':'No identified gap at the stated hypotheses with the authenticated published/author-primary structural interfaces. No proof-assistant or human peer review and no exhaustive priority determination.',
        'primary_dependencies':'Lopes–Solotar free resolution and cohomology quotient; Benkart–Lopes–Ondrus derivation/normalizer classification, checked at characteristic-zero arbitrary-field scope. Full cited articles not independently reproved.',
        'scope_exclusions':['positive characteristic','h=0 included in the nonzero abstract-presentation classification','twisted-coefficient replacement for ordinary HH','general Gerstenhaber or Poisson classification','Keller/Jacobian/Dixmier/etale implications','worldwide firstness or current openness'],
        'fresh_controls':{'assertions':631,'polynomial_parameters':12,'normalizer_primitives':96,'generator_linear_rank':3,'generator_augmented_rank':4,'all_final_checks_passed':True,
                         'initial_harness_error':'Preserved first attempt used expression modulo for characteristic-three reduction; corrected own harness only. No paper defect inferred.'},
        'replay':{'unmodified_isolated_runs':2,'ordinary_and_optimized_byte_identical':True,'source_files_unchanged':12,'package_builder_run':False},
        'independence':{'sibling_reports_read':False,'historical_assessment_bodies_read':False,'PRIORITY_md_read':False,
                        'incidental_exposure':'Author source-reading and status statements in the mandatory manuscript, dependency notes and README, not used in lieu of mathematical checks.'},
        'report':bind(HERE/'REVIEW.md'),'evidence':bind(HERE/'evidence.json'),'source_custody':bind(HERE/'source-custody.json'),
        'research_log':bind(HERE/'RESEARCH_LOG.md'),'review_type':'AI adversarial mathematical review, not human peer review or publication clearance.'}
    write('verdict.json',verdict)
    for b in evidence['artifacts']:
        p=Path(b['path']);assert p.stat().st_size==b['bytes'] and sha(p)==b['sha256']
    print(json.dumps({'status':'PASS','report':bind(HERE/'REVIEW.md'),'verdict':bind(HERE/'verdict.json'),
                     'evidence':bind(HERE/'evidence.json'),'source_custody':bind(HERE/'source-custody.json')},indent=2))
if __name__=='__main__':main()
