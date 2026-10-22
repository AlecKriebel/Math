#!/usr/bin/env python3
"""PR280 read-only exact authenticated/public metadata, bytes, ZIP and DOI verification."""
import argparse
import json
from urllib.parse import quote, urlsplit
from urllib.request import Request, urlopen
import uuid
from ops_binding import *


def fetch(url):
    with urlopen(Request(url,headers={'User-Agent':'Math-publication-verification/1.0'}),timeout=60) as response:
        return response.read(),response.status,response.url


def public_metadata_projection(public, intended):
    metadata=dict(public['metadata'])
    resource=metadata.pop('resource_type',None)
    if (resource!={'type':intended['upload_type'],'subtype':intended['publication_type'],'title':'Preprint'}
            or 'upload_type' in metadata or 'publication_type' in metadata
            or metadata.get('license')!={'id':intended['license']}):
        raise RuntimeError('Unexpected public resource-type/license schema or identity')
    # The public API's observed representation is different from the deposition
    # API. Normalize only these exact two structural representations; all intended
    # values and every other metadata field still pass the existing verifier.
    metadata['upload_type']=resource['type']
    metadata['publication_type']=resource['subtype']
    metadata['license']=metadata['license']['id']
    return {**public,'metadata':metadata}


def verify_doi_destination(identifier,resolution):
    """Require the final canonical intended record, not status200 alone.

    This destination policy is stricter than conservative dedup URL leads:
    canonical plural record path only, no query/fragment, exact decimal ID.
    """
    if type(identifier) is not int or identifier<=0 or not isinstance(resolution,dict):
        raise RuntimeError('Malformed expected DOI destination identity')
    status=resolution.get('http_status');url=resolution.get('resolved_url')
    if (type(status) is not int or status!=200 or not isinstance(url,str) or not url
            or any(ord(c)<=32 or ord(c)==127 for c in url)):
        raise RuntimeError('Successful exact final DOI destination is missing')
    try:parsed=urlsplit(url)
    except ValueError as error:
        raise RuntimeError('Malformed final DOI destination') from error
    if (parsed.scheme!='https' or ascii_lower(parsed.netloc) not in {'zenodo.org','zenodo.org:443'}
            or parsed.username is not None or parsed.password is not None
            or parsed.path!='/records/'+str(identifier) or '?' in url or '#' in url):
        raise RuntimeError('DOI final URL is not the exact canonical intended HTTPS Zenodo record')
    return {'status':status,'resolved_url':url,'exact_expected_record_destination_verified':True,
            'expected_record':identifier,'policy':'HTTPS zenodo.org, optional exact443, canonical plural path, no query/fragment'}


def verify_public_record(identifier, metadata, selected, inspection, public, downloads, status):
    doi='10.5281/zenodo.'+str(identifier)
    if (inspection.get('id')!=identifier or inspection.get('state')!='published'
            or inspection.get('doi')!=doi or inspection.get('doi_url')!='https://doi.org/'+doi
            or inspection.get('doi_resolution',{}).get('http_status')!=200
            or status!=200 or int(public['id'])!=identifier or public['doi']!=doi):
        raise RuntimeError('Exact published record/DOI200 identity not verified')
    doi_destination=verify_doi_destination(identifier,inspection.get('doi_resolution'))
    # Compare every intended field on the public record as well as authenticated
    # inspection; only the existing tool's explicit normalizations are allowed.
    normalizations=zenodo.verify(public_metadata_projection(public,metadata),metadata,selected)
    normalizations += [{'field':'upload_type/publication_type','kind':'public_resource_type_type_subtype'},
                       {'field':'license','kind':'public_license_id_object'}]
    results=[]
    for entry in selected:
        name=entry['name']
        data,code,destination=downloads[name]
        if code!=200 or len(data)!=entry['size'] or sha(data)!=entry['sha256'] or hashlib.md5(data).hexdigest()!=entry['md5']:
            raise RuntimeError('Downloaded public bytes differ: '+name)
        result={'name':name,'bytes':len(data),'sha256':sha(data),'md5':entry['md5'],
                'http_status':code,'downloaded_and_matches_reviewed':True}
        if name.endswith('.zip'):
            result.update(check_zip(data))
        results.append(result)
    return {'timestamp':stamp(),'pr':280,'record':identifier,'doi':doi,'doi_url':'https://doi.org/'+doi,
        'title':metadata['title'],'version':metadata['version'],'release_manifest_sha256':RELEASE_SHA,
        'files':results,'all_public_file_bytes_match_reviewed':True,
        'all_intended_authenticated_and_public_metadata_verified':True,
        'metadata_normalizations':normalizations,'record_http_status':status,
        'doi_resolution':doi_destination,
        'read_only_remote_operations':True}


def verify_live(identifier):
    require_release_clearance()
    metadata,selected=manifest()
    inspection=zenodo.run(argparse.Namespace(command='inspect',manifest=PUBLICATION/'zenodo-deposit.json',
                                             sandbox=False,check_doi=True))
    # Inspection is GET-only but may refresh local saved DOI state in the existing tool.
    atomic_json(AUDIT/'ZENODO_PUBLISHED_INSPECTION.json',inspection)
    raw=PRIVATE/('public_files_'+uuid.uuid4().hex)
    raw.mkdir(parents=True)
    data,status,_=fetch('https://zenodo.org/api/records/'+str(identifier))
    atomic_bytes(raw/'record.json',data)
    public=json.loads(data)
    downloads={}
    for entry in selected:
        name=entry['name']
        downloads[name]=fetch('https://zenodo.org/records/'+str(identifier)+'/files/'+quote(name,safe='')+'?download=1')
        atomic_bytes(raw/name,downloads[name][0])
    receipt=verify_public_record(identifier,metadata,selected,inspection,public,downloads,status)
    require_release_clearance()
    receipt['raw_receipts']=str(raw)
    atomic_json(AUDIT/'ZENODO_PUBLIC_FILE_VERIFICATION.json',receipt)
    return receipt


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--deposit-id',required=True,type=int)
    args=parser.parse_args()
    print(json.dumps(verify_live(args.deposit_id),indent=2))


if __name__=='__main__':
    main()
