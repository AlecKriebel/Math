from pathlib import Path,PurePosixPath
import hashlib,json,zipfile,stat
root=Path(__file__).resolve().parent
package=root.parent/'publication_package_v1'
checks=[]
def ck(label,condition):
    checks.append({'label':label,'passed':bool(condition)})
    if not condition:raise RuntimeError(label)
def record(data):return {'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
seal_path=package/'PACKAGE_SEAL.json';seal=json.loads(seal_path.read_text())
ck('supplied seal identity',record(seal_path.read_bytes())['sha256']=='0bbad9ab0d715f7e720183571986fa18e27d9c5c1133726cc8b806c5f571fec5')
files={str(p.relative_to(package)):record(p.read_bytes()) for p in package.rglob('*') if p.is_file() and p!=seal_path}
ck('exact full package inventory',files==seal['package_safe_files'])
ck('29 files excluding seal',len(files)==29)
ck('no filesystem symlinks',not any(p.is_symlink() for p in package.rglob('*')))
for name,rec in seal['upload_files'].items():ck('upload '+name,files[name]==rec)
ck('exact three upload files',set(seal['upload_files'])=={'outer_focal_period.pdf','outer_focal_period.tex','verification-package.zip'})
metadata=json.loads((package/'materials/metadata.json').read_text())
deposit=json.loads((package/'zenodo-deposit.json').read_text())
ck('all metadata identities',metadata==seal['metadata_exact']==deposit['metadata'])
ck('deposit file order and identity',[x['path'] for x in deposit['files']]==list(seal['upload_files']))
ck('TeX sources identical',(package/'outer_focal_period.tex').read_bytes()==(package/'materials/outer_focal_period.tex').read_bytes())
manifest=json.loads((package/'materials/MANIFEST.json').read_text())
materials={str(p.relative_to(package/'materials')):record(p.read_bytes()) for p in (package/'materials').rglob('*') if p.is_file() and p.name!='MANIFEST.json'}
ck('manifest all payload files excluding self',materials==manifest['files'])
with zipfile.ZipFile(package/'verification-package.zip') as z:
    names=z.namelist()
    ck('ZIP CRC and decompression',z.testzip() is None)
    ck('ZIP exact unique inventory',len(names)==len(set(names))==25)
    ck('ZIP exact seal inventory',{name:record(z.read(name)) for name in names}==seal['zip_entries'])
    ck('ZIP equals materials',{name:record(z.read(name)) for name in names}=={str(p.relative_to(package/'materials')):record(p.read_bytes()) for p in (package/'materials').rglob('*') if p.is_file()})
    for i in z.infolist():
        p=PurePosixPath(i.filename)
        ck('ZIP path safety '+i.filename,not p.is_absolute() and '..' not in p.parts and '\\' not in i.filename and not any(ord(c)<32 for c in i.filename))
        ck('ZIP no symlinks/encryption '+i.filename,not stat.S_ISLNK(i.external_attr>>16) and not i.flag_bits&1)
origins=json.loads((package/'materials/SOURCE_ORIGINS.json').read_text())
checkout=package.parents[4]
origin_results=[]
for name,rec in origins.items():
    source=checkout/rec['source_repository_path']
    # nearest checkout is the directory containing draft_pr_publication_program_20260930
    if not source.exists():
        for p in package.parents:
            candidate=p/rec['source_repository_path']
            if candidate.exists():source=candidate;break
    b=(package/'materials'/name).read_bytes()
    ck('origin expected bytes '+name,record(b)=={k:rec[k] for k in ['bytes','sha256']})
    ck('origin unaltered source '+name,source.exists() and b==source.read_bytes())
    origin_results.append({'payload':name,'source_exists':source.exists(),'identity':b==source.read_bytes()})
result={'status':'PASS','package_files_excluding_seal':len(files),'zip_entries':25,'checks':checks,'origins':origin_results,'seal_sha256':record(seal_path.read_bytes())['sha256'],'upload_files':seal['upload_files']}
(root/'PACKAGE_AUDIT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':'PASS','checks':len(checks),'files':len(files),'zip_entries':25,'origins':len(origins)},indent=2))
