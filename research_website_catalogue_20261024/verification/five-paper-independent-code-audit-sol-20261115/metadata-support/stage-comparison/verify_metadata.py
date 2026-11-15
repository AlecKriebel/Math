#!/usr/bin/env python3
"""Independent pure metadata/custody check of the explicitly selected pair.

No stage/source programs are imported or run. The only imported audit helper
is this lane's own pre-stage sealed approved-input checker. All other actions
are JSON/HTML parsing and byte/hash comparisons; stdout is the only output.
"""
from copy import deepcopy
import hashlib
from html.parser import HTMLParser
import importlib.util
import json
from pathlib import Path
import re
import sys
sys.dont_write_bytecode=True

OWN=Path(__file__).resolve().parent
PRE=OWN.parent
BASE=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
STAGE=BASE/'verification/five-paper-private-stage-sol-20261115'
FINAL_SHA='80db4036c349909dea6138effb23c3ae764a0e2a748aa2efc521b0b5a5439eec'
MANIFEST_SHA='4a470cdf6f34cae17e378a50f5d678d61a44f1053be8fe756d0f86f338a76a3a'
checks=[];controls=[]


def load(path):
    def unique(pairs):
        out={}
        for key,value in pairs:
            if key in out:raise RuntimeError('Duplicate JSON key: '+key)
            out[key]=value
        return out
    return json.loads(path.read_text(),object_pairs_hook=unique)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def strict(a,b):
    if type(a) is not type(b):return False
    if isinstance(a,dict):return list(a)==list(b) and all(strict(a[k],b[k]) for k in a)
    if isinstance(a,list):return len(a)==len(b) and all(strict(x,y) for x,y in zip(a,b))
    return a==b


def check(test,name):
    if not test:raise RuntimeError(name)
    checks.append(name)


def reject(name,accepted):
    if accepted:raise RuntimeError('Metadata control survived: '+name)
    controls.append(name)


class HTML(HTMLParser):
    def __init__(self,text):
        super().__init__(convert_charrefs=True)
        self.metas={};self.canonicals=[];self.iframes=[];self.links=[];self.scripts=[]
        self.all_text=[];self.in_ld=False;self.ld='';self.feed(text)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='meta':self.metas.setdefault(a.get('name',a.get('property','')),[]).append(a.get('content'))
        if tag=='link' and a.get('rel')=='canonical':self.canonicals.append(a.get('href'))
        if tag=='iframe':self.iframes.append(a)
        if tag=='a':self.links.append(a)
        if tag=='script' and a.get('type')=='application/ld+json':self.in_ld=True;self.ld=''
    def handle_endtag(self,tag):
        if tag=='script' and self.in_ld:self.scripts.append(json.loads(self.ld));self.in_ld=False
    def handle_data(self,text):
        if self.in_ld:self.ld+=text
        else:self.all_text.append(text)
    def one(self,name):
        values=self.metas.get(name,[])
        if len(values)!=1:raise RuntimeError('Not exactly one metadata value: '+name)
        return values[0]


# The pre-stage snapshot remains immutable and predates target inspection.
preseal=load(PRE/'PRE_STAGE_BINDINGS_SEAL.json')
check(sha(PRE/'PRE_STAGE_BINDINGS_SEAL.json')=='8d6c48338dffac18f4cd40cf192e096cd8bd35e5e859cdf18507c45ee7e38656','Independent pre-stage seal unchanged')
for name,key in [('APPROVED_METADATA.json','approved_metadata_sha256'),('INPUT_MANIFEST.json','approved_input_manifest_sha256'),('EXPECTED_IDENTITIES.json','expected_identities_sha256'),('verify_approved.py','approved_verifier_sha256'),('PRE_STAGE_APPROVED_RESULT.json','pre_stage_result_sha256')]:
    check(sha(PRE/name)==preseal[key],'Pre-stage sealed payload '+name)
spec=importlib.util.spec_from_file_location('own_pre_stage_metadata',PRE/'verify_approved.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
approved_result=module.validate()
check(approved_result['status']=='PASS_APPROVED_METADATA_BINDINGS_STAGE_UNREAD','Own pre-stage metadata custody still passes')
approved=load(PRE/'APPROVED_METADATA.json')
guard=load(OWN/'INPUT_MANIFEST.json')
for item in guard['files']:
    f=Path(item['path'])
    check(f.is_file() and f.stat().st_size==item['bytes'] and sha(f)==item['sha256'],'Immutable final-stage input '+str(f))
check(sha(STAGE/'FINAL_SEAL.json')==FINAL_SHA and sha(STAGE/'OWNED_MANIFEST.json')==MANIFEST_SHA,'Assigned actual final stage identity')
seal=load(STAGE/'FINAL_SEAL.json');manifest=load(STAGE/'OWNED_MANIFEST.json');ready=load(STAGE/'CANDIDATE_READY.json')
for name,key in [('OWNED_MANIFEST.json','owned_manifest_sha256'),('CANDIDATE_READY.json','candidate_ready_sha256'),('CANDIDATE_CODE_MANIFEST.json','code_manifest_sha256'),('FROZEN_INPUT_SET.json','frozen_inputs_sha256'),('FRESH_BASELINE.json','baseline_sha256')]:
    check(sha(STAGE/name)==seal[key],'Actual final owner seal binding '+name)
check(seal['selected_candidate_pair']==['candidate-a/public','candidate-b/public'],'Only explicitly selected final pair')
check(seal['production_install_authorized'] is False and seal['AA'] is None and seal['canonical_URL_assignment'] is None,'Owner seal has no production/native URL authority')
for item in manifest['files']:
    f=STAGE/item['path']
    check(f.stat().st_size==item['bytes'] and sha(f)==item['sha256'],'Whole owner opaque custody '+item['path'])
frozen=load(STAGE/'FROZEN_INPUT_SET.json')
check(len(frozen['input_files'])==663,'Actual663 owner frozen inputs')
for item in frozen['input_files']:
    check('/23385145/' not in item['path'],'118 absent from stage input scope')
    f=Path(item['path'])
    check(f.stat().st_size==item['bytes'] and sha(f)==item['sha256'],'Actual original owner input '+item['path'])
for name,original,key in [
    ('SUPPLEMENTAL_EDITORIAL_AUTHORITY.json',approved['whole_literal_root_adoption_original'],'production_install_authority'),
    ('SUPPLEMENTAL_DLAB_AUTHORITY.json',approved['whole_literal_Dlab_override_original'],'production_or_live_authority')]:
    supplemental=load(STAGE/name)
    check(strict(supplemental['whole_root_authority_original'],original),'Complete additive authority '+name)
    check(sha(Path(supplemental['root_authority_path']))==supplemental['root_authority_sha256'] and supplemental[key] is False,'Exact private-only additive authority '+name)
freeze_seal=load(STAGE/'INPUT_FREEZE_SEAL.json')
for name,key in [('FROZEN_INPUT_SET.json','frozen_inputs_sha256'),('FRESH_BASELINE.json','baseline_sha256'),('PRIVATE_STAGE_POLICY.json','policy_sha256'),('RECORD_LAYOUTS.json','record_layouts_sha256')]:
    check(sha(STAGE/name)==freeze_seal[key],'Original initial freeze '+name)
check(freeze_seal['production_install_authorized'] is False and freeze_seal['AA'] is None and freeze_seal['canonical_url'] is None,'Initial freeze gates remain unassigned')
code=load(STAGE/'CANDIDATE_CODE_MANIFEST.json')
for item in code['files']:
    f=STAGE/item['path']
    check(f.stat().st_size==item['bytes'] and sha(f)==item['sha256'],'Exact inspected/pinned stage source code '+item['path'])

candidate_roots=[STAGE/'candidate-a/public',STAGE/'candidate-b/public']
entries=ready['all_22_exact_outputs'];expected_paths={x['path'] for x in entries}
check(len(entries)==len(expected_paths)==22,'Exactly22 selected output paths')
for root in candidate_roots:
    check({str(f.relative_to(root)) for f in root.rglob('*') if f.is_file()}==expected_paths,'Exact selected file set '+str(root))
    for item in entries:
        f=root/item['path']
        check(not f.is_symlink() and f.stat().st_size==item['bytes'] and sha(f)==item['sha256'],'Selected ready output '+str(f))
for item in entries:
    check((candidate_roots[0]/item['path']).read_bytes()==(candidate_roots[1]/item['path']).read_bytes(),'Pairwise selected bytes '+item['path'])

whole_source_objects=0;verdicts=0;native_asset_checks=0;scholarly_checks=[]
for approved_record in approved['records']:
    rid=approved_record['record_id'];q=BASE/'papers'/rid;current=frozen['records'][rid];layout=current['layout']
    check(strict(current['source_ready_original'],approved_record['whole_literal_source_ready_original']),rid+' exact pre-stage source-ready object')
    check(strict(current['native_record_original'],approved_record['whole_literal_native_record_original']),rid+' exact pre-stage native record')
    check(strict(current['whole_root_scientific_authority'],approved_record['whole_literal_root_science_authority_original']),rid+' exact whole root scientific authority')
    for config in approved_record['approved_configuration_objects']:
        name=Path(config['approved_binding_original']['path']).name
        field='whole_config_original' if name=='publication.json' else 'whole_promotion_original'
        if layout['kind']=='html':field='whole_config_original'
        check(strict(current[field],config['whole_literal_original_object']),rid+' exact frozen full approved '+name)
    check(strict(load(q/layout['editorial_seal']),current['editorial_seal_original']),rid+' complete original editorial seal')
    for name,obj in current['whole_native_root_JSON_objects'].items():
        check(strict(load(q/'sources'/name),obj),rid+' full heterogeneous native original '+name)
        whole_source_objects+=1
    for item in approved_record['whole_three_literal_scientific_verdicts']:
        check(strict(current['whole_three_custom_verdicts'][item['lane']],item['whole_literal_original_object']),rid+' full literal scientific verdict '+item['lane'])
        verdicts+=1
    config=current['whole_config_original'];promotion=current['whole_promotion_original']
    if layout['kind'] in ['config','html-config']:
        slug=config['slug'];abstract=config['abstract'];followup=config['follow_up'];code_license=config['code_license']
        check(config['canonical_url'] is None and config['AA'] is None and promotion['canonical_url'] is None and promotion['AA'] is None,rid+' original native canonical/AA flags remain null')
        check(code_license==approved_record['approved_code_license_policy']['explicit_approved_code_license'],rid+' exact approved code license, no default')
    else:
        slug=promotion['proposed']['slug'];abstract=(q/layout['abstract']).read_text().strip();followup=promotion['science']['follow_up']
        check(promotion['state']['canonical_url'] is None and promotion['state']['AA'] is None and promotion['state']['root_editorial_adoption'] is None,rid+' original nested public flags remain null')
    check(followup is None,rid+' approved follow-up remains null')
    planned='https://aleckriebel.com/research/'+slug+'/'
    pdf=next(a for a in approved_record['approved_assets'] if a['actual_native_path'].endswith('.pdf'))
    archive=next(a for a in approved_record['approved_assets'] if a['actual_native_path'].endswith('.zip'))
    pdf_name=Path(pdf['actual_native_path']).name;zip_name=Path(archive['actual_native_path']).name
    for root in candidate_roots:
        folder=root/'research'/slug;html=(folder/'index.html').read_text();parsed=HTML(html)
        check(parsed.one('citation_title')==approved_record['title'] and parsed.one('citation_doi')==approved_record['DOI'],rid+' selected exact title/DOI')
        check(parsed.one('citation_publication_date')==approved_record['original_publication_date'].replace('-','/'),rid+' selected original publication date')
        check(parsed.one('citation_pdf_url')==planned+pdf_name and parsed.one('citation_author_orcid')=='0009-0001-9320-500X',rid+' exact selected PDF/ORCID citation')
        check(parsed.one('robots')=='index,follow' and parsed.canonicals==[planned] and parsed.one('og:url')==planned,rid+' consistent private proposed head URLs/robots')
        check(len(parsed.scripts)==1 and parsed.scripts[0]['@context']=='https://schema.org',rid+' one valid scholarly graph')
        graph=parsed.scripts[0]['@graph'];article=next(x for x in graph if x['@type']=='ScholarlyArticle');webpage=next(x for x in graph if x['@type']=='WebPage')
        check(article['name']==article['headline']==approved_record['title'] and article['identifier']['value']==approved_record['DOI'],rid+' scholarly exact identity')
        check(article['datePublished']==approved_record['original_publication_date'] and article['version']==approved_record['API_version'] and article['creativeWorkStatus']=='Unrefereed preprint',rid+' scholarly date/version/status without generic PASS')
        check(article['abstract']==abstract,rid+' complete exact approved scholarly abstract')
        check(article['license']=='https://creativecommons.org/licenses/by/4.0/' and article['author']['sameAs']=='https://orcid.org/0009-0001-9320-500X',rid+' native article rights and author identity')
        check(article['url']==planned and article['sameAs']=='https://doi.org/'+approved_record['DOI'] and webpage['url']==planned,rid+' proposed graph identifiers consistent')
        encoding=article['encoding'];encoding=encoding if isinstance(encoding,list) else [encoding]
        check(any(x['encodingFormat']=='application/pdf' and x['contentUrl']==planned+pdf_name for x in encoding),rid+' exact encoded complete native PDF')
        check(len(parsed.iframes)==1 and parsed.iframes[0]['src'].split('#')[0]==pdf_name and bool(parsed.iframes[0].get('title')),rid+' titled whole native reader')
        check(any('download' in a and a.get('href')==pdf_name for a in parsed.links) and any('download' in a and a.get('href')==zip_name for a in parsed.links),rid+' exact complete PDF/ZIP downloads')
        original_urls=[x['original_native_asset_descriptor']['original_api_file_object']['links']['self'] for x in approved_record['approved_assets']]
        check([a['href'] for a in parsed.links if a.get('href') in original_urls]==original_urls,rid+' complete native API links in original asset order')
        body=' '.join(parsed.all_text)
        check(('MIT License' in body)==(rid=='23149775'),rid+' actual separate code-rights display only where granted')
        if rid=='23174283':check('Zenodo version 1.0' in body,rid+' unprinted source version remains explicitly Zenodo metadata')
        if rid=='23441890':
            override=approved['whole_literal_Dlab_override_original']
            check(any(a.get('href')==override['new_href'] for a in parsed.links) and not any(a.get('href')==override['old_href'] for a in parsed.links),rid+' exact adopted Dlab href override')
        check((folder/'citation.bib').read_bytes()==(q/layout['bib']).read_bytes(),rid+' whole approved BibTeX bytes')
        for a in approved_record['approved_assets']:
            original=Path(a['actual_native_path']);staged=folder/original.name
            check(staged.read_bytes()==original.read_bytes() and staged.stat().st_size==a['bytes'] and sha(staged)==a['sha256'],rid+' exact native staged bytes '+original.name)
            native_asset_checks+=1
        scholarly_checks.append({'record_id':rid,'candidate':root.parent.name,'date':article['datePublished'],'version':article['version'],'DOI':article['identifier']['value'],'native_article_license':article['license'],'future_canonical_is_private_proposal':True})

# Small metadata falsifiers use only memory; no stage mutation is created.
sample=approved['records'][0]['whole_literal_native_versions_original'];m=deepcopy(sample);m['hits']['hits'][0]['swh']={};reject('version null normalized to empty object',strict(m,sample))
sample=approved['records'][0]['whole_three_literal_scientific_verdicts'][0]['whole_literal_original_object'];m=deepcopy(sample);m['status']='PASS';reject('whole custom scientific status coerced to generic PASS',strict(m,sample))
sample=frozen['records']['23430498']['whole_config_original'];m=deepcopy(sample);m['code_license']='MIT';reject('115 generic MIT default',strict(m,sample))
sample=frozen['records']['23174283']['whole_promotion_original'];m=deepcopy(sample);m['source']['printed_PDF_version']='1.0';reject('114 invented printed version',strict(m,sample))
m=deepcopy(seal);m['AA']='https://example.invalid/';reject('premature native AA assignment',strict(m,seal))
m=deepcopy(seal);m['production_install_authorized']=True;reject('premature installation authority',strict(m,seal))
reject('bool/int coercion',strict(True,1))
reject('native asset order reversed',strict(['zip','pdf'],['pdf','zip']))
reject('wrong native asset body',hashlib.sha256(b'truncated').hexdigest()==pdf['sha256'])
reject('created date substituted for publication date',approved['records'][2]['created_original'][:10]==approved['records'][2]['original_publication_date'])

print(json.dumps({'status':'QUALIFIED_PASS_SELECTED_FIVE_METADATA_AND_NATIVE_CUSTODY',
                  'selected_pair':['candidate-a/public','candidate-b/public'],
                  'pre_stage_approved_checker':approved_result,
                  'stage_comparison_checks':len(checks),'immutable_comparison_inputs':len(guard['files']),
                  'actual_owner_payloads_checked':len(manifest['files']),'actual_owner_original_inputs_checked':len(frozen['input_files']),
                  'whole_native_root_JSON_objects_checked':whole_source_objects,'whole_literal_scientific_verdicts_checked':verdicts,
                  'original_assets':10,'paired_asset_byte_comparisons':native_asset_checks,
                  'all_selected_output_paths_compared':22,'candidate_pair_byte_identical':True,
                  'selected_scholarly_metadata':scholarly_checks,'negative_controls_rejected':len(controls),'negative_controls':controls,
                  'qualification':'Rendered robots/canonical/graph URLs are private future proposals. Original native/config gates and owner public/AA authority remain false/null; no live assignment or deployment is certified.',
                  'substantive_metadata_blocker_found':False,'record118_excluded':True,
                  'stage_or_source_code_executed':False,'network_or_browser':False,'preexisting_writes':False,
                  'scientific_reassessment_or_production_authority':False},indent=2))
