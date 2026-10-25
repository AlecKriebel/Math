from pathlib import Path
import json,hashlib,re,datetime
b=Path(__file__).resolve().parents[2]; r=b/'reviews/scope'; s=b/'sources'
receipt=json.loads((s/'receipt.json').read_text()); record=json.loads((s/'record.json').read_text())
base=s/'published-source/complete_graph_extremality_db_source_and_certificates/universal_simultaneous_amplification/phase5_exact_threshold/paper_db_extremality'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
tex=(base/'main.tex').read_text(); raw=re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}',tex,re.S).group(1).strip()
(r/'abstract-source.tex.txt').write_text(raw+'\n')
abstract=re.sub(r'\s+',' ',raw).replace('death--Birth','death–Birth').replace('$J_n$','Jₙ').replace('$n\\ge3$','n ≥ 3').replace('$K_4$','K₄')
assert '$' not in abstract and '\\' not in abstract
abstract=abstract.replace(' Second, we close','\n\nSecond, we close')
files=receipt['files']; by={x['name']:x for x in files}
pdf='complete_graph_extremality_db.pdf'; archive='complete_graph_extremality_db_source_and_certificates.tar.gz'; referee='paper_i_complete_graph_extremality_referee_package_2026-08-23_r4.tar.gz'
c={
 'title':record['metadata']['title'],
 'slug':'death-birth-complete-graph-local-optimality',
 'description':'Local complete-graph optimality at fitness two for directed death–Birth replacement, with strong-selection rigidity for every fixed finite population structure.',
 'abstract':abstract,
 'plain_language':[
 'Imagine a population whose connections determine who can replace whom. At each step, one individual dies at random; the possible parents compete to fill that vacancy according to their fitness and connection weights. A mutant has fixed relative fitness r, and fixation means that its descendants eventually occupy the entire population.',
 'The first result concerns a mutant with twice the residents’ fitness. When every individual can replace every other with equal probability, any sufficiently small change to the normalized replacement probabilities lowers the chance that one randomly placed mutant takes over. This holds even for directed changes that treat the two directions differently.',
 'The second result fixes the population structure and makes the mutant increasingly fit. Eventually, every structure gives a lower fixation probability than the well-mixed population unless its replacement probabilities are exactly the well-mixed ones. The result closes the complete-support case left outside the earlier obstruction for graphs with missing connections.',
 'These statements constrain two different ways of changing the model. They do not establish that the complete graph is globally best at fitness two, and they do not rule out a growing sequence of populations whose required size depends on fitness.'
 ],
 'result':[
 'The model is a finite loopless directed weighted graph with positive total incoming weight at every target. Normalize the incoming weights at each target to obtain a row-stochastic replacement kernel P, with the dead target indexing the row. Residents have fitness 1, and the initial state is one mutant placed uniformly among the n vertices.',
 'For every fixed n ≥ 3, Theorem 1 makes the uniform off-diagonal kernel Jₙ a strict nondegenerate local maximizer of fixation probability at r = 2 in the full normalized kernel space. The first derivative vanishes and the second derivative is strictly negative in every nonzero zero-diagonal, row-sum-zero direction, including nonreversible directions.',
 'For a fixed n ≥ 3 with every directed off-diagonal edge positive, Theorem 2 identifies the leading 1/r fixation deficit as a positive constant times a sum of squared differences between incoming weights at the same target. The coefficient vanishes exactly when normalization gives P = Jₙ. In that equality case the entire replacement process agrees with the well-mixed process at every fitness.',
 'Combining that expansion with the existing obstruction for strongly connected noncomplete supports and a source-component argument gives Corollary 3: every fixed normalized kernel P ≠ Jₙ is strictly suppressing for all sufficiently large r. The threshold may depend on P. For n = 2, every admissible loopless normalized kernel already equals J₂.',
 'The paper also proves global maximality at every r > 1 for positive undirected weighted triangles and for two specified symmetric weighted K₄ families. A further necessary condition says that, in a connected undirected graph sequence amplifying at every fixed beneficial fitness eventually, the support degree of a uniformly chosen vertex must tend to infinity in probability.'
 ],
 'why_it_works':[
 'At fitness two, the local replacement event can be represented by an OR of a geometrically distributed number of possible parents. Running these maps backward gives a finite set-valued ancestry process. Its stationary law turns fixation into a coverage probability and then into a stationary collision observable.',
 'At the complete kernel, permutation symmetry splits the curvature into three distinct kinds of perturbation: column imbalance, symmetric balanced changes and antisymmetric circulation. The paper proves the required sign in all three sectors using analytic estimates together with exact rational certificates over explicitly finite ranges.',
 'For strong selection, an expansion of the finite absorption equations isolates a sum of squares measuring unequal competitors for the same death event. The triangle and symmetric K₄ statements use separate exact algebraic certificates.'
 ],
 'limitations':[
 'The fitness-two theorem is local at each fixed population size. It gives no radius uniform in n, global concavity, or global optimality over all directed or undirected kernels. Fitness two is a fixed finite selection strength, not a weak-selection limit.',
 'The strong-selection threshold depends on the fixed structure. Its quantifiers do not exclude one fitness-independent sequence of growing graphs that amplifies for each fixed r > 1 beyond a size threshold depending on r.',
 'The assumptions include death–Birth updating, no self-loops, constant mutant fitness and a uniformly placed single initial mutant. The conclusions are not automatically statements about Birth–death updating, arbitrary initial configurations, frequency-dependent selection or empirical biological populations.',
 'The low-order global results cover positive undirected triangles and the S₁ × S₃ and S₂ × S₂ weighted K₄ families. They do not classify every six-edge weighted K₄. Diverging support degree is necessary for the stated growing-family behavior, not sufficient; very weak positive edges are still support edges.',
 'The all-size local theorem includes finite exact computer-assisted portions. The supplied certificate programs and their integrity checks do not by themselves establish every analytic step or historical priority. The work uses no empirical biological data.'
 ],
 'background':[
 {'title':'Tkadlec, Pavlogiannis, Chatterjee and Nowak (2020), Limits on amplifiers of natural selection under death–Birth updating','url':'https://doi.org/10.1371/journal.pcbi.1007494','note':'Theorem 1 establishes eventual suppression for strongly connected noncomplete directed or weighted supports. The present paper treats the remaining complete-support case and supplies a separate argument for non-strongly-connected supports.'},
 {'title':'Svoboda, Joshi, Tkadlec and Chatterjee (2024), Amplifiers of selection for the Moran process with both Birth-death and death-Birth updating','url':'https://doi.org/10.1371/journal.pcbi.1012008','note':'An earlier construction of growing weighted populations that amplify under both update rules over a bounded fitness interval; it illustrates why fixed-graph and growing-family statements differ.'},
 {'title':'Harris (1978), Additive set-valued Markov processes and graphical methods','url':'https://doi.org/10.1214/aop/1176995523','note':'The manuscript credits the established graphical approach to additive set-valued processes. Its finite fair-geometric construction is given directly in Section 3.'},
 {'title':'Krone and Neuhauser (1997), Ancestral processes with selection','url':'https://doi.org/10.1006/tpbi.1997.1299','note':'Ancestral selection graphs precede this paper. The ancestry method is not claimed as a new general concept.'},
 {'title':'Foo, Gunnarsson, Leder and Sivakoff (2024), Dynamics of advantageous mutant spread in spatial death-birth and birth-death Moran models','url':'https://doi.org/10.1007/s42967-023-00278-6','note':'Earlier spatial death–Birth work constructs the process and its dual on integer lattices. The present manuscript concerns arbitrary finite directed kernels.'},
 {'title':'Kriebel (2026), No universal death–birth amplifier, v1.0.0','url':'https://doi.org/10.5281/zenodo.21753405','note':'The August 2, 2026 software release is the manuscript’s stated predecessor for its strong-selection and low-order results. This consolidated preprint has its own August 25 record and adds the fitness-two theory.'},
 {'title':'Kriebel (2026), Simultaneous amplification beyond fitness three halves','url':'https://doi.org/10.5281/zenodo.21852072','note':'A separate unrefereed companion software release about growing graph families. Its construction is contextual and is not a proof dependency of the present theorems.'}
 ],
 'collaboration':'I welcome substantive collaboration on independent verification of the ancestry construction, curvature certificates and strong-selection argument, comparison with the evolutionary graph theory literature, and preparation for journal review. Expertise in stochastic processes, evolutionary graph theory or exact computer-assisted proofs would be particularly useful.',
 'follow_up':None,
 'followup_rationale':'No new public follow-up is proposed. Global complete-graph maximality at fitness two and all-beneficial-fitness growing-family amplification are explicit open questions in the manuscript. The source does not establish a sufficiently supported new conjecture or concrete mechanism to justify adding a separate follow-up proposal.',
 'publication_date':record['metadata']['publication_date'],'version':record['metadata']['version'],'doi':record['metadata']['doi'],'author':'Alec Kriebel',
 'pdf_filename':pdf,'supplement_filename':archive,'supplement_label':'Source and exact certificates (TAR.GZ)',
 'additional_assets':[
 {'filename':referee,'kind':'tar.gz','label':'Referee and reproduction package (TAR.GZ)'},
 {'filename':archive+'.sha256','kind':'text','label':'Source archive SHA-256'},
 {'filename':referee+'.sha256','kind':'text','label':'Referee package SHA-256'}
 ],
 'status':'Unrefereed preprint, version 1.0.0, developed with extensive AI assistance. No external human peer review or formal proof-assistant certification is claimed.',
 'ai_disclosure':'Generative AI was used substantively in mathematical exploration, derivation, proof analysis, software development, verification, literature support and manuscript preparation. Alec Kriebel is the named author and accepts responsibility for the work. This remains an unrefereed preprint; AI review and computational checks are not external human peer review or formal proof-assistant certification.',
 'edition_note':'The manuscript is dated August 2026. This page cites the consolidated Zenodo preprint published on August 25, 2026, version 1.0.0. The earlier August 2 software release is a separate predecessor record, not this paper’s DOI.',
 'source_binding':{
 'record_id':'22089748','concept_record_id':str(record['conceptrecid']),'record_url':'https://zenodo.org/records/22089748','doi':record['metadata']['doi'],'zenodo_version':record['metadata']['version'],'manuscript_version':None,'manuscript_date':'August 2026','publication_date':record['metadata']['publication_date'],'archive_version_label':'1.0.0','version_source':'Version 1.0.0 and August 25 publication date come from Zenodo. The manuscript prints August 2026 without a numbered version; the referee-package format date August 23 is distinct.','source_retrieved_utc':receipt['retrieved_utc'],'source_receipt_sha256':sha(s/'receipt.json'),'record_metadata_sha256':sha(s/'record.json'),'pdf_sha256':by[pdf]['sha256'],'supplement_sha256':by[archive]['sha256'],'files':files,'primary_tex_path':str((base/'main.tex').relative_to(b)),
 'reviewed_documents':[{'filename':pdf,'pages':30,'read_scope':'Complete manuscript via corresponding full TeX, all seven sections, Appendices A–C and references; PDF text extraction and first-page visual check.'}],
 'support_read_scope':'Current package navigation, claim-to-code map, version, declarations, environment and provenance notes; replay call inventory inspected without executing scientific code. All reader PDFs mapped. Analytic and adversarial validation remain separate.',
 'abstract_source':'Full published abstract from main.tex, cross-checked against page 1; only whitespace, dash and math typography normalized. Added one paragraph break before Second.',
 'archive_pdf_identity':'All four directly present reader PDF occurrences are byte-identical to the 30-page published PDF. The nested source TAR.GZ is also byte-identical to the separately published source archive; there is no distinct supplement PDF.',
 'metadata_related_identifiers':record['metadata'].get('related_identifiers',[]),
 'predecessor':{'record_id':'21753405','doi':'10.5281/zenodo.21753405','publication_date':'2026-08-02','resource_type':'software','distinct_concept_record':True,'inspection':'Fresh metadata only; 455 MB predecessor repository archive not downloaded or used to establish absence/firstness.'},
 'review_boundary':'Independent acquisition, scope and bounded primary-source interface check; not a mathematical gate, novelty certificate or human peer review.'}
}
(r/'content.json').write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n')
sourcepaths=[base/'main.tex',*sorted((base/'sections').glob('*.tex')),*sorted((base/'appendices').glob('*.tex')),base/'references.tex']
binding={'record_id':'22089748','source_receipt_sha256':sha(s/'receipt.json'),'record_json_sha256':sha(s/'record.json'),'source_files':files,'complete_manuscript_sources':[{'path':str(p.relative_to(b)),'sha256':sha(p),'lines':len(p.read_text().splitlines()),'read_scope':'full file'} for p in sourcepaths],'content_sha256':sha(r/'content.json'),'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
(r/'source-bindings.json').write_text(json.dumps(binding,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'abstract_words':len(abstract.split()),'manuscript_files':len(sourcepaths),'content_sha256':sha(r/'content.json'),'all_published_assets':len(files)},indent=2))
