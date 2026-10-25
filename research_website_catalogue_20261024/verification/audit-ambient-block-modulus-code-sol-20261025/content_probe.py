"""Only in-memory proposed-page faults; outputs confined to this fresh audit."""
from pathlib import Path
from html import escape
from datetime import date
import hashlib,json,runpy,sys,builtins,io
E=Path(__file__).resolve().parent;P=E.parents[1];S=P/'verification/local-ambient-block-modulus-stage-sol-20261025'
rid,case,mode=sys.argv[1:4];c=json.loads((P/'papers'/rid/'publication.json').read_text());target=S/'public/research'/c['slug']/'index.html';original=target.read_bytes();text=original.decode()
def once(a,b):
 global text
 if text.count(a)!=1:raise RuntimeError(('mutation_match_not_one',case,a,text.count(a)))
 text=text.replace(a,b,1)
if case=='pristine':pass
elif case=='wrong_h1':once('>'+escape(c['title'])+'</a></h1>','>A different unapproved theorem</a></h1>')
elif case=='extra_outside_body_claim':once('</article>','<p>The result has formal proof certification and journal peer review.</p></article>')
elif case=='abstract_sentence_omitted':
 p='<p>'+escape(c['abstract'])+'</p>';once(p,'<p>'+escape(c['abstract'].rsplit('. ',1)[0])+'.</p>')
elif case=='critical_result_equation':
 old={'23333353':'φ=(δ₀₀+δ₁₁)/2','23416806':'N=max{2,ℓ,4(|M|+1)}','23441617':'Mod₂Γ(E,F)=∞'}[rid];once(escape(old),escape(old.replace('/2','/3').replace('4(|M|+1)','3(|M|+1)').replace('=∞','=1')))
elif case=='last_scope_paragraph_omitted':once('<p>'+escape(c['limitations'][-1])+'</p>','')
elif case=='edition_note_omitted':once('<p>'+escape(c['edition_note'])+'</p>','')
elif case=='AI_status_changed':once('<p>'+escape(c['ai_disclosure'])+'</p>','<p>Externally peer-reviewed and formally certified.</p>')
elif case=='visible_date_changed':
 dt=date.fromisoformat(c['publication_date']);once('>'+f'{dt.day} {dt.strftime("%B %Y")}'+'</time>','>1 January 2030</time>')
elif case=='visible_edition_changed':once('</time> · '+escape(c['edition_label'])+' ·','</time> · Version 9.9 ·')
elif case=='citation_edition_changed':once('('+escape(c['citation_edition_label'])+') [Preprint]','(Version 9.9) [Preprint]')
elif case=='original_PDF_label_changed':once('>Download the original from Zenodo</a>','>Rebuilt supplementary PDF</a>')
elif case=='original_ZIP_label_changed':once('>Zenodo original complete ZIP</a>','>Selected scripts only</a>')
elif case=='original_PDF_href_changed':
 raw=c['source_binding']['published_file_objects'];u=next(x['links']['self'] for x in raw if x['key']==c['pdf_filename']);once('href="'+escape(u)+'" download>Download the original','href="'+escape(next(x['links']['self'] for x in raw if x['key']==c['supplement_filename']))+'" download>Download the original')
elif case=='background_link_label_changed':once('>'+escape(c['background'][0]['title'])+'</a>','>An unrelated uncredited source</a>')
elif case=='background_link_href_changed':once('href="'+escape(c['background'][0]['url'])+'"','href="https://example.invalid/unrelated"')
elif case=='byline_changed':once('By Alec Kriebel, independent researcher.','By Someone Else, independent researcher.')
elif case=='schema_version_changed':once('"version": "1.0"','"version": "9.9"')
elif case=='h1_valid_but_wrong_href':once('<h1><a href="/research/'+c['slug']+'/">','<h1><a href="/research/">')
elif case=='Research_valid_but_wrong_href':once('<a href="/research/">Research</a>','<a href="/blog/">Research</a>')
elif case=='public_HK180_regression':once('Acta Math. 181 (1998)','Acta Math. 180 (1998)')
else:raise ValueError(case)
changed=text.encode();(E/'mutations').mkdir(exist_ok=True)
(E/'mutations'/f'{rid}-{case}-{mode}.json').write_text(json.dumps({'record_id':rid,'case':case,'mode':mode,'path':str(target),'original_SHA256':hashlib.sha256(original).hexdigest(),'changed_read_SHA256':hashlib.sha256(changed).hexdigest(),'changed':changed!=original,'in_memory_only':True},indent=2)+'\n')
rb,rt=Path.read_bytes,Path.read_text
Path.read_bytes=lambda p:changed if p==target else rb(p)
Path.read_text=lambda p,*a,**k:Path.read_bytes(p).decode(k.get('encoding') or 'utf-8')
# The unmodified private read-only adapter provides old resources without copying them.
sys.path[:0]=[str(S),str(P/'scripts')]
sys.argv=[str(S/'stage_reader.py'),str(S/'final-content-check.stage.py'),rid,'--site',str(S/'public'),'--output-dir',str(E/'qa'/mode),'--output-stem',rid+'-'+case]
real_open,real_io=builtins.open,io.open
def guarded(file,mode='r',*a,**k):
 if any(x in mode for x in 'wax+') and isinstance(file,(str,bytes,Path)):
  if not Path(file).resolve().is_relative_to(E):raise RuntimeError('audit_write_outside_own_namespace:'+str(file))
 return real_open(file,mode,*a,**k)
builtins.open=guarded;io.open=guarded
runpy.run_path(str(S/'stage_reader.py'),run_name='__main__')
