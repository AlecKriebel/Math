from pathlib import Path
import difflib
E=Path(__file__).resolve().parent;P=E.parents[1]
def change(s,a,b,n=1):
 if s.count(a)!=n:raise ValueError(('replacement count',a,s.count(a),n))
 return s.replace(a,b)
s=(E/'inputs/render_page.py').read_text()
s=change(s,'from odd_ear_blocking_source import OEB_IDS, STATUSES as OEB_STATUSES, odd_ear_blocking_source_view, approved_material_note','from odd_ear_blocking_source import OEB_IDS, STATUSES as OEB_STATUSES, odd_ear_blocking_source_view, approved_material_note\nfrom banach_mtp2_source import BM_IDS, banach_mtp2_source_view')
s=change(s,"if paper.name not in ABM_IDS and paper.name not in OEB_IDS:assert", "if paper.name not in ABM_IDS and paper.name not in OEB_IDS and paper.name not in BM_IDS:assert")
s=change(s,'if paper.name in OEB_IDS:\n    raw_receipt',"if paper.name in BM_IDS:\n    raw_receipt, receipt, asset_root = banach_mtp2_source_view(paper,c,gate)\n    receipt_path=paper/c['source_binding']['source_receipt_path']\nelif paper.name in OEB_IDS:\n    raw_receipt")
# Existing branches are otherwise unchanged for all old record IDs.
s=s.replace('or paper.name in OEB_IDS else','or paper.name in OEB_IDS or paper.name in BM_IDS else')
s=s.replace('or paper.name in OEB_IDS:', 'or paper.name in OEB_IDS or paper.name in BM_IDS:')
start=s.index('sections+=f\'<section id="paper"');end=s.index('\nif paper.name in OEB_IDS:',start)
old=s[start:end]
s=s[:start]+'''if paper.name in BM_IDS:
    sections+=f'<section id="paper"><h2>Read the paper</h2>{paper_intro_html}<p><a href="{h(c["pdf_filename"])}">Open PDF</a> · <a href="{h(c["pdf_filename"])}" download>Download PDF</a> · <a href="{h(original_pdf_url)}" download>Download original PDF from Zenodo</a></p><iframe class="paper-pdf" src="{h(c["pdf_filename"])}#view=FitH" title="{h(c["title"])} — complete {c["pdf_pages"]}-page paper" loading="lazy"></iframe></section>'
else:
    '''+old+ s[end:]
s=change(s,'if paper.name in OEB_IDS:\n    sections+=', '''if paper.name in BM_IDS:
    sections+=f'<section id="materials"><h2>Supporting materials</h2><ul><li><a href="{h(c["supplement_filename"])}" download>Download complete ZIP</a> · <a href="{h(sg_asset_urls[c["supplement_filename"]])}" download>Download original complete ZIP from Zenodo</a></li>'+''.join(f'<li><a href="{h(x["url"])}">{h(x["label"])}</a></li>' for x in c['related_resources'])+'</ul></section>'
    if paper.name=='23217863': sections+=section('licensing','Licensing',[c['license'],c['license_note']])
elif paper.name in OEB_IDS:
    sections+=''')
s=change(s,"sections+=f'<section id=\"cite\">", "bibtex_download=' download' if paper.name in BM_IDS else ''\nsections+=f'<section id=\"cite\">")
s=change(s,'<a href="citation.bib">Download BibTeX','<a href="citation.bib"{bibtex_download}>Download BibTeX')
(E/'render_page.proposed.py').write_text(s)
# Private runtime paths are separated from the reviewable installation proposal.
r=s.replace('ROOT = Path(__file__).resolve().parents[1]',f'ROOT = Path({str(P)!r})').replace("SITE = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public/research')",f'SITE = Path({str(E/"public/research")!r})')
(E/'render_page.stage.py').write_text(r)
(E/'render_page.diff').write_text(''.join(difflib.unified_diff((E/'inputs/render_page.py').read_text().splitlines(True),s.splitlines(True),fromfile='installed/scripts/render_page.py',tofile='proposed/scripts/render_page.py')))
