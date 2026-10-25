from pathlib import Path
import json,hashlib,re,datetime
BASE=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/papers')
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,obj):p.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
def squash(t):return ' '.join(t.split())
ids=['23441906','23431313']
inputs={}
for id in ids:
 b=BASE/id
 files=[p for p in (b/'sources').rglob('*') if p.is_file()]
 for r in ['analytic','adversarial','scope']:
  files += [p for p in (b/'reviews'/r).iterdir() if p.is_file()]
 inputs[id]={str(p.relative_to(b)):sha(p) for p in files}
# The brace scope's complete abstract is normalized directly against original TeX.
b=BASE/'23441906';d=json.loads((b/'reviews/scope/content.json').read_text())
texpath=b/'sources/published-source/simple-brace-counterexample-source-and-verification/main.tex'
raw=re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}',texpath.read_text(),re.S).group(1).strip()
normalized=squash(raw.replace("Ced\\'o",'Cedó').replace('~',' ').replace('\\,',' ').replace('$','').replace('\\ne','≠').replace('^3','³'))
assert normalized==d['abstract']
d.pop('candidate_gate',None);d['candidate_only']=True
d['status']='Unrefereed preprint, Zenodo version 1.0.0, dated 17 October 2026. Developed with extensive AI assistance; no completed human peer review or formal proof-assistant certification is claimed.'
d['collaboration']='I welcome substantive collaboration from researchers in brace theory, finite groups and the Yang–Baxter equation on independent verification, comparison with earlier constructions and preparation for journal review. Coauthorship would reflect a substantive research contribution and mutual agreement.'
d['follow_up']=None
d['followup_rationale']='No follow-up question is included: the current review does not establish a concrete new direction that meets the requested high bar.'
d['description']='A 20,000-element simple left brace answers Cedó’s two-trivial-factor question using a triple-star obstruction that survives every change of coordinates.'
d['background'][1]['title']='Catino, Colazzo and Stefanelli — Regular subgroups of the affine group and asymmetric product of radical braces'
brace=d
# Nijenhuis uses the full literal original abstract, including its limitations/disclosure.
b=BASE/'23431313';texpath=b/'sources/published-source/paper.tex'
raw_n=re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}',texpath.read_text(),re.S).group(1).strip()
abstract_n=squash(raw_n.replace('$','').replace('\\R^n','ℝⁿ').replace('\\lambda','λ'))
assert abstract_n==squash((b/'reviews/scope/abstract_original.txt').read_text())
nij={
 'title':'A torus-collar proof of the real-spectrum compact-support classification for Nijenhuis operators',
 'slug':'nijenhuis-real-spectrum-compact-support',
 'description':'A smooth torus-collar construction realizes any prescribed real-spectrum Jordan matrix locally in a compactly supported Nijenhuis operator.',
 'abstract':abstract_n,
 'plain_language':[
  'A Nijenhuis operator assigns a linear transformation to each point of a space while satisfying a differential compatibility condition. This paper asks which matrix patterns can hold throughout an open region when the entire field must become exactly zero outside a bounded region.',
  'Every pattern with real eigenvalues can be realized. The construction allows repeated eigenvalues and Jordan blocks of any size, including matrices that cannot be diagonalized. It fixes both the numerical eigenvalues and the block pattern in a suitable local frame.',
  'The difficult step is turning the field off without breaking its compatibility condition. The paper makes that transition in a thin neighborhood of a torus, removing the connections within each Jordan block in a controlled order.',
  'Outside the chosen region, the matrix pattern is allowed to change. The converse is an established obstruction: a smooth compactly supported real Nijenhuis operator cannot have a nonreal eigenvalue anywhere.'
 ],
 'result':[
  'For every integer n ≥ 1 and every prescribed numerical real Jordan matrix J whose eigenvalues are all real, there is a globally C∞, compactly supported real Nijenhuis operator on ℝⁿ whose matrix is J in a smooth commuting local frame on a nonempty open domain.',
  'The construction includes repeated eigenvalues, multiple blocks belonging to the same eigenvalue, blocks of arbitrary size, negative or zero eigenvalues and the zero matrix.',
  'Conversely, every eigenvalue at every point of any smooth compactly supported real Nijenhuis operator on ℝⁿ is real. Together, these statements give the classification asked for in the printed historical problem.',
  'The prescribed numerical matrix is realized on an open domain in the same dimension. The theorem does not prescribe the ambient Cartesian-frame matrix or require one Jordan type throughout the whole space.'
 ],
 'why_it_works':[
  'In a thin torus neighborhood, all coefficients depend on one transverse variable. For the block matrix L = [[A(t), b(t)], [0, λ(t)]], the Nijenhuis condition reduces to the ordered equation (A − λI)A′ = 0.',
  'A finite sequence first removes the transverse coupling, then turns off each Jordan block’s arrows in order and moves its scalar part to zero. Smooth transitions with constant end intervals join these stages and leave exact zero bands at both ends.',
  'An embedded torus collar lies in ℝⁿ in the required dimension. The tensor is pushed into that collar and extended by zero; the zero bands make the extension smooth and compactly supported.',
  'For necessity, the paper uses the established local splitting and holomorphic structure of nonreal spectral blocks in a zero-point rigidity argument. Compact support allows extension to a sphere with a neighborhood on which the tensor is zero.'
 ],
 'limitations':[
  'The result is C∞ smooth. It does not give a nonzero real-analytic compactly supported operator.',
  'The matrix J appears in a smooth commuting local frame on a domain chosen by the construction. The ambient Cartesian-frame matrix and an arbitrarily preassigned realization domain are not prescribed.',
  'Rank, eigenvalues and Jordan type may change outside the realization domain. Global algebraic regularity and a single global Jordan type are not guaranteed; algebraic regularity is distinct from smoothness.',
  'The nonreal obstruction concerns globally compactly supported operators. It does not forbid local models with nonreal eigenvalues or operators without compact support.',
  'Earlier work supplies the nonreal obstruction, real semisimple and two-dimensional examples, local point realizations, and the splitting and holomorphic tools. Historical priority of the full result or this construction is not established.'
 ],
 'background':[
  {'title':'Bolsinov, Matveev, Miranda and Tabachnikov — Open Problems, Questions, and Challenges in Finite-Dimensional Integrable Systems','url':'https://arxiv.org/abs/1804.03737v2','note':'Problem 5.11 in the 2020 author version asks for compact support and a fixed algebraic type on an open domain. It already records the nonreal obstruction and real semisimple and two-dimensional examples.'},
  {'title':'Bolsinov, Konyaev and Matveev — Nijenhuis Geometry','url':'https://arxiv.org/abs/1903.04603v2','note':'Provides local spectral splitting, the canonical complex and holomorphic structure for nonreal blocks, and earlier realizations of arbitrary algebraic types at individual points.'},
  {'title':'Bolsinov, Konyaev and Matveev — Nijenhuis geometry III: gl-regular Nijenhuis operators','url':'https://doi.org/10.4171/RMI/1416','note':'Established local results for regular Jordan layers provide related context. They are distinct from the compact-support transition with arbitrary repeated blocks considered here.'},
  {'title':'Bolsinov, Konyaev and Matveev — Nijenhuis geometry IV','url':'https://arxiv.org/abs/2304.10626v1','note':'Develops symmetries and functional constructions subject to differential compatibility conditions. These earlier methods are credited; the page makes no exhaustive claim about their possible consequences.'}
 ],
 'collaboration':'I welcome substantive collaboration from researchers in Nijenhuis geometry, differential geometry or integrable systems on independent verification, comparison with earlier constructions and preparation for journal review. Coauthorship would reflect a substantive research contribution and mutual agreement.',
 'follow_up':None,
 'followup_rationale':'No follow-up question is included: no independently supported new direction meeting the requested high bar was established.',
 'publication_date':'2026-10-17',
 'version':'1.0','doi':'10.5281/zenodo.23431313','author':'Alec Kriebel',
 'pdf_filename':'paper.pdf','supplement_filename':None,
 'additional_assets':[{'filename':'pr1094_supportkit_v1.0.zip','label':'Source and supporting kit (ZIP)'}],
 'related_resources':[],
 'status':'Unrefereed preprint, Zenodo version 1.0. The manuscript is dated 15 October 2026; the Zenodo record was created on 17 October 2026. Developed with extensive AI assistance, without completed human peer review or formal proof-assistant certification.',
 'ai_disclosure':'AI tools were used extensively in solving, source comparison, verification and writing. Internal AI reviews and finite computational controls do not constitute external human peer review or formal proof-assistant certification.',
 'candidate_only':True
}
for id,d,raw in [('23441906',brace,raw),('23431313',nij,raw_n)]:
 b=BASE/id;dest=b/'reviews/publication';receipt=json.loads((b/'sources/receipt.json').read_text());record=json.loads((b/'sources/record.json').read_text());meta=record['metadata']
 texp=(b/'sources/published-source/paper.tex') if id=='23431313' else (b/'sources/published-source/simple-brace-counterexample-source-and-verification/main.tex')
 for a in receipt['files']:
  p=b/'sources'/a['name'];data=p.read_bytes()
  assert len(data)==a['bytes'] and sha(p)==a['sha256'] and hashlib.md5(data).hexdigest()==a['md5']
 assert sha(b/'sources/record.json')==receipt['record_sha256']
 d['source_binding']={
  'record_id':id,'concept_record_id':str(record['conceptrecid']),'record_url':'https://zenodo.org/records/'+id,'doi':'10.5281/zenodo.'+id,
  'zenodo_version':meta['version'],'manuscript_version':d['version'],'manuscript_date':meta['publication_date'],'zenodo_publication_date':meta['publication_date'],'record_created_utc':record['created'],
  'page_date_basis':'Record creation date is used for the page publication date; the earlier local preparation/manuscript date is preserved separately and is not represented as public availability.' if id=='23431313' else 'Printed manuscript date and Zenodo publication-date metadata agree.',
  'source_retrieved_utc':receipt['retrieved_utc'],'receipt_sha256':sha(b/'sources/receipt.json'),'record_sha256':sha(b/'sources/record.json'),'pdf_sha256':next(a['sha256'] for a in receipt['files'] if a['name']==d['pdf_filename']),
  'supplement_sha256':None,'files':receipt['files'],'source_tex_path':str(texp.relative_to(b)),'source_tex_sha256':sha(texp),
  'reviewed_documents':[{'filename':d['pdf_filename'],'pages':5,'read_scope':'Complete current manuscript; duplicate embedded readers match the same public PDF.'}],
  'abstract_source':'Complete literal abstract from the current published TeX, cross-checked against the frozen scope extraction; only math typography and whitespace normalized, no sentence omitted.',
  'archive_reader_note':'One distinct reader PDF. Outer and historical nested PDF copies are byte-identical.' if id=='23431313' else 'One distinct reader PDF. The embedded main PDF is byte-identical.',
  'publication_state':'Draft only; no root publication clearance or shared-file ownership has been granted.'
 }
 (dest/'original-abstract.tex').write_text(raw+'\n')
 (dest/'original-abstract.txt').write_text(d['abstract']+'\n')
 write(dest/'publication.draft.json',d)
 report_paths=['reviews/analytic/REVIEW.md','reviews/analytic/verdict.json','reviews/adversarial/REVIEW.md','reviews/adversarial/verdict.json']
 report_paths += ['reviews/scope/SCOPE_REVIEW.md','reviews/scope/scope.json','reviews/scope/SCOPE_FREEZE.json'] if id=='23431313' else ['reviews/scope/REVIEW.md','reviews/scope/verdict.json','reviews/scope/content.json']
 bindings={rel:sha(b/rel) for rel in report_paths}
 for family in ['analytic','adversarial']:
  v=json.loads((b/'reviews'/family/'verdict.json').read_text())
  assert v.get('report_sha256')==sha(b/'reviews'/family/'REVIEW.md')
 for rel,digest in inputs[id].items():assert sha(b/rel)==digest
 note='The manuscript and Zenodo metadata give15 October2026, expressly identified as local preparation. The record was created17 October2026 UTC. The draft uses17 October for public-page publication_date, while retaining15 October as the manuscript/metadata date and explaining both in the public status. This avoids a claim of public availability on15 October.' if id=='23431313' else 'Version1.0.0 and17 October2026 agree between the original manuscript and record. No source/edition inconsistency found.'
 preflight={'prepared_utc':now,'record_id':id,'status':'DRAFT_READY_PENDING_ROOT_CLEARANCE','draft_sha256':sha(dest/'publication.draft.json'),'original_tex_abstract_sha256':sha(dest/'original-abstract.tex'),'normalized_complete_abstract_sha256':sha(dest/'original-abstract.txt'),'abstract_words':len(d['abstract'].split()),'abstract_fidelity':'Exact complete source abstract after declared typography/whitespace conversion.','review_bindings':bindings,'source_receipt_sha256':sha(b/'sources/receipt.json'),'record_sha256':sha(b/'sources/record.json'),'source_tex_sha256':sha(texp),'public_asset_checks':[{'name':a['name'],'bytes':a['bytes'],'md5':a['md5'],'sha256':a['sha256'],'status':'MATCH'} for a in receipt['files']],'unchanged_input_files_checked':len(inputs[id]),'immutable_input_inventory_sha256':hashlib.sha256(json.dumps(inputs[id],sort_keys=True).encode()).hexdigest(),'date_note':note,'follow_up':None,'promotion_created':False,'public_files_rendered':False,'site_or_shared_files_modified':False,'clearance_granted':False,'scope':'Editorial preflight only. Drafts remain under reviews/publication; no promotion, public rendering, source/review edits, Git, deployment, Sheet, UI, redirect or outreach action.'}
 write(dest/'draft-bindings.json',preflight)
 (dest/'PREFLIGHT.md').write_text('# Publication draft preflight\n\nPrepared '+now+'. Editorial draft100% complete; publication remains pending root clearance.\n\nThe complete original abstract is retained. All three final review bodies were read, exact version/source bindings were checked, and the draft preserves the reviewed scope, earlier-work credit, concise unrefereed/AI status and a passive invitation for substantive collaboration. Follow-up is null.\n\n'+note+'\n\nOnly this publication draft folder was written for this work. Frozen sources/reviews remain unchanged. No promotion record, public page, shared checker/index/sitemap/CSS, commit, deployment, Sheet update or redirect was created.\n')
 print(json.dumps({'id':id,'draft':str(dest/'publication.draft.json'),'draft_sha256':sha(dest/'publication.draft.json'),'abstract_words':preflight['abstract_words'],'status':preflight['status'],'date_note':note},ensure_ascii=False))
