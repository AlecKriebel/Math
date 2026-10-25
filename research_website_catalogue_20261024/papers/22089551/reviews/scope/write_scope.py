from pathlib import Path
import json,re,hashlib
from datetime import datetime,timezone
p=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/papers/22089551');s=p/'sources';w=p/'reviews/scope'
m=json.loads((s/'record.json').read_text())['metadata'];receipt=json.loads((s/'receipt.json').read_text());files={f['name']:f for f in receipt['files']}
t=(s/'published-source/bimolecular_positive_recurrence_submission_v1_2_4/manuscript/paper_content.tex').read_text()
abstract=' '.join(re.findall(r'\\begin\{abstract\}(.*?)\\end\{abstract\}',t,re.S)[1].split())
assert abstract.startswith('Stochastic mass-action reaction networks are chemical-master-equation models')
assert '\\' not in abstract
c={
 'title':m['title'],
 'slug':'positive-recurrence-bimolecular-reaction-networks',
 'description':'Positive recurrence for finite weakly reversible bimolecular stochastic reaction networks with one linkage class, without the pure-species condition.',
 'abstract':abstract,
 'plain_language':[
  'A stochastic reaction network describes molecules being created, consumed, and transformed by random reaction events. This paper asks when such a system has a stationary probability distribution: a consistent long-run distribution of molecule counts within the states it can reach.',
  'The theorem applies when every complex contains at most two molecules and the reaction diagram is strongly connected, so any complex can return to any other through a directed sequence of reactions. It works for any finite number of species and every choice of positive reaction-rate constants. It removes an earlier extra requirement that each species appear by itself in a one- or two-molecule complex.',
  'The surprising point is that stability can emerge over several reactions even when the next jump pushes the population outward. For example, in 0 → A + B → B → 0, a state containing many A molecules but no B can initially only gain molecules. The newly created B then enables a reaction that consumes A. The proof tracks these delayed effects instead of requiring every state to have an immediate inward drift.',
  'For every initial population, the reachable states form one closed communicating class. A nonabsorbing class has finite mean return times and one stationary law; an absorbing state has its point-mass law. This does not mean that individual trajectories stay bounded, that all molecule-count moments are finite, or that equilibrium is reached quickly.'
 ],
 'result':[
  'Let a finite stochastic mass-action reaction network be weakly reversible, have exactly one linkage class, and have molecularity |y| ≤ 2 for every complex y. For every positive rate vector and initial population x₀, the set Γ(x₀) of states reachable by enabled reactions is a closed communicating class. On a nonabsorbing Γ(x₀), the minimal continuous-time Markov chain is nonexplosive and positive recurrent. An absorbing singleton carries its point-mass stationary law.',
  'Consequently, every reachable class has a unique stationary probability distribution. The claim is class-wise: different initial populations can belong to different classes, for example because of conservation or lattice restrictions.',
  'Compared with the single-linkage binary theorem of Anderson, Cappelletti and Kim, the result removes the condition that each species Sᵢ have Sᵢ or 2Sᵢ among the complexes. It retains weak reversibility, one linkage class, and bimolecularity.',
  'The reachability statement uses only weak reversibility: every enabled reaction can be followed by a directed return path that remains enabled at the population level. Positive recurrence requires the additional hypotheses above. Combinatorial return-path existence and finite expected stochastic return time are distinct assertions.'
 ],
 'limitations':[
  'The theorem assumes stochastic mass-action kinetics, a finite network, strictly positive rate constants, one linkage class, and at most two molecules in every complex. It does not settle the full weakly reversible positive-recurrence conjecture for multiple linkage classes or higher molecularity.',
  'The stationary distribution is unique on each reachable class, not necessarily on the entire population state space. Absorbing singletons are handled separately from positive return times in nonabsorbing classes.',
  'The proof gives qualitative recurrence and a regenerative representation of the stationary law. It gives no closed-form or product-form formula, tail bound, exponential ergodicity guarantee, or useful universal mixing-time estimate. Integrability of unbounded molecule-count observables needs a separate argument.',
  'The finite exceptional set used by the proof depends on the network and rates. Its location cannot be bounded by species and complex counts alone uniformly over positive rates. Deterioration of the proof’s drift coefficient is a limitation of that construction, not a lower bound on the system’s true mixing rate.',
  'The supporting computations check finite identities and calibration examples. They do not prove the universal theorem, enumerate its analytic exceptional set, or establish an empirical claim about a particular biological system.',
  'This is an unrefereed preprint developed with substantial generative-AI assistance in mathematical exploration, criticism, computation, and writing. The author is responsible for the claims; the public materials do not replace independent expert peer review.'
 ],
 'background':[
  {'title':'Anderson and Kim (2018), Some Network Conditions for Positive Recurrence of Stochastically Modeled Reaction Networks','url':'https://doi.org/10.1137/17M1161427','note':'Formulates the broader weak-reversibility recurrence conjecture and proves structural sufficient conditions using tier methods. The present paper addresses a specified subclass of that problem.'},
  {'title':'Anderson, Cappelletti and Kim (2020), Stochastically modeled weakly reversible reaction networks with a single linkage class','url':'https://doi.org/10.1017/jpr.2020.28','note':'The direct predecessor proves binary single-linkage recurrence with the extra pure-species condition, using a multi-step embedded-chain argument. The present claimed advance removes that condition.'},
  {'title':'Paulevé, Craciun and Koeppl (2014), Dynamical properties of Discrete Reaction Networks','url':'https://doi.org/10.1007/s00285-013-0686-2','note':'Already establishes symmetric reachability for weakly reversible discrete reaction networks. Its combinatorial use of recurrence is different from finite-mean return in a stochastic process.'},
  {'title':'Anderson, Craciun, Gopalkrishnan and Wiuf (2015), Lyapunov Functions, Stationary Distributions, and Non-equilibrium Potential for Reaction Networks','url':'https://doi.org/10.1007/s11538-015-0102-8','note':'Connects classical reaction-network entropy functions to stochastic stationary distributions. The distinctive ingredient here is subtracting the carried target before applying the log-factorial potential.'},
  {'title':'Xu, On the Regularity of Reaction Systems','url':'https://arxiv.org/abs/2409.05340v3','note':'The current revision establishes nonexplosion for every binary mass-action system, a broader regularity result. Nonexplosion alone does not establish the positive recurrence proved under this paper’s additional graph hypotheses.'},
  {'title':'ConStRAINeD project, announced two-dimensional chemical recurrence theorem','url':'https://constrained.polito.it/publications/','note':'Agazzi, Anderson, Cappelletti, Laurence and Mattingly report a complementary two-species result; their manuscript is listed as in preparation. The present claim allows arbitrarily many species but restricts linkage and molecularity.'}
 ],
 'collaboration':'I welcome substantive collaboration on an independent probability-theoretic review of the marked-target drift argument, its boundary cases, and the conversion to continuous-time recurrence, or on developing a journal submission. Expertise in stochastic reaction networks and Foster–Lyapunov methods would be especially useful.',
 'follow_up':None,
 'publication_date':m['publication_date'],
 'version':m['version'],
 'doi':m['doi'],
 'author':'Alec Kriebel',
 'pdf_filename':'paper-v1.2.4.pdf',
 'supplement_filename':'bimolecular-positive-recurrence-v1.2.4.zip',
 'why_it_works':[
  'After each reaction, the proof records the complex that was just produced. Subtracting that carried target from the population gives a nonnegative residual. A log-factorial potential of the residual changes by exactly the logarithm of a target/source falling-factorial ratio.',
  'A reaction whose source is the carried target changes this potential by zero. Strong connectivity supplies short directed paths of these target-following reactions. A scalar bound propagates a sufficiently negative terminal drift backward through the entire episode, even when intermediate reactions occur on very different scales.',
  'Along any divergent sequence, bimolecularity gives a finite case split: either a useful high-growth source is available over a lower terminal complex, or a linear invariant contradicts divergence within the fixed class. This yields negative expected episode drift outside a finite set. A finite trace-chain argument gives finite mean returns, and repeated visits with positive holding times establish nonexplosion and continuous-time recurrence.'
 ],
 'source_binding':{
  'record_id':'22089551','record_url':'https://zenodo.org/records/22089551','doi':m['doi'],'version':m['version'],'zenodo_publication_date':m['publication_date'],'manuscript_date':'2026-08-22','source_retrieved_utc':receipt['retrieved_utc'],
  'pdf_sha256':files['paper-v1.2.4.pdf']['sha256'],'supplement_sha256':files['bimolecular-positive-recurrence-v1.2.4.zip']['sha256'],
  'files':receipt['files'],
  'reviewed_documents':[{'filename':'paper-v1.2.4.pdf','pages':16,'read_scope':'all pages'},{'filename':'supplementary-note-v1.2.4.pdf','pages':2,'read_scope':'all pages'}],
  'abstract_source':'Published main PDF page 1; cross-checked against the non-JAP abstract branch in manuscript/paper_content.tex. Whitespace normalization only. The separate JAP abstract in the archive is not substituted.',
  'archive_pdf_identity':'Uploaded main PDF is byte-identical to manuscript/main_arxiv.pdf; uploaded supplementary PDF is byte-identical to manuscript/supplementary_note.pdf.'
 },
 'additional_assets':[{'filename':'supplementary-note-v1.2.4.pdf','label':'Supplementary note (PDF, 2 pages)','kind':'pdf','media_type':'application/pdf','bytes':files['supplementary-note-v1.2.4.pdf']['bytes'],'sha256':files['supplementary-note-v1.2.4.pdf']['sha256'],'url':'https://zenodo.org/records/22089551/files/supplementary-note-v1.2.4.pdf'}],
 'followup_rationale':'No follow-up meets the requested high bar. Multiple linkage classes, higher molecularity, and quantitative recurrence estimates are already identified in the manuscript and broader literature. This scope review has not found a new precise conjecture with a persuasive mechanism or preliminary evidence. The failure of the existing path argument across linkage classes and the extra top-complex configurations above molecularity two are real gaps, not routine extensions.',
 'status':'Unrefereed preprint, version 1.2.4, developed with substantial generative-AI assistance. Independent specialist review welcome.'
}
(w/'content.json').write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n')
now=datetime.now(timezone.utc).isoformat()
ex={'created_utc':now,'method':'Fresh pypdf page.extract_text() extraction from the published source-bound PDFs, with one-based page markers','documents':[]}
for name,pages in [('paper-v1.2.4',16),('supplementary-note-v1.2.4',2)]:
 b=(w/(name+'.txt')).read_bytes()
 ex['documents'].append({'source_filename':name+'.pdf','source_sha256':files[name+'.pdf']['sha256'],'pages':pages,'extracted_text_filename':name+'.txt','extracted_text_sha256':hashlib.sha256(b).hexdigest(),'extracted_text_bytes':len(b),'reading_coverage':f'pages 1–{pages}'})
(w/'extraction_receipt.json').write_text(json.dumps(ex,ensure_ascii=False,indent=2)+'\n')
v={'record_id':'22089551','role':'independent_publication_scope_and_primary_literature_review','completed_utc':now,'completion_percent':100,'scope_verdict':'content_ready_subject_to_separate_mathematical_gate','mathematical_gate':'not_assessed_by_this_verdict','substantive_defect_found':False,'novelty_certified':False,'peer_review_certified':False,'follow_up':None,'read_scope':{'main_pdf':'all 16 pages','supplementary_pdf':'both pages','source':'main_arxiv.tex and relevant paper_content.tex abstract/introduction; embedded PDF byte identities and ZIP inventory'},'independence':'No current or archived analytic/adversarial opinions were consulted, including the audits carried in the published ZIP.','publication_conditions':['Retain every graph and kinetics hypothesis.','Present the pure-species-condition removal as the precise claimed advance over Anderson–Cappelletti–Kim.','Do not market nonexplosion or symmetric reachability as new discoveries.','Credit the announced complementary two-species theorem without claiming it has a published manuscript.','Distinguish class-wise stationary laws from bounded trajectories, finite moments, or fast mixing.','Use current Xu v3 regularity title and scope in background while leaving the original abstract unchanged.','Disclose unrefereed status and material AI assistance.'],'files':['content.json','REVIEW.md','verdict.json','RESEARCH_LOG.md','extraction_receipt.json']}
(w/'verdict.json').write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
ref=json.loads(Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/papers/23331395/publication.json').read_text())
assert all(k in c and type(c[k])==type(val) for k,val in ref.items())
print('Wrote content, verdict, extraction receipt. Abstract words:',len(abstract.split()))
