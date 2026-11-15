"""Exact127/128 custody/adapters. Importing this file performs no reads or writes."""
from pathlib import Path, PurePosixPath
import hashlib
import html
import json
import re
import xml.etree.ElementTree as ET

A = Path(__file__).resolve().parent
CAT = A.parent.parent
W = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
FACT = CAT / 'verification/lefschetz-link-editorial-fact-audit-sol-20261115'
IDS = ('23570763', '23331295')
SEALS = ('f9a6c973d657449db4087605189e0ac4a655a246fbf012b9c05a7dc60566187e',
         '307ac0b4005de084926d2a99ecd309854e544957f03a5c7620d999475c218d4d')
SCIENCE = ('56a6e20fcef53e11e3cd7ab2bba1ad6503d0720509983be7b60d5a19bd9dc33f',
           'a4dbd16bc3bd3bb81b674183f3c75f87d1234b5a0facb89320bb8f08a3b5ed25')
ADOPTIONS = ('2d0d6f6ee869787cb707995351cf39e2509dfa3d66a19d2111a8381cbe3ca175',
             '6bbd8861012b089a3b39376b4a1dc731509ecadff744f17e769c37576f5d8287')
FACT_CLOSURE = CAT/'verification/root-lefschetz-link-editorial-fact-audit-closure-20261115.json'
FACT_CLOSURE_SHA = 'd652464eb2a63233666699e69e0a21c68c10d12cdbaef1fc39686d4769ceb50c'
CONFIGS = ('config/publication.json', 'publication.json')
PROMOTIONS = ('config/promotion.json', 'promotion.json')
ASSET_NAMES = (('periodic-lefschetz-source-and-verification.zip','periodic-lefschetz.pdf'),
               ('nullstellensatz.tex','verification-package.zip','nullstellensatz.pdf'))
BASE_COUNTS = (605,90,91)
FINAL_COUNTS = (614,92,93)
FACT_SEAL = '196423f4a8f777c768c96962273b00eb19a7a200fb7cef9d0eb2076a6a80f988'
CSS = ('main p,main li,main td,main th{overflow-wrap:anywhere}'
       'main .math{white-space:pre-wrap;overflow-wrap:anywhere}'
       'main pre{white-space:pre-wrap;overflow-wrap:anywhere}'
       'main iframe{display:block;width:100%;height:80vh;min-height:500px;'
       'max-height:1000px;border:1px solid #ccc;box-sizing:border-box}')


def need(ok, why):
    if not ok:
        raise ValueError(why)


def sha(body):
    return hashlib.sha256(body).hexdigest()


def read(path):
    p = Path(path)
    need(p.is_file() and not p.is_symlink() and p.resolve()==p, 'regular nonsymlink input: '+str(p))
    return p.read_bytes()


def obj(path):
    return json.loads(read(path))


def same(a,b):
    if type(a) is not type(b): return False
    if isinstance(a,dict): return list(a)==list(b) and all(same(a[k],b[k]) for k in a)
    if isinstance(a,list): return len(a)==len(b) and all(same(x,y) for x,y in zip(a,b))
    return a==b


def names(root):
    root=Path(root)
    need(root.is_dir() and not root.is_symlink() and root.resolve()==root,'real namespace root')
    paths=list(root.rglob('*'))
    need(not any(p.is_symlink() for p in paths),'no namespace symlink')
    need(all(p.is_dir() or p.is_file() for p in paths),'only regular namespace entries')
    return sorted(p for p in paths if p.is_file()), sorted(p.relative_to(root).as_posix() for p in paths if p.is_dir())


def pinned(path,n,h):
    body=read(path)
    need(len(body)==n and sha(body)==h,'whole byte/hash pin: '+str(path))
    return body


def structured(text):
    matches=list(re.finditer(r'<script type="application/ld\+json">\s*(.*?)\s*</script>',text,re.S))
    need(len(matches)==1,'exactly one scholarly JSONLD object')
    return matches[0],json.loads(matches[0][1])


def main_block(text):
    matches=re.findall(r'<main(?: id="main")?>.*?</main>',text,re.S)
    need(len(matches)==text.count('<main')==text.count('</main>')==1,'one complete main')
    return matches[0]


def scholarly(value):
    if '@graph' in value:
        articles=[x for x in value['@graph'] if x.get('@type')=='ScholarlyArticle']
        need(len(articles)==1,'one actual127 article in its original graph')
        return articles[0]
    need(value.get('@type')=='ScholarlyArticle','actual128 scholarly object')
    return value


def guard_fact_and_owners():
    need(sha(read(FACT/'SEAL.json'))==FACT_SEAL,'exact sealed informed fact audit')
    fseal=obj(FACT/'SEAL.json'); fm=obj(FACT/'OWNED_MANIFEST.json')
    need(sha(read(FACT/'OWNED_MANIFEST.json'))==fseal['OWNED_MANIFEST_SHA256'],'whole fact audit manifest')
    for row in fm['files']: pinned(FACT/row['path'],row['bytes'],row['SHA256'])
    actual,_=names(FACT)
    need({p.relative_to(FACT).as_posix() for p in actual}=={r['path'] for r in fm['files']}|{'OWNED_MANIFEST.json','SEAL.json'},
         'complete fact audit namespace; exact root controls only')
    original=obj(FACT/'INPUT_MANIFEST.json')
    need(len(original['files'])==244,'all244 original fact-audit inputs')
    for row in original['files']: pinned(Path(row['path']),row['bytes'],row['SHA256'])
    counts=[]
    for ns in original['strict_namespaces']:
        root=Path(ns['root']); fs,ds=names(root)
        need([p.relative_to(root).as_posix() for p in fs]==sorted(ns['exact_relative_file_names']) and
             ds==ns['exact_relative_directory_names'],'strict complete source/editorial namespace')
        counts.append(len(fs))
    need(counts==[65,41,65,60],'exact source/editorial cardinalities, including nested terminal names')
    for rid,seal,science in zip(IDS,SEALS,SCIENCE):
        ed=CAT/'papers'/rid/'reviews/editorial'
        need(sha(read(ed/'SEAL.json'))==seal,'current literal editorial seal')
        need(sha(read(CAT/'verification'/('root-clearance-'+rid+'-20261115.json')))==science,'exact scientific authority')
    return original


def adopted_editorials():
    """Root has authorized source-only freezing; this function never reads W."""
    need(sha(read(FACT_CLOSURE))==FACT_CLOSURE_SHA,'actual root3383-check fact-audit closure')
    values=[]
    for rid,pin in zip(IDS,ADOPTIONS):
        path=CAT/'verification'/('root-editorial-'+rid+'-20261115.json')
        body=read(path);need(sha(body)==pin,'only new final root editorial receipt')
        value=json.loads(body)
        need(value['record_id']==rid and value['root_editorial_adopted'] is True and
             value['full_original_scope_and_copy_adopted'] is True and
             value['private_stage_preparation_authorized'] is True and
             value['production_installation_authorized'] is False and
             value['website_baseline_freeze_requires_separate_explicit_GO'] is True,
             'exact root editorial/private-stage versus website authority distinction')
        values.append(value)
    need(values[0]['future_127_ZIP_MediaObject_omit_blanket_encoding_license_preserve_visible_split_CCBY_MIT_rights'] is True,
         'root authorized127 mixed-ZIP encoding refinement')
    return values


def code_guard():
    m=obj(A/'CODE_MANIFEST.json')
    need(len(m['files'])==6,'exact six proposed helper bodies')
    for row in m['files']: pinned(A/row['path'],row['bytes'],row['SHA256'])
    return sha(read(A/'CODE_MANIFEST.json'))


def authorize(go_path,go_sha):
    """Must finish before any website read, listing, baseline capture or rendering."""
    go_path=Path(go_path)
    need(go_path.is_absolute() and go_path.is_relative_to(CAT/'verification'),'root GO lives in verification')
    raw=read(go_path); need(sha(raw)==go_sha,'explicit fresh root GO pin')
    g=json.loads(raw)
    need(g['schema']=='lefschetz-link-private-stage-root-GO-v1','specific two-paper root GO schema')
    need(g['explicit_new_website_GO'] is True and g['full_editorial_adoption_complete'] is True,'both root gates explicitly complete')
    need(g['stage_directory']==str(A) and g['website_root']==str(W),'exact assigned stage and website')
    need(g['writer_transcription_of_actual_root_GO'] is True and g['root_stage_code_adopted'] is False,
         'honest writer record of explicit root GO; no invented root code adoption')
    need(g['current_stage_code_manifest_SHA256']==code_guard(),'current exact fully read helper bodies')
    need(g['baseline_counts']==list(BASE_COUNTS) and g['virtual_counts']==list(FINAL_COUNTS),'fresh605/90/91 only, future614/92/93')
    need(g['private_freeze_and_render_only'] is True and g['production_installation_authorized'] is False,'private authority only')
    need(g['fact_audit_SEAL_SHA256']==FACT_SEAL,'root adoption names this informed fact audit')
    adoptions=g['editorial_adoptions']
    need([r['record_id'] for r in adoptions]==list(IDS),'two distinct exact editorial adoption receipts')
    for rid,seal,pin,row in zip(IDS,SEALS,ADOPTIONS,adoptions):
        need(row['owner_editorial_SEAL_SHA256']==seal and row['full_copy_and_configs_adopted'] is True,'explicit full owner adoption')
        p=CAT/'verification'/('root-editorial-'+rid+'-20261115.json')
        need(row['path']==str(p),'exact root editorial receipt path')
        body=read(p);need(sha(body)==row['SHA256']==pin,'whole immutable final root editorial receipt pin')
        authority=json.loads(body)
        need(authority['production_installation_authorized'] is False,'root editorial receipt grants no installation')
    fact=Path(g['root_fact_audit_adoption']['path'])
    need(fact.is_relative_to(CAT/'verification') and sha(read(fact))==g['root_fact_audit_adoption']['SHA256'],
         'exact separate root fact-audit adoption/closure receipt')
    receipt=Path(g['prior_installation_receipt']['path'])
    need(receipt.is_relative_to(CAT/'verification') and sha(read(receipt))==g['prior_installation_receipt']['SHA256'],
         'fresh prior triplet installation receipt')
    installed=json.loads(read(receipt))
    need(re.fullmatch(r'[0-9a-f]{40}',g['prior_installation_commit']) is not None,'exact installed commit identity')
    need(installed['commit']==g['prior_installation_commit'] and installed['counts']==list(BASE_COUNTS),
         'actual new PUBLICATION605/90/91 receipt, not a reused old baseline')
    prior=Path(g['prior_root_stage_adoption']['path'])
    need(sha(read(prior))==g['prior_root_stage_adoption']['SHA256']==
         'a6930706d0e71f94459d7048f6f2f6797abc3b304212b0a80498727b5d8670bf',
         'exact root adoption of installed preceding triplet')
    need(g['native_verified_published_count']==87 and g['baseline_index_count_is_native_verified_count'] is False,
         '90 index records do not claim90native-verified publications')
    need(re.fullmatch(r'\d{4}-\d{2}-\d{2}',g['build_date']) is not None,'explicit current build date')
    return g


def frozen_inputs():
    binding=obj(A/'AUTHORIZATION_BINDING.json')
    g=authorize(binding['root_GO_path'],binding['root_GO_SHA256'])
    need(same(binding['whole_original_root_GO'],g),'whole original explicit GO object retained')
    source=obj(A/'SOURCE_INPUTS.json'); website=obj(A/'WEBSITE_BASELINE.json')
    need(website['root_GO_SHA256']==binding['root_GO_SHA256'],'same specific GO throughout freeze')
    guard_fact_and_owners()
    by={}
    for row in source['files']+website['files']:
        body=pinned(A/row['blob'],row['bytes'],row['SHA256'])
        need(read(Path(row['path']))==body,'fresh original whole frozen input')
        by[row['path']]=body
    fs,ds=names(W/'public')
    need([str(p) for p in fs]==website['public_namespace'] and ds==website['public_directory_namespace'],
         'entire current website namespace matches fresh authorized freeze')
    need(website['baseline_counts']==list(BASE_COUNTS),'no inherited prior baseline')
    return g,source,website,by


def records(by):
    rows=[]
    for index,(rid,config_rel,promotion_rel) in enumerate(zip(IDS,CONFIGS,PROMOTIONS)):
        ed=CAT/'papers'/rid/'reviews/editorial';source=CAT/'papers'/rid/'sources'
        c=json.loads(by[str(ed/config_rel)]); pro=json.loads(by[str(ed/promotion_rel)])
        ready=json.loads(by[str(source/'SOURCE_READY.json')])
        original=by[str(ed/'candidate/index.html')].decode();main=main_block(original)
        need(main==by[str(ed/'PUBLIC_MAIN.html')].decode().strip(),'entire owner public main exactly retained')
        need(main.startswith('<main>'),'known exact missing-main-id owner form')
        main=main.replace('<main>','<main id="main">',1)
        for key in ['follow_up','canonical_url','AA','native_sheet_aa_url']:
            need(c[key] is None and pro[key] is None,'original null private config gates intact')
        for key in ['deployed','live_verified','browser_verified','native_verified','ready_to_publish','production_integration_authorized']:
            need(pro[key] is False,'original false future publication gates intact')
        need(same(c['source_binding']['whole_original_source_ready'],ready),'whole READY binding, all types/order/null/history')
        need(ready['printed_date'] is None and ready['printed_version'] is None and ready['mathematical_PDF_TeX_or_pixels_read'] is False,
             'source acquisition unread/history not rewritten')
        need(ready['whole_regular_payload_occurrences']==(18 if index==0 else 15) and ready['selected_actual_PDF']['pages']==4,'original full archive/PDF scope')
        need(len(ready['embedded_PDFs'])==(1 if index==0 else 0),'actual embedded PDF distinction')
        assets=ready['all_native_assets_in_original_order']
        need([q['original_api_file_object']['key'] for q in assets]==list(ASSET_NAMES[index]),'actual native order ZIP/PDF and TeX/ZIP/PDF')
        for q in assets:
            key=q['original_api_file_object']['key']
            need(by[q['path']]==by[str(ed/'candidate/assets'/key)],'whole original/native candidate download')
        _,graph=structured(original);article=scholarly(graph)
        need(article['abstract']==c['abstract'] and article['datePublished']==c['publication_date'] and article['version']==c['version'],
             'whole original abstract and scholarly identity')
        need(len(article['encoding'])==len(assets),'complete original encoding list')
        need([q['contentUrl'] for q in article['encoding']]==[q['original_api_file_object']['links']['self'] for q in assets],
             'native original scholarly encoding order')
        if index==0:
            need(c['code_license']=='MIT' and c['version']==c['printed_version']=='1.0.0' and c['publication_date']=='2026-10-22','actual127 version/rights')
            need(article['encoding'][0]['license']==['https://creativecommons.org/licenses/by/4.0/','https://opensource.org/license/mit/'],
                 'actual127 heterogeneous ZIP license instruments')
        else:
            need(c['code_license'] is None and c['printed_version'] is None and c['printed_version_field_present'] is False and
                 c['version']=='1.0' and c['publication_date']=='2026-10-12' and c['native_record_created'].startswith('2026-10-13'),
                 'actual128 broad CC BY/null code instrument and absent printed version/date distinction')
            authority=json.loads(by[str(CAT/'verification/root-clearance-23331295-20261115.json')])
            update=pro['new_root_primary_access_update_separate_from_immutable_peer_limits']
            need(same(update['whole_original_root_qualification'],authority['additional_Stoimenow_root_vs_peer_qualification']),
                 'exact new root2010 finding separate from immutable peer limits')
            need(update['root_new_all46page_or_predecessor_absence_certificate'] is False and update['immutable_peer_failed_access_objects_rewritten'] is False,
                 'no invented full2010/absence audit or rewritten peers')
        url='https://aleckriebel.com/research/'+c['slug']+'/'
        need(c['proposed_canonical_url']==url,'exact owner canonical proposal')
        rows.append({'rid':rid,'ed':ed,'config':c,'promotion':pro,'ready':ready,'assets':assets,'main':main,'article':article,'url':url})
    return rows


def dump(value):
    return json.dumps(value,ensure_ascii=False).replace('<','\\u003c')
