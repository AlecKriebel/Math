"""Whole visible text contract from approved fields and independently frozen notes.
Uses the unchanged existing parser; no output hash is learned from rendered HTML.
"""
from datetime import date
from abm_body_contract import BodyText
MATERIAL_NOTES = {'23576280': 'The archive includes the identical paper PDF, editable TeX, exact diagnostic code, results and original license notices. Authored prose is CC BY 4.0; authored code is MIT.', '23331258': 'The archive includes the editable TeX, original proof packet, exact diagnostic code, results and historical audit material. Authored manuscript, proofs, code and audits in the deposit are licensed CC BY 4.0; external references retain their own terms.'}
def expected_body(c):
    rid=str(c['source_binding']['record_id'])
    dt=date.fromisoformat(c['publication_date']);day=f'{dt.day} {dt.strftime("%B %Y")}';doi='https://doi.org/'+c['doi'];author='; '.join(c.get('authors',[c['author']]))
    words=['Skip to content','Alec Kriebel','Research | Blog | ORCID',c['title'],f"By {author}, independent researcher. {c['publication_date_label']} {day} · {c['edition_label']} · Unrefereed preprint",f"Read the paper (PDF, {c['pdf_pages']} pages) · {c['supplement_label']} · Zenodo record · CC BY 4.0",'Plain-English explanation · Read on this page · Collaboration',c['abstract_heading'],c['abstract'],'The idea in plain English',*c['plain_language'],'The precise result',*c['result'],'Why the result holds',*c['why_it_works'],'Scope and limitations',*c['limitations'],'Status and AI use',c['status'],c['ai_disclosure']]
    if c.get('edition_note'):words.append(c['edition_note'])
    words+=['Read the paper',c['reader_intro'],'Open PDF in a full window · Download PDF · Download the original from Zenodo','Supporting materials',c['supplement_label']+' · Zenodo original complete ZIP',MATERIAL_NOTES[rid],'Collaborate on this result',c['collaboration'],'Authorship and responsibilities would be discussed in relation to the substantive contributions made.','Contact Alec','Cite this paper',f"{author}. ({dt.year}). {c['title']} ({c['citation_edition_label']}) [Preprint]. Zenodo. {doi}",'Download BibTeX','Background and prior work']
    words += [x['title']+(' : '+x['note'] if x.get('note') else '') for x in c['background']]
    words+=['Research home | me@aleckriebel.com','© 2013–2026 Kriebel LLC.']
    return ' '.join(' '.join(words).split())
