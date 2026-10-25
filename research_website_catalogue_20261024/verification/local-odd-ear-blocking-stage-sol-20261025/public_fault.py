"""One memory-only mutation of an actual private article or asset read.

No corrupt fixture, modified source, or altered public file is written. Binary
controls exercise hash rejection only; parsers still read the actual originals.
"""
from pathlib import Path
import datetime,hashlib,json,re,runpy,sys
from html import escape
O=Path(__file__).resolve().parent;P=O.parents[1]
rid,case,outdir=sys.argv[1:4];out=Path(outdir)
c=json.loads((P/'papers'/rid/'publication.json').read_text())
folder=O/'public/research'/c['slug'];target=folder/'index.html';before=target.read_bytes();text=before.decode()
rb,rt=Path.read_bytes,Path.read_text
def replace(old,new):
 global text
 if text.count(old)!=1:raise RuntimeError('mutation must have exactly one target:'+case)
 text=text.replace(old,new,1)
expected=[]
if case=='visible_date':
 old=re.search(r'(<time datetime="[^"]+">)(.*?)(</time>)',text).group(0)
 replace(old,re.sub(r'(?<=>)[^<]+(?=</time>)','1 January 2000',old));expected=['exact_byline_date_header_edition']
elif case=='header_version':
 old=' · '+c['edition_label']+' · ';replace(old,' · Version 99 · ');expected=['exact_byline_date_header_edition']
elif case=='citation_version':
 old='('+c['citation_edition_label']+') [Preprint]';replace(old,'(Version 99) [Preprint]');expected=['exact_citation_edition']
elif case=='omit_status':
 old=re.search(r'<section id="status">.*?</section>',text,re.S).group(0);replace(old,'');expected=['exact_ordered_full_status_paragraphs']
elif case=='truncate_abstract':
 old='<h2>Original abstract</h2><p>'+escape(c['abstract'])+'</p>';replace(old,'<h2>Original abstract</h2><p>'+escape(c['abstract'].rsplit('. ',1)[0])+'.</p>');expected=['whole_original_abstract']
elif case=='omit_result':
 section=re.search(r'<section id="result">.*?</section>',text,re.S).group(0)
 last=re.findall(r'<p>.*?</p>',section,re.S)[-1];replace(section,section.replace(last,''));expected=['exact_whole_approved_body_text']
elif case=='alter_proof':
 old='β(z*B)=max |E(B[S])|' if rid=='23576280' else 'τ(H)=m+τ(Q)'
 section=re.search(r'<section id="proof">.*?</section>',text,re.S).group(0)
 if section.count(old)!=1:raise RuntimeError('proof target count')
 replace(section,section.replace(old,'β(z*B)=0' if rid=='23576280' else 'τ(H)=0'));expected=['exact_whole_approved_body_text']
elif case=='add_human_review':
 replace('</article>','<p>External human peer review has certified this theorem.</p></article>');expected=['exact_whole_approved_body_text']
elif case=='wrong_iframe':
 replace('src="'+c['pdf_filename']+'#view=FitH"','src="wrong.pdf#view=FitH"');expected=['iframe']
elif case=='wrong_original_pdf':
 old=re.search(r'<a href="[^"]+" download>Download the original from Zenodo</a>',text).group(0)
 replace(old,'<a href="https://zenodo.org/records/1/files/wrong.pdf" download>Download the original from Zenodo</a>');expected=['exact_original_PDF_label_download']
elif case=='borrow_code_license':
 if rid=='23576280':replace('authored code is MIT.','authored code is CC BY 4.0.')
 else:replace('Authored manuscript, proofs, code and audits in the deposit are licensed CC BY 4.0;','Authored manuscript, proofs, code and audits in the deposit are licensed MIT;')
 expected=['exact_approved_material_note_and_code_license']
elif case=='h1_destination':
 old='<h1><a href="/research/'+c['slug']+'/">';replace(old,'<h1><a href="/research/">');expected=['exact_h1_selflink_destination']
elif case=='Research_destination':
 old='<nav aria-label="Main navigation"><a href="/research/">Research</a>'
 replace(old,'<nav aria-label="Main navigation"><a href="/blog/">Research</a>');expected=['exact_main_Research_destination']
elif case=='ORCID_destination':
 replace('<a href="'+c['orcid']+'">ORCID</a>','<a href="https://orcid.org/0000-0000-0000-0000">ORCID</a>');expected=['exact_other_fixed_template_destinations']
elif case=='footer_destination':
 replace('<a href="/research/">Research home</a>','<a href="/blog/">Research home</a>');expected=['exact_other_fixed_template_destinations']
elif case=='paper_jump':
 replace('<a href="#paper">Read on this page</a>','<a href="#cite">Read on this page</a>');expected=['exact_other_fixed_template_destinations']
elif case in ('PDF_hash_read','ZIP_hash_read','BibTeX_read'):
 target=folder/(c['pdf_filename'] if case=='PDF_hash_read' else c['supplement_filename'] if case=='ZIP_hash_read' else 'citation.bib')
 before=rb(target);after=before+b'\nMEMORY_ONLY_FAULT\n'
 expected=['pdf_filename' if case=='PDF_hash_read' else 'supplement_filename' if case=='ZIP_hash_read' else 'exact_full_prepared_BibTeX']
else:raise RuntimeError('unknown control:'+case)
if case not in ('PDF_hash_read','ZIP_hash_read','BibTeX_read'):after=text.encode()
def read_bytes(p):return after if p==target else rb(p)
def read_text(p,*a,**k):return after.decode(k.get('encoding') or (a[0] if a else None) or 'utf-8') if p==target else rt(p,*a,**k)
Path.read_bytes=read_bytes;Path.read_text=read_text
receipt={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'record_id':rid,'case':case,'path':str(target),'original_bytes':len(before),'original_sha256':hashlib.sha256(before).hexdigest(),'virtual_bytes':len(after),'virtual_sha256':hashlib.sha256(after).hexdigest(),'expected_failed_checks':expected,'memory_only':True,'parser_corruption_not_claimed':case in ('PDF_hash_read','ZIP_hash_read')}
(out/'mutation.json').write_text(json.dumps(receipt,indent=2)+'\n')
sys.argv=[str(O/'stage_reader.py'),str(O/'final-content-check.stage.py'),rid,'--site',str(O/'public'),'--output-dir',str(out),'--output-stem','qa']
runpy.run_path(str(O/'stage_reader.py'),run_name='__main__')
