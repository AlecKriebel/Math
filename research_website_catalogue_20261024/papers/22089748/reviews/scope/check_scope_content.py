from pathlib import Path
import hashlib, json, re, html, datetime
b=Path(__file__).resolve().parents[2]; r=b/'reviews/scope'; s=b/'sources'
c=json.loads((r/'content.json').read_text()); rec=json.loads((s/'record.json').read_text()); receipt=json.loads((s/'receipt.json').read_text())
checks=[]
def check(name,truth):
 if not truth: raise AssertionError(name)
 checks.append(name)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
check('title matches fresh Zenodo',c['title']==rec['metadata']['title'])
check('date matches fresh Zenodo',c['publication_date']==rec['metadata']['publication_date']=='2026-08-25')
check('version matches fresh Zenodo',c['version']==rec['metadata']['version']=='1.0.0')
check('DOI matches selected record',c['doi']==rec['metadata']['doi']=='10.5281/zenodo.22089748')
check('receipt binding',c['source_binding']['source_receipt_sha256']==sha(s/'receipt.json'))
check('metadata binding',c['source_binding']['record_metadata_sha256']==sha(s/'record.json'))
check('no invented printed numbered version',c['source_binding']['manuscript_version'] is None)
check('printed month retained',c['source_binding']['manuscript_date']=='August 2026')
source=(b/c['source_binding']['primary_tex_path']).read_text(); a=re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}',source,re.S).group(1)
expected=re.sub(r'\s+',' ',a).strip().replace('death--Birth','death–Birth').replace('$J_n$','Jₙ').replace('$n\\ge3$','n ≥ 3').replace('$K_4$','K₄')
check('complete abstract exact after allowed typography',expected==re.sub(r'\s+',' ',c['abstract']).strip())
check('two abstract paragraphs',len(c['abstract'].split('\n\n'))==2)
def canon(t):
 return re.sub(r'\s+','',t.replace('Jₙ','J_n').replace('K₄','K_4').replace('’',"'").replace('–','-'))
metadata_abstract=html.unescape(re.sub(r'<[^>]*>','',rec['metadata']['description']))
check('complete abstract agrees with fresh record description',canon(metadata_abstract)==canon(c['abstract']))
names={c['pdf_filename'],c['supplement_filename']}|{x['filename'] for x in c['additional_assets']}
check('all five published files exposed',names=={f['name'] for f in receipt['files']} and len(names)==5)
for f in receipt['files']:
 p=s/f['name'];check('bytes '+f['name'],p.stat().st_size==f['bytes']);check('sha256 '+f['name'],sha(p)==f['sha256']);check('md5 '+f['name'],'md5:'+hashlib.md5(p.read_bytes()).hexdigest()==f['zenodo_checksum'])
check('accurate source TAR.GZ label',c['supplement_label'].endswith('(TAR.GZ)'))
check('accurate referee TAR.GZ kind',c['additional_assets'][0]['kind']=='tar.gz')
check('primary DOI never replaced by predecessor',c['source_binding']['predecessor']['doi']!=c['doi'])
check('original related metadata retained',c['source_binding']['metadata_related_identifiers']==rec['metadata']['related_identifiers'])
check('no unsubstantiated new followup',c['follow_up'] is None)
text=' '.join(c['result']+c['limitations'])
for term in ['uniformly','no self-loops','n ≥ 3','strict nondegenerate local','nonreversible','P ≠ Jₙ','threshold','n = 2','S₁ × S₃','S₂ × S₂','not a weak-selection','no radius uniform','not sufficient']:
 check('scope term '+term,term.lower() in text.lower())
check('explicit AI disclosure','Generative AI' in c['ai_disclosure'])
check('unrefereed status','unrefereed preprint' in c['ai_disclosure'])
check('substantive collaboration', 'substantive collaboration' in c['collaboration'])
check('concise SEO description',len(c['description'])<=170)
bind=json.loads((r/'source-bindings.json').read_text())
for f in bind['complete_manuscript_sources']:check('manuscript source '+f['path'],sha(b/f['path'])==f['sha256'])
check('content binding',sha(r/'content.json')==bind['content_sha256'])
check('report exists',(r/'REVIEW.md').is_file())
out={'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','check_count':len(checks),'checks':checks,'scope':'Metadata, source-abstract identity, asset hashes and candidate-scope checks only; no mathematical certificate replay.'}
(r/'content-qa.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':'PASS','checks':len(checks),'abstract_words':len(c['abstract'].split()),'description_characters':len(c['description'])}))
