from pathlib import Path
import json,re,hashlib
from datetime import datetime,timezone
root=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/papers/22729537')
p=root/'reviews/scope'; src=root/'sources'
r=json.loads((src/'record.json').read_text())['metadata']; receipt=json.loads((src/'receipt.json').read_text())
tex=(src/'published-source/NMSC_Paper_A_Source/manuscript/main.tex').read_text()
abstract=tex.split('\\begin{abstract}',1)[1].split('\\end{abstract}',1)[0].strip().replace('$\\CCR$','CCR').replace('$L$','L').replace('$(L+1)$','(L + 1)').replace('--','–')
abstract='\n\n'.join(' '.join(x.split()) for x in abstract.split('\n\n'))
assert '\\' not in abstract and '$' not in abstract
assets={f['name']:f for f in receipt['files']}
content={
 'title':r['title'],
 'slug':'direct-sequence-laws-network-multispecies-coalescent',
 'description':'What multilocus DNA sequence laws reveal about gene genealogies, and why demographic complexity limits finite-locus identification under the NMSC.',
 'abstract':abstract,
 'plain_language':[
  'Different stretches of DNA can have different family trees, even when sampled from the same species. This paper asks what could be learned from the exact probabilities of every possible DNA alignment, while keeping track of which sites belong to the same nonrecombining stretch.',
  'Under the stated evolutionary model, the complete collection of these probabilities contains exactly the information in the distribution of gene family trees, including their branching times, together with a normalized mutation model. It does not require treating estimated gene trees as observed facts. This is an ideal population-level statement, not a claim that one finite dataset reveals every hidden genealogy.',
  'That information still need not identify a unique species network. Some different histories produce exactly the same distribution of observations. The paper describes the common observable behavior in a finite mathematical representation, called canonical coalescent-response behavior, or CCR.',
  'One especially striking result concerns the length of each DNA stretch. For any chosen length L, the paper constructs two different demographic histories for just two taxa that agree on every alignment probability through length L but disagree at length L + 1. A universal length guarantee therefore has to account for demographic complexity. On a fixed compact class with finitely many specified presentations, a sufficiently long finite locus does determine the full observational equivalence class.'
 ],
 'result':[
  'Fix a finite labelled sampling design with at least two sampled lineages and at least one sample from every terminal taxon. The principal model uses a finite temporal population network, positive finite coalescence rates and epoch durations, inheritance probabilities strictly between zero and one, independent routing of ancestral lineages, independent loci with known nonrecombining boundaries, contemporaneous samples, and one shared irreducible stationary reversible finite-state substitution generator Q.',
  'The complete indexed family of length-L alignment laws is equivalent to the triple (π, Q₀, μ̄), where π is the stationary distribution, Q₀ = Q/(−tr Q), and μ̄ is the law of rooted metric gene genealogies in mutation units. The equivalence is pointwise, including reversible models with repeated eigenvalues, rather than only a generic claim.',
  'Two normalized genealogy laws agree exactly when their CCR representations are isomorphic as typed linear response systems. CCR retains observable coalescence behavior and removes analytically invisible event times; it is not a canonical species graph. The paper proves contextual invisibility of sample-unary funnels and recovers sampled-complete species trees with exactly the demographic rates exposed to at least two ancestral lineages.',
  'Every at-most-one-reticulation presentation has a complete finite port-response quotient. Graph incidences and inheritance weights are recovered on the incidence-separated subclass. The reduced level-1 graph result additionally requires scalar-separator faithfulness and local incidence separation. Parent-corridor demographic histories remain classified by their full response equations, which can have genuine ambiguities.',
  'For each fixed finite union K of compact semianalytic normalized finite-presentation charts, some finite length L*(K) determines the entire indexed family. The proof gives no practical numerical bound. Conversely, with demographic epoch count unbounded, no determining length can depend only on taxon count, reticulation count, alphabet size, and sampling design: exact two-taxon, zero-reticulation collisions exist at every prescribed finite order.'
 ],
 'limitations':[
  'The data object is the exact collection of population alignment laws indexed by locus length. It is stronger than pooled single-site frequencies, gene-tree topology summaries, or a finite empirical alignment.',
  'The principal equivalence assumes a shared stationary reversible mutation process, contemporaneous samples, known locus boundaries, and no recombination within loci. Unknown nonreversible generators, unspecified rate mixtures, and within-locus recombination are outside that theorem.',
  'A change of physical time unit remains possible unless an external calibration fixes it. Other indistinguishable network or demographic histories can remain even after this scale is fixed.',
  'CCR is a finite analytic linear representation of behavior. Its positive cone does not provide a stochastic occupancy basis or an NMSC graph realization. No unconditional level-1, level-2, or general-network graph-recovery theorem is claimed.',
  'Finite determination requires the stated compact semianalytic classes and fixed finite presentations. It does not supply a usable locus-length bound, a global noncompact theorem, or numerical stability. Finite testing of two proposed models additionally assumes exact inputs with a terminating equality test.',
  'The consistency results concern the observational equivalence class under the stated sampling and estimation conditions. The released finite computations support specific identities and examples; they do not certify all universal theorems or establish performance on biological datasets.'
 ],
 'background':[
  {'title':'Allman, Baños and Rhodes (2022), Identifiability of species network topologies from genomic sequences using the logDet distance','url':'https://doi.org/10.1007/s00285-022-01734-2','note':'Earlier direct-sequence work recovers substantial level-1 topology from logDet distances. The present paper instead studies the full indexed collection of within-locus laws under its shared-generator assumptions.'},
  {'title':'Zhu and Degnan (2017), Displayed Trees Do Not Determine Distinguishability Under the Network Multispecies Coalescent','url':'https://doi.org/10.1093/sysbio/syw097','note':'Distinguishability depends on the stochastic observation model, branch-length information, and sampling. The present funnel theorem should not be read as the first discovery of network ambiguity.'},
  {'title':'Yang and Flouri (2022), Estimation of Cross-Species Introgression Rates Using Genomic Data Despite Model Unidentifiability','url':'https://doi.org/10.1093/molbev/msac083','note':'Full-likelihood introgression models already exhibit exact label-switching ambiguities. This provides an important precedent for separating observable behavior from a unique biological parameterization.'},
  {'title':'Allman, Baños, Garrote-López and Rhodes (2024), Identifiability of Level-1 Species Networks from Gene Tree Quartets','url':'https://doi.org/10.1007/s11538-024-01339-4','note':'Quartet concordance factors identify network features while retaining specific ambiguities. Those topology summaries are a different observation object from complete metric-genealogy or indexed sequence laws.'},
  {'title':'Allman, Ané, Baños and Rhodes (2025), Beyond Level-1: Identifiability of a Class of Galled Tree-Child Networks','url':'https://doi.org/10.1007/s11538-025-01545-8','note':'Graph-identifiability results beyond level 1 already exist for restricted network classes and data conditions. The present paper makes no unrestricted higher-level graph claim.'},
  {'title':'Bhaskar and Song (2014), Descartes’ rule of signs and the identifiability of population demographic models from genomic variation data','url':'https://doi.org/10.1214/14-AOS1264','note':'Earlier demographic identifiability bounds explicitly depend on the number of pieces in the history. Their expected site-frequency-spectrum setting differs from the finite linked-locus laws studied here.'},
  {'title':'Siu (1969), Noetherianness of Rings of Holomorphic Functions on Stein Compact Subsets','url':'https://doi.org/10.1090/S0002-9939-1969-0247135-7','note':'Siu’s real-analytic Theorem 2 and compact-semianalytic consequence, following Frisch, provide the established analytic foundation for finite determination on the paper’s compact classes.'}
 ],
 'collaboration':'I welcome substantive collaboration on an independent review of the sequence–genealogy equivalence, the qualified graph-identifiability statements, or the finite-determination argument, as well as work toward a journal submission. Relevant expertise includes phylogenetic identifiability, coalescent theory, and analytic realization theory.',
 'follow_up':None,
 'publication_date':r['publication_date'],
 'version':r['version'],
 'doi':r['doi'],
 'author':'Alec Kriebel',
 'pdf_filename':'NMSC_Paper_A_Main.pdf',
 'supplement_filename':'NMSC_Paper_A_Reproducibility.zip',
 'why_it_works':[
  'Within one locus, all sites share a random genealogy. Their joint probabilities give mixed moments of the conditional site-pattern probabilities. Compact moment determinacy recovers the distribution of those conditional probabilities from all indexed lengths.',
  'Pairwise determinants then give additive gene-tree distances. Contemporaneous sampling restores the root, while reversibility lets a matrix logarithm recover the normalized substitution generator. Finite partition-and-population states describe the resulting coalescence densities; reachable and observable future responses define CCR.',
  'Analyticity on fixed presentations and the Frisch–Siu compact-germ theorem reduce equality of all sequence coordinates to finitely many coordinates on the stated compact classes. For the opposing result, Jukes–Cantor pair probabilities reduce to moments of a transformed coalescence time; a Vandermonde Jacobian produces exact demographic collisions through any chosen order.'
 ],
 'source_binding':{
  'record_id':'22729537','record_url':'https://zenodo.org/records/22729537','doi':'10.5281/zenodo.22729537','version':'1.0.0','zenodo_publication_date':'2026-09-12','manuscript_date':'2026-09-05','source_retrieved_utc':receipt['retrieved_utc'],
  'reviewed_documents':[{'filename':'NMSC_Paper_A_Main.pdf','pages':37,'read_scope':'all pages'},{'filename':'NMSC_Paper_A_Supplement.pdf','pages':27,'read_scope':'all pages'}],
  'files':receipt['files'],
  'abstract_source':'Published main PDF page 1, cross-checked against the abstract in the published source ZIP; typographic normalization only.'
 },
 'additional_assets':[
  {'filename':'NMSC_Paper_A_Supplement.pdf','label':'Technical supplement (PDF, 27 pages)','type':'pdf','role':'technical_supplement','sha256':assets['NMSC_Paper_A_Supplement.pdf']['sha256'],'url':'https://zenodo.org/records/22729537/files/NMSC_Paper_A_Supplement.pdf'},
  {'filename':'NMSC_Paper_A_Source.zip','label':'Complete TeX source (ZIP)','type':'zip','role':'source_archive','sha256':assets['NMSC_Paper_A_Source.zip']['sha256'],'url':'https://zenodo.org/records/22729537/files/NMSC_Paper_A_Source.zip'}
 ],
 'followup_rationale':'No public follow-up is proposed. Unknown stationary nonreversible generator recovery, quantitative bounds or stability, and broader positive graph realization are substantial directions already indicated by the manuscript or established literature, but this scope review has not isolated a new precise conjecture with enough mechanism or evidence to meet the high bar. They should not be added merely to fill a section.',
 'status':'Preprint, version 1.0.0. Independent specialist review welcome.'
}
(p/'content.json').write_text(json.dumps(content,ensure_ascii=False,indent=2)+'\n')
now=datetime.now(timezone.utc).isoformat()
verdict={'record_id':'22729537','role':'independent_publication_scope_and_primary_literature_review','completed_utc':now,'completion_percent':100,'scope_verdict':'content_ready_subject_to_separate_mathematical_gate','mathematical_gate':'not_assessed_by_this_verdict','substantive_defect_found':False,'novelty_certified':False,'peer_review_certified':False,'follow_up':None,'read_scope':{'main_pdf_pages':'1–37','supplement_pdf_pages':'1–27','source_archive':'abstract, bibliography and archive inventory','reproducibility_archive':'README and archive inventory; finite reports not used as proof'},'independence':'No archived or current analytic/adversarial reviewer verdict was consulted. Scope conclusion and content were formed directly from the published main paper, supplement, source metadata, and primary literature.','publication_conditions':['Retain all principal-model assumptions and the all-indexed-length population-law meaning.','Describe CCR as canonical linear behavior, never a general canonical graph.','Retain incidence-separation and scalar-separator-faithfulness qualifications.','Distinguish compact finite determination from an explicit finite bound or practical inference algorithm.','Link both PDFs and both ZIPs.','Use Zenodo date 2026-09-12 while retaining manuscript date 2026-09-05 only as manuscript metadata.'],'files':['content.json','REVIEW.md','verdict.json','RESEARCH_LOG.md']}
(p/'verdict.json').write_text(json.dumps(verdict,ensure_ascii=False,indent=2)+'\n')
print('Wrote content.json and verdict.json; abstract words:',len(abstract.split()))
