#!/usr/bin/env python3
"""Read-only editorial contract, authority/custody and closure checks. No renderer/replay."""
from pathlib import Path, PurePosixPath
import argparse
import copy
import hashlib
import json
import zipfile

E=Path(__file__).resolve().parent
B=E.parent.parent
P=B.parent.parent


def require(value, message):
    if not value:
        raise RuntimeError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_bytes())


def same(a,b):
    """Preserve native types, empty/null distinction, dict order and all list order."""
    if type(a) is not type(b):
        return False
    if isinstance(a,dict):
        return list(a)==list(b) and all(same(a[k],b[k]) for k in a)
    if isinstance(a,list):
        return len(a)==len(b) and all(same(x,y) for x,y in zip(a,b))
    return a==b


def file_entry(entry):
    f=Path(entry['path'])
    require(f.is_file() and not f.is_symlink(), 'protected original absent/nonregular '+str(f))
    require(f.stat().st_size==entry['bytes'] and sha(f)==entry['sha256'], 'protected original changed '+str(f))


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--require-seal',action='store_true');args=ap.parse_args()
    a=P/'verification/root-clearance-23539734-20261114.json'
    require(sha(a)=='b8b13db377e57e2b264c37b6e252aabb6f6fabc52246840af24e6dcfcff7601e','exact root authority')
    root=read(a); s=B/'sources'; ready=read(s/'SOURCE_READY.json'); receipts=read(s/'api-receipts.json')
    native=read(s/'record.raw.json'); latest=read(s/'latest.raw.json'); versions=read(s/'versions.raw.json')
    norm=read(s/'normalized-metadata.json'); sections=read(E/'public-sections.json')
    p=read(B/'publication.json');q=read(B/'promotion.json')
    flags=read(E/'PUBLICATION_REQUIREMENTS.json')
    statekeys=['rendered','deployed','rendered_public_copy_approved','rendered_copy_verified','local_http_verified',
               'live_http_verified','live_verified','browser_verified','native_verified',
               'native_sheet_publication_verified','public_page_published','root_editorial_clearance_received',
               'production_integration_authorized','publication_clearance','ready_to_publish','canonical_verified']
    nullkeys=['canonical_url','AA','native_sheet_aa_url']
    verdicts={lane:read(Path(item['verdict_path'])) for lane,item in root['reviews'].items()}
    abstractmeta=read(E/'ABSTRACT_PRESENTATION.json')
    tex=(s/'published-source/birational-cycle-verification/paper/main.tex').read_text()
    original=tex.split('\\begin{abstract}',1)[1].split('\\end{abstract}',1)[0]
    abstract=original
    for old,new in abstractmeta['replacement_order']:
        abstract=abstract.replace(old,new)
    abstract=' '.join(abstract.split())

    def contract(pub,prom):
        require(all(same(pub[k],v) for k,v in sections.items()),'complete public prose/metadata changed')
        require(pub['abstract']==abstract and pub['abstract_is_original'] is True,'entire normalized original abstract')
        require(pub['prepared_bibtex']==(E/'citation.bib').read_text(),'prepared citation')
        require(pub['license']=='CC BY 4.0' and pub['code_license']=='CC BY 4.0','native text/code rights')
        require(prom['scientific_status']==root['status'],'literal scientific status')
        require(same(prom['whole_root_scientific_clearance_record'],root),'whole root object including native flags')
        require(same(prom['reviews'],root['reviews']),'whole root family entries')
        require(same(prom['whole_original_custom_family_verdicts'],verdicts),'complete custom family verdicts')
        require(same(prom['whole_original_source_ready'],ready),'promotion whole readiness')
        require(same(prom['whole_original_native_transport_receipts'],receipts),'promotion whole actual receipts')
        binding=pub['source_binding']
        for key,obj in [('whole_original_source_ready',ready),('whole_native_record',native),
                        ('whole_native_latest_record',latest),('whole_native_versions',versions),
                        ('whole_normalized_metadata',norm),('whole_original_native_transport_receipts',receipts),
                        ('all_assets_in_original_order',ready['all_assets_in_original_order'])]:
            require(same(binding[key],obj),'native whole-object/order/null contract '+key)
        require(binding['source_receipt_path']=='sources/api-receipts.json','actual receipt filename')
        require(binding['source_receipt_sha256']==sha(s/'api-receipts.json'),'receipt binding')
        require(binding['source_ready_sha256']==sha(s/'SOURCE_READY.json'),'readiness binding')
        require(pub['version']=='1.1' and pub['publication_date']=='2026-10-21' and pub['pdf_pages']==8,'edition')
        require(pub['follow_up'] is None and prom['follow_up'] is None,'follow-up remains null')
        require(prom['status']=='PRIVATE_EDITORIAL_PREPARED_UNPUBLISHED','editorial state')
        for obj in [pub['review_metadata'],binding['publication_state'],prom,flags]:
            require(all(obj[k] is False for k in statekeys),'unpublished gate changed')
            require(all(obj[k] is None for k in nullkeys),'unverified canonical/AA changed')
        require(all(pub[k] is None for k in nullkeys),'top-level unverified canonical/AA')
        require(prom['root_clearance_sha256']==sha(a),'root hash')
        require(prom['all203_status']=='ONGOING','overall programme remains ongoing')
    contract(p,q)
    require(original==(E/'abstract-source.tex').read_text(),'complete original abstract substring')
    require(p['review_metadata']['completion_percent']==100,'editorial task incomplete')
    require(q['publication_sha256']==sha(B/'publication.json'),'promotion publication binding')
    require([x['original_api_file_object']['key'] for x in ready['all_assets_in_original_order']]==
            ['fixed-birational-cycle-nonlimit-verification.zip','fixed-birational-cycle-nonlimit.pdf'],'ZIP/PDF native order')
    require(len(receipts)==5 and all(x['HTTP_status']==200 for x in receipts),'native receipt list')
    for receipt in receipts:
        file_entry(receipt['body'])
        require(isinstance(receipt['response_headers_in_received_order'],list),'ordered original headers')
    for lane,item in root['reviews'].items():
        for role in ['report','verdict','seal']:
            require(sha(Path(item[role+'_path']))==item[role+'_sha256'],'original family binding')
        require(same(verdicts[lane],item['verdict_original']),'root whole literal custom verdict')
    copied=read(E/'ORIGINAL_OBJECT_COPIES.json')['objects']
    for item in copied:
        old=Path(item['original_path']); new=E/item['copy_path']
        require(sha(old)==item['sha256'] and old.read_bytes()==new.read_bytes(),'raw original object copy')
    protected=read(E/'PROTECTED_INPUTS.json')['files']
    for item in protected:
        file_entry(item)
    native_members=0
    archive=s/'fixed-birational-cycle-nonlimit-verification.zip'
    require(sha(archive)==p['source_binding']['supplement_sha256'],'complete original ZIP')
    with zipfile.ZipFile(archive) as z:
        for info in z.infolist():
            if info.is_dir():
                continue
            name=PurePosixPath(info.filename)
            require(not name.is_absolute() and '..' not in name.parts,'unsafe native member')
            require((s/'published-source'/info.filename).read_bytes()==z.read(info),'native extracted payload changed')
            native_members+=1
    require(native_members==69,'full native payload count')
    require(sha(s/p['pdf_filename'])==p['source_binding']['pdf_sha256'],'complete original PDF')
    for item in read(E/'PREPARED_CONFIG_COPIES.json')['configs']:
        f=Path(item['installed_private_path']);f2=E/item['prepared_copy_path']
        require(sha(f)==item['sha256'] and f.read_bytes()==f2.read_bytes(),'prepared private config copy')
    public=(E/'PUBLIC_COPY.md').read_text()
    for key in ['abstract','status','edition_note','ai_disclosure','collaboration']:
        require(p[key] in public,'public paragraph absent '+key)
    for key in ['plain_language','result','why_it_works','limitations']:
        require(all(v in public for v in p[key]),'public paragraph absent '+key)
    for item in p['background']:
        require(item['title'] in public and item['url'] in public and item['note'] in public,'public positive credit absent')
    require(all(x not in public for x in ['PASS_AT_DECLARED','147,619','46,298','/Users/alec/','8347742']),
            'private audit data in public copy')
    # Contract falsifiers mutate in-memory copies only; no original/config files are edited.
    mutations=[
        lambda x,y:x.__setitem__('abstract',x['abstract'].split('.')[0]),
        lambda x,y:x['result'].__setitem__(0,x['result'][0].replace('T_p(z)/p','T_p(z)/p²')),
        lambda x,y:x['limitations'].pop(),
        lambda x,y:x['result'].__setitem__(3,x['result'][3].replace('upper','natural')),
        lambda x,y:x['result'].__setitem__(4,x['result'][4].replace('Ω_p','F_p²')),
        lambda x,y:x['result'].__setitem__(5,x['result'][5].replace('bounded continuous','unbounded')),
        lambda x,y:x.__setitem__('code_license','MIT'),
        lambda x,y:y.__setitem__('scientific_status','PASS'),
        lambda x,y:y['whole_root_scientific_clearance_record'].__setitem__('status','PASS'),
        lambda x,y:x['source_binding']['all_assets_in_original_order'].reverse(),
        lambda x,y:x['source_binding']['whole_native_record'].__setitem__('swh',None),
        lambda x,y:y['whole_root_scientific_clearance_record'].__setitem__('substantive_defect',{}),
        lambda x,y:x['review_metadata'].__setitem__('ready_to_publish',True),
        lambda x,y:x.__setitem__('canonical_url',x['proposed_canonical_url']),
        lambda x,y:x.__setitem__('prepared_bibtex',x['prepared_bibtex'].replace('23539734','23539733')),
        lambda x,y:y.__setitem__('follow_up','An unreviewed question')]
    rejected=0
    for mutate in mutations:
        x,y=copy.deepcopy(p),copy.deepcopy(q);mutate(x,y)
        try:
            contract(x,y)
        except RuntimeError:
            rejected+=1
        else:
            raise RuntimeError('negative control was accepted')
    require(rejected==16,'negative control count')
    sealhash=None
    if args.require_seal:
        seal=read(E/'SEAL.json');manifest=read(E/'MANIFEST.json')
        require(sha(E/'MANIFEST.json')==seal['manifest_sha256'],'manifest seal binding')
        require(sha(B/'publication.json')==seal['publication_sha256'],'sealed publication')
        require(sha(B/'promotion.json')==seal['promotion_sha256'],'sealed promotion')
        for item in manifest['files']:
            file_entry({'path':str(E/item['path']),'bytes':item['bytes'],'sha256':item['sha256']})
        actual={str(f.relative_to(E)) for f in E.rglob('*') if f.is_file()}
        expected={x['path'] for x in manifest['files']}|{'MANIFEST.json','SEAL.json'}
        require(actual==expected,'owned sealed inventory')
        require(seal['completion_percent']==100,'seal incomplete')
        sealhash=sha(E/'SEAL.json')
    print(json.dumps({'status':'PASS_PRIVATE_EDITORIAL_CONTRACT','readonly':True,'file_writes':False,
                      'negative_controls_rejected':rejected,'raw_original_object_copies':len(copied),
                      'protected_original_files':len(protected),'original_native_payloads':native_members,
                      'rendered':False,'deployed':False,'public_page_published':False,
                      'canonical_url':None,'AA':None,'seal_sha256':sealhash},sort_keys=True))


if __name__=='__main__':
    main()
