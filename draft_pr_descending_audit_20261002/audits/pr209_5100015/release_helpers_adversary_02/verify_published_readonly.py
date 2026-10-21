"""Read-only verification of existing deposits. Importing performs no action."""
import sys
if not __debug__ or sys.flags.optimize:
    raise RuntimeError('Release verification refuses optimized Python')
from pathlib import Path
from datetime import datetime,timezone
import json,subprocess,urllib.request,hashlib
from release_binding import (context,binding,unchanged,publication,publication_lineage,verify_doi,
    acquire,exclusive_json,require,durable_mkdir,tool_publication,digest,pin,load)


def now():return datetime.now(timezone.utc).isoformat()


def fresh_folder(PUB,kind):
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    folder=Path(PUB)/'private_transport'/kind/stamp
    durable_mkdir(folder,exist_ok=False)
    return folder


def inspect_existing(R,CTX,record_id,folder):
    tool=Path('/Users/alec/Documents/Math/zenodo_deposit_tool/zenodo.py')
    py='/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
    try:run=subprocess.run([py,'-B',str(tool),'inspect',str(R/'deposit.json'),'--check-doi'],capture_output=True,text=True,timeout=180)
    except Exception as e:
        for suffix,value in [('stdout.json',getattr(e,'stdout',None)),('stderr.txt',getattr(e,'stderr',None))]:
            (folder/('inspect-'+suffix)).write_bytes(value if isinstance(value,bytes) else (value or '').encode())
        exclusive_json(folder/'INSPECT_EXCEPTION.json',{'utc':now(),'type':type(e).__name__,'error':str(e)})
        raise
    (folder/'inspect-stdout.json').write_text(run.stdout);(folder/'inspect-stderr.txt').write_text(run.stderr)
    require(run.returncode==0,'Read-only published inspection failed; no publication retry allowed')
    v=json.loads(run.stdout);tool_publication(v,CTX,record_id);unchanged(R,CTX)
    exclusive_json(folder/'INSPECT_READBACK.json',v)
    return v


def public_bytes(R,CTX,v,folder):
    require(v.get('doi')=='10.5281/zenodo.'+str(v['id']) and v.get('doi_url')=='https://doi.org/'+v['doi'] and v.get('record_url')=='https://zenodo.org/records/'+str(v['id']),'Invalid DOI/record identity')
    verify_doi(v)
    downloads=[]
    for row in CTX['expected_files']:
        url=v['record_url']+'/files/'+row['name']+'?download=1'
        request=urllib.request.Request(url,headers={'User-Agent':'Math-Research-Publication-Verification/1.0'})
        with urllib.request.urlopen(request,timeout=60) as response:raw=response.read()
        saved=folder/row['name'];saved.write_bytes(raw)
        # A failed payload is retained in full before its hash is checked.
        require(len(raw)==row['size'] and hashlib.sha256(raw).hexdigest()==row['sha256'],'Actual public download SHA256/size mismatch')
        downloads.append({'file':row['name'],'url':url,'bytes':len(raw),'sha256':row['sha256'],
            'payload':pin(saved,R.parent),'actual_public_download_byte_hash_match':True})
        exclusive_json(folder/('DOWNLOAD_'+str(len(downloads))+'.json'),downloads[-1])
    return downloads


def verify_existing(R,PUB,CTX):
    R=Path(R);PUB=Path(PUB)
    if (PUB/'ZENODO_VERIFIED_PUBLICATION.json').exists():return publication(R,PUB,CTX)
    publication_lineage(R,PUB,CTX)
    attempt=load(PUB/'PUBLISH_ATTEMPT.json');record_id=attempt['id']
    folder=fresh_folder(PUB,'zenodo_verification')
    try:
        v=inspect_existing(R,CTX,record_id,folder)
        shared={'release_binding':binding(CTX),'metadata':CTX['metadata'],'files':CTX['expected_files'],
            'id':record_id,'publish_attempt_sha256':digest(PUB/'PUBLISH_ATTEMPT.json')}
        tool_receipt=PUB/'ZENODO_TOOL_PUBLICATION_RECEIPT.json'
        if not tool_receipt.exists():
            exclusive_json(tool_receipt,dict(shared,utc=now(),source='read-only-recovery',tool_readback=v))
        else:
            t=load(tool_receipt)
            require(all(t.get(k)==value for k,value in shared.items()),'Retained tool publication lineage differs')
            tool_publication(t.get('tool_readback'),CTX,record_id)
        downloads=public_bytes(R,CTX,v,folder);unchanged(R,CTX)
        provider_path=PUB/'ZENODO_PROVIDER_CONFIRMED_PUBLICATION.json'
        if not provider_path.exists():
            provider=dict(shared,utc=now(),submitted=True,provider_metadata_MD5_and_size_verified=True,
                tool_publication_receipt_sha256=digest(tool_receipt),tool_readback=v)
            exclusive_json(provider_path,provider)
        else:
            provider=load(provider_path)
            require(all(provider.get(k)==value for k,value in shared.items()),'Retained provider publication lineage differs')
            tool_publication(provider.get('tool_readback'),CTX,record_id)
            verify_doi(provider['tool_readback'])
        v=provider['tool_readback']
        lineage=publication_lineage(R,PUB,CTX,complete=True)
        receipt={'utc':now(),'submitted':True,'metadata_and_files_verified':True,'id':record_id,
            'doi':v['doi'],'doi_url':v['doi_url'],'record_url':v['record_url'],'metadata':CTX['metadata'],
            'files':CTX['expected_files'],'metadata_normalizations':v.get('metadata_normalizations',[]),
            'doi_resolution':v['doi_resolution'],'tool_postpublication_readback':v,
            'additional_actual_public_file_downloads':downloads,'additional_public_readback_error':None,
            'exact_reviewed_frozen_files_published':True,'single_publish_attempt':True,
            'release_binding':binding(CTX),'lineage':lineage}
        exclusive_json(PUB/'ZENODO_VERIFIED_PUBLICATION.json',receipt)
        return publication(R,PUB,CTX)
    except Exception as e:
        pending={'utc':now(),'submitted':True,'id':record_id,'release_binding':binding(CTX),
            'error':str(e),'recovery':'Run read-only verification only; never restage or republish'}
        exclusive_json(folder/'PENDING.json',pending)
        if not (PUB/'PUBLICATION_VERIFICATION_PENDING.json').exists():exclusive_json(PUB/'PUBLICATION_VERIFICATION_PENDING.json',pending)
        raise RuntimeError('Deposit outcome retained; public verification pending. Read-only recovery only.') from e


def verify_publication_live(R,PUB,CTX):
    """Caller holds release lock; fresh actual provider/DOI/public bytes, no receipt replacement."""
    R=Path(R);PUB=Path(PUB);z=publication(R,PUB,CTX);before=digest(PUB/'ZENODO_VERIFIED_PUBLICATION.json')
    folder=fresh_folder(PUB,'zenodo_live')
    try:
        v=inspect_existing(R,CTX,z['id'],folder);downloads=public_bytes(R,CTX,v,folder)
        for key in ['id','doi','doi_url','record_url']:require(v.get(key)==z.get(key),'Live publication identity differs')
        unchanged(R,CTX);require(digest(PUB/'ZENODO_VERIFIED_PUBLICATION.json')==before,'Accepted publication changed during live validation')
        result={'utc':now(),'release_binding':binding(CTX),'publication_receipt_sha256':before,
            'id':z['id'],'doi_url':z['doi_url'],'doi_resolution':v['doi_resolution'],
            'inspect_readback':pin(folder/'INSPECT_READBACK.json',R.parent),'actual_public_file_downloads':downloads}
        exclusive_json(folder/'LIVE_VERIFIED.json',result)
        return result
    except Exception as e:
        exclusive_json(folder/'LIVE_PENDING.json',{'utc':now(),'error':str(e),'recovery':'Read-only reconciliation; no publication mutation'})
        raise


if __name__=='__main__':
    PUB=Path(__file__).resolve().parent;R=PUB.parent/'preprint'
    lock=acquire(PUB)
    try:
        CTX=context(R);r=verify_existing(R,PUB,CTX)
        print(json.dumps({k:v for k,v in r.items() if k not in ['metadata','tool_postpublication_readback']},indent=2))
    finally:lock.close()
