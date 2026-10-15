#!/usr/bin/env python3
"""Build a deterministic, explicitly allowlisted PR906 verification archive."""
from pathlib import Path, PurePosixPath
import hashlib
import json
import shutil
import stat
import zipfile

P=Path(__file__).resolve().parent
A=P.parent
ORIGINAL_PREFIX='unsolved_math_prioritization/attempts/30006419/'
PIN='acab12ef33c8e2dc566337cfe01b94f2fe81f06ede4b31f1c363e055741fb0df'

def require(ok,message):
    if not ok: raise RuntimeError(message)

def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def records(manifest):
    for key in ['files','intentional_public_files','artifacts']:
        if key in manifest: return manifest[key]
    if 'public_files' in manifest:
        return {r['path']:{'bytes':r['bytes'],'sha256':r['sha256']}
                for r in manifest['public_files']}
    raise RuntimeError('Unsupported public review manifest schema')

def main():
    bundle=P/'tmp/bundle'
    if bundle.exists():
        require(not bundle.is_symlink(),'Symlinked disposable bundle')
        shutil.rmtree(bundle)
    bundle.mkdir(parents=True)
    mapping={}
    def add(source,name,expected=None):
        q=PurePosixPath(name)
        require(not q.is_absolute() and q.as_posix()==name and
                all(x not in ('','.','..') for x in q.parts),'Unsafe output path')
        require(name not in mapping,'Duplicate payload: '+name)
        require(stat.S_ISREG(source.lstat().st_mode),'Nonregular input: '+str(source))
        if expected:
            require(source.stat().st_size==expected['bytes'] and digest(source)==expected['sha256'],
                    'Sealed artifact changed: '+str(source))
        # The only public file below a private-source directory is its declared ignore guard.
        require('private_sources' not in q.parts or q.name=='.gitignore','Raw source payload forbidden')
        dest=bundle/name;dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(source,dest);mapping[name]=dest
    snapshot=json.loads((A/'ORIGINAL_SNAPSHOT.json').read_text())
    for name,expected_sha in snapshot['files'].items():
        require(name.startswith(ORIGINAL_PREFIX),'Wrong original target')
        source=A/'original'/name
        require(digest(source)==expected_sha,'Original packet changed: '+name)
        add(source,'original_packet/'+name[len(ORIGINAL_PREFIX):])
    require(digest(bundle/'original_packet/PUBLIC_MANIFEST.json')==PIN,'Wrong external original pin')
    for family in ['reshetnyak_proof_family','ks_proof_family','computation_family',
                   'source_model_family','priority_family']:
        folder=A/'reviews'/family
        manifest=json.loads((folder/'MANIFEST.json').read_text())
        for name,record in records(manifest).items():
            add(folder/name,'reviews/'+family+'/'+name,record)
        add(folder/'MANIFEST.json','reviews/'+family+'/MANIFEST.json')
    for name in ['note.tex','README.md','requirements.txt','verify_package.py']:
        add(P/name,name)
    add(P/'output/pdf/note.pdf','note.pdf')
    for name in ['ORIGINAL_SNAPSHOT.json','PR_DESCRIPTION_ANCHOR.json',
                 'TARGET_IDENTITY_PREFLIGHT.json','PRIORITY_ACCESS_ADDENDUM.md',
                 'BIBLIOGRAPHIC_IDENTITIES.json','ROOT_PRIORITY_SOURCE_RECORD.json',
                 'ROOT_PRIORITY_QUERY_LOG.md']:
        add(A/name,name)
    data={'schema_version':1,'pr':906,'problem_id':'30006419',
          'original_pr_head':snapshot['head'],'original_public_manifest_sha256':PIN,
          'scope':'Authored PDF/source, unchanged historical packet, public reviews and source metadata only',
          'files':{name:{'bytes':path.stat().st_size,'sha256':digest(path)}
                   for name,path in sorted(mapping.items())}}
    manifest_path=bundle/'PACKAGE_MANIFEST.json'
    manifest_path.write_text(json.dumps(data,indent=2)+'\n')
    archive=P/'harmonic-sphere-source-verification-v1.0.zip'
    with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for name in sorted([*mapping,'PACKAGE_MANIFEST.json']):
            info=zipfile.ZipInfo(name,date_time=(2026,10,13,0,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED
            info.external_attr=0o100644<<16
            z.writestr(info,(bundle/name).read_bytes())
    receipt={'manifest_sha256':digest(manifest_path),'archive_sha256':digest(archive),
             'archive_bytes':archive.stat().st_size,'payload_files':len(mapping),
             'zip_members':len(mapping)+1,'original_files_unchanged':len(snapshot['files']),
             'authored_pdf_included':True,'raw_third_party_sources_included':False}
    (P/'BUILD_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))

if __name__=='__main__': main()
