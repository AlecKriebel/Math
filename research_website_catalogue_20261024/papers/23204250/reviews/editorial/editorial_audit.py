"""Finite editorial content/custody closure. Reads data; writes only this folder.
No scientific program, imported project module, network, Git, or site operation.
"""
from pathlib import Path
from html.parser import HTMLParser
import hashlib
import json
import re
import zipfile
from datetime import datetime, timezone

OWN = Path(__file__).resolve().parent
P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
PAPER = P / 'papers/23204250'
SOURCE = PAPER / 'sources'
TERMINALS = ['OWNED_MANIFEST.json', 'FINAL.json']

def need(condition, message):
    if not condition:
        raise RuntimeError(message)

def pin_bytes(data):
    return {'bytes': len(data), 'SHA256': hashlib.sha256(data).hexdigest()}

def pin(path):
    need(path.is_file() and not path.is_symlink(), 'not regular: ' + str(path))
    return pin_bytes(path.read_bytes())

def same(path, digest, size=None):
    got = pin(path)
    need(got['SHA256'] == digest and (size is None or got['bytes'] == size), 'pin mismatch: ' + str(path))
    return got

def read_json(path):
    return json.loads(path.read_text())

def write_json(name, value):
    target = OWN / name
    need(target.parent == OWN and not target.is_symlink(), 'write scope')
    target.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

def inventory(base):
    files, dirs = {}, []
    for item in sorted(base.rglob('*')):
        need(not item.is_symlink(), 'symlink: ' + str(item))
        relative = item.relative_to(base).as_posix()
        if item.is_dir():
            dirs.append(relative)
        elif item.is_file():
            files[relative] = pin(item)
        else:
            need(False, 'nonregular: ' + str(item))
    return files, dirs

def protected(base, manifest_name, manifest_hash, terminal_pins, counts):
    same(base / manifest_name, manifest_hash)
    manifest = read_json(base / manifest_name)
    exclusions = next(manifest[k] for k in ['excluded_terminal_files', 'exact_root_terminal_controls', 'exact_root_terminal_exclusions'] if k in manifest)
    need(exclusions == list(terminal_pins), 'terminal list/order: ' + str(base))
    expected = manifest.get('payloads')
    if expected is None:
        rows = manifest['files']
        expected = {row['path']: {'bytes': row['bytes'], 'SHA256': row['SHA256']} for row in rows}
        need(len(expected) == len(rows), 'duplicate manifest paths')
    actual, dirs = inventory(base)
    need(set(actual) == set(expected) | set(terminal_pins), 'finite file extent: ' + str(base))
    need(dirs == manifest['directories'], 'finite directory extent: ' + str(base))
    need((len(actual), len(dirs)) == counts, 'namespace counts: ' + str(base))
    for name, meta in expected.items():
        need(actual[name] == meta, 'protected payload: ' + str(base / name))
    for name, digest in terminal_pins.items():
        need(actual[name]['SHA256'] == digest, 'protected terminal: ' + str(base / name))
    return {'namespace': base.relative_to(P).as_posix(), 'files':len(actual), 'directories':len(dirs), 'manifest':actual[manifest_name], 'exact_terminal_pins':{name:actual[name] for name in terminal_pins}, 'whole_finite_namespace_verified':True}

class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.meta, self.links, self.ids, self.text = {}, [], [], {}
        self.capture, self.depth = None, 0
        self.jsonld, self.in_jsonld = '', False
        self.iframe, self.canonical, self.base = [], [], []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if self.capture:
            self.depth += 1
        elif a.get('id') in ['original-abstract', 'record-description']:
            self.capture, self.depth = a['id'], 1
            self.text[self.capture] = ''
        if 'id' in a:
            self.ids.append(a['id'])
        if tag == 'meta':
            key = a.get('name', a.get('property'))
            need(key not in self.meta, 'duplicate metadata')
            self.meta[key] = a.get('content')
        if tag == 'a':
            self.links.append({'href':a.get('href'), 'download':'download' in a})
        if tag == 'iframe':
            self.iframe.append(a)
        if tag == 'link' and a.get('rel') == 'canonical':
            self.canonical.append(a)
        if tag == 'base':
            self.base.append(a)
        if tag == 'script' and a.get('type') == 'application/ld+json':
            self.in_jsonld = True
    def handle_endtag(self, tag):
        if self.capture:
            self.depth -= 1
            if self.depth == 0:
                self.capture = None
        if tag == 'script':
            self.in_jsonld = False
    def handle_data(self, data):
        if self.capture:
            self.text[self.capture] += data
        if self.in_jsonld:
            self.jsonld += data

def norm(text):
    return ' '.join(text.split())

def run():
    now = datetime.now(timezone.utc).isoformat()
    same(OWN/'INITIAL.md','d62a68b3a7dfcf0d72a490dd59a6e577c05f2b3e1c0fdeb01d566a39fa2f7333',8731)
    same(OWN/'INITIAL_SEAL.json','5e5cb9b06981f3f3606693e38a3fcd41512a8a85597fe4c54c0cba02cbc5816a')
    authority_pin = same(P/'verification/root-clearance-23204250-20261115.json','b8b89c874818ca9b6e8568e53745b1ce3384788e4aade73f7eead426d0d61852',6319)
    same(PAPER/'reviews/root/ROOT_REVIEW_20261115.md','97cb0138a591b0a7eb6ef1aac14446cd6ca577cc27368940ce390f2a8e75ad32',5846)
    custody = [
        protected(SOURCE,'SOURCE_READY_MANIFEST.json','1aa69507121968210f03e87725249a90b41f2c96c05e1ca4fcc86014386fc7d6',{'SOURCE_READY_CLOSURE.json':'7f59e0c1672d530a00239e8f4e678076196d8abc55b1169223c7ee7e2f408433','SOURCE_READY_MANIFEST.json':'1aa69507121968210f03e87725249a90b41f2c96c05e1ca4fcc86014386fc7d6','SOURCE_READY_SEAL.json':'94bd3bbf71c9fd618b6bf12616120aace2a6d3fe04707d6f73bb1bd787dd8ecf'},(104,13)),
        protected(PAPER/'reviews/scope','OWNED_MANIFEST.json','9f8b418055ed2c47dafa5c5036d2897c07304e760c86352d7b3bef0195fe58bf',{'CLOSURE.json':'5a63b1a5922558ab96d62b21a8c881cb775fd2be40d1d764e2b2ad57f82595c0','FINAL_SEAL.json':'c499db8a573a91c899ef5eafb6e75e228995635f7db9c208c780989433c60531','OWNED_MANIFEST.json':'9f8b418055ed2c47dafa5c5036d2897c07304e760c86352d7b3bef0195fe58bf'},(345,20)),
        protected(PAPER/'reviews/adversarial','MANIFEST.json','7070e14f4620aa8e70821e3c000f35762dc1e82be7181e413cc90c4a0d71f6ff',{'FINAL_SEAL.json':'d81c64ab39f7b86e706feeb79bb8fb35a1b4f192edc34363a9510ca003aa2030','MANIFEST.json':'7070e14f4620aa8e70821e3c000f35762dc1e82be7181e413cc90c4a0d71f6ff'},(348,6)),
        protected(PAPER/'reviews/root','ROOT_MANIFEST_20261115.json','741a490da85b0f2cf8c2a00504509e624f445e6d48547dcda7ec161d82264bec',{'ROOT_FINAL_SEAL_20261115.json':'91faa753268ac78b5e003c3a05079905b340637b37fd4c4efe8b8e39de05a5c6','ROOT_MANIFEST_20261115.json':'741a490da85b0f2cf8c2a00504509e624f445e6d48547dcda7ec161d82264bec'},(23,2)),
    ]
    core_path = PAPER/'reviews/root/ROOT_CORE_CUSTODY_20261115.json'
    core_pin = same(core_path,'8be3cf485930a27cd2d995c1e51d31c5ca58072711e6884fd4b0642b2534bae3',3190)
    core = read_json(core_path)
    need(len(core['files']) == 18, 'qualified core count')
    for row in core['files']:
        same(P/row['path'],row['SHA256'],row['bytes'])
    same(SOURCE/'record.response.body','dc1a60a1b2539ce3a2ec5a4b07a5f76325f5919f4ba2d28c480c92bffccd908a',6804)
    same(SOURCE/'files.response.body','26602b20d3e02b191f0f35be4f80c2b80968b8c68fe8718ebc1fa21d62c5ed89',2698)
    record, native_files = read_json(SOURCE/'record.response.body'), read_json(SOURCE/'files.response.body')
    need('version' not in record['metadata'], 'native version absence')
    names = ['paper.pdf','tsp-verification.zip','tsp-source.zip']
    need([row['key'] for row in record['files']] == names, 'native record order')
    need([row['key'] for row in native_files['entries']] == names, 'native entry order')
    assets = []
    zip_payloads = 0
    for row in record['files']:
        name = row['key']
        src, local = SOURCE/'assets'/name, OWN/'preview'/name
        need(pin(src) == pin(local) and pin(src)['bytes'] == row['size'], 'native unchanged: '+name)
        need(hashlib.md5(local.read_bytes()).hexdigest() == row['checksum'].split(':')[1], 'native checksum: '+name)
        if name.endswith('.zip'):
            with zipfile.ZipFile(local) as archive:
                need(archive.testzip() is None, 'ZIP CRC')
                zip_payloads += sum(not member.is_dir() for member in archive.infolist())
        assets.append({'name':name, **pin(local), 'original_native_file_object':row})
    need(zip_payloads == 35, 'ZIP payload occurrence count')
    tex_path = SOURCE/'published-source/asset-003/main.tex'
    same(tex_path,'97917390b62c13412f4e5734c3e64e654033f5ca4b8ef05d683b9067ea7e17ea',18972)
    abstract_raw = re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}',tex_path.read_text(),re.S).group(1)
    abstract_plain = abstract_raw.replace('$N$','N').replace('$2^{\\Theta(N)}$','2^Theta(N)').replace('$3n$','3n').replace('$2n$','2n')
    abstract_plain = norm(abstract_plain)
    html_path = OWN/'preview/index.html'
    html = html_path.read_text()
    parsed = Page()
    parsed.feed(html)
    need(len(parsed.ids) == len(set(parsed.ids)) and parsed.ids.count('main') == 1, 'semantic unique main/ids')
    need(norm(parsed.text['original-abstract']) == abstract_plain.replace('2^Theta(N)','2Θ(N)'), 'complete manuscript abstract')
    need(parsed.text['record-description'] == record['metadata']['description'], 'complete native description')
    need(not parsed.canonical and not parsed.base, 'private URL authority')
    need(parsed.meta['robots'] == 'noindex,nofollow,noarchive', 'private noindex')
    need(parsed.meta['citation_publication_date'] == '2026/10/06' and parsed.meta['citation_doi'] == record['doi'], 'citation date/DOI')
    need(parsed.meta['citation_title'] == record['metadata']['title'], 'citation title')
    need(parsed.meta['citation_author_orcid'] == 'https://orcid.org/0009-0001-9320-500X', 'ORCID')
    ld = json.loads(parsed.jsonld)
    need(ld['datePublished'] == '2026-10-06' and ld['abstract'] == abstract_plain, 'JSON-LD abstract/date')
    need('url' not in ld and 'version' not in ld, 'no invented URL/version')
    need(all('license' not in entry for entry in ld['encoding']), 'no blanket mixed ZIP license')
    native_links = [row for row in parsed.links if row['href'] in names]
    need(native_links == [{'href':'paper.pdf','download':False},{'href':'paper.pdf','download':True},{'href':'tsp-verification.zip','download':True},{'href':'tsp-source.zip','download':True}], 'four native controls/order')
    originals = [row['links']['self'] for row in record['files']]
    need([row['href'] for row in parsed.links if row['href'] in originals] == originals, 'original Zenodo links/order')
    need(len(parsed.iframe) == 1 and parsed.iframe[0]['src'] == 'paper.pdf#view=FitH' and bool(parsed.iframe[0]['title']), 'titled local PDF embed')
    need({'href':'citation.bib','download':True} in parsed.links, 'BibTeX link')
    bib = (OWN/'preview/citation.bib').read_text()
    need(record['doi'] in bib and record['metadata']['title'] in bib and '2026-10-06' in bib and 'version =' not in bib, 'BibTeX identity')
    main_match, head_match = re.search(r'<main id="main">.*?</main>',html,re.S), re.search(r'<head>.*?</head>',html,re.S)
    need(main_match is not None and head_match is not None and html.count('<main') == 1, 'whole actual MAIN/head')
    main_pin, head_pin = pin_bytes(main_match.group().encode()), pin_bytes(head_match.group().encode())
    render = read_json(OWN/'RENDER_RECEIPT.json')
    need(render['status'] == 'PASS_LOCAL_HEADLESS_LAYOUT' and render['blocked_external_requests'] == [] and render['page_errors'] == [], 'render result')
    need([row['width'] for row in render['layouts']] == [1100,390], 'layout widths')
    need(all(row['audit']['scrollWidth'] == row['width'] and row['audit']['overflowElements'] == [] and row['skip_link_first_keyboard_focus'] for row in render['layouts']), 'layout/keyboard checks')
    need(not (OWN/'.render-profile').exists() and not (OWN/'.render-tmp').exists(), 'temporary browser extent removed')
    reads = read_json(OWN/'HELPER_READS.json')
    for row in reads['current_helpers']:
        need(row['full_current_body_personally_read_before_execution'], 'helper reading ledger')
        same(OWN/row['path'],row['SHA256'],row['bytes'])
    execution = read_json(OWN/'EXECUTION_RESULTS.json')
    need([row['exit_code'] for row in execution['render_runs']] == [1,1,1,0,0], 'literal execution sequence')
    need((OWN/'render.stderr').read_bytes() == b'' and (OWN/'render.stdout').read_text() == 'PASS_LOCAL_HEADLESS_LAYOUT desktop=1100 mobile=390 horizontal_overflow=0 external_requests=0\n', 'actual current render streams')
    model = {'schema':'private_tsp_editorial_page_v1','record_id':23204250,'sheet_row':139,'native_metadata_original':record['metadata'],'native_record_created_original':record['created'],'native_record_file_objects_original':record['files'],'native_files_entries_original':native_files['entries'],'native_version_field_present':False,'native_version_original':None,'printed_date':'2026-10-06','printed_version':None,'manuscript_abstract':abstract_plain,'native_record_description':record['metadata']['description'],'proposed_slug':'exact-semidefinite-tsp','canonical_url':None,'base_url':None,'production_url':None,'AA':None,'follow_up':None,'publication_authority':False,'private_preview':True,'full_original_scientific_claim_retained':True,'scientific_authority_reference':authority_pin,'rights':{'new_prose_documentation':'CC BY 4.0','new_code':'MIT','third_party_rights_retained':True,'blanket_mixed_ZIP_license':False},'whole_actual_MAIN':main_pin,'whole_head':head_pin,'assets':assets}
    write_json('PAGE_MODEL.json',model)
    write_json('CONTENT_RECEIPT.json',{'UTC':now,'status':'PASS_COMPLETE_ACTUAL_COPY_AND_METADATA','whole_page':pin(html_path),'whole_actual_MAIN':{**main_pin,'start_byte':len(html[:main_match.start()].encode()),'end_byte_exclusive':len(html[:main_match.end()].encode())},'whole_head':head_pin,'BibTeX':pin(OWN/'preview/citation.bib'),'CSS':pin(OWN/'preview/research.css'),'four_native_controls':native_links,'original_Zenodo_links':originals,'native_assets':assets,'complete_abstract_and_distinct_description_verified':True,'all_native_order_literal_objects_preserved_in_model':True,'no_version_invented':True,'native_ZIP_regular_payload_occurrences_CRC_checked':zip_payloads,'review_limitations_retained':True,'publication_authority':False})
    write_json('CUSTODY_RECEIPT.json',{'UTC':now,'protected_namespaces':custody,'qualified_core_reference':core_pin,'qualified_core_statement':core['qualification'],'qualified_core_files_verified':18,'global_cache_baseline_claim':False,'source_historical_unread_false_null_fields_untouched':True,'native_scientific_programs_executed':[],'protected_or_website_Git_Sheet_network_deploy_redirect_contact_writes':False})
    for name in TERMINALS:
        need((OWN/name).is_file() and not (OWN/name).is_symlink(), 'terminal must already exist')
    actual, dirs = inventory(OWN)
    payloads = {name:meta for name,meta in actual.items() if name not in TERMINALS}
    write_json('OWNED_MANIFEST.json',{'UTC':now,'owned_root':str(OWN),'files':[{'path':name,**meta} for name,meta in payloads.items()],'directories':dirs,'exact_existing_root_terminal_controls':TERMINALS,'subtree_basename_or_future_exclusions':[],'ignored_private_assets_and_rasters_included':True})
    write_json('FINAL.json',{'UTC':now,'status':'PRIVATE_EDITORIAL_CANDIDATE_FROZEN','record_id':23204250,'sheet_row':139,'manifest':pin(OWN/'OWNED_MANIFEST.json'),'payload_files':len(payloads),'complete_owned_files':len(payloads)+len(TERMINALS),'complete_directories':len(dirs),'exact_existing_root_terminal_controls':TERMINALS,'no_future_subtree_or_basename_exclusions':True,'whole_actual_MAIN':main_pin,'whole_page':pin(html_path),'whole_head':head_pin,'model':pin(OWN/'PAGE_MODEL.json'),'BibTeX':pin(OWN/'preview/citation.bib'),'helpers':reads['current_helpers'],'current_actual_render_exit_code':0,'seal_invocation_exit_code_reported_externally':True,'protected_finite_namespaces_verified':True,'assigned_editorial_completion_percent':100,'research_goal_completion_claim':False,'canonical_url':None,'base_url':None,'AA':None,'follow_up':None,'publication_authority':False,'fact_review_pending_root_handoff':True,'immutable_after_seal':True})
    print(json.dumps({'status':'PRIVATE_EDITORIAL_CANDIDATE_FROZEN','FINAL':pin(OWN/'FINAL.json'),'whole_actual_MAIN':main_pin,'files':len(payloads)+2,'directories':len(dirs)},separators=(',',':')))

if __name__ == '__main__':
    run()
