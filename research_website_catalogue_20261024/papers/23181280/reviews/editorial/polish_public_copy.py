from pathlib import Path
import json,hashlib
P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
notes={
'23181280':[
'Problem 1 supplies the exact common-tree, whole-root-orientation question; Problem 2 has a different objective.',
'The classical NP-completeness machinery includes satisfiability with at most three literals per clause.',
'Section 6.1 explains the classical Martin formulation and its common-edge/root-orientation variables.',
'Proposition 2 gives the prior spanning-tree lift and its interpretation.'
],
'23442760':[
'The convex-body convergence question is interpreted with explicit unit-mass probability densities.',
'Theorem 11 gives the earlier logarithmic-factor bound; Lemmas 1 and 4 contain the constrained-gradient and quadratic-proxy reductions.',
'The quadratic Taylor upper estimator for general polynomial objectives is an established reduction.',
'The older endpoint-polynomial theorem and shell/core comparison are credited antecedents; the stated older-ingredient deduction is retained.',
'Interval/Jacobi and product-box examples already establish the classical worst-case quadratic exponent.',
'The final overview records a logarithmic factor for general convex bodies; its contents do not certify worldwide openness.'
]}
for rid,credit in notes.items():
 p=P/'papers'/rid;a=p/'reviews/editorial';pub=json.loads((p/'publication.json').read_text())
 for b,n in zip(pub['background'],credit):b['note']=n
 (p/'publication.json').write_text(json.dumps(pub,indent=2,ensure_ascii=False)+'\n')
 prom=json.loads((p/'promotion.json').read_text());prom['publication_sha256']=hashlib.sha256((p/'publication.json').read_bytes()).hexdigest();(p/'promotion.json').write_text(json.dumps(prom,indent=2,ensure_ascii=False)+'\n')
 sec=json.loads((a/'public-sections.json').read_text());sec['background']=pub['background'];sec['publication_config_sha256']=prom['publication_sha256'];(a/'public-sections.json').write_text(json.dumps(sec,indent=2,ensure_ascii=False)+'\n')
 public=f'# {pub["title"]}\n\nAlec Kriebel · ORCID {pub["orcid"]}\n\n{pub["citation_edition_label"]} · Unrefereed preprint · CC BY 4.0\n\n## Original abstract\n\n{pub["abstract"]}\n\n'
 for label,field in [('In plain language','plain_language'),('Main result','result'),('Why it works','why_it_works'),('Scope and prior work','limitations')]:public+='## '+label+'\n\n'+'\n\n'.join(pub[field])+'\n\n'
 public+='## References\n\n'+'\n\n'.join(f'[{b["title"]}]({b["url"]}) {b["note"]}' for b in pub['background'])+'\n\n## Research status\n\n'+pub['ai_disclosure']+'\n\n## Contributions\n\n'+pub['collaboration']+'\n\n## Paper and support\n\n'+pub['reader_intro']+'\n\nDownload the paper and complete source and verification archive from [the selected Zenodo edition]('+pub['source_binding']['record_url']+').\n'
 (a/'PUBLIC_COPY.md').write_text(public)
