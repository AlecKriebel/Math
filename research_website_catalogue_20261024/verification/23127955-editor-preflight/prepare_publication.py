"""Prepare the independently root-cleared common-tangent page."""
from pathlib import Path
import copy,datetime,hashlib,json,re,zipfile
ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
P=ROOT/'papers/23127955'
SITE=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public/research')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
assert not (P/'publication.json').exists() and not (P/'promotion.json').exists()
candidate=P/'reviews/scope/content.json';c=copy.deepcopy(json.loads(candidate.read_text()))
receipt=json.loads((P/'sources/receipt.json').read_text());record=json.loads((P/'sources/record.json').read_text())
assert receipt['record_sha256']==sha(P/'sources/record.json')
for item in receipt['files']:
 f=P/'sources'/item['name'];assert sha(f)==item['sha256'] and f.stat().st_size==item['bytes']
 assert 'md5:'+hashlib.md5(f.read_bytes()).hexdigest()==item['zenodo_checksum']
with zipfile.ZipFile(P/'sources'/c['supplement_filename']) as z:
 assert z.testzip() is None
 members=[i for i in z.infolist() if not i.is_dir()];assert len(members)==15
 for i in members:assert (P/'sources/published-source'/i.filename).read_bytes()==z.read(i)
assert (P/'sources/published-source/common_tangent_nullness.pdf').read_bytes()==(P/'sources/common_tangent_nullness.pdf').read_bytes()
texpath=P/'sources/published-source/paper.tex';tex=texpath.read_text()
a=re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}',tex,re.S).group(1)
normalized=' '.join(a.replace(r'\R^3','ℝ³').replace('$','').replace('~',' ').split())
assert normalized==' '.join(c['abstract'].split()) and len(normalized.split())==122
c['abstract']=normalized
assert r'\date{3 October 2026\\\small Unrefereed preprint}' in tex
for key in ['title','version','publication_date','doi']:assert c[key]==record['metadata'][key]
assert sha(P/'reviews/scope/verdict.json')=='c5851ea4d6dc5dab9ad6db72be5780dad0e512a0fd463cf61d6ec9e39c5ecb8b'
assert sha(P/'reviews/scope/REVIEW.md')=='491c8667112ca0267ec1db340eceb3f167c9c76a628d9af0ce1475dbe6242960'
reviews={}
for role in ['analytic','adversarial','scope']:
 rp=f'reviews/{role}/REVIEW.md';vp=f'reviews/{role}/verdict.json';v=json.loads((P/vp).read_text())
 assert v['completion_percent']==100 and v['status']==('PASS_SCOPE_ONLY' if role=='scope' else 'PASS')
 if 'report_sha256' in v:assert v['report_sha256']==sha(P/rp)
 if isinstance(v.get('report'),dict):assert v['report']['sha256']==sha(P/rp)
 for item in v.get('artifacts',[]):
  if isinstance(item,dict):assert sha(P/item['path'])==item['sha256']
 reviews[role]={'report':rp,'sha256':sha(P/rp),'verdict_file':vp,'verdict_sha256':sha(P/vp),'verdict':v}
c['orcid']='https://orcid.org/0009-0001-9320-500X'
c['ai_disclosure']='This is an unrefereed preprint. Extensive AI assistance was used in solving, drafting and internal mathematical verification. It has not undergone conventional external human peer review or formal proof-assistant verification.'
c['why_it_works'][0]='The proof first localizes actual contacts to countably many disjoint compact caps. After separating the lower-dimensional cases, it constructs countably many Lipschitz families of lines tangent to two compact convex sets, each described by two parameters. The construction uses support inequalities and a contraction argument, so it does not require smooth boundaries or differentiable support functions.'
c['source_binding'].update({
 'abstract_source':'sources/published-source/paper.tex','abstract_source_sha256':sha(texpath),'abstract_word_count':122,
 'abstract_normalization':'Complete original abstract retained as its single source paragraph; only TeX-to-Unicode and whitespace normalization.',
 'frozen_scope_content_path':'reviews/scope/content.json','frozen_scope_content_sha256':sha(candidate),
 'files':receipt['files'],'embedded_assets':[],
 'version_source':'Zenodo metadata supplies version 1.0. The title page gives 3 October 2026 and Unrefereed preprint, with no numbered edition.',
 'review_boundary':'Root-cleared AI analytic, adversarial and source-scope reviews at the stated theorem; no human peer-review, formal-proof or exhaustive novelty certification.'
})
assert c['follow_up'] is None
save(HERE/'site-before.json',{str(p.relative_to(SITE)):sha(p) for p in SITE.rglob('*') if p.is_file()})
save(P/'publication.json',c)
gate={
 'record_id':'23127955','status':'PASS','disposition_by':'root','created_utc':utc(),
 'approved_scope':'Any three pairwise disjoint convex subsets of R^3, with tangency requiring actual contact and the whole affine line in a supporting plane. The union of complete common tangent lines has three-dimensional Lebesgue outer measure zero, including nonclosed, unbounded, lower-dimensional and nonsmooth inputs. No stronger manifold, rectifiability, Hausdorff-dimension, closedness, line-space measure, higher-dimensional or first-priority claim.',
 'root_clearance':'Explicit final root PASS after all three complete reports and stable 100% scope verdict were read and bound. Publication/promotion/render/local QA authorized; no deployment, Git, sheet or browser action assigned to this editor.',
 'pdf_sha256':c['source_binding']['pdf_sha256'],'supplement_sha256':c['source_binding']['supplement_sha256'],
 'publication_sha256':sha(P/'publication.json'),'source_receipt_sha256':sha(P/'sources/receipt.json'),'source_files':receipt['files'],'reviews':reviews,
 'scope_gate_resolution':'The frozen scope-only candidate and verdict retain their original pending-mathematical-gate wording. Root subsequently read the final mathematical reports and the stable final scope report/verdict, then authorized the exact theorem. Scope records are unchanged.',
 'nonblocking_proof_wording':'The planar intersection height is a smooth function of line coordinates; composition with the Lipschitz family is differentiable at the selected good parameter. Global smoothness in the parameter is neither assumed nor promoted.',
 'source_repair':False,'human_peer_review':False,'formal_machine_verification':False
}
save(P/'promotion.json',gate)
save(HERE/'preflight-bindings.json',{'timestamp':utc(),'status':'PASS','completion_percent':80,'publication_sha256':sha(P/'publication.json'),'promotion_sha256':sha(P/'promotion.json'),'source_receipt_sha256':sha(P/'sources/receipt.json'),'source_tex_sha256':sha(texpath),'abstract_words':122,'source_files_checked':15,'reviews':{k:{a:b for a,b in v.items() if a!='verdict'} for k,v in reviews.items()}})
(HERE/'RESEARCH_LOG.md').write_text('# Common-tangent publication editor\n\n'+utc()+' — 80% complete. Explicit final root PASS received after stable 100% scope binding. All full reports read; the editor also authored the independent adversarial report before seeing sibling opinions. Original PDF/ZIP MD5/size/SHA, all 15 extracted bytes, identical embedded PDF, complete 122-word source abstract and review report/verdict/artifact hashes checked. Candidate preserved with one source paragraph and clearer lower-dimensional qualification; AI/unrefereed status explicit, follow_up null. Pending render, content QA and all-three-page unchanged-file binding. No source/review edits, Git/deploy/sheet/browser/outreach.\n')
print(json.dumps({'status':'PASS','publication_sha256':sha(P/'publication.json'),'promotion_sha256':sha(P/'promotion.json')}))
