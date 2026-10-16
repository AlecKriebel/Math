"""Check actual raw ZIP streams against the documented explicit DEFLATE level."""
from pathlib import Path
import datetime
import hashlib
import io
import json
import struct
import zlib
import zipfile

ROOT = Path(__file__).resolve().parent


def require(ok, message):
    if not ok:
        raise ValueError(message)


def raw_stream(data, level):
    compressor = zlib.compressobj(level, zlib.DEFLATED, -15)
    return compressor.compress(data) + compressor.flush()


def check(name):
    raw = (ROOT / name).read_bytes()
    rows = []
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        require(archive.testzip() is None, 'CRC mismatch')
        names = archive.namelist()
        require(names == sorted(set(names)), 'Unsorted or duplicate ZIP members')
        for info in archive.infolist():
            require(info.compress_type == zipfile.ZIP_DEFLATED, 'Wrong compression method')
            require(info.date_time == (2026, 10, 15, 0, 0, 0), 'Wrong fixed timestamp')
            require(info.external_attr >> 16 == 0o100644, 'Wrong member type/mode')
            header = struct.unpack_from('<4s5H3I2H', raw, info.header_offset)
            require(header[0] == b'PK\x03\x04', 'Bad local header')
            start = info.header_offset + 30 + header[-2] + header[-1]
            compressed = raw[start:start+info.compress_size]
            payload = archive.read(info)
            require(compressed == raw_stream(payload, 9),
                    'Member does not match explicit level9: ' + name + '/' + info.filename)
            rows.append({'path': info.filename, 'compressed_bytes': len(compressed),
                         'matches_explicit_level9': True,
                         'differs_from_default': compressed != raw_stream(payload, -1)})
    return {'archive': name, 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest(),
            'members': len(rows), 'distinguishing_members': sum(r['differs_from_default']
                                                              for r in rows),
            'streams': rows}


def main():
    archives = [check(name) for name in
                ('source-and-verification.zip', 'zenodo-upload-kit.zip')]
    require(archives[0]['distinguishing_members'] > 0, 'No distinguishing source stream')
    receipt = {'checked_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
               'status': 'PASS_ACTUAL_EXPLICIT_LEVEL9_STREAMS',
               'zlib_runtime': zlib.ZLIB_RUNTIME_VERSION, 'archives': archives,
               'scope': 'Exact recompression in this zlib runtime; no mathematical theorem certificate.'}
    (ROOT / 'ROOT_COMPRESSION_STREAMS.json').write_text(json.dumps(receipt, indent=2)+'\n')
    print(json.dumps({'status': receipt['status'], 'archives': [
        {k: a[k] for k in ('archive', 'members', 'distinguishing_members', 'sha256')}
        for a in archives]}, indent=2))


if __name__ == '__main__':
    main()
