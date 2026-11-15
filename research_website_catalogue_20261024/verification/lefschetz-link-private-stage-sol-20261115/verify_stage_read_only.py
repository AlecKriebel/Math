"""Self-contained default offline custody; no project imports or rendering.

No subprocess, network, source/scientific execution, controls, or writes.
Before AUTHORIZATION_BINDING exists this never inspects any website path.
"""
from pathlib import Path
import hashlib
import html
import json
import re
import zipfile
import xml.etree.ElementTree as ET

A=Path(__file__).resolve().parent;CAT=A.parent.parent
W=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
FACT=CAT/'verification/lefschetz-link-editorial-fact-audit-sol-20261115'
IDS=('23570763','23331295')
ADOPT=('2d0d6f6ee869787cb707995351cf39e2509dfa3d66a19d2111a8381cbe3ca175',
       '6bbd8861012b089a3b39376b4a1dc731509ecadff744f17e769c37576f5d8287')
ASSETS=(('periodic-lefschetz-source-and-verification.zip','periodic-lefschetz.pdf'),
        ('nullstellensatz.tex','verification-package.zip','nullstellensatz.pdf'))
checks=0


def need(ok,why):
    global checks
    checks+=1
    if not ok:raise ValueError(why)


def sha(b):return hashlib.sha256(b).hexdigest()


def read(p):
    p=Path(p);need(p.is_file() and not p.is_symlink() and p.resolve()==p,'regular whole input')
    return p.read_bytes()


def obj(p):return json.loads(read(p))


def same(a,b):
    if type(a) is not type(b):return False
    if isinstance(a,dict):return list(a)==list(b) and all(same(a[k],b[k]) for k in a)
    if isinstance(a,list):return len(a)==len(b) and all(same(x,y) for x,y in zip(a,b))
    return a==b


def names(root):
    root=Path(root);need(root.is_dir() and not root.is_symlink() and root.resolve()==root,'real namespace root')
    paths=list(root.rglob('*'));need(not any(p.is_symlink() for p in paths),'no namespace symlinks')
    need(all(p.is_file() or p.is_dir() for p in paths),'only regular namespace entries')
    return sorted(str(p) for p in paths if p.is_file()),sorted(p.relative_to(root).as_posix() for p in paths if p.is_dir())


def pinned(p,n,h):
    b=read(p);need(len(b)==n and sha(b)==h,'whole input byte/hash pin');return b


def structured(text):
    found=list(re.finditer(r'<script type="application/ld\+json">\s*(.*?)\s*</script>',text,re.S))
    need(len(found)==1,'one exact JSONLD script');return found[0],json.loads(found[0][1])


def main_tree(text):
    found=re.findall(r'<main(?: id="main")?>.*?</main>',text,re.S)
    need(len(found)==text.count('<main')==text.count('</main>')==1,'one whole main tree');return found[0]


def article(value):
    if '@graph' in value:
        found=[q for q in value['@graph'] if q.get('@type')=='ScholarlyArticle'];need(len(found)==1,'one original scholarly article');return found[0]
    need(value['@type']=='ScholarlyArticle','actual128 original scholarly object');return value


def finish(phase,source_count,typed=0,extra=None):
    sealed=False;owned_count=None
    if (A/'FINAL_SEAL.json').exists():
        seal=obj(A/'FINAL_SEAL.json');owned=obj(A/'OWNED_MANIFEST.json')
        need(sha(read(A/'OWNED_MANIFEST.json'))==seal['owned_manifest_SHA256'],'owned manifest final seal')
        fs,ds=names(A)
        need({str(Path(p).relative_to(A)) for p in fs}=={r['path'] for r in owned['files']}|{'OWNED_MANIFEST.json','FINAL_SEAL.json'},
             'entire own namespace; exact root terminal exclusions only')
        need(ds==owned['exact_relative_directories'],'whole owned directory namespace')
        for r in owned['files']:pinned(A/r['path'],r['bytes'],r['SHA256'])
        sealed=True;owned_count=len(owned['files'])
    print(json.dumps({'phase':phase,'positive_custody_checks':checks,'frozen_source_files':source_count,
                      'whole_typed_ordered_objects':typed,'own_final_seal_checked':sealed,'owned_payloads':owned_count,
                      'project_imports':False,'renderer_or_fault_or_scientific_replay':False,
                      'network_subprocess_or_writes':False,**(extra or {})},indent=2))


def main():
    code=obj(A/'CODE_MANIFEST.json');need(len(code['files'])==6,'six complete current helper bodies')
    for r in code['files']:pinned(A/r['path'],r['bytes'],r['SHA256'])
    need('inputs/' in read(A/'.gitignore').decode().splitlines() and 'blobs/' in read(A/'.gitignore').decode().splitlines(),
         'whole raw input/blob directories ignored')
    need(sha(read(FACT/'SEAL.json'))=='196423f4a8f777c768c96962273b00eb19a7a200fb7cef9d0eb2076a6a80f988','exact sealed informed audit')
    fact_owned=obj(FACT/'OWNED_MANIFEST.json')
    need(sha(read(FACT/'OWNED_MANIFEST.json'))==obj(FACT/'SEAL.json')['OWNED_MANIFEST_SHA256'],'complete original fact manifest')
    fact_names,_=names(FACT)
    need({str(Path(p).relative_to(FACT)) for p in fact_names}=={r['path'] for r in fact_owned['files']}|{'OWNED_MANIFEST.json','SEAL.json'},
         'strict whole281-file fact-audit namespace')
    for r in fact_owned['files']:pinned(FACT/r['path'],r['bytes'],r['SHA256'])
    original=obj(FACT/'INPUT_MANIFEST.json');need(len(original['files'])==244,'all244 original inputs')
    for r in original['files']:pinned(Path(r['path']),r['bytes'],r['SHA256'])
    counts=[]
    for ns in original['strict_namespaces']:
        root=Path(ns['root']);fs,ds=names(root)
        need([str(Path(p).relative_to(root)) for p in fs]==sorted(ns['exact_relative_file_names']) and ds==ns['exact_relative_directory_names'],
             'complete source/editorial namespace including every nested terminal name')
        counts.append(len(fs))
    need(counts==[65,41,65,60],'actual complete namespace counts')
    for rid,h in zip(IDS,ADOPT):
        p=CAT/'verification'/('root-editorial-'+rid+'-20261115.json');need(sha(read(p))==h,'new final root editorial adoption only')
        r=obj(p);need(r['root_editorial_adopted'] is True and r['full_original_scope_and_copy_adopted'] is True and
                     r['private_stage_preparation_authorized'] is True and r['production_installation_authorized'] is False,
                     'private source preparation versus later installation authority')
    source_count=0;typed=0;frozen={}
    source=None
    if (A/'SOURCE_INPUTS.json').exists():
        source=obj(A/'SOURCE_INPUTS.json');source_count=len(source['files'])
        expected_source={r['path'] for r in original['files']}|set(fact_names)|{
            str(CAT/'verification'/('root-editorial-'+rid+'-20261115.json')) for rid in IDS}|{
            str(CAT/'verification/root-lefschetz-link-editorial-fact-audit-closure-20261115.json')}
        need(len(source['files'])==len(expected_source) and {r['path'] for r in source['files']}==expected_source,
             'whole exact528source/original/audit/adoption inputs, no duplicates or dropped originals')
        need(len(source['whole_original_root_adoptions'])==2,'both complete root adoption objects')
        for rid,value in zip(IDS,source['whole_original_root_adoptions']):
            need(same(value,obj(CAT/'verification'/('root-editorial-'+rid+'-20261115.json'))),
                 'whole literal root adoption including historical custom verdicts')
        for r in source['files']:
            b=pinned(A/r['blob'],r['bytes'],r['SHA256']);need(read(Path(r['path']))==b,'whole source frozen/original equality')
            frozen[r['path']]=b
            if Path(r['path']).suffix=='.json' or Path(r['path']).name in {'record.response.body','latest.response.body.redirect-01','versions-page001.response.body','files.response.body'}:
                need(same(json.loads(b),obj(r['path'])),'whole original scalar types/key/list order/null/history');typed+=1
    if not (A/'AUTHORIZATION_BINDING.json').exists():
        need(not (A/'WEBSITE_BASELINE.json').exists(),'no partial unbound website freeze')
        need(not (A/'candidate-a').exists() and not (A/'candidate-b').exists(),'no rendering before bound specific GO')
        finish('SOURCE_PREPARATION_ONLY_NO_WEBSITE_INSPECTION',source_count,typed,
               {'website_read_or_frozen_by_this_closure':False,'rendered_outputs':False});return
    # Every website read in this standalone verifier is after these explicit authorization guards.
    binding=obj(A/'AUTHORIZATION_BINDING.json');go_bytes=read(Path(binding['root_GO_path']))
    need(sha(go_bytes)==binding['root_GO_SHA256'],'exact new explicit GO transcription pin')
    go=json.loads(go_bytes)
    need(same(binding['whole_original_root_GO'],go),'whole original explicit GO object retained')
    need(go['schema']=='lefschetz-link-private-stage-root-GO-v1' and go['explicit_new_website_GO'] is True and
         go['writer_transcription_of_actual_root_GO'] is True and go['root_stage_code_adopted'] is False and
         go['current_stage_code_manifest_SHA256']==sha(read(A/'CODE_MANIFEST.json')) and
         go['baseline_counts']==[605,90,91] and go['virtual_counts']==[614,92,93] and
         go['production_installation_authorized'] is False,'specific honest private two-paper GO, not science/root-code adoption')
    need(go['native_verified_published_count']==87 and go['baseline_index_count_is_native_verified_count'] is False,
         'index90 is not native-verified90')
    need(go['stage_directory']==str(A) and go['website_root']==str(W) and go['full_editorial_adoption_complete'] is True and
         go['private_freeze_and_render_only'] is True,'exact private stage/site/full-editorial scope')
    receipt=Path(go['prior_installation_receipt']['path'])
    need(sha(read(receipt))==go['prior_installation_receipt']['SHA256'],'new prior installation receipt whole pin')
    installed=obj(receipt)
    need(installed['commit']==go['prior_installation_commit']=='27cd946786754d66b44cbb309dae76da238b133e' and
         installed['counts']==[605,90,91],'actual newly installed605/90/91; never old baseline')
    prior=Path(go['prior_root_stage_adoption']['path'])
    need(sha(read(prior))==go['prior_root_stage_adoption']['SHA256']==
         'a6930706d0e71f94459d7048f6f2f6797abc3b304212b0a80498727b5d8670bf','exact prior root stage authority')
    need(source is not None,'source freeze exists before website freeze')
    website=obj(A/'WEBSITE_BASELINE.json');need(website['root_GO_SHA256']==binding['root_GO_SHA256'],'same new GO throughout')
    expected_website=set(website['public_namespace'])|{
        str(W/'firebase.json'),str(W/'.firebaserc'),
        go['prior_installation_receipt']['path'],binding['root_GO_path'],
        go['root_fact_audit_adoption']['path'],go['prior_root_stage_adoption']['path']}
    need(len(website['public_namespace'])==len(set(website['public_namespace']))==605 and
         len(website['files'])==len(expected_website)==611 and
         {r['path'] for r in website['files']}==expected_website,
         'exact whole605public plus six required external baseline inputs')
    for r in website['files']:
        b=pinned(A/r['blob'],r['bytes'],r['SHA256']);need(read(Path(r['path']))==b,'all fresh website/config/receipt bytes unchanged')
        frozen[r['path']]=b
    fs,ds=names(W/'public')
    need(fs==sorted(website['public_namespace']) and ds==website['public_directory_namespace'] and len(fs)==605,'whole actual fresh605 namespace; compare common lexical order')
    if not (A/'candidate-a').exists() and not (A/'candidate-b').exists():
        finish('AUTHORIZED_FRESH_BASELINE_ONLY_RENDER_PENDING',source_count,typed,{'baseline_counts':[605,90,91]});return
    need((A/'candidate-a/public').is_dir() and (A/'candidate-b/public').is_dir(),'both actual paired candidates required')
    overlay=obj(A/'OVERLAY_MANIFEST.json')['files'];contract=obj(A/'STAGE_CONTRACT.json')
    need(len(overlay)==len({r['path'] for r in overlay})==11 and [r['path'] for r in overlay]==contract['overlay_paths'],'exact11overlaypaths')
    paired={}
    for r in overlay:
        left=pinned(A/'candidate-a/public'/r['path'],r['bytes'],r['SHA256'])
        need(left==read(A/'candidate-b/public'/r['path']),'whole actual normal/-O paired buffers');paired[r['path']]=left
    for name in ['candidate-a','candidate-b']:
        actual,_=names(A/name/'public')
        need(actual==sorted(str(A/name/'public'/r['path']) for r in overlay),'complete exact11 candidate namespace')
    ledger=obj(A/'EXECUTION_LEDGER.json');need(ledger['actual_tool_exits_recorded'] is True,'actual whole tool receipts')
    need([r['name'] for r in ledger['runs']]==['BUILD_NORMAL','BUILD_OPTIMIZED','CONTROLS_NORMAL','CONTROLS_OPTIMIZED'],
         'all four actual distinct renderer/control run records')
    for r,opt in zip(ledger['runs'],[0,1,0,1]):
        need(r['exit_code']==0 and read(A/r['stderr'])==b'','actual empty stderr/success exit')
        raw=read(A/r['stdout']);need(sha(raw)==r['stdout_SHA256'],'whole actual stdout pin')
        result=json.loads(raw);need(result['optimization_level']==opt,'actual separate normal and optimized modes')
        if r['name'].startswith('BUILD'):need(result['actual_all_eleven_buffers_written'] is True,'actual paired render/write commands')
        else:need(result['fault_count']==9 and all(q['rejected'] is True for q in result['new_memory_only_faults']),'nine new bounded editorial-loss controls')
    asset_count=0
    for idx,rid in enumerate(IDS):
        ed=CAT/'papers'/rid/'reviews/editorial';s=CAT/'papers'/rid/'sources'
        c=json.loads(frozen[str(ed/('config/publication.json' if idx==0 else 'publication.json'))])
        ready=json.loads(frozen[str(s/'SOURCE_READY.json')]);url='https://aleckriebel.com/research/'+c['slug']+'/'
        original=frozen[str(ed/'candidate/index.html')].decode();old_main=main_tree(original)
        expected_main=old_main.replace('<main>','<main id="main">',1)
        text=paired['research/'+c['slug']+'/index.html'].decode()
        need(main_tree(text)==expected_main,'whole exact adopted main, only initial main id added')
        need(text.count('<h2>Original abstract</h2>')==1 and html.escape(c['abstract']) in main_tree(text),'full visible original abstract')
        need('<link rel="canonical" href="'+url+'">' in text and '<meta name="robots" content="index,follow">' in text and 'noindex' not in text,
             'complete future canonical/indexfollow head in private output')
        for k,v in [('citation_title',c['title']),('citation_author',c['author']),('citation_author_orcid',c['orcid']),
                    ('citation_publication_date',c['publication_date'].replace('-','/')),('citation_version',c['version']),
                    ('citation_doi',c['doi']),('citation_pdf_url',url+'assets/'+c['pdf_filename'])]:
            need('<meta name="'+k+'" content="'+html.escape(v)+'">' in text,'complete accurate citation metadata')
        need(text.count('<style>')==1 and '<style>'+contract['nonhiding_supplemental_css']+'</style>' in text,'exact nonhiding stylesheet')
        _,graph=structured(text);page,new=graph['@graph'];_,old_graph=structured(original);old=article(old_graph)
        need(page['dateCreated']==page['dateModified']==go['build_date'] and new['datePublished']==c['publication_date'] and
             new['abstract']==c['abstract'] and new['version']==c['version'],'original scholarly identity versus webpage build date')
        for k,v in old.items():
            if k not in {'@id','url','mainEntityOfPage','inLanguage','isAccessibleForFree','encoding'}:
                need(k in new and same(v,new[k]),'every unchanged original scholarly field')
        assets=ready['all_native_assets_in_original_order']
        need([a['original_api_file_object']['key'] for a in assets]==list(ASSETS[idx]) and len(new['encoding'])==len(assets),'whole original asset order including128TeX')
        for a,enc in zip(assets,new['encoding']):
            key=a['original_api_file_object']['key'];body=paired['research/'+c['slug']+'/assets/'+key]
            need(body==frozen[a['path']]==frozen[str(ed/'candidate/assets'/key)],'whole original/candidate/rendered native asset')
            need(hashlib.md5(body).hexdigest()==a['original_api_file_object']['checksum'].split(':')[1],'native original MD5')
            need(enc['contentUrl']==url+'assets/'+key and enc['sameAs']==a['original_api_file_object']['links']['self'],'exact local/original encoding URLs')
            if idx==0 and key.endswith('.zip'):need('license' not in enc,'root authorized127 mixed ZIP no blanket encoding license')
            else:need(enc['license']=='https://creativecommons.org/licenses/by/4.0/','actual PDF or128 broad CC BY grant')
            if key.endswith('.zip'):
                with zipfile.ZipFile(Path(a['path'])) as z:
                    regular=[q for q in z.infolist() if not q.is_dir()]
                    need(len(regular)==(18 if idx==0 else 15),'whole original18/15 ZIP payload counts')
                    for q in regular:z.read(q)  # full decompression/CRC; no scientific interpretation or execution
                    pdfs=[q for q in regular if q.filename.endswith('.pdf')]
                    need(len(pdfs)==(1 if idx==0 else 0),'original embedded PDF distinction')
                    if pdfs:need(z.read(pdfs[0])==frozen[ready['selected_actual_PDF']['path']],'whole127 embedded PDF identity')
            asset_count+=1
        need(paired['research/'+c['slug']+'/assets/citation.bib']==frozen[str(ed/'candidate/assets/citation.bib')],'whole approved BibTeX unchanged')
        need(c['canonical_url'] is None and c['AA'] is None and c['follow_up'] is None,'original private null gates retained')
        if idx==1:need(c['printed_version'] is None and c['code_license'] is None,'actual128 absent printed version and separate code instrument')
    oldindex=frozen[str(W/'public/research/index.html')].decode();oldm,oldschema=structured(oldindex)
    index=paired['research/index.html'].decode();_,newschema=structured(index)
    need(same(oldschema['mainEntity']['itemListElement'],newschema['mainEntity']['itemListElement'][:90]),'all90prior typed ordered records')
    need(newschema['mainEntity']['numberOfItems']==len(newschema['mainEntity']['itemListElement'])==92,'actual92index records')
    insertion=contract['index_additions'];need(index.count(insertion)==1,'one exact visible pair addition')
    restored=index.replace(insertion,'',1);rm,_=structured(restored)
    need(restored[:rm.start(1)]+oldm[1]+restored[rm.end(1):]==oldindex,'all prior visible index/scaffold bytes retained')
    sitemap=paired['research/sitemap.xml'];addition=contract['sitemap_additions'].encode()
    need(sitemap.count(addition)==1 and sitemap.replace(addition,b'',1)==frozen[str(W/'public/research/sitemap.xml')],
         'all91 old whole sitemap nodes/raw bytes retained')
    need(len(ET.fromstring(sitemap))==93,'actual93 sitemap nodes')
    base={str(Path(p).relative_to(W/'public')) for p in website['public_namespace']}
    need(len(base|set(paired))==614 and len(base-set(paired))==603 and base&set(paired)=={'research/index.html','research/sitemap.xml'},
         'exact9new leaves/2aggregates;603unrelated public files unchanged')
    r=obj(A/'READY.json');need(r['production_install_authorized'] is False and r['canonical_url'] is None and r['AA'] is None and
                              r['native_Sheet_publication_verified'] is False and r['follow_up'] is None,'later production/native gates unassigned')
    finish('PRIVATE_PAIRED_OUTPUT_CUSTODY',source_count,typed,{'baseline_counts':[605,90,91],'virtual_counts':[614,92,93],
           'whole_paired_overlay_files':11,'whole_native_assets':asset_count,'prior_index_records_preserved':90,
           'prior_sitemap_nodes_preserved':91,'unrelated_public_files_unchanged':603,'native_verified_published_count':87})


if __name__=='__main__':main()
