"""Add only exact-three dispatch and text contract in private proposals."""
from pathlib import Path
import ast,difflib,json
O=Path(__file__).resolve().parent;P=O.parents[1]
def once(s,a,b):
    if s.count(a)!=1:raise RuntimeError('expected_one:'+a[:90])
    return s.replace(a,b,1)
r0=(O/'inputs/render_page.py').read_text();c0=(O/'inputs/final-content-check.py').read_text()
imp='from ambient_block_modulus_source import ABM_IDS, STATUSES as ABM_STATUSES, ambient_block_modulus_source_view, normalize_abm_abstract'
r=once(r0,'ROOT = Path(__file__).resolve().parents[1]',imp+'\n\nROOT = Path(__file__).resolve().parents[1]')
r=once(r,"assert gate['status'] == 'PASS'","if paper.name not in ABM_IDS:assert gate['status'] == 'PASS'")
r=once(r,'if paper.name in SG_IDS:\n    raw_receipt, receipt, asset_root = spanning_sos_gin_source_view',"if paper.name in ABM_IDS:\n    raw_receipt, receipt, asset_root = ambient_block_modulus_source_view(paper,c,gate)\n    receipt_path=paper/c['source_binding']['source_receipt_path']\nelif paper.name in SG_IDS:\n    raw_receipt, receipt, asset_root = spanning_sos_gin_source_view")
# Only membership conditions gain these IDs; no old record changes branches.
r=r.replace('if paper.name in SG_IDS else {}','if paper.name in SG_IDS or paper.name in ABM_IDS else {}').replace("if paper.name in SG_IDS else f'https", "if paper.name in SG_IDS or paper.name in ABM_IDS else f'https")
r=r.replace('or paper.name in SG_IDS:', 'or paper.name in SG_IDS or paper.name in ABM_IDS:').replace('or paper.name in SG_IDS else','or paper.name in SG_IDS or paper.name in ABM_IDS else')
r=once(r,"if paper.name in SG_IDS:paper_intro=c['reader_intro']","if paper.name in SG_IDS or paper.name in ABM_IDS:paper_intro=c['reader_intro']")
r=once(r,'if paper.name in SG_IDS:\n    tex_link=',"if paper.name in ABM_IDS:\n    sections+=f'<section id=\"materials\"><h2>Supporting materials</h2><ul><li><a href=\"{h(c[\"supplement_filename\"])}\" download>{h(c[\"supplement_label\"])}</a> · <a href=\"{h(sg_asset_urls[c[\"supplement_filename\"]])}\">Zenodo original complete ZIP</a></li></ul></section>'\nelif paper.name in SG_IDS:\n    tex_link=")
r=once(r,"if paper.name in SG_IDS: bib=","if paper.name in SG_IDS or paper.name in ABM_IDS: bib=")
c=once(c0,'parser=argparse.ArgumentParser',imp+'\nfrom abm_body_contract import BodyText as ABMBodyText, expected_body as expected_abm_body\nparser=argparse.ArgumentParser')
c=once(c,'TEX_PATHS={',"TEX_PATHS={\n '23333353':'published-source/ambient_independence_verification/ambient_independence.tex',\n '23416806':'published-source/paper.tex',\n '23441617':'published-source/manuscript/main.tex',")
c=once(c,'def abstract_tokens(tex,record_id=None):','def abstract_tokens(tex,record_id=None):\n if record_id in ABM_IDS:return wt(normalize_abm_abstract(record_id,tex))')
c=once(c,' if rid in SG_IDS:\n  gate=json.loads'," if rid in ABM_IDS:\n  gate=json.loads((p/'promotion.json').read_text());raw_receipt,receipt,asset_root=ambient_block_modulus_source_view(p,c,gate);receipt_file=p/c['source_binding']['source_receipt_path']\n elif rid in SG_IDS:\n  gate=json.loads")
c=once(c,"if rid in SG_IDS:test('bibtex'","if rid in SG_IDS or rid in ABM_IDS:test('bibtex'")
c=c.replace('or rid in SG_IDS else','or rid in SG_IDS or rid in ABM_IDS else')
c=once(c," if rid in SG_IDS:record_file="," if rid in SG_IDS or rid in ABM_IDS:record_file=")
c=once(c,'and rid not in SG_IDS:\n  materials=', 'and rid not in SG_IDS and rid not in ABM_IDS:\n  materials=')
c=once(c,"test('promotion_pdf_binding',gate['status']=='PASS'", "test('promotion_pdf_binding',(gate['status']==ABM_STATUSES[rid] if rid in ABM_IDS else gate['status']=='PASS')")
c=once(c," result['papers'][rid]=",(O/'new-record-checks.block.txt').read_text()+" result['papers'][rid]=")
for n,s in [('render_page.proposed.py',r),('final-content-check.proposed.py',c)]:ast.parse(s);(O/n).write_text(s)
rs=once(r,'ROOT = Path(__file__).resolve().parents[1]','ROOT = Path('+repr(str(P))+')');rs=once(rs,"SITE = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public/research')",'SITE = Path('+repr(str(O/'public/research'))+')')
cs=once(c,'R=Path(__file__).resolve().parents[1]','R=Path('+repr(str(P))+')')
for n,s in [('render_page.stage.py',rs),('final-content-check.stage.py',cs)]:ast.parse(s);(O/n).write_text(s)
for a,b,n in [(r0,r,'shared-renderer'),(c0,c,'shared-checker'),(r,rs,'renderer-private-overrides'),(c,cs,'checker-private-overrides')]:
    (O/(n+'.diff')).write_text(''.join(difflib.unified_diff(a.splitlines(True),b.splitlines(True),fromfile='current' if n.startswith('shared') else 'proposed',tofile='proposed' if n.startswith('shared') else 'private-only')))
for fn in ['ambient_block_modulus_source.py','abm_body_contract.py']:(O/(fn+'.diff')).write_text(''.join(difflib.unified_diff([], (O/fn).read_text().splitlines(True),fromfile='/dev/null',tofile='scripts/'+fn)))
print('PRIVATE_PROPOSALS_ONLY')
