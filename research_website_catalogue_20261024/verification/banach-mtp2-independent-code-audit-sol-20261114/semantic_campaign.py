#!/usr/bin/env python3
"""Read-only, new-record-only positive and fault probes against candidate code.

Faults live only in memory: no page, asset, source, config, site or stage write.
Absent old navigation targets are read from the real baseline, never copied.
"""
from pathlib import Path
from html import escape
import copy,hashlib,json,sys
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parents[2]
E=P/'verification/local-banach-mtp2-stage-sol-20261025/resume'
S=E/'public';LIVE=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public')
sys.path[:0]=[str(E),str(P/'scripts')]
from bm_body_contract import check_bm_page
from banach_mtp2_source import banach_mtp2_source_view,validate_bm_assets,validate_bm_edition,validate_bm_transports
rt,rb,exists=Path.read_text,Path.read_bytes,Path.exists
def sha(p):return hashlib.sha256(rb(p)).hexdigest()
index=rt(S/'research/index.html');sitemap=rt(S/'research/sitemap.xml')
rows=[]
def attempt(rid,name,fn,positive=False):
 try:
  v=fn();faults=[k for k,x in v.get('checks',{}).items() if not x] if isinstance(v,dict) else []
 except Exception as ex:faults=[type(ex).__name__+': '+str(ex)]
 passed=(not faults) if positive else bool(faults)
 rows.append({'record':rid,'case':name,'positive':positive,'passed':passed,'evidence':faults})
def main():
 if len(sys.argv)!=1:raise ValueError('No arguments accepted')
 # Only existence resolution falls through, without writing or reading old article bodies.
 Path.exists=lambda p:exists(p) or (p.is_relative_to(S) and exists(LIVE/p.relative_to(S)))
 try:
  for rid in ['23217863','23146753']:
   paper=P/'papers'/rid;c=json.loads(rb(paper/'publication.json'));g=json.loads(rb(paper/'promotion.json'))
   f=S/'research'/c['slug']/'index.html';original=rt(f)
   check=lambda:check_bm_page(P,S,rid,index,sitemap)
   attempt(rid,'untouched_new_article',check,True)
   faults=[]
   def replace(name,old,new):
    if original.count(old)<1 or old==new:raise ValueError('No-op mutation: '+name)
    faults.append((name,original.replace(old,new,1)))
   for wrapper in ['template','noscript','select','textarea','plaintext','xmp','noframes','noembed','object','iframe']:
    faults.append(('outer_'+wrapper,original.replace('<body>','<'+wrapper+'><body>',1).replace('</body>','</body></'+wrapper+'>',1)))
   for token in [' hidden',' inert',' aria-hidden="true"',' style="display:none"',' class="skip-link"']:
    replace('article'+token,'<article>','<article'+token+'>')
   replace('head_style_hides_main','</head>','<style>main{display:none}</style></head>')
   replace('head_link_extra_stylesheet','</head>','<link rel="stylesheet" href="/hidden.css"></head>')
   replace('body_event_attribute','<article>','<article onclick="this.remove()">')
   replace('unclosed_body','</body>','')
   replace('extra_body','</body>','</body><body>')
   replace('wrong_named_Research','href="/research/">Research</a>','href="/blog/">Research</a>')
   replace('wrong_h1_self','<h1><a href="/research/'+c['slug']+'/">','<h1><a href="/research/other/">')
   replace('wrong_canonical','rel="canonical" href="https://aleckriebel.com/research/'+c['slug']+'/"','rel="canonical" href="https://aleckriebel.com/research/other/"')
   replace('wrong_visible_date','datetime="'+c['publication_date']+'"','datetime="2026-11-14"')
   replace('wrong_citation_date','content="'+c['publication_date'].replace('-','/')+'"','content="2026/11/14"')
   replace('wrong_DOI','name="citation_doi" content="'+c['doi']+'"','name="citation_doi" content="10.0/wrong"')
   replace('wrong_ORCID','name="citation_author_orcid" content="0009-0001-9320-500X"','name="citation_author_orcid" content="0000-0000-0000-0000"')
   replace('wrong_description','name="description" content="'+escape(c['description'])+'"','name="description" content="Unsupported claim"')
   replace('wrong_abstract_heading','<h2>Original abstract</h2>','<h2>Summary</h2>')
   for key in ['abstract','status','ai_disclosure','edition_note','collaboration']:
    replace('alter_'+key,'<p>'+escape(c[key])+'</p>','<p>'+escape(c[key])+' Changed.</p>')
   for key in ['plain_language','result','why_it_works','limitations']:
    for j,v in enumerate(c[key]):replace(key+'_'+str(j),'<p>'+escape(v)+'</p>','<p>'+escape(v)+' Changed.</p>')
   for j,v in enumerate(c['background']):replace('prior_credit_'+str(j),escape(v['note']),escape(v['note'])+' Changed.')
   replace('extra_reader','</iframe>','</iframe><iframe src="another.pdf"></iframe>')
   replace('reader_without_fit_fragment','src="'+c['pdf_filename']+'#view=FitH"','src="'+c['pdf_filename']+'"')
   replace('reader_wrong_title','title="'+escape(c['title'])+' — complete '+str(c['pdf_pages'])+'-page paper"','title="Different reader"')
   prefix='/research/'+c['slug']+'/' if rid=='23146753' else ''
   for name,label in [(c['pdf_filename'],'Download PDF'),(c['supplement_filename'],'Download complete ZIP'),('citation.bib','Download BibTeX')]:
    old='<a href="'+prefix+name+'" download>'+label+'</a>'
    replace('local_'+label+'_wrong_target',old,old.replace(prefix+name,'wrong.file'))
    replace('local_'+label+'_no_download',old,old.replace(' download',''))
   for key,label in [('pdf_filename','Download original PDF from Zenodo'),('supplement_filename','Download original complete ZIP from Zenodo')]:
    old='<a href="https://zenodo.org/api/records/'+rid+'/files/'+c[key]+'/content" download>'+label+'</a>'
    replace('original_'+key+'_wrong_target',old,old.replace('/files/'+c[key]+'/content','/files/wrong/content'))
   replace('license_header','>CC BY 4.0</a>','>MIT</a>')
   if rid=='23217863':
    replace('mixed_license_loss','<p>'+escape(c['license_note'])+'</p>','<p>All files use CC BY.</p>')
    replace('invented_version_in_schema','"creativeWorkStatus":','"version": "1.0", "creativeWorkStatus":')
    replace('strict_threshold_changed',escape('d_BM(M,N)<1+ε_M'),escape('d_BM(M,N)≤1+ε_M'))
   else:
    replace('wrong_Zenodo_schema_version','"version": "1.0"','"version": "2.0"')
    replace('wrong_MTP_inequality',escape('p(x∧y)p(x∨y)≥p(x)p(y)'),escape('p(x∧y)p(x∨y)≤p(x)p(y)'))
    replace('empty_edge_boundary_removed',escape('For a nonempty edge set'),escape('For every edge set'))
   for name,mut in faults:
    Path.read_text=lambda p,*a,_m=mut,**kw:_m if p==f else rt(p,*a,**kw)
    attempt(rid,name,check)
   Path.read_text=rt
   for key in ['pdf_filename','supplement_filename']:
    target=f.parent/c[key];data=rb(target);mut=bytes([data[0]^1])+data[1:]
    Path.read_bytes=lambda p,_t=target,_m=mut:_m if p==_t else rb(p)
    attempt(rid,'asset_one_byte_'+key,check)
   Path.read_bytes=rb
   for name,mutator in [('generic_PASS',lambda x:x.__setitem__('status','PASS')),('qualified_status_suffix',lambda x:x.__setitem__('status',x['status']+'_UNKNOWN')),('whole_family_loss',lambda x:x['reviews'].pop('scope')),('whole_custom_false_changed',lambda x:x['reviews']['analytic']['verdict'].__setitem__('human_peer_review',True)),('premature_published',lambda x:x.__setitem__('public_page_published',True))]:
    obj=copy.deepcopy(g);mutator(obj);attempt(rid,name,lambda obj=obj:banach_mtp2_source_view(paper,c,obj))
   raw=json.loads(rb(paper/c['source_binding']['source_receipt_path']));api=json.loads(rb(paper/c['source_binding']['raw_record_path']))
   for name,mutator in [('native_array_reverse',lambda x:x['all_assets'].reverse()),('native_array_alias',lambda x:x.__setitem__('assets',x.pop('all_assets'))),('native_boolean_size',lambda x:x['all_assets'][0].__setitem__('bytes',True)),('native_MD5_short',lambda x:x['all_assets'][0].__setitem__('md5',x['all_assets'][0]['md5'][1:]))]:
    obj=copy.deepcopy(raw);mutator(obj);attempt(rid,name,lambda obj=obj:validate_bm_assets(paper,rid,obj,api))
   attempt(rid,'restored_untouched_new_article',check,True)
 finally:Path.read_text,Path.read_bytes,Path.exists=rt,rb,exists
 result={'scope':'Read-only new-record-only in-memory campaign; no old69 replay, fixtures, source/site changes or browser claim.','code_sha256':{n:sha(E/n) for n in ['banach_mtp2_source.py','bm_body_contract.py','render_page.proposed.py','final-content-check.proposed.py']},'cases':rows,'total':len(rows),'satisfied':sum(x['passed'] for x in rows),'status':'ALL_NEW_ONLY_CONTROLS_SATISFIED' if all(x['passed'] for x in rows) else 'UNRESOLVED_CANDIDATE_CONTROL_ESCAPE','optimized':not __debug__}
 print(json.dumps(result,indent=2,ensure_ascii=False))
 if not all(x['passed'] for x in rows):raise SystemExit(1)
if __name__=='__main__':main()
