#!/usr/bin/env python3
"""Build only positively selected, hash-checked PR464 archive payloads."""
import argparse, datetime, hashlib, io, json, os, tempfile, zipfile
from pathlib import Path, PurePosixPath
ROOT=Path(__file__).resolve().parent
PACKAGE=ROOT/'package'
FORBIDDEN={'private_sources','private_cases','mutation_fixtures','.secrets','.zenodo-state','__pycache__','venv','.venv'}
def require(ok,msg):
    if not ok: raise RuntimeError(msg)
def sha(b): return hashlib.sha256(b).hexdigest()
def output_path(root,name,new=False):
    """Check owned unresolved output paths before any generated-file write."""
    require(not root.is_symlink() and root.resolve()==root,'Unsafe output root')
    rel=PurePosixPath(name)
    require(not rel.is_absolute() and rel.as_posix()==name and all(c not in {'','.', '..'} for c in rel.parts),'Noncanonical output path')
    p=root.joinpath(*rel.parts);cursor=root
    for part in rel.parts:
        cursor=cursor/part
        require(not cursor.is_symlink(),'Symlink in generated output path')
    require(p.resolve().is_relative_to(root) and p.parent.is_dir(),'Escaping or unavailable output parent')
    if new: require(not p.exists(),'Never overwrite a frozen review input')
    elif p.exists(): require(p.is_file() and p.stat().st_nlink==1,'Unsafe existing output file type or hard link')
    return p
def write_output(root,name,data,new=False):
    """Install complete bytes without following a replaced leaf or hard link.

    Individual replacements are atomic; the group is not a filesystem
    transaction or a lock against a hostile concurrent ancestor change.
    """
    destination=output_path(root,name,new)
    fd,tmp=tempfile.mkstemp(prefix='.'+destination.name+'-',dir=destination.parent)
    temporary=Path(tmp)
    try:
        with os.fdopen(fd,'wb') as stream: stream.write(data)
        os.chmod(temporary,0o644)
        output_path(root,name,new)
        if new: os.link(temporary,destination)  # complete, exclusive, never overwrites
        else: os.replace(temporary,destination)
    finally:
        temporary.unlink(missing_ok=True)

def selected_path(name):
    require(type(name) is str and name and "\\" not in name and not any(ord(c)<32 for c in name),'Invalid selected path representation')
    rel=PurePosixPath(name)
    require(not rel.is_absolute() and rel.as_posix()==name and all(c not in {'','.', '..'} for c in rel.parts),'Noncanonical selected archive path: '+name)
    require(not FORBIDDEN.intersection(rel.parts) and rel.suffix!='.pyc','Excluded selected archive path: '+name)
    require(not PACKAGE.is_symlink() and PACKAGE.resolve()==PACKAGE,'Unsafe package root')
    p=PACKAGE.joinpath(*rel.parts);cursor=PACKAGE
    for part in rel.parts:
        cursor=cursor/part
        require(not cursor.is_symlink(),'Symlink in selected archive path')
    require(p.resolve().is_relative_to(PACKAGE) and p.is_file(),'Selected file unavailable: '+name)
    return p

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--freeze',type=int);args=ap.parse_args()
    # Refuse an invalid/existing immutable freeze before changing ANY output.
    freeze_name=None
    if args.freeze is not None:
        require(args.freeze>0,'Invalid review round')
        freeze_name=f'PACKAGE_REVIEW_INPUT_{args.freeze}.json'
        output_path(ROOT,freeze_name,new=True)
    for n in ['SHA256SUMS.json','regular_zas_bianchi_verification_v1.zip','ARCHIVE_RECEIPT.json','deposit.json']:
        output_path(PACKAGE,n)
    output_path(ROOT,'BRANCH_INSTALL_PLAN.json')
    names=['README.md','CURRENT_PUBLICATION_NOTES.md','manuscript.tex','metadata.json','verification/PUBLIC_OUTPUT_WHITELIST.json','REVIEW_EVIDENCE_SELECTION.json']
    evidence=json.loads(selected_path('REVIEW_EVIDENCE_SELECTION.json').read_text())
    require(evidence['positive_explicit_selection'] is True,'Explicit review evidence selection absent')
    for e in evidence['entries']:
        p=selected_path(e['path']);require(sha(p.read_bytes())==e['sha256'] and p.stat().st_size==e['bytes'],'Review evidence byte drift');names.append(e['path'])
    white=json.loads(selected_path('verification/PUBLIC_OUTPUT_WHITELIST.json').read_text())
    require(white.get('positive_whitelist_only') is True,'Verification whitelist policy missing')
    for e in white['public_files']:
        n='verification/'+e['path'];p=selected_path(n)
        require(sha(p.read_bytes())==e['sha256'] and p.stat().st_size==e['bytes'],'Verification byte drift: '+n);names.append(n)
    require(len(names)==len(set(names)),'Duplicate archive payload path')
    files={n:{'sha256':sha(selected_path(n).read_bytes()),'bytes':selected_path(n).stat().st_size} for n in sorted(names)}
    manifest={'scope':'Exactly selected source, canonical metadata, authored review evidence and verification payloads. This manifest, the ZIP and the separate public PDF have no circular hashes.','files':files}
    write_output(PACKAGE,'SHA256SUMS.json',(json.dumps(manifest,indent=2,sort_keys=True)+'\n').encode())
    archive=PACKAGE/'regular_zas_bianchi_verification_v1.zip'
    buffer=io.BytesIO()
    with zipfile.ZipFile(buffer,'w',compression=zipfile.ZIP_DEFLATED) as z:
        for n in sorted([*names,'SHA256SUMS.json']):
            i=zipfile.ZipInfo(n,(2026,10,12,0,0,0));i.compress_type=zipfile.ZIP_DEFLATED;i.external_attr=0o100644<<16;z.writestr(i,selected_path(n).read_bytes())
    write_output(PACKAGE,archive.name,buffer.getvalue())
    with zipfile.ZipFile(archive) as z:
        require(z.testzip() is None,'Archive CRC failure')
        require(set(z.namelist())==set(names)|{'SHA256SUMS.json'},'Archive selection drift')
        for n,e in files.items():require(sha(z.read(n))==e['sha256'] and len(z.read(n))==e['bytes'],'Archive readback byte drift')
        require(z.read('SHA256SUMS.json')==selected_path('SHA256SUMS.json').read_bytes(),'Manifest readback drift')
    receipt={'built_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'archive':archive.name,'sha256':sha(archive.read_bytes()),'bytes':archive.stat().st_size,'file_count':len(names)+1,'payload_count':len(names),'selection':'explicit whitelists only','readback':'all payload SHA256/sizes, exact entry set and CRC verified'}
    write_output(PACKAGE,'ARCHIVE_RECEIPT.json',(json.dumps(receipt,indent=2)+'\n').encode())
    metadata=json.loads(selected_path('metadata.json').read_text())
    deposit={'metadata':metadata,'files':[{'path':'manuscript.pdf','name':'regular_zas_bianchi_defect.pdf'},{'path':archive.name}]}
    write_output(PACKAGE,'deposit.json',(json.dumps(deposit,indent=2)+'\n').encode())
    install_names=sorted([*names,'SHA256SUMS.json','manuscript.pdf',archive.name,'ARCHIVE_RECEIPT.json','deposit.json'])
    entries=[{'local_program_path':str(selected_path(n).relative_to(ROOT.parent.parent.parent)),'repository_destination':'unsolved_math_prioritization/attempts/30004807/preprint_20261012/'+n,'sha256':sha(selected_path(n).read_bytes()),'bytes':selected_path(n).stat().st_size} for n in install_names]
    write_output(ROOT,'BRANCH_INSTALL_PLAN.json',(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'positive_selection_only':True,'entries':entries},indent=2)+'\n').encode())
    if args.freeze is not None:
        top=['README.md','manuscript.tex','manuscript.pdf','metadata.json','SHA256SUMS.json',archive.name,'ARCHIVE_RECEIPT.json','deposit.json']
        freeze={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pr':464,'problem':'30004807','original_head':'97b2ed225574ca61bd03cb8db021a533e04938dc','files':{n:{'sha256':sha(selected_path(n).read_bytes()),'bytes':selected_path(n).stat().st_size} for n in top},'source_receipt_sha256':sha((ROOT/'SOURCE_RECEIPT.json').read_bytes()),'mathematical_acceptance_gate_sha256':sha((ROOT/'MATHEMATICAL_ACCEPTANCE_GATE.json').read_bytes()),'branch_install_plan_sha256':sha((ROOT/'BRANCH_INSTALL_PLAN.json').read_bytes()),'archive_contains_explicit_payload_manifest':True,'publication_not_yet_authorized_by_review_gate':True}
        write_output(ROOT,freeze_name,(json.dumps(freeze,indent=2)+'\n').encode(),new=True)
    print(json.dumps(receipt,indent=2))
if __name__=='__main__':main()
