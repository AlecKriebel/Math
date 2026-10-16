"""Independent standard-library fixed-package and safe ZIP identity audit."""
from pathlib import Path, PurePosixPath
import hashlib, json, stat, zipfile

ROOT = Path(__file__).resolve().parent
PACKAGE = ROOT.parent / 'publication_package_v1'

def need(condition, message):
    if not condition:
        raise RuntimeError(message)

def pin(data):
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}

def main():
    names = json.loads((PACKAGE / 'SAFE_ALLOWLIST.json').read_bytes())['safe_authored_files']
    need(len(names) == 14 and len(set(names)) == 14, 'top count/duplicates')
    need(set(names) == {p.name for p in PACKAGE.iterdir()}, 'top exact names')
    top = {name: pin((PACKAGE / name).read_bytes()) for name in names}
    need(top['PACKAGE_SEAL.json'] == {'bytes': 2727, 'sha256': '6498125474c6e7c3da00cdc3d1b5b8c6c90223f005da3aa6f2ed946c768067e1'}, 'external seal')
    seal = json.loads((PACKAGE / 'PACKAGE_SEAL.json').read_bytes())
    need(seal['safe_files'] == {k:v for k,v in top.items() if k != 'PACKAGE_SEAL.json'}, 'seal closure')
    out = ROOT / 'private' / 'extracted'
    need(not out.exists(), 'fresh private extraction required')
    out.mkdir(parents=True)
    members = {}
    with zipfile.ZipFile(PACKAGE / 'verification-package.zip') as z:
        infos = z.infolist()
        need(len(infos) == 71, 'ZIP count')
        for info in infos:
            name = info.filename
            p = PurePosixPath(name)
            need(name not in members, 'duplicate ZIP name')
            need(not p.is_absolute() and '..' not in p.parts and '\\' not in name, 'path unsafe')
            mode = info.external_attr >> 16
            need(not stat.S_ISLNK(mode) and not info.is_dir(), 'symlink/directory')
            need(not info.flag_bits & 1, 'encrypted member')
            data = z.read(info)
            members[name] = pin(data)
            target = out / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        need(z.testzip() is None, 'CRC failure')
    inv = json.loads((out / 'ARCHIVE_INVENTORY.json').read_bytes())
    need(inv['files'] == {k:v for k,v in members.items() if k != 'ARCHIVE_INVENTORY.json'}, 'inventory exact closure')
    need((out / 'ARCHIVE_INVENTORY.json').read_bytes() == (PACKAGE / 'ARCHIVE_INVENTORY.json').read_bytes(), 'inventory duplicate')
    common = sorted(set(top) & set(members))
    need(all(top[n] == members[n] for n in common), 'top/archive mismatch')
    need(len([n for n in members if n.startswith('original_submitted_head/')]) == 19, 'original count')
    result = {'verdict':'PASS_IDENTITIES_AND_SAFE_EXTRACTION', 'top_files':top, 'zip_members':members,
              'top_archive_identical_names':common, 'archive_count':len(members),
              'inventory_count':len(inv['files']), 'original_submitted_count':19,
              'crc_all_pass':True, 'safe_paths_and_types':True,
              'note':'No script from the package was executed by this audit.'}
    (ROOT / 'PACKAGE_IDENTITY_RECEIPT.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['top_files','zip_members']}, indent=2))

if __name__ == '__main__':
    main()
