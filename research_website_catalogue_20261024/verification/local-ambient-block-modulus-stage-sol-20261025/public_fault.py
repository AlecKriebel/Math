"""Mutate a single in-memory public read and run the real proposed checker."""
from pathlib import Path
from html import escape
from datetime import date
import hashlib,json,runpy,sys
O=Path(__file__).resolve().parent;P=O.parents[1];rid,case,mode=sys.argv[1:4];out=O/mode
c=json.loads((P/'papers'/rid/'publication.json').read_text());article=O/'public/research'/c['slug'];target=article/'index.html';original=target.read_bytes();text=original.decode()
def once(a,b):
    global text
    if text.count(a)!=1:raise RuntimeError(('expected_exact_one',case,a,text.count(a)))
    text=text.replace(a,b,1)
if case=='wrong_visible_date':
    dt=date.fromisoformat(c['publication_date']);shown=f'{dt.day} {dt.strftime("%B %Y")}';once('>'+shown+'</time>','>1 January 2030</time>')
elif case=='wrong_visible_edition':once('</time> · '+escape(c['edition_label'])+' ·','</time> · Version 9.9 ·')
elif case=='wrong_citation_edition':once('('+escape(c['citation_edition_label'])+') [Preprint]','(Version 9.9) [Preprint]')
elif case=='omit_status':once('<p>'+escape(c['status'])+'</p>','')
elif case=='reorder_status':once('<p>'+escape(c['status'])+'</p><p>'+escape(c['ai_disclosure'])+'</p>','<p>'+escape(c['ai_disclosure'])+'</p><p>'+escape(c['status'])+'</p>')
elif case=='omit_proof':once('<p>'+escape(c['why_it_works'][0])+'</p>','')
elif case=='wrong_iframe':once('src="'+c['pdf_filename']+'#view=FitH"','src="'+c['pdf_filename']+'#page=2"')
elif case=='wrong_original_PDF_href':once(c['related_resources'][0]['url'],'https://zenodo.org/api/records/00000000/files/wrong.pdf/content')
elif case=='wrong_schema_license':once('"license": "https://creativecommons.org/licenses/by/4.0/"','"license": "https://creativecommons.org/licenses/by-nc/4.0/"')
elif case=='wrong_orcid':once('name="citation_author_orcid" content="0009-0001-9320-500X"','name="citation_author_orcid" content="0000-0000-0000-0000"')
elif case=='changed_reader_bytes':target=article/c['pdf_filename'];original=target.read_bytes()
elif case=='changed_ZIP_bytes':target=article/c['supplement_filename'];original=target.read_bytes()
elif case=='wrong_h1':once('>'+escape(c['title'])+'</a></h1>','>An unapproved mathematical claim</a></h1>')
elif case=='extra_outside_claim':once('</article>','<p>This proves every open problem in this field.</p></article>')
elif case=='mislabel_original_PDF':once('>Download the original from Zenodo</a>','>Download a later repaired edition</a>')
elif case=='mislabel_original_ZIP':once('>Zenodo original complete ZIP</a>','>Selected verification subset</a>')
elif case=='wrong_result_math':once('<p>'+escape(c['result'][0])+'</p>','<p>'+escape(c['result'][0]+' The theorem holds without any hypotheses.')+'</p>')
elif case=='raw_TeX_extra':once('</article>',r'<p>\unsupported{mathematics}</p></article>')
elif case=='changed_BibTeX':target=article/'citation.bib';original=target.read_bytes()
elif case=='HK_181_to_180':once('Acta Math. 181 (1998)','Acta Math. 180 (1998)')
else:raise RuntimeError('unsupported_fault')
changed=(bytes([original[0]^1])+original[1:]) if case in ['changed_reader_bytes','changed_ZIP_bytes','changed_BibTeX'] else text.encode();rb,rt=Path.read_bytes,Path.read_text
(out/('mutation-'+rid+'-'+case+'.json')).write_text(json.dumps({'record_id':rid,'case':case,'path':str(target),'original_SHA256':hashlib.sha256(original).hexdigest(),'changed_read_SHA256':hashlib.sha256(changed).hexdigest(),'in_memory_only':True},indent=2)+'\n')
Path.read_bytes=lambda p:changed if p==target else rb(p)
Path.read_text=lambda p,*a,**k:Path.read_bytes(p).decode(k.get('encoding') or 'utf-8')
sys.argv=[str(O/'stage_reader.py'),str(O/'final-content-check.stage.py'),rid,'--site',str(O/'public'),'--output-dir',str(out),'--output-stem','checker-'+rid+'-'+case]
runpy.run_path(str(O/'stage_reader.py'),run_name='__main__')
