"""Byte-identity audit of a pinned, non-executable author freeze. No extraction."""
import hashlib
import io
import json
import pathlib
import stat
import sys
import zipfile

ARCHIVE_SHA = 'feb85b4fd09b96aced2438889fbc0866302a56478fef12ad447f95fc8da336be'
MANIFEST_SHA = '4bc74cfa1a957a2f9a6d87e5c0251bd30fc05195b1da8e86503da30d4611e56c'
EXPECTED = {
 'checks.json': (2377, '65196247914f8a8d617cd09764b70c2822bd2babec3e7375194cf327447aa3d0'),
 'proof.md': (13218, '33ccbc5cae54b3090939e98362d6f3d62b51e90b99ab89e2a85be9e4839e8f71'),
 'source_metadata.json': (4696, '573520b0ddedada3aa8733cbe6d4520785e29b43036d02675d5807cb89bf0943'),
 'status.md': (5125, 'c60d210bb9b957ca1bd63c228a3e1912c3b6177769c889a8243aa7d718c539ad'),
}
def need(condition, message):
 if not condition:
  raise ValueError(message)
def digest(data):
 return hashlib.sha256(data).hexdigest()
def pairs(items):
 result = {}
 for key, value in items:
  need(key not in result, 'duplicate JSON key')
  result[key] = value
 return result
def nonfinite(value):
 raise ValueError('non-finite JSON number')
def parse(data):
 return json.loads(data.decode('utf-8', errors='strict'), object_pairs_hook=pairs, parse_constant=nonfinite)
def read_regular(path, size):
 p = pathlib.Path(path)
 need(not p.is_symlink(), 'input symlink')
 s = p.stat()
 need(stat.S_ISREG(s.st_mode), 'input not regular file')
 need(s.st_size == size, 'input byte count mismatch')
 data = p.read_bytes()
 need(len(data) == size, 'read byte count mismatch')
 return data

def verify(archive, manifest):
 mb = read_regular(manifest, 1028)
 need(digest(mb) == MANIFEST_SHA, 'external manifest SHA-256 mismatch')
 m = parse(mb)
 need(m['archive'] == {'filename': 'MIXED_PERVERSE_30002888_AUTHOR_SAFE_FREEZE.zip', 'bytes':11285, 'sha256':ARCHIVE_SHA}, 'manifest archive identity')
 need(len(m['files']) == len(EXPECTED), 'manifest file count')
 need({x['path']:(x['bytes'],x['sha256']) for x in m['files']} == EXPECTED, 'manifest membership')
 b = read_regular(archive, 11285)
 need(digest(b) == ARCHIVE_SHA, 'archive SHA-256 mismatch')
 rows=[]
 with zipfile.ZipFile(io.BytesIO(b)) as z:
  infos=z.infolist()
  names=[i.filename for i in infos]
  need(len(names)==len(set(names))==4, 'duplicate ZIP names or bad member count')
  need(set(names)==set(EXPECTED), 'ZIP exact file set')
  need(not z.comment, 'ZIP comment')
  for i in infos:
   need(i.filename == i.orig_filename, 'ZIP name rewriting')
   need('/' not in i.filename and '\\' not in i.filename and '\x00' not in i.filename, 'unsafe name')
   need(not i.is_dir() and not i.flag_bits & 1, 'directory or encryption')
   mode=i.external_attr >> 16
   need(not stat.S_ISLNK(mode), 'ZIP symlink')
   need(stat.S_IFMT(mode) in (0,stat.S_IFREG), 'ZIP special type')
   need(mode & 0o111 == 0, 'ZIP executable bit')
   count,sha=EXPECTED[i.filename]
   need(i.file_size==count, 'member advertised byte count')
   raw=z.read(i)
   need(len(raw)==count and digest(raw)==sha, 'member identity')
   text=raw.decode('utf-8', errors='strict')
   need('\x00' not in text, 'NUL in text')
   if i.filename.endswith('.json'):
    parsed=parse(raw)
    need(type(parsed) is dict, 'JSON root')
   need(not text.startswith('#!'), 'script marker')
   rows.append({'path':i.filename,'bytes':len(raw),'sha256':digest(raw)})
  need(z.testzip() is None, 'ZIP CRC')
 return {'ok':True,'archive_bytes':len(b),'archive_sha256':digest(b),'manifest_sha256':digest(mb),'files':sorted(rows,key=lambda x:x['path']),'executed_archive_members':False,'mathematical_truth_checked_by_code':False}

if __name__ == '__main__':
 try:
  need(len(sys.argv)==3, 'usage: verify_author.py AUTHOR.zip MANIFEST.json')
  print(json.dumps(verify(sys.argv[1],sys.argv[2]), sort_keys=True))
 except (OSError, ValueError, KeyError, TypeError, zipfile.BadZipFile) as e:
  print(json.dumps({'ok':False,'error':str(e)},sort_keys=True))
  sys.exit(1)
