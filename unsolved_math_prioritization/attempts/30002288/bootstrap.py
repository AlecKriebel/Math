#!/usr/bin/env python3
"""Externally trusted gate; python -I -S -B bootstrap.py ROOT MANIFEST_SHA [ENTRY]."""
import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):
    raise SystemExit('REJECT: require -I -S -B before any nonbuiltin import')
import hashlib, io, json, os, stat, tempfile, zipfile
from pathlib import Path, PurePosixPath
ANCHORS=[{'role': 'original', 'archive': {'filename': 'FRACTIONAL_INFINITY_30002288_AUTHOR_SAFE_FREEZE.zip', 'bytes': 12226, 'sha256': 'ba1f6ed2632036cb0e0efa1ce62e1c3824bb8c14e34e036e15c66402ec73d1d2'}, 'manifest': {'filename': 'FRACTIONAL_INFINITY_30002288_AUTHOR_EXTERNAL_MANIFEST.json', 'bytes': 1320, 'sha256': 'b3a70f59cb89dbc0d7e18ee845cd6ac31db9c3180e1ebc684b94890be418294d'}, 'members': ['PROOF.md', 'README.md', 'RESULTS.json', 'SOURCES.json', 'STATUS.json', 'verify_math.py'], 'bootstrap': {'filename': 'FRACTIONAL_INFINITY_30002288_AUTHOR_BOOTSTRAP.py', 'bytes': 2978, 'sha256': '3ee635186fde48045f97d08aebf2ea2802b56a9a96ff92d37c0335579250cb1b'}}, {'role': 'corrected', 'archive': {'filename': 'FRACTIONAL_INFINITY_30002288_CORRECTED_SAFE.zip', 'bytes': 12405, 'sha256': '4acbfd16b42c4d155ae422823d4ea4937d542b8a574ca781a13aa58fa9193ec8'}, 'manifest': {'filename': 'FRACTIONAL_INFINITY_30002288_CORRECTED_EXTERNAL_MANIFEST.json', 'bytes': 1346, 'sha256': 'cb29a9d6228fba9c1daffbe6ef6e8fccbe8281abce5d0e20964769ba3f0a413c'}, 'members': ['PROOF.md', 'README.md', 'RESULTS.json', 'SOURCES.json', 'STATUS.json', 'verify_math.py'], 'bootstrap': {'filename': 'FRACTIONAL_INFINITY_30002288_CORRECTED_BOOTSTRAP.py', 'bytes': 2978, 'sha256': 'e509bdc4ab88a6726574470df4a3a08e15ff865e2845e311d19caa4bb0b69490'}}, {'role': 'audit', 'archive': {'filename': 'FRACTIONAL_INFINITY_30002288_INDEPENDENT_AUDIT_SAFE.zip', 'bytes': 24056, 'sha256': 'abdde8edde1c008b74d60aa0b123f5aed962bb3381ff53de4f1ea66b996c73b0'}, 'manifest': {'filename': 'FRACTIONAL_INFINITY_30002288_INDEPENDENT_AUDIT_EXTERNAL_MANIFEST.json', 'bytes': 2423, 'sha256': '066b1eb0b6a641726370b58ec8500b927316260019afae4914dfbe9f1b07b059'}, 'members': ['ACCEPTANCE.json', 'ACCEPTANCE.md', 'AUTHOR_REPLAY_RESULTS.json', 'CORPUS_VERIFICATION.json', 'CORRECTED_REPLAY_RESULTS.json', 'INDEPENDENT_DIAGNOSTICS_RESULTS.json', 'MATHEMATICAL_AUDIT.md', 'PATCH_METADATA.json', 'README.md', 'SOURCE_VERIFICATION.json', 'VISCOSITY_TEST_CLASS.patch', 'independent_diagnostics.py', 'replay_author.py', 'replay_corrected.py'], 'bootstrap': {'filename': 'FRACTIONAL_INFINITY_30002288_INDEPENDENT_AUDIT_BOOTSTRAP.py', 'bytes': 3014, 'sha256': '9f664fd0b4d636a8b8ded07a3fb9a5500a8a2aeb838aa0b6c575ba3fad56e1b1'}}, {'role': 'review2', 'archive': {'filename': 'FRACTIONAL_INFINITY_30002288_SECOND_REVIEW_SAFE.zip', 'bytes': 15403, 'sha256': 'b70d94c31cc429b6276b8be910fa3feaf5297f21322f5142a07eadeafd056c48'}, 'manifest': {'filename': 'FRACTIONAL_INFINITY_30002288_SECOND_REVIEW_EXTERNAL_MANIFEST.json', 'bytes': 1671, 'sha256': '82014e876476df1118a4defc7e6c24271932fe2be805490810a4711f54322be8'}, 'members': ['CONTROL_RESULTS.json', 'DIAGNOSTIC_RESULTS.json', 'README.md', 'REVIEW.md', 'SEPARATE_ACCEPTANCE.json', 'SOURCE_CHECKS.json', 'VISCOSITY_TEST_CLASS.patch', 'review_diagnostics.py'], 'bootstrap': {'filename': 'FRACTIONAL_INFINITY_30002288_SECOND_REVIEW_BOOTSTRAP.py', 'bytes': 2487, 'sha256': '78eef318aa6f3bf2853357e82b86113ad3dc0688168d3f58c8207f8b7b8ffb90'}}, {'role': 'supplement', 'archive': {'filename': 'FRACTIONAL_INFINITY_30002288_SELECTION_ADDENDUM_V2_SAFE.zip', 'bytes': 3425, 'sha256': 'c83da041a8cc4caeb35308e7c531cdd510e5d83f8c9e8f5805541fe6495e0cd5'}, 'manifest': {'filename': 'FRACTIONAL_INFINITY_30002288_SELECTION_ADDENDUM_V2_MANIFEST.json', 'bytes': 811, 'sha256': '12af36746c3671d296a3b050951dc44deb0950b32371154a31275e2fb9894df1'}, 'members': ['SELECTION_LIMITS.md', 'STATUS_ADDENDUM.json']}]
FILES={'audit/ACCEPTANCE.json', 'archives/FRACTIONAL_INFINITY_30002288_INDEPENDENT_AUDIT_SAFE.zip', 'test_publication.py', 'review2/VISCOSITY_TEST_CLASS.patch', 'audit/AUTHOR_REPLAY_RESULTS.json', 'historical_bootstraps/FRACTIONAL_INFINITY_30002288_AUTHOR_BOOTSTRAP.py', 'audit/PATCH_METADATA.json', 'original/SOURCES.json', 'manifests/FRACTIONAL_INFINITY_30002288_INDEPENDENT_AUDIT_EXTERNAL_MANIFEST.json', 'corrected/SOURCES.json', 'review2/review_diagnostics.py', 'audit/INDEPENDENT_DIAGNOSTICS_RESULTS.json', 'original/verify_math.py', 'review2/CONTROL_RESULTS.json', 'PUBLICATION_TEST_RESULTS.json', 'README.md', 'historical_bootstraps/FRACTIONAL_INFINITY_30002288_SECOND_REVIEW_BOOTSTRAP.py', 'review2/README.md', 'manifests/FRACTIONAL_INFINITY_30002288_CORRECTED_EXTERNAL_MANIFEST.json', 'archives/FRACTIONAL_INFINITY_30002288_SECOND_REVIEW_SAFE.zip', 'historical_bootstraps/FRACTIONAL_INFINITY_30002288_CORRECTED_BOOTSTRAP.py', 'corrected/verify_math.py', 'verify_publication.py', 'audit/VISCOSITY_TEST_CLASS.patch', 'manifests/FRACTIONAL_INFINITY_30002288_AUTHOR_EXTERNAL_MANIFEST.json', 'PUBLICATION_METADATA.json', 'audit/replay_corrected.py', 'original/RESULTS.json', 'audit/replay_author.py', 'audit/ACCEPTANCE.md', 'corrected/STATUS.json', 'PUBLICATION_MANIFEST.json', 'supplement/STATUS_ADDENDUM.json', 'audit/README.md', 'corrected/RESULTS.json', 'manifests/FRACTIONAL_INFINITY_30002288_SELECTION_ADDENDUM_V2_MANIFEST.json', 'original/STATUS.json', 'audit/independent_diagnostics.py', 'original/README.md', 'corrected/PROOF.md', 'archives/FRACTIONAL_INFINITY_30002288_AUTHOR_SAFE_FREEZE.zip', 'test_packets.py', 'manifests/FRACTIONAL_INFINITY_30002288_SECOND_REVIEW_EXTERNAL_MANIFEST.json', 'original/PROOF.md', 'review2/REVIEW.md', 'isolated_runner.py', 'audit/CORPUS_VERIFICATION.json', 'corrected/README.md', 'bootstrap.py', 'audit/CORRECTED_REPLAY_RESULTS.json', 'review2/SEPARATE_ACCEPTANCE.json', 'review2/DIAGNOSTIC_RESULTS.json', 'review2/SOURCE_CHECKS.json', 'archives/FRACTIONAL_INFINITY_30002288_SELECTION_ADDENDUM_V2_SAFE.zip', 'RESEARCH_LOG.md', 'archives/FRACTIONAL_INFINITY_30002288_CORRECTED_SAFE.zip', 'audit/MATHEMATICAL_AUDIT.md', 'supplement/SELECTION_LIMITS.md', 'audit/SOURCE_VERIFICATION.json', 'historical_bootstraps/FRACTIONAL_INFINITY_30002288_INDEPENDENT_AUDIT_BOOTSTRAP.py'}
DIRS={'historical_bootstraps', 'supplement', 'archives', 'review2', 'corrected', 'original', 'manifests', 'audit'}
def need(ok,message):
    if not ok:raise ValueError(message)
def digest(b):return hashlib.sha256(b).hexdigest()
def unique(pairs):
    out={}
    for k,v in pairs:need(k not in out,'duplicate JSON key');out[k]=v
    return out
def js(b):return json.loads(b,object_pairs_hook=unique)
def ordinary_path(value,directory):
    path=Path(value)
    need(path.is_absolute() and '..' not in path.parts,'absolute lexical path without traversal required')
    for p in path.parents:need(stat.S_ISDIR(p.lstat().st_mode),'symlink/non-directory ancestry')
    mode=path.lstat().st_mode
    need(stat.S_ISDIR(mode) if directory else stat.S_ISREG(mode),'nonregular entrypoint or root')
    return path
def read_regular(path):
    st=path.lstat();need(stat.S_ISREG(st.st_mode) and st.st_nlink==1,'nonregular or hardlinked payload')
    fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW)
    try:
        actual=os.fstat(fd);need(stat.S_ISREG(actual.st_mode) and actual.st_nlink==1 and (actual.st_dev,actual.st_ino)==(st.st_dev,st.st_ino),'entry changed during read')
        with os.fdopen(fd,'rb',closefd=False) as src:data=src.read()
    finally:os.close(fd)
    return data
def snapshot(value,pin):
    root=ordinary_path(value,True);paths={};dirs=set()
    for current,ds,fs in os.walk(root,followlinks=False):
        for n in ds+fs:
            p=Path(current)/n;rel=p.relative_to(root).as_posix();mode=p.lstat().st_mode
            if stat.S_ISDIR(mode):dirs.add(rel)
            else:need(stat.S_ISREG(mode),'nonregular payload: '+rel);paths[rel]=p
    need(dirs==DIRS and set(paths)==FILES,'strict inventory mismatch')
    data={n:read_regular(p) for n,p in paths.items()}
    raw=data['PUBLICATION_MANIFEST.json'];need(digest(raw)==pin,'external publication manifest pin mismatch');m=js(raw)
    need(type(m) is dict and set(m)=={'schema','files'} and m['schema']=='fractional-infinity-publication-sha256-v1','publication schema')
    need(type(m['files']) is dict and set(m['files'])==FILES-{'PUBLICATION_MANIFEST.json'},'manifest inventory')
    for n,record in m['files'].items():
        need(type(record) is dict and set(record)=={'bytes','sha256'} and type(record['bytes']) is int and record['bytes']>=0,'manifest record schema')
        need(record=={'bytes':len(data[n]),'sha256':digest(data[n])},'payload hash mismatch: '+n)
    for anchor in ANCHORS:
        role=anchor['role'];names=set(anchor['members'])
        for label,directory in [('archive','archives'),('manifest','manifests'),('bootstrap','historical_bootstraps')]:
            if label not in anchor:continue
            r=anchor[label];b=data[directory+'/'+r['filename']]
            need((len(b),digest(b))==(r['bytes'],r['sha256']),'immutable '+label+' pin mismatch')
        ar=data['archives/'+anchor['archive']['filename']];mr=data['manifests/'+anchor['manifest']['filename']]
        entries=js(mr)['files'];need(set(entries)==names,'frozen manifest inventory')
        with zipfile.ZipFile(io.BytesIO(ar)) as z:
            infos=z.infolist();need(len(infos)==len(names) and set(z.namelist())==names,'archive inventory')
            need(z.testzip() is None,'archive CRC')
            for info in infos:
                n=info.filename;p=PurePosixPath(n)
                need(p.name==n and not p.is_absolute() and stat.S_ISREG(info.external_attr>>16) and not info.is_dir(),'archive member type/path')
                b=data[role+'/'+n];need(z.read(info)==b,'archive/member byte mismatch')
                need(entries[n]=={'bytes':len(b),'sha256':digest(b)},'frozen manifest/member mismatch')
    return data

def main():
    ordinary_path(str(Path(__file__).absolute()),False)
    need(3<=len(sys.argv)<=4,'usage: ROOT EXTERNAL_MANIFEST_SHA [verify_publication.py|test_publication.py|integrity]')
    root,pin=sys.argv[1:3];entry=sys.argv[3] if len(sys.argv)==4 else 'verify_publication.py'
    need(entry in {'verify_publication.py','test_publication.py','integrity'},'unsupported entrypoint')
    data=snapshot(root,pin)
    if entry=='integrity':print(json.dumps({'status':'PASS','files':len(data),'archives':5,'archive_members':36},sort_keys=True,indent=2));return
    # Execute verified bytes in a private snapshot, never a second read from input.
    with tempfile.TemporaryDirectory(prefix='fractional infinity validated ') as td:
        copied=Path(td)/'package';copied.mkdir()
        for name,b in data.items():p=copied/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
        sys.argv=[str(copied/entry),'--expected-manifest',pin]
        exec(compile(data[entry],str(copied/entry),'exec'),{'__name__':'__main__','__file__':str(copied/entry)})
if __name__=='__main__':
    try:main()
    except Exception as e:print('REJECT: '+str(e),file=sys.stderr);sys.exit(1)
