"""Prepare two individually root-cleared pages from immutable source editions."""
from pathlib import Path
import copy, datetime, hashlib, json, re, zipfile

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
SITE = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public/research')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p, data): p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def utc(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
TEX = {
 '23127646':'sources/published-source/biconstrained-asymmetry-verification/biconstrained-asymmetry-verification/biconstrained_asymmetry.tex',
 '23191301':'sources/published-source/odd_power_sos_verification/paper.tex'
}
def normalize_abstract(rid, body):
 body=body.replace('$','')
 if rid=='23127646':
  for old,new in [(r'\psi','ψ'),(r'\theta','θ'),(r'\geq','≥')]: body=body.replace(old,new)
  body=body.replace('ψ(x,y)','ψ(x, y)').replace('|ψ(13/27,14/27)-ψ(14/27,13/27)|≥','|ψ(13/27, 14/27) − ψ(14/27, 13/27)| ≥').replace('ψ(1-θ,θ)=1-θ/d(θ)','ψ(1 − θ, θ) = 1 − θ/d(θ)')
 else:
  body=body.replace('q=3','q = 3').replace(r'3\cdot10^{62}','3 · 10^62').replace(r'q\ge3','q ≥ 3').replace(r'220\times220','220 × 220')
 return ' '.join(body.split())

save(HERE/'site-before.json',{str(p.relative_to(SITE)):sha(p) for p in SITE.rglob('*') if p.is_file()})
all_bindings={}
for rid in ('23127646','23191301'):
 p=ROOT/'papers'/rid
 assert not (p/'publication.json').exists() and not (p/'promotion.json').exists()
 cp=p/'reviews/scope'/('candidate-content.json' if rid=='23127646' else 'content.json')
 c=json.loads(cp.read_text());receipt=json.loads((p/'sources/receipt.json').read_text());record=json.loads((p/'sources/record.json').read_text())
 assert receipt['complete'] and len(receipt['files'])==2 and receipt['record_sha256']==sha(p/'sources/record.json')
 for a in receipt['files']:
  f=p/'sources'/a['name'];assert sha(f)==a['sha256'] and f.stat().st_size==a['bytes']
  assert 'md5:'+hashlib.md5(f.read_bytes()).hexdigest()==a['zenodo_checksum']
 archive=next(a for a in receipt['files'] if a['name'].endswith('.zip'))
 with zipfile.ZipFile(p/'sources'/archive['name']) as z:
  assert z.testzip() is None
  members=[i for i in z.infolist() if not i.is_dir()]
  bases=[p/'sources/published-source',p/'sources/published-source'/Path(archive['name']).stem]
  base=next(b for b in bases if all((b/i.filename).is_file() for i in members))
  for i in members: assert (base/i.filename).read_bytes()==z.read(i)
 tex=(p/TEX[rid]).read_text();a=re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}',tex,re.S).group(1)
 assert normalize_abstract(rid,a)==c['abstract']
 assert len(c['abstract'].split())=={'23127646':109,'23191301':123}[rid]
 for key in ['title','version','publication_date','doi']: assert c[key]==record['metadata'][key]
 expected_date={'23127646':r'\date{October 3, 2026}','23191301':r'\date{6 October 2026}'}[rid]
 assert expected_date in tex
 reviews={}
 for role in ['analytic','adversarial','scope']:
  rp=f'reviews/{role}/REVIEW.md';vp=f'reviews/{role}/verdict.json';v=json.loads((p/vp).read_text())
  reviews[role]={'report':rp,'sha256':sha(p/rp),'verdict_file':vp,'verdict_sha256':sha(p/vp),'verdict':v}
  for key in ['report_sha256','review_sha256']:
   if key in v: assert v[key]==sha(p/rp)
  entries=v.get('artifacts',v.get('evidence',[]))
  if isinstance(entries,dict): entries=[{'path':name,'sha256':digest} for name,digest in entries.items()]
  for item in entries:
   if not isinstance(item,dict) or not isinstance(item.get('sha256'),str): continue
   locations=[p/item['path'],p/'reviews'/role/item['path']]
   f=next(q for q in locations if q.exists());assert sha(f)==item['sha256']
 assert reviews['analytic']['verdict']['status']=='PASS'
 av=reviews['adversarial']['verdict'];assert av.get('status',av.get('verdict'))=='PASS'
 sv=reviews['scope']['verdict']
 if rid=='23127646': assert sv['verdict']=='PASS_SCOPE_ONLY'
 else: assert sv['scope_verdict']=='no_publication_scope_defect_identified' and sv['content_sha256']==sha(cp)

 if rid=='23127646':
  content={
   'title':c['title'],'slug':c['slug_suggestion'],
   'description':'Swapping two connection thresholds changes the guaranteed two-step reachability in finite graphs, with a proved gap of at least 1/108.',
   'abstract':c['abstract'],
   'plain_language':[
    'Imagine three groups of vertices, with connections between neighboring groups. Each adjacent pair must meet a minimum connection requirement in both directions. How large a fraction of the first group must at least one vertex in the third group be able to reach in two steps?',
    'Exchanging the two thresholds can change that guarantee. At thresholds 13/27 and 14/27, the guarantees differ by at least 1/108. This is a statement about all eligible finite graphs; looking at two individual examples would not suffice.',
    'The surprising feature is that the proof establishes a definite gap without finding either exact guarantee or deciding which is larger. It obtains an exact boundary formula involving an integer, then uses a known small construction to restrict the possible integers.'
   ],
   'result':[
    'The graph is finite and simple, partitioned into nonempty stable parts A, B and C, with no A–C edges. An (x,y)-biconstrained graph satisfies all four conditions: every A vertex has at least x|B| neighbors in B; every B vertex has at least x|A| neighbors in A and y|C| neighbors in C; every C vertex has at least y|B| neighbors in B.',
    'For each graph, take the largest fraction of A reachable from any single C vertex through B. Each reached A vertex is counted once, however many paths reach it. The function ψ(x,y) is the infimum of this maximum over all eligible finite graphs and partitions. It is the best universal guarantee; its attainment is not assumed in the definition.',
    'The main separation is |ψ(13/27,14/27) − ψ(14/27,13/27)| ≥ 1/108. Neither exact value nor their ordering is asserted.',
    'More generally, for every rational θ with 0 < θ < 1, the paper proves ψ(1−θ,θ) = 1−θ/d(θ), and this value is attained by a finite ordinary graph.',
    'Here d(θ) is the minimum unweighted maximum row degree of a finite binary matrix M with distinct columns and strictly positive rational probability vectors b and q satisfying Mq = θ1 and Mᵀb = θ1. A row degree counts column types, not weighted mass. Rows may repeat and the matrix may be rectangular.'
   ],
   'why_it_works':[
    'On the boundary x+y=1, a vertex in C that misses a vertex in A forces their middle neighborhoods to be complementary. If the maximum reach is below one, this applies to every C vertex and forces exact degree equalities between B and C. Grouping identical neighborhoods produces a regular incidence template. The reverse degree condition from B to A bounds the smallest missed class, giving a lower bound valid for every finite graph.',
    'For the matching upper bound, a template attaining the least integer degree gives weighted vertex types. Strictly positive middle weights preserve the paths between distinct types, and rational weights turn the construction into an ordinary finite graph by replacing types with integer numbers of vertices. This proves the formula and finite attainment.',
    'The seven-type construction of Chudnovsky, Hompe, Scott, Seymour and Spirkl, together with its complement, gives d(13/27) ≤ 4 and d(14/27) ≤ 4. The formula then leaves only finitely many integer possibilities; none give equal guarantees, and every possible absolute gap is at least 1/108.'
   ],
   'limitations':[
    'The boundary formula is stated for rational θ strictly between zero and one. The page makes no claim about irrational boundary parameters, the endpoints, or the full function away from this boundary.',
    'The two integer minima, the two exact ψ-values and their ordering remain unevaluated here. The displayed finite graphs supply upper bounds only and are not claimed to attain the infima. The bound 1/108 is not claimed to be the exact gap.',
    'All four degree inequalities and strict positivity of the rational template weights matter. The known symmetry of the related one-direction function φ is a different result. The inherited seven-type example is credited prior work; the contribution here is the universal rational-boundary formula and its quantitative asymmetry consequence. No exhaustive priority or current-openness certification is claimed.'
   ],
   'background':[
    {'title':'Paul Seymour — Biconstrained graphs, Oberwolfach Report 1/2019','url':'https://ems.press/content/serial-article-files/46780','note':'Printed pages 46–47 give the four degree conditions and ask whether ψ is symmetric.'},
    {'title':'Chudnovsky, Hompe, Scott, Seymour and Spirkl — Concatenating Bipartite Graphs (2022)','url':'https://www.combinatorics.org/ojs/index.php/eljc/article/view/v29i2p47','note':'The finite weighted framework and Figure 1 supply the credited seven-type template. Theorem 2.3 concerns φ symmetry; Theorem 12.2 concerns a special minimal-value case for ψ.'}
   ],
   'collaboration':'I welcome collaboration with researchers in extremal graph theory who would like to examine the boundary formula, its incidence-template argument and relationship to earlier biconstrained results, or help prepare a journal submission.',
   'follow_up':None,'follow_up_reason':c['follow_up_reason'],
   'status':'Unrefereed preprint developed with extensive AI assistance.',
   'ai_disclosure':'Research, proof development, computational checks, literature review and writing were extensively AI-assisted. This is an unrefereed preprint without external human peer review or formal proof-assistant verification. The archive includes the published source and exact computational controls.',
   'author':c['author'],'orcid':c['orcid'],'publication_date':c['publication_date'],'version':c['version'],'doi':c['doi'],
   'pdf_filename':c['pdf']['filename'],'supplement_filename':c['supplement']['filename'],
   'source_binding':{}
  }
 else:
  content=copy.deepcopy(c);content.pop('review_metadata',None)
  content['description']='A finite sextic example shows that requiring a fixed odd power to be a sum of squares need not define a convex set.'
  content['result'][0]+=' Here n counts variables.'
  content['ai_disclosure']='AI tools were used extensively in derivation, literature comparison, reproduction, writing and adversarial verification. This is an unrefereed preprint without human peer review or formal proof-assistant verification. Its mathematical and source claims remain open to independent correction.'
  content['orcid']='https://orcid.org/0009-0001-9320-500X'
 binding=content['source_binding']
 binding.update({
  'record_id':rid,'concept_record_id':str(record['conceptrecid']),'record_url':'https://zenodo.org/records/'+rid,'doi':c['doi'],
  'zenodo_version':c['version'],'manuscript_version':None,'publication_date':c['publication_date'],
  'manuscript_date':{'23127646':'October 3, 2026','23191301':'6 October 2026'}[rid],
  'version_source':'Zenodo metadata supplies version 1.0; the manuscript prints its date without a numbered version.',
  'source_retrieved_utc':receipt['retrieved_utc'],'files':receipt['files'],'embedded_assets':[],
  'pdf_sha256':next(x['sha256'] for x in receipt['files'] if x['name']==content['pdf_filename']),
  'supplement_sha256':archive['sha256'],
  'abstract_source':TEX[rid],'abstract_source_sha256':sha(p/TEX[rid]),'abstract_word_count':len(c['abstract'].split()),
  'abstract_normalization':'Entire published abstract retained; only TeX math commands, delimiters, spacing and mathematical typography normalized.',
  'frozen_scope_content_path':str(cp.relative_to(p)),'frozen_scope_content_sha256':sha(cp),
  'reviewed_documents':[{'filename':content['pdf_filename'],'pages':4 if rid=='23127646' else 6,'read_scope':'all pages by each manuscript reviewer'}],
  'source_extraction_files_bound':len(members),
  'review_boundary':'AI analytic, adversarial and source-scope reviews; not human peer review, formal proof certification or exhaustive novelty certification.'
 })
 assert content['follow_up'] is None
 save(p/'publication.json',content)
 gate={
  'record_id':rid,'status':'PASS','disposition_by':'root','created_utc':utc(),
  'approved_scope':('All finite simple biconstrained tripartite graphs with all four minimum-degree inequalities; exact rational-boundary formula psi(1-theta,theta)=1-theta/d(theta) with finite attainment and positive rational regular templates using unweighted distinct-column row degree. Explicit absolute gap at least 1/108 for 13/27 and 14/27. No exact invariant minima, exact psi values, ordering, sharp-gap or inherited-seed novelty claim.' if rid=='23127646' else 'Explicit nonconvexity of C(3*10^62,6,3) for ordinary real-polynomial SOS using disjoint coefficient-1 modified Motzkin sextics; for each fixed odd q>=3 some finite n(q). Dimension counts variables. Classical seed, cube and separation/product ingredients credited. No common dimension, ternary, smallest-dimension, stubbornness, classification or first-priority claim.'),
  'root_clearance':'Explicit individual root PASS and publication/promotion/render/local-QA authorization received after root read all three complete reports.',
  'pdf_sha256':binding['pdf_sha256'],'supplement_sha256':binding['supplement_sha256'],
  'publication_sha256':sha(p/'publication.json'),'source_receipt_sha256':sha(p/'sources/receipt.json'),'source_files':receipt['files'],
  'reviews':reviews,'scope_gate_resolution':'The frozen scope-only candidate was completed before mathematical gate clearance and retains its historical pending fields. Root subsequently read both final mathematical reports and authorized this precise scope; original scope files were not changed.',
  'source_repair':False,'human_peer_review':False,'formal_machine_verification':False
 }
 save(p/'promotion.json',gate)
 all_bindings[rid]={'publication_sha256':sha(p/'publication.json'),'promotion_sha256':sha(p/'promotion.json'),'source_receipt_sha256':sha(p/'sources/receipt.json'),'source_tex':TEX[rid],'source_tex_sha256':sha(p/TEX[rid]),'abstract_words':len(c['abstract'].split()),'archive_members_checked':len(members),'reviews':{k:{a:b for a,b in v.items() if a!='verdict'} for k,v in reviews.items()}}
save(HERE/'preflight-bindings.json',{'timestamp':utc(),'completion_percent':80,'status':'PASS','papers':all_bindings})
(HERE/'RESEARCH_LOG.md').write_text('# Publication editor — 23127646 and 23191301\n\n'+utc()+' — 80% complete. All six full reports read and exact source abstracts, dates, editions, original asset MD5/size/SHA, ZIP extraction bytes and reviewer report/verdict/evidence hashes rebound. Both have explicit root clearance; publication and promotion records prepared. Abstracts retain 109 and 123 words respectively. Original source/scope/review files unchanged. Pending render, scoped checker extension, content QA and unchanged-file audit. No Git, deployment, spreadsheet, browser or outreach.\n')
print(json.dumps({'status':'PASS','papers':all_bindings},ensure_ascii=False,indent=2))
