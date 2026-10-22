"""Accept only the exact release cleared by a sealed new second review."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import zipfile

P = Path(__file__).resolve().parent
ROOT = P.parent
A = P / 'audits/pr908_30006191'
HEAD = 'a35667b1bb0bafed69916709997a4684223ecc93'
FREEZE = '805791b8ec0fc6e15f7cc707ca77d49cfd904d447ceeed637d7bce181f924ce4'
PACKAGE = 'eff4b4b19c1d931d3f067af7261c315a33452b732ba1c647163e3995804f5b39'
CORRECTED_BODY = '5e765b0801b99feeeb048225706e62c3f16ca842b71e283b6bacb8b198097845'


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def digest(path):
    require(path.is_file() and not path.is_symlink(), 'Nonregular artifact: ' + str(path))
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(args):
    return subprocess.run(args, cwd=ROOT, check=True, capture_output=True,
                          text=True).stdout


def save(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')


def main():
    now = datetime.now(timezone.utc).isoformat()
    pub = A / 'publication'
    require(digest(pub / 'PREPUBLICATION_FREEZE.json') == FREEZE, 'Wrong freeze')
    freeze = json.loads((pub / 'PREPUBLICATION_FREEZE.json').read_text())
    require(freeze['revision_candidate'] == 2 and
            freeze['original_pr_head'] == HEAD and
            freeze['package_manifest_sha256'] == PACKAGE and
            len(freeze['files']) == 13, 'Wrong release scope')
    for name, record in freeze['files'].items():
        file = pub / name
        require(digest(file) == record['sha256'] and file.stat().st_size == record['bytes'],
                'Frozen release drift: ' + name)
    with zipfile.ZipFile(pub / 'bounded-region-fermions-source-verification-v1.0.zip') as archive:
        require(hashlib.sha256(archive.read('PACKAGE_MANIFEST.json')).hexdigest() == PACKAGE,
                'Archive manifest pin changed')
    manifests = {}
    results = {}
    for number in [1, 2]:
        folder = A / 'reviews' / ('full_package_0' + str(number))
        manifest = json.loads((folder / 'MANIFEST.json').read_text())
        records = manifest['intentional_public_files']
        allowlist = manifest.get('explicit_public_allowlist', manifest.get('public_allowlist'))
        require(type(allowlist) is list and
                set(allowlist) - {'MANIFEST.json'} == set(records),
                'Review public allowlist inconsistent')
        require({'RESULT.json', 'AUDIT.md', 'AUTHENTICATION_start.json',
                 'AUTHENTICATION_end.json'} <= set(records),
                'Review verdict/report/endpoints are not sealed')
        for name, record in records.items():
            file = folder / name
            require(digest(file) == record['sha256'] and file.stat().st_size == record['bytes'],
                    'Sealed review drift: ' + str(file))
        manifests[number] = digest(folder / 'MANIFEST.json')
        results[number] = json.loads((folder / 'RESULT.json').read_text())
    require(manifests == {
        1: '39ca8d9572fb4d0504fdde337bea57b2c43740f20d51369b622cc70133cf2ac4',
        2: 'b3f9b72432f831bac749e60598ddf08bb3fa4b1058b1976627cddfe64ef6b55d'},
        'Unexpected sealed whole-package review manifest')
    first, second = results[1], results[2]
    require({r['id'] for r in first['required_issues']} == {'R1'} and
            {r['id'] for r in first['optional_issues']} == {'O1'},
            'Unrecognized first-review finding')
    require(second.get('clean_for_publication') is True and
            second.get('required_issues') == [] and
            second.get('optional_issues') == [],
            'Second review has not cleared every required and optional issue')
    require(second['proof_verdict'] == 'PASS' and
            second['source_binding_verdict'] == 'PASS' and
            second['priority_framing_verdict'] == 'PASS_NO_FIRSTNESS_OR_NOVELTY_CERTIFICATION'
            and second['previous_review_findings']['R1_live_description'] ==
            'REPAIRED_EXACT_LIVE_READBACK' and
            second['previous_review_findings']['O1_README_descriptor_spacing'] == 'REPAIRED',
            'Mathematical, priority, or prior-finding review gate not passed')
    require(second['freeze_sha256'] == FREEZE and
            second['package_manifest_sha256'] == PACKAGE and
            second['original_pr_head'] == HEAD,
            'Second review cleared a different release')
    for phase in ['start', 'end']:
        auth = json.loads((A / 'reviews/full_package_02' /
                           ('AUTHENTICATION_' + phase + '.json')).read_text())
        require(auth['status'] == 'PASS' and auth['freeze_sha256'] == FREEZE and
                auth['package_manifest_sha256'] == PACKAGE and
                auth['original_files_git_disk_archive_identical'] == 26,
                'Second review endpoint authentication failed')
    repair = json.loads((A / 'REVIEW01_REPAIR_RECEIPT.json').read_text())
    require(repair['required_issue'] == 'R1' and repair['optional_issue'] == 'O1' and
            repair['new_body_sha256'] == CORRECTED_BODY and
            repair['live_body_exact_readback'] is True,
            'First-review resolution receipt inconsistent')
    snapshot = json.loads((A / 'ORIGINAL_SNAPSHOT.json').read_text())
    require(snapshot['head'] == HEAD and len(snapshot['files']) == 26,
            'Wrong original packet')
    for name, pin in snapshot['files'].items():
        require(digest(A / 'original' / name) == pin, 'Original disk packet drift')
        raw = subprocess.run(['git', 'show', HEAD + ':' + name], cwd=ROOT,
                             check=True, capture_output=True).stdout
        require(hashlib.sha256(raw).hexdigest() == pin, 'Original Git packet drift')
    pr = json.loads(run(['gh', 'pr', 'view', '908', '--repo', 'AlecKriebel/Math',
                        '--json', 'state,isDraft,headRefOid,headRefName,url,body']))
    require(pr['state'] == 'OPEN' and pr['isDraft'] is True and pr['headRefOid'] == HEAD,
            'Live eligibility changed')
    require(hashlib.sha256(pr['body'].encode('utf-8')).hexdigest() == CORRECTED_BODY,
            'Live corrected body drift')
    queue = run(['gh', 'api', 'repos/AlecKriebel/Math/contents/'
                 'unsolved_math_prioritization/QUEUE.md?ref=' + HEAD,
                 '-H', 'Accept: application/vnd.github.raw+json'])
    rows = [row for row in queue.splitlines() if '| 30006191 /' in row]
    require(len(rows) == 1 and rows[0].split('|')[8].strip() == 'claimed_solved'
            and rows[0].split('|')[9].strip() == '1/5', 'Exact status gate changed')
    parent = run(['git', 'ls-remote', 'origin', 'refs/heads/main']).split()[0]
    run(['git', 'fetch', '--no-write-fetch-head', 'origin', parent])
    source = json.loads((A / 'TARGET_IDENTITY_PREFLIGHT.json').read_text())
    catalogue = json.loads(run(['git', 'show', parent + ':'
                               'unsolved_math_prioritization/catalog.json']))
    target = next(t for t in catalogue if str(t['id']) == '30006191')
    require(target.get('present') is True and target.get('holds') == [] and
            target['statement_hash'] == source['statement_hash'] and
            target['review_hash'] == source['review_hash'],
            'Current main source identity or review holds changed')
    accepted = {
        'utc': now, 'accepted': True, 'original_pr_head': HEAD,
        'live_gate_status': 'claimed_solved', 'original_attempt_turns': '1/5',
        'candidate_revision': 2, 'freeze_sha256': FREEZE,
        'package_manifest_sha256': PACKAGE, 'files': freeze['files'],
        'exact_claim': 'Explicit fixed smooth compactly supported radial pair potential, '
                       'fixed ball and fixed smooth mode in d=3: both literal unsmeared '
                       'orderings admit changing unit Slaters and specified times '
                       'with directional annihilation vector limit, vector/operator/'
                       'creation norm 2 and changing normal-state squared value 4; '
                       'every fixed vector and normal state remains continuous.',
        'proof_gap': 'None found in the precise inspected existential model.',
        'source_scope': 'OWR7/2025 printed p.371 fermionic bounded-region question; '
                        'operator-norm versus strong topology fixed at p.365.',
        'priority': 'Earlier Siebert arXiv:2609.34402v1 mechanism and direct qualitative '
                    'cutoff adaptation credited. Additional audit-time energy bootstrap '
                    'recovers maximal cutoff limit and is not a theorem stated in that '
                    'source. First priority, quantitative novelty and continued openness '
                    'are not asserted; bounded coverage gaps disclosed.',
        'full_package_reviews': [
            {'round': 1, 'clean_context': True, 'manifest_sha256': manifests[1],
             'required_repairs': ['R1 live PR metadata'],
             'optional_improvements': ['O1 editorial word/number spacing'],
             'globally_resolved': True, 'evidence': 'REVIEW01_REPAIR_RECEIPT.json'},
            {'round': 2, 'clean_context': True, 'manifest_sha256': manifests[2],
             'required_repairs': [], 'optional_improvements': [],
             'clean_for_publication': True, 'freeze_sha256': FREEZE}],
        'AI_assisted': True, 'unrefereed': True,
        'independent_human_peer_review': False,
        'formal_machine_proof_certification': False,
        'merge_and_publication_authorized_by_user': True}
    save(A / 'ACCEPTANCE.json', accepted)
    (A / 'ACCEPTANCE.md').write_text(
        'Accept the exact bounded-region d=3 existential result and unchanged original '
        'packet after two sequential fresh whole-package adversarial reviews. The '
        'first review\'s live metadata correction and optional spacing improvements '
        'are globally resolved; the new second review reports no remaining issue. '
        'Credit the earlier cluster/phase mechanism, direct qualitative cutoff '
        'adaptation and separately identified audit bootstrap. First priority, '
        'quantitative novelty and continued openness are not asserted. Publish '
        'the exact frozen candidate2 note and verification archive using its '
        'reviewed descriptor, with extensive AI/unrefereed/no-human-review '
        'disclosures and original 1/5 attempt count preserved.\n')
    save(A / 'FINAL_ACCEPTANCE_GATE.json', {
        'utc': now, 'pr': {k: v for k, v in pr.items() if k != 'body'},
        'corrected_body_sha256': CORRECTED_BODY, 'remote_main': parent,
        'source_identity_unchanged': True, 'review_manifests': manifests,
        'original_files_unchanged': 26, 'freeze_sha256': FREEZE,
        'exact_queue_status': 'claimed_solved'})
    state = json.loads((P / 'CURRENT_STATE.json').read_text())
    state.update(utc=now, phase='PR908_accepted_merge_and_publish_next',
                 active_pr_completion_estimate_percent=96,
                 shard_completion_estimate_percent=(3 + .96) / 12 * 100)
    save(P / 'CURRENT_STATE.json', state)
    for log in [A / 'RESEARCH_LOG.md', P / 'RESEARCH_LOG.md']:
        with log.open('a') as out:
            out.write('\n' + now + ' — PR908 accepted (96% workflow; shard33%): '
                      'both sequential fresh reviews authenticated; R1/O1 resolved '
                      'globally and review02 clean. Exact frozen files, original26, '
                      'live corrected body, claimed_solved1/5 and current source/holds '
                      'all unchanged. Merge and exact-metadata publication next.\n')
    print(json.dumps({'accepted': True, 'freeze_sha256': FREEZE,
                      'live_status': 'claimed_solved'}, indent=2))


if __name__ == '__main__':
    main()
