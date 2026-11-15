#!/usr/bin/env python3
"""Read-only metadata/custody checks; no browser/network/scientific replay.

Stdlib only, stdout only. Strict equality distinguishes bool/int, null/empty
objects, dictionary key order, list order and duplicate ordered headers.
"""
from copy import deepcopy
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path

BASE = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
OWN = Path(__file__).resolve().parent
checks = []
mutations = []


def require(value, name):
    if not value:
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


def data(f):
    return json.loads(f.read_text())


def sha(f):
    return hashlib.sha256(f.read_bytes()).hexdigest()


def gates113(publication, promotion):
    off = ['production_integration_authorized', 'publication_clearance',
           'ready_to_publish', 'rendered_copy_verified', 'local_http_verified',
           'deployed', 'live_verified', 'browser_verified', 'native_verified',
           'canonical_verified']
    for container in [publication['review_metadata'], promotion]:
        if any(container[k] is not False for k in off):
            return False
        if any(container[k] is not None for k in ['canonical_url', 'native_sheet_aa_url', 'AA']):
            return False
    return (publication['canonical_url'] is None and publication['AA'] is None
            and publication['follow_up'] is None and promotion['follow_up'] is None
            and publication['seo']['canonical_url'] is None
            and publication['seo']['open_graph_url'] is None)


def gates114(promotion):
    state = promotion['state']
    off = ['public_promotion_authority', 'production_config_authority',
           'production_config_created', 'site_created', 'site_deployed',
           'live_page_verified', 'browser_publication_gate', 'native_service_gate',
           'tracker_gate', 'redirect_gate', 'git_gate', 'release_gate']
    return (all(state[k] is False for k in off)
            and all(state[k] is None for k in ['root_editorial_adoption', 'canonical_url', 'AA'])
            and promotion['science']['follow_up'] is None
            and promotion['source']['native_API_version'] == '1.0'
            and promotion['source']['printed_PDF_version'] is None)


def rejected(name, changed_is_valid):
    if changed_is_valid:
        raise RuntimeError('Metadata mutation survived: '+name)
    mutations.append(name)


guard = data(OWN/'INPUT_MANIFEST.json')
for item in guard['files']:
    f = Path(item['path'])
    require(f.is_file() and f.stat().st_size == item['bytes'] and sha(f) == item['sha256'],
            'Protected bytes: '+str(f.relative_to(BASE)))

records = {}
for rid, version, date, order in [
    (23441890, '1.0.0', '2026-10-17', ['source-and-verification.zip', 'paper.pdf']),
    (23174283, '1.0', '2026-10-05', ['spherical_fibonacci_separation.pdf', 'spherical_fibonacci_verification.zip'])
]:
    q = BASE/'papers'/str(rid)
    root_file = BASE/'verification'/('root-clearance-'+str(rid)+'-20261114.json')
    root, ready = data(root_file), data(q/'sources/SOURCE_READY.json')
    record, latest, versions = [data(q/'sources'/f) for f in ['record.raw.json','latest.raw.json','versions.raw.json']]
    require(strict(root['whole_original_source_ready_object'], ready), str(rid)+' root whole SOURCE_READY')
    require(root['source_ready_sha256'] == sha(q/'sources/SOURCE_READY.json'), str(rid)+' source ready hash')
    require(ready['version'] == version and record['metadata']['version'] == version, str(rid)+' exact native version')
    require(ready['publication_date'] == date == record['metadata']['publication_date'], str(rid)+' declared publication date')
    require(ready['created'] == record['created'] and ready['updated'] == record['updated'], str(rid)+' distinct native timestamps')
    require(record['metadata']['license'] == {'id':'cc-by-4.0'}, str(rid)+' actual license object')
    require((q/'sources/record.raw.json').read_bytes() == (q/'sources/latest.raw.json').read_bytes(), str(rid)+' record/latest identical bytes')
    require(record['swh'] == {} and versions['hits']['hits'][0]['swh'] is None, str(rid)+' native empty-object versus null preserved')
    require(versions['hits']['total'] == 1, str(rid)+' complete native one-version response')
    require([x['key'] for x in record['files']] == order, str(rid)+' native asset order')
    require([x['original_api_file_object']['key'] for x in ready['all_assets_in_original_order']] == order, str(rid)+' ready asset order')
    for asset, raw in zip(ready['all_assets_in_original_order'], record['files']):
        f = Path(asset['path'])
        require(strict(asset['original_api_file_object'], raw), str(rid)+' complete original file object '+raw['key'])
        require(f.stat().st_size == raw['size'] == asset['bytes'] and sha(f) == asset['sha256']
                and hashlib.md5(f.read_bytes()).hexdigest() == raw['checksum'].split(':')[1], str(rid)+' native asset size/MD5/SHA '+raw['key'])
    receipts = root['whole_native_transport_objects']
    require(len(receipts) == 6, str(rid)+' six complete transport objects, five requests')
    for wrapper in receipts:
        f = Path(wrapper['path'])
        require(wrapper['sha256'] == sha(f) and strict(wrapper['original'], data(f)), str(rid)+' exact transport object '+f.name)
    individual = [data(q/'sources'/('transport-0'+str(i)+'-'+kind+'.json')) for i,kind in [(1,'record'),(2,'latest'),(3,'versions'),(4,'asset'),(5,'asset')]]
    aggregate = data(q/'sources/transport-receipts.json')
    require(strict(individual,aggregate['ordinary_HTTPS_requests_in_native_object_and_file_order']), str(rid)+' aggregate exact request ordering')
    require(all(sum(pair[0]=='content-type' for pair in x['response_headers_in_received_order']) == 2 for x in individual[3:]), str(rid)+' duplicate asset content-type headers retained')
    for lane in ['scope','analytic','adversarial']:
        wrapper = root['reviews'][lane]
        f = q/'reviews'/lane/'VERDICT.json'
        require(wrapper['verdict_sha256'] == sha(f) and strict(wrapper['verdict_original'],data(f)), str(rid)+' whole literal '+lane+' verdict')
    require(root['canonical_url'] is None and root['AA'] is None and root['follow_up'] is None and root['public_promotion_authority'] is False, str(rid)+' root current public boundary')
    records[rid] = {'root':root,'ready':ready,'record':record,'latest':latest,'versions':versions,'folder':q}

q = records[23441890]['folder']
pub, pro = data(q/'publication.json'), data(q/'promotion.json')
binding = pub['source_binding']
require(gates113(pub,pro), '113 all current public gates false and null followup/canonical/AA')
require(pro['publication_sha256'] == sha(q/'publication.json'), '113 promotion binds exact publication bytes')
require(strict(pro['whole_root_scientific_clearance_record'],records[23441890]['root']), '113 whole exact root authority')
for key, raw in [('whole_native_record','record'),('whole_native_latest_record','latest'),('whole_native_versions','versions')]:
    require(strict(binding[key],records[23441890][raw]), '113 publication complete '+raw)
    promoted = {'whole_native_record':'whole_original_native_record','whole_native_latest_record':'whole_original_native_latest_record','whole_native_versions':'whole_original_native_versions'}[key]
    require(strict(pro[promoted],records[23441890][raw]), '113 promotion complete '+raw)
require(strict(binding['whole_original_source_ready'],records[23441890]['ready']), '113 publication whole source ready')
require(strict(pro['whole_original_source_ready'],records[23441890]['ready']), '113 promotion whole source ready')
require(strict(binding['whole_original_native_transport_objects'],records[23441890]['root']['whole_native_transport_objects']), '113 publication whole transports')
require(strict(pro['whole_original_native_transport_objects'],records[23441890]['root']['whole_native_transport_objects']), '113 promotion whole transports')
for lane in ['scope','analytic','adversarial']:
    require(strict(pub['review_metadata']['whole_original_review_verdicts'][lane], records[23441890]['root']['reviews'][lane]['verdict_original']), '113 publication whole '+lane+' verdict')
require(pub['version']=='1.0.0' and pub['publication_date']=='2026-10-17' and pub['license']==pub['code_license']=='CC BY 4.0', '113 public version/date/license')
require(binding['license_text_original']==(q/'sources/published-source/kourovka-21-149/LICENSE.txt').read_text(), '113 actual authored license text retained')
require(pub['reader_intro'].find('six-page')>=0 and pub['pdf_pages']==6, '113 complete six-page reader requirement')

q = records[23174283]['folder']
p114 = data(q/'publication/promotion/promotion.json')
snapshot = data(q/'reviews/editorial/LITERAL_INPUT_SNAPSHOT.json')
require(gates114(p114), '114 public gates false/null and native-versus-printed version distinction')
require(strict(snapshot['source_ready_original'],records[23174283]['ready']), '114 whole literal source ready snapshot')
require(strict(snapshot['whole_native_transport_objects'],records[23174283]['root']['whole_native_transport_objects']), '114 whole literal transport snapshot')
for lane in ['scope','analytic','adversarial']:
    require(strict(snapshot['literal_custom_verdicts'][lane],records[23174283]['root']['reviews'][lane]['verdict_original']), '114 whole literal '+lane+' verdict snapshot')
for f in (q/'reviews/editorial/inputs').iterdir():
    if not f.is_file():
        continue
    mapping = {'root-clearance.json':BASE/'verification/root-clearance-23174283-20261114.json',
               'root-review.md':q/'reviews/root/ROOT_REVIEW_20261114.md',
               'scope-VERDICT.json':q/'reviews/scope/VERDICT.json',
               'analytic-VERDICT.json':q/'reviews/analytic/VERDICT.json',
               'adversarial-VERDICT.json':q/'reviews/adversarial/VERDICT.json'}
    original = mapping.get(f.name,q/'sources'/f.name)
    require(f.read_bytes()==original.read_bytes(), '114 byte-identical input '+f.name)
source = p114['source']
require(source['declared_publication_date']=='2026-10-05' and source['record_created']=='2026-10-05T23:41:09.395608+00:00' and source['record_updated']=='2026-10-10T21:33:20.838889+00:00', '114 separate declared/created/updated')
require(strict(source['license_original'],records[23174283]['record']['metadata']['license']), '114 actual license retained')
for item in [source['PDF'],source['original_support_ZIP']]:
    f=q/'publication/promotion'/item['file']
    require(f.stat().st_size==item['bytes'] and sha(f)==item['sha256'] and hashlib.md5(f.read_bytes()).hexdigest()==item['MD5'], '114 complete byte-identical staged '+f.name)
later=p114['prior_work']['later_matching_related_work']
require(later['record_id']==23681420 and later['declared_publication_date']=='2026-10-27' and later['chronology_only'] is True and later['independence_inference'] is False and later['influence_inference'] is False and later['absolute_priority_inference'] is False, '114 neutral later matching-work metadata')

class Head(HTMLParser):
    def __init__(self):
        super().__init__();self.meta={};self.canonical=[];self.frames=[];self.links=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='meta':self.meta[a.get('name',a.get('property',''))]=a.get('content')
        if tag=='link' and a.get('rel')=='canonical':self.canonical.append(a.get('href'))
        if tag=='iframe':self.frames.append(a)
        if tag=='a':self.links.append(a)

html=(q/'publication/promotion/page.html').read_text();head=Head();head.feed(html)
require(head.meta['robots']=='noindex,nofollow' and not head.canonical, '114 private HTML robots and no assigned canonical')
require(head.meta['citation_doi']=='10.5281/zenodo.23174283' and head.meta['citation_publication_date']=='2026/10/05', '114 exact HTML citation metadata')
require(len(head.frames)==1 and 'spherical_fibonacci_separation.pdf' in head.frames[0].get('src','') and head.frames[0].get('title'), '114 whole PDF reader and descriptive title')
require(any('download' in a and a.get('href')=='assets/spherical_fibonacci_separation.pdf' for a in head.links), '114 explicit PDF download link')
require(any('download' in a and a.get('href')=='assets/spherical_fibonacci_verification.zip' for a in head.links), '114 explicit whole ZIP download link')

# Pure in-memory checks; no altered original or staged file is created.
m=deepcopy(pro);m['deployed']=True;rejected('113 premature deployed flag',gates113(pub,m))
m=deepcopy(pro);m['AA']='https://example.invalid/';rejected('113 premature AA assignment',gates113(pub,m))
m=deepcopy(pub);m['follow_up']='generic new problem';rejected('113 invented follow-up',gates113(m,pro))
m=deepcopy(binding['whole_native_versions']);m['hits']['hits'][0]['swh']={};rejected('normalize native versions null to empty object',strict(m,records[23441890]['versions']))
m=deepcopy(records[23441890]['root']['whole_native_transport_objects']);m[0]['original']['response_headers_in_received_order']=dict(m[0]['original']['response_headers_in_received_order']);rejected('flatten ordered headers to dictionary',strict(m,records[23441890]['root']['whole_native_transport_objects']))
m=deepcopy(p114);m['source']['printed_PDF_version']='1.0';rejected('114 invent printed manuscript version',gates114(m))
m=deepcopy(p114);m['state']['canonical_url']=m['proposed']['page_url'];rejected('114 premature canonical assignment',gates114(m))
m=deepcopy(p114);m['science']['follow_up']='broader rational criterion';rejected('114 already-covered follow-up',gates114(m))
rejected('bool coerced into integer',strict(True,1))
m=deepcopy(records[23174283]['ready']);m['all_assets_in_original_order'].reverse();rejected('reverse original PDF-before-ZIP order',strict(m,records[23174283]['ready']))

print(json.dumps({'status':'QUALIFIED_PASS_METADATA_AND_CUSTODY_BOTH_RECORDS',
                  'records':[23441890,23174283], 'checks':len(checks),
                  'protected_preexisting_files_checked':len(guard['files']),
                  'negative_controls_rejected':len(mutations),'negative_controls':mutations,
                  'strict_type_dictionary_key_order_and_list_order':True,
                  'all_six_literal_scientific_verdicts_preserved':True,
                  'public_adoption_authority':False,'network_or_browser':False,
                  'scientific_campaign_or_existing_verifier_executed':False,
                  'preexisting_writes':False},indent=2))
