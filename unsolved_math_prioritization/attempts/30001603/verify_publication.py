#!/usr/bin/env python3
"""Read-only portable replay. Optional argument: external PUBLICATION_MANIFEST SHA-256."""
from pathlib import Path, PurePosixPath
import hashlib, json, subprocess, sys
ROOT = Path(__file__).resolve().parent
ANCHORS = {
 'toric_jets_30001603/MANIFEST.json': '5ae79fd9ca09fc095a33d7acfa27818377163c1eb2161977ff172cf641420616',
 'toric_jets_30001603_corrected_release/RELEASE_MANIFEST.json': '506886489cb3eba4235fa555b4d3fb6c5b46dcb8d2b6b577576f8419e2b17a9e',
 'toric_jets_30001603_corrected_release/packet/MANIFEST.json': '670f3a5365201fdcda372dbd6037aefb062cda2a7dd3537522a19c4a5204fe55',
 'toric_jets_30001603_corrected_release/packet/PROOF.md': '1ae5a43cbf52ba23c3b39a99a4d5c4c376305edb375a0b343da935e8328210ed',
 'toric_jets_30001603_independent_audit/MANIFEST.json': 'efd9065e283904c34c9f3c863e85b159945186e504c6c3657d5a2547078935d1',
 'toric_jets_30001603_delta_audit/MANIFEST.json': 'cbe8f0dda40f3376538b7eb9c0704a48b0cd2b0326e86b2e232474ea469b8224',
 'toric_jets_30001603_delta_audit/EXACT_ACCEPTANCE.json': '90bd2601d5f9d2b85a04ea6de59aab6982c10400ef9a11df43c3c5a6604cf24f',
}
def require(ok, message):
 if not ok: raise ValueError(message)
def sha(data): return hashlib.sha256(data).hexdigest()
def unique(pairs):
 result = {}
 for key, value in pairs:
  require(key not in result, 'duplicate JSON key')
  result[key] = value
 return result
def snapshot():
 return {p.relative_to(ROOT).as_posix(): (p.stat().st_size, sha(p.read_bytes())) for p in ROOT.rglob('*') if p.is_file()}
def main():
 require(len(sys.argv) in (1, 2), 'Usage: python3 -B verify_publication.py [external_manifest_sha256]')
 raw = (ROOT/'PUBLICATION_MANIFEST.json').read_bytes()
 if len(sys.argv) == 2: require(sha(raw) == sys.argv[1], 'external publication-manifest anchor mismatch')
 manifest = json.loads(raw, object_pairs_hook=unique)
 require(manifest['problem_id'] == '30001603', 'problem identity')
 records = manifest['files']; names = [r['path'] for r in records]
 require(len(names) == len(set(names)), 'duplicate manifest member')
 for name in names:
  p = PurePosixPath(name)
  require(name == p.as_posix() and not p.is_absolute() and '..' not in p.parts and name != 'PUBLICATION_MANIFEST.json', 'unsafe manifest path')
 paths = list(ROOT.rglob('*'))
 require(not any(p.is_symlink() for p in paths), 'symlink in publication')
 require(all(p.is_file() or p.is_dir() for p in paths), 'nonregular member')
 before = snapshot()
 require(set(before) == set(names) | {'PUBLICATION_MANIFEST.json'}, 'exact publication file membership')
 expected_dirs = {str(p) for name in names for p in PurePosixPath(name).parents if str(p) != '.'}
 require({p.relative_to(ROOT).as_posix() for p in paths if p.is_dir()} == expected_dirs, 'exact publication directory membership')
 for r in records: require(before[r['path']] == (r['bytes'], r['sha256']), 'publication member hash: ' + r['path'])
 for path, anchor in ANCHORS.items(): require(before[path][1] == anchor, 'independent frozen anchor: ' + path)
 acceptance = json.loads((ROOT/'toric_jets_30001603_delta_audit/EXACT_ACCEPTANCE.json').read_bytes(), object_pairs_hook=unique)
 require(acceptance['accepted'] is True and acceptance['verdict'] == 'PASS' and acceptance['disposition'] == 'already_solved' and acceptance['author_turns_used'] == 1, 'corrected acceptance verdict')
 commands = [
  ('corrected_packet', [ROOT/'toric_jets_30001603_corrected_release/packet/CHECK_PACKET.py']),
  ('final_delta_acceptance', [ROOT/'toric_jets_30001603_delta_audit/CHECK_DELTA.py']),
  ('historical_original_audit', [ROOT/'toric_jets_30001603_independent_audit/CHECK_AUDIT.py', ROOT/'toric_jets_30001603']),
 ]
 results = {}
 for label, args in commands:
  run = subprocess.run([sys.executable, '-B', *map(str, args)], check=True, capture_output=True)
  require(not run.stderr, label + ' unexpected stderr')
  results[label] = json.loads(run.stdout, object_pairs_hook=unique)
 require(snapshot() == before, 'replay changed publication input bytes')
 print(json.dumps({
  'result': 'PASS', 'disposition': 'already_solved', 'author_turns': '1/5',
  'publication_manifest_sha256': sha(raw), 'publication_files': len(before),
  'external_publication_anchor_checked': len(sys.argv) == 2, 'frozen_anchors_checked': len(ANCHORS),
  'all_input_bytes_preserved': True, 'replays': results,
  'note': 'The original freeze and original correction-required verdict are historical. Only the corrected packet is accepted.',
 }, indent=2, sort_keys=True))
if __name__ == '__main__': main()
