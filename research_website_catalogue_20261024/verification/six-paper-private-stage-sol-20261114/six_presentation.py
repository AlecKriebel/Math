"""Approved auxiliary wording and exact record-specific reader interfaces."""
from six_common import *
import re
LICENSE_NOTICES={
 '23539734':['Authored text and code: CC BY 4.0. Third-party cited works retain their own rights.'],
 '22929857':['Paper, LaTeX, research notes, review reports and prose: CC BY 4.0. Python scripts and website code: MIT. Third-party works retain their own rights.'],
 '23320818':['Authored paper and accompanying materials are CC BY 4.0; third-party works retain their own rights.']}
MATERIAL_NOTES={
 '22929857':['The complete ZIP includes the editable manuscript, verification companions and internal AI-assisted review materials. Exact algebra and ordinary numerical diagnostics are supporting checks; the analytic proof carries the theorem.'],
 '23320818':['The complete original ZIP contains the manuscript source, verification companions and preserved available historical inputs. The complete PDF is a separate native asset. The analytic proof establishes the quantified claims; finite exact computations provide supporting consistency and falsification evidence.']}
def presentation(bundle):
    rid=bundle['rid'];c=bundle['c'];E=bundle['paper']/'reviews/editorial'
    if rid in {'23124601','23333046'}:
        r=load(E/'READER_REQUIREMENTS.json');links=r['required_links'];src=c['pdf_filename']+'#view=FitH';title=r['pdf_iframe_title']
        pdf=links[:3];ziplinks=links[3:5];bib=links[5];downloads={x['href']:None for x in links if x['download']}
    elif rid=='23383952':
        r=load(E/'PUBLICATION_REQUIREMENTS.json');src=c['pdf_filename']+'#view=FitH';title=r['pdf']['iframe_title']
        pdf=[{'href':c['pdf_filename'],'label':'Open PDF in a full window','download':False},
             {'href':c['pdf_filename'],'label':'Download PDF','download':True},
             {'href':r['pdf']['zenodo_original_link'],'label':'Zenodo original PDF','download':True}]
        ziplinks=[{'href':c['supplement_filename'],'label':'Download the complete manuscript source and verification materials (ZIP)','download':True},
                  {'href':r['support']['zenodo_original_link'],'label':'Zenodo original complete ZIP','download':True}]
        bib={'href':'citation.bib','label':'Download BibTeX','download':True};downloads={x['href']:None for x in [*pdf,*ziplinks,bib] if x['download']}
    else:
        r=load(E/'PUBLICATION_REQUIREMENTS.json')['reader'];src=r['iframe_src'];title=r['accessible_title']
        openlabel={'23539734':'Open complete PDF','22929857':'Open the complete PDF','23320818':'Open the complete PDF'}[rid]
        dl={'23539734':'Download complete PDF','22929857':'Download the complete PDF','23320818':'Download the complete PDF'}[rid]
        zl={'23539734':'Download complete original ZIP','22929857':'Download the complete reproducibility ZIP','23320818':'Download the complete verification ZIP'}[rid]
        pdf=[{'href':r['direct_open'],'label':openlabel,'download':False},
             {'href':r['local_PDF_download']['href'],'label':dl,'download':True},
             {'href':r['original_PDF_open_and_download'],'label':'Zenodo original PDF','download':True}]
        ziplinks=[{'href':r['local_ZIP_download']['href'],'label':zl,'download':True},
                  {'href':r['original_complete_ZIP_download'],'label':'Zenodo original ZIP','download':True}]
        bib={'href':r['citation_download']['href'],'label':'Download BibTeX','download':True}
        downloads={pdf[1]['href']:c['pdf_filename'],pdf[2]['href']:c['pdf_filename'],ziplinks[0]['href']:c['supplement_filename'],ziplinks[1]['href']:c['supplement_filename'],bib['href']:'citation.bib'}
    text=(E/'PUBLIC_COPY.md').read_text();plain=re.sub(r'\[([^\]]+)\]\([^\n]+?\)',r'\1',text).replace('**','')
    for p in [*LICENSE_NOTICES.get(rid,[]),*MATERIAL_NOTES.get(rid,[])]:require(p in plain,'auxiliary_text_is_root_adopted_copy')
    return {'pdf_links':pdf,'zip_links':ziplinks,'bib_link':bib,'download_values':downloads,'iframe_src':src,'iframe_title':title,
            'license_notices':LICENSE_NOTICES.get(rid,[]),'material_notes':MATERIAL_NOTES.get(rid,[])}
