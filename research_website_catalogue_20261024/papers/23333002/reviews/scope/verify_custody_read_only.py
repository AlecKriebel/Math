"""Bounded pure custody only: stdlib, no project imports, exec, network or writes."""
from pathlib import Path, PurePosixPath
import json
import hashlib
import zipfile
import zlib

OWN = Path(__file__).resolve().parent
SOURCE = OWN.parents[1] / 'sources'
READY_SHA = '91a2924e8c97f248e5ac8c9d5b61f6623c93df30b40d71cdbf852284bb294d1b'
INITIAL_SHA = '69396dfe975a48150d6d4232a04c030338de80caddc554bd2475f1b3fdebd7b2'

def require(ok, label):
 if not ok:
  raise ValueError(label)

def bind(path):
 path = Path(path)
 require(path.is_file() and not path.is_symlink(), 'regular:' + str(path))
 data = path.read_bytes()
 return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}

def load(path):
 def pairs(rows):
  out = {}
  for key, value in rows:
   require(key not in out, 'duplicate JSON key')
   out[key] = value
  return out
 return json.loads(Path(path).read_bytes(), object_pairs_hook=pairs)

def verify():
 require(bind(SOURCE / 'SOURCE_READY.json')['sha256'] == READY_SHA, 'source-ready exact pin')
 require(bind(OWN / 'INITIAL_SEAL.json')['sha256'] == INITIAL_SHA, 'immutable independent initial')
 initial = load(OWN / 'INITIAL_SEAL.json')
 im = load(OWN / 'INITIAL_OWNED_MANIFEST.json')
 require(bind(OWN / 'INITIAL_OWNED_MANIFEST.json')['sha256'] == initial['initial_owned_manifest_sha256'], 'initial manifest seal')
 for row in im['files']:
  require(bind(OWN / row['path']) == {k: row[k] for k in ('bytes', 'sha256')}, 'initial artifact:' + row['path'])
 inputs = load(OWN / 'INPUT_MANIFEST.json')['all_source_files']
 require(len(inputs) == 122, 'all122 original source files')
 require({str(q) for q in SOURCE.rglob('*') if q.is_file()} == {r['path'] for r in inputs}, 'exact original source namespace')
 require(not any(q.is_symlink() for q in SOURCE.rglob('*')), 'source has no symlink')
 for row in inputs:
  require(bind(row['path']) == {k: row[k] for k in ('bytes', 'sha256')}, 'original source:' + row['path'])
 ready = load(SOURCE / 'SOURCE_READY.json')
 require(ready['record_id'] == 23333002 and ready['version'] == '1.0' and ready['publication_date'] == '2026-10-12', 'original edition identity')
 require(ready['created'] == '2026-10-13T05:49:11.621031+00:00', 'separate native creation date')
 require(ready['native_license_metadata_whole_field'] == {'present': True, 'original_value': {'id': 'cc-by-4.0'}}, 'whole original native license metadata')
 for obj in ready['whole_native_API_objects']:
  require(bind(obj['path']) == {'bytes': obj['bytes'], 'sha256': obj['SHA256']}, 'whole native API body:' + obj['role'])
 assets = ready['all_native_assets_in_original_order']
 require([x['original_api_file_object']['key'] for x in assets] == ['robinson-tangency-certificates-v1.0.pdf', 'robinson-tangency-source-verification-v1.0.zip'], 'native PDF/ZIP order')
 for asset in assets:
  data = Path(asset['path']).read_bytes()
  api = asset['original_api_file_object']
  require(bind(asset['path']) == {'bytes': asset['bytes'], 'sha256': asset['SHA256']} and len(data) == api['size'] and 'md5:' + hashlib.md5(data).hexdigest() == api['checksum'], 'whole original native asset:' + api['key'])
 archive = Path(assets[1]['path'])
 payloads = []
 with zipfile.ZipFile(archive) as z:
  names = set()
  folded = set()
  for member in z.infolist():
   if member.is_dir():
    continue
   name = member.filename
   pp = PurePosixPath(name)
   require(not pp.is_absolute() and '..' not in pp.parts and pp.as_posix() == name and '\\' not in name, 'safe original ZIP path')
   require(name not in names and name.casefold() not in folded, 'no duplicate or case-colliding ZIP names')
   names.add(name)
   folded.add(name.casefold())
   mode = member.external_attr >> 16
   require(mode & 0o170000 != 0o120000, 'no ZIP symlink')
   data = z.read(member)
   require(len(data) == member.file_size and zlib.crc32(data) & 0xffffffff == member.CRC, 'exact ZIP size/CRC')
   extracted = SOURCE / 'published-source' / name
   require(extracted.read_bytes() == data, 'whole original extracted member identity:' + name)
   payloads.append({'original_member': name, 'bytes': len(data), 'CRC32': f'{member.CRC:08x}', 'sha256': hashlib.sha256(data).hexdigest()})
 require(len(payloads) == 85 and sum(x['bytes'] for x in payloads) == 556745, 'all85 complete native payloads')
 require(not any(x['original_member'].lower().endswith('.pdf') for x in payloads), 'no embedded PDF substituted for original reader')
 final = OWN / 'SEAL.json'
 if final.exists():
  seal = load(final)
  manifest = load(OWN / 'OWNED_MANIFEST.json')
  require(bind(OWN / 'OWNED_MANIFEST.json')['sha256'] == seal['owned_manifest_sha256'], 'final owned manifest seal')
  require({str(q.relative_to(OWN)) for q in OWN.rglob('*') if q.is_file()} == {x['path'] for x in manifest['files']} | {'OWNED_MANIFEST.json', 'SEAL.json'}, 'entire final owned namespace')
  for row in manifest['files']:
   require(bind(OWN / row['path']) == {k: row[k] for k in ('bytes', 'sha256')}, 'final owned artifact:' + row['path'])
 return {'custody_result': 'Exact original-source, initial-seal and whole-native-ZIP custody verified; no scientific replay.', 'source_files_unchanged': len(inputs), 'initial_payloads_verified': len(im['files']), 'whole_ZIP_payloads': len(payloads), 'expanded_bytes': 556745, 'payload_bindings': payloads, 'final_owned_seal_present_and_verified': final.exists(), 'project_imports': 0, 'scientific_or_source_execution': 0, 'network': 0, 'file_writes': 0}

if __name__ == '__main__':
 print(json.dumps(verify(), indent=2))
