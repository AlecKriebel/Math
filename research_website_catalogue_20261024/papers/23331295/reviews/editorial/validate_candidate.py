"""Read-only editorial fidelity checks; standard library, no scientific code."""
from pathlib import Path
from html.parser import HTMLParser
import hashlib
import io
import json
import re
import zipfile


def need(value, message):
    if not value: raise ValueError(message)


def literal(value): return json.dumps(value, ensure_ascii=False, separators=(',', ':'), allow_nan=False)
def same(a, b): need(type(a) is type(b) and literal(a) == literal(b), 'whole typed/ordered object differs')


class Doc(HTMLParser):
    void = {'meta', 'link', 'br'}
    parents = {'html': {'root'}, 'head': {'html'}, 'body': {'html'}, 'meta': {'head'}, 'link': {'head'},
        'style': {'head'}, 'script': {'head'}, 'title': {'head'}, 'main': {'body'}, 'article': {'main'},
        'header': {'article'}, 'h1': {'header'}, 'section': {'article'}, 'h2': {'section'},
        'p': {'header', 'section'}, 'ul': {'section'}, 'li': {'ul'}, 'a': {'p', 'li'}, 'iframe': {'section'}, 'br': {'p'}}

    def __init__(self, text):
        super().__init__(convert_charrefs=True); self.root = {'tag': 'root', 'attrs': {}, 'children': []}
        self.stack = [self.root]; self.nodes = []; self.doctype = 0
        self.feed(text); self.close(); need(len(self.stack) == 1 and self.doctype == 1, 'complete balanced document')

    def handle_decl(self, text):
        need(text.lower() == 'doctype html' and len(self.stack) == 1, 'HTML doctype only'); self.doctype += 1

    def handle_comment(self, text): raise ValueError('unapproved document comment')
    def unknown_decl(self, text): raise ValueError('unknown declaration')

    def handle_starttag(self, tag, attrs):
        parent = self.stack[-1]; a = dict(attrs)
        need(len(a) == len(attrs) and tag in self.parents and parent['tag'] in self.parents[tag], 'closed visible HTML grammar')
        need(not any(k in {'hidden', 'inert', 'style', 'aria-hidden', 'srcdoc'} or k.startswith('on') for k in a), 'hiding/event attribute')
        node = {'tag': tag, 'attrs': a, 'children': [], 'parent': parent}; parent['children'].append(node); self.nodes.append(node)
        if tag not in self.void: self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        need(tag in self.void, 'selfclosing nonvoid element'); self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag):
        need(len(self.stack) > 1 and self.stack[-1]['tag'] == tag, 'explicit balanced close'); self.stack.pop()

    def handle_data(self, text):
        if self.stack[-1]['tag'] == 'iframe': need(not text.strip(), 'iframe raw text must be empty')
        self.stack[-1]['children'].append(text)


def text(node): return ''.join(c if isinstance(c, str) else text(c) for c in node['children'])
def nodes(doc, tag): return [n for n in doc.nodes if n['tag'] == tag]
def one(doc, tag):
    found = nodes(doc, tag); need(len(found) == 1, 'single ' + tag); return found[0]


def validate(root, pub, page, assets):
    root = Path(root); protocol = json.loads((root / 'SOURCE_PROTOCOL_BINDINGS.json').read_bytes())
    draft = json.loads((root / 'DRAFT_SECTIONS.json').read_bytes()); ready = protocol['whole_original_SOURCE_READY']['whole_literal_object']
    need(pub['title'] == ready['title'] and pub['doi'] == ready['DOI'], 'original identity')
    need(type(pub['version']) is str and pub['version'] == '1.0' and pub['printed_version'] is None and pub['printed_version_field_present'] is False, 'native1.0 versus absent printed version')
    need(pub['publication_date'] == '2026-10-12' and pub['native_record_created'] == ready['created'] and pub['native_record_updated'] == ready['updated'], 'original12Oct and distinct13Oct metadata')
    need(pub['canonical_url'] is None and pub['AA'] is None and pub['follow_up'] is None, 'private authority boundary')
    need(pub['license'] == pub['authored_package_license'] == 'CC BY 4.0' and pub['code_license'] is None, 'actual broad CC BY grant; no MIT default')
    need(pub['abstract'] == protocol['actual_source_manuscript_and_companion_read']['entire_original_abstract_rendered_plain'], 'complete original abstract')
    for key in draft: same(pub[key], draft[key])
    same(pub['source_binding']['whole_original_source_ready'], ready)
    same(pub['review_metadata']['whole_original_two_scientific_custom_verdicts'], protocol['whole_original_two_scientific_custom_verdicts'])
    same(pub['review_metadata']['root_scientific_authority'], protocol['whole_root_scientific_authority'])
    update = pub['review_metadata']['new_root_primary_access_update_separate_from_immutable_peer_limits']
    same(update, protocol['new_root_Stoimenow_finding_separate_from_immutable_peer_limits'])
    need(update['current_root_authenticates_exact_2010_definitions_theorem_and_context'] is True and update['root_new_all46page_or_predecessor_absence_certificate'] is False, 'exact updated root primary scope')
    need(set(assets) == {'nullstellensatz.tex', 'verification-package.zip', 'nullstellensatz.pdf', 'citation.bib'}, 'all3 native assets plus BibTeX')
    for a in ready['all_native_assets_in_original_order']:
        raw = assets[a['original_api_file_object']['key']]
        need(len(raw) == a['bytes'] and hashlib.sha256(raw).hexdigest() == a['SHA256'], 'whole native asset unchanged')
        need(hashlib.md5(raw).hexdigest() == a['original_api_file_object']['checksum'].split(':')[1], 'actual native MD5')
    need(assets['citation.bib'] == pub['prepared_bibtex'].encode(), 'whole prepared BibTeX')
    need(assets['nullstellensatz.tex'] == Path(ready['controlling_TeX']['extracted_path']).read_bytes(), 'standalone/control TeX equality')
    with zipfile.ZipFile(io.BytesIO(assets['verification-package.zip'])) as z:
        entries = [e for e in z.infolist() if not e.is_dir()]; need(len(entries) == 15, 'all15 original regular payloads')
        need(not any(e.filename.lower().endswith('.pdf') for e in entries), 'no invented embedded PDF')
        base = Path(ready['controlling_TeX']['extracted_path']).parent
        for entry in entries:
            need('..' not in Path(entry.filename).parts and not Path(entry.filename).is_absolute(), 'safe original archive path')
            need(z.read(entry) == (base / entry.filename).read_bytes(), 'whole native CRC/member bytes')
    html = page.decode(); d = Doc(html); main = one(d, 'main'); article = one(d, 'article')
    need(main['parent']['tag'] == 'body' and article['parent'] is main and not main['attrs'] and not article['attrs'], 'whole main/article visible')
    need(text(one(d, 'h1')) == pub['title'] and text(one(d, 'title')) == pub['seo']['title'], 'full titles')
    sections = {n['attrs'].get('id'): n for n in nodes(d, 'section')}
    need(len(sections) == 12 and list(sections) == ['abstract','plain-language','result','why-it-works','limitations','background','collaboration','status','read','cite','primary-background','rights'], 'entire full section order')
    expected = {'abstract': [pub['abstract']], 'plain-language':pub['plain_language'], 'result':pub['result'],
        'why-it-works':pub['why_it_works'], 'limitations':pub['limitations'], 'background':pub['background'],
        'collaboration':[pub['collaboration']], 'status':[pub['ai_disclosure']], 'cite':[pub['citation_text']],
        'rights':[pub['rights_notice'], 'Creative Commons Attribution 4.0 International']}
    for key, value in expected.items():
        paragraphs = [text(n) for n in sections[key]['children'] if isinstance(n,dict) and n['tag']=='p']
        need(paragraphs == value, 'complete paragraph fidelity: ' + key)
    need(pub['edition_note'] in text(one(d, 'header')) and 'Zenodo version 1.0' in text(one(d, 'header')), 'edition note/printed absence')
    metas = {n['attrs'].get('name', n['attrs'].get('charset')):n['attrs'].get('content') for n in nodes(d,'meta')}
    for k,v in {'robots':'noindex,nofollow','description':pub['description'],'citation_title':pub['title'],'citation_author':pub['author'],'citation_author_orcid':pub['orcid'],'citation_publication_date':'2026/10/12','citation_version':'1.0','citation_doi':pub['doi'],'citation_pdf_url':'assets/nullstellensatz.pdf'}.items(): need(metas.get(k)==v,'scholarly metadata: '+k)
    need(not nodes(d,'link'), 'no premature canonical or external style assignment')
    script = one(d,'script'); need(script['attrs']=={'type':'application/ld+json'},'inert JSON-LD only'); s=json.loads(text(script))
    for k,v in {'abstract':pub['abstract'],'datePublished':'2026-10-12','version':'1.0','license':pub['license_url'],'headline':pub['title']}.items(): need(s[k]==v,'whole scholarly identity: '+k)
    expected_enc=[{'@type':'MediaObject','encodingFormat':a['whole_original_native_files_entry']['mimetype'],'contentUrl':a['original_api_file_object']['links']['self']} for a in ready['all_native_assets_in_original_order']]
    same(s['encoding'],expected_enc)
    frame=one(d,'iframe');need(frame['attrs']=={'class':'paper-pdf','loading':'lazy','src':'assets/nullstellensatz.pdf#view=FitH','title':pub['title']+' — complete four-page PDF'},'complete unchanged4page reader')
    read_lists=[n for n in sections['read']['children'] if isinstance(n,dict) and n['tag']=='ul'];need(len(read_lists)==1,'native downloads list')
    native_links=[]
    for li in read_lists[0]['children']:
        if isinstance(li,dict): native_links.append(next(n['attrs']['href'] for n in li['children'] if isinstance(n,dict) and n['tag']=='a'))
    need(native_links==['assets/nullstellensatz.tex','assets/verification-package.zip','assets/nullstellensatz.pdf'],'actual TeX ZIP PDF download order')
    hrefs=[n['attrs'].get('href') for n in nodes(d,'a')]
    for a in ['nullstellensatz.tex','verification-package.zip','nullstellensatz.pdf','citation.bib']:
        need(any(n['attrs'].get('href')=='assets/'+a and 'download' in n['attrs'] for n in nodes(d,'a')),'direct original download '+a)
    need(pub['orcid'] in hrefs and 'https://doi.org/'+pub['doi'] in hrefs,'ORCID and DOI')
    style=text(one(d,'style'));need('font-family:Arial,Helvetica,sans-serif' in style and 'background:#fff' in style and 'color:#111' in style,'white Arial layout')
    need(not re.search(r'display\s*:\s*none|visibility\s*:\s*hidden|opacity\s*:\s*0|font-size\s*:\s*0',style,re.I),'no hiding CSS')
    visible=text(main)
    for private in ['SOURCE_READY','SHA256','8460','40-run','2026-11-15','403 responses','root review','peer verdict']:
        need(private not in visible,'no private audit narrative')
    return {'literal_custom_status':'COMPLETE_PRIVATE_EDITORIAL_COPY_NATIVE_ASSET_IDENTITY_AND_ACTUAL_ROOT_SCOPE_CONFIRMED','PDF_pages':4,'ZIP_regular_payloads':15,'native_order':['TeX','ZIP','PDF'],'original_abstract_complete':True,'printed_version':None,'native_version':'1.0','whole_custom_science_verdicts':2,'actual_transports':8,'source_programmes_executed':False,'publication_authority':False}


def load(root):
    root=Path(root);return json.loads((root/'publication.json').read_bytes()),(root/'candidate/index.html').read_bytes(),{p.name:p.read_bytes() for p in (root/'candidate/assets').iterdir() if p.is_file()}


if __name__=='__main__':
    root=Path(__file__).resolve().parent
    print(json.dumps(validate(root,*load(root)),indent=2))
