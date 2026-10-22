#!/usr/bin/env python3
"""Prepare a local, reviewable repository tree. This performs no Git/service write."""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
import shutil
import stat
import zipfile

AUDIT = Path(__file__).resolve().parent
PROGRAM = AUDIT.parents[1]
PREFIX = 'unsolved_math_prioritization/attempts/30006166/'

WRAPPER = r'''#!/usr/bin/env python3
"""Bind the current repository package; finite replays do not prove the theorem."""
import argparse,hashlib,json,stat,subprocess,sys,zipfile
from pathlib import Path,PurePosixPath
def need(ok,label):
 if not ok:raise RuntimeError(label)
def unique(pairs):
 d={}
 for k,v in pairs:
  need(k not in d,'duplicate JSON key');d[k]=v
 return d
def load(p):return json.loads(p.read_bytes(),object_pairs_hook=unique)
def bind(root,pin):
 manifest=root/'PUBLICATION_MANIFEST.json'
 need(stat.S_ISREG(manifest.lstat().st_mode),'regular manifest')
 need(hashlib.sha256(manifest.read_bytes()).hexdigest()==pin,'external outer manifest pin')
 d=load(manifest);need(d['format']=='wreath-hyperfinite-30006166-preprint-v2','outer format')
 rows=d['files'];names=[r['path'] for r in rows]
 need(len(names)==len(set(names)),'unique entries')
 need(all(type(n) is str and n==str(PurePosixPath(n)) and n not in ('','.','PUBLICATION_MANIFEST.json') and not n.startswith('/') and '..' not in PurePosixPath(n).parts and chr(92) not in n for n in names),'safe paths')
 dirs={str(p) for n in names for p in PurePosixPath(n).parents if str(p)!='.'}
 actual_files=set();actual_dirs=set()
 for p in root.rglob('*'):
  mode=p.lstat().st_mode;n=p.relative_to(root).as_posix()
  if stat.S_ISREG(mode):actual_files.add(n)
  elif stat.S_ISDIR(mode):actual_dirs.add(n)
  else:raise RuntimeError('nonregular member: '+n)
 need(actual_files==set(names)|{'PUBLICATION_MANIFEST.json'} and actual_dirs==dirs,'closed repository inventory')
 for r in rows:
  b=(root/r['path']).read_bytes()
  need(type(r['bytes']) is int and len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256'],'member binding: '+r['path'])
 return len(actual_files)
def main():
 a=argparse.ArgumentParser();a.add_argument('trusted_manifest_sha256');a.add_argument('--full',action='store_true');args=a.parse_args()
 root=Path(__file__).absolute().parent;count=bind(root,args.trusted_manifest_sha256)
 pub=root/'publication_20261013';pre=pub/'preprint';package=pub/'verification_package'
 metadata=load(root/'PUBLICATION_METADATA.json');kit=load(pre/'zenodo-deposit.json')
 need(kit['metadata']==load(package/'metadata.json')==metadata['zenodo_metadata'],'current metadata identity')
 need((pre/'note.tex').read_bytes()==(package/'note.tex').read_bytes(),'current note source')
 need((pre/'output/pdf/note.pdf').read_bytes()==(package/'note.pdf').read_bytes(),'current PDF')
 with zipfile.ZipFile(pre/'verification.zip') as z:
  entries=z.infolist();names=[i.filename for i in entries]
  need(len(names)==len(set(names))==metadata['verification_members'],'archive inventory')
  for i in entries:
   n=PurePosixPath(i.filename)
   need(not i.is_dir() and not n.is_absolute() and '..' not in n.parts and str(n)==i.filename and stat.S_ISREG(i.external_attr>>16),'regular safe ZIP member')
   need(z.read(i)==(package/i.filename).read_bytes(),'ZIP/extracted identity')
 frozen=package/'source'
 changed_wrappers={'PUBLICATION_MANIFEST.json','PUBLICATION_METADATA.json','README.md','RESEARCH_LOG.md','verify_publication.py'}
 for p in frozen.rglob('*'):
  if p.is_file() and p.relative_to(frozen).as_posix() not in changed_wrappers:
   need(p.read_bytes()==(root/p.relative_to(frozen)).read_bytes(),'preserved original payload')
 flags=['-I','-B']+(['-O'] if sys.flags.optimize else [])
 cmd=[sys.executable,*flags,str(package/'verify_package.py'),metadata['package_index_sha256']]+(['--full'] if args.full else [])
 r=subprocess.run(cmd,cwd='/',capture_output=True,text=True,timeout=900)
 need(r.returncode==0,'inner package verification: '+r.stderr)
 result={'status':'PASS','regular_files':count,'archive_members_verified':len(entries),'inner':json.loads(r.stdout),'infinite_theorem_verified_by_program':False}
 bind(root,args.trusted_manifest_sha256);print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':main()
'''


def sha(content):
    return hashlib.sha256(content).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', default='r1')
    args = parser.parse_args()
    if not args.label.isalnum():
        raise RuntimeError('Preparation label must be alphanumeric')
    compile(WRAPPER, 'verify_publication.py', 'exec')
    pre = AUDIT / 'preprint'
    sealed = json.loads((AUDIT / 'PACKAGE_SEAL_R1.json').read_bytes())
    for row in sealed['core_files']:
        if sha((pre / row['path']).read_bytes()) != row['sha256']:
            raise RuntimeError('R1 sealed core changed; reseal before assembly')
    work = PROGRAM / 'work'
    work.mkdir(exist_ok=True)
    tree = work / ('pr815_revision_' + args.label)
    if tree.exists():
        raise RuntimeError('Retain existing preparation; choose a fresh revision directory')
    shutil.copytree(AUDIT / 'source', tree)
    publication = tree / 'publication_20261013'
    publication.mkdir()
    extracted = publication / 'verification_package'
    extracted.mkdir()
    with zipfile.ZipFile(pre / 'verification.zip') as archive:
        for info in archive.infolist():
            name = Path(info.filename)
            if name.is_absolute() or '..' in name.parts or info.is_dir() or not stat.S_ISREG(info.external_attr >> 16):
                raise RuntimeError('unsafe archive')
        archive.extractall(extracted)
    for row in sealed['core_files']:
        target = publication / 'preprint' / row['path']
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(pre / row['path'], target)
    build = json.loads((pre / 'BUILD_RECEIPT.json').read_bytes())
    kit = json.loads((pre / 'zenodo-deposit.json').read_bytes())
    metadata = {'format': 'wreath-hyperfinite-30006166-preprint-v2', 'problem_id': 30006166,
                'original_head': sealed['frozen_original_head'], 'original_turns': '3/5',
                'scope': 'dense G_delta in all continuous restricted W Cantor actions, entire Borel orbit relation',
                'AI_assisted': True, 'human_peer_review': False, 'formal_verification': False,
                'historical_firstness_certified': False, 'worldwide_openness_certified': False,
                'verification_members': build['members'], 'package_index_sha256': build['index_sha256'],
                'zenodo_metadata': kit['metadata'],
                'original_immutable_freeze': 'publication_20261013/verification_package/source/',
                'current_preprint': 'publication_20261013/preprint/output/pdf/note.pdf'}
    (tree / 'PUBLICATION_METADATA.json').write_text(json.dumps(metadata, indent=2) + '\n')
    (tree / 'verify_publication.py').write_text(WRAPPER)
    (tree / 'README.md').write_text('''# Generic Cantor actions of Z wr Z are hyperfinite

Problem30006166 / OWR-14299082-012: claimed_solved, original3/5 proof effort. The complete affirmative argument covers the entire Cantor-space orbit relation for a dense G_delta in the space of all continuous restricted Z wr Z actions. This is AI-assisted, unrefereed work; no human refereeing, formal verification, historical firstness or worldwide current-openness certificate is claimed.

The current [five-page note](publication_20261013/preprint/output/pdf/note.pdf), [proof source](publication_20261013/preprint/note.tex), [verification archive](publication_20261013/preprint/verification.zip), and [reproduction instructions](publication_20261013/preprint/README.md) form the preprint package. Existing generic-height principles of AGW, Doucha and DMT are credited explicitly, along with the published Iyer–Shinko baseline and precise CJMST inputs. The full exceptional integer-height preimage is exhausted rather than discarded.

All original author, audit, independent-review and ZIP payloads are preserved. Original top-level wrappers are frozen unchanged inside `publication_20261013/verification_package/source/`; current wrappers enumerate the complete enlarged repository tree. Historical pending-review/no-publication labels remain dated history. `PUBLICATION_TEST_RESULTS.json` retains the original replay evidence; fresh assembled-package evidence and final package-review receipts are in the dedicated shard audit folder on main.

Run `python3 -I -B verify_publication.py TRUSTED_OUTER_MANIFEST_SHA256 --full` from an otherwise intact copy of this folder. The trusted digest comes from the prepared-revision receipt. It checks the outer inventory, current note/metadata identity, every archive/extracted member, original immutable payloads, and portable finite checks. Repeat with `-O` for optimization mode. These computations do not prove the infinite theorem or priority.
''')
    with (tree / 'RESEARCH_LOG.md').open('a') as log:
        log.write('\n## ' + datetime.datetime.now(datetime.timezone.utc).isoformat() + ' — preprint preparation (50%)\n\nFresh independent mathematics and bounded priority audits completed; no proof repair required. Current five-page note adds all required lifting predecessor credits and published baseline citation. Verification package preserves original61 files and3 ZIPs; final package review is a separate gate before merge/publication. Original3/5 effort unchanged.\n')
    rows = []
    for path in sorted(tree.rglob('*')):
        if path.is_file() and path.name != 'PUBLICATION_MANIFEST.json':
            rows.append({'path': path.relative_to(tree).as_posix(), 'bytes': path.stat().st_size,
                         'sha256': sha(path.read_bytes())})
        elif path.is_file() and path.parent != tree:
            rows.append({'path': path.relative_to(tree).as_posix(), 'bytes': path.stat().st_size,
                         'sha256': sha(path.read_bytes())})
    manifest = {'format': 'wreath-hyperfinite-30006166-preprint-v2', 'files': rows}
    (tree / 'PUBLICATION_MANIFEST.json').write_text(json.dumps(manifest, indent=2) + '\n')
    mapping = {'pr': 815, 'problem_id': 30006166, 'expected_head': sealed['frozen_original_head'],
               'original_turns': '3/5', 'final_review_status': 'AWAITING_FRESH_PACKAGE_REVIEWS',
               'findings': 'Complete affirmative resolution of generic Cantor W=Z wr Z whole-space hyperfiniteness; credited lifting predecessors; AI-assisted, unrefereed five-page preprint and verification package; final package review pending.',
               'commit_message': 'Prepare full-target generic wreath hyperfiniteness preprint and verified package',
               'receipt_path': str(AUDIT / 'PREPARED_PR_REVISION_RECEIPT_R1.json'),
               'files': [{'local_path': str(path), 'repo_path': PREFIX + path.relative_to(tree).as_posix(),
                          'sha256': sha(path.read_bytes())} for path in sorted(tree.rglob('*')) if path.is_file()]}
    (AUDIT / 'PREPARED_PR_MAPPING_R1.json').write_text(json.dumps(mapping, indent=2) + '\n')
    receipt = {'timestamp_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
               'tree': str(tree), 'files': len(mapping['files']),
               'outer_manifest_sha256': sha((tree / 'PUBLICATION_MANIFEST.json').read_bytes()),
               'core_seal': 'PACKAGE_SEAL_R1.json', 'Git_or_service_mutations': False}
    (AUDIT / 'LOCAL_PR_ASSEMBLY_R1.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt))


if __name__ == '__main__':
    main()
