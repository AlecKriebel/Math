"""Read-only release-archive integrity and extraction audit."""
from pathlib import Path, PurePosixPath
from zipfile import ZipFile
from hashlib import sha256
import json
import stat
import sys

base = Path(__file__).resolve().parents[2]
result = []
for argument in sys.argv[1:]:
    path = Path(argument).resolve()
    with ZipFile(path) as z:
        names = z.namelist()
        if len(names) != len(set(names)) or len(names) != len({s.casefold() for s in names}):
            raise AssertionError(f'Duplicate or case-colliding names: {path}')
        for info in z.infolist():
            p = PurePosixPath(info.filename)
            if p.is_absolute() or '..' in p.parts or '\\' in info.filename or ':' in info.filename:
                raise AssertionError(f'Unsafe member path: {info.filename}')
            if info.flag_bits & 1:
                raise AssertionError(f'Encrypted member: {info.filename}')
            mode = info.external_attr >> 16
            if stat.S_ISLNK(mode):
                raise AssertionError(f'Symlink member: {info.filename}')
            if any(part in ('__MACOSX', '.git', 'build', '__pycache__') for part in p.parts):
                raise AssertionError(f'Unexpected build/system metadata: {info.filename}')
            if p.name == '.DS_Store':
                raise AssertionError(f'Unexpected Finder metadata: {info.filename}')
        if z.testzip() is not None:
            raise AssertionError(f'CRC failure: {path}')
        result.append({'archive':str(path.relative_to(base)),
                       'sha256':sha256(path.read_bytes()).hexdigest(),
                       'files':[{'path':i.filename,'size':i.file_size,
                                 'sha256':sha256(z.read(i)).hexdigest()}
                                for i in z.infolist() if not i.is_dir()]})
Path(__file__).with_name('archive_audit.json').write_text(json.dumps(result,indent=2)+'\n')
for item in result:
    print('PASS',item['archive'],len(item['files']),'files',item['sha256'])
    for entry in item['files']:
        print(' ',entry['path'],entry['size'])
