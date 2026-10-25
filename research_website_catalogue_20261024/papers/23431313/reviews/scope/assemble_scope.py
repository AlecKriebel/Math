from pathlib import Path
import datetime, hashlib, json, zipfile, io, stat
from pathlib import PurePosixPath

ROOT=Path(__file__).resolve().parent
BASE=ROOT.parents[1]
SRC=BASE/'sources'
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
def digest(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def writej(n,d):(ROOT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
receipt=json.loads((SRC/'receipt.json').read_text())
record=json.loads((SRC/'record.json').read_text())
tex=SRC/'published-source/paper.tex'
abstract=tex.read_text().split('\\begin{abstract}\n',1)[1].split('\\end{abstract}',1)[0]
(ROOT/'abstract_original.tex').write_text(abstract)
plain=' '.join(abstract.split()).replace('$','').replace('\\R^n','ℝⁿ').replace('\\lambda','λ')
(ROOT/'abstract_original.txt').write_text(plain+'\n')
writej('abstract_receipt.json',{'source':'sources/published-source/paper.tex','source_sha256':digest(tex)['sha256'],'pdf_page':1,'main_pdf_sha256':receipt['files'][0]['sha256'],'extraction':'Complete literal abstract environment retained in TeX. Plain copy collapses whitespace and converts math notation only; no sentence omitted.','tex':digest(ROOT/'abstract_original.tex'),'plain':digest(ROOT/'abstract_original.txt'),'plain_whitespace_word_count':len(plain.split())})
(ROOT/'ORIGINAL_ABSTRACT.md').write_text('# Complete original abstract\n\n'+plain+'\n\nExact source and output bindings: abstract_receipt.json.\n')

primary=json.loads((ROOT/'primary-source-receipts.json').read_text())
interfaces=[
 {'source':'problems-v2.pdf','read':'Pages28–29, observations and complete Problem5.11 with surrounding remarks','interface':'The printed question asks which Segre characteristics occur unchanged on a domain U⊂ℝⁿ for a compactly supported Nijenhuis operator. It separately records real semisimple examples, a two-dimensional Jordan example, and the obstruction to nonreal eigenvalues. It explicitly calls size≥3 Jordan blocks unknown at that historical stage.','role':'Original historical target, not a certificate that it was still open in October2026.','limits':'Problem5.10 is the different everywhere-algebraically-regular closed-manifold problem; Problem5.12 asks for real-analytic surface examples. Neither is the present target.'},
 {'source':'problems-v1.pdf','read':'Pages36–37, observations and complete Problem4.10 with following discussion','interface':'The earlier author edition has the same compact-support/local-unchanged-type question as Problem4.10, with semisimple/nonreal/two-dimensional examples.','role':'Exact historical numbering/version comparison.','limits':'Corpus label5.9 is not the locator in either inspected author edition. Original journal work is2018; author-v2 is dated2020.'},
 {'source':'bkm-v2.pdf','read':'Definition2.1–2.3 p7; admissible factorization and Theorem3.1/proof pp18–20; Theorem3.3/proof and local holomorphic consequences pp22–24; Theorem4.5 and following remark pp27–28; Theorem6.1 and full proof pp41–43','interface':'Local splitting for coprime smooth characteristic factors yields integrable complementary distributions and blocks depending on their own coordinates, even at algebraically nongeneric points. A smooth Nijenhuis block with no real spectrum has a canonical integrable complex structure and holomorphic operator coefficients. Theorem6.1 states persistence of a nonreal eigenvalue with constant algebraic multiplicity on a closed connected manifold. Theorem4.5 assumes independent coefficients of factored characteristic polynomials and realizes arbitrary types at points, generically becoming semisimple nearby.','role':'Load-bearing local splitting/holomorphic interfaces for the paper’s weaker zero-point obstruction, and credited earlier point realizations.','limits':'Source is author-v2, not equated to unread Advances in Mathematics publisher bytes. Paper supplies a separate maximum argument for the zero-point consequence and does not rely on the final polynomial-reduction sentence to certify every step of stronger persistence. Point realization is distinct from a fixed nonsemisimple type on an open domain and a global compact transition.'},
 {'source':'bkm3-published.pdf','read':'Published pages155–161 (definitions, real-analytic convention, Theorem1.10); p173 proof interface','interface':'gl-regular means one Jordan block per eigenvalue. The article works in the real-analytic category. Theorem1.10 constructs a local Nijenhuis perturbation from a nilpotent Jordan block into the closure of a chosen regular layer; the proof gives the layer on a nonempty open subset.','role':'Comparison/attribution, not an existence theorem imported to build the new collar.','limits':'Does not state arbitrary repeated blocks for the same eigenvalue, a compact zero transition, or a global smooth compact-support classification.'},
 {'source':'bkm3-v1.pdf','read':'Author p3 real-analytic convention and p7 regular-layer definition/Theorem1.4','interface':'The corresponding author-v1 statement is Theorem1.4, not journal Theorem1.4.','role':'Versioned numbering crosscheck.','limits':'Not silently identified with final issue bytes.'},
 {'source':'bkm3-online-first.pdf','read':'Publisher header and pp6–7 regular-layer definition/Theorem1.10','interface':'Online-first publisher copy uses Theorem1.10, consistently with final issue copy; pagination differs.','role':'Additional bibliographic version confirmation.','limits':'Acquired separately and hashed; it is not the final paginated PDF.'},
 {'source':'bkm4-v1.pdf','read':'Definitions and regularity p4; Theorem1.2 and coefficient expansion p6; Theorem1.4/formulas5–6 and surrounding smooth/analytic qualifications pp8–10; Lemma2.3/compatibility equation20 and proof start p17','interface':'Symmetries of a gl-regular Nijenhuis generator are Nijenhuis, including outputs that may be zero or singular. Variable polynomial coefficients must satisfy the displayed differential compatibility equations. For a single nilpotent Jordan block, the smooth local symmetry formula depends on triangular Toeplitz coordinates; for size3 its upper-right coefficient includes an unwrapped coordinate times a derivative of a transverse function.','role':'Accurate boundary on a possible prior local construction route.','limits':'No claim that outputs must remain gl-regular; no blanket exclusion of other uses of this framework. The formula by itself does not establish periodic angular dependence or exact compact zero bands.'}
]
for x in interfaces:
 r=next(t for t in primary if t['name']==x['source']);x.update({k:r[k] for k in ['url','version','sha256','pages']})
writej('primary_interfaces.json',interfaces)

support=[]
for name,reading in [('paper.tex','Full315-line current proof and references read and compared with all five PDF pages'),('README.md','Full current mathematical scope and execution instructions read; appended historical review/accounting summaries incidentally visible, not adopted'),('scripts/run_checks.py','Full exact polynomial control program read; all schedule, jet and deliberate-fault mechanisms mapped; not executed')]:
 p=SRC/'published-source'/name;support.append({'path':str(p.relative_to(BASE)),**digest(p),'reading':reading})
claims=[
 {'pages':'1','claim':'Theorem1 existence','scope':'For every n≥1 and each prescribed real Jordan matrix J whose spectrum is entirely real, there exists a globally C∞ compactly supported real (1,1)-tensor L on ℝⁿ with Nijenhuis torsion zero. Its matrix is exactly J in a smooth commuting local frame on a nonempty open domain. Numerical eigenvalues, block sizes and grouping are prescribed, including repeated eigenvalues, nonsemisimple blocks and zero data.'},
 {'pages':'1,3–4','claim':'Theorem1 necessity','scope':'For every globally smooth compactly supported real Nijenhuis operator on ℝⁿ, every eigenvalue at every point is real. The proof extends by zero to the one-point compactification Sⁿ and invokes the paper’s zero-point lemma grounded in prior local splitting/holomorphic theory.'},
 {'pages':'2','claim':'Ordered collar equation','scope':'For L=[[A(t),b(t)],[0,λ(t)]] in the global commuting angular/transverse frame of T^(n−1)×(−1,1), every angular torsion component vanishes and mixed torsion equals(A−λI)A′. Product order is essential; no separate condition on b′ or λ′ is imposed.'},
 {'pages':'2–3','claim':'Lemma1 finite Jordan schedule','scope':'For any real-spectrum Jordan matrix in n≥2, designate one terminal vector transverse, retain its arrow in b, clear b, and process angular Jordan blocks. Move λ while A is fixed; then remove superdiagonal arrows in predecessor-first order, then move the scalar block with λ matched. Repeated/zero eigenvalues and singleton blocks are allowed; no division by spectral gaps. Smooth plateau reparameterizations permit gluing.'},
 {'pages':'3','claim':'Embedding and compact extension','scope':'T^d embeds two-sidedly in ℝ^(d+1) by tubular induction with explicit trivial rank-two normal frame. The dimension-n collar around T^(n−1) carries the construction. q(t)=S(2(t²−1/16)) gives J on |t|≤1/4 and exactly zero on |t|≥3/4. The support is compactly contained in the open collar, so zero extension is smooth and torsion-free. n=1 is handled separately by scalar bump; J=0 is allowed.'},
 {'pages':'3–4','claim':'Lemma2 zero-point rigidity','scope':'On a closed connected smooth manifold, a real Nijenhuis operator vanishing at one point has entirely real spectrum. Proof takes a maximal positive imaginary part and maximal multiplicity, uses local splitting into a conjugate-pair block, holomorphic coefficients/maximum principle, then open-and-closed propagation. No gl-regularity, semisimplicity or real analyticity of the original tensor is assumed.'},
 {'pages':'4–5','claim':'Prior-work and reproduction boundary','scope':'Credits nonreal obstruction, prior semisimple/two-dimensional examples, arbitrary-type point realizations and local splitting/holomorphic mechanisms. GeometryIII regular-layer and GeometryIV symmetry results are compared at their actual hypotheses. Finite controls corroborate indexing, not the universal geometric/analytic proof; no historical omitted-program replay or priority claim.'}
]
limitations=[
 'Classification of which Jordan types can be realized on some open domain, not a classification of all global Nijenhuis tensor fields up to equivalence.',
 'The matrix is prescribed in a smooth commuting local frame, not in the fixed ambient Cartesian frame. The domain is chosen by the construction, not an arbitrary preassigned domain.',
 'Type, rank and eigenvalues may change outside the realization region, and the operator becomes exactly zero. No everywhere-gl-regular or constant-global-type conclusion.',
 'C∞ smooth construction only; no nonzero real-analytic compact-support result. The comparison GeometryIII theorem has additional analytic/gl-regular restrictions.',
 'Necessity uses a closed connected manifold after compactification. The statement does not forbid local nonreal Nijenhuis models or nonreal spectrum on noncompact fields without compact support.',
 'Finite mathematical controls do not prove the all-dimensional schedule, tubular embedding, gluing or maximum-principle argument. Scope executes no checker and issues no mathematical approval.',
 'The earlier obstruction and local constructions are credited; full-result and construction-method priority, novelty and worldwide prior openness remain unestablished.',
 'Version1.0 manuscript and metadata date are15October2026; fresh API created/submitted record is17October2026. Manuscript preparation date is not evidence of public availability on15October.',
 'Extensive AI assistance and unrefereed status remain explicit. No external human peer review, journal acceptance or proof-assistant certification is established.'
]

# Inspect every nested archive without opening historical opinion texts.
nested=[]
def inspect_archive(data,name,depth=0):
 assert depth<5
 with zipfile.ZipFile(io.BytesIO(data)) as z:
  assert len(z.infolist())<10000 and sum(m.file_size for m in z.infolist())<200*1024*1024
  seen=set();pdfs=[];children=[];items=[]
  for m in z.infolist():
   p=PurePosixPath(m.filename);mode=m.external_attr>>16
   assert not p.is_absolute() and '..' not in p.parts and '\\' not in m.filename
   assert not stat.S_ISLNK(mode) and stat.S_IFMT(mode) in (0,stat.S_IFREG,stat.S_IFDIR)
   assert str(p).casefold() not in seen;seen.add(str(p).casefold())
   if m.is_dir():continue
   b=z.read(m);d={'member':m.filename,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()};items.append(d)
   if b'%PDF-' in b[:1024]:pdfs.append(d)
   if zipfile.is_zipfile(io.BytesIO(b)):
    children.append(m.filename);inspect_archive(b,name+'!'+m.filename,depth+1)
  nested.append({'archive':name,'sha256':hashlib.sha256(data).hexdigest(),'safe_paths_types_crc':True,'regular_members':len(items),'pdf_members':pdfs,'nested_archives':children,'members':items})
magic=[]
for p in (SRC/'published-source').rglob('*'):
 if p.is_file():
  b=p.read_bytes()
  if b'%PDF-' in b[:1024]:magic.append(str(p.relative_to(SRC)))
  if zipfile.is_zipfile(p):inspect_archive(b,str(p.relative_to(SRC)))
assert len(nested)==1 and nested[0]['regular_members']==74 and not nested[0]['nested_archives']
assert nested[0]['pdf_members'][0]['sha256']==receipt['files'][0]['sha256']
writej('nested_archive_map.json',nested)
reader=json.loads((ROOT/'reader_document_map.json').read_text())
reader['documents']=[d for d in reader['documents'] if '!paper.pdf' not in d['path']]
reader['documents'].append({'path':'sources/'+nested[0]['archive']+'!paper.pdf','pages':5,'bytes':69486,'sha256':receipt['files'][0]['sha256'],'text':'reviews/scope/reader-a1e2da77dd73.txt','role':'Historical nested copy, byte-identical to operative main reader'})
reader.update({'distinct_reader_documents':1,'distinct_reader_pages':5,'additional_reader_pdfs':0,'all_reader_pdfs_read':True,'all5_main_pages_visually_inspected':True,'all129_member_magic_scan':True,'nested_archives':1,'nested_archive_members':74,'nested_archive_map':'nested_archive_map.json'})
writej('reader_document_map.json',reader)
scope={'record_id':'23431313','work_id':'Z-23431312','sheet_row':63,'title':record['metadata']['title'],'version':'1.0','publication_date':'2026-10-15','record_created_utc':record['created'],'date_qualification':'15October is manuscript/preparation and metadata date; record creation is17October. No claim of public availability on15October.','doi':'10.5281/zenodo.23431313','record_url':'https://zenodo.org/records/23431313','eligibility':'published_paper_record_with_manuscript','review_type':'acquisition_and_scope','status':'SCOPE_COMPLETE','mathematical_verdict':None,'completion_percent':100,'completed_utc':now,'bound_assets':receipt['files'],'record_sha256':digest(SRC/'record.json')['sha256'],'receipt_sha256':digest(SRC/'receipt.json')['sha256'],'main_pdf_sha256':receipt['files'][0]['sha256'],'main_tex_sha256':digest(tex)['sha256'],'source_support':support,'reader_map':'reader_document_map.json','reader_pages':5,'archive_regular_files':129,'nested_archives':1,'nested_archive_members':74,'additional_reader_pdfs':0,'original_abstract':'abstract_original.txt','abstract_receipt':'abstract_receipt.json','content_candidate':'CONTENT_CANDIDATE.md','report':'SCOPE_REVIEW.md','primary_interfaces':'primary_interfaces.json','claim_map':claims,'limitations':limitations,'follow_up':None,'follow_up_rationale':'No independently justified new question or conjecture established by this scope. Existing analytic, global-regularity and arbitrary-domain variants have different hypotheses; do not list them merely to populate a page.','scope_verification':{'all_public_assets_size_md5_sha256_match':True,'all129_extracted_files_final_rehashed_unchanged':True,'nested74_members_safe_and_hashed':True,'complete_main_paper_read':True,'all5_main_pages_visually_inspected':True,'original_primary_question_authenticated':True,'seven_primary_pdf_downloads_successful':True,'submitted_diagnostics_executed':False},'independence':{'sibling_reviews_read':False,'historical_dedicated_verdict_or_acceptance_bodies_read':False,'incidental_status_exposure':['Fresh record description and current paper summarize prior bounded comparison and review activity, while explicitly withholding priority.','Current README contains appended captured repair/accounting summaries with acceptance labels and superseded pending-readiness claims. They were incidentally visible during complete current instructions reading.','Current mathematical checker contains PASS output templates; no stored result file opened.'],'interpretation':'Only actual mathematical source, current instructions and raw primary texts inform scope. Historical appraisal bodies remain opaque; raw byte hashing/nested inventory does not read their opinions.'},'strongest_verified_scope_result':'Exact five-page edition and129-member public archive authenticated;74-member nested historical kit safely mapped with identical reader. Complete current proof and mathematical checker read; original question and imported/compared primary theorem interfaces mapped at their precise hypotheses.','remaining_gap':'Independent analytic/adversarial reviewers must validate the ordered collar identity and schedule in all dimensions, smooth same-dimensional torus embedding/zero extension and the zero-point maximum-principle argument at the stated source interfaces. Scope supplies no mathematical approval, novelty certificate or publication permission.','publication_actions':[]}
writej('scope.json',scope)

(ROOT/'CONTENT_CANDIDATE.md').write_text('''# Conditional page content — compactly supported Nijenhuis operators

Editorial candidate only. Independent mathematical clearance and the parent publication gate are still required; no page was created by this scope task.

Suggested slug: `nijenhuis-real-spectrum-compact-support`

Suggested search title: `Compactly supported Nijenhuis operators | Alec Kriebel`

Suggested description: `A smooth torus-collar construction realizes every real-spectrum Jordan type locally in a compactly supported Nijenhuis operator, including nonsemisimple blocks.`

Paper title: **A torus-collar proof of the real-spectrum compact-support classification for Nijenhuis operators**

Status: Unrefereed preprint · Version 1.0 · Manuscript dated 15 October 2026. The Zenodo record was created on 17 October 2026. AI tools were extensively involved; internal AI review is not independent human peer review.

## In plain language

A Nijenhuis operator assigns a linear transformation to each point of a space while satisfying a differential compatibility condition. The question here is whether a chosen matrix pattern can appear throughout an open region while the whole field becomes exactly zero outside a bounded region.

The paper gives a construction whenever all eigenvalues are real. It accommodates repeated eigenvalues and Jordan blocks of any size, including matrices that cannot be diagonalized. Both the numerical eigenvalues and the block pattern can be prescribed on the chosen region, in a suitable local coordinate frame. Outside that region, the pattern is allowed to change as the operator becomes zero.

The converse is an earlier obstruction: a smooth compactly supported real Nijenhuis operator cannot have a nonreal eigenvalue anywhere. The paper supplies the precise deduction needed for its application.

## What is interesting

The difficulty is turning off a non-diagonalizable matrix field without breaking the Nijenhuis condition. The construction uses a thin neighborhood of a torus, so only one transverse variable needs to control the transition. It removes the arrows of each Jordan block in a specified order, then reaches a region where the tensor is exactly zero. This gives an open region with the requested pattern, rather than just realizing that pattern at a single point.

## Relation to earlier work

The historical target is [Problem 5.11 in the 2020 author version of the integrable-systems problem survey](https://arxiv.org/abs/1804.03737v2), corresponding to Problem 4.10 in its 2018 version. That source already records the nonreal obstruction and real semisimple and two-dimensional examples. The paper also credits the local splitting, complex/holomorphic structure and point-realization results of [Bolsinov, Konyaev and Matveev](https://arxiv.org/abs/1903.04603v2).

This is presented as an explicit proof of that printed historical classification question. Priority of the full result and of this construction remains unestablished; the page should not claim a first solution or that the question was still open worldwide in 2026.

## Scope and limitations

The construction is globally smooth on ℝⁿ for every n ≥ 1. The prescribed matrix appears in a commuting local frame on some nonempty open region, not necessarily in the fixed Cartesian frame or on an arbitrarily specified region. The type, rank and eigenvalues may change elsewhere. The theorem does not require the operator to remain algebraically regular everywhere and does not give a nonzero real-analytic compact-support construction.

## Paper and supporting files

- [Version-specific Zenodo record and DOI](https://doi.org/10.5281/zenodo.23431313)
- [Published paper PDF](https://zenodo.org/records/23431313/files/paper.pdf)
- [Source and supporting kit](https://zenodo.org/records/23431313/files/pr1094_supportkit_v1.0.zip)

Use the existing PDF embed with a direct-download fallback. Include the complete original abstract from `abstract_original.txt`, preserving its attribution, priority qualification and AI/unrefereed disclosure.

## Collaboration

Researchers working in Nijenhuis geometry, differential geometry or integrable systems are welcome to examine the proof, identify corrections and discuss substantive further work or a journal submission. Coauthorship would reflect a meaningful contribution and mutual agreement.

No follow-up question or conjecture is proposed for this page.
''')

(ROOT/'SCOPE_REVIEW.md').write_text(f'''# Acquisition and scope — Zenodo 23431313

Completed {now}; scope 100%. Mathematical verdict: **not issued**. No publication, site, spreadsheet, Git, deploy, UI or outreach actions.

## Exact edition and custody

Frozen queue row 63, work Z-23431312, identifies version-specific record 23431313, *A torus-collar proof of the real-spectrum compact-support classification for Nijenhuis operators*, version 1.0. This is an expressly published manuscript with its own five-page PDF. Alec Kriebel, independent researcher; ORCID 0009-0001-9320-500X; CC BY 4.0. Cite DOI 10.5281/zenodo.23431313 for this edition, not the concept DOI 23431312.

The paper and metadata are dated 15 October 2026; the metadata notes say that date was local preparation before publication. Fresh API creation time is {record['created']}. Do not turn the preparation date into a claim of public availability on 15 October.

Both public assets were freshly fetched and checked against API and frozen-queue size and MD5. PDF SHA256: `{receipt['files'][0]['sha256']}`. ZIP SHA256: `{receipt['files'][1]['sha256']}`. Sources/receipt.json binds original/resolved URLs, timestamps, bytes and every extracted member. All 129 regular outer-archive members passed path/type/duplicate and CRC checks, and were compared byte-for-byte again at completion.

Magic scanning found one nested historical pre-repair support ZIP with 74 safely checked regular members, no further nested archives, and a paper.pdf identical to the operative PDF. The outer archive’s paper.pdf is also identical. Thus there is one distinct five-page reader and no additional reader supplement. Nested archive contents were hashed and mapped without opening historical opinion bodies; see nested_archive_map.json. No submitted bytes were changed.

## Reading coverage and independence

Read all five published pages, all 315 lines of paper.tex, the complete current README, and the full portable exact-polynomial checker scripts/run_checks.py. All five PDF pages were rendered and visually inspected. The current manuscript contains the complete all-dimensional proof; its mathematical program is corroborative and not an outsourced proof certificate. No submitted checker, historical result or build was executed or adopted.

Historical directories contain dedicated reports, verdicts, acceptance files and old administrative snapshots; those bodies remain opaque. The current README appends captured repair/accounting summaries reporting prior acceptance and pending states, and these were incidentally visible during reading of current execution instructions. Current metadata and paper also summarize prior bounded reviews. These are disclosed authored history, not fresh evidence. The checker contains a PASS output template, but stored NEW_CONTROLS_RESULT and historical outputs were not opened. No sibling review or conclusion was read. Raw primary source locations and hash receipts only were shared with the parent for independent reviewers.

## Exact claim and boundaries

Theorem 1 classifies realizable Jordan types, not all globally defined operators up to equivalence. A smooth real (1,1)-tensor L is Nijenhuis when N_L(X,Y)=L²[X,Y]+[LX,LY]−L[LX,Y]−L[X,LY] vanishes for every pair of vector fields. The existence claim covers every n≥1 and every real Jordan matrix J with entirely real spectrum, fixing numerical real eigenvalues as well as block sizes and their eigenvalue grouping. It includes repeated eigenvalues, multiple blocks for the same eigenvalue, nonsemisimple blocks, nilpotent blocks, singleton blocks and J=0.

The resulting tensor is globally C∞ and compactly supported on ℝⁿ. Its matrix is J in a smooth commuting local frame on some nonempty open domain. A coordinate box inside the central band supplies a local domain; no global real-valued angular coordinate system is claimed. The ambient Cartesian matrix is not prescribed. The domain is chosen by the construction, not arbitrarily preassigned. Rank, type and eigenvalues may change elsewhere and the tensor becomes zero. Global algebraic/gl-regularity is not asserted; here regularity in that algebraic sense is distinct from smoothness. There is no nonzero real-analytic compact-support claim.

Conversely, every eigenvalue at every point of a compactly supported smooth real Nijenhuis field on ℝⁿ must be real. This is a global compact-support obstruction, not a prohibition on local nonreal models or on fields without compact support. The paper credits the obstruction to prior literature.

## Construction and proof interface map

For n≥2, use T^(n−1)×(−1,1) with commuting invariant angular fields and a transverse field. In block form L=[[A(t),b(t)],[0,λ(t)]], angular-pair torsions vanish and mixed torsion is precisely (A−λI)A′. The factor order matters. b′ and λ′ have no separate constraint in this ansatz; this does not license an arbitrary position-dependent cutoff of a general tensor.

Lemma 1 chooses a terminal vector of one Jordan block as transverse. The remaining hyperplane is invariant, the distinguished block is shortened, and the lost terminal arrow is retained in b so that the initial matrix is exactly J. After clearing b with A fixed, one processes angular blocks. Move λ to the active eigenvalue with A fixed; remove superdiagonal arrows in predecessor-first order so KK′=0; then move the scalar block to zero with λ matched. Other blocks stay fixed during that stage. Finitely many C∞ switches with genuine endpoint plateaus allow smooth concatenation, including repeated/zero eigenvalues and size-one blocks. There is no division by an eigenvalue or a spectral gap.

The even smooth parameter q(t)=S(2(t²−1/16)) gives the requested J on the central |t|≤1/4 band and exact zero on the |t|≥3/4 bands. This produces real zero neighborhoods for extension, rather than only pointwise zero at the boundary. The torus hypersurface construction is same-dimensional: embed T^d in ℝ^(d+1) by taking the boundary of a small rank-two normal disk bundle of T^(d−1). The displayed normal frame and compact tubular-neighborhood theorem supply the induction. A thin collar of T^(n−1) in ℝⁿ is then an n-dimensional open set. The support lies in the image of the compact interior subcollar, so pushing forward and extending by zero is globally smooth; Nijenhuis torsion is natural and local. n=1 is handled separately by a scalar plateau bump because the alternating two-form torsion vanishes in one dimension.

The necessity argument is the weaker zero-point Lemma 2 on a closed connected manifold. A positive maximum of the imaginary part of a nonreal eigenvalue, then maximal algebraic multiplicity at that maximum, defines a nonempty closed locus. Local spectral splitting and a canonical complex structure give holomorphic characteristic coefficients. The maximum principle makes the sum of imaginary parts constant, then shifted real-root polynomial coefficients constant, making the locus open. Connectedness forces the nonreal eigenvalue at a zero point, a contradiction. Compactly supported L extends by zero near infinity to Sⁿ, where the lemma applies. The paper does not assert real analyticity, gl-regularity or semisimplicity as hypotheses for this lemma.

These mechanisms have been read and mapped, not independently approved here. Standard tubular-neighborhood, smooth-switch, root-continuity and maximum-principle facts are background imports. The paper’s explicit same-dimensional embedding and all boundary/gluing deductions remain with the mathematical reviewers.

## Original problem and fresh primary interfaces

Seven primary PDFs were freshly acquired and hashed: both historical problem author editions, BKM author-v2, Geometry III author-v1/online-first/final issue versions, and Geometry IV author-v1. Exact URLs and read scopes are in primary-source-receipts.json and primary_interfaces.json.

The original question is Problem 5.11, p.29, in arXiv:1804.03737v2 (14 January 2020); in author-v1 (10 April 2018) it is Problem 4.10, p.37. Both actual question bodies and adjacent remarks were inspected. The target is compact support together with unchanged prescribed algebraic type on an open domain. The question already states real semisimple and two-dimensional Jordan examples and the nonreal obstruction. The adjacent everywhere-regular closed-manifold problem is separate. The question’s historical wording supplies no claim of worldwide openness in 2026.

BKM arXiv:1903.04603v2, pp.18–24, supplies admissible coprime local splitting and the canonical complex/holomorphic structure without assuming an algebraically generic point. The splitting block coefficients are independent of complementary coordinates. Its pp.27–28 Theorem 4.5 and remark realize arbitrary types at local points, generically semisimple nearby. This does not by itself give a fixed nonsemisimple type throughout an open domain with compact support. Its pp.41–43 Theorem 6.1 states the stronger persistence of a nonreal eigenvalue with constant multiplicity on a closed connected manifold. The entire source proof was inspected at this interface. The current paper uses the local splitting/holomorphic mechanism for a separate weaker deduction and explicitly avoids adopting a final polynomial-reduction sentence as proof of the whole stronger theorem. Its example under z↦z²+1 concerns that sentence’s literal pair count, not a counterexample to spectral persistence. No conclusion about an unread Advances in Mathematics publisher proof is inferred from author-v2 bytes.

Geometry III’s final issue Theorem 1.10 (p.161; proof interface p.173) corresponds to author-v1 Theorem 1.4, p.7. Definitions and the real-analytic convention were inspected. It concerns regular layers (one Jordan block per eigenvalue) near a nilpotent block and is not a compact-support theorem. The online-first copy also uses 1.10; it has its own hash and pagination. Geometry IV author-v1, Theorems 1.2/1.4 and Lemma 2.3, allows singular or zero symmetry outputs from a gl-regular generator but imposes differential compatibility on functional coefficients. The local triangular formula can involve unwrapped coordinates; it does not by itself ensure periodic angular coefficients or compact zero bands. The paper’s comparison does not exclude every alternative use of that framework.

No exhaustive novelty search is claimed. Older works and later 2025/2026 bodies mentioned as unread in the paper have not been silently certified or equated to consulted versions. Full-result and construction-method priority remain unknown.

## Computational support, candidate and limitations

The current standard-library program encodes rational univariate polynomial stages, ordered block schedules over compositions in dimensions2–6 and several larger examples, independent coordinate first-jet torsion comparisons, and deliberately invalid arrow order, raw cutoffs and unmatched scalar changes. Code review establishes what it attempts to check; no result from it is reported as freshly reproduced. Polynomial stages need the manuscript’s smooth plateau reparameterization argument to become the advertised C∞ glued field. The program does not verify all dimensions, torus embeddings, holomorphicity or the maximum principle.

The complete original abstract is preserved in abstract_original.tex and abstract_original.txt with a source-bound receipt. CONTENT_CANDIDATE.md explains the result and credits earlier work without a firstness claim. It preserves smooth versus analytic, local frame versus Cartesian matrix, chosen domain versus arbitrary domain, and local fixed type versus changing global type. It keeps the manuscript date distinct from the record creation date. Follow-up:null; no unvalidated variant is listed merely to fill a section.

## Strongest verified scope result and remaining gap

The exact five-page current edition and all129 outer members are authenticated unchanged. The74-member nested historical kit has been safely mapped and adds no distinct reader. Complete current mathematics and necessary code support were read; original question and theorem interfaces were checked against fresh primary versions with exact assumptions and numbering. This completes acquisition and editorial scope.

Independent mathematical review must still validate the universal collar schedule, embedding/extension and zero-point argument and reproduce meaningful controls. This scope supplies no mathematical PASS, journal-readiness decision, priority certification or permission to publish. The completed WARM scope and all preceding finalized evidence remain unchanged.
''')

assetchecks=[]
for a in receipt['files']:
 b=(SRC/a['name']).read_bytes()
 assert len(b)==a['bytes'] and hashlib.md5(b).hexdigest()==a['md5'] and hashlib.sha256(b).hexdigest()==a['sha256']
 assetchecks.append({'name':a['name'],**digest(SRC/a['name']),'matches_receipt':True})
count=0
for ar in receipt['archives']:
 with zipfile.ZipFile(SRC/ar['name']) as z:
  for m in ar['members']:
   b=(SRC/'published-source'/m['member']).read_bytes();assert b==z.read(m['member']) and len(b)==m['bytes'] and hashlib.sha256(b).hexdigest()==m['sha256'];count+=1
assert count==129 and digest(SRC/'record.json')['sha256']==receipt['record_sha256']
writej('final_integrity_check.json',{'checked_utc':now,'public_assets':assetchecks,'record_unchanged':True,'zip_extracted_members_compared_byte_for_byte':count,'all_unchanged':True,'outer_pdf_magic_members':magic,'nested_archives':1,'nested_members_crc_and_hash_checked':74,'all_nested_readers_identical_to_main':True,'submitted_checker_executions':0,'scientific_verdict':None})
with (ROOT/'RESEARCH_LOG.md').open('a') as f:f.write(f'\n## {now} — 100%\nAcquisition and scope finalized. Full original abstract, exact claim/limitation map, primary interfaces and conditional page candidate saved. Nested historical74-memberZIP safely inspected; its reader is identical to current five-pagePDF. Every129 outer member and both public assets reauthenticated unchanged. No mathematical PASS, checker execution, repair, new follow-up or publication action. Prior WARM scope preserved.\n')
freeze={'frozen_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'completion_percent':100,'mathematical_verdict':None,'files':{str(p.relative_to(ROOT)):digest(p) for p in sorted(ROOT.rglob('*')) if p.is_file() and 'cache' not in p.relative_to(ROOT).parts and p.name!='SCOPE_FREEZE.json' and '__pycache__' not in p.relative_to(ROOT).parts}}
writej('SCOPE_FREEZE.json',freeze)
print(json.dumps({'status':'SCOPE_COMPLETE','mathematical_verdict':None,'abstract_words':len(plain.split()),'frozen_artifacts':len(freeze['files']),'source_members_unchanged':count,'nested_members':74},indent=2))
