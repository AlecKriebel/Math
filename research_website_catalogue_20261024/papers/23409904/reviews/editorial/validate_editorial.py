"""Read-only original custody plus in-memory editorial negative controls."""
from pathlib import Path
from copy import deepcopy
from datetime import datetime,timezone
import hashlib,json,re,zipfile
P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024');ID='23409904';D=P/'papers'/ID;E=D/'reviews/editorial'
PDF='global-hessian-realizations-v1.0.pdf';ZIP='global-hessian-realizations-source-verification-v1.0.zip'
def readj(f):return json.loads(f.read_text())
def binding(f):
 b=f.read_bytes();return dict(bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def savej(f,o):f.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
def norm(s):
 s=' '.join(s.split())
 for a,b in [('$M$','M'),('$n$','n'),('$n\\geq1$','n≥1'),('$\\R^{\\binom{2n+4}{3}}$','ℝ^{binomial(2n+4,3)}')]:s=s.replace(a,b)
 return s

def validate(p,r,s,a):
 root=readj(P/'verification/root-clearance-23409904-20261025.json');raw=readj(D/'sources/zenodo-record.raw.json');meta=readj(D/'sources/metadata.normalized.json');receipt=readj(D/'sources/receipt.json');m=raw['metadata'];b=p['source_binding'];good=[];bad=[]
 def ck(name,ok):(good if ok else bad).append(name)
 ck('exact author/title/ORCID',p['title']==m['title'] and p['author']=='Alec Kriebel' and p['orcid']=='https://orcid.org/0009-0001-9320-500X')
 ck('exact declared date/version',p['publication_date']==m['publication_date']=='2026-10-15' and p['version']==m['version']=='1.0')
 ck('separate exact created/updated fields',b['record_created_utc']==raw['created']==root['record_created_utc'] and b['record_updated_utc']==raw['updated'])
 canonical='https://aleckriebel.com/research/global-hessian-realizations-statistical-manifolds/'
 ck('exact canonical slug',p['canonical_url']==canonical and p['slug']=='global-hessian-realizations-statistical-manifolds')
 ck('actual custom metadata paths no aliases',b['metadata_path']=='sources/metadata.normalized.json' and b['record_path']=='sources/zenodo-record.raw.json' and not (D/'sources/record.json').exists() and not (D/'sources/paper.pdf').exists())
 ck('whole original normalized/raw metadata agree',meta['complete_metadata']==raw['metadata'] and meta['complete_actual_file_objects']==raw['files'])
 for key,path in [('metadata_sha256',b['metadata_path']),('record_sha256',b['record_path']),('receipt_sha256',b['receipt_path']),('source_tex_sha256',b['source_tex_path'])]:ck('exact '+key,b[key]==binding(D/path)['sha256'])
 tex=(D/root['source_tex_path']).read_text();at=re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}',tex,re.S).group(1).strip()
 ck('entire original abstract exact normalization',p['abstract']==norm(at) and b['abstract_tex']==at and (E/'abstract-source.tex').read_text()==at+'\n' and p['abstract_heading']=='Original abstract' and p['abstract_is_original'] is True)
 ck('whole frozen initial abstract retained',readj(D/b['frozen_scope_content_path'])['full_original_abstract_TeX']==at and b['frozen_scope_content_sha256']==binding(D/b['frozen_scope_content_path'])['sha256'])
 ck('complete separate later root authority',r['root_clearance_record']==root and r['approved_scope']==root['approved_scope'] and r['status']==root['status']=='PASS' and r['disposition_by']=='root')
 ck('exact original source receipt object',r['source_receipt_record']==receipt and r['source_files']==receipt['files'] and b['files']==receipt['files'])
 ck('all four receipt entries distinct from two published assets',len(b['files'])==4 and b['transport_receipt_entry_count']==4 and b['published_asset_count']==2 and len(raw['files'])==2 and b['published_file_objects']==raw['files']==r['published_file_objects'])
 ck('endpoint entries retain null actual file objects',[(x['filename'],x['actual_file_object']) for x in b['files'] if x['actual_file_object'] is None]==[('versions.raw.json',None),('latest.raw.json',None)])
 for x in b['files']:
  if x['actual_file_object'] is not None:
   ck('actual complete file object '+x['filename'],x['actual_file_object']==next(y for y in raw['files'] if y['key']==x['filename']) and x['requested_url']==x['actual_file_object']['links']['self'] and x['status']==200)
 for lane,v in r['reviews'].items():
  ck('whole original '+lane+' custom verdict',v['verdict']==readj(D/v['verdict_file']) and v['verdict_sha256']==binding(D/v['verdict_file'])['sha256']==root['reviews'][lane]['verdict_sha256'])
  ck('whole separate '+lane+' root authority',v['root_authority_entry']==root['reviews'][lane])
  ck('complete '+lane+' report binding',v['sha256']==binding(D/v['report'])['sha256']==root['reviews'][lane]['report_sha256'])
 ck('six-page selected original reader',p['pdf_filename']==PDF and p['pdf_pages']==6 and b['pdf_sha256']==binding(D/'sources'/PDF)['sha256']==root['pdf_sha256'])
 ck('complete unchanged deposited ZIP',p['supplement_filename']==ZIP and b['supplement_sha256']==binding(D/'sources'/ZIP)['sha256']==root['supplement_sha256'])
 ck('only selected PDF and complete ZIP assets',p['additional_assets']==[] and b['embedded_assets']==[] and b['additional_reader_pdfs']==[] and a['proposed_standalone_assets']==[PDF,ZIP])
 ss={x['id']:x for x in s['sections']}
 ck('all eleven indexable sections',len(ss)==len(s['sections'])==11)
 for id_,key in [('abstract','abstract'),('plain-language','plain_language'),('result','result'),('proof','why_it_works'),('limits','limitations'),('collaborate','collaboration')]:ck('complete '+id_+' prose',ss[id_]['paragraphs']==(p[key] if isinstance(p[key],list) else [p[key]]))
 ck('complete brief status and edition',ss['status']['paragraphs']==[p['ai_disclosure'],p['edition_note']] and len(p['ai_disclosure'].split())<60)
 ck('full prior-credit references',ss['background']['references']==p['background'])
 ck('CC BY header/schema',s['header']['license']==p['license']=='CC BY 4.0' and s['metadata']['license']=='https://creativecommons.org/licenses/by/4.0/')
 ck('citation/canonical/abstract metadata',all(s['metadata'][x]==p[y] for x,y in [('canonical','canonical_url'),('description','description'),('abstract','abstract'),('citation_title','title'),('citation_author','author'),('citation_author_orcid','orcid'),('citation_doi','doi')]) and s['metadata']['citation_pdf_url']==canonical+PDF and s['metadata']['citation_publication_date']=='2026/10/15')
 ck('ScholarlyArticle unrefereed schema',s['metadata']['scholarly_type']=='ScholarlyArticle' and s['metadata']['creativeWorkStatus']=='Unrefereed preprint')
 reader=ss['paper'];links=reader['links'];downloads=[x for x in links if x.get('download') is True]
 ck('one exact selected-reader iframe',sum('iframe' in x for x in s['sections'])==1 and reader['iframe']['src']==canonical+PDF)
 ck('one direct open and two explicit downloads',sum(x.get('role')=='open' for x in links)==1 and links[0]['url']==canonical+PDF and len(downloads)==2 and [x['url'] for x in downloads]==[canonical+PDF,f'https://zenodo.org/records/{ID}/files/{PDF}'])
 ck('correct six-page reader intro',reader['paragraphs']==['Read the complete 6-page paper in the on-page PDF reader.'])
 ck('full ZIP local and original links',[x['url'] for x in ss['materials']['links']]==[canonical+ZIP,f'https://zenodo.org/records/{ID}/files/{ZIP}'])
 ck('prepared complete BibTeX',s['bibtex']==(E/'citation.bib').read_text() and all(x in s['bibtex'] for x in [p['title'],p['doi'],canonical,'version = {1.0}','month = oct',p['bibtex_note']]))
 ck('follow-up and AA null',p['follow_up'] is None and r['follow_up'] is None and s['follow_up'] is None and s['native_sheet_aa_url'] is None and r['native_sheet_aa_url'] is None)
 ck('all public gates pending',not any([r['rendered_copy_verified'],r['live_verified'],r['browser_verified'],p['review_metadata']['rendered'],p['review_metadata']['deployed'],a['rendered'],a['live_verified'],a['browser_verified'],a['native_sheet_mutated'],a['shared_scripts_changed']]))
 result=' '.join(p['result']);proof=' '.join(p['why_it_works']);limits=' '.join(p['limitations']);plain=' '.join(p['plain_language']);public=' '.join([p['abstract'],p['description'],result,proof,limits,plain,p['ai_disclosure'],p['edition_note']])
 ck('full smooth positive boundaryless universal input',all(x in result for x in ['Hausdorff, second-countable','without boundary','one fixed finite dimension n≥1','g positive definite','prescribed ordered mutually g-dual pair of torsion-free']))
 ck('proper global positive ordinary Hessian and dimension',all(x in result for x in ['N=binomial(2n+4,3)>n','one smooth Ψ:U→ℝ with positive ordinary Hessian G=Hess Ψ','proper smooth embedding f:M→U','f*G=g']))
 ck('exact ordered projections and affine flatness',all(x in result for x in ['G-orthogonal tangential projections induce exactly ∇ and ∇*, in that order','both flat and torsion-free on U','does not assert vanishing Levi–Civita curvature']))
 ck('both torsions iff retained',all(x in result for x in ['if and only if both prescribed torsions vanish','Necessity applies separately to each connection']))
 ck('noncompact/disconnected/zero-dimensional endpoints',all(x in result for x in ['No compactness, connectedness or completeness','countable discrete set','empty case is vacuous']))
 ck('finite feature and variable Schur mechanism',all(x in proof for x in ['degree at most three','without a finite atlas or a uniform inverse bound','φ·df=0','λ=1+tr(A⁻¹)‖B‖²_HS','at least (2+t)I','one smooth function','local affine coordinates']))
 ck('essential domain/coordinate/probability/dimension limits',all(x in limits for x in ['nonconvex and incomplete','dual affine coordinates are local','neither global injectivity of ∇Ψ','no fixed finite probability model','N is optimal','not positivity of the scalar value']))
 ck('four final-body and AJLS priority limits',all(x in limits for x in ['final Lê 2006','final Lê 2007','separate Lauritzen Lancaster','Abe','page 239','not deductive inputs','No first solution, first priority','current worldwide openness']))
 ck('finite computation limits without replay narrative',all(x in limits for x in ['Exact finite controls and numerical examples corroborate identities','diagnostic choices rather than proved roundoff bounds']) and 'replay' not in public.lower())
 ck('brief honest extensive-AI disclosure',all(x in p['ai_disclosure'].lower() for x in ['extensively','unrefereed','human','journal peer review','formal proof-assistant','responsible']))
 ck('passive substantive collaboration',all(x in p['collaboration'] for x in ['Substantive','actual research and writing contributions','mutual agreement']) and 'contact' not in p['collaboration'].lower())
 ck('no private public replay/custody narrative',not any(x in public.lower() for x in ['root review','custody','290','220','2026-10-25','replay passed','hash','seal','4/5','native historical','12 sample','reviewer controls']) and not re.search(r'\b[0-9a-f]{64}\b',public))
 return bad,good

def negatives(p,r,s,a):
 actions=[]
 def add(name,fn):actions.append((name,fn))
 add('remove first abstract sentence',lambda p,r,s,a:p.update(abstract=p['abstract'].split('. ',1)[1]))
 add('remove final abstract qualifications',lambda p,r,s,a:p.update(abstract=p['abstract'].rsplit('. ',1)[0]+'.'))
 add('alter original abstract quantifier',lambda p,r,s,a:p.update(abstract=p['abstract'].replace('both torsions','one torsion')))
 add('wrong Original abstract heading',lambda p,r,s,a:p.update(abstract_heading='Summary'))
 add('wrong version',lambda p,r,s,a:p.update(version='1.1'))
 add('creation date substituted for declared',lambda p,r,s,a:p.update(publication_date='2026-10-16'))
 add('wrong ORCID',lambda p,r,s,a:p.update(orcid='unknown'))
 add('wrong canonical',lambda p,r,s,a:p.update(canonical_url='https://aleckriebel.com/research/other/'))
 add('truncate original scope verdict',lambda p,r,s,a:r['reviews']['scope'].update(verdict={}))
 add('truncate original analytic uppercase-VERDICT object',lambda p,r,s,a:r['reviews']['analytic'].update(verdict={}))
 add('manufacture original adversarial PASS',lambda p,r,s,a:r['reviews']['adversarial']['verdict'].update(manufactured_pass=True))
 add('rewrite later exact root authority',lambda p,r,s,a:r['root_clearance_record'].update(status='EDITORIAL_PASS'))
 add('drop original version-endpoint receipt',lambda p,r,s,a:r['source_receipt_record']['files'].pop())
 add('invent receipt transport alias',lambda p,r,s,a:r['source_receipt_record']['files'][0].update(http_status=200))
 add('misclassify four receipts as four published assets',lambda p,r,s,a:p['source_binding'].update(published_asset_count=4))
 add('omit original separate root lane object',lambda p,r,s,a:r['reviews']['scope'].update(root_authority_entry={}))
 add('add private standalone asset',lambda p,r,s,a:p['additional_assets'].append({'filename':'primary.pdf'}))
 add('drop license schema',lambda p,r,s,a:s['metadata'].update(license=''))
 add('omit BibTeX',lambda p,r,s,a:s.update(bibtex=''))
 add('invent follow-up',lambda p,r,s,a:p.update(follow_up='new solution campaign'))
 add('manufacture live pass',lambda p,r,s,a:r.update(live_verified=True))
 add('wrong reader page count',lambda p,r,s,a:p.update(pdf_pages=7))
 add('omit Zenodo download',lambda p,r,s,a:next(x for x in s['sections'] if x['id']=='paper')['links'].pop())
 add('substitute historical iframe',lambda p,r,s,a:next(x for x in s['sections'] if x['id']=='paper')['iframe'].update(src='history.pdf'))
 add('omit original full ZIP',lambda p,r,s,a:next(x for x in s['sections'] if x['id']=='materials')['links'].pop())
 def both(p,s,key,section,old,new):
  p[key]=[x.replace(old,new) for x in p[key]];next(x for x in s['sections'] if x['id']==section)['paragraphs']=deepcopy(p[key])
 add('remove properness from both public views',lambda p,r,s,a:both(p,s,'result','result','proper smooth embedding f:M→U','smooth immersion f:M→U'))
 add('replace one global potential by local potentials',lambda p,r,s,a:both(p,s,'result','result','one smooth Ψ:U→ℝ','a family of local potentials'))
 add('reverse prescribed ordering',lambda p,r,s,a:both(p,s,'result','result','exactly ∇ and ∇*, in that order','exactly ∇* and ∇, in that order'))
 add('omit one necessary torsion',lambda p,r,s,a:both(p,s,'result','result','both prescribed torsions vanish','one prescribed torsion vanishes'))
 add('replace pointwise correction by constant',lambda p,r,s,a:both(p,s,'why_it_works','proof','λ=1+tr(A⁻¹)‖B‖²_HS','λ=1'))
 add('lose unresolved final-body priority limit',lambda p,r,s,a:both(p,s,'limitations','limits','final Lê 2006 article','resolved historical paper'))
 out=[]
 for name,fn in actions:
  pp,rr,ss,aa=map(deepcopy,(p,r,s,a));fn(pp,rr,ss,aa);bad,good=validate(pp,rr,ss,aa);assert bad,('control accepted',name);out.append(dict(name=name,rejected=True,failed_invariants=bad))
 return out

if __name__=='__main__':
 p=readj(D/'publication.json');r=readj(D/'promotion.json');s=readj(E/'public-sections.json');a=readj(E/'SCHEMA_ADAPTER.json');bad,good=validate(p,r,s,a);assert not bad,bad;neg=negatives(p,r,s,a)
 members=[]
 with zipfile.ZipFile(D/'sources'/ZIP) as z:
  for i in z.infolist():
   if i.is_dir():continue
   f=D/'sources/published-source'/i.filename;data=z.read(i);assert f.is_file() and f.read_bytes()==data
   members.append(dict(member=i.filename,bytes=len(data),sha256=hashlib.sha256(data).hexdigest()))
 for x in readj(D/'sources/receipt.json')['files']:
  data=(D/'sources'/x['filename']).read_bytes();assert len(data)==x['bytes'] and hashlib.sha256(data).hexdigest()==x['sha256'] and hashlib.md5(data).hexdigest()==x['md5']
  if x['actual_file_object'] is not None:assert len(data)==x['actual_file_object']['size'] and 'md5:'+hashlib.md5(data).hexdigest()==x['actual_file_object']['checksum']
 before=readj(E/'inputs-before.json')['original_input_bindings'];after={n:binding(P/n) for n in before};assert before==after
 now=datetime.now(timezone.utc).isoformat();savej(E/'custody-before-after.json',dict(utc=now,before=before,after=after,all_unchanged=True,unrelated_mutable_site_or_core_frozen=False));savej(E/'editorial-validation.json',dict(utc=now,status='PASS_EDITORIAL_CONSISTENCY_ONLY',positive_invariants=good,positive_count=len(good),negative_controls=neg,negative_controls_rejected=len(neg),fixture_copies=0,archive_members=members,archive_regular_members_compared=len(members),original_binding_count=len(before),all_original_bindings_preserved=True,source_programs_run=False,rendered=False,live_verified=False,browser_verified=False,native_sheet_mutated=False,native_AA=None))
 print(len(good),'positive invariants;',len(neg),'changed-object controls rejected;',len(members),'members exact;',len(before),'frozen originals unchanged')
