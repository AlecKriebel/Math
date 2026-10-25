"""Audit-owned exact-stage checker controls; only own QA files may be written."""
from pathlib import Path
from datetime import date
from html import escape
import builtins,io,json,runpy,sys,hashlib,re
E=Path(__file__).resolve().parent
P=E.parents[1]
S=P/'verification/local-spanning-sos-gin-stage-sol-20261025'
sys.path.insert(0,str(S));sys.path.insert(1,str(P/'scripts'))
rid,case,mode=sys.argv[1:4]
c=json.loads((P/'papers'/rid/'publication.json').read_text())
target=S/'public/research'/c['slug']/'index.html'
original=target.read_bytes();text=original.decode()
def once(a,b):
 global text
 if text.count(a)!=1:raise RuntimeError(('one_mutation_required',case,a,text.count(a)))
 text=text.replace(a,b,1)
if case=='abstract_last_sentence_removed':
 a=escape(c['abstract']);parts=a.rsplit('. ',1)
 once('<p>'+a+'</p>','<p>'+parts[0]+'.</p>')
elif case=='header_date':
 d=date.fromisoformat(c['publication_date']);v=f'{d.day} {d.strftime("%B %Y")}'
 once('>'+v+'</time>','>1 January 2030</time>')
elif case=='status_reordered':
 a='<p>'+escape(c['status'])+'</p>';b='<p>'+escape(c['ai_disclosure'])+'</p>'
 once(a+b,b+a)
elif case=='extra_status_claim':
 a='<section id="status">';start=text.index(a);end=text.index('</section>',start)
 text=text[:end]+'<p>This work has external human peer review and formal proof certification.</p>'+text[end:]
elif case=='header_license_removed':once(' · <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>','')
elif case=='local_PDF_download_attribute_removed':once('<a href="'+c['pdf_filename']+'" download>Download PDF</a>','<a href="'+c['pdf_filename']+'">Download PDF</a>')
elif case=='Gin_null_schema_version':once('"creativeWorkStatus": "Unrefereed preprint"','"version": null, "creativeWorkStatus": "Unrefereed preprint"')
elif case=='Gin_TeX_link_commented':
 a='<li><a href="'+c['related_resources'][2]['url']+'">Zenodo original published TeX source</a></li>'
 once(a,'<!-- '+a+' -->')
elif case=='Gin_TeX_link_mislabelled':once('>Zenodo original published TeX source</a>','>Unrelated numerical table</a>')
elif case=='SOS_exact_constant_corrupted':once('Cₙ=4(n+2)²(π/2)^(2n+4)(1+2^(n+2))','Cₙ=4(n+2)²(π/2)^(2n+5)(1+2^(n+2))')
elif case=='SOS_unit_mass_corrupted':once('∫_K q dx=1','∫_K q dx=2')
elif case=='Gin_resolution_corrupted':once('0→S(−7)³⊕S(−9)→S(−6)⁵→J^(top)→0','0→S(−7)⁴⊕S(−9)→S(−6)⁵→J^(top)→0')
elif case=='common_tree_removed':once('keeping the same underlying tree throughout','allowing an independent tree for each root')
elif case=='unapproved_body_claim':once('<section id="paper">','<p>This is an externally refereed theorem with a formal proof certificate.</p><section id="paper">')
elif case=='wrong_visible_h1':once('<h1><a href="/research/'+c['slug']+'/">'+escape(c['title'])+'</a></h1>','<h1><a href="/research/'+c['slug']+'/">An unrelated result</a></h1>')
elif case!='pristine':raise ValueError(case)
changed=text.encode();rb,rt=Path.read_bytes,Path.read_text
Path.read_bytes=lambda p:changed if p==target else rb(p)
Path.read_text=lambda p,*a,**k:Path.read_bytes(p).decode(k.get('encoding') or 'utf-8')
real_open=builtins.open
def guarded(file,mode='r',*a,**k):
 if isinstance(file,(str,bytes,Path)) and any(v in mode for v in ['w','a','x','+']):
  if not Path(file).resolve().is_relative_to(E):raise RuntimeError('write_outside_owned_audit:'+str(file))
 return real_open(file,mode,*a,**k)
builtins.open=guarded;io.open=guarded
out=E/mode;out.mkdir(exist_ok=True)
meta={'record':rid,'case':case,'mode':mode,'mutated_read_path':str(target),'original_sha256':hashlib.sha256(original).hexdigest(),'changed_read_sha256':hashlib.sha256(changed).hexdigest(),'actual_original_file_unchanged':True,'mutation_in_memory_only':True,'writes_guarded_to':str(E)}
(out/(rid+'-'+case+'-mutation.json')).write_text(json.dumps(meta,indent=2)+'\n')
sys.argv=[str(S/'stage_reader.py'),str(S/'final-content-check.stage.py'),rid,'--site',str(S/'public'),'--output-dir',str(out),'--output-stem',rid+'-'+case]
runpy.run_path(str(S/'stage_reader.py'),run_name='__main__')
