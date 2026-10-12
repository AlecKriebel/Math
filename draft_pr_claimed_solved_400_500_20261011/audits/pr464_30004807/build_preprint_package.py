#!/usr/bin/env python3
"""Build only positively selected, hash-checked PR464 archive payloads."""
import argparse, datetime, hashlib, json, zipfile
from pathlib import Path, PurePosixPath
ROOT=Path(__file__).resolve().parent
PACKAGE=ROOT/'package'
FORBIDDEN={'private_sources','private_cases','mutation_fixtures','.secrets','.zenodo-state','__pycache__','venv','.venv'}
def require(ok,msg):
    if not ok: raise RuntimeError(msg)
def sha(b): return hashlib.sha256(b).hexdigest()
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
    (PACKAGE/'SHA256SUMS.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
    archive=PACKAGE/'regular_zas_bianchi_verification_v1.zip'
    with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED) as z:
        for n in sorted([*names,'SHA256SUMS.json']):
            i=zipfile.ZipInfo(n,(2026,10,12,0,0,0));i.compress_type=zipfile.ZIP_DEFLATED;i.external_attr=0o100644<<16;z.writestr(i,selected_path(n).read_bytes())
    with zipfile.ZipFile(archive) as z:
        require(z.testzip() is None,'Archive CRC failure')
        require(set(z.namelist())==set(names)|{'SHA256SUMS.json'},'Archive selection drift')
        for n,e in files.items():require(sha(z.read(n))==e['sha256'] and len(z.read(n))==e['bytes'],'Archive readback byte drift')
        require(z.read('SHA256SUMS.json')==selected_path('SHA256SUMS.json').read_bytes(),'Manifest readback drift')
    receipt={'built_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'archive':archive.name,'sha256':sha(archive.read_bytes()),'bytes':archive.stat().st_size,'file_count':len(names)+1,'payload_count':len(names),'selection':'explicit whitelists only','readback':'all payload SHA256/sizes, exact entry set and CRC verified'}
    (PACKAGE/'ARCHIVE_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
    metadata=json.loads(selected_path('metadata.json').read_text())
    deposit={'metadata':metadata,'files':[{'path':'manuscript.pdf','name':'regular_zas_bianchi_defect.pdf'},{'path':archive.name}]}
    (PACKAGE/'deposit.json').write_text(json.dumps(deposit,indent=2)+'\n')
    install_names=sorted([*names,'SHA256SUMS.json','manuscript.pdf',archive.name,'ARCHIVE_RECEIPT.json','deposit.json'])
    entries=[{'local_program_path':str(selected_path(n).relative_to(ROOT.parent.parent.parent)),'repository_destination':'unsolved_math_prioritization/attempts/30004807/preprint_20261012/'+n,'sha256':sha(selected_path(n).read_bytes()),'bytes':selected_path(n).stat().st_size} for n in install_names]
    (ROOT/'BRANCH_INSTALL_PLAN.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'positive_selection_only':True,'entries':entries},indent=2)+'\n')
    if args.freeze is not None:
        require(args.freeze>0,'Invalid review round')
        f=ROOT/f'PACKAGE_REVIEW_INPUT_{args.freeze}.json';require(not f.exists(),'Never overwrite a frozen review input')
        top=['README.md','manuscript.tex','manuscript.pdf','metadata.json','SHA256SUMS.json',archive.name,'ARCHIVE_RECEIPT.json','deposit.json']
        freeze={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pr':464,'problem':'30004807','original_head':'97b2ed225574ca61bd03cb8db021a533e04938dc','files':{n:{'sha256':sha(selected_path(n).read_bytes()),'bytes':selected_path(n).stat().st_size} for n in top},'source_receipt_sha256':sha((ROOT/'SOURCE_RECEIPT.json').read_bytes()),'mathematical_acceptance_gate_sha256':sha((ROOT/'MATHEMATICAL_ACCEPTANCE_GATE.json').read_bytes()),'branch_install_plan_sha256':sha((ROOT/'BRANCH_INSTALL_PLAN.json').read_bytes()),'archive_contains_explicit_payload_manifest':True,'publication_not_yet_authorized_by_review_gate':True}
        f.write_text(json.dumps(freeze,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))
if __name__=='__main__':main()
