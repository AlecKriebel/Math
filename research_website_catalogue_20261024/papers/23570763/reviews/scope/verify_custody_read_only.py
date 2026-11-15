"""Bounded pure source/initial/final custody. No project imports or science run.

Only stdlib reads, hashing and original ZIP member comparison; no dynamic
execution, subprocess, network, filesystem mutation or supplied checker import.
"""
from pathlib import Path, PurePosixPath
import json
import hashlib
import zipfile
import zlib

OWN = Path(__file__).resolve().parent
SOURCE = OWN.parents[1] / 'sources'
READY_SHA = '64b0c9408ee2d24da06d20d3c9bd7653e2ed9537f571a1051d40826ee5e0ab73'
INITIAL_SHA = 'f896dc624b7ccd8c495ef327100dfa229d01606601c4714f9377c9055aff5002'

def need(ok, label):
 if not ok:
  raise ValueError(label)

def bind(path):
 path = Path(path)
 need(path.is_file() and not path.is_symlink(), 'regular:' + str(path))
 data = path.read_bytes()
 return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}

def load(path):
 def pairs(rows):
  out = {}
  for k, v in rows:
   need(k not in out, 'duplicate JSON key')
   out[k] = v
  return out
 return json.loads(Path(path).read_bytes(), object_pairs_hook=pairs)

def verify():
 need(bind(SOURCE / 'SOURCE_READY.json')['sha256'] == READY_SHA, 'exact source-ready pin')
 need(bind(OWN / 'INITIAL_SEAL.json')['sha256'] == INITIAL_SHA, 'exact immutable initial seal')
 initial = load(OWN / 'INITIAL_SEAL.json')
 need(bind(OWN / 'INITIAL_OWNED_MANIFEST.json')['sha256'] == initial['initial_owned_manifest_sha256'], 'initial manifest seal')
 early = load(OWN / 'INITIAL_OWNED_MANIFEST.json')['files']
 for x in early:
  need(bind(OWN / x['path']) == {k: x[k] for k in ('bytes', 'sha256')}, 'immutable early artifact:' + x['path'])
 inputs = load(OWN / 'INPUT_MANIFEST.json')['all_original_source_files']
 need(len(inputs) == 65, 'all65 original source files')
 need({str(q) for q in SOURCE.rglob('*') if q.is_file()} == {x['path'] for x in inputs}, 'entire original source namespace')
 need(not any(q.is_symlink() for q in SOURCE.rglob('*')), 'source no symlinks')
 for x in inputs:
  need(bind(x['path']) == {k: x[k] for k in ('bytes', 'sha256')}, 'original source:' + x['path'])
 ready = load(SOURCE / 'SOURCE_READY.json')
 need(ready['record_id'] == 23570763 and ready['version'] == '1.0.0' and ready['publication_date'] == '2026-10-22', 'actual native identity and edition')
 need(ready['created'] == '2026-10-22T16:11:19.267654+00:00', 'original creation timestamp separate')
 need(ready['native_license_metadata_whole_field'] == {'present': True, 'original_value': {'id': 'cc-by-4.0'}}, 'whole native license metadata')
 for obj in ready['whole_native_API_objects']:
  need(bind(obj['path']) == {'bytes': obj['bytes'], 'sha256': obj['SHA256']}, 'whole native API body:' + obj['role'])
 assets = ready['all_native_assets_in_original_order']
 need([x['original_api_file_object']['key'] for x in assets] == ['periodic-lefschetz-source-and-verification.zip', 'periodic-lefschetz.pdf'], 'original ZIP/PDF order')
 for x in assets:
  data = Path(x['path']).read_bytes()
  api = x['original_api_file_object']
  need(bind(x['path']) == {'bytes': x['bytes'], 'sha256': x['SHA256']} and len(data) == api['size'] and 'md5:' + hashlib.md5(data).hexdigest() == api['checksum'], 'whole native asset:' + api['key'])
 need(bind(ready['controlling_TeX']['extracted_path']) == {'bytes': 13429, 'sha256': 'd71584d4b4e7431662bd6a3812e939feb7f29d0c4cf926fca6c6d07e1c292cb2'}, 'entire controlling265-line TeX')
 pdf = Path(assets[1]['path']).read_bytes()
 payloads = []
 embedded = []
 with zipfile.ZipFile(assets[0]['path']) as z:
  names = set()
  folded = set()
  for info in z.infolist():
   if info.is_dir():
    continue
   name = info.filename
   pp = PurePosixPath(name)
   need(not pp.is_absolute() and '..' not in pp.parts and pp.as_posix() == name and '\\' not in name, 'safe original archive path')
   need(name not in names and name.casefold() not in folded, 'no duplicate/case collision')
   names.add(name)
   folded.add(name.casefold())
   need((info.external_attr >> 16) & 0o170000 != 0o120000, 'no archive symlink')
   body = z.read(info)
   need(len(body) == info.file_size and zlib.crc32(body) & 0xffffffff == info.CRC, 'whole archive CRC and size')
   path = SOURCE / 'published-source/asset-001' / name
   need(path.read_bytes() == body, 'entire extracted original member:' + name)
   if name.lower().endswith('.pdf'):
    embedded.append(name)
    need(body == pdf, 'embedded PDF exact identity to actual published standalone reader')
   payloads.append({'original_member': name, 'bytes': len(body), 'CRC32': f'{info.CRC:08x}', 'sha256': hashlib.sha256(body).hexdigest()})
 need(len(payloads) == 18 and sum(x['bytes'] for x in payloads) == 129597, 'all18 full original ZIP payloads')
 need(embedded == ['periodic_lefschetz_source/paper.pdf'], 'exact sole embedded PDF, not replacement reader')
 if (OWN / 'SEAL.json').exists():
  final = load(OWN / 'SEAL.json')
  need(bind(OWN / 'OWNED_MANIFEST.json')['sha256'] == final['owned_manifest_sha256'], 'final owned manifest seal')
  manifest = load(OWN / 'OWNED_MANIFEST.json')['files']
  need({str(q.relative_to(OWN)) for q in OWN.rglob('*') if q.is_file()} == {x['path'] for x in manifest} | {'OWNED_MANIFEST.json', 'SEAL.json'}, 'entire sealed final owned namespace')
  for x in manifest:
   need(bind(OWN / x['path']) == {k: x[k] for k in ('bytes', 'sha256')}, 'final owned artifact:' + x['path'])
 return {'custody_result': 'Complete original-source/ZIP and immutable independent-initial custody verified; no scientific replay.', 'unchanged_source_files': len(inputs), 'immutable_initial_payloads': len(early), 'whole_native_ZIP_payloads': len(payloads), 'expanded_bytes': 129597, 'payload_bindings': payloads, 'embedded_PDF_identical_to_actual_standalone': True, 'final_owned_seal_verified_if_present': (OWN / 'SEAL.json').exists(), 'project_imports': 0, 'dynamic_or_supplied_code_execution': 0, 'network': 0, 'file_writes': 0}

if __name__ == '__main__':
 print(json.dumps(verify(), indent=2))
