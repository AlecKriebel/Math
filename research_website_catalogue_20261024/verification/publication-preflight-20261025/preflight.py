"""Read-only five-paper publication preflight; writes only this QA evidence directory."""
from pathlib import Path
import json,hashlib,zipfile,re,subprocess,datetime,unicodedata
P=Path(__file__).resolve().parents[2];O=Path(__file__).resolve().parent
TEX={'23203334':'published-source/source-and-verification/main.tex','22929486':'published-source/kourovka_16_45/proof.tex','23088066':'published-source/paper.tex','23353160':'published-source/grassmann_calibrations_v1/research_note.tex','23147866':'w4_locc_dense_coding.tex'}
def name(x):return x.get('name',x.get('filename'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def norm(a,rid):
 a=a.replace("'",'’').replace('--','–').replace('~',' ')
 for x,y in {r'\mup':'μ′',r'\Sep':'Sep',r'\mathbb R^{12}':'R¹²',r'K\"ahler':'Kähler','Bru\\ss\\':'Bruß',r'\hbin':'h₂',r'\ldots':'…','C_{4,12}':'C₄,₁₂',r'C_b^\infty\cap L^2':'C_b^∞ ∩ L²',r'e_a e_b/m_a':'eₐe_b/mₐ'}.items():a=a.replace(x,y)
 a=a.replace(r'\[','').replace(r'\]','').replace('$','')
 return re.sub(r'\s+','',unicodedata.normalize('NFKC',a))
r={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'mode':'candidate-only preflight, no publication authorization','papers':{},'issues':[]}
for rid,tp in TEX.items():
 p=P/'papers'/rid;s=p/'sources';cpath=p/'reviews/scope/content.json';c=json.loads(cpath.read_text());receipt=json.loads((s/'receipt.json').read_text());record=json.loads((s/'record.json').read_text());meta=record['metadata'];binding=c['source_binding'];tex=(s/tp).read_text();a=re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}',tex,re.S).group(1)
 checks={};assets=[]
 def test(k,v):
  checks[k]=bool(v)
  if not v:r['issues'].append(rid+': '+k)
 test('record_doi_title_date',all(c[k]==meta[k] for k in ['title','doi','publication_date']))
 test('version_source',c['version']==meta['version'] if 'version' in meta else binding['zenodo_version'] is None and rid=='23203334')
 test('complete_original_abstract',norm(a,rid)==norm(c['abstract'],rid))
 test('receipt_name_or_filename_present',all(isinstance(name(x),str) and name(x) for x in receipt['files']))
 test('all_record_assets_in_receipt',{x['key'] for x in record['files']}=={name(x) for x in receipt['files']})
 test('all_receipt_assets_in_candidate_binding',sorted((name(x),x['bytes'],x['sha256'],x['url']) for x in receipt['files'])==sorted((name(x),x['bytes'],x['sha256'],x['url']) for x in binding['files']))
 for item in receipt['files']:
  f=s/name(item);source=next(x for x in record['files'] if x['key']==name(item));raw=f.read_bytes();v={'name':f.name,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'md5':hashlib.md5(raw).hexdigest()}
  test('asset_integrity_'+f.name,v['sha256']==item['sha256'] and v['bytes']==item['bytes']==source['size'] and 'md5:'+v['md5']==source['checksum'])
  if f.suffix=='.zip':
   with zipfile.ZipFile(f) as z:
    test('zip_CRC_'+f.name,z.testzip() is None);v['zip_members']=len(z.infolist());v['internal_pdfs']=[n for n in z.namelist() if n.endswith('.pdf')];v['nested_archives']=[n for n in z.namelist() if n.lower().endswith(('.zip','.tar','.tgz','.gz','.7z'))]
    v['internal_pdf_sha256']={n:hashlib.sha256(z.read(n)).hexdigest() for n in v['internal_pdfs']}
  assets.append(v)
 pdf=s/c['pdf_filename'];txt=subprocess.check_output(['pdftotext','-layout',str(pdf),'-'],text=True);pages=txt.split('\f');pages=pages[:-1] if not pages[-1].strip() else pages
 test('pdf_page_count',len(pages)==binding['reviewed_documents'][0]['pages']);test('all_PDF_pages_have_text',all(len(pg.strip())>100 for pg in pages))
 test('candidate_PDF_binding',sha(pdf)==binding['pdf_sha256']);test('candidate_ZIP_binding',sha(s/c['supplement_filename'])==binding['supplement_sha256'] if c.get('supplement_filename') else binding['supplement_sha256'] is None)
 test('no_unsolicited_followup',c['follow_up'] is None)
 test('no_verification_replay_dates',not any(x in json.dumps({k:v for k,v in c.items() if k!='source_binding'}).lower() for x in ['24 october 2026','october 24','audit completed','checks passed']))
 reports=[]
 for f in sorted((p/'reviews').glob('*/REVIEW.md')):
  vf=f.parent/'verdict.json';reports.append({'family':f.parent.name,'report':str(f.relative_to(p)),'sha256':sha(f),'verdict_file':str(vf.relative_to(p)),'verdict_sha256':sha(vf)})
 primary_linked={c['pdf_filename']}
 if c.get('supplement_filename'):primary_linked.add(c['supplement_filename'])
 primary_linked.update(x['filename'] for x in c.get('additional_assets',[]))
 for item in receipt['files']:
  if any('/files/'+name(item) in x['url'] for x in c.get('related_resources',[])):primary_linked.add(name(item))
 (O/(rid+'-original-abstract.tex.txt')).write_text(a.strip()+'\n');(O/(rid+'-page1.txt')).write_text(pages[0])
 r['papers'][rid]={'candidate_sha256':sha(cpath),'receipt_sha256':sha(s/'receipt.json'),'record_sha256':sha(s/'record.json'),'tex_path':tp,'tex_sha256':sha(s/tp),'title':c['title'],'slug':c['slug'],'publication_date':c['publication_date'],'metadata_version':meta.get('version'),'candidate_version':c['version'],'pages':len(pages),'assets':assets,'checks':checks,'report_bindings':reports,'unlinked_files_available_via_record':sorted(set(name(x) for x in receipt['files'])-primary_linked),'publication_exists_at_check':(p/'publication.json').exists(),'promotion_exists_at_check':(p/'promotion.json').exists(),'raw_tex_commands_in_abstract':sorted(set(re.findall(r'\\[A-Za-z]+',a)))}
(O/'preflight.json').write_text(json.dumps(r,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'checked_papers':len(r['papers']),'published_assets':sum(len(x['assets']) for x in r['papers'].values()),'issues':r['issues'],'pages':{rid:v['pages'] for rid,v in r['papers'].items()},'unlinked_files':{rid:v['unlinked_files_available_via_record'] for rid,v in r['papers'].items()}},indent=2))
