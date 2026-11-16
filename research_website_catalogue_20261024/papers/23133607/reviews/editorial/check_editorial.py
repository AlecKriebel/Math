"""CC BY 4.0, Alec Kriebel 2026. Pure read-only editorial data guard.
No writes, subprocess, network, scientific imports, or native execution.
The explicit sealer is a separate file. Frozen packets are rejected.
"""
from pathlib import Path
from html.parser import HTMLParser
import hashlib
import json
import re
import zipfile

OWN = Path(__file__).resolve().parent
P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
SOURCE = P/'papers/23133607/sources'
TERMINALS = ['OWNED_MANIFEST.json','FINAL.json']

def require(ok, message):
    if not ok:
        raise ValueError(message)

def data_pin(data):
    return {'bytes':len(data),'SHA256':hashlib.sha256(data).hexdigest()}

def file_pin(path):
    require(path.is_file() and not path.is_symlink(), 'ordinary file required: '+str(path))
    return data_pin(path.read_bytes())

def check_pin(path, expected):
    actual=file_pin(path)
    require(actual['SHA256']==expected['SHA256'] and ('bytes' not in expected or actual['bytes']==expected['bytes']), 'pin mismatch: '+str(path))
    return actual

def load(path):
    return json.loads(path.read_text())

def inventory(root):
    files, dirs = {}, []
    for path in sorted(root.rglob('*')):
        require(not path.is_symlink(), 'symlink rejected: '+str(path))
        name=path.relative_to(root).as_posix()
        if path.is_dir():
            dirs.append(name)
        elif path.is_file():
            files[name]=file_pin(path)
        else:
            require(False,'nonordinary object: '+str(path))
    return files,dirs

def frozen_namespace(ref):
    root=P/ref['root']
    manifest_path=root/ref['manifest']
    check_pin(manifest_path,{'SHA256':ref['manifest_SHA256']})
    manifest=load(manifest_path)
    keys=['excluded_terminal_files','exact_root_terminal_exclusions','exact_outer_terminal_names','exact_terminal_controls','exact_existing_root_terminal_controls']
    exclusions=next(manifest[key] for key in keys if key in manifest)
    require(exclusions==list(ref['terminals']), 'exact terminal order: '+ref['root'])
    if 'payloads' in manifest:
        expected=manifest['payloads']
    else:
        expected={row['path']:{'bytes':row['bytes'],'SHA256':row['SHA256']} for row in manifest['files']}
        require(len(expected)==len(manifest['files']),'duplicate paths')
    actual,dirs=inventory(root)
    require(set(actual)==set(expected)|set(ref['terminals']), 'finite files: '+ref['root'])
    require(dirs==manifest['directories'] and len(dirs)==ref['directories'] and len(actual)==ref['files'], 'finite directories/counts: '+ref['root'])
    for name,meta in expected.items():
        require(actual[name]==meta,'changed protected payload: '+str(root/name))
    for name,digest in ref['terminals'].items():
        require(actual[name]['SHA256']==digest,'changed protected terminal: '+str(root/name))
    return {'root':ref['root'],'files':len(actual),'directories':len(dirs),'manifest':file_pin(manifest_path),'terminals':{name:actual[name] for name in ref['terminals']},'whole_finite_extent_verified':True}

class Facts(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids,self.anchors,self.iframes,self.canonical,self.bases=[],[],[],[],[]
        self.meta={}
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:
            self.ids.append(a['id'])
        if tag=='a':
            self.anchors.append({'href':a.get('href'),'download':'download' in a})
        if tag=='iframe':
            self.iframes.append(a)
        if tag=='meta':
            key=a.get('name',a.get('property'))
            require(key not in self.meta,'duplicate metadata')
            self.meta[key]=a.get('content')
        if tag=='base':
            self.bases.append(a)
        if tag=='link' and a.get('rel')=='canonical':
            self.canonical.append(a)

class Text(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.pieces=[]
    def handle_data(self,data):
        self.pieces.append(data)

def plain(fragment):
    parser=Text()
    parser.feed(fragment)
    return ' '.join(''.join(parser.pieces).split())

def audit(closing=False):
    final=OWN/'FINAL.json'
    require(not final.exists() or (closing and final.read_bytes()==b'{}\n'), 'frozen packet: no execution authorized')
    refs=load(OWN/'REFERENCE_PINS.json')
    protected=[frozen_namespace(ref) for ref in refs['namespaces']]
    authority_ref=refs['scientific_authority']
    authority_pin=check_pin(P/authority_ref['path'],authority_ref)
    authority=load(P/authority_ref['path'])
    require(authority['status']=='PASS_FULL_ORIGINAL_SCIENTIFIC_CLAIM' and authority['full_original_claim_preserved'], 'scientific authority')
    core_ref=refs['qualified_core_reference']
    core_pin=check_pin(P/core_ref['path'],core_ref)
    core=load(P/core_ref['path'])
    require(len(core['files'])==18,'qualified 17 plus 405b core')
    for row in core['files']:
        check_pin(P/row['path'],row)
    check_pin(OWN/'INITIAL.md',{'bytes':10854,'SHA256':'68d9395eb95df51b72c408e286c73feded0146757211bf73751a3e789e8529b1'})
    check_pin(OWN/'INITIAL_SEAL.json',{'bytes':2008,'SHA256':'727374f6c426d6e065ec17a690cd21470693715abc4109a41b46d54ef5dd2ef8'})
    for row in load(OWN/'INITIAL_SEAL.json')['complete_initial_payloads']:
        if row['path']=='RESEARCH_LOG.md':
            require(data_pin((OWN/row['path']).read_bytes()[:row['bytes']])=={'bytes':row['bytes'],'SHA256':row['SHA256']},'append-only original log checkpoint')
        else:
            check_pin(OWN/row['path'],row)
    record=load(SOURCE/'record.response.body')
    native_files=load(SOURCE/'files.response.body')
    names=['qss-self-duality-note.pdf','qss-self-duality-verification.zip']
    require([row['key'] for row in record['files']]==names and [row['key'] for row in native_files['entries']]==names,'native two-asset order')
    require(record['metadata']['version']=='1.0' and isinstance(record['metadata']['version'],str),'literal version string')
    assets=[]
    for row in record['files']:
        local=OWN/'preview'/row['key']
        source=SOURCE/'assets'/row['key']
        require(file_pin(local)==file_pin(source) and file_pin(local)['bytes']==row['size'],'unchanged native asset')
        require('md5:'+hashlib.md5(local.read_bytes()).hexdigest()==row['checksum'],'native MD5')
        assets.append({'key':row['key'],**file_pin(local),'original_file_object':row})
    check_pin(OWN/'preview'/names[0],refs['original_PDF'])
    check_pin(OWN/'preview'/names[1],refs['original_ZIP'])
    with zipfile.ZipFile(OWN/'preview'/names[1]) as archive:
        require(archive.testzip() is None,'native ZIP CRC')
        require(sum(not row.is_dir() for row in archive.infolist())==33,'33 native regular payloads')
    tex_path=SOURCE/'published-source/asset-002/qss-self-duality-verification/manuscript.tex'
    check_pin(tex_path,refs['original_TeX'])
    abstract=re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}',tex_path.read_text(),re.S).group(1)
    for old,new in [("Dieudonn\\'e",'Dieudonné'),('$p$','p'),('$p^{2n}$','p^(2n)'),('$n\\geq3$','n ≥ 3'),('$p>3$','p > 3'),('$W(\\overline{\\mathbb F}_p)$','W(algebraic closure of F_p)')]:
        abstract=abstract.replace(old,new)
    abstract=' '.join(abstract.split())
    html_path=OWN/'preview/index.html'
    html=html_path.read_text()
    main=re.search(r'<main id="main">.*?</main>',html,re.S)
    head=re.search(r'<head>.*?</head>',html,re.S)
    require(main is not None and head is not None and html.count('<main')==1,'whole actual MAIN/head')
    facts=Facts()
    facts.feed(html)
    require(len(facts.ids)==len(set(facts.ids)) and facts.ids.count('main')==1,'unique semantic identifiers')
    visible_abstract=plain(re.search(r'<p id="original-abstract">(.*?)</p>',html,re.S).group(1))
    expected_visible=abstract.replace('p^(2n)','p2n').replace('W(algebraic closure of F_p)','W(F̅p)')
    require(visible_abstract==expected_visible,'complete printed abstract including closure bar')
    raw_description=re.search(r'<div id="record-description">(.*?)</div>',html,re.S).group(1)
    require(raw_description==record['metadata']['description'],'complete distinct native description HTML')
    require(not facts.canonical and not facts.bases,'no private production URL')
    require(facts.meta['robots']=='noindex,nofollow,noarchive','private robots')
    require(facts.meta['citation_publication_date']=='2026/10/04' and facts.meta['citation_version']=='1.0','native date/version metadata')
    require(facts.meta['citation_title']==record['metadata']['title'] and facts.meta['citation_doi']==record['doi'],'citation identity')
    structured=json.loads(re.findall(r'<script type="application/ld\+json">(.*?)</script>',html,re.S)[0])
    require(structured['abstract']==abstract and structured['datePublished']=='2026-10-04' and structured['version']=='1.0','JSON-LD original abstract/date/version')
    require('url' not in structured and 'MIT' not in html,'no production URL or invented MIT')
    local_controls=[row for row in facts.anchors if row['href'] in names]
    require(local_controls==[{'href':names[0],'download':False},{'href':names[0],'download':True},{'href':names[1],'download':True}],'native open/download controls')
    original_urls=[row['links']['self'] for row in record['files']]
    require([row['href'] for row in facts.anchors if row['href'] in original_urls]==original_urls,'native original-link order')
    require(len(facts.iframes)==1 and facts.iframes[0]['src']==names[0]+'#view=FitH' and bool(facts.iframes[0]['title']),'titled native embed')
    require({'href':'citation.bib','download':True} in facts.anchors,'BibTeX link')
    main_text=plain(main.group())
    for marker in ['every prime p > 3 and every integer n ≥ 3','algebraic closure of Fp','whose special fiber Hn is quasi-supersingular','Hn ≄ HnD','Gn ≄ GnD']:
        require(marker in main_text,'full claim marker: '+marker)
    require('Private preview' not in main_text and 'private preview' not in main_text,'no administrative preview copy inside MAIN')
    render=load(OWN/'RENDER_RECEIPT.json')
    require(render['status']=='PASS_LOCAL_HEADLESS_LAYOUT' and render['external_requests']==[] and render['page_errors']==[],'render pass')
    require(render['input_bytes_identical_before_after_render'] is True,'render input stability')
    require(list(render['inputs'])==['html','css','renderer'],'complete render inputs')
    require({key:row['path'] for key,row in render['inputs'].items()}=={'html':'preview/index.html','css':'preview/research.css','renderer':'render_preview.mjs'},'exact render input paths')
    for row in render['inputs'].values():
        check_pin(OWN/row['path'],row)
    require([row['width'] for row in render['layouts']]==[1100,390],'bounded render widths')
    require(all(row['audit']['scroll_width']==row['width'] and not row['audit']['overflow'] and row['skip_link_first_focus'] for row in render['layouts']),'render overflow/keyboard')
    require(not (OWN/'render-work').exists(),'temporary browser extent removed')
    helper_reads=load(OWN/'HELPER_READS.json')
    for row in helper_reads['current_helpers']:
        require(row['full_current_body_read_before_execution'],'helper reading')
        check_pin(OWN/row['path'],row)
    bib=(OWN/'preview/citation.bib').read_text()
    require(record['doi'] in bib and record['metadata']['title'] in bib and 'version = {1.0}' in bib and '2026-10-04' in bib,'BibTeX identity')
    main_pin=data_pin(main.group().encode())
    head_pin=data_pin(head.group().encode())
    model={'schema':'private_qss_editorial_v1','record_id':23133607,'sheet_row':140,'native_metadata_original':record['metadata'],'native_created_original':record['created'],'native_record_file_objects_original':record['files'],'native_files_response_original':native_files,'native_version_original':'1.0','printed_version':None,'printed_date':'2026-10-04','manuscript_abstract':abstract,'native_record_description_original':record['metadata']['description'],'base_field':'algebraic closure of F_p','Witt_base':'W(algebraic closure of F_p)','quasi_supersingular_hypothesis':'special fiber only','full_original_claim_retained':True,'proposed_slug':'takao-self-duality-counterexample','canonical_url':None,'base_url':None,'production_url':None,'AA':None,'follow_up':None,'publication_authority':False,'private_preview':True,'rights':{'original_note_and_authored_verification':'CC BY 4.0','new_editorial_materials_and_code':'CC BY 4.0','third_party_rights_retained':True,'MIT_grant':False},'scientific_authority':authority_ref,'assets':assets,'whole_actual_MAIN':main_pin,'whole_head':head_pin}
    content={'status':'PASS_FULL_ORIGINAL_COPY_AND_NATIVE_IDENTITY','page':file_pin(html_path),'whole_actual_MAIN':{**main_pin,'start_byte':len(html[:main.start()].encode()),'end_byte_exclusive':len(html[:main.end()].encode())},'whole_head':head_pin,'BibTeX':file_pin(OWN/'preview/citation.bib'),'CSS':file_pin(OWN/'preview/research.css'),'native_assets':assets,'three_native_controls':local_controls,'original_Zenodo_links':original_urls,'complete_manuscript_abstract_and_native_description':True,'actual_closure_overbar_preserved':True,'native_version':'1.0','printed_version':None,'native_ZIP_CRC_regular_occurrences':33,'no_private_label_in_MAIN':True,'publication_authority':False}
    custody={'status':'PASS_FINITE_REFERENCE_CUSTODY','namespaces':protected,'qualified_core_reference':{**core_ref,'actual':core_pin},'qualified_core_statement':refs['qualified_core_scope'],'scientific_authority_actual':authority_pin,'source_historical_false_null_states_unchanged':True,'old_TSP_52_files_4_directories_unchanged':True,'global_cache_baseline_claim':False,'scientific_programs_or_native_helpers_executed':[],'new_foreign_scientific_bodies_copied':False}
    return {'model':model,'content':content,'custody':custody,'helpers':helper_reads['current_helpers']}

if __name__=='__main__':
    before=inventory(OWN)
    result=audit()
    require(inventory(OWN)==before,'read-only guard changed owned bytes or extent')
    print(json.dumps({'status':'PASS_READ_ONLY_EDITORIAL_GUARD','writes':0,'before_after_owned_bytes_and_extent_identical':True,'MAIN':result['content']['whole_actual_MAIN'],'protected_namespaces':len(result['custody']['namespaces'])},separators=(',',':')))
