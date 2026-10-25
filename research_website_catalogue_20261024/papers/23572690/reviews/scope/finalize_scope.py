"""Source custody and editorial validation only; no deposited program execution."""
from pathlib import Path
import datetime, hashlib, json, re, subprocess, zipfile

HERE=Path(__file__).resolve().parent
BASE=HERE.parents[1]
S=BASE/'sources'
P=S/'published-source/bv-generators-source-and-verification'
NOW=datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,obj): (HERE/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
r=json.loads((S/'receipt.json').read_text()); m=json.loads((S/'record.json').read_text())
members=json.loads((S/'extraction-integrity.json').read_text())['members']
assert m['metadata']['version']=='1.0.0' and m['metadata']['publication_date']=='2026-10-22'
assert sha(S/'record.json')==r['record_sha256']
assert len(r['files'])==2 and len(members)==12
for f in r['files']:
 b=(S/f['name']).read_bytes()
 assert len(b)==f['bytes'] and hashlib.sha256(b).hexdigest()==f['sha256'] and hashlib.md5(b).hexdigest()==f['md5']
with zipfile.ZipFile(S/'bv-generators-source-and-verification.zip') as z:
 assert z.testzip() is None
 for f in members:
  b=(S/f['path']).read_bytes()
  assert len(b)==f['bytes'] and hashlib.sha256(b).hexdigest()==f['sha256']
  assert z.read(f['member'])==b
manifest=json.loads((P/'source-manifest.json').read_text())
assert len({f['path'] for f in manifest['files']})==len(manifest['files'])
assert {f['path'] for f in manifest['files']}|{'source-manifest.json'}=={p.relative_to(P).as_posix() for p in P.rglob('*') if p.is_file()}
for f in manifest['files']:
 assert sha(P/f['path'])==f['sha256'] and (P/f['path']).stat().st_size==f['bytes']
assert sha(P/'paper.pdf')==sha(S/'bv-generators.pdf')
save('custody-final.json',{'utc':NOW,'status':'PASS_INTEGRITY_ONLY','public_assets_checked':2,'extracted_members_checked':12,'package_manifest_entries_checked':len(manifest['files']),'duplicate_reader_identical':True,'mathematical_programs_executed':False,'original_files_mutated':False})

tex=(P/'main.tex').read_text()
abstract_tex=re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}',tex,re.S).group(1).strip()
(HERE/'abstract.tex.txt').write_text(abstract_tex+'\n')
mapping={r'\(k\)':'k',r'\(0\ne h\in k[x]\)':'0≠h∈k[x]',r'\(A_h=k\langle x,Y\rangle/(Yx-xY-h(x))\)':'A_h=k⟨x,Y⟩/(Yx−xY−h(x))',r'\(h\)':'h','--':'–','~':' '}
abstract=abstract_tex
for old,new in mapping.items(): abstract=abstract.replace(old,new)
abstract=re.sub(r'\s+',' ',abstract).strip()
assert '\\' not in abstract
binding={'record_id':'23572690','pdf_sha256':sha(S/'bv-generators.pdf'),'receipt':'sources/receipt.json','receipt_sha256':sha(S/'receipt.json'),'metadata_sha256':sha(S/'record.json'),'all_public_assets':[{'filename':f['name'],'sha256':f['sha256'],'bytes':f['bytes']} for f in r['files']],'embedded_assets':[]}
content={
 'title':'BV generators for polynomial Weyl subalgebras',
 'slug':'bv-generators-polynomial-weyl-subalgebras',
 'description':'A characteristic-zero classification of when the canonical Hochschild cohomology of a polynomial Weyl subalgebra admits a Batalin–Vilkovisky generator.',
 'abstract':abstract,
 'plain_language':[
  'Hochschild cohomology packages information about an algebra and its possible deformations. It comes with both a product and a bracket. A Batalin–Vilkovisky, or BV, generator is a single operator that recovers the bracket from the product and whose square is zero.',
  'This paper considers a family of algebras governed by one polynomial h. Its proposed classification is simple to state: a BV generator exists exactly when h has no repeated irreducible factor. Nonzero constant polynomials are included in the positive case.',
  'The negative case is stronger than failure to find a suitable formula. A repeated factor produces cohomology classes whose product is zero but whose bracket is nonzero. Together with a central annihilating class, these relations rule out every degree-minus-one bracket generator, even if its square is not required to vanish.',
 ],
 'result':[
  'For any characteristic-zero field k and nonzero h∈k[x], let A_h=k⟨x,Y⟩/(Yx−xY−h(x)). Theorem 1 states that h being squarefree, the canonical Gerstenhaber bracket on ordinary HH•(A_h,A_h) being zero, existence of a bracket generator, and existence of a BV generator are equivalent.',
  'For squarefree h, the zero operator is a BV generator. If h has a repeated irreducible factor over k, no bracket generator exists. The argument works over the original field and does not require the polynomial to split into linear factors.',
 ],
 'why_it_works':[
  'Published results describe the algebra’s resolution and derivations. The paper compares that resolution with normalized bars to identify the canonical cup product needed for the obstruction.',
  'When d=gcd(h,h′) is nonconstant, a central degree-one class annihilates every other degree-one class under the cup product. This forces any possible bracket generator to vanish on degree one. An explicit cup-zero pair with nonzero bracket then gives a contradiction.',
  'When d=1, the second and higher cohomology groups vanish and the remaining degree-one derivations commute. The entire bracket is therefore zero.',
 ],
 'limitations':[
  'The classification concerns this one-variable polynomial family over fields of characteristic zero, with its ordinary Hochschild cohomology and canonical product and bracket. It does not classify arbitrary Weyl subalgebras, positive-characteristic cases, twisted-coefficient variants, or Poisson analogues.',
  'For h≠0, A_h is the subalgebra of the first Weyl algebra generated by x and yh(x). The literal embedded h=0 case instead gives k[x], which the paper treats separately using Δ(f∂x)=−f′. Setting h=0 in the abstract two-generator presentation gives a different algebra, k[x,Y].',
  'The result uses established resolution and derivation theorems. The accompanying finite exact computations support selected identities; they are not proof-assistant certification or a replacement for the universal argument.',
  'Earlier work already ruled out bracket generators for other ordinary Hochschild cohomology algebras. This paper claims a classification for the stated family, with bounded historical coverage, rather than the first nonexistence phenomenon. It makes no Jacobian- or Dixmier-conjecture claim.',
 ],
 'background':[
  {'title':'Lopes, with Solotar — Gerstenhaber algebra structure on Hochschild cohomology','url':'https://doi.org/10.4171/OWR/2023/46','note':'Question (2), printed page 2702, asks about BV structures for this family when its Nakayama automorphism is not semisimple. The workshop took place in 2023; the report was published in July 2024.'},
  {'title':'Lopes and Solotar — Lie structure on the Hochschild cohomology of a family of subalgebras of the Weyl algebra','url':'https://doi.org/10.4171/JNCG/439','note':'Provides the free resolution, characteristic-zero cohomology quotient, derivation structure and Nakayama automorphism used by the note.'},
  {'title':'Benkart, Lopes and Ondrus — Derivations of a parametric family of subalgebras of the Weyl algebra','url':'https://doi.org/10.1016/j.jalgebra.2014.11.007','note':'The established derivation and normalizer classification supplies the degree-one spanning description and center.'},
  {'title':'Herscovich and Li — Gerstenhaber structure on Hochschild cohomology of the Fomin–Kirillov algebra on 3 generators','url':'https://doi.org/10.4171/DM/X18','note':'Proposition 4.15 is an earlier ordinary-Hochschild no-generator result and a predecessor of the cup/bracket obstruction strategy.'},
  {'title':'Kowalzig and Krähmer — Batalin–Vilkovisky structures on Ext and Tor','url':'https://doi.org/10.1515/crelle-2012-0086','note':'Theorem 1.7 assumes a semisimple modular automorphism; this hypothesis cannot be silently dropped for the nonconstant-polynomial branch.'},
  {'title':'Bian, Itagaki, Kou, Lyu and Zhou — BV structures for self-injective Nakayama algebras','url':'https://arxiv.org/abs/2603.04834v2','note':'Theorem 7.11 treats truncated basic cycle algebras, a different family. Its Criterion 7.7 includes a commuting-odd-generators hypothesis.'},
 ],
 'collaboration':'I welcome substantive collaboration from researchers in Hochschild cohomology, noncommutative algebra and BV structures, particularly on checking the canonical cup-product comparison, refining the relation to earlier results, and developing a journal-ready treatment. Any coauthorship would reflect a substantive contribution to the research.',
 'follow_up':None,'followup_rationale':'No follow-up is proposed: this scope assignment has not established an unusually strong, independently justified paper-worthy question or conjecture.',
 'publication_date':'2026-10-22','version':'1.0.0','doi':'10.5281/zenodo.23572690','author':'Alec Kriebel',
 'pdf_filename':'bv-generators.pdf','supplement_filename':None,
 'additional_assets':[{'filename':'bv-generators-source-and-verification.zip','label':'Source and verification package (ZIP)'}],
 'status':'Unrefereed preprint',
 'ai_disclosure':'AI tools were used extensively in mathematical exploration, proof development, computation, literature research, manuscript preparation and adversarial auditing. Internal AI reviews do not constitute formal independent human peer review, journal acceptance or proof-assistant certification.',
 'source_binding':binding,'related_resources':[],'candidate_only':True,
 'candidate_gate':'Scope and attribution candidate only. Independent mathematical reviews and root publication approval remain required; no mathematical PASS is supplied here.',
}
save('content.json',content)
assert json.loads((HERE/'content.json').read_text())['abstract']==abstract
save('abstract-check.json',{'utc':NOW,'status':'PASS_SOURCE_FIDELITY_ONLY','source':str((P/'main.tex').relative_to(BASE)),'source_sha256':sha(P/'main.tex'),'complete_original_abstract':True,'paragraphs':1,'normalization_map':mapping,'whitespace_only_after_macro_replacement':True,'candidate_sha256':sha(HERE/'content.json')})
save('independence.json',{'role':'scope','mathematical_verdict':None,'historical_assessment_bodies_read':False,'sibling_findings_read':False,'opaque_files':['PRIORITY.md','CHECK_RESULTS.json'],'incidental_exposure':['Current manuscript/record contain author priority and historical-publication assertions.','DEPENDENCIES.md states historical source-reading claims; URLs were used as locators but all cited interfaces were newly read in primary bodies.','build_release.py contains frozen workflow/publication_ready prose and status-producing code; not adopted as a current verdict.'],'no_math_programs_executed':True,'no_unrelated_Keller_archive_imported':True})
primary=HERE/'cache/primary-sources'
rows=[]
for path in sorted(primary.glob('receipt-*.json')):
 for item in json.loads(path.read_text()):
  q=dict(item);q['receipt_file']=path.name
  if (primary/q['filename']).exists():
   q['sha256_rechecked']=sha(primary/q['filename'])
   info=subprocess.check_output(['pdfinfo',str(primary/q['filename'])],text=True)
   q['pages']=int(re.search(r'^Pages:\s+(\d+)',info,re.M).group(1))
  rows.append(q)
save('primary-references.json',{'utc':NOW,'retrievals':rows,'metadata_links':['https://ems.press/journals/jncg/articles/3731350','https://ems.press/journals/dm/articles/13131885','https://ems.press/journals/owr/articles/14298013','https://www.sciencedirect.com/science/article/pii/S0021869314006395','https://www.degruyterbrill.com/document/doi/10.1515/crelle-2012-0086/html']})
interfaces=[
 ('owr-2023-46.pdf','Complete Lopes contribution, printed2702–2703/PDF22–23','Exact characteristic-zero embedded-family Question(2); BV sign convention and separate Questions(1)/(3).','Fresh publisher report'),
 ('lopes-solotar-published.pdf','Proposition2.1; Section3 through Proposition3.9/Corollary3.11/Nakayama paragraph; Section6.1/Theorem6.2','Length-two resolution, HH2 quotient, higher vanishing, ambient basis, center and derivation spanning; characteristic-zero branch.','Fresh final publisher PDF; complete later homotopy/Virasoro classification not independently reconstructed'),
 ('benkart-lopes-ondrus-v2.pdf','Theorem4.9/Lemma4.11 and proofs; Theorems5.1/5.3/5.7; Lemma5.6; Proposition5.9/Theorem5.13 and proofs; Section5.5 conclusion','Derivation decomposition, normalizers, central degree-one classes, arbitrary characteristic-zero field, monic-radical versus scalar-normalized pi convention.','Fresh arXiv1406.1508v2, not final journal bytes; not every internal lemma or full48pp audited'),
 ('herscovich-li-published.pdf','Opening scope; complete Proposition4.15 and proof','Older FK(3) no bracket generator even without square-zero, characteristic different from2,3; direct predecessor credit, different finite-dimensional family.','Fresh final publisher PDF; entire structural table not independently recomputed'),
 ('kowalzig-krahmer-author.pdf','Theorem1.7; Sections7.3–7.4/Definition7.5 and proof interface','Twisted Calabi–Yau plus semisimple modular automorphism; ordinary cohomology through twisted-homology duality.','Fresh author manuscript, not asserted equivalent to final61pp publisher edition'),
 ('bian-etal-v2.pdf','Introductory scope; Criterion7.7 hypotheses/proof; Theorems7.8/7.11 and intervening example','Different truncated-basic-cycle family; criterion assumes zero mutual odd-generator bracket.','Fresh arXiv2603.04834v2; entire cohomology computation not re-audited'),
]
save('primary-interfaces.json',{'utc':NOW,'interfaces':[{'filename':a,'sha256':sha(primary/a),'read':b,'interface':c,'limits':d} for a,b,c,d in interfaces],'unresolved_primary_access':['Author HL URL failed TLS hostname validation; final publisher PDF succeeded instead.','Final publisher BLO/KK bodies not acquired; exact version-specific author bodies supplied the relevant interfaces.'],'scope_not_novelty_certification':True})
read={'main.tex':'complete current source','paper.pdf':'duplicate complete6page reader','DEPENDENCIES.md':'necessary named structural interfaces; historical reading claims not adopted','exact_checks.py':'complete finite diagnostic code read, not executed','build_release.py':'complete offline packaging code read, not executed','source-manifest.json':'integrity mapping only'}
save('support-map.json',{'utc':NOW,'files':[{'path':f['path'],'sha256':f['sha256'],'use':read.get(Path(f['path']).name,'mapped/hash-checked only; body opaque or unnecessary')} for f in members],'no_mathematical_execution':True})
with (HERE/'research-log.md').open('a') as f:f.write('\n- '+NOW+' — 100% of acquisition/scope: all6manuscript pages, full mathematical source and necessary support mapped; fresh primary question/structural/comparison interfaces read; complete original abstract and conditional candidate prepared. All2public assets/12extracted members/source manifest unchanged. No mathematical PASS or checker execution; independent mathematical reviews and root promotion gate remain.\n')
artifacts=[{'path':q.relative_to(HERE).as_posix(),'bytes':q.stat().st_size,'sha256':sha(q)} for q in sorted(HERE.rglob('*')) if q.is_file() and q.name not in {'artifact-manifest.json','verdict.json'}]
save('artifact-manifest.json',{'utc':NOW,'files':artifacts})
save('verdict.json',{
 'schema_version':1,'record_id':'23572690','doi':'10.5281/zenodo.23572690','role':'scope','status':'SCOPE_COMPLETE','mathematical_verdict':None,'publication_clearance':False,'completed_utc':NOW,'completion_percent':100,
 'source_binding':{'pdf_filename':'bv-generators.pdf','pdf_sha256':sha(S/'bv-generators.pdf'),'source_zip_filename':'bv-generators-source-and-verification.zip','source_zip_sha256':sha(S/'bv-generators-source-and-verification.zip'),'record_sha256':sha(S/'record.json'),'receipt_sha256':sha(S/'receipt.json'),'extraction_integrity_sha256':sha(S/'extraction-integrity.json'),'reader_map_sha256':sha(S/'reader-pdf-map.json'),'public_assets':r['files']},
 'coverage':{'current_manuscript_pages':6,'all_current_pages_read':True,'full_current_mathematical_source_read':True,'necessary_support_read':True,'distinct_reader_pdfs':1,'embedded_reader_identical':True,'mathematical_programs_executed':False,'historical_assessments_read':False,'sibling_findings_read':False,'unrelated_Keller_papers_imported':False},
 'strongest_scope_result':'Exact Zenodo edition/all assets authenticated; complete current proof scope and primary question/structural interfaces mapped; original full abstract and conditional candidate prepared.',
 'exact_scope':'Any characteristic-zero field; nonzero h in k[x]; ordinary canonical HH*(A_h,A_h); squarefree iff zero bracket iff any degree-minus-one generator iff BV generator. Embedded h=0 treated separately as k[x].',
 'remaining_gate':'Independent mathematical reviews and root assessment. This scope result does not certify theorem correctness, worldwide priority, or authorize publication.',
 'excluded_claims':['positive characteristic','arbitrary Weyl subalgebras','twisted-coefficient/modified-product variants','all Poisson analogues','unrelated Keller papers','Jacobian or Dixmier conjecture implications','identification of embedded h=0 with the abstract polynomial plane'],
 'primary_limits':['Fresh final LS/HL/OWR publisher bodies; fresh specific BLO/KK author bodies and BIKLZ v2.','Final publisher equivalence for BLO/KK not independently authenticated.','Not all internal proofs of imported structural theorems rederived; finite checks do not replace them.'],
 'candidate':{'file':'content.json','sha256':sha(HERE/'content.json'),'candidate_only':True,'full_abstract_fidelity':'PASS_SOURCE_FIDELITY_ONLY','follow_up':None},
 'unchanged_originals':{'public_assets':2,'extracted_regular_files':12},
 'artifacts':{'report':'REVIEW.md','report_sha256':sha(HERE/'REVIEW.md'),'manifest':'artifact-manifest.json','manifest_sha256':sha(HERE/'artifact-manifest.json'),'primary_interfaces':'primary-interfaces.json','primary_interfaces_sha256':sha(HERE/'primary-interfaces.json'),'independence':'independence.json'},
})
print(json.dumps({'status':'SCOPE_COMPLETE','mathematical_verdict':None,'report_sha256':sha(HERE/'REVIEW.md'),'content_sha256':sha(HERE/'content.json'),'verdict_sha256':sha(HERE/'verdict.json'),'artifacts':len(artifacts)},indent=2))
