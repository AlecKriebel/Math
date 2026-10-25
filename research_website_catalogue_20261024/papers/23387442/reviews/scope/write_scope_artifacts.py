from pathlib import Path
import datetime, hashlib, json, re

ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
SRC=ROOT/'sources'
ARCH=SRC/'published-source/satoh_filtration_verification'
NOW=datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def writej(name,x): (OUT/name).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
record=json.loads((SRC/'record.json').read_text())
receipt=json.loads((SRC/'receipt.json').read_text())
inventory=json.loads((SRC/'extraction-integrity.json').read_text())
primary=json.loads((OUT/'primary-source-receipts.json').read_text())
texpath=ARCH/'satoh_filtration_counterexamples.tex'
tex=texpath.read_text()
abstract_tex=re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}',tex,re.S).group(1).strip()
(OUT/'ABSTRACT.tex').write_text(abstract_tex+'\n')
abstract='Let A_n(k) be the integral Andreadakis filtration of the automorphism group of a free group, and let D_n(k) be the kernel of its action on J/J^{k+1} in the rational SL(2,ℂ) matrix-entry algebra at the trivial representation. We construct elements of D_n(5) \\ A_n(5) for every n≥4, and of D_n(6) \\ A_n(6) for every n≥3. Thus the equality in all degrees conjectured in Satoh’s 2018 report is false at every rank in its stated range. The construction uses a classical degree-five Lie identity, elementary free-group automorphisms, and integral Magnus coefficients. The proof works with actual powers of J, rather than only values along one-parameter representations.'
(OUT/'ABSTRACT.txt').write_text(abstract+'\n')
# Typography/whitespace-only normalization of the complete source abstract.
normalized=abstract_tex
for a,b in [('$',''),('\\SL','SL'),('\\C','ℂ'),('\\setminus',' \\ '),('\\geq','≥'),('Satoh\'s','Satoh’s')]: normalized=normalized.replace(a,b)
normalized=' '.join(normalized.split()).replace(' \\  ',' \\ ')
if normalized!=abstract:
 raise ValueError(('abstract transcription mismatch',normalized,abstract))
# Only byte-integrity and editorial metadata checks run here. No mathematical program is imported or executed.
for f in receipt['files']:
 p=SRC/f['name']
 if p.stat().st_size!=f['bytes'] or sha(p)!=f['sha256'] or hashlib.md5(p.read_bytes()).hexdigest()!=f['md5']: raise ValueError(f['name'])
for f in inventory['members']:
 p=Path(f['path'])
 if p.stat().st_size!=f['bytes'] or sha(p)!=f['sha256']: raise ValueError(f['member'])
for f in primary:
 p=OUT/'cache/primary-sources'/f['name']
 if p.stat().st_size!=f['bytes'] or sha(p)!=f['sha256']: raise ValueError(f['name'])
read_paths={
 'satoh_filtration_counterexamples.pdf':'Entire current four-page reader; duplicate of standalone public PDF.',
 'satoh_filtration_counterexamples.tex':'Entire current 285-line manuscript source, including exact abstract.',
 'native/unsolved_math_prioritization/attempts/30003703/release/PROOF.md':'Entire original mathematical proof support; historical assessment wording incidental and not adopted.',
 'native/unsolved_math_prioritization/attempts/30003703/release/verify.py':'Entire 192-line mathematical program body read; never executed or imported.',
 'reviews/freegroup_01/controls.py':'Entire 206-line unitriangular mathematical control body read; never executed or imported.',
 'reviews/matrix_ideal_01/matrix_controls.py':'Entire 116-line exact polynomial/matrix control body read; never executed or imported.',
 'requirements.txt':'Read; pins sympy==1.14.0.'}
member_map=[]
for f in inventory['members']:
 name=f['member']
 if name in read_paths: handling='read'; description=read_paths[name]
 elif name.endswith('.py'): handling='catalogued_only_not_executed';description='Other packaging, historical audit or priority program; unnecessary for this scope pass.'
 elif name.endswith('.pdf'): handling='duplicate_reader';description='Reader identity recorded by extraction inventory.'
 elif name.endswith('.gitignore'): handling='catalogued_hidden_member';description='Included in safe extraction and hash inventory.'
 else: handling='catalogued_only_body_opaque';description='Historical assessment, replay, priority/status, package metadata or provenance body not consulted as evidence.'
 member_map.append({**f,'scope_handling':handling,'scope_description':description})
writej('reader-support-map.json',{'created_utc':NOW,'public_asset_count':len(receipt['files']),'archive_regular_member_count':len(member_map),'all_members_rehashed':True,'distinct_reader_count':1,'embedded_pdf_identical_to_main':True,'nested_archives':inventory['nested_archives'],'current_pdf_pages':4,'published_helper_execution':False,'members':member_map})
interfaces=[
 {'source':'owr2018-02.pdf','url':primary[0]['url'],'sha256':primary[0]['sha256'],'read_extent':'Satoh contribution in full, printed pp.87–90 (PDF pages45–48); definitions and literal conjecture on printed pp.88–89.','version':'Original published OWR Report2/2018, workshop14–20January2018; DOI10.4171/OWR/2018/2.','interface':'The Q-subalgebra generated by individual SL(2,ℂ) matrix-entry functions, augmentation ideal J, full quotient J/J^{k+1}, inclusion A_n(k)⊆D_n(k), equality through degree4 and all-degree equality conjecture in the n≥3 discussion.','scope_boundary':'The original text supplies the target statement and attribution. Its presence in2018 establishes neither current openness nor firstness of a2026 negative answer.'},
 {'source':'satoh-v2.pdf','url':primary[1]['url'],'sha256':primary[1]['sha256'],'read_extent':'Definitions and Lemmas3.1–3.2 in §3, §4.2 (definition and comparison interfaces), and §6 Theorem6.3; inspected these relevant primary-body passages, not the entire31-page paper.','version':'arXiv1607.05411v2,8December2017,31pages. PDF conversion metadata is not the version publication date.','interface':'Component functions, finite generation via determinant-one adjugates, invariant augmentation ideal, full quotient filtration, inclusion A⊆D and low-degree equality k=1,2,3,4 for m≥2.','scope_boundary':'The2021 Pacific Journal of Mathematics publication is related bibliographic metadata, not an authenticated identical body in this intake. No assertion that v2 and final are identical.'},
 {'source':'burde-v2.pdf','url':primary[2]['url'],'sha256':primary[2]['sha256'],'read_extent':'Identity(4), surrounding §2 context; Theorem4.14 and nearby §4 discussion; bibliography entry18.','version':'arXiv1411.0950v2,27February2015,14pages.','interface':'Identity(4) is [z,[[z,x],[z,y]]]=0. After z=X,x=Y,y=Z and reversing the outer bracket, it is the manuscript P. Theorem4.14 attributes a characteristic-zero sl2 identity basis containing it to Razmyslov.','scope_boundary':'Razmyslov attribution is through the inspected Burde body. Original Razmyslov and final Burde journal bodies were not inspected. The manuscript itself proves its stronger all-2×2-matrices/commutative-ring identity without importing a classification theorem.'}
]
writej('primary-read-ledger.json',{'created_utc':NOW,'interfaces':interfaces,'unavailable_or_uninspected':[{'source':'Satoh2017 Proc.EdinburghMath.Soc. DOI10.1017/S0013091516000456','status':'Full final body not acquired; bounded web DOI opening failed. Original2018 report and2017 arXiv v2 provide the actual target/model interfaces.'},{'source':'Satoh2021 PacificJ.Math. DOI10.2140/pjm.2021.312.477','status':'Full final body not acquired; bounded web DOI opening failed. Inspected version is arXiv1607.05411v2 only.'},{'source':'Razmyslov1973 and later related literature','status':'Original Razmyslov not read; no exhaustive novelty audit or current-worldwide-openness inference.'}]})
binding={'record_id':'23387442','concept_record_id':str(record['conceptrecid']),'record_url':'https://zenodo.org/records/23387442','doi':record['doi'],'zenodo_version':record['metadata']['version'],'manuscript_version':None,'manuscript_date':'2026-10-15','zenodo_publication_date':record['metadata']['publication_date'],'record_created_utc':record['created'],'record_updated_utc':record['updated'],'page_date_basis':'Printed15October2026 and Zenodo publication-date metadata agree. Creation is recorded separately; neither asserts earlier first deposit or research priority.','source_retrieved_utc':receipt['retrieved_utc'],'receipt_sha256':sha(SRC/'receipt.json'),'record_sha256':sha(SRC/'record.json'),'pdf_sha256':next(x['sha256'] for x in receipt['files'] if x['name'].endswith('.pdf')),'supplement_sha256':None,'files':receipt['files'],'source_tex_path':str(texpath.relative_to(ROOT)),'source_tex_sha256':sha(texpath),'reviewed_documents':[{'filename':'satoh_filtration_counterexamples.pdf','pages':4,'read_scope':'Complete current manuscript and source; scope preparation only, mathematical verification pending.'}],'abstract_source':'Complete current TeX abstract, PDF-cross-checked, with mathematical typography and whitespace normalized only.','publication_state':'CANDIDATE_ONLY_MATHEMATICAL_REVIEW_AND_ROOT_CLEARANCE_PENDING','archive_reader_note':'One embedded main PDF is byte-identical to standalone public PDF; no distinct supplement or nested archive.','version_source':'Version1.0 is Zenodo metadata; printed manuscript has date but no version number.'}
candidate={
 'title':record['metadata']['title'],
 'slug':'satoh-sl2-representation-filtration-counterexamples',
 'description':'Explicit free-group automorphisms separate Satoh’s SL(2) representation filtration from the integral Andreadakis filtration in degrees five and six.',
 'abstract':abstract,
 'plain_language':[
 'A free group starts with symbols that can be combined into words, with no relations beyond cancellation. An automorphism changes the generators while preserving the group. Two filtrations measure how hard such a change is to detect: one uses successive group quotients, while the other uses two-by-two matrix representations near the trivial representation.',
 'The paper gives explicit changes that the matrix test misses to a specified order even though the corresponding group quotient detects them. It treats degree five for every rank at least four, and degree six for every rank at least three.',
 'The key idea is that a classical identity holds for two-by-two matrices but not for freely noncommuting symbols. Turning this mismatch into words gives counterexamples to the all-degree equality stated in Satoh’s2018 report.'
 ],
 'result':[
 'For the free group F_n, let A_n(k) be the kernel of the action on F_n/Γ_{k+1}F_n, using the integral lower central series. Let D_n(k) be the kernel of the action on the entire J/J^{k+1}, where J is the augmentation ideal in the rational algebra of SL(2,ℂ) matrix-entry functions.',
 'With group commutator [g,h]=ghg⁻¹h⁻¹, set w=[[[x₁,x₂],[x₁,x₃]],x₁]. For every n≥4, the automorphism x₄↦x₄w fixing the other generators lies in D_n(5) but not A_n(5).',
 'Set v=[[[x₁,x₂],[x₁,[x₁,x₂]]],x₁]. For every n≥3, the automorphism x₃↦x₃v fixing the other generators lies in D_n(6) but not A_n(6). Thus equality in all degrees fails at every rank n≥3 covered by the stated conjecture.'
 ],
 'why_it_works':[
 'The classical identity [[[X,Y],[X,Z]],X]=0 for two-by-two matrices follows here directly from Cayley–Hamilton over any commutative coefficient ring. Substituting Z=[X,Y] gives the weighted degree-six identity.',
 'A filtered group-commutator calculation transfers these identities to actual powers J⁶ and J⁷ in the matrix-entry algebra. It controls the whole ideal quotient, rather than only selected representations or one associated graded piece.',
 'Integral Magnus expansions retain a nonzero degree-five coefficient for w and degree-six coefficient for v. These obstruct membership in the next lower central subgroup. Each word omits the generator that is moved, so the displayed substitutions have explicit inverses.'
 ],
 'limitations':[
 'This is a result about the rational SL(2,ℂ) matrix-entry algebra and the full ideal quotient J/J^{k+1}. It is not a theorem about a trace algebra, a character algebra or a Grothendieck representation ring.',
 'The theorem does not establish a degree-five counterexample at rank three, failure in every degree, or an extension to larger matrix sizes.',
 'It addresses the representation-filtration equality formulated in2018. It is distinct from the comparison of the Andreadakis filtration with the lower central series of IA_n.',
 'The matrix identity and the general algebraic tools are classical. The stated contribution is their explicit application to this equality; no new polynomial identity, historical firstness, exhaustive novelty clearance or continuing worldwide openness is claimed.'
 ],
 'background':[
 {'title':'Satoh — On the Johnson homomorphisms of the automorphism groups of free groups','url':'https://doi.org/10.4171/OWR/2018/2','note':'The2018 Oberwolfach report, pp.87–90, supplies the component-function algebra, the full ideal quotient and the stated all-degree equality conjecture.'},
 {'title':'Satoh — On the graded quotients of the SL(m,ℂ)-representation algebras of groups','url':'https://arxiv.org/abs/1607.05411v2','note':'The inspected2017 preprint supplies the precise filtration definitions and the equality through degree four. It is identified separately from the related2021 journal publication.'},
 {'title':'Burde — Derivation double Lie algebras','url':'https://arxiv.org/abs/1411.0950v2','note':'Identity(4) is the classical degree-five identity used here, after a sign and variable change. Theorem4.14 attributes its place in an sl₂ identity basis to Razmyslov; this attribution is through Burde.'}
 ],
 'collaboration':'I welcome substantive collaboration from researchers in free-group automorphisms and polynomial identities on independent verification, comparison with earlier literature and development toward journal review. Coauthorship would reflect actual research contributions and mutual agreement.',
 'follow_up':None,'followup_rationale':'No follow-up is proposed. An untreated rank or degree alone does not meet the requested bar for a substantial new research question.',
 'publication_date':'2026-10-15','version':'1.0','doi':record['doi'],'author':'Alec Kriebel','orcid':'https://orcid.org/0009-0001-9320-500X','pdf_filename':'satoh_filtration_counterexamples.pdf','supplement_filename':None,
 'additional_assets':[{'filename':'satoh_filtration_verification.zip','label':'Source and verification materials (ZIP)'}],
 'status':'Unrefereed preprint, Zenodo version1.0, dated15October2026. Developed with extensive AI assistance; no independent human peer review or proof-assistant certification is claimed.',
 'ai_disclosure':'AI tools were used extensively in developing the constructions, checking proofs and computations, investigating sources and writing. Internal AI reviews do not constitute independent human peer review.',
 'source_binding':binding,'related_resources':[],'candidate_only':True,'candidate_gate':'Scope candidate only. Independent mathematical review and root publication clearance remain pending; this document does not grant a mathematical PASS or permission to publish.'
}
# Readable spacing in public prose; no scientific content is changed.
for field in ['plain_language','result','why_it_works','limitations']:
 candidate[field]=[re.sub(r'(?<=[A-Za-z’])(?=\d{4})',' ',x) for x in candidate[field]]
for item in candidate['background']:
 item['note']=re.sub(r'(?<=[A-Za-z])(?=\d{4})',' ',item['note']).replace('Identity(4)','Identity (4)').replace('Theorem4.14','Theorem 4.14')
candidate['status']='Unrefereed preprint, Zenodo version 1.0, dated 15 October 2026. Developed with extensive AI assistance; no independent human peer review or proof-assistant certification is claimed.'
writej('candidate.json',candidate)
writej('abstract-check.json',{'checked_utc':NOW,'method':'Exact complete TeX abstract extracted; explicit typography/whitespace normalization compared to plain transcription; PDF cross-read.','source_tex_sha256':sha(texpath),'abstract_tex_sha256':sha(OUT/'ABSTRACT.tex'),'abstract_text_sha256':sha(OUT/'ABSTRACT.txt'),'complete_source_abstract_equal_after_normalization':True,'omitted_sentences':0,'candidate_abstract_equal':candidate['abstract']==abstract,'meta_description_characters':len(candidate['description'])})
writej('evidence.json',{'record_id':'23387442','row':68,'status':'SCOPE_COMPLETE_MATHEMATICAL_REVIEW_PENDING','created_utc':NOW,'source_binding':binding,'integrity':{'queue_match':receipt['queue_matched'],'public_files_rehashed':2,'all_archive_regular_members_rehashed':107,'hidden_members_included':True,'nested_archives':[],'distinct_reader_pdfs':1,'embedded_pdf_identical':True,'primary_pdfs_rehashed':3},'reading':{'main_pdf':'All4pages','current_tex':'All285lines','support_files_read':read_paths,'primary_interfaces':interfaces},'checks_run':['Fresh public asset MD5, byte size and SHA256 against Zenodo/frozen queue','Safe archive path/type/CRC and per-member hash inventory including hidden member','Final rehash of all2public assets,107members and3primary PDFs','Complete abstract normalization/identity check'],'published_mathematical_helpers_executed':[],'mathematical_pass_issued':False,'historical_assessment_policy':{'dedicated_bodies_read':False,'filenames_catalogued':True,'incidental_exposure':'Current manuscript §5 includes historical review/priority statements and a489-evaluation claim. Original mathematical PROOF.md includes brief assessment wording, and read program bodies contain comments and literal PASS output labels. No retained verdict, review, priority or replay body was read or adopted; no run result is inferred.'},'remaining_gates':['Independent analytic mathematical reconstruction','Independent adversarial falsification and meaningful program replay','Root disposition before any publication candidate may be promoted'],'follow_up':None})
(OUT/'REVIEW.md').write_text('''# Scope and acquisition review — Zenodo 23387442

**Disposition: SCOPE COMPLETE; mathematical review and publication clearance pending.** This is an intake, provenance and editorial-scope report. It makes no mathematical PASS, verification-runtime or novelty claim.

## Identity and complete acquisition

The frozen queue identifies row 68, work Z-23387441, current record 23387442, title *Counterexamples to Satoh’s SL(2) representation-filtration conjecture*, version 1.0 and publication-date metadata 15 October 2026. Fresh metadata and both public assets match that identity. The printed manuscript also says 15 October 2026 but has no printed version number. The record was created at 2026-10-15T07:50:10.998117+00:00; that event is kept distinct from a manuscript date or a claim of research priority.

The main PDF is four pages, 68,204 bytes, SHA256 `14f43ff1132036fbdf08b7d0253d413f868a7dc1ff753d18de97847cd292df5b`. The ZIP is 254,008 bytes, SHA256 `edd395241058eb7becb2fdd7ba84d34a2d389eef35f44eeb1e32060db0e7ea8d`. Original metadata, download URLs, resolved URLs, times, sizes, Zenodo MD5 checksums and SHA256 values are in `sources/receipt.json`. There are exactly two public assets. Fresh metadata is bound by SHA256 `0290ebbae1fc2ac04cde8d714f0911041c1eddfa5feac748f9d12d85c9b19d9a`.

Safe extraction checked all paths, file types and CRCs, including the hidden `.gitignore`. All 107 regular members have byte sizes, CRCs, original archive modes and SHA256 bindings. There are no nested archives. The only embedded PDF is byte-identical to the standalone main PDF, so there is one distinct reader, not an extra edition or reader supplement. All public assets, all 107 extracted members and all three fresh primary PDFs were rehashed at finalization. These are integrity checks, not mathematical verification.

## Reading and independence

Read the complete current four-page PDF and all 285 lines of its TeX source. Read the original `release/PROOF.md`, original `release/verify.py` (192 lines), `reviews/freegroup_01/controls.py` (206 lines), `reviews/matrix_ideal_01/matrix_controls.py` (116 lines), and the SymPy 1.14.0 requirements pin. Those programs were inspected as mathematical support; none was imported or executed. Other package and review files are explicitly classified in `reader-support-map.json` rather than silently counted as read.

Dedicated historical assessment, verdict, priority, acceptance and replay bodies remain opaque. Filenames and byte hashes were inventoried. Unavoidable exposure was limited to historical statements in the current manuscript’s verification/status section, short assessment wording inside the original mathematical proof, and code comments or literal output labels in the mathematical programs. In particular, the manuscript’s 489-evaluation claim is not a fresh result here. No sibling review was consulted.

## Exact model and theorem claimed

The lower central series is integral: Γ₁F_n=F_n and Γ_{r+1}F_n=[Γ_rF_n,F_n]. The first filtration is A_n(k)=ker(Aut F_n→Aut(F_n/Γ_{k+1}F_n)). The second uses the rational algebra of individual SL(2,ℂ) matrix-entry functions on Hom(F_n,SL(2,ℂ)); J is generated by a_ij(g)−δ_ij, and D_n(k) is the kernel of the action on the **entire** quotient J/J^{k+1}. This is not a single graded piece, trace/character algebra or Grothendieck representation ring. The substitution convention is a_ij(g)^φ=a_ij(φ(g)); an inverse convention has the same kernel.

With [g,h]=ghg⁻¹h⁻¹, the paper defines w=[[[x₁,x₂],[x₁,x₃]],x₁] and v=[[[x₁,x₂],[x₁,[x₁,x₂]]],x₁]. Its exact theorem claims that fixing other generators and sending x₄↦x₄w gives an element of D_n(5)\\A_n(5) for every n≥4, while x₃↦x₃v gives an element of D_n(6)\\A_n(6) for every n≥3. The second construction alone refutes equality in all degrees at every rank in the source’s n≥3 range. It does not claim failure in every degree. It does not settle degree five at rank three, larger matrix sizes or the separate Andreadakis-versus-lower-central-IA comparison.

## Proof and support interfaces for independent reviewers

The current proof has four explicit interfaces. First, Cayley–Hamilton gives the classical identity P(X,Y,Z)=[[[X,Y],[X,Z]],X]=0 for arbitrary 2×2 matrices over a commutative ring; Q(X,Y)=P(X,Y,[X,Y]) has weighted degree six. The proof uses no division or diagonalization. Second, the exact identity [1+u,1+z]−1=(uz−zu)(1+u)⁻¹(1+z)⁻¹ transfers successive commutators to actual ideal powers. The manuscript applies P and Q in the commutative associated graded ring and obtains M(w)−I∈Mat₂(J⁶) and M(v)−I∈Mat₂(J⁷); it does not infer ideal membership from one-parameter arcs or require a polynomial, reduced or smooth associated graded ring.

Third, the integral Magnus map into noncommutative formal power series supplies only the implication Γ_r→1+terms of degree at least r. The source identifies coefficients −1 on X₁X₁X₂X₁X₃ and +1 on X₁X₁X₁X₂X₁X₂ to obstruct Γ₆ and Γ₇ membership. No Magnus injectivity or converse dimension-subgroup theorem is invoked. Fourth, each word omits the moved generator, giving an explicit inverse; determinant-one adjugate formulas show that the generator-matrix entries generate the full algebra, so the ideal congruence controls the full quotient action.

The original proof packet uses a traceless leading-term formulation and determinant relation; the current manuscript instead proves the stronger all-matrix identity directly. The original checker uses exact sparse free-associative arithmetic and Python assertions. It should not be treated as an effective guard under Python `-O`, which disables assertions. The separate free-group program uses untruncated integer unitriangular matrices and explicit failures, but reads a retained coefficient/word transcription for comparison. The matrix program uses exact SymPy polynomial rings and finite Gauss-coordinate quotients, including wrong-variable/dimension/coefficient-ring controls. These are code-reading observations only. Future reviewers should develop independent reasoning first, then replay in an isolated copy and distinguish finite controls from universal proof.

The paper displays two further finite witnesses: UT₆ assignments send w to I−E₁₆, and UT₇ assignments send v to I+E₁₇. This scope review has not freshly multiplied them. The universal proof, finite witness identities and all program output remain for the separate mathematical reviewers.

## Original problem and primary-source boundaries

The fresh original published OWR Report 2/2018 was read at Satoh’s entire contribution, printed pp.87–90 (PDF pp.45–48). Printed pp.88–89 define the same matrix-entry Q-algebra, J, full quotient and n≥3 discussion. Page89 states the all-degree equality conjecture after listing inclusion and equality in degrees1–4. Thus the model and target are anchored in the actual original body rather than a title or search snippet. Its existence in2018 does not establish current openness or the priority of a later negative answer.

The fresh Satoh arXiv1607.05411v2 body (8 December2017) was inspected at §3 definitions/Lemmas3.1–3.2, §4.2 and Theorem6.3. It supplies the component-function algebra, determinant-one finite generation, invariant ideal, full-quotient definition and low-degree comparison. This exact preprint version is distinguished from its related2021 Pacific Journal of Mathematics publication. The2017 Edinburgh and2021 Pacific final full bodies were not acquired after bounded unsuccessful DOI openings; no claim of exact final-body equivalence is made. Low-degree equality is contextual and does not replace the paper’s explicit counterexample proof.

Fresh Burde arXiv1411.0950v2 (27 February2015) was inspected at identity(4), its context, Theorem4.14 and reference18. Identity(4), [z,[[z,x],[z,y]]]=0, becomes the source’s P after renaming variables and reversing the outer bracket. Theorem4.14 describes a characteristic-zero sl₂ identity basis containing it and attributes it to Razmyslov. The manuscript proves its stronger matrix identity directly. Historical Razmyslov credit is therefore explicitly **through Burde**; the original Razmyslov body and final Burde journal body were not read. No new polynomial identity or universal PI method should be advertised.

`primary-source-receipts.json` binds exact fresh URLs, version descriptions, PDF byte sizes and hashes. `primary-read-ledger.json` records precisely the relevant portions read; it does not claim that all31 Satoh or14 Burde pages were read. No exhaustive priority search has been conducted or inferred from historical audit claims.

## Conditional page content and publication boundaries

`ABSTRACT.tex` is the entire original source abstract. `ABSTRACT.txt` and `candidate.json` preserve all its sentences with only typography/whitespace normalization; `abstract-check.json` records exact normalization equality. The candidate has descriptive metadata, full abstract, an accessible explanation, the two explicit automorphisms and rank/degree quantifiers, important model exclusions, prior credit, all public assets, a concise AI disclosure and a professional general collaboration invitation. It contains no internal replay narrative. It has `candidate_only=true` and is not a publication approval or rendered page.

The candidate is an unrefereed preprint. It must not be described as human-reviewed, formally certified, a new matrix identity, a result for every degree, a larger-matrix theorem, or a demonstrated first solution. The source’s limited literature access is preserved privately and no current worldwide-open-status claim appears publicly. The version is Zenodo metadata; the manuscript prints its date only. The default follow-up is null: the mere absence of a rank-three degree-five claim is insufficient to justify a substantial research proposal.

## Strongest established intake result and remaining gap

The strongest completed result of this assignment is a complete, queue-matched and checksum-bound public-source inventory, one distinct reader, a full manuscript/support scope map, actual primary-body alignment of the stated conjecture and its classical ingredient, and a complete restrained page candidate. The mathematical theorem is neither certified nor rejected here. Its analytic proof reconstruction, adversarial falsification, meaningful isolated helper replay and final root disposition remain pending. No site, Sheet, Git, Zenodo, redirect or outreach action was performed; all original published bytes remain unchanged.
''')
writej('verdict.json',{'record_id':'23387442','row':68,'role':'intake_scope_only','status':'SCOPE_COMPLETE_MATHEMATICAL_REVIEW_PENDING','completion_percent':100,'completed_utc':NOW,'pdf_sha256':binding['pdf_sha256'],'archive_sha256':next(x['sha256'] for x in receipt['files'] if x['name'].endswith('.zip')),'source_binding':binding,'mathematical_verdict':None,'published_helpers_executed':False,'publication_authorized':False,'candidate_only':True,'follow_up':None,'strongest_verified_result':'Fresh complete queue-matched public asset/member inventory; one distinct reader; full current manuscript and necessary proof/code support read; actual original conjecture and classical primary interfaces inspected; full abstract and restrained conditional candidate bound to those sources.','remaining_gap':'Independent analytic and adversarial mathematical reviews, meaningful isolated replay and root disposition before publication.','historical_assessment_bodies_read':False,'incidental_exposure_disclosed':True,'report_sha256':sha(OUT/'REVIEW.md'),'evidence_sha256':sha(OUT/'evidence.json'),'candidate_sha256':sha(OUT/'candidate.json')})
with (OUT/'RESEARCH_LOG.md').open('a') as f:
 f.write(f'\n## {NOW} — 100% of intake/scope assignment\nCompleted primary-body interface ledger, all-member reader/support map, exact full abstract extraction/normalization, conditional restrained candidate and source-bound report/evidence/verdict. Finalized integrity checks on2public files,107archive members and3primary PDFs; no published mathematical helper was executed. Mathematical reviews and root publication disposition remain pending. Follow-up null. Historical assessment bodies and sibling findings stayed opaque; incidental current-manuscript/proof/code status wording is disclosed. No external mutation or outreach.\n')
files=['REVIEW.md','verdict.json','evidence.json','candidate.json','ABSTRACT.tex','ABSTRACT.txt','abstract-check.json','primary-read-ledger.json','primary-source-receipts.json','reader-support-map.json','RESEARCH_LOG.md','write_scope_artifacts.py','queue_identity.json']
writej('FINAL_HASHES.json',{'created_utc':NOW,'status':'SCOPE_COMPLETE_MATHEMATICAL_REVIEW_PENDING','files':{name:sha(OUT/name) for name in files}})
print(json.dumps({'status':'SCOPE_COMPLETE_MATHEMATICAL_REVIEW_PENDING','hashes':{name:sha(OUT/name) for name in ['REVIEW.md','verdict.json','evidence.json','candidate.json','FINAL_HASHES.json']},'abstract_words':len(abstract.split()),'description_characters':len(candidate['description'])},indent=2))
