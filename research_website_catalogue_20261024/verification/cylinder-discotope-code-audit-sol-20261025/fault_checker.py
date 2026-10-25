"""Independent altered-read checker controls; only this audit's QA files written."""
from pathlib import Path
from html import escape
import hashlib,json,re,runpy,sys

A=Path(__file__).resolve().parent
R=A.parents[1]
S=R/'verification/local-cylinder-discotope-stage-sol-20261025'
sys.path[:0]=[str(S),str(R/'scripts')]
rid,case=sys.argv[1:3]
c=json.loads((R/'papers'/rid/'publication.json').read_text())
article=S/'public/research'/c['slug']
target=article/'index.html'
original=target.read_bytes()
text=original.decode()
def once(old,new):
    global text
    if text.count(old)!=1:raise RuntimeError(('not_exactly_one_actual_token',case,old,text.count(old)))
    text=text.replace(old,new,1)
if case=='pristine':pass
elif case=='omit_status_paragraph':once('<p>'+escape(c['status'])+'</p>','')
elif case=='wrong_visible_date':
    shown={'23387774':'15 October 2026','23074543':'30 September 2026'}[rid]
    once('>'+shown+'</time>','>1 January 2030</time>')
elif case=='wrong_visible_edition':once('</time> · '+escape(c['edition_label'])+' ·','</time> · '+escape(c['edition_label']).replace('1.0','9.9')+' ·')
elif case=='wrong_visible_citation_edition':once('('+escape(c['citation_edition_label'])+') [Preprint]','(Version 9.9) [Preprint]')
elif case=='omit_proof_paragraph':once('<p>'+escape(c['why_it_works'][0])+'</p>','')
elif case=='wrong_iframe':once('src="'+c['pdf_filename']+'#view=FitH"','src="'+c['pdf_filename']+'#page=2"')
elif case=='wrong_original_download':once('https://zenodo.org/records/'+rid+'/files/'+c['pdf_filename'],'https://zenodo.org/records/00000000/files/'+c['pdf_filename'])
elif case=='wrong_schema_license':once('"license": "https://creativecommons.org/licenses/by/4.0/"','"license": "https://creativecommons.org/licenses/by-nc/4.0/"')
elif case=='wrong_orcid':once('name="citation_author_orcid" content="0009-0001-9320-500X"','name="citation_author_orcid" content="0000-0000-0000-0000"')
elif case=='altered_reader_bytes':target=article/c['pdf_filename'];original=target.read_bytes()
else:raise RuntimeError('unknown_case')
changed=(bytes([original[0]^1])+original[1:]) if case=='altered_reader_bytes' else text.encode()
rb,rt=Path.read_bytes,Path.read_text
Path.read_bytes=lambda q:changed if q==target else rb(q)
Path.read_text=lambda q,*a,**k:Path.read_bytes(q).decode(k.get('encoding') or (a[0] if a else None) or 'utf-8')
(A/('mutation-'+rid+'-'+case+'.json')).write_text(json.dumps({'record_id':rid,'case':case,'path':str(target),'original_SHA256':hashlib.sha256(original).hexdigest(),'changed_read_SHA256':hashlib.sha256(changed).hexdigest(),'original_bytes':len(original),'changed_read_bytes':len(changed),'changed_in_memory_only':True},indent=2)+'\n')
sys.argv=[str(S/'stage_reader.py'),str(S/'final-content-check.stage.py'),rid,'--site',str(S/'public'),'--output-dir',str(A),'--output-stem','checker-'+rid+'-'+case]
runpy.run_path(str(S/'stage_reader.py'),run_name='__main__')
