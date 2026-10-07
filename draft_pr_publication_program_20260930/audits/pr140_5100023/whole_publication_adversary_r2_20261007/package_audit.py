import datetime
import hashlib
import json
import pathlib
import zipfile

root=pathlib.Path(__file__).resolve().parent
package=pathlib.Path('/Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr85_30001203/isolated_main_integration_20261005/checkout/draft_pr_publication_program_20260930/audits/pr140_5100023/publication_package_v1')
def sha(body):return hashlib.sha256(body).hexdigest()
def check(ok,desc):
    if not ok:raise RuntimeError(desc)
manifest=json.loads((package/'PACKAGE_MANIFEST.json').read_text())
for row in manifest['members']:
    body=(package/row['relative']).read_bytes()
    check(len(body)==row['bytes'] and sha(body)==row['sha256'],row['relative'])
members={row['relative'] for row in manifest['members']}
actual={str(p.relative_to(package)) for p in package.rglob('*') if p.is_file()}
excluded={'PACKAGE_MANIFEST.json','antipedal_centroids_support.zip','antipedal_centroids.log'}
check(actual==members|excluded,'complete file census')
ziprows=[]
with zipfile.ZipFile(package/'antipedal_centroids_support.zip') as archive:
    check(archive.testzip() is None,'ZIP CRC')
    names=archive.namelist()
    check(len(names)==len(set(names))==26,'unique ZIP26')
    check(set(names)==(members-{'antipedal_centroids.pdf'})|{'PACKAGE_MANIFEST.json'},'ZIP census')
    for name in names:
        check(not pathlib.PurePosixPath(name).is_absolute() and '..' not in pathlib.PurePosixPath(name).parts,'ZIP path safety')
        body=archive.read(name)
        check(body==(package/name).read_bytes(),f'ZIP bytes {name}')
        ziprows.append(dict(path=name,bytes=len(body),sha256=sha(body)))
        if name.endswith(('.py','.md','.tex','.json','.txt')):
            check(b'/Users/' not in body and b'/home/' not in body,'private path in public '+name)
        check(not name.endswith('.pdf'),'third-party paper in ZIP')
verification=package/'verification'
vm=json.loads((verification/'MANIFEST.json').read_text())
vnames={row['relative'] for row in vm['members']}
check(len(vnames)==16,'verification16plusmanifest')
check({str(p.relative_to(verification)) for p in verification.rglob('*') if p.is_file()}==vnames|{'MANIFEST.json'},'verification census')
for row in vm['members']:
    body=(verification/row['relative']).read_bytes()
    check(len(body)==row['bytes'] and sha(body)==row['sha256'],'verification hash '+row['relative'])
metadata=json.loads((package/'metadata.json').read_text())
deposit=json.loads((package/'zenodo-deposit.json').read_text())
check(deposit['metadata']==metadata,'deposit metadata equality')
check([row['path'] for row in deposit['files']]==['antipedal_centroids.pdf','antipedal_centroids_support.zip'],'deposit intended files')
check(metadata['publication_type']=='preprint' and metadata['creators'][0]['orcid']=='0009-0001-9320-500X','publication metadata')
reproduction=json.loads((root/'fresh_reproduction/REPRODUCTION.json').read_text())
check(reproduction['status']=='PASS' and reproduction['positive_runs']==6 and reproduction['negative_runs_rejected']==8,'fresh reproduction verdict')
check(reproduction['all_children_reaped_and_groups_empty'],'fresh reproduction custody')
counts=[r['exact_conditions'] for r in reproduction['runs'] if r['outcome']=='PASS']
check(counts==[686292,686292,12846,12846,19,19],'fresh production counts')
result=dict(status='PASS',utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            package_files=len(actual),manifest_members=len(members),zip_members=len(ziprows),
            verification_files=len(vnames)+1,excluded_local_build_receipt='antipedal_centroids.log',
            zip_complete_bytes=True,duplicate_or_unsafe_members=False,third_party_papers_exported=False,
            local_private_paths_in_public_archive=False,deposit_metadata_equal=True,
            reproduction_counts=counts,zip_rows=ziprows)
(root/'PACKAGE_AUDIT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='zip_rows'}))
