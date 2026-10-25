"""Create standalone proposed code/overrides; never mutate current originals."""
from pathlib import Path
import ast,difflib,hashlib,json,shutil

O=Path(__file__).resolve().parent;R=O.parents[1]
require=lambda x,msg: x or (_ for _ in ()).throw(RuntimeError(msg))
(O/'inputs').mkdir(exist_ok=True)
original_renderer=(R/'scripts/render_page.py').read_text()
original_checker=(R/'verification/final-content-check.py').read_text()
for name,text in [('render_page.py',original_renderer),('final-content-check.py',original_checker)]:
    f=O/'inputs'/name
    if f.exists():require(f.read_text()==text,'immutable_input_copy_changed')
    else:f.write_text(text)

def once(text,old,new):
    require(text.count(old)==1,'expected_exact_one:'+old[:90])
    return text.replace(old,new,1)

r=once(original_renderer,'from cfh_source import CFH_IDS, cfh_source_view','from cfh_source import CFH_IDS, cfh_source_view\nfrom cylinder_discotope_source import CD_IDS, cylinder_discotope_source_view, display_cd_abstract')
r=once(r,'if paper.name in CFH_IDS:\n    raw_receipt, receipt, asset_root = cfh_source_view(paper, c, gate)','if paper.name in CD_IDS:\n    raw_receipt, receipt, asset_root = cylinder_discotope_source_view(paper, c, gate)\nelif paper.name in CFH_IDS:\n    raw_receipt, receipt, asset_root = cfh_source_view(paper, c, gate)')
r=once(r,"authors=c.get('authors',[c['author']])","authors=c.get('authors',[c['author']])\nrendered_abstract=display_cd_abstract(paper.name,c['abstract']) if paper.name in CD_IDS else c['abstract']")
r=once(r,"'abstract':c['abstract']","'abstract':rendered_abstract")
r=once(r,"c['abstract'].split('\\n\\n')","rendered_abstract.split('\\n\\n')")
r=r.replace('or paper.name in CFH_IDS','or paper.name in CFH_IDS or paper.name in CD_IDS')
r=once(r,"original_pdf_download=' download' if paper.name in CFH_IDS else ''","original_pdf_download=' download' if paper.name in CFH_IDS or paper.name in CD_IDS else ''")
r=once(r,'if paper.name in CFH_IDS:\n    checksum_link=','if paper.name in CFH_IDS or paper.name in CD_IDS:\n    checksum_link=')
r=once(r,"paper_intro={'23383961'","paper_intro={'23387774':'Read the complete 7-page paper in the on-page PDF reader.','23074543':'Read the complete 4-page paper in the on-page PDF reader.','23383961'")
group="('23444606','23440119','23224103','23390551','23430326','23204952','22983138','23409904')"
r=r.replace('if paper.name in '+group+':','if paper.name in '+group+' or paper.name in CD_IDS:')
r=once(r,"h(c.get('publication_date_label', 'Published'))","h('Manuscript and declared publication date' if paper.name in CD_IDS else c.get('publication_date_label', 'Published'))")
old_background=next(x for x in r.splitlines() if x.startswith("sections+='<section id=\"background\""))
new_background="""def background_entry(x):
    title=h(x['title'])
    link=(f'<span>{title}</span>' if paper.name in CD_IDS and not x['url'] else f'<a href="{h(x["url"])}">{title}</a>')
    return '<li>'+link+(': '+h(x['note']) if x.get('note') else '')+'</li>'
sections+='<section id="background"><h2>Background and prior work</h2><ul>'+''.join(background_entry(x) for x in c['background'])+'</ul></section>'"""
r=once(r,old_background,new_background)
related="""if paper.name in CD_IDS and c.get('related_resources'):
    sections+='<section id="related"><h2>Related source editions</h2><ul>'+''.join(f'<li><a href="{h(x["url"])}">{h(x["title"])}</a>'+(': '+h(x['note']) if x.get('note') else '')+'</li>' for x in c['related_resources'])+'</ul></section>'
"""
r=once(r,"sections+=section('collaborate'",related+"sections+=section('collaborate'")

c=once(original_checker,'from cfh_source import cfh_source_view, normalized_cfh_abstract','from cfh_source import cfh_source_view, normalized_cfh_abstract\nfrom cylinder_discotope_source import CD_IDS, PINS as CD_PINS, cylinder_discotope_source_view, normalized_cd_abstract, display_cd_abstract')
c=once(c,'TEX_PATHS={',"TEX_PATHS={\n '23387774':'published-source/cylinder_areas.tex',\n '23074543':'published-source/paper.tex',")
c=once(c,'def abstract_tokens(tex,record_id=None):','def abstract_tokens(tex,record_id=None):\n if record_id in CD_IDS:return wt(normalized_cd_abstract(record_id,tex))')
c=once(c,"all(art[k]==c[k] for k in ['description','abstract'])","all(art[k]==(display_cd_abstract(rid,c[k]) if rid in CD_IDS and k=='abstract' else c[k]) for k in ['description','abstract'])")
c=once(c,"expected=c[key] if isinstance(c[key],list) else c[key].split('\\n\\n')","expected=c[key] if isinstance(c[key],list) else c[key].split('\\n\\n')\n  if rid in CD_IDS and key=='abstract':expected=[display_cd_abstract(rid,c['abstract'])]")
c=once(c,'if rid in CFH_IDS:\n  gate=json.loads',"if rid in CD_IDS:\n  gate=json.loads((p/'promotion.json').read_text());raw_receipt,receipt,asset_root=cylinder_discotope_source_view(p,c,gate)\n elif rid in CFH_IDS:\n  gate=json.loads")
c=c.replace('or rid in CFH_IDS else','or rid in CFH_IDS or rid in CD_IDS else')
record_line=next(x for x in c.splitlines() if x.startswith(' record_file='))
c=once(c,record_line," if rid in CD_IDS:record_file=p/'sources/zenodo-record.raw.json'\n else:"+record_line.strip())
c=once(c,"if c.get('edition_label'):test(","if c.get('edition_label') and rid not in CD_IDS:test(")
c=once(c,"and rid not in CFH_IDS:\n  materials=","and rid not in CFH_IDS and rid not in CD_IDS:\n  materials=")
new_checks=(O/'new-record-checks.block.txt').read_text()
c=once(c," result['papers'][rid]=",new_checks+" result['papers'][rid]=")

for name,text in [('render_page.proposed.py',r),('final-content-check.proposed.py',c)]:
    ast.parse(text);(O/name).write_text(text)
rs=once(r,'ROOT = Path(__file__).resolve().parents[1]','ROOT = Path('+repr(str(R))+')')
rs=once(rs,"SITE = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public/research')",'SITE = Path('+repr(str(O/'public/research'))+')')
cs=once(c,"R=Path(__file__).resolve().parents[1]",'R=Path('+repr(str(R))+')')
for name,text in [('render_page.stage.py',rs),('final-content-check.stage.py',cs)]:ast.parse(text);(O/name).write_text(text)
for old,new,label in [(original_renderer,r,'shared-renderer'),(original_checker,c,'shared-checker'),(r,rs,'renderer-staging-overrides'),(c,cs,'checker-staging-overrides')]:
    (O/(label+'.diff')).write_text(''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile='current' if 'shared' in label else 'proposed',tofile='proposed' if 'shared' in label else 'private-stage')))
(O/'new-helper.diff').write_text(''.join(difflib.unified_diff([], (O/'cylinder_discotope_source.py').read_text().splitlines(True),fromfile='/dev/null',tofile='scripts/cylinder_discotope_source.py')))
report={'status':'STATIC_PROPOSALS_CREATED','only_two_new_IDs':['23387774','23074543'],'originals_written':False,'proposed_hashes':{n:hashlib.sha256((O/n).read_bytes()).hexdigest() for n in ['cylinder_discotope_source.py','render_page.proposed.py','final-content-check.proposed.py']},'stage_overrides':'Only explicit programme/site root constants; no source fixtures, aliases or production files changed.'}
(O/'proposal-static-checks.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
