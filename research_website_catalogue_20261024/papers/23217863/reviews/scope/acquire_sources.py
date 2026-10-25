"""Fresh public-source custody, recursive safe archive inspection; no source code execution."""
from pathlib import Path,PurePosixPath
from datetime import datetime,timezone
from io import BytesIO
import hashlib,json,os,stat,tarfile,urllib.request,zipfile
from pypdf import PdfReader
P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024');p=P/'papers/23217863';s=p/'sources';r=p/'reviews/scope'
now=lambda:datetime.now(timezone.utc).isoformat()
sha=lambda data:hashlib.sha256(data).hexdigest()
def dump(base,name,value):(base/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
assert not(s/'SOURCE_READY.json').exists()
api=json.loads((s/'record.raw.json').read_bytes());receipts=json.loads((s/'api-receipts.json').read_text())
assert api['id']==23217863 and api['metadata']['title']=='Ordinary Banach–Mazur rigidity of von Neumann algebras'
assert 'version'not in api['metadata']
prior=json.loads((P/'papers/23441617/reviews/editorial/custody.json').read_text())['earlier_owned_bindings'];ed=P/'papers/23441617/reviews/editorial'
for rel,b in json.loads((ed/'MANIFEST.json').read_text())['owned_output_bindings'].items():prior[str(P/'papers/23441617'/rel)]=b
for name in ['MANIFEST.json','SEAL.json','SEAL.sha256']:
    f=ed/name;prior[str(f)]={'bytes':f.stat().st_size,'sha256':sha(f.read_bytes())}
for path,b in prior.items():assert Path(path).stat().st_size==b['bytes'] and sha(Path(path).read_bytes())==b['sha256'],path
dump(r,'PRESERVATION_BEFORE.json',{'utc':now(),'owned_prior_bindings_only':prior,'stale_mutable_core_site_baselines_followed':False})
def fetch(url,target):
    start=now();request=urllib.request.Request(url,headers={'User-Agent':'IndependentResearchSourceCustody/1.0','Accept':'application/json' if target.suffix=='.json' else '*/*'})
    with urllib.request.urlopen(request,timeout=35) as response:
        data=response.read(48*1024*1024+1);headers=dict(response.headers.items());status=response.status;final=response.url
    if len(data)>48*1024*1024:raise ValueError('download_size_bound')
    target.write_bytes(data);receipts.append({'requested_url':url,'started_utc':start,'completed_utc':now(),'status':status,'final_url':final,'headers':headers,'path':str(target),'bytes':len(data),'sha256':sha(data)})
    dump(s,'api-receipts.json',receipts)
    if status!=200:raise ValueError('unexpected_public_response_status')
    return data
latest=json.loads(fetch('https://zenodo.org/api/records/23217863/versions/latest',s/'latest.raw.json'))
versions=json.loads(fetch('https://zenodo.org/api/records/23217863/versions',s/'versions.raw.json'))
assert latest['id']==api['id'] and latest['metadata']==api['metadata'] and latest['files']==api['files']
assets=[]
for obj in api['files']:
    name=obj['key']
    if not isinstance(name,str) or PurePosixPath(name).name!=name or name in ['', '.', '..'] or '\\'in name or '\x00'in name:raise ValueError('unsafe_API_filename')
    if any(x['original_api_file_object']['key']==name for x in assets):raise ValueError('duplicate_API_filename')
    url=obj['links']['self'];assert url.startswith('https://zenodo.org/api/records/23217863/files/')
    data=fetch(url,s/name);md5=hashlib.md5(data).hexdigest()
    assert len(data)==obj['size'] and obj['checksum']=='md5:'+md5
    assets.append({'original_api_file_object':obj,'path':str(s/name),'bytes':len(data),'md5':md5,'sha256':sha(data)})
members=[];containers=[];total_expanded=0
def canonical(name):
    if not isinstance(name,str) or '\\'in name or '\x00'in name or name.startswith('/') or ':'in name:raise ValueError('unsafe_archive_name:'+repr(name))
    value=name.rstrip('/')
    while value.startswith('./'):value=value[2:]
    parts=value.split('/')
    if not value or any(x in ['', '.', '..'] for x in parts):raise ValueError('noncanonical_archive_name:'+repr(name))
    return value
def kind(data,name):
    if zipfile.is_zipfile(BytesIO(data)):return 'zip'
    if name.lower().endswith(('.tar','.tar.gz','.tgz','.tar.bz2','.tar.xz')) or data[257:262]==b'ustar':
        with tarfile.open(fileobj=BytesIO(data),mode='r:*'):pass
        return 'tar'
    return None
def inspect(data,identifier,root,depth,archive_kind):
    global total_expanded
    if depth>6 or len(containers)>=20:raise ValueError('archive_depth_count_bound')
    root.mkdir(parents=True,exist_ok=True);containers.append({'container':identifier,'kind':archive_kind,'depth':depth,'bytes':len(data),'sha256':sha(data),'extraction_root':str(root)})
    seen=set();regular=[]
    if archive_kind=='zip':
        with zipfile.ZipFile(BytesIO(data)) as z:
            for info in z.infolist():
                mode=info.external_attr>>16
                if stat.S_ISLNK(mode) or stat.S_IFMT(mode) not in [0,stat.S_IFREG,stat.S_IFDIR]:raise ValueError('archive_nonregular_member')
                relative=canonical(info.filename)
                if relative in seen:raise ValueError('duplicate_archive_extraction_path')
                seen.add(relative)
                if info.is_dir():continue
                if info.flag_bits&1:raise ValueError('encrypted_archive_member')
                total_expanded+=info.file_size
                if total_expanded>40*1024*1024 or len(members)+len(regular)>5000:raise ValueError('expanded_archive_bound')
                content=z.read(info)
                regular.append((info.filename,relative,content,{'CRC32':format(info.CRC,'08x'),'compressed_bytes':info.compress_size}))
    else:
        with tarfile.open(fileobj=BytesIO(data),mode='r:*') as z:
            for info in z:
                if info.isdir() and info.name in ['.','./']:continue
                relative=canonical(info.name)
                if relative in seen:raise ValueError('duplicate_archive_extraction_path')
                seen.add(relative)
                if info.isdir():continue
                if not info.isfile():raise ValueError('tar_link_or_nonregular_member')
                total_expanded+=info.size
                if total_expanded>40*1024*1024 or len(members)+len(regular)>5000:raise ValueError('expanded_archive_bound')
                content=z.extractfile(info).read();regular.append((info.name,relative,content,{'tar_size':info.size}))
    for original,relative,content,extra in regular:
        target=root/relative;target.parent.mkdir(parents=True,exist_ok=True)
        if target.exists() or not target.resolve().is_relative_to(root.resolve()):raise ValueError('extraction_collision_or_escape')
        target.write_bytes(content);nested=kind(content,original)
        members.append({'container':identifier,'member':original,'extracted_path':str(target),'bytes':len(content),'sha256':sha(content),'safe_regular_member':True,'nested_archive':nested,**extra})
        if nested:
            # Qualified namespace retains distinct occurrences without overwriting outer files.
            nestedroot=s/'nested-source'/Path(identifier.replace('::','/'))/(relative+'.contents')
            inspect(content,identifier+'::'+original,nestedroot,depth+1,nested)
for item in assets:
    path=Path(item['path']);data=path.read_bytes();archive_kind=kind(data,path.name)
    if archive_kind:inspect(data,path.name,s/'published-source',0,archive_kind)
pdfs=[]
for item in assets:
    if item['original_api_file_object']['key'].lower().endswith('.pdf'):
        path=Path(item['path']);assert path.read_bytes().startswith(b'%PDF-');pdfs.append({'path':str(path),'bytes':item['bytes'],'sha256':item['sha256'],'pages':len(PdfReader(path).pages),'actual_standalone_API_asset':True})
assert len(pdfs)==1
tex=[]
for item in members:
    if item['member'].lower().endswith('.tex'):tex.append({k:item[k] for k in ['container','member','extracted_path','bytes','sha256']})
dump(s,'archive-members.json',{'utc':now(),'archive_containers':containers,'members':members,'regular_member_occurrences':len(members),'container_count':len(containers),'nested_archive_count':sum(x['depth']>0 for x in containers),'expanded_bytes_all_depths':total_expanded,'all_members_safely_read_and_extracted':True})
norm={'utc':now(),'derivative_not_raw_API':True,'record_id':api['id'],'conceptrecid':api['conceptrecid'],'metadata':api['metadata'],'version_field_present':False,'version_value':None,'created':api['created'],'updated':api['updated'],'latest_record_id':latest['id'],'all_original_API_file_objects':api['files'],'all_assets':assets,'all_TeX_candidates':tex}
dump(s,'normalized-metadata.json',norm)
ready={'utc':now(),'status':'SOURCE_READY_FRESH_COMPLETE_PUBLIC_OBJECTS_RECURSIVE_CUSTODY','record_id':23217863,'sheet_row':103,'title':api['metadata']['title'],'version_field_present':False,'version':None,'publication_date':api['metadata']['publication_date'],'created':api['created'],'updated':api['updated'],'doi':api['metadata']['doi'],'conceptrecid':api['conceptrecid'],'latest_record_id':latest['id'],'versions_total_original':versions.get('hits',{}).get('total'),'all_assets':assets,'actual_standalone_readers':pdfs,'selected_actual_PDF':pdfs[0],'regular_archive_member_occurrences':len(members),'archive_containers':len(containers),'nested_archives':sum(x['depth']>0 for x in containers),'expanded_bytes_all_depths':total_expanded,'all_TeX_candidates':tex,'local_candidate_used_instead_of_fresh_download':False,'historical_or_current_opinions_or_foreign_primary_bodies_read':False,'manuscript_mathematics_not_yet_read':True,'originals_now_immutable':True}
dump(s,'SOURCE_READY.json',ready)
files=[{'path':str(f.relative_to(s)),'bytes':f.stat().st_size,'sha256':sha(f.read_bytes())} for f in sorted(s.rglob('*')) if f.is_file()]
dump(s,'SOURCE_READY_MANIFEST.json',{'utc':now(),'status':'FROZEN_SOURCE_READY_ORIGINALS','file_count':len(files),'files':files})
dump(s,'SOURCE_READY_SEAL.json',{'utc':now(),'status':'SEALED_IMMUTABLE_SOURCE_READY','manifest':'SOURCE_READY_MANIFEST.json','manifest_sha256':sha((s/'SOURCE_READY_MANIFEST.json').read_bytes()),'SOURCE_READY_sha256':sha((s/'SOURCE_READY.json').read_bytes()),'original_bindings':len(files),'manuscript_or_primary_science_read':False})
with (r/'RESEARCH_LOG.md').open('a') as f:f.write(now()+' — Fresh record/latest/versions and all API assets authenticated; recursive archive custody complete, one actual reader selected. Metadata version absent/null retained. SOURCE_READY sealed before manuscript mathematics/history/primaries. Source acquisition100%; scientific review0%; all203 programme ongoing.\n')
print(json.dumps({'status':'SOURCE_READY','PDF':pdfs,'TeX_candidates':tex,'source_bindings':len(files),'regular_occurrences':len(members),'archive_containers':len(containers),'expanded_bytes':total_expanded,'SOURCE_READY_sha256':sha((s/'SOURCE_READY.json').read_bytes()),'manifest_sha256':sha((s/'SOURCE_READY_MANIFEST.json').read_bytes()),'seal_sha256':sha((s/'SOURCE_READY_SEAL.json').read_bytes())},indent=2,ensure_ascii=False))
