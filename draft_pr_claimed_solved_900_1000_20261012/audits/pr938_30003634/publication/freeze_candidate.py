#!/usr/bin/env python3
"""Freeze the review candidate only after live eligibility and all local gates."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import zipfile

P = Path(__file__).resolve().parent
A = P.parent
ROOT = A.parents[2]
HEAD = '2b3ea2de7a9a9ea4fa8cba9a34cbdb01063bda3b'


def require(condition, label):
    if not condition:
        raise RuntimeError(label)


def command(args):
    return subprocess.run(args, cwd=ROOT, check=True, capture_output=True,
                          text=True).stdout.strip()


def fp(path):
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def main():
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--revision',type=int,default=1);args=ap.parse_args()
    require(args.revision>=1,'Bad candidate revision')
    pr = json.loads(command(['gh', 'pr', 'view', '938', '--repo', 'AlecKriebel/Math',
            '--json', 'number,state,isDraft,headRefOid,headRefName,baseRefName']))
    require(pr['state'] == 'OPEN' and pr['isDraft'] is True and pr['headRefOid'] == HEAD
            and pr['baseRefName'] == 'main', 'Live draft/head gate changed')
    command(['git', 'fetch', '--no-write-fetch-head', 'origin', HEAD])
    queue = command(['git', 'show', HEAD+':unsolved_math_prioritization/QUEUE.md'])
    rows = [line for line in queue.splitlines() if line.startswith('|') and
            len(line.split('|')) > 8 and line.split('|')[2].strip().split(' / ')[0] == '30003634']
    require(len(rows) == 1 and rows[0].split('|')[8].strip() == 'claimed_solved',
            'Immutable PR-head status is not exactly claimed_solved')
    main_sha = command(['git', 'ls-remote', 'origin', 'refs/heads/main']).split()[0]
    command(['git', 'fetch', '--no-write-fetch-head', 'origin', main_sha])
    catalog = json.loads(command(['git', 'show', main_sha+':unsolved_math_prioritization/catalog.json']))
    targets = [x for x in catalog if str(x['id']) == '30003634']
    require(len(targets) == 1, 'Ambiguous target')
    target = targets[0]
    source = json.loads((A/'TARGET_IDENTITY_PREFLIGHT.json').read_text())
    require(target['present'] is True and target['holds'] == [] and
            target['review_hash'] == source['review_hash'] and
            target['statement_hash'] == source['statement_hash'], 'Source identity/holds changed')
    built = json.loads((P/'BUILD_RECEIPT.json').read_text())
    modes = ['normal', 'O', 'OO', 'env2']
    replays = [json.loads((P/('PACKAGE_REPLAY_'+m+'.json')).read_text()) for m in modes]
    require(all(x['status'] == 'PASS' and x['package_manifest_sha256'] == built['manifest_sha256']
                and x['worker_optimization'] == 0 for x in replays), 'Replay gate not current')
    require(all(x == replays[0] for x in replays), 'Outer optimization changes replay result')
    guards = json.loads((P/'PACKAGE_GUARD_CHALLENGES.json').read_text())
    require(guards['status'] == 'PASS' and guards['hostile_inventory_runs'] == 140 and
            guards['false_assertion_child_runs'] == 4 and
            guards['package_manifest_sha256'] == built['manifest_sha256'], 'Guard gate not current')
    copy_guard = json.loads((P/'COPY_GUARD_CHALLENGE.json').read_text())
    require(copy_guard['status'] == 'PASS' and copy_guard['tampered_copy_runs'] == 4 and
            copy_guard['all_copies_rejected_before_execution'] is True and
            copy_guard['package_manifest_sha256'] == built['manifest_sha256'], 'Copy authentication gate not current')
    qa = json.loads((P/'PDF_VISUAL_QA.json').read_text())
    require(qa['all_pages_pass'] is True and qa['pages'] == 4 and
            qa['source_sha256'] == fp(P/'note.tex')['sha256'] and
            qa['pdf_sha256'] == fp(P/'output/pdf/note.pdf')['sha256'], 'PDF gate not current')
    live_body = command(['gh', 'pr', 'view', '938', '--repo', 'AlecKriebel/Math', '--json', 'body,title'])
    live_description = json.loads(live_body)
    require(live_description['body'] == (A/'PR_DESCRIPTION_CORRECTED.md').read_text(), 'Live description differs from repaired scope')
    archive = P/'deep-derived-pure-braids-source-verification-v1.0.zip'
    with zipfile.ZipFile(archive) as z:
        require(len(z.namelist()) == len(set(z.namelist())) == built['zip_members'],
                'Archive membership mismatch')
        require(z.read('note.pdf') == (P/'output/pdf/note.pdf').read_bytes(), 'Archive PDF differs')
        require(hashlib.sha256(z.read('PACKAGE_MANIFEST.json')).hexdigest() == built['manifest_sha256'],
                'Archive manifest differs')
        snapshot = json.loads((A/'ORIGINAL_SNAPSHOT.json').read_text())
        prefix = 'unsolved_math_prioritization/attempts/30003634/'
        for name, expected in snapshot['files'].items():
            require(hashlib.sha256(z.read('original_packet/'+name[len(prefix):])).hexdigest() == expected,
                    'Archive original file differs')
    metadata_check = subprocess.run(['python3', str(ROOT/'zenodo_deposit_tool/zenodo.py'),
                'check', str(P/'zenodo-deposit.json')], cwd=ROOT, check=True,
                capture_output=True, text=True)
    (P/'LOCAL_ZENODO_CHECK.json').write_text(metadata_check.stdout)
    files = ['note.tex', 'output/pdf/note.pdf', archive.name, 'README.md',
             'requirements.txt', 'verify_package.py', 'run_checked.py', 'zenodo-deposit.json',
             'build_package.py', 'package_guard_challenges.py', 'replay_all_modes.py',
             'freeze_candidate.py', 'copy_guard_challenge.py', 'prepare_metadata.py','PDF_VISUAL_QA.json','BUILD_RECEIPT.json','PACKAGE_GUARD_CHALLENGES.json','COPY_GUARD_CHALLENGE.json']+[('PACKAGE_REPLAY_'+m+'.json') for m in modes]
    freeze = {'utc': datetime.now(timezone.utc).isoformat(), 'pr': 938, 'problem_id': '30003634',
              'revision_candidate': args.revision, 'original_pr_head': HEAD,
              'original_candidate_turns': '1/5 unchanged', 'current_known_turns':'2/5, one separately recorded complete stronger mechanism', 'original_files_unchanged': 44,
              'files': {name: fp(P/name) for name in files},
              'package_manifest_sha256': built['manifest_sha256'], 'pdf_pages': 4,
              'live_eligibility': {'pr': pr, 'queue_row': rows[0], 'status': 'claimed_solved',
                                  'remote_main': main_sha, 'source_hashes_and_holds_match': True,
                                  'live_description_sha256': hashlib.sha256(live_description['body'].encode()).hexdigest(),
                                  'live_description_exact_readback': True},
              'local_gates': {'full_replays': modes, 'all_replays_identical': True,
                              'hostile_inventory_runs': 140, 'false_assertion_child_runs': 4,
                              'post_copy_corruption_runs_rejected_before_execution': 4,
                              'all_pdf_pages_visual_pass': True, 'local_zenodo_check_pass': True},
              'priority': 'Every finite derived depth outside integral smoothF1; prior general signature/quasimorphism tools explicitly credited, including Kawasaki etal2025Lemma7.12. Bounded primary search established no complete predecessor; no firstness/current-openness or new general group lemma claim.',
              'acceptance': 'REVIEWABLE_ALL_DEPTH_CANDIDATE_PENDING_NEW_SEQUENTIAL_FULL_PACKAGE_REVIEWS',
              'candidate_editing_stops_until_review_findings': True}
    helpers=['accept_pr938.py','merge_pr938.py','run_pr938_zenodo.py','append_pr938_tracker.py','update_pr938_publication_ledger.py','finalize_pr938_and_gate_next.py']
    freeze['future_helpers']={n:fp(ROOT/'draft_pr_claimed_solved_900_1000_20261012'/n) for n in helpers}
    freeze['pr_description_sha256']=hashlib.sha256(live_description['body'].encode()).hexdigest()
    (P/'PREPUBLICATION_FREEZE.json').write_text(json.dumps(freeze, indent=2)+'\n')
    import shutil
    snapshot=P/'reviewed_candidates'/('candidate'+str(args.revision).zfill(2))
    require(not snapshot.exists(),'Candidate snapshot exists; preserve it')
    snapshot.mkdir(parents=True)
    for n in files+['PREPUBLICATION_FREEZE.json']:
        q=snapshot/n;q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(P/n,q)
    (snapshot/'future_helpers').mkdir()
    for n in helpers:shutil.copyfile(ROOT/'draft_pr_claimed_solved_900_1000_20261012'/n,snapshot/'future_helpers'/n)
    print(json.dumps({'freeze_sha256': fp(P/'PREPUBLICATION_FREEZE.json')['sha256'],
                      'package_manifest_sha256': built['manifest_sha256'],
                      'frozen_files': len(files), 'live_status': 'claimed_solved'}, indent=2))


if __name__ == '__main__':
    main()
