"""Whole visible-body contract from approved fields and fixed labels, independent of generated HTML."""
from datetime import date
from abm_body_contract import BodyText

def expected_body(c):
    dt=date.fromisoformat(c['publication_date']);day=f'{dt.day} {dt.strftime("%B %Y")}';doi='https://doi.org/'+c['doi'];author='; '.join(c.get('authors',[c['author']]))
    words=['Skip to content','Alec Kriebel','Research | Blog | ORCID',c['title'],f"By {author}, independent researcher. {c['publication_date_label']} {day} · {c['edition_label']} · Unrefereed preprint",f"Read the paper (PDF, {c['pdf_pages']} pages) · {c['supplement_label']} · Zenodo record · CC BY 4.0",'Plain-English explanation · Read on this page · Collaboration',c['abstract_heading'],c['abstract'],'The idea in plain English',*c['plain_language'],'The precise result',*c['result'],'Why the result holds',*c['why_it_works'],'Scope and limitations',*c['limitations'],'Status and AI use',c['status'],c['ai_disclosure']]
    if c.get('edition_note'):words.append(c['edition_note'])
    words+=['Read the paper',c['reader_intro'],'Open PDF · Download PDF · Download original PDF from Zenodo','Supporting materials','Download complete ZIP · Download original complete ZIP from Zenodo']
    words += [x['label'] for x in c['related_resources']]
    if c['source_binding']['record_id']==23217863:words+=['Licensing',c['license'],c['license_note']]
    words+=['Collaborate on this result',c['collaboration'],'Authorship and responsibilities would be discussed in relation to the substantive contributions made.','Contact Alec','Cite this paper',f"{author}. ({dt.year}). {c['title']} ({c['citation_edition_label']}) [Preprint]. Zenodo. {doi}",'Download BibTeX','Background and prior work']
    words += [x['title']+(' : '+x['note'] if x.get('note') else '') for x in c['background']]
    words+=['Research home | me@aleckriebel.com','© 2013–2026 Kriebel LLC.']
    return ' '.join(' '.join(words).split())
