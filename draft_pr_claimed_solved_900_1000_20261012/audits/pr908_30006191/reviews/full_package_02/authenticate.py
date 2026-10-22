#!/usr/bin/env python3
"""Independent read-only authentication of the assigned PR908 candidate."""
from pathlib import Path, PurePosixPath
import datetime, hashlib, json, stat, subprocess, sys, zipfile

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parents[1]
REPO = AUDIT.parents[2]
PUB = AUDIT / 'publication'
HEAD = 'a35667b1bb0bafed69916709997a4684223ecc93'
FREEZE = '805791b8ec0fc6e15f7cc707ca77d49cfd904d447ceeed637d7bce181f924ce4'
ARCHIVE = 'ba0001722eafc6aea46aee6e85106895378481f2f827124c4acea282fb9d6495'
PACKAGE = 'eff4b4b19c1d931d3f067af7261c315a33452b732ba1c647163e3995804f5b39'

def require(ok, label):
    if not ok: raise RuntimeError(label)

def sha(b): return hashlib.sha256(b).hexdigest()

def read(path):
    require(stat.S_ISREG(path.lstat().st_mode), 'not regular '+str(path))
    return path.read_bytes()

def main():
    phase = sys.argv[1]
    raw = read(PUB/'PREPUBLICATION_FREEZE.json')
    require(sha(raw) == FREEZE, 'freeze anchor')
    frozen = json.loads(raw)
    require(len(frozen['files']) == 13, 'frozen count')
    for p,r in frozen['files'].items():
        b=read(PUB/p)
        require(len(b)==r['bytes'] and sha(b)==r['sha256'], 'freeze '+p)
    archive=PUB/'bounded-region-fermions-source-verification-v1.0.zip'
    require(sha(read(archive))==ARCHIVE, 'archive anchor')
    with zipfile.ZipFile(archive) as z:
        names=z.namelist()
        require(len(names)==len(set(names))==110, 'duplicate/wrong ZIP entries')
        for i in z.infolist():
            p=PurePosixPath(i.filename)
            require(not p.is_absolute() and p.as_posix()==i.filename and '..' not in p.parts, 'unsafe ZIP')
            require(stat.S_IFMT(i.external_attr >> 16) in (0,stat.S_IFREG), 'nonfile ZIP')
        pm=z.read('PACKAGE_MANIFEST.json')
        require(sha(pm)==PACKAGE, 'manifest anchor')
        records=json.loads(pm)['files']
        require(len(records)==109 and set(names)==set(records)|{'PACKAGE_MANIFEST.json'}, 'ZIP inventory')
        for p,r in records.items():
            b=z.read(p)
            require(len(b)==r['bytes'] and sha(b)==r['sha256'], 'ZIP hash '+p)
            if '/' not in p:
                source=PUB/'output/pdf/note.pdf' if p=='note.pdf' else (PUB/p if (PUB/p).exists() else AUDIT/p)
                require(read(source)==b,'ZIP current root byte identity '+p)
        require(z.read('note.pdf')==read(PUB/'output/pdf/note.pdf'), 'PDF identity')
        require(z.read('note.tex')==read(PUB/'note.tex'), 'TeX identity')
        original=json.loads(read(AUDIT/'ORIGINAL_SNAPSHOT.json'))
        require(original['head']==HEAD and len(original['files'])==26, 'original anchor')
        prefix='unsolved_math_prioritization/attempts/30006191/bounded_region_v2/'
        for p,d in original['files'].items():
            b=subprocess.check_output(['git','show',HEAD+':'+p],cwd=REPO)
            require(sha(b)==d, 'git original '+p)
            require(read(AUDIT/'original'/p)==b, 'disk original '+p)
            require(z.read('original_packet/'+p.removeprefix(prefix))==b, 'ZIP original '+p)
        family_counts={}
        manifests=[p for p in names if p.startswith('reviews/') and p.endswith('/MANIFEST.json')]
        for mp in manifests:
            m=json.loads(z.read(mp))
            records2=m.get('intentional_public_files',m.get('files',m.get('artifact_fingerprints')))
            if isinstance(records2,list): records2={r['path']:r for r in records2}
            require(type(records2) is dict,'unknown family manifest '+mp)
            folder=str(PurePosixPath(mp).parent)
            if 'explicit_public_allowlist' in m: require(set(m['explicit_public_allowlist'])==set(records2),'family allowlist '+mp)
            if 'public_allowlist' in m: require(set(m['public_allowlist'])==set(records2)|{'MANIFEST.json'},'family allowlist '+mp)
            actual={p.removeprefix(folder+'/') for p in names if p.startswith(folder+'/')}
            require(actual==set(records2)|{'MANIFEST.json'},'family exact archive inventory '+mp)
            for p,r in records2.items():
                # Family manifests use paths local to the family directory.
                full=folder+'/'+p
                b=z.read(full)
                d=r['sha256'] if isinstance(r,dict) else r
                require(sha(b)==d,'family '+full)
                require(read(AUDIT/full)==b,'live family bytes '+full)
                if isinstance(r,dict) and 'bytes' in r: require(len(b)==r['bytes'],'family bytes '+full)
            family_counts[folder]=len(records2)
        result={'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'phase':phase,'freeze_sha256':FREEZE,'frozen_files':13,'archive_sha256':ARCHIVE,
          'package_manifest_sha256':PACKAGE,'zip_members':110,'payloads':109,
          'original_head':HEAD,'original_files_git_disk_archive_identical':26,
          'family_manifests':family_counts,'pdf_sha256':sha(read(PUB/'output/pdf/note.pdf'))}
    (HERE/f'AUTHENTICATION_{phase}.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))

if __name__=='__main__': main()
