import hashlib, io, json, pathlib, stat, sys, zipfile

def fail(msg): raise ValueError(msg)
def digest(b): return hashlib.sha256(b).hexdigest()
def require(ok,msg):
    if not ok: fail(msg)
def unique(pairs):
    d={}
    for k,v in pairs:
        require(k not in d,'duplicate JSON key');d[k]=v
    return d

def check_payload(archive_bytes, entries):
    require(len({x['path'] for x in entries})==len(entries),'duplicate manifest path')
    expected={x['path']:x for x in entries}
    with zipfile.ZipFile(io.BytesIO(archive_bytes)) as z:
        names=z.namelist();require(len(names)==len(set(names)),'duplicate ZIP member')
        require(set(names)==set(expected),'strict ZIP inventory mismatch')
        require(z.testzip() is None,'CRC error')
        for info in z.infolist():
            name=info.filename;p=pathlib.PurePosixPath(name)
            require(not p.is_absolute() and '..' not in p.parts and '\\' not in name and str(p)==name,'unsafe ZIP path')
            require(not info.is_dir(),'directories not allowed')
            mode=info.external_attr>>16
            require(not stat.S_ISLNK(mode),'symlink not allowed')
            require(mode&0o111==0,'executable mode not allowed')
            require(p.suffix in {'.md','.json','.patch'},'unexpected file type')
            b=z.read(info);text=b.decode('utf-8');require('\x00' not in text,'binary text')
            require(len(b)==expected[name]['bytes'],'member byte mismatch')
            require(digest(b)==expected[name]['sha256'],'member hash mismatch')
            if p.suffix=='.json':json.loads(text,object_pairs_hook=unique)
    return len(entries)

def check_archive(archive,manifest,expected_archive_sha,expected_manifest_sha):
    before={p:(p.read_bytes(),p.stat().st_size,p.stat().st_mtime_ns,p.stat().st_mode) for p in [archive,manifest]}
    a=before[archive][0];m=before[manifest][0]
    require(digest(a)==expected_archive_sha,'archive pin mismatch')
    require(digest(m)==expected_manifest_sha,'external manifest pin mismatch')
    spec=json.loads(m,object_pairs_hook=unique)
    require(len(a)==spec['archive_bytes'],'archive bytes mismatch')
    require(digest(a)==spec['archive_sha256'],'archive manifest digest mismatch')
    count=check_payload(a,spec['files'])
    after={p:(p.read_bytes(),p.stat().st_size,p.stat().st_mtime_ns,p.stat().st_mode) for p in [archive,manifest]}
    require(before==after,'input mutation')
    return {'archive':archive.name,'bytes':len(a),'sha256':digest(a),'manifest_sha256':digest(m),'member_count':count,'strict_inventory':True,'crc':True,'all_utf8_text':True,'no_executable_members':True,'input_immutable':True}


PINNED = [{'archive': 'ISOCRYSTAL_MONODROMY_30002618_AUTHOR_SAFE_FREEZE.zip', 'manifest': 'ISOCRYSTAL_MONODROMY_30002618_AUTHOR_EXTERNAL_MANIFEST.json', 'archive_sha256': '0947c56eb1d4642ac9e92298022a21419aac91a740d1b0ee4ace588260dd2665', 'manifest_sha256': '7a348b1bc2d5430ec84c790cf1758974227502220f902eea478a93f7cdc681ea'}, {'archive': 'ISOCRYSTAL_MONODROMY_30002618_CORRECTED_SAFE.zip', 'manifest': 'ISOCRYSTAL_MONODROMY_30002618_CORRECTED_EXTERNAL_MANIFEST.json', 'archive_sha256': 'aa53b811b554fbd7655d4d18073c62ac49c65bcdc68dbf898f6e40e2286306d2', 'manifest_sha256': '9fb9ecf3d28d5961d48490ea17446afb0465bf34fdc97c326e629703ccab0461'}, {'archive': 'ISOCRYSTAL_MONODROMY_30002618_INDEPENDENT_AUDIT_SAFE.zip', 'manifest': 'ISOCRYSTAL_MONODROMY_30002618_INDEPENDENT_AUDIT_EXTERNAL_MANIFEST.json', 'archive_sha256': '98d9386a7b67b8dcb8c6de7ff57436dfd20342c9fb9dfb4f1941281d05f155a9', 'manifest_sha256': 'd41f4a6db4e4e161182e90f54c189b670a20334a2029e6877decf79fe48132c1'}]

if __name__ == "__main__":
    require(len(sys.argv) <= 2, "usage: bootstrap [artifact_directory]")
    root = pathlib.Path(sys.argv[1]) if len(sys.argv) == 2 else pathlib.Path.cwd()
    results = [check_archive(root / x["archive"], root / x["manifest"], x["archive_sha256"], x["manifest_sha256"]) for x in PINNED]
    print(json.dumps({"all_passed": True, "archives": results}, sort_keys=True, indent=2))
