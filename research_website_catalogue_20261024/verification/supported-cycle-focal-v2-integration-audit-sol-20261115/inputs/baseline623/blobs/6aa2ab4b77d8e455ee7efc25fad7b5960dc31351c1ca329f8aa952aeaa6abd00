"""Read-only resolution of deposited files and explicitly bound ZIP members."""
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from io import BytesIO
from copy import deepcopy
import hashlib
import re
import stat
import zipfile


def normalized_receipt_view(raw):
    """Return an independent asset-list view; hashes must use the original bytes."""
    if not isinstance(raw, dict):
        raise ValueError('Receipt must be an object')
    present = [key for key in ('files', 'assets') if key in raw]
    if not present:
        raise ValueError('Receipt has no deposited asset list')
    for key in present:
        if not isinstance(raw[key], list) or not all(isinstance(x, dict) for x in raw[key]):
            raise ValueError('Receipt asset list must contain objects')
    if len(present) == 2 and raw['files'] != raw['assets']:
        raise ValueError('Conflicting files and assets lists')
    result = deepcopy(raw)
    result['files'] = deepcopy(raw[present[0]])
    return result


def asset_name(item):
    name, filename = item.get('name'), item.get('filename')
    if name is not None and filename is not None and name != filename:
        raise ValueError('Conflicting receipt name and filename')
    value = name if name is not None else filename
    safe_relative(value, basename=True)
    return value


def safe_relative(value, *, basename=False):
    if (not isinstance(value, str) or not value or '\\' in value or '\x00' in value
            or ':' in value or value.startswith('/')
            or any(part in ('', '.', '..') for part in value.split('/'))):
        raise ValueError('Unsafe asset path: ' + repr(value))
    if basename and len(PurePosixPath(value).parts) != 1:
        raise ValueError('Asset filename must be a basename: ' + value)
    return value


def digest(data):
    return hashlib.sha256(data).hexdigest()


def checked_sha(value):
    if not isinstance(value, str) or not re.fullmatch(r'[0-9a-f]{64}', value):
        raise ValueError('Invalid asset SHA-256')
    return value


@dataclass(frozen=True)
class ResolvedAsset:
    path: Path
    sha256: str
    embedded: bool = False
    pages: int | None = None

    def read_bytes(self):
        data = self.path.read_bytes()
        if digest(data) != self.sha256:
            raise ValueError('Resolved asset changed: ' + str(self.path))
        return data


class PublishedAssets:
    def __init__(self, sources, receipt, embedded_assets=()):
        self.sources = Path(sources).resolve(strict=True)
        self.deposited = {}
        receipt = normalized_receipt_view(receipt)
        for item in receipt['files']:
            name = asset_name(item)
            if name in self.deposited:
                raise ValueError('Duplicate receipt asset: ' + name)
            checked_sha(item['sha256'])
            self.deposited[name] = item
        self.embedded = {}
        members, extracted = set(), set()
        for item in embedded_assets:
            name = safe_relative(item['filename'], basename=True)
            archive = safe_relative(item['archive_filename'], basename=True)
            member = safe_relative(item['archive_member'])
            source = safe_relative(item['source_relative_path'])
            checked_sha(item['sha256'])
            if name in self.deposited or name in self.embedded:
                raise ValueError('Duplicate or ambiguous embedded filename: ' + name)
            if (archive, member) in members or source in extracted:
                raise ValueError('Duplicate embedded member/source binding: ' + name)
            if archive not in self.deposited or not archive.endswith('.zip'):
                raise ValueError('Embedded archive is not a deposited ZIP: ' + archive)
            if PurePosixPath(member).name != name or PurePosixPath(source).name != name:
                raise ValueError('Embedded member/source filename mismatch: ' + name)
            pages = item.get('pages')
            if pages is not None and (type(pages) is not int or pages < 1):
                raise ValueError('Invalid embedded PDF page count')
            self.embedded[name] = item
            members.add((archive, member))
            extracted.add(source)

    def additional_asset_kind(self, item):
        """Validate declared kinds; infer only authenticated, recognizable PDF/ZIPs."""
        name = safe_relative(item['filename'], basename=True)
        asset = self.resolve(name)
        suffix = PurePosixPath(name).suffix
        if 'kind' in item:
            if item['kind'] not in ('pdf', 'zip', 'text'):
                raise ValueError('Unsupported additional asset kind: ' + repr(item['kind']))
            if item['kind'] in ('pdf', 'zip') and suffix != '.' + item['kind']:
                raise ValueError('Additional asset kind does not match filename: ' + name)
            return item['kind']
        if suffix == '.zip' and zipfile.is_zipfile(BytesIO(asset.read_bytes())):
            return 'zip'
        if suffix == '.pdf' and asset.read_bytes().startswith(b'%PDF-'):
            return 'pdf'
        raise ValueError('Cannot infer additional asset kind: ' + name)

    def _path(self, relative):
        safe_relative(relative)
        path = self.sources / relative
        current = self.sources
        for part in PurePosixPath(relative).parts:
            current = current / part
            if current.is_symlink():
                raise ValueError('Symlink in asset path: ' + relative)
        resolved = path.resolve(strict=True)
        if not resolved.is_relative_to(self.sources) or not resolved.is_file():
            raise ValueError('Asset is not a contained regular file: ' + relative)
        return resolved

    def _deposited(self, name):
        item = self.deposited[name]
        path = self._path(name)
        data = path.read_bytes()
        if digest(data) != item['sha256']:
            raise ValueError('Deposited asset SHA-256 mismatch: ' + name)
        expected_size = item.get('bytes', item.get('size'))
        if expected_size is not None and len(data) != expected_size:
            raise ValueError('Deposited asset size mismatch: ' + name)
        return ResolvedAsset(path, item['sha256'])

    def resolve(self, name):
        safe_relative(name, basename=True)
        if name in self.deposited:
            return self._deposited(name)
        if name not in self.embedded:
            raise ValueError('Asset has no deposited or embedded binding: ' + name)
        item = self.embedded[name]
        archive = self._deposited(item['archive_filename'])
        with zipfile.ZipFile(BytesIO(archive.read_bytes())) as z:
            names = set()
            for entry in z.infolist():
                safe_relative(entry.filename.rstrip('/') if entry.is_dir() else entry.filename)
                if entry.filename in names:
                    raise ValueError('Duplicate ZIP member: ' + entry.filename)
                if stat.S_ISLNK(entry.external_attr >> 16):
                    raise ValueError('ZIP symlink member: ' + entry.filename)
                names.add(entry.filename)
            try:
                member = z.read(item['archive_member'])  # Includes the ZIP CRC check.
            except KeyError as exc:
                raise ValueError('Missing embedded ZIP member: ' + item['archive_member']) from exc
        if digest(member) != item['sha256']:
            raise ValueError('Embedded ZIP member SHA-256 mismatch: ' + name)
        path = self._path(item['source_relative_path'])
        if path.read_bytes() != member:
            raise ValueError('Extracted source differs from original ZIP member: ' + name)
        return ResolvedAsset(path, item['sha256'], embedded=True, pages=item.get('pages'))
