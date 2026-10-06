"""Read-only anonymous full public metadata/files and exact DOI identity."""
from publication_guard import *
from run_zenodo_step import identity,require_published,inspected_publication
from urllib.parse import urlsplit
def public_argv(url):
    p=urlsplit(url);require(p.scheme=='https' and p.netloc in ('zenodo.org','doi.org') and not p.query and not p.fragment,'Exact public endpoint required')
    return ['/usr/bin/curl','-q','--fail','--silent','--show-error','--location','--proto','=https','--proto-redir','=https','--no-netrc','--header','Authorization:','--header','Cookie:','--max-time','50','--user-agent','Math-Zenodo-Deposit-Tool/1.0',url]

def fetch(label,url):
    out,result=execute(label,public_argv(url),OUT/'private_public_readback',parse_json=False)
    require(result['stderr']['logical_bytes']==0,'Public read stderr requires read-only reconciliation')
    return out,result

def compare_public_record(record,published):
    require_published(published);rid=published['id']
    identity(dict(id=record['id'],doi=record['doi'],doi_url=published['doi_url'],record_url=published['record_url']),True)
    require(record['id']==rid,'Public record identity differs')
    metadata=load(F/'record_metadata.json');remote=record['metadata']
    mapped={key:(remote['license']['id'] if key=='license' else remote['resource_type']['type'] if key=='upload_type' else remote['resource_type']['subtype'] if key=='publication_type' else remote[key]) for key in metadata}
    require(mapped==metadata,'Exact public metadata differs; reconcile representation rather than alter publication')
    require(remote['doi']==published['doi'] and len(record['files'])==2 and {x['key'] for x in record['files']}=={'spectral_tensor_consistency.pdf','spectral_tensor_verification.zip'},'Exact public files/DOI differ')
    for item in record['files']:
        require(item['links']['self']=='https://zenodo.org/api/records/'+str(rid)+'/files/'+item['key']+'/content','Public content endpoint differs')
    return record['files']

def verify_public_evidence(published):
    """Independently re-read every actual anonymous byte before tracker use."""
    require(inspected_publication()==published,'Confirmed inspected receipt changed')
    public=load(OUT/'PUBLIC_RECORD_VERIFICATION.json');rid=published['id']
    require(public['status']=='PASS_PUBLIC_RECORD_EXACT_METADATA_AND_BOTH_FULL_FILE_BYTES' and public['record_id']==rid and public['DOI']==published['doi'] and public['doi_url']==published['doi_url'] and public['record_url']==published['record_url'],'Exact public verification identity differs')
    require(public['all_reviewed_metadata_fields_exact'] is True and public['public_schema_mapping']==['license.id','resource_type.type','resource_type.subtype'],'Full metadata comparison declaration incomplete')
    raw,err,native=authenticate_execution('record',public_argv('https://zenodo.org/api/records/'+str(rid)),OUT/'private_public_readback')
    require(not err and public['actual_record_read']==native,'Actual anonymous record capture differs')
    items=compare_public_record(json.loads(raw),published)
    files=public['all_file_bytes'];require(type(files)==list and len(files)==2 and {x['name'] for x in files}=={x['key'] for x in items},'Complete public file evidence absent')
    for item in items:
        name=item['key'];b,err,native=authenticate_execution('file_'+name,public_argv(item['links']['self']),OUT/'private_public_readback')
        local=(F/name).read_bytes();digest=hashlib.md5(b).hexdigest()
        require(not err and b==local and len(b)==item['size'] and item['checksum']=='md5:'+digest,'Full public bytes/checksum differ from frozen candidate')
        row=next(x for x in files if x['name']==name)
        require(row==dict(name=name,bytes=len(b),sha256=sha(b),md5=digest,entire_public_download_equals_reviewed_file=True,actual_anonymous_native_process=native),'Full public file evidence differs from reconstructed actual download')
    require(public['doi_resolution']==published['doi_resolution'] and public['publication_state_confirmed_independently_of_resolver'] is True and public['no_individual_contacted'] is True,'Public receipt interpretation differs')
    return public

def main():
    lock=acquire();published=inspected_publication()
    rid=published['id'];api='https://zenodo.org/api/records/'+str(rid)
    raw,native=fetch('record',api);record=json.loads(raw)
    compare_public_record(record,published)
    files=[]
    for item in record['files']:
        name=item['key'];url=item['links']['self'];require(url=='https://zenodo.org/api/records/'+str(rid)+'/files/'+name+'/content','Public content endpoint differs')
        b,actual=fetch('file_'+name,url);local=(F/name).read_bytes()
        require(b==local and len(b)==item['size'] and item['checksum']=='md5:'+hashlib.md5(b).hexdigest(),'Entire public content differs')
        files.append(dict(name=name,bytes=len(b),sha256=sha(b),md5=hashlib.md5(b).hexdigest(),entire_public_download_equals_reviewed_file=True,actual_anonymous_native_process=actual))
    # DOI resolver availability is distinct from actual publication; the kit
    # retains its fresh optional resolver observation in the inspected receipt.
    clearance()
    result=dict(UTC=utc(),status='PASS_PUBLIC_RECORD_EXACT_METADATA_AND_BOTH_FULL_FILE_BYTES',record_id=rid,DOI=published['doi'],doi_url=published['doi_url'],record_url=published['record_url'],all_reviewed_metadata_fields_exact=True,public_schema_mapping=['license.id','resource_type.type','resource_type.subtype'],all_file_bytes=files,actual_record_read=native,doi_resolution=published['doi_resolution'],no_individual_contacted=True,publication_state_confirmed_independently_of_resolver=True)
    write(OUT/'PUBLIC_RECORD_VERIFICATION.json',result)
    verify_public_evidence(published)
    print(json.dumps({k:v for k,v in result.items() if k not in ('all_file_bytes','actual_record_read')},indent=2))
if __name__=='__main__':main()
