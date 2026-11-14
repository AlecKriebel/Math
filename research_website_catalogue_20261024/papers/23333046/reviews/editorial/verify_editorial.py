"""Read-only editorial/native-schema/custody verification, no proof replay."""
from pathlib import Path,PurePosixPath
import copy,hashlib,json,re,zipfile
from pypdf import PdfReader
O=Path(__file__).resolve().parent;T=O.parent.parent;P=T.parent.parent
ROOT=P/'verification/root-clearance-23333046-20261025.json'
ROOT_SHA='56a4dbb028c9017b4df3a559ffb5eefd087dbe312b511c10afee0a2f73d24ff6'
STATUS='PASS_WITH_KNOWN_ANTECEDENTS_AND_EXPLICIT_UNFRAMED_CATEGORY_LIMITS'
GATES=['rendered','deployed','rendered_public_copy_approved','local_http_verified','live_http_verified',
       'browser_verified','native_sheet_publication_verified','public_page_published','root_editorial_clearance_received']
def need(v,m):
 if not v:raise RuntimeError(m)
def load(p):return json.loads(p.read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def binding(p):
 b=p.read_bytes();return dict(bytes=len(b),sha256=sha(b))

def validate(pub,prom,sec,req,ready,root,transport,raw):
 need(root==load(ROOT) and root['status']==STATUS,'Exact full qualified root authority')
 need(pub['title']==ready['title']==raw['metadata']['title'] and raw['id']==23333046,'Exact title/record')
 need(pub['author']=='Alec Kriebel' and pub['orcid']=='https://orcid.org/0009-0001-9320-500X','Sole author/ORCID')
 need(pub['doi']==raw['doi']=='10.5281/zenodo.23333046','Selected DOI')
 need(pub['version']==ready['version']=='1.0' and pub['version_field_present'] is True,'API version')
 need(pub['publication_date']==ready['publication_date']=='2026-10-12','Declared manuscript date')
 sb=pub['source_binding']
 need(sb['source_assets_field']=='all_assets_in_original_order' and
      sb['all_assets_in_original_order']==ready['all_assets_in_original_order'],'Whole native assets')
 need('all_assets' not in sb and 'assets' not in sb,'No asset-schema alias')
 need(sb['source_receipt_original']==prom['source_receipt_original']==ready,'Whole original ready and false/null history')
 assets=ready['all_assets_in_original_order'];ar,pdf=assets
 need([x['original_api_file_object'] for x in assets]==raw['files']==sb['published_file_objects'],'Whole native API file objects/order')
 need([x['original_api_file_object']['key'] for x in assets]==
      ['local_deformation_devissage_source_verification_v1.zip','characteristic_two_counterexample_local_deformation_devissage.pdf'],
      'Original ZIP then PDF')
 need(sb['transport_receipt_original']==prom['transport_receipt_original']==transport and len(transport)==5,
      'Whole five transport objects')
 need(all(x['HTTP_status']==200 and 'body' in x and 'response_headers_in_received_order' in x
          and 'status' not in x for x in transport),'Original HTTP_status/body receipt shape')
 need(sb['source_receipt_sha256']==prom['source_receipt_sha256']==sha((T/'sources/SOURCE_READY.json').read_bytes()),'Readiness bytes')
 need(sb['metadata_path']=='sources/normalized-metadata.json' and
      sb['metadata_sha256']==sha((T/'sources/normalized-metadata.json').read_bytes()),'Existing derivative metadata')
 need(sb['raw_record_path']=='sources/record.raw.json' and
      sb['raw_record_sha256']==sha((T/'sources/record.raw.json').read_bytes()),'Actual raw metadata')
 need(sb['record_created_utc']==ready['created']==raw['created']=='2026-10-13T05:43:05.275367+00:00'
      and sb['record_updated_utc']==ready['updated']==raw['updated'],'Actual creation/update distinction')
 need(sb['manuscript_version'] is None and sb['manuscript_version_printed'] is False and
      sb['zenodo_version']=='1.0','Unprinted manuscript version')
 need(pub['edition_label']==pub['citation_edition_label']=='Zenodo version 1.0' and pub['edition_note']==
      'Manuscript and declared publication date: 12 October 2026. Zenodo records version 1.0; the manuscript prints no version number.',
      'Visible date/edition labels')
 need(pub['pdf_filename']==pdf['original_api_file_object']['key'] and
      pub['supplement_filename']==ar['original_api_file_object']['key'] and pub['pdf_pages']==5,'Selected reader/support')
 need(sb['pdf_sha256']==prom['pdf_sha256']==pdf['sha256'] and
      sb['supplement_sha256']==prom['supplement_sha256']==ar['sha256'],'Original full asset hashes')
 need((sb['public_page_reader_pdf_count'],sb['archive_outer_regular_file_count'],sb['archive_regular_member_occurrences'],
       sb['archive_container_count'],sb['nested_archive_count'],sb['archive_embedded_pdf_count'],sb['total_distinct_reader_pdf_count'])==
      (1,154,154,1,0,1,1),'Complete archive/distinct reader accounting')
 need(pub['license']=='CC BY 4.0' and pub['license_url']=='https://creativecommons.org/licenses/by/4.0/' and
      raw['metadata']['license']['id']=='cc-by-4.0','Actual CC license')
 need('Licence: CC BY 4.0.' in (T/'sources/published-source/local_deformation_devissage_v1/README.md').read_text(),
      'Actual README license grant')
 need(prom['status']==pub['review_metadata']['scientific_clearance_status']==STATUS and
      prom['root_clearance_record']==root and prom['root_clearance_sha256']==ROOT_SHA,'Separate exact root adoption')
 for family,entry in root['reviews'].items():
  original=load(P/entry['verdict']);adopted=prom['reviews'][family]
  need(original==entry['whole_original_custom_verdict']==adopted['verdict'],'Whole custom verdict '+family)
  need(adopted['root_authority_entry']==entry,'Whole root entry '+family)
  need(sha((P/entry['report']).read_bytes())==entry['report_sha256'] and
       sha((P/entry['verdict']).read_bytes())==entry['verdict_sha256'],'Actual complete family bindings')
 for obj in [pub,prom]:need(obj['AA'] is None and obj['canonical_url'] is None and obj['follow_up'] is None,'Null authority/follow-up')
 for obj in [pub['review_metadata'],prom]:need(all(obj[x] is False for x in GATES) and obj['native_sheet_aa_url'] is None,'False later gates')
 need(pub['review_metadata']['scientific_clearance_received'] is True,'Science received separately')
 for key in ['title','description','status','edition_label','edition_note','abstract_heading','abstract','plain_language',
             'result','why_it_works','limitations','background','ai_disclosure','collaboration','reader_intro']:
  need(pub[key]==sec[key],'Entire public paragraph binding '+key)
 need(70<=len(pub['description'])<=200,'SEO description')
 tex=(T/pub['source_binding']['source_tex_path']).read_text()
 original=tex.split('\\begin{abstract}',1)[1].split('\\end{abstract}',1)[0]
 need(sb['abstract_tex']==(O/'ORIGINAL_ABSTRACT.tex').read_text()==original,'Entire exact abstract substring')
 normalized=original
 replacements={r'$\F_4$':'F₄',r'$t\mapsto t/(1+at)$':'t↦t/(1+at)',r'$\F_2$':'F₂','restriction--induction':'restriction–induction'}
 need(sb['abstract_normalization']['exact_presentational_replacements']==replacements,'Exact permitted notation map')
 for a,b in replacements.items():normalized=normalized.replace(a,b)
 need(pub['abstract']==' '.join(normalized.split()) and pub['abstract_heading']=='Original abstract'
      and pub['abstract_is_original'] is True,'Full original indexable abstract')
 result=' '.join(pub['result']);limits=' '.join(pub['limitations']);why=' '.join(pub['why_it_works'])
 for text in ['k=F₄=F₂[u]/(u²+u+1)','G=(k,+)','N=(F₂,+)','ρ(a)(t)=t/(1+at)',
              'local Artinian W(k)-algebras with identified residue field k','nilpotent constant terms',
              'D_N^Q is the actual fixed subfunctor of D_N','complete Noetherian local W(k)-algebra with residue k',
              'no choice of natural maps f:D_N^Q→F←D_Q:g','actual restriction–induction map D_G→D_N^Q×_F D_Q',
              'every tangent dimension of F','does not replace either component by a versal hull']:
  need(text in result,'Literal theorem/category missing: '+text)
 need('both the subgroup and quotient deformation functors are prorepresentable remains unaddressed' in limits and
      'all-recipient tangent collapse are established antecedents' in limits,'Conditional variant/prior limits')
 need('every natural map to a prorepresentable Hom-functor' in why and 'full formal-series argument' in why,
      'Universal mechanism preserved')
 need(len(pub['background'])==4 and all(x in json.dumps(pub['background'],ensure_ascii=False)
      for x in ['Byszewski','Cornelissen','Proposition 4.1','Proposition 6.1','injection collision','naturality']),
      'Substantive known-antecedent credit')
 for text in ['AI tools were used extensively','unrefereed research note','without external human peer review',
              'formal proof-assistant certification','actual research contributions and mutual agreement']:
  need(text in pub['ai_disclosure']+' '+pub['collaboration'],'Disclosure/collaboration')
 bib=(O/'CITATION.bib').read_text();need(pub['prepared_bibtex']==req['prepared_bibtex']==bib and sb['prepared_bibtex_sha256']==sha(bib.encode()),'Exact prepared BibTeX')
 for text in [pub['title'],'date = {2026-10-12}','version = {1.0}',pub['doi'],'0009-0001-9320-500X']:need(text in bib,'Citation identity')
 route='/research/'+pub['slug']+'/';pn=pub['pdf_filename'];zn=pub['supplement_filename']
 pu=pdf['original_api_file_object']['links']['self'];zu=ar['original_api_file_object']['links']['self']
 need(req['planned_path']==route and req['pdf_iframe_count']==1 and req['pdf_local_href']==route+pn and
      req['zip_local_href']==route+zn and req['pdf_original_href']==pu and req['zip_original_href']==zu,'One unchanged reader')
 need([(x['label'],x['href'],x['download']) for x in req['required_links']]==
      [('Open PDF',route+pn,False),('Download PDF',route+pn,True),('Download original PDF from Zenodo',pu,True),
       ('Download complete ZIP',route+zn,True),('Download original complete ZIP from Zenodo',zu,True),('Download BibTeX',route+'citation.bib',True)],
      'All exact open/download links')
 need(req['article_assets']==['index.html',pn,zn,'citation.bib'] and req['extra_assets']==pub['additional_assets']==[],
      'Only original complete assets')
 return True

def controls(values):
 out=[]
 def reject(name,mutate):
  v=copy.deepcopy(values);mutate(v)
  try:validate(*v)
  except (RuntimeError,KeyError,TypeError,IndexError):out.append(dict(name=name,rejected=True))
  else:raise RuntimeError('Accepted changed input: '+name)
 reject('generic scientific PASS',lambda v:v[1].__setitem__('status','PASS'))
 reject('altered whole family verdict',lambda v:v[1]['reviews']['scope']['verdict'].__setitem__('follow_up','new project'))
 reject('dropped analytic category limits',lambda v:v[1]['reviews']['analytic']['verdict'].pop('precise_limits'))
 reject('manufactured original publication authority',lambda v:v[1]['reviews']['adversarial']['verdict'].__setitem__('publication_clearance',True))
 reject('altered complete root entry',lambda v:v[1]['reviews']['scope']['root_authority_entry'].pop('whole_original_custom_verdict'))
 reject('creation substituted for declared date',lambda v:v[0].__setitem__('publication_date','2026-10-13'))
 reject('invented printed version',lambda v:v[0]['source_binding'].__setitem__('manuscript_version','1.0'))
 reject('wrong selected DOI',lambda v:v[0].__setitem__('doi','10.5281/zenodo.23333045'))
 reject('normalized assets alias',lambda v:v[0]['source_binding'].__setitem__('assets',v[0]['source_binding']['all_assets_in_original_order']))
 reject('changed native order',lambda v:v[0]['source_binding']['all_assets_in_original_order'].reverse())
 reject('rewritten source pending-history field',lambda v:v[1]['source_receipt_original'].__setitem__('target_mathematics_not_yet_read',False))
 reject('invented transport status field',lambda v:v[0]['source_binding']['transport_receipt_original'][0].__setitem__('status',200))
 reject('altered native file URL',lambda v:v[0]['source_binding']['all_assets_in_original_order'][1]['original_api_file_object']['links'].__setitem__('self','https://example.invalid/paper.pdf'))
 reject('missing original archive member',lambda v:v[0]['source_binding'].__setitem__('archive_regular_member_occurrences',153))
 reject('identical embedded PDF counted as second reader',lambda v:v[0]['source_binding'].__setitem__('total_distinct_reader_pdf_count',2))
 reject('wrong reader page count',lambda v:v[0].__setitem__('pdf_pages',4))
 reject('truncated original abstract',lambda v:v[0].__setitem__('abstract',v[0]['abstract'].split('.')[0]+'.'))
 def change_both(v,key,index,a,b):
  v[0][key][index]=v[0][key][index].replace(a,b);v[2][key]=copy.deepcopy(v[0][key])
 reject('recipient narrowed to dimension one in both copies',lambda v:change_both(v,'result',2,'every tangent dimension of F','only tangent dimension one'))
 reject('fixed subfunctor replaced by hull in both copies',lambda v:change_both(v,'result',1,'the actual fixed subfunctor','a chosen versal hull'))
 reject('nilpotent coordinate constants forbidden in both copies',lambda v:change_both(v,'result',1,'including changes with nilpotent constant terms','excluding all constant terms'))
 reject('conditional component variant falsely solved in both copies',lambda v:change_both(v,'limitations',1,'remains unaddressed','is also solved'))
 reject('known recipient collapse advertised as new in both copies',lambda v:change_both(v,'limitations',2,'all-recipient tangent collapse are established antecedents','all-recipient tangent collapse are new discoveries'))
 reject('incorrect license',lambda v:v[0].__setitem__('license','CC0'))
 reject('missing prior credit',lambda v:v[0]['background'].pop())
 reject('second iframe',lambda v:v[3].__setitem__('pdf_iframe_count',2))
 reject('missing original PDF download',lambda v:v[3]['required_links'].pop(2))
 reject('download semantics removed',lambda v:v[3]['required_links'][1].__setitem__('download',False))
 reject('ZIP subset link',lambda v:v[3]['required_links'][3].__setitem__('href','selected-sources.zip'))
 reject('incorrect prepared edition',lambda v:v[0].__setitem__('prepared_bibtex',v[0]['prepared_bibtex'].replace('version = {1.0}','version = {1.1}')))
 reject('native AA populated',lambda v:v[1].__setitem__('AA','https://example.invalid/'))
 reject('publication gate advanced',lambda v:v[1].__setitem__('public_page_published',True))
 reject('unsanctioned follow-up',lambda v:v[0].__setitem__('follow_up','Prove all framed variants'))
 return out

def main():
 need(sha(ROOT.read_bytes())==ROOT_SHA,'Root source bytes')
 before=load(O/'ORIGINAL_INPUTS_BEFORE.json')['bindings'];prior=load(O/'PROTECTED_PRIOR_PACKAGES.json')['bindings']
 for path,x in {**before,**prior}.items():need(binding(Path(path))==x,'Original/prior binding changed: '+path)
 for x in load(O/'ORIGINAL_OBJECT_COPIES.json')['objects']:
  need(binding(Path(x['original']))==binding(O/x['copy'])=={k:x[k] for k in ['bytes','sha256']},'Original object copy')
 need(not (T/'sources/record.json').exists() and not (T/'sources/receipt.json').exists(),'Invented source alias')
 pub=load(T/'publication.json');prom=load(T/'promotion.json');sec=load(O/'public-sections.json');req=load(O/'READER_REQUIREMENTS.json')
 ready=load(T/'sources/SOURCE_READY.json');root=load(ROOT);transport=load(T/'sources/api-receipts.json');raw=load(T/'sources/record.raw.json')
 values=[pub,prom,sec,req,ready,root,transport,raw];validate(*values)
 need(prom['publication_sha256']==sha((T/'publication.json').read_bytes()),'Actual publication bytes')
 need(len(PdfReader(Path(ready['selected_actual_PDF']['path'])).pages)==5,'Actual PDF pages')
 for x in ready['all_assets_in_original_order']:
  b=Path(x['path']).read_bytes();obj=x['original_api_file_object']
  need(len(b)==x['bytes']==obj['size'] and sha(b)==x['sha256'] and hashlib.md5(b).hexdigest()==x['md5']==obj['checksum'].split(':',1)[1],
       'Full original API asset')
 members=load(T/'sources/archive-members.json')['members'];need(len(members)==154,'All original regular members')
 with zipfile.ZipFile(ready['all_assets_in_original_order'][0]['path']) as z:
  need(len(z.infolist())==154,'Complete original ZIP')
  for x in members:
   n=x['original_member_name'];p=PurePosixPath(n);need(not p.is_absolute() and '..' not in p.parts,'Original safe path')
   b=z.read(n);need(len(b)==x['bytes'] and sha(b)==x['sha256'] and b==Path(x['extracted_path']).read_bytes(),'Original payload')
  embedded=z.read('local_deformation_devissage_v1/research_note.pdf')
  need(embedded==Path(ready['selected_actual_PDF']['path']).read_bytes(),'One byte-identical embedded reader')
  need(z.read('local_deformation_devissage_v1/research_note.tex')==
       z.read('local_deformation_devissage_v1/evidence/package_review_02/research_note_review_copy.tex'),
       'Original identical TeX copies')
 public=(O/'PUBLIC_COPY.md').read_text()
 for key in ['abstract','status','edition_note','ai_disclosure','collaboration','reader_intro']:need(pub[key] in public,'Full public copy '+key)
 for key in ['plain_language','result','why_it_works','limitations']:need(all(x in public for x in pub[key]),'Public paragraph omission '+key)
 need(pub['prepared_bibtex'].rstrip() in public,'Public exact citation')
 need(not re.search(r'\b(?:SHA256|custody|checkpoint|replay|root-clearance|assert)\b|20261025|HTTP403|39 executions',public,re.I),'Private audit narrative in public copy')
 changed=controls(values);sealed=False
 if (O/'SEAL.json').exists():
  seal=load(O/'SEAL.json');m=load(O/'MANIFEST.json');need(sha((O/'MANIFEST.json').read_bytes())==seal['manifest_sha256'],'Manifest seal')
  for x in m['files']:need(binding(O/x['path'])=={k:x[k] for k in ['bytes','sha256']},'Sealed owned file')
  need({str(p.relative_to(O)) for p in O.rglob('*') if p.is_file() and p.name not in ['MANIFEST.json','SEAL.json']}==
       {x['path'] for x in m['files']},'Owned inventory')
  for n in ['publication.json','promotion.json']:need(binding(T/n)==m['configs'][n],'Sealed config')
  sealed=True
 return dict(status='PASS',original_bindings=len(before),prior_bindings=len(prior),whole_object_copies=17,
             recursive_original_payloads=154,reader_pages=5,changed_input_controls=changed,manifest_checked=sealed,
             source_programs_executed=0,mathematical_replays=0,rendering=False,network=False,native=False,writes=0)
if __name__=='__main__':print(json.dumps(main(),indent=2))
