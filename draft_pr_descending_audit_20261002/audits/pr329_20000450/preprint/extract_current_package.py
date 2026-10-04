"""Extract the locally built archive into a fresh controlled replay directory."""
from pathlib import Path, PurePosixPath
import hashlib, json, stat, sys, zipfile
A=Path(__file__).resolve().parent.parent;R=A.parents[2]
assert len(sys.argv)==2 and sys.argv[1].isdigit();v=int(sys.argv[1]);assert v>=2
archive=R/'problems/20000450_pentagonal_torsion/preprint/pentagonal-torsion-verification.zip'
D=A/'root_preprint_private'/f'archive_replay_v{v:02d}'
assert not D.exists();D.mkdir(parents=True)
with zipfile.ZipFile(archive) as z:
    assert len(z.namelist())==len(set(z.namelist())) and z.testzip() is None
    for info in z.infolist():
        n=PurePosixPath(info.filename)
        assert not n.is_absolute() and '..' not in n.parts
        mode=info.external_attr>>16;assert mode in {stat.S_IFDIR|0o755,stat.S_IFREG|0o644}
        p=D/str(n)
        if info.is_dir():
            assert mode==stat.S_IFDIR|0o755;p.mkdir(exist_ok=True);p.chmod(0o755)
        else:
            assert mode==stat.S_IFREG|0o644;p.parent.mkdir(parents=True,exist_ok=True)
            p.write_bytes(z.read(info.filename));p.chmod(0o644)
print(json.dumps(dict(status='EXTRACTED_REQUIRES_NATIVE_REPLAY',directory=str(D),
    archive_sha256=hashlib.sha256(archive.read_bytes()).hexdigest(),members=len(z.namelist())),indent=2))
