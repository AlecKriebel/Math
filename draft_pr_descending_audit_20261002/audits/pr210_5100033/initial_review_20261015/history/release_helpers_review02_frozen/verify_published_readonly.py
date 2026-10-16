"""Verify an existing published deposit; never stage or publish."""
import sys
if not __debug__ or sys.flags.optimize:
    raise RuntimeError('Release verification refuses optimized Python')
from pathlib import Path
from datetime import datetime,timezone
import json,subprocess,urllib.request
from release_binding import context,binding,unchanged,publication,verify_doi,acquire,exclusive_json,require


def verify_existing(R,PUB,CTX):
    if (PUB/'ZENODO_VERIFIED_PUBLICATION.json').exists():return publication(R,PUB,CTX)
    attempt=json.loads((PUB/'PUBLISH_ATTEMPT.json').read_text())
    require(attempt.get('release_binding')==binding(CTX),'Publication attempt belongs to another cleared release')
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    T=PUB/'private_transport/zenodo';T.mkdir(parents=True,exist_ok=True)
    tool=Path('/Users/alec/Documents/Math/zenodo_deposit_tool/zenodo.py')
    py='/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
    run=subprocess.run([py,'-B',str(tool),'inspect',str(R/'deposit.json'),'--check-doi'],capture_output=True,text=True,timeout=180)
    (T/(stamp+'-readonly-inspect-stdout.json')).write_text(run.stdout)
    (T/(stamp+'-readonly-inspect-stderr.txt')).write_text(run.stderr)
    require(run.returncode==0,'Read-only published inspection failed; no new publication request allowed')
    v=json.loads(run.stdout);unchanged(R,CTX)
    require(v.get('state')=='published' and v.get('id')==attempt['id'],'Existing deposit publication not confirmed')
    require(v.get('files')==CTX['expected_files'],'Provider file set differs from clearance')
    provider={'utc':datetime.now(timezone.utc).isoformat(),'submitted':True,'id':v['id'],'provider_metadata_MD5_and_size_verified':True,'record_role':'Dated provider-only confirmation before supplementary public SHA256 and DOI promotion checks','release_binding':binding(CTX),'tool_readback':v}
    (PUB/'ZENODO_PROVIDER_CONFIRMED_PUBLICATION.json').write_text(json.dumps(provider,indent=2)+'\n')
    downloads=[]
    try:
        require(v.get('doi')=='10.5281/zenodo.'+str(v['id']) and v.get('doi_url')=='https://doi.org/'+v['doi'] and v.get('record_url')=='https://zenodo.org/records/'+str(v['id']),'Invalid DOI/record identity')
        verify_doi(v)
        import hashlib
        for row in CTX['expected_files']:
            url=v['record_url']+'/files/'+row['name']+'?download=1'
            request=urllib.request.Request(url,headers={'User-Agent':'Math-Research-Publication-Verification/1.0'})
            with urllib.request.urlopen(request,timeout=60) as response:raw=response.read()
            require(len(raw)==row['size'] and hashlib.sha256(raw).hexdigest()==row['sha256'],'Actual public download SHA256/size mismatch')
            downloads.append({'file':row['name'],'bytes':len(raw),'sha256':row['sha256'],'actual_public_download_byte_hash_match':True})
    except Exception as e:
        (PUB/'PUBLICATION_VERIFICATION_PENDING.json').write_text(json.dumps(dict(utc=datetime.now(timezone.utc).isoformat(),submitted=True,id=v['id'],release_binding=binding(CTX),actual_public_downloads=downloads,error=str(e),recovery='Run this read-only verifier only; never restage or republish'),indent=2)+'\n')
        raise RuntimeError('Deposit is published; DOI/public SHA verification pending. Read-only recovery only.') from e
    unchanged(R,CTX)
    receipt={'utc':datetime.now(timezone.utc).isoformat(),'submitted':True,'metadata_and_files_verified':True,'id':v['id'],'doi':v['doi'],'doi_url':v['doi_url'],'record_url':v['record_url'],'metadata':CTX['metadata'],'files':CTX['expected_files'],'metadata_normalizations':v.get('metadata_normalizations',[]),'doi_resolution':v['doi_resolution'],'tool_postpublication_readback':v,'additional_actual_public_file_downloads':downloads,'additional_public_readback_error':None,'exact_reviewed_frozen_files_published':True,'single_publish_attempt':True,'release_binding':binding(CTX)}
    exclusive_json(PUB/'ZENODO_VERIFIED_PUBLICATION.json',receipt)
    return publication(R,PUB,CTX)


if __name__=='__main__':
    PUB=Path(__file__).resolve().parent;R=PUB.parent/'preprint'
    _RELEASE_LOCK=acquire(PUB);CTX=context(R)
    r=verify_existing(R,PUB,CTX)
    print(json.dumps({k:v for k,v in r.items() if k not in ['metadata','tool_postpublication_readback']},indent=2))
