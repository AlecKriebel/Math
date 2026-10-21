"""Read back a real shard release; never mutate Git, services, or source inputs."""
from pathlib import Path
import argparse
import datetime
import hashlib
import json
import os
import stat
import subprocess
import sys

D = Path(__file__).resolve().parent.parent
REPO = D.parent
OUT = D / 'final_completion_20261017/closure_20261017'
sys.path.insert(0, str(REPO / 'zenodo_deposit_tool'))
import zenodo as z


def need(condition, message):
    if not condition:
        raise RuntimeError(message)


def read(path):
    return json.loads(path.read_text())


def run(*argv):
    return subprocess.check_output(argv, cwd=REPO, timeout=90)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('output_name')
    parser.add_argument('--strict-current', action='store_true')
    args = parser.parse_args()
    output = OUT / args.output_name
    need(output.parent == OUT and not output.exists(), 'Preserve prior verification evidence')
    receipt = read(D / 'LATEST_PUSH_RECEIPT.json')
    commit, parent = receipt['commit'], receipt['parent']
    need(receipt['shared_index_bytes_unchanged'] and not receipt['force_push'], 'Release boundary failed')
    remote_commit = json.loads(run('gh', 'api', f'repos/AlecKriebel/Math/git/commits/{commit}'))
    need(remote_commit['sha'] == commit and remote_commit['tree']['sha'] == receipt['tree'] and
         [p['sha'] for p in remote_commit['parents']] == [parent], 'Actual remote commit differs')
    ancestry = json.loads(run('gh', 'api', f'repos/AlecKriebel/Math/compare/{commit}...main',
                             '--jq', '{status, ahead_by, behind_by, merge_base: .merge_base_commit.sha}'))
    need(ancestry['status'] in ('identical', 'ahead') and ancestry['merge_base'] == commit,
         'Released commit is not confirmed on main')
    tree = {}
    for item in run('git', 'ls-tree', '-r', '-z', '--full-tree', commit, '--', D.name).split(b'\0'):
        if item:
            info, path = item.split(b'\t', 1)
            mode, kind, oid = info.decode().split()
            need(kind == 'blob', 'Unexpected non-file release entry')
            tree[os.fsdecode(path)] = (mode, oid)
    root_entry = run('git', 'ls-tree', commit, '--', D.name).decode().split()[2]
    remote_subtree = run('gh', 'api', 'repos/AlecKriebel/Math/git/trees/main', '--jq',
                         '.tree[] | select(.path == "' + D.name + '") | .sha').decode().strip()
    need(root_entry == remote_subtree, 'Current main shard tree differs from released snapshot')
    changed = run('git', 'diff-tree', '--no-commit-id', '--name-only', '-r', parent, commit).decode().splitlines()
    need(changed and all(p.startswith(D.name + '/') for p in changed), 'Release changed another program')
    private = [p for p in tree if p.startswith(D.name + '/audits/') and
               ('/sources/raw/' in p or '/sources/rawprivate/' in p or '/sources/raw_private/' in p or
                ('/service_receipts_20261016/' in p and
                 (p.endswith('/COMMANDS.jsonl') or
                  (Path(p).name.startswith('COMMANDS') and p.endswith('.jsonl.gz')))) or
                (p.startswith(D.name + '/audits/pr1032_30001739/reviews/package_') and '/source_renders/' in p))]
    need(not private, 'Private live data entered release tree')
    object_format = run('git', 'rev-parse', '--show-object-format').decode().strip()

    def binding(path):
        path = Path(path)
        relative = str(path.relative_to(REPO))
        mode = path.lstat().st_mode
        if stat.S_ISLNK(mode):
            payload, expected_mode = os.fsencode(os.readlink(path)), '120000'
        else:
            need(stat.S_ISREG(mode), 'Unsupported working file')
            payload = path.read_bytes()
            expected_mode = '100755' if mode & 0o111 else '100644'
        oid = hashlib.new(object_format, b'blob ' + str(len(payload)).encode() + b'\0' + payload).hexdigest()
        need(tree.get(relative) == (expected_mode, oid), 'Released bytes differ: ' + relative)

    state = read(D / 'STATE.json')
    need(len(state['completed_prs']) == 18 and state['next_pr'] is None, 'Incomplete workflow state')
    stable = {D / 'FINAL_REPORT.md'}
    audit_folder = D / 'final_completion_20261017/attempt_01'
    stable.update(p for p in audit_folder.iterdir() if p.is_file())
    for n in state['completed_prs']:
        folder = next((D / 'audits').glob(f'pr{n}_*'))
        cfg = D / f'service_resume_20261016/PR{n}_SERVICE_CONFIG.json'
        manifest = D / read(cfg)['manifest'] if cfg.exists() else folder / 'publication/zenodo-deposit.json'
        stable.add(manifest)
        _, files = z.load_manifest(manifest.resolve())
        verified = read(audit_folder / f'NATIVE_AND_MERGE_PR{n}.json')
        need([(f['name'], f['size'], f['sha256']) for f in files] ==
             [(f['name'], f['bytes'], f['sha256']) for f in verified['files']], 'Published file binding drift')
        stable.update(f['path'] for f in files)
    for path in stable:
        binding(path)
    public_count = None
    if args.strict_current:
        paths = []
        for base, dirs, names in os.walk(D, followlinks=False):
            for name in list(dirs):
                p = Path(base) / name
                if p.is_symlink():
                    paths.append(p)
                    dirs.remove(name)
            paths.extend(Path(base) / name for name in names)
        relatives = [str(p.relative_to(REPO)) for p in paths]
        ignored = subprocess.run(['git', 'check-ignore', '--no-index', '-z', '--stdin'], cwd=REPO,
                                 input=b'\0'.join(os.fsencode(p) for p in relatives) + b'\0', capture_output=True)
        need(ignored.returncode in (0, 1), 'Git ignore read failed')
        ignored_paths = {os.fsdecode(p) for p in ignored.stdout.split(b'\0') if p}
        # This generated receipt necessarily records the preceding checkpoint.
        self_receipt = str((D / 'LATEST_PUSH_RECEIPT.json').relative_to(REPO))
        public = [(p, r) for p, r in zip(paths, relatives) if r not in ignored_paths and r != self_receipt]
        need({r for _, r in public} == set(tree) - {self_receipt}, 'Current public release file-set drift')
        for path, _ in public:
            binding(path)
        public_count = len(public)
    baseline = read(OUT / 'RELEASE_PREFLIGHT.json')
    branch = run('git', 'branch', '--show-current').decode().strip()
    head = run('git', 'rev-parse', 'HEAD').decode().strip()
    index = Path(run('git', 'rev-parse', '--git-path', 'index').decode().strip())
    index = index if index.is_absolute() else REPO / index
    index_hash = hashlib.sha256(index.read_bytes()).hexdigest()
    need(branch == 'main' and head == baseline['shared_head'] and index_hash == baseline['shared_index_sha256'],
         'Shared checkout HEAD/index changed during isolated release')
    result = {'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'status': 'PASS_ACTUAL_REMOTE_MAIN_RELEASE_READBACK', 'commit': commit, 'parent': parent,
              'tree': receipt['tree'], 'shard_tree': root_entry, 'remote_ancestry': ancestry,
              'changed_paths_only_this_program': len(changed), 'private_live_data_paths_absent': True,
              'stable_published_assets_manifests_audit_and_report_bound': len(stable),
              'strict_current_public_file_set_and_bytes_checked': args.strict_current,
              'current_public_files_checked': public_count, 'self_referential_latest_receipt_exception': True,
              'shared_branch': branch, 'shared_head': head, 'shared_index_sha256': index_hash,
              'shared_checkout_unchanged': True, 'no_remote_or_source_mutation_by_verifier': True}
    output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result), flush=True)


if __name__ == '__main__':
    main()
