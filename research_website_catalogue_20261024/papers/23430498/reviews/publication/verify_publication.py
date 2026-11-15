#!/usr/bin/env python3
"""Read-only editorial/source contract and targeted in-memory controls.

No renderer, source checker, browser, service, network, deployment or file
mutation is invoked. Default checks the terminal seal; --preseal omits it.
"""
from pathlib import Path
from hashlib import sha256
from datetime import datetime,timezone
from html.parser import HTMLParser
from copy import deepcopy
import json
import re
import sys
import zipfile

P=Path(__file__).resolve().parent
B=P.parents[1]
CAT=B.parents[1]
AUTH=CAT/'verification/root-clearance-23430498-20261115.json'
AUTH_SHA='9791b6178d1a0dc8bd9b32b5f0f56f1812f72e5d0dc1fafc03e806cdc80d8d2d'
READY_SHA='1f728d52dd3bb791833a837fb3bae7eab1b3a37ce7ecd9c4655b94f4d693cf46'
TERMINAL={'MANIFEST.json','VALIDATION.json','SEAL.json'}
GATES=['production_integration_authorized','publication_clearance','ready_to_publish',
 'rendered_copy_verified','local_http_verified','deployed','live_verified',
 'browser_verified','native_verified','canonical_verified']
NULLS=['canonical_url','native_sheet_aa_url','AA']


def need(ok,label):
    if not ok:raise ValueError(label)


def h(body):return sha256(body).hexdigest()


def read(path):return json.loads(path.read_bytes())


def abstract_text(tex):
    text=tex.replace(r'\operatorname{span}_{\Q}\{1,\ell,\ell^2\}', 'span_ℚ{1, ℓ, ℓ²}')
    text=text.replace(r'k\geq2','k ≥ 2').replace(r'0\leq n\leq2','0 ≤ n ≤ 2')
    return ' '.join(text.replace('$','').replace('--','–').split())


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.meta={};self.links=[];self.iframes=[];self.scripts=[];self.h1=0
        self.runtime_scripts=[];self.data=[];self.script=False;self.current=''
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='meta':self.meta[a.get('name',a.get('property',''))]=a.get('content')
        if tag=='link':self.links.append(a)
        if tag=='iframe':self.iframes.append(a)
        if tag=='h1':self.h1+=1
        if tag=='script':
            if a.get('src'):self.runtime_scripts.append(a['src'])
            self.script=True;self.current=''
    def handle_data(self,text):
        if self.script:self.current+=text
        else:self.data.append(text)
    def handle_endtag(self,tag):
        if tag=='script':self.scripts.append(self.current);self.script=False


def model(config,promotion,ready,authority,abstract,verdicts,native,transport):
    need(config['title']==native['record']['metadata']['title'],'native-title')
    need(config['publication_date']=='2026-10-13' and config['version']=='1.0','native-date-version')
    need(config['abstract']==abstract and config['abstract_is_original'] is True,'original-abstract')
    definition=' '.join(config['definitions'])
    need(all(x in definition for x in ['smooth, ordered and labelled','No strand framing',
      'height monotonicity','ℚ-valued','both self-crossings and mixed crossings',
      'actual three-dimensional exterior group','abstractly','No preferred-meridian-basis',
      'entire algebra of finite polynomials','repeated indices','arbitrary lengths','cancellations']),
      'complete-category-and-Milnor-algebra')
    result=config['result'];need(len(result)==3,'three-theorem-components')
    need(all(x in result[0] for x in ['recalled filtered Habegger–Masbaum',
      '𝓜₂(2) = span_ℚ{1, ℓ, ℓ²}','a₁ ∉ 𝓜₂(2) + 𝓝₂(2)','(k,n) = (2,2)']),
      'theorem-part1')
    need(all(x in result[1] for x in ['every k ≥ 2','every 0 ≤ n ≤ 2','𝓝ₙ(k) = 0']),
      'theorem-part2')
    need(all(x in result[2] for x in ['There exists a nonzero rational invariant',
      '𝓝₇(2)','exact ordinary order seven','every n ≥ 7','same invariant']),
      'theorem-part3')
    limits=' '.join(config['limitations'])
    need(all(x in limits for x in ['existential and noncanonical','named nonsingular',
      'diagram-weight calculation is not such a link evaluation','orders three through six',
      'least positive kernel order','higher-strand higher-order','larger order bounds',
      'disk-separated insertion','Arbitrary stacking or deletion','priority','Morimoto','Li',
      'No worldwide firstness or current worldwide openness']), 'scope-and-priority-limits')
    credit=' '.join(config['background'])
    need(all(x in credit for x in ['Stanford','Habegger–Masbaum','Casson','Meilhan',
      'Meilhan–Yasuhara','Nogueira','Kauffman–Lambropoulou','Alvarez–Labastida',
      'Willerton','Bleiler–Moriah','Rubinstein–Scharlemann','Bruno–Mecchia','Hatcher',
      'Duzhin–Karev','Bar-Natan']), 'positive-classical-credit')
    need(config['follow_up'] is None and promotion['follow_up'] is None,'default-null-followup')
    need(config['license']==config['code_license']=='CC BY 4.0' and
         config['license_url']=='https://creativecommons.org/licenses/by/4.0/', 'actual-CCBY-license')
    need(all(x in config['ai_disclosure'] for x in ['Extensive AI','unrefereed',
      'not human peer review','formal proof certification']) and
      promotion['human_peer_review'] is False and promotion['formal_certification'] is False,
      'AI-unrefereed-no-human-formal')
    need('contributions actually made' in config['collaboration'],'substantive-collaboration')
    binding=config['source_binding']
    need(binding['whole_original_source_ready']==ready and promotion['whole_original_source_ready']==ready,
         'whole-native-SOURCE_READY')
    need(binding['record_created_utc']=='2026-10-17T04:50:39.560366+00:00' and
         binding['zenodo_publication_date']=='2026-10-13','declared-created-distinction')
    for key,label in [('record','whole_native_record'),('latest','whole_native_latest_record'),
                      ('versions','whole_native_versions'),('files','whole_native_files_object')]:
        need(binding[label]==native[key],'whole-native-'+key)
    need(binding['whole_original_native_transport_objects']==transport and
         promotion['whole_original_native_transport_objects']==transport,'whole-raw-transport-schemas')
    need(binding['all_assets_in_original_order']==ready['all_native_assets_in_original_order'],
         'native-ZIP-then-PDF-order')
    need(binding['pdf_sha256']=='3a3f2a9e4bbd002217fca218f963957245b767e4a782e80b917031a3ef2d250f'
         and binding['supplement_sha256']=='55448cdcfb582cf2869f8b421f2141ed1d03d30a528e112df4935499280004d1'
         and binding['archive_payload_occurrences']==194 and config['pdf_pages']==13,
         'complete-original-reader-and-archive')
    need(promotion['whole_root_scientific_clearance_record']==authority and
         config['review_metadata']['scientific_status']==promotion['scientific_status']==authority['status'],
         'whole-literal-root-authority')
    for lane,value in verdicts.items():
        need(config['review_metadata']['whole_original_review_verdicts'][lane]['whole_literal_verdict']==value
             and promotion['reviews'][lane]['whole_literal_verdict']==value,
             'whole-custom-verdict-'+lane)
    need(all(config['review_metadata'][x] is False and promotion[x] is False for x in GATES),
         'all-publication-gates-false')
    need(all(config['review_metadata'][x] is None and promotion[x] is None for x in NULLS)
         and config['canonical_url'] is None and config['AA'] is None and
         config['seo']['canonical_url'] is None and config['seo']['open_graph_url'] is None,
         'canonical-AA-null')
    need(config['review_metadata']['root_copy_and_config_adoption_required'] is True and
         promotion['root_copy_and_config_adoption_required'] is True and
         promotion['source_repair'] is False and promotion['narrowed_replacement'] is False,
         'root-adoption-no-source-repair')


def main():
    args=sys.argv[1:];need(args in ([],['--preseal'],['--inputs-only']),'arguments')
    need(h(AUTH.read_bytes())==AUTH_SHA,'root-authority-hash')
    authority=read(AUTH);ready=read(B/'sources/SOURCE_READY.json')
    need(h((B/'sources/SOURCE_READY.json').read_bytes())==READY_SHA,'source-ready-hash')
    need(authority['source_ready']==ready and authority['editorial_preparation_authorized'] is True
         and authority['production_or_browser_authority'] is False and
         authority['actual_root_reading']['DKv5_actual_pages']==10,'literal-root-status-and-correction')
    protected=read(P/'PROTECTED_INPUTS.json')['files']
    for item in protected:
        q=Path(item['path']);need(q.is_file() and not q.is_symlink(),'protected-input-exists')
        need(q.stat().st_size==item['bytes'] and h(q.read_bytes())==item['SHA256'],'protected-input-unchanged')
    config=read(P/'publication.json');promotion=read(P/'promotion.json')
    native={'record':read(B/'sources/record-attempt2.body'),'latest':read(B/'sources/latest.raw.json'),
            'versions':read(B/'sources/versions.page-001.raw.json'),'files':read(B/'sources/files.raw.json')}
    transport=[{'filename':n,'whole_original_object':read(B/'sources'/n)} for n in ready['transport_files']]
    verdicts={lane:read(B/'reviews'/lane/'VERDICT.json') for lane in ['analytic','scope','adversarial']}
    tex=Path(ready['controlling_TeX']['path']).read_text()
    original=re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}',tex,re.S).group(1)
    need((P/'abstract-source.tex').read_text()==original,'whole-abstract-source')
    abstract=abstract_text(original)
    model(config,promotion,ready,authority,abstract,verdicts,native,transport)
    need(promotion['publication_sha256']==h((P/'publication.json').read_bytes()),'config-byte-binding')
    article=read(P/'article-config.json')
    need(article['publication_sha256']==h((P/'publication.json').read_bytes()) and
         article['promotion_sha256']==h((P/'promotion.json').read_bytes()) and
         article['canonical_url'] is None and article['AA'] is None and
         article['publication_authorized'] is False,'article-config-bindings')
    html_source=(P/'preview/index.html').read_text();page=Page();page.feed(html_source)
    need(page.h1==1 and len(page.iframes)==1 and page.runtime_scripts==[],'accessible-static-reader')
    need(abstract in page.data and abstract in (P/'PUBLIC_COPY.md').read_text(),'visible-full-original-abstract')
    need(page.meta['robots']=='noindex,nofollow' and not any(x.get('rel')=='canonical' for x in page.links)
         and 'og:url' not in page.meta,'private-preview-no-live-canonical')
    for key,value in read(P/'SCHOLARLY_METADATA.json')['citation_meta'].items():
        need(page.meta[key]==value,'exact-citation-meta')
    need(page.meta['citation_publication_date']=='2026/10/13' and page.meta['citation_version']=='1.0'
         and page.meta['citation_doi']=='10.5281/zenodo.23430498','citation-original-identity')
    schema=json.loads(page.scripts[0]);expected=read(P/'SCHOLARLY_METADATA.json')['scholarly_article']
    need(len(page.scripts)==1 and schema==expected and schema['abstract']==abstract
         and schema['datePublished']=='2026-10-13' and schema['version']=='1.0', 'scholarly-schema')
    need([x['encodingFormat'] for x in schema['encoding']]==['application/zip','application/pdf'],
         'schema-native-assets-order')
    need('background:#fff' in html_source and 'Arial,Helvetica,sans-serif' in html_source
         and 'max-width:780px' in html_source and '@media(max-width:600px)' in html_source,
         'simple-white-responsive-style')
    visible=' '.join(page.data)
    need(not any(x in visible for x in ['2026-11-15','2026-11-14','03:33','194-member','518 protected',
         'root clearance','adversarial115','twelve-family','nine pages','MIT License']),
         'public-copy-no-private-audit-narrative')
    for item in ready['all_native_assets_in_original_order']:
        q=P/'preview/assets'/item['original_api_file_object']['key']
        need(q.read_bytes()==Path(item['path']).read_bytes() and h(q.read_bytes())==item['SHA256'],
             'complete-byte-identical-native-asset')
    zip_path=P/'preview/assets'/config['supplement_filename']
    with zipfile.ZipFile(zip_path) as z:
        need(len(z.infolist())==194 and z.testzip() is None,'whole-194-member-archive-CRC')
    search=read(P/'PDF_SEARCHABILITY.json')
    need(search['page_count']==13 and len(search['per_page_text_characters'])==13
         and all(x>100 for x in search['per_page_text_characters']) and
         search['source_PDF_SHA256']==search['copied_PDF_SHA256']==config['source_binding']['pdf_sha256'],
         'searchable-complete-original-PDF')
    captures=read(P/'CDP_PREVIEW_RECEIPTS.json')
    need(len(captures['receipts'])==4,'final-private-preview-count')
    for rec in captures['receipts']:
        need(rec['explicit_device_metrics_override'] is True and rec['private_localhost_only'] is True and
             rec['production_or_native_verification'] is False and
             rec['HTML_SHA256']==h((P/'preview/index.html').read_bytes()) and
             h(Path(rec['screenshot']).read_bytes())==rec['screenshot_SHA256'] and
             rec['screenshot_bytes']>20000 and rec['metrics']['innerWidth']==rec['window'][0]
             and rec['metrics']['scrollWidth']<=rec['window'][0]
             and rec['metrics']['ready']=='complete','actual-private-preview-binding')
    execution=read(P/'CDP_EXECUTION_TOOL_RESULT.json')
    need(execution['exit_code']==0 and json.loads(execution['output'])['private_captures']==4,
         'actual-private-preview-execution')
    # Mutate only in-memory models and demand the intended semantic failure.
    controls=[('original-abstract',lambda c,p:c.__setitem__('abstract',c['abstract'][:100])),
      ('theorem-part2',lambda c,p:c['result'].__setitem__(1,'For k=2 only, N=0.')),
      ('theorem-part3',lambda c,p:c['result'].__setitem__(2,'There is a framed order-at-most-seven example.')),
      ('complete-category-and-Milnor-algebra',lambda c,p:c['definitions'].__setitem__(2,'Only short distinct-index Milnor invariants are used.')),
      ('scope-and-priority-limits',lambda c,p:c.__setitem__('limitations',['The least kernel order is seven.'])),
      ('actual-CCBY-license',lambda c,p:c.__setitem__('code_license','MIT')),
      ('default-null-followup',lambda c,p:c.__setitem__('follow_up','Classify missing orders3–6.')),
      ('all-publication-gates-false',lambda c,p:p.__setitem__('ready_to_publish',True)),
      ('canonical-AA-null',lambda c,p:p.__setitem__('canonical_url',c['proposed_canonical_url'])),
      ('whole-literal-root-authority',lambda c,p:c['review_metadata'].__setitem__('scientific_status','PASS')),
      ('whole-custom-verdict-adversarial',lambda c,p:c['review_metadata']['whole_original_review_verdicts']['adversarial']['whole_literal_verdict'].__setitem__('root_scientific_clearance',True)),
      ('whole-native-SOURCE_READY',lambda c,p:c['source_binding']['whole_original_source_ready']['all_native_assets_in_original_order'][0].__setitem__('sha256','normalized')),
      ('native-ZIP-then-PDF-order',lambda c,p:c['source_binding']['all_assets_in_original_order'].reverse()),
      ('declared-created-distinction',lambda c,p:c['source_binding'].__setitem__('record_created_utc','2026-10-13')),
      ('whole-raw-transport-schemas',lambda c,p:c['source_binding']['whole_original_native_transport_objects'].pop()),
      ('complete-original-reader-and-archive',lambda c,p:c.__setitem__('pdf_pages',12)),
      ('AI-unrefereed-no-human-formal',lambda c,p:p.__setitem__('human_peer_review',True))]
    rejected=[]
    for expected,change in controls:
        c,p=deepcopy(config),deepcopy(promotion);change(c,p)
        try:model(c,p,ready,authority,abstract,verdicts,native,transport)
        except ValueError as error:
            need(str(error)==expected,'negative control rejected for wrong reason: '+str(error))
            rejected.append(expected)
        else:raise ValueError('negative control escaped: '+expected)
    owned_count=None
    if args!=['--inputs-only']:
        manifest=read(P/'MANIFEST.json');names=set()
        for item in manifest['files']:
            q=P/item['path'];need(q.is_relative_to(P) and not q.is_symlink(),'owned-path')
            need(q.stat().st_size==item['bytes'] and h(q.read_bytes())==item['SHA256'],'owned-byte-identity')
            names.add(item['path'])
        actual={str(q.relative_to(P)) for q in P.rglob('*') if q.is_file()
                and str(q.relative_to(P)) not in TERMINAL and not q.is_relative_to(P/'preview/cache')}
        need(actual==names,'owned-manifest-membership');owned_count=len(names)
    if not args:
        seal=read(P/'SEAL.json')
        for name,key in [('MANIFEST.json','MANIFEST_SHA256'),('VALIDATION.json','VALIDATION_SHA256'),
          ('REPORT.md','REPORT_SHA256'),('VERDICT.json','VERDICT_SHA256'),
          ('publication.json','PUBLICATION_SHA256'),('promotion.json','PROMOTION_SHA256')]:
            need(h((P/name).read_bytes())==seal[key],'terminal-seal-binding')
        validation=read(P/'VALIDATION.json')
        need(validation['exit_code']==0 and validation['result']['verdict']=='PASS'
             and validation['verifier_SHA256']==h(Path(__file__).read_bytes()),'captured-read-only-validation')
    print(json.dumps({'UTC':datetime.now(timezone.utc).isoformat(),'verdict':'PASS',
      'mode':args[0] if args else 'terminal-read-only','protected_existing_files':len(protected),
      'PDF_pages':13,'whole_original_archive_payloads':194,'literal_whole_custom_verdicts':3,
      'negative_controls_rejected':rejected,'private_final_preview_images':4,
      'owned_manifest_payloads':owned_count,'production_browser_native_canonical_gates':False,
      'programs_replayed':[],'network_requests':[],'writes':[]},indent=2))


if __name__=='__main__':main()
