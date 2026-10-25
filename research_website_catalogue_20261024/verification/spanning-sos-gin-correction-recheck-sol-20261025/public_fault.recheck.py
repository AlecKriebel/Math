"""Alter one actual public output read; write only own QA receipts."""
from pathlib import Path
from html import escape
from datetime import date
import hashlib,json,runpy,sys
from spanning_sos_gin_source import display_sg_text
O=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/verification/spanning-sos-gin-correction-recheck-sol-20261025');P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024');S=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/verification/local-spanning-sos-gin-stage-sol-20261025');rid,case,mode=sys.argv[1:4];out=O/mode
c=json.loads((P/'papers'/rid/'publication.json').read_text());article=S/'public/research'/c['slug'];target=article/'index.html';original=target.read_bytes();text=original.decode()
def once(a,b):
    global text
    if text.count(a)!=1:raise RuntimeError(('expected_exact_one',case,a,text.count(a)))
    text=text.replace(a,b,1)
if case=='wrong_visible_date':
    dt=date.fromisoformat(c['publication_date']);shown=f'{dt.day} {dt.strftime("%B %Y")}';once('>'+shown+'</time>','>1 January 2030</time>')
elif case=='wrong_visible_edition':once('</time> · '+escape(c['edition_label'])+' ·','</time> · Version 9.9 ·')
elif case=='wrong_visible_citation_edition':once('('+escape(c['citation_edition_label'])+') [Preprint]','(Version 9.9) [Preprint]')
elif case=='omit_status_paragraph':once('<p>'+escape(c['status'])+'</p>','')
elif case=='omit_proof_paragraph':once('<p>'+escape(display_sg_text(rid,c['why_it_works'][0]))+'</p>','')
elif case=='wrong_iframe':once('src="'+c['pdf_filename']+'#view=FitH"','src="'+c['pdf_filename']+'#page=2"')
elif case=='wrong_original_download':once(c['related_resources'][0]['url'],'https://zenodo.org/api/records/00000000/files/wrong.pdf/content')
elif case=='wrong_schema_license':once('"license": "https://creativecommons.org/licenses/by/4.0/"','"license": "https://creativecommons.org/licenses/by-nc/4.0/"')
elif case=='wrong_orcid':once('name="citation_author_orcid" content="0009-0001-9320-500X"','name="citation_author_orcid" content="0000-0000-0000-0000"')
elif case=='wrong_readable_math':
    token={'23181280':'p+2q=K+(1−h)+(q−m)','23442760':'Cₙ=4(n+2)²(π/2)^(2n+4)(1+2^(n+2))','23395703':'p=min{d≥0:x₂ᵈ∈B}=8'}[rid];once(escape(token),escape(token+'+1'))
elif case=='altered_reader_bytes':target=article/c['pdf_filename'];original=target.read_bytes()
elif case=='drop_TeX_original_link':once('<li><a href="'+c['related_resources'][2]['url']+'">Zenodo original published TeX source</a></li>','')
elif case=='invent_Gin_schema_version':once('"creativeWorkStatus": "Unrefereed preprint"','"version": "1.0", "creativeWorkStatus": "Unrefereed preprint"')
else:raise RuntimeError('unsupported_fault')
changed=(bytes([original[0]^1])+original[1:]) if case=='altered_reader_bytes' else text.encode();rb,rt=Path.read_bytes,Path.read_text
(out/('mutation-'+rid+'-'+case+'.json')).write_text(json.dumps({'record_id':rid,'case':case,'path':str(target),'original_SHA256':hashlib.sha256(original).hexdigest(),'changed_read_SHA256':hashlib.sha256(changed).hexdigest(),'in_memory_only':True},indent=2)+'\n')
Path.read_bytes=lambda p:changed if p==target else rb(p)
Path.read_text=lambda p,*a,**k:Path.read_bytes(p).decode(k.get('encoding') or 'utf-8')
sys.argv=[str(S/'stage_reader.py'),str(O/'final-content-check.stage.py'),rid,'--site',str(S/'public'),'--output-dir',str(out),'--output-stem','checker-'+rid+'-'+case]
runpy.run_path(str(S/'stage_reader.py'),run_name='__main__')
