from pathlib import Path
import datetime, hashlib, json, re
ROOT=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
NOW=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()

def abstract_from_tex(tex,kind):
    raw=re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}',tex,re.S).group(1).strip()
    text=' '.join(raw.split())
    if kind=='bv':
        replacements={r'\(0\ne h\in k[x]\)':'0≠h∈k[x]',r'\(A_h=k\langle x,Y\rangle/(Yx-xY-h(x))\)':'A_h=k⟨x,Y⟩/(Yx−xY−h(x))',r'\(k\)':'k',r'\(h\)':'h','Batalin--Vilkovisky':'Batalin–Vilkovisky','~':' '}
    else:
        replacements={r"T\'othm\'er\'esz":'Tóthmérész'}
    for a,b in replacements.items():text=text.replace(a,b)
    return raw,text

def finalize(rid,draft,source_tex,scope_path,kind):
    base=ROOT/'papers'/rid;s=base/'sources';out=base/'reviews/publication';record=json.loads((s/'record.json').read_text());m=record['metadata'];receipt=json.loads((s/'receipt.json').read_text())
    assets=receipt.get('files',receipt.get('assets'));main='bv-generators.pdf' if kind=='bv' else 'paper.pdf';support='bv-generators-source-and-verification.zip' if kind=='bv' else 'pr1097_support_v1_0.zip'
    abstract_tex,abstract=abstract_from_tex((s/source_tex).read_text(),kind)
    assert draft['abstract']==abstract,(rid,draft['abstract'],abstract)
    (out/'abstract_original.tex').write_text(abstract_tex+'\n');(out/'abstract_original.txt').write_text(abstract+'\n')
    all_assets=[]
    for item in assets:
        p=s/item['name'];data=p.read_bytes();sha=H(p);md5=hashlib.md5(data).hexdigest()
        assert sha==item['sha256'] and len(data)==item['bytes'] and md5==item['md5']
        all_assets.append({'filename':item['name'],'url':item['url'],'bytes':len(data),'sha256':sha,'md5':md5})
    assert draft['version']==m['version'] and draft['publication_date']==m['publication_date'] and draft['title']==m['title']
    manuscript_date=m['publication_date'];created=record['created'];created_day=created[:10]
    if rid=='23431676':
        date_note='The manuscript and Zenodo metadata are dated 15 October 2026; the Zenodo record was created on 17 October 2026. The earlier date records manuscript preparation, not verified public availability. Neither date establishes first priority.'
        draft['status']='Unrefereed preprint, Zenodo version 1.0. The manuscript is dated 15 October 2026; the Zenodo record was created on 17 October 2026. Developed with extensive AI assistance, without completed human peer review or formal proof-assistant certification.'
    else:
        date_note='The manuscript and declared Zenodo edition are dated 22 October 2026. The Zenodo record was created on the same date. These dates identify this edition; they do not establish first priority.'
        draft['status']='Unrefereed preprint, Zenodo version 1.0.0, dated 22 October 2026. Developed with extensive AI assistance, without completed human peer review or formal proof-assistant certification.'
    draft.update({'doi':m['doi'],'author':'Alec Kriebel','publication_date_label':'Manuscript dated','edition_label':'Version '+m['version'],'citation_edition_label':'Version '+m['version'],'edition_note':date_note,'bibtex_note':f"Unrefereed preprint, version {m['version']}; manuscript and declared Zenodo date {manuscript_date}; Zenodo record created {created_day}",'follow_up':None,'followup_rationale':'No independently justified follow-up meeting the requested high bar was established.','pdf_filename':main,'supplement_filename':None,'additional_assets':[{'filename':support,'label':'Source and verification package (ZIP)'}],'related_resources':[],'candidate_only':True,'candidate_gate':'DRAFT ONLY. Independent review reports are complete; root scientific disposition and publication clearance are pending. This draft does not authorize promotion, rendering, publication or deployment.'})
    draft['source_binding']={'record_id':rid,'concept_record_id':str(record.get('conceptrecid','')),'record_url':f'https://zenodo.org/records/{rid}','doi':m['doi'],'zenodo_version':m['version'],'manuscript_version':draft['version'],'manuscript_date':manuscript_date,'zenodo_publication_date':m['publication_date'],'record_created_utc':created,'receipt_sha256':H(s/'receipt.json'),'metadata_sha256':H(s/'record.json'),'pdf_sha256':H(s/main),'all_public_assets':all_assets,'source_tex_path':'sources/'+source_tex,'source_tex_sha256':H(s/source_tex),'abstract_source':'sources/'+source_tex,'abstract_source_sha256':H(s/source_tex),'abstract_word_count':len(abstract.split()),'abstract_normalization':'Complete original abstract, preserving every sentence; mathematical typography, TeX accents and whitespace only normalized.','reviewed_documents':[{'filename':main,'pages':6,'read_scope':'Complete current published manuscript and full corresponding TeX.'}],'embedded_assets':[],'archive_reader_note':'Embedded paper.pdf is byte-identical to the top-level six-page PDF, not a second publication.','frozen_scope_content_path':str(scope_path.relative_to(base)),'frozen_scope_content_sha256':H(scope_path),'publication_date_policy':{'publication_date':manuscript_date,'publication_date_label':'Manuscript dated','record_created_utc':created,'required_note':date_note,'citation_date_basis':'Preserve the manuscript and declared edition date, explicitly distinguish record creation, and do not infer first public availability or website publication date.'}}
    bindings=[]
    for role in ['analytic','adversarial','scope']:
        for filename in ['REVIEW.md','verdict.json']:
            p=base/'reviews'/role/filename
            assert p.exists(),str(p)
            bindings.append({'role':role,'path':str(p.relative_to(base)),'sha256':H(p)})
    draft['review_metadata']={'prepared_utc':NOW(),'completion_percent':100,'publication_state':'DRAFT_ONLY_PENDING_ROOT_DISPOSITION','scientific_clearance_received':False,'publication_authorized':False,'root_clearance_file':None,'promotion_created':False,'rendered':False,'deployment_authorized_to_editor':False,'review_report_bindings':bindings}
    (out/'publication.draft.json').write_text(json.dumps(draft,ensure_ascii=False,indent=2)+'\n')
    abstract_check={'created_utc':NOW(),'complete_original_abstract_match':True,'normalization':draft['source_binding']['abstract_normalization'],'abstract_word_count':len(abstract.split()),'abstract_source_sha256':H(s/source_tex),'original_tex_excerpt_sha256':H(out/'abstract_original.tex'),'normalized_abstract_sha256':H(out/'abstract_original.txt')}
    (out/'abstract-check.json').write_text(json.dumps(abstract_check,indent=2)+'\n')
    before=json.loads((out/'review-preservation-before.json').read_text());changed=[item['path'] for item in before['files'] if H(base/item['path'])!=item['sha256']];assert not changed,changed
    keys=['title','slug','description','abstract','plain_language','result','why_it_works','limitations','background','collaboration','follow_up','publication_date','version','doi','author','pdf_filename','supplement_filename','additional_assets','status','ai_disclosure','source_binding','related_resources']
    assert all(k in draft for k in keys) and draft['follow_up'] is None
    preflight={'utc':NOW(),'record_id':rid,'status':'READY_DRAFT_ONLY','root_disposition':'PENDING','publication_authorized':False,'scientific_clearance_received':False,'promotion_created':False,'rendered':False,'mandatory_saved_objective_read':'GOAL.md','objective_sha256':H(ROOT/'GOAL.md'),'template_keys_present':True,'complete_original_abstract_match':True,'all_public_assets_included':True,'asset_sha256_md5_size_matches':True,'edition_metadata_match':True,'record_created_distinguished':True,'date_policy':'Manuscript date label; explicit separate record-created timestamp; no public-availability or website-publication backdating.','follow_up':None,'source_pdf_sha256':H(s/main),'source_tex_sha256':H(s/source_tex),'draft_sha256':H(out/'publication.draft.json'),'abstract_sha256':H(out/'abstract_original.txt'),'scope_candidate_sha256':H(scope_path),'sealed_reviews_unchanged':not changed,'preserved_review_artifact_count':len(before['files']),'review_report_bindings':bindings,'shared_files_touched':False,'website_sheet_git_ui_outreach_actions':False,'remaining_work':'Root exact-scope disposition and publication clearance are required before promotion/rendering. No claim is made that this draft is published.'}
    (out/'preflight.json').write_text(json.dumps(preflight,indent=2)+'\n')
    (out/'PREFLIGHT.md').write_text('# Publication preflight — '+rid+'\n\nDraft only, prepared from the complete current six-page manuscript, complete TeX and frozen scope candidate. The complete original abstract is retained. Every public asset is bound by size, MD5 and SHA256; all three completed review reports and verdicts are bound by hash without modifying them.\n\nRoot scientific disposition and publication clearance remain pending. No promotion, render, shared checker/index, website, Git, spreadsheet, UI, redirect, deployment or outreach action was taken. Follow-up is null.\n\n'+date_note+'\n\nMathematical copy is confined to the stated theorem. '+('The BV copy specifies ordinary canonical Hochschild cohomology over characteristic-zero fields and nonzero h; the embedded h=0 polynomial line is explicitly distinct from the abstract polynomial plane.' if kind=='bv' else 'The reachability copy specifies finite nonempty loopless strongly connected directed multigraphs, binary adjacency/multiplicities and nonnegative initial/target configurations, variable vertex count and deterministic polynomial-time many-one reductions. It credits prior coNP membership separately from source HALTING NP-completeness. It makes no simple-graph, unary, bounded-degree or bounded-chip-count classification.')+'\n')
    with (out/'RESEARCH_LOG.md').open('a') as f:f.write('\n## '+NOW()+' —100% of draft-preflight assignment\nFull actual current manuscript and TeX, complete original abstract and scope candidate read. Conditional plain-template copy prepared, with complete abstract, exact domain/attribution, AI/unrefereed disclosure and null follow-up. Dates/version/API assets rechecked; date policy distinguishes manuscript/declared edition from record creation and does not backdate availability. Both public assets verified. All three final report/verdict hashes bound; '+str(len(before['files']))+' pre-existing review artifacts unchanged. Root clearance remains absent; draft is not promoted or rendered. Only this publication folder and the other explicitly assigned publication folder were written.\n')
    freeze={'sealed_utc':NOW(),'record_id':rid,'status':'READY_DRAFT_ONLY','root_disposition':'PENDING','files':[{'path':p.name,'bytes':p.stat().st_size,'sha256':H(p)} for p in sorted(out.iterdir()) if p.is_file() and p.name!='FINAL_HASHES.json']}
    (out/'FINAL_HASHES.json').write_text(json.dumps(freeze,indent=2)+'\n')
    print(json.dumps({'record_id':rid,'draft_sha256':H(out/'publication.draft.json'),'preflight_sha256':H(out/'preflight.json'),'freeze_sha256':H(out/'FINAL_HASHES.json'),'abstract_words':len(abstract.split()),'review_artifacts_preserved':len(before['files'])},indent=2))

bvscope=ROOT/'papers/23572690/reviews/scope/content.json';bv=json.loads(bvscope.read_text())
bv['description']='A characteristic-zero classification of BV generators for the ordinary Hochschild cohomology of polynomial Weyl subalgebras.'
bv['plain_language'][1]='This paper considers a family of algebras governed by one polynomial h. The classification is simple to state: a BV generator exists exactly when h has no repeated irreducible factor. Nonzero constant polynomials are included in the positive case.'
bv['collaboration']='I welcome substantive collaboration from researchers in Hochschild cohomology, noncommutative algebra and BV structures on independent verification, comparison with earlier results and preparation for journal review. Any coauthorship would reflect a substantive contribution to the research.'
bv['limitations'][-1]='Earlier work already ruled out bracket generators for other ordinary Hochschild cohomology algebras. This paper gives a classification for the stated family, with bounded historical coverage. It makes no first-discovery claim.'
finalize('23572690',bv,'published-source/bv-generators-source-and-verification/main.tex',bvscope,'bv')

rcscope=ROOT/'papers/23431676/reviews/scope/candidate.json';sc=json.loads(rcscope.read_text())
reach={
 'title':sc['title'],'slug':sc['suggested_slug'],
 'description':'Legal chip-firing reachability is coNP-complete for loopless strongly connected directed multigraphs with binary multiplicities and nonnegative chip counts.',
 'abstract':sc['abstract_original_complete'],
 'plain_language':[
  'In a chip-firing game, a vertex with enough chips can send chips along all its outgoing arcs. This paper asks whether some finite sequence of legal moves can reach a specified final arrangement.',
  'The result classifies this question as coNP-complete for a precise family of directed multigraphs. Arc multiplicities and chip counts are written in binary, so a compact input can describe very large numbers of parallel arcs and chips. The graph is loopless and strongly connected: every vertex can reach every other along directed paths.',
  'The proof turns the question of whether legal play can continue indefinitely into a specified-target reachability question. It computes the new graph and target directly, without first finding a recurrent arrangement or writing out the potentially very long sequence of moves.'
 ],
 'result':[
  'For finite nonempty loopless strongly connected directed multigraphs, deciding whether a finite sequential legal firing word takes a nonnegative initial configuration to a specified nonnegative target is coNP-complete under deterministic polynomial-time many-one reductions.',
  'The number of vertices varies with the input. Adjacency entries, including arc multiplicities, and both configurations are encoded in binary. The empty firing word is allowed, and a word may stop even when another move remains available. Malformed inputs are rejected.',
  'The reduction supplies coNP-hardness. Prior work by Hujter, Kiss and Tóthmérész supplies coNP membership; the paper explains the earlier certificate argument with attribution.'
 ],
 'why_it_works':[
  'Conservation bounds the number of possible source configurations. A legal word that is long enough must repeat a state, so it can be continued forever. This cutoff can be numerically large while its binary representation stays short.',
  'The new graph simulates the source until a gate has collected enough chips. Firing the gate releases a reserve that lets the remaining prescribed moves reach an explicitly calculated target. A marker ensures that every target-reaching word has fired the gate, even if its other firing counts differ from the intended ones.',
  'The graph and target use polynomially many bits. The reduction computes them without executing the long simulation. The earlier coNP-membership argument gives polynomial-size certificates of nonreachability using reduced firing counts.'
 ],
 'limitations':[
  'Parallel arcs, large degrees and large chip counts are used. No corresponding classification is established for simple graphs, unary encodings, bounded degrees or bounded total chip counts.',
  'The theorem concerns legal reachability of a specified target on a varying input graph. It is not a halting or rotor-routing classification, or a claim about all configurations on one fixed graph.',
  'Both input configurations are nonnegative. Signed intermediate normalization in the hardness proof does not establish coNP membership for every signed formulation.',
  'The cutoff bounds a simulation horizon, not the running time of a reachability algorithm. Finite verification controls supplement the written proof and do not certify it formally.',
  'Source hardness, coNP membership, period deletion, recurrence and reserve-simulation arguments are earlier work. Priority of the complete result or gate/marker mechanism, independent discovery and present worldwide openness remain unestablished.'
 ],
 'background':[
  {'title':'Farrell and Levine — CoEulerian graphs','url':'https://arxiv.org/abs/1502.04690v3','note':'Corollary 3.2 provides NP-completeness of the source HALTING problem and its total-Laplacian hardness interface.'},
  {'title':'Hujter, Kiss and Tóthmérész — On the complexity of the chip-firing reachability problem','url':'https://arxiv.org/abs/1507.03209v4','note':'Theorem 12 already establishes coNP membership. Problem 19 records the historical general-digraph hardness question; Theorem 14 retains a recurrent-target premise.'},
  {'title':'Björner and Lovász — Chip-firing games on directed graphs','url':'https://www.cs.elte.hu/~lovasz/morepapers/abacus.pdf','note':'Earlier period deletion and reduced-firing-count machinery underlie the credited certificate argument.'},
  {'title':'Tóthmérész — Rotor-routing reachability is easy, chip-firing reachability is hard','url':'https://arxiv.org/abs/2102.11970v2','note':'Earlier recurrence-to-reachability conversion and a polynomial-hierarchy barrier are distinct from the directly computed target used here.'},
  {'title':'Kiss and Tóthmérész — Chip-firing games on Eulerian digraphs and NP-hardness of computing the rank of a divisor on a graph','url':'https://arxiv.org/abs/1407.6958v3','note':'Earlier work uses large reserves for finite-horizon simulation. Scaling and reserve simulation in general are not claimed as new.'}
 ],
 'collaboration':'I welcome substantive collaboration from researchers in chip-firing, combinatorics and computational complexity on independent verification, comparison with earlier constructions and preparation for journal review. Any coauthorship would reflect actual research contributions.',
 'publication_date':sc['edition_date'],'version':sc['version'],
 'ai_disclosure':'AI tools were used extensively in solving, checking, source comparison, programming and writing. Internal AI reviews and finite computational controls do not constitute external human peer review, journal acceptance or proof-assistant certification.'
}
finalize('23431676',reach,'published-source/pr1097_support_v1_0/paper.tex',rcscope,'reach')
