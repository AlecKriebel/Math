#!/usr/bin/env python3
"""Read-only stdlib metadata/custody audit; stdout only, no old verifier.

Uses each actual schema as deposited. It does not normalize the distinct
116 transport structures or 117 api-receipts structure into one authority.
No network/browser/scientific program invocation or file writes.
"""
from copy import deepcopy
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path

BASE = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
OWN = Path(__file__).resolve().parent
checks = []
controls = []
ROOT_HASHES = {
    23149775:'b1ae0e007d98f9ece4c712556239c0a9802befd93154972a3d5af39ea9c583b7',
    23331080:'df67490c786bef3bcb1623cfb4a25f5b8948a74d49c039b199543a7cf21da315',
}


def data(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(test, name):
    if not test:
        raise RuntimeError(name)
    checks.append(name)


def strict(a, b):
    if type(a) is not type(b):
        return False
    if isinstance(a, dict):
        return list(a) == list(b) and all(strict(a[k], b[k]) for k in a)
    if isinstance(a, list):
        return len(a) == len(b) and all(strict(x, y) for x, y in zip(a, b))
    return a == b


def gates(p):
    s = p['state']
    names = ['public_promotion_authority','production_config_authority',
             'production_config_created','site_created','site_deployed',
             'live_page_verified','browser_publication_gate','native_service_gate',
             'tracker_gate','redirect_gate','git_gate','release_gate']
    return (all(s[k] is False for k in names)
            and all(s[k] is None for k in ['root_editorial_adoption','canonical_url','AA'])
            and p['science']['follow_up'] is None)


def exact116_properties(p):
    s = p['source']
    return (s['native_API_version'] == '1.0' and s['printed_PDF_version'] == '1.0'
            and s['declared_printed_publication_date'] == '2026-10-04'
            and s['paper_prose_license'] == 'CC BY 4.0' and s['original_code_license'] == 'MIT')


def exact117_properties(p):
    s = p['source']
    return (s['version'] == '1.0' and s['declared_publication_date'] == '2026-10-12'
            and s['separate_code_license'] is None and s['readiness_schema_tag_present'] is False)


def reject(name, accepted):
    if accepted:
        raise RuntimeError('In-memory metadata mutation survived: '+name)
    controls.append(name)


class Head(HTMLParser):
    def __init__(self):
        super().__init__(); self.meta={}; self.canonical=[]; self.frames=[]; self.links=[]
        self.in_ld=False; self.ld=''
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag=='meta': self.meta[a.get('name',a.get('property',''))]=a.get('content')
        if tag=='link' and a.get('rel')=='canonical': self.canonical.append(a.get('href'))
        if tag=='iframe': self.frames.append(a)
        if tag=='a': self.links.append(a)
        if tag=='script' and a.get('type')=='application/ld+json': self.in_ld=True
    def handle_endtag(self, tag):
        if tag=='script': self.in_ld=False
    def handle_data(self, text):
        if self.in_ld: self.ld += text


guard=data(OWN/'INPUT_MANIFEST.json')
for item in guard['files']:
    f=Path(item['path'])
    require(f.is_file() and f.stat().st_size==item['bytes'] and sha(f)==item['sha256'],
            'Protected bytes: '+str(f.relative_to(BASE)))

records={}
for rid in [23149775,23331080]:
    q=BASE/'papers'/str(rid)
    root_file=BASE/'verification'/('root-clearance-'+str(rid)+'-20261114.json')
    root,ready,snapshot,promotion=[data(f) for f in [root_file,q/'sources/SOURCE_READY.json',q/'reviews/editorial/LITERAL_INPUT_SNAPSHOT.json',q/'publication/promotion/promotion.json']]
    record_file=q/'sources'/('record-attempt2.body' if rid==23149775 else 'record.raw.json')
    versions_file=q/'sources'/('versions.page-001.raw.json' if rid==23149775 else 'versions.raw.json')
    record,versions=data(record_file),data(versions_file)
    require(sha(root_file)==ROOT_HASHES[rid], str(rid)+' exact assigned root authority hash')
    require(strict(root['source_ready']['original'],ready) and root['source_ready']['sha256']==sha(q/'sources/SOURCE_READY.json'), str(rid)+' full root SOURCE_READY object/hash')
    require(strict(root['source_manifest_original'],data(q/'sources/SOURCE_READY_MANIFEST.json')), str(rid)+' whole root native source manifest')
    require(strict(root['source_seal_original'],data(q/'sources/SOURCE_READY_SEAL.json')), str(rid)+' whole root native source seal')
    require(strict(root['native_record_original'],record), str(rid)+' complete native record in root')
    require(strict(snapshot['source_ready_original'],ready) and strict(snapshot['native_record_original'],record), str(rid)+' complete source/record snapshot')
    require(record_file.read_bytes()==(q/'sources/latest.raw.json').read_bytes(), str(rid)+' record/latest complete byte identity')
    require(record['swh']=={} and versions['hits']['hits'][0]['swh'] is None, str(rid)+' native empty-object/null distinction')
    require(versions['hits']['total']==1, str(rid)+' native complete one-version response')
    require(record['metadata']['version']=='1.0' and record['metadata']['license']=={'id':'cc-by-4.0'}, str(rid)+' actual native version/license object')
    require(gates(promotion), str(rid)+' current public gates false; adoption/canonical/AA/followup null')
    require(root['public_promotion_authority'] is False and root['canonical_url'] is None and root['AA'] is None and root['follow_up'] is None, str(rid)+' root public boundary')
    require(promotion['science']['root_clearance_SHA256']==sha(root_file), str(rid)+' nested promotion exact root reference')
    verdict_key='literal_custom_verdicts' if rid==23149775 else 'literal_three_custom_verdicts'
    for lane in ['scope','analytic','adversarial']:
        f=q/'reviews'/lane/'VERDICT.json'
        original=data(f);wrapper=root['reviews'][lane]
        require(wrapper['verdict_sha256']==sha(f) and strict(wrapper['verdict_original'],original), str(rid)+' root complete literal '+lane+' verdict')
        require(strict(snapshot[verdict_key][lane],original), str(rid)+' snapshot complete literal '+lane+' verdict')
    assets=ready['all_native_assets_in_original_order'] if rid==23149775 else ready['all_assets_in_original_order']
    require([x['original_api_file_object']['key'] for x in assets]==[x['key'] for x in record['files']], str(rid)+' native asset order retained')
    require([x['key'].rsplit('.',1)[1] for x in record['files']]==['pdf','zip'], str(rid)+' PDF then complete ZIP')
    for item,raw in zip(assets,record['files']):
        f=Path(item['path']);h=item['SHA256'] if rid==23149775 else item['sha256']
        require(strict(item['original_api_file_object'],raw), str(rid)+' complete original asset object '+raw['key'])
        require(f.stat().st_size==item['bytes']==raw['size'] and sha(f)==h and hashlib.md5(f.read_bytes()).hexdigest()==raw['checksum'].split(':')[1], str(rid)+' native size/MD5/SHA '+raw['key'])
        staged=q/'publication/promotion/assets'/raw['key']
        require(staged.read_bytes()==f.read_bytes(), str(rid)+' whole staged asset byte identity '+raw['key'])
    source=promotion['source']
    require(source['record_created']==record['created'] and source['record_updated']==record['updated'], str(rid)+' exact distinct created/updated timestamps')
    require(source['DOI']==record['doi'] and source['title']==record['metadata']['title'], str(rid)+' exact title/DOI')
    # Byte copies use their actual names and locations, never transport guesses.
    inputs=q/'reviews/editorial/inputs'
    mappings={'root-clearance.json':root_file,'root-review.md':q/'reviews/root/ROOT_REVIEW_20261114.md',
              'acquisition-VERDICT.json':q/'acquisition/VERDICT.json'}
    mappings.update({lane+'-VERDICT.json':q/'reviews'/lane/'VERDICT.json' for lane in ['scope','analytic','adversarial']})
    for copy in inputs.iterdir():
        if copy.is_file():
            original=mappings.get(copy.name,q/'sources'/copy.name)
            require(copy.read_bytes()==original.read_bytes(), str(rid)+' complete byte copy '+copy.name)
    html=(q/'publication/promotion/page.html').read_text();head=Head();head.feed(html);ld=json.loads(head.ld)
    declared=record['metadata']['publication_date'];doi=record['doi'];pdf=record['files'][0]['key'];archive=record['files'][1]['key']
    require(head.meta['robots']=='noindex,nofollow' and not head.canonical, str(rid)+' private HTML robots and absent canonical')
    require(head.meta['citation_doi']==doi and head.meta['citation_publication_date']==declared.replace('-','/') and head.meta['citation_title']==record['metadata']['title'], str(rid)+' exact HTML scholarly citation')
    require(ld['datePublished']==declared and ld['version']=='1.0' and ld['identifier']['value']==doi and ld['license']=='https://creativecommons.org/licenses/by/4.0/' and ld.get('url') is None, str(rid)+' JSON-LD native date/version/DOI/license without canonical assignment')
    require(len(head.frames)==1 and pdf in head.frames[0].get('src','') and bool(head.frames[0].get('title')), str(rid)+' titled complete PDF reader')
    require(any('download' in a and a.get('href')=='assets/'+pdf for a in head.links), str(rid)+' explicit PDF download')
    require(any('download' in a and a.get('href')=='assets/'+archive for a in head.links), str(rid)+' explicit whole ZIP download')
    records[rid]={'folder':q,'root':root,'ready':ready,'record':record,'versions':versions,'snapshot':snapshot,'promotion':promotion,'html':html}

r=records[23149775];q=r['folder'];p=r['promotion'];s=r['snapshot']
require(exact116_properties(p), '116 native/printed version/date and separate CC-BY/MIT rights')
require(p['source']['declared_printed_publication_date']==r['record']['metadata']['publication_date'] and r['ready']['publication_date_declared']=='2026-10-04', '116 original4Oct date not5Oct creation or10Oct update')
require('Creative Commons Attribution 4.0' in Path(p['source']['paper_license_source']).read_text() and Path(p['source']['code_license_source']).read_text().startswith('MIT License'), '116 actual separate paper/code license texts')
require('Original verification code:' in r['html'] and '>MIT License</a>' in r['html'], '116 actual public CC-BY/MIT distinction')
transport_names=r['ready']['transport_files']
require(transport_names==['metadata.transport.json','record-attempt2.transport.json','native.transport.v2.json','asset.transport.v3.json'], '116 actual four mixed transport names/order')
wrappers=s['four_heterogeneous_transport_objects_in_native_order']
require([x['name'] for x in wrappers]==transport_names, '116 exact heterogeneous wrapper order')
objects=[]
for wrapper in wrappers:
    f=Path(wrapper['original_source_path']);obj=data(f);objects.append(obj)
    require(wrapper['sha256']==sha(f) and strict(wrapper['original_object'],obj), '116 whole actual transport '+f.name)
require([type(x) for x in objects]==[list,dict,list,list], '116 list/dict/list/list schemas retained')
exception=objects[0][0]
require(exception['error_type']=='HTTPError' and exception['successful_body'] is False and '403' in exception['error'] and 'HTTP_status' not in exception and 'response_headers_in_received_order' not in exception and 'body' not in exception, '116 honest first403 exception-only capture limit')
require([x['HTTP_status'] for x in objects[2]]==[200,200,200,406], '116 v2 success and406 failure order retained')
failed=objects[2][-1];failure_body=Path(failed['body']['path'])
require(failure_body.stat().st_size==88 and sha(failure_body)==failed['body']['SHA256'] and data(failure_body)['status']==406, '116 failed .pdf is88-byte406 JSON, not reader')
for obj in [objects[1]]+objects[2]+objects[3]:
    f=Path(obj['body']['path'])
    require(f.stat().st_size==obj['body']['bytes'] and sha(f)==obj['body']['SHA256'], '116 actual transport body bytes '+f.name)
require(all(x['HTTP_status']==200 and x['request_headers']['Accept']=='*/*' for x in objects[3]), '116 separate ordinary wildcard successful asset attempts')
require(all(sum(h[0]=='content-type' for h in x['response_headers_in_received_order'])==2 for x in objects[3]), '116 duplicate successful asset headers retained')
require(Path(r['ready']['selected_actual_PDF']['path'])!=failure_body, '116 failed response not substituted for complete reader')

r=records[23331080];q=r['folder'];p=r['promotion'];s=r['snapshot']
require(exact117_properties(p), '117 exact version/date; no invented schema tag or separate code license')
require(p['source']['declared_publication_date']==r['record']['metadata']['publication_date']=='2026-10-12', '117 declared12Oct date not13Oct creation')
require('The authored paper and package are distributed under CC BY 4.0' in (q/'sources/published-source/positivity-loss-30003571/paper/README.md').read_text(), '117 actual authored package CC-BY grant')
require('deposited supporting material' in r['html'] and '>MIT License</a>' not in r['html'], '117 public native CC-BY rights without MIT substitution')
for key,name in [('source_manifest_original','SOURCE_READY_MANIFEST.json'),('source_seal_original','SOURCE_READY_SEAL.json'),('native_latest_original','latest.raw.json'),('native_versions_original','versions.raw.json'),('native_normalized_metadata_original','normalized-metadata.json'),('native_archive_custody_original','archive-members.json')]:
    require(strict(s[key],data(q/'sources'/name)), '117 whole source snapshot '+name)
require(strict(s['acquisition_verdict_original'],data(q/'acquisition/VERDICT.json')), '117 complete historical acquisition verdict')
api=data(q/'sources/api-receipts.json')
require(type(api) is list and len(api)==5 and strict(s['five_whole_transport_objects_in_native_order'],api), '117 actual five-object api-receipts snapshot')
require(sha(q/'sources/api-receipts.json')==r['ready']['actual_transport_receipt_sha256'], '117 exact receipt binding')
for obj in api:
    f=Path(obj['body']['path'])
    require(obj['HTTP_status']==200 and f.stat().st_size==obj['body']['bytes'] and sha(f)==obj['body']['sha256'], '117 actual transport body '+f.name)
require(all(sum(h[0]=='content-type' for h in x['response_headers_in_received_order'])==2 for x in api[3:]), '117 duplicate asset header ordering retained')

# Small meaningful in-memory falsifiers; no modified file is created.
p116=records[23149775]['promotion'];p117=records[23331080]['promotion']
m=deepcopy(p116);m['state']['site_deployed']=True;reject('premature deployment',gates(m))
m=deepcopy(p117);m['state']['AA']='https://example.invalid/';reject('premature native AA',gates(m))
m=deepcopy(p117);m['science']['follow_up']='generic question';reject('invented follow-up',gates(m))
m=deepcopy(p116);m['source']['original_code_license']='CC BY 4.0';reject('erase116 separate MIT code grant',exact116_properties(m))
m=deepcopy(p117);m['source']['separate_code_license']='MIT';reject('invent117 MIT grant',exact117_properties(m))
m=deepcopy(p116);m['source']['declared_printed_publication_date']='2026-10-05';reject('replace116 declared date by creation date',exact116_properties(m))
m=deepcopy(p116);m['source']['native_API_version']='1.1';reject('alter native version',exact116_properties(m))
m=deepcopy(objects);m[0][0]['HTTP_status']=403;reject('invent unrecorded first-response status schema',strict(m,objects))
m=deepcopy(objects);m[2]=m[2][:-1];reject('erase406 failure object',strict(m,objects))
m=deepcopy(api);m[0]['response_headers_in_received_order']=dict(m[0]['response_headers_in_received_order']);reject('flatten117 ordered headers',strict(m,api))
m=deepcopy(records[23331080]['versions']);m['hits']['hits'][0]['swh']={};reject('coerce native null to empty object',strict(m,records[23331080]['versions']))
reject('coerce boolean into integer',strict(True,1))
m=deepcopy(records[23331080]['ready']);m['all_assets_in_original_order'].reverse();reject('reverse native asset order',strict(m,records[23331080]['ready']))
m=deepcopy(records[23149775]['snapshot']['literal_custom_verdicts']);m['scope']['literal_verdict']='PASS';reject('coerce literal custom verdict into generic PASS',strict(m,records[23149775]['snapshot']['literal_custom_verdicts']))

print(json.dumps({'status':'QUALIFIED_PASS_METADATA_CUSTODY_116_117',
                  'records':[23149775,23331080], 'checks':len(checks),
                  'protected_preexisting_files':len(guard['files']),
                  'whole_literal_scientific_verdicts_preserved':6,
                  'strict_types_key_order_lists_headers':True,
                  'heterogeneous116_failure_and_success_provenance_preserved':True,
                  'actual117_five_api_receipts_preserved':True,
                  'negative_controls_rejected':len(controls),'negative_controls':controls,
                  'preexisting_writes':False,'network_or_browser':False,
                  'scientific_or_existing_content_program_executed':False,
                  'public_adoption_authority':False},indent=2))
