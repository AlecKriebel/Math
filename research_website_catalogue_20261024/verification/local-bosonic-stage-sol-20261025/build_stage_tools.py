"""Build exact production proposals and private copies; no production writes."""
from pathlib import Path
import ast, copy, datetime, difflib, hashlib, json, re, shutil, unicodedata, warnings
O=Path(__file__).resolve().parent
R=O.parents[1]
Q=R/'verification/local-quadratic-stage-sol-20261025'
S=O/'public'
LIVE=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public')
changes=[]
def replace(text,old,new):
    assert text.count(old)==1,old
    changes.append((old,new))
    return text.replace(old,new,1)
def write(name,text):
    path=O/name
    if path.exists():
        history=O/'iterations'/sha(path)
        history.mkdir(parents=True,exist_ok=True)
        if not (history/name).exists():shutil.copyfile(path,history/name)
    path.write_text(text)
def patch(name,old,new,a,b):
    write(name,''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile=a,tofile=b)))
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

renderer=(O/'inputs/render_page.py').read_text()
original_renderer=renderer
renderer=replace(renderer,'from published_assets import PublishedAssets, asset_name, normalized_receipt_view','from published_assets import PublishedAssets, asset_name, normalized_receipt_view\nfrom bosonic_source import bosonic_source_view')
renderer=replace(renderer,"raw_receipt = json.loads((paper/'sources/receipt.json').read_bytes())\nreceipt = normalized_receipt_view(raw_receipt)\nassets = PublishedAssets(paper/'sources', receipt, c.get('source_binding', {}).get('embedded_assets', []))", "receipt_path = paper/'sources/receipt.json'\nasset_root = paper/'sources'\nif paper.name == '23203100':\n    raw_receipt, receipt, asset_root = bosonic_source_view(paper, c, gate)\n    receipt_path = paper/c['source_binding']['receipt_path']\nelse:\n    raw_receipt = json.loads(receipt_path.read_bytes())\n    receipt = normalized_receipt_view(raw_receipt)\nassets = PublishedAssets(asset_root, receipt, c.get('source_binding', {}).get('embedded_assets', []))")
renderer=replace(renderer,"hashlib.sha256((paper/'sources/receipt.json').read_bytes()).hexdigest()","hashlib.sha256(receipt_path.read_bytes()).hexdigest()")
renderer=replace(renderer,"schema={'@context'", "if c['version'] is None: article.pop('version')\nschema={'@context'")
renderer=replace(renderer,"sections+=f'<section id=\"paper\"", "pdf_download=f'<a href=\"{h(c[\"pdf_filename\"])}\" download>Download PDF</a> · ' if paper.name=='23203100' else ''\nsections+=f'<section id=\"paper\"")
renderer=replace(renderer,'Open PDF in a full window</a> · <a href="https://zenodo.org/records/','Open PDF in a full window</a> · {pdf_download}<a href="https://zenodo.org/records/')
renderer=replace(renderer,"citation_edition_label=c.get('citation_edition_label', 'Version '+c['version'])", "citation_edition_label=c['citation_edition_label'] if 'citation_edition_label' in c else ('Version '+c['version'] if c['version'] is not None else 'No version number supplied')")
renderer=replace(renderer,"if c.get('supplement_filename'):\n    download_links.append", "if paper.name=='23203100':\n    download_links.append(f'<a href=\"{h(c[\"pdf_filename\"])}\" download>Download PDF</a>')\nif c.get('supplement_filename'):\n    download_links.append")
renderer=replace(renderer,"h(c.get('edition_label', 'Version '+c['version']))", "h(c['edition_label'] if 'edition_label' in c else ('Version '+c['version'] if c['version'] is not None else 'No version number supplied'))")
renderer=replace(renderer,"bibtex_note=c.get('bibtex_note', 'Unrefereed preprint, version '+c['version'])", "bibtex_note=c['bibtex_note'] if 'bibtex_note' in c else ('Unrefereed preprint, version '+c['version'] if c['version'] is not None else 'Unrefereed preprint; no version number supplied')")
renderer_changes=changes[:];changes=[]
write('render_page.proposed.py',renderer)
patch('proposed-shared-renderer.diff',original_renderer,renderer,'a/scripts/render_page.py','b/scripts/render_page.py')
stage_renderer=renderer.replace('ROOT = Path(__file__).resolve().parents[1]','ROOT = Path('+repr(str(R))+')').replace("SITE = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public/research')",'SITE = Path('+repr(str(S/'research'))+')')
stage_renderer=stage_renderer.replace('from published_assets import', 'sys.path.insert(0, '+repr(str(R/'scripts'))+')\nfrom published_assets import',1)
write('render_page.stage.py',stage_renderer)
patch('renderer-staging-overrides.diff',renderer,stage_renderer,'proposed production renderer','owned stage renderer')
shutil.copyfile(O/'bosonic_source.proposed.py',O/'bosonic_source.py')
patch('proposed-new-source-adapter.diff','',(O/'bosonic_source.proposed.py').read_text(),'/dev/null','b/scripts/bosonic_source.py')

normalizers=r'''def normalized_bosonic_abstract(body):
 return ' '.join(body.replace('--','–').split())
def normalized_amplifier_abstract(body):
 body=body.replace('\n\\[\n',' ').replace('\n\\]\n',' ')
 for old,new in [('R^6-8R^5+22R^4-30R^3+21R^2-6R+1.','R⁶ − 8R⁵ + 22R⁴ − 30R³ + 21R² − 6R + 1.'),(r'r\in(1,R)','r ∈ (1,R)'),(r'1<r<\Rhyb','1 < r < R_hyb'),(r'\Rsim\geq\Rhyb=1.5028569127905696\ldots>3/2','R_sim ≥ R_hyb = 1.5028569127905696… > 3/2'),(r'\Rsim','R_sim'),(r'\Rhyb','R_hyb'),(r'(\sigma,\lambda)','(σ,λ)'),('$',''),('--','–')]:body=body.replace(old,new)
 if '\\' in body:raise ValueError('Unrecognized amplifier abstract command')
 return '\n\n'.join(' '.join(p.split()) for p in re.split(r'\n\s*\n',body.strip()))
'''
# These are source text, so only the ordinary string escapes in the function
# bodies need one level of reduction; raw TeX literals stay literal.
normalizers=normalizers.replace("'\\n\\\\[\\n'", "'\\n\\\\[\\n'")
checker=(Q/'final-content-check.proposed.py').read_text()
quadratic_checker=checker
checker=replace(checker,'from published_assets import PublishedAssets, asset_name, normalized_receipt_view','from published_assets import PublishedAssets, asset_name, normalized_receipt_view\nfrom bosonic_source import bosonic_source_view')
checker=replace(checker,'BRAID_WAVE_WREATH_IDS=',normalizers+'BRAID_WAVE_WREATH_IDS=')
checker=replace(checker," '23356964':'published-source/generic-wreath-hyperfiniteness-verification/note.tex',\n"," '23356964':'published-source/generic-wreath-hyperfiniteness-verification/note.tex',\n '23203100':'extracted/zenodo-upload-kit/manuscript/main.tex',\n '22089807':'published-source/universal_simultaneous_amplification/phase4_landmark_closure/paper_hybrid_threshold/main.tex',\n")
checker=replace(checker,'def abstract_tokens(tex,record_id=None):\n',"def abstract_tokens(tex,record_id=None):\n if record_id=='23203100':return wt(normalized_bosonic_abstract(tex))\n if record_id=='22089807':return wt(normalized_amplifier_abstract(tex))\n")
checker=replace(checker,"all(art[k]==c[k] for k in ['description','abstract','version'])", "all(art[k]==c[k] for k in ['description','abstract']) and (('version' not in art) if rid=='23203100' else art['version']==c['version'])")
checker=replace(checker," raw_receipt=json.loads((p/'sources/receipt.json').read_bytes());receipt=normalized_receipt_view(raw_receipt); hashes={'html':sha(f),'publication':sha(p/'publication.json')}\n resolver=PublishedAssets(p/'sources',receipt,c.get('source_binding',{}).get('embedded_assets',[]))", " receipt_file=p/'sources/receipt.json';asset_root=p/'sources'\n if rid=='23203100':\n  gate=json.loads((p/'promotion.json').read_text());raw_receipt,receipt,asset_root=bosonic_source_view(p,c,gate);receipt_file=p/c['source_binding']['receipt_path']\n else:raw_receipt=json.loads(receipt_file.read_bytes());receipt=normalized_receipt_view(raw_receipt)\n hashes={'html':sha(f),'publication':sha(p/'publication.json')}\n resolver=PublishedAssets(asset_root,receipt,c.get('source_binding',{}).get('embedded_assets',[]))")
checker=replace(checker,"c.get('bibtex_note','Unrefereed preprint, version '+c['version'])", "(c['bibtex_note'] if 'bibtex_note' in c else ('Unrefereed preprint, version '+c['version'] if c['version'] is not None else 'Unrefereed preprint; no version number supplied'))")
checker=replace(checker,"record_file=p/'sources'/('metadata.json' if rid=='23306332' else 'record.json')", "record_file=p/'sources'/('metadata.json' if rid=='23306332' else 'record/zenodo_record.json' if rid=='23203100' else 'record.json')")
checker=replace(checker,"rid in ('21699161','23203334')", "rid in ('21699161','23203334','23203100')")
checker=replace(checker,"gate['pdf_sha256']==sha(p/'sources'/c['pdf_filename'])", "gate['pdf_sha256']==sha(asset_root/c['pdf_filename'])")
checker=replace(checker," result['papers'][rid]={'checks':checks,",(O/'bosonic-checks.block.txt').read_text()+(O/'amplifier-checks.block.txt').read_text()+" result['papers'][rid]={'checks':checks,")
write('final-content-check.proposed.py',checker)
patch('proposed-shared-checker.diff',(O/'inputs/final-content-check.py').read_text(),checker,'a/verification/final-content-check.py','b/verification/final-content-check.py')
patch('proposed-checker-after-quadratic.diff',quadratic_checker,checker,'accepted quadratic checker proposal','combined checker proposal')
stage_checker=checker.replace("sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))",'sys.path.insert(0, '+repr(str(R/'scripts'))+')')
stage_checker=stage_checker.replace('R=Path(__file__).resolve().parents[1]','R=Path('+repr(str(R))+')')
stage_checker=stage_checker.replace('\n   good=q.is_file()\n',"\n   if not q.is_file() and u.path in ('/','/blog/','/favicon.ico'):\n    q=Path("+repr(str(LIVE))+")/unquote(u.path).lstrip('/')\n    if q.is_dir():q=q/'index.html'\n   good=q.is_file()\n")
write('final-content-check.stage.py',stage_checker)
patch('checker-staging-overrides.diff',checker,stage_checker,'proposed production checker','owned stage checker')
# Inverting every declared modification recovers the accepted quadratic source
# byte-for-byte, preserving its entire branch and all original dispatches.
restored=checker
for old,new in reversed(changes):
    assert restored.count(new)==1,new
    restored=restored.replace(new,old,1)
assert restored==quadratic_checker
restored_renderer=renderer
for old,new in reversed(renderer_changes):restored_renderer=restored_renderer.replace(new,old,1)
assert restored_renderer==original_renderer
for name in ['render_page.proposed.py','render_page.stage.py','final-content-check.proposed.py','final-content-check.stage.py','bosonic_source.proposed.py']:
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter('always');compile((O/name).read_text(),name,'exec')
    assert not caught,[(str(x.message)) for x in caught]
write('integration-static-checks.json',json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'completion_percent':35,'status':'PASS','accepted_quadratic_source_recovered_byte_for_byte':True,'original_renderer_recovered_byte_for_byte':True,'original_checker_sha256':sha(R/'verification/final-content-check.py'),'production_proposals_contain_private_paths':any('local-bosonic-stage' in (O/n).read_text() for n in ['render_page.proposed.py','final-content-check.proposed.py','bosonic_source.proposed.py']),'original_46_mappings_and_quadratic_mapping_unchanged':True,'syntax_warnings':[]},indent=2)+'\n')
print('Production proposals and private copies built; current shared scripts unchanged.')
