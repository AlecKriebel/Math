from pathlib import Path
import datetime,hashlib,json,re
R=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024');P=R/'papers/23431716';O=P/'reviews/publication';S=P/'sources'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
clearance_path=R/'verification/root-clearance-chip-firing-20261025.json';clearance=json.loads(clearance_path.read_text())
receipt=json.loads((S/'receipt.json').read_text());record=json.loads((S/'record.json').read_text());meta=record['metadata']
assert clearance['status']=='PASS' and clearance['record_id']=='23431716'
assert clearance['source_receipt_sha256']==sha(S/'receipt.json')
for item in receipt['files']:assert sha(S/item['name'])==item['sha256']
texpath=S/'published-source/paper.tex';tex=texpath.read_text();raw=re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}',tex,re.S).group(1)
abstract=' '.join(raw.replace('--','–').split())
assert len(abstract.split())==142
assert abstract==(P/'reviews/scope/abstract_original.txt').read_text().strip()
content={
 'title':meta['title'],
 'slug':'chip-firing-halting-simple-digraphs',
 'description':'An attributed proof that conservative chip-firing halting is NP-complete on simple strongly connected digraphs, including graphs without opposite arcs.',
 'abstract':abstract,
 'plain_language':[
 'Place a pile of chips at each vertex of a directed graph. A vertex can fire when it has enough chips to send one along every outgoing arrow. Firing moves chips without creating or removing any. The question is whether the game can eventually reach a position where no vertex can fire.',
 'This paper proves that deciding whether the game halts is NP-complete even when the graph has no loops or repeated arrows and every vertex can reach every other vertex. A separate construction also forbids arrows pointing in opposite directions between the same two vertices.',
 'The difficulty persists with polynomially many initial chips and a graph that becomes very shallow after removing one specified vertex. The construction encodes a Boolean formula through counters that cycle modulo small primes: a stable position can be reached exactly when the formula has a satisfying assignment.'
 ],
 'result':[
 'The input is a finite loopless simple strongly connected digraph with at least two vertices and an arbitrary nonnegative integer chip configuration encoded in binary. Each vertex fires at its actual outdegree and sends one chip along each outgoing arc. There is no dissipative sink.',
 'HALTING asks whether some finite legal firing sequence reaches a stable configuration. The problem is NP-complete under deterministic polynomial-time many-one reductions. The same conclusion holds for the oriented subclass, which additionally forbids antiparallel arcs.',
 'Hardness holds when a specified root r is supplied and deleting r leaves an acyclic graph with no directed path of two arcs. The reduction also has polynomial numerical total initial chips in the source 3-SAT input length, so the hardness persists when chip counts are written in unary.',
 'Membership in NP covers arbitrary binary chip counts. A certificate records how many times each vertex fires, with polynomially many bits, and certifies a nonnegative stable endpoint. It need not list the full firing sequence.'
 ],
 'why_it_works':[
 'A modular bank stores a number of chips that is largest exactly at selected residues. Its priming specializes the established primed-toppler construction of Holroyd–Levine–Winkler. The prime/Boolean/clause encoding is due to Stockmeyer–Meyer and is also reconstructed by Gramlich.',
 'The proof realizes these counters as an ordinary conservative graph. At each checkpoint, every emitted chip has returned to the correct part of the graph. The root becomes unable to fire precisely when all residue conditions hold. The Chinese remainder theorem connects such a checkpoint to a satisfying Boolean assignment.',
 'A legal checkpoint sequence establishes both directions of the reduction. Classical least action relates this sequence to all legal firing orders, without a fairness assumption. The proof also gives an explicit bound for a short firing-count certificate, using the NP-membership method of Farrell–Levine.'
 ],
 'limitations':[
 'These are worst-case complexity statements. Unless P = NP, no polynomial-time algorithm solves every valid input. This does not mean that every instance is difficult, and the polynomial-bit certificate does not give a polynomial-time simulation of the game.',
 'The theorem does not claim bounded-degree or Eulerian hardness, and it does not concern a fixed graph, a dissipative-sink model, weighted firing thresholds or a specified target configuration. The oriented construction is separate from the simple construction, which allows antiparallel arcs.',
 'The primed-toppler mechanism, prime-residue encoding, root-last stabilization, least action, tree periods and NP-membership method have prior sources. The paper supplies a complete conservative graph realization and halting reduction with those antecedents credited.',
 'Exact full-result and realization priority remain unknown. A bounded source comparison does not establish that the historical question was still open worldwide immediately before this work. Finite computational checks support the written proof; they do not establish the universal theorem by exhaustion.'
 ],
 'background':[
 {'title':'Farrell and Levine, CoEulerian graphs','url':'https://doi.org/10.1090/proc/12952','note':'This work states the historical simple-digraph question and proves NP membership. Its least-action and tree-period methods are credited and reproved here at the required scope.'},
 {'title':'Holroyd, Levine and Winkler, Abelian logic gates','url':'https://arxiv.org/abs/1511.00422v2','note':'Lemma 4.1 supplies the primed-toppler mechanism used by the modular-storage construction. The paper does not claim this mechanism as new.'},
 {'title':'Stockmeyer and Meyer, Word Problems Requiring Exponential Time: Preliminary Report','url':'https://esp.mit.edu/download/827dcf47cbc9cf4a3b04dbf773ea54fb/M3175_meyer-stockmeyer-word-probs.pdf','note':'Theorem 6.1 contains the classical prime/Boolean/clause encoding. The present proof uses its complementary acceptance formulation.'},
 {'title':'Gregor Gramlich, Probabilistic and Nondeterministic Unary Automata','url':'https://ggramlich.github.io/Publications/unaryMFCS03.pdf','note':'Fact 3 reconstructs the same prime-residue encoding and is explicitly credited as a source.'},
 {'title':'Matthew Farrell, The halting problem for chip-firing on finite directed graphs','url':'https://pi.math.cornell.edu/files/Research/SeniorTheses/farrellMatthewThesis.pdf','note':'The thesis supplies prior root-last stabilization and conserved-mass context. Lionel Levine is the thesis adviser, not a coauthor.'},
 {'title':'Kimmo Eriksson, No Polynomial Bound for the Chip Firing Game on Directed Graphs','url':'https://www.ams.org/journals/proc/1991-112-04/S0002-9939-1991-1065944-3/S0002-9939-1991-1065944-3.pdf','note':'Exponentially long games on simple directed graphs with polynomially many initial chips were already known. A short halting certificate should not be confused with a short simulation.'}
 ],
 'collaboration':'I welcome substantive collaboration on independent mathematical review, comparison with the chip-firing and computational-complexity literature, or preparation for journal submission. Expertise in chip-firing dynamics, abelian networks or exact complexity reductions would be especially useful.',
 'follow_up':None,
 'followup_rationale':'No follow-up is proposed. Further graph restrictions would need a separate novelty and feasibility assessment before presenting them as a worthwhile research direction.',
 'publication_date':meta['publication_date'],'version':meta['version'],'doi':meta['doi'],'author':'Alec Kriebel',
 'pdf_filename':'paper.pdf','supplement_filename':'pr1098_support_v1_0.zip','supplement_label':'Source and verification (ZIP)','additional_assets':[],
 'status':'Unrefereed preprint, version 1.0, developed with extensive AI assistance. Exact full-result and realization priority remain unknown.',
 'ai_disclosure':'AI tools were used extensively in solving, checking, adversarial review, source comparison, programming and writing. The author is responsible for the claims. The paper has not received external human peer review or journal acceptance and is not formally certified in a proof assistant.',
 'source_binding':{
  'record_id':'23431716','concept_record_id':str(record['conceptrecid']),'record_url':'https://zenodo.org/records/23431716','doi':meta['doi'],
  'zenodo_version':meta['version'],'manuscript_version':'1.0','manuscript_date':'16 October 2026','publication_date':meta['publication_date'],
  'version_source':'Zenodo metadata specifies version 1.0, and the printed manuscript date line reads Version 1.0, 16 October 2026.',
  'source_retrieved_utc':receipt['retrieved_utc'],'source_receipt_sha256':sha(S/'receipt.json'),'record_sha256':sha(S/'record.json'),
  'pdf_sha256':sha(S/'paper.pdf'),'supplement_sha256':sha(S/'pr1098_support_v1_0.zip'),'files':receipt['files'],
  'reviewed_documents':[{'filename':'paper.pdf','pages':7,'read_scope':'all pages'}],'embedded_assets':[],
  'archive_pdf_identity':'The source archive contains no additional reader PDF or nested archive.',
  'abstract_source':'sources/published-source/paper.tex','abstract_source_sha256':sha(texpath),'abstract_word_count':142,
  'abstract_normalization':'Complete original abstract; whitespace flattened and TeX double hyphens converted to en dashes only. All attribution, priority and AI-review qualifications retained.',
  'frozen_scope_content_path':'reviews/scope/CONTENT_CANDIDATE.md','frozen_scope_content_sha256':sha(P/'reviews/scope/CONTENT_CANDIDATE.md'),
  'review_boundary':'Root scientific clearance is for the exact stated theorem. AI review is not external human peer review, a formal proof-assistant certificate or exhaustive priority certification.'
 },
 'review_metadata':{'prepared_utc':now,'draft_completion_percent':100,'scientific_clearance_received':True,'publication_state':'CLEARED_FOR_LOCAL_PUBLICATION_PREPARATION'}
}
assert content['title']==meta['title'] and content['doi']=='10.5281/zenodo.23431716'
assert r'\date{Version 1.0, 16 October 2026}' in tex
(P/'publication.json').write_text(json.dumps(content,indent=2,ensure_ascii=False)+'\n')
reviews={}
for role,c in clearance['reviews'].items():
 report=P/c['report'];verdict=P/c['verdict_file']
 assert sha(report)==c['report_sha256'] and sha(verdict)==c['verdict_sha256'],role
 reviews[role]={'report':c['report'],'sha256':sha(report),'verdict_file':c['verdict_file'],'verdict_sha256':sha(verdict),'verdict':json.loads(verdict.read_text()),'root_disposition':c['substantive_verdict']}
promotion={
 'record_id':'23431716','status':'PASS','disposition_by':'root','created_utc':now,'approved_scope':clearance['approved_scope'],
 'root_clearance':clearance['authorization'],'root_clearance_file':str(clearance_path.relative_to(R)),'root_clearance_sha256':sha(clearance_path),'root_clearance_record':clearance,
 'pdf_sha256':clearance['pdf_sha256'],'supplement_sha256':clearance['supplement_sha256'],'publication_sha256':sha(P/'publication.json'),
 'source_receipt_sha256':clearance['source_receipt_sha256'],'source_files':receipt['files'],'reviews':reviews,
 'scope_gate_resolution':'The independent scope report remains frozen with no mathematical verdict. Root read all three final reports and the complete published manuscript and issued a separately bound scientific clearance. No source or reviewer verdict was rewritten.',
 'source_repair':False,'human_peer_review':False,'formal_machine_verification':False,'follow_up':None
}
(P/'promotion.json').write_text(json.dumps(promotion,indent=2,ensure_ascii=False)+'\n')
(O/'publication.json').write_bytes((P/'publication.json').read_bytes())
(O/'promotion.json').write_bytes((P/'promotion.json').read_bytes())
with (O/'RESEARCH_LOG.md').open('a') as f:f.write('\n## '+now+' — 55%\nPrepared publication.json with all142 original abstract words and exact approved graph/chip/schedule boundaries. Credited HLW primed topplers, Stockmeyer–Meyer/Gramlich CRT encoding and Farrell–Levine NP membership, plus earlier stabilization/long games. Root clearance and all three complete reviewer verdict JSON objects are hash-bound in promotion.json; original reviewer files untouched. No follow-up or firstness claim.\n')
print(json.dumps({'title':content['title'],'slug':content['slug'],'abstract_words':len(abstract.split()),'publication_sha256':sha(P/'publication.json'),'promotion_sha256':sha(P/'promotion.json'),'review_roles':list(reviews)}))
