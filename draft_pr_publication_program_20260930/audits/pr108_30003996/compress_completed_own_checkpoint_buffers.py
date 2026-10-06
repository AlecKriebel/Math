#!/usr/bin/env python3
"""Losslessly retain specified private completed-checkpoint buffers; never touch sources or tracked files."""
from pathlib import Path
import argparse, datetime, gzip, hashlib, json, os, shutil, subprocess

A = Path(__file__).resolve().parent
C = A.parents[2]
BATCHES = {
    'pr107': ('pr107_30003997', ['94.stdout.bin', '87.stdout.bin', '96.stdout.bin'], 'ROOT_COMPLETED_PRIVATE_BUFFER_COMPRESSION_20261006.json'),
    'pr104': ('pr104_600008', ['150.stdout.bin', '143.stdout.bin', '152.stdout.bin'], 'ROOT_COMPLETED_PR104_PRIVATE_BUFFER_COMPRESSION_20261006.json'),
}

def require(ok, why):
    if not ok:
        raise RuntimeError(why)

def digest(path, compressed=False):
    h = hashlib.sha256(); n = 0
    opener = gzip.open if compressed else open
    with opener(path, 'rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(chunk); n += len(chunk)
    return n, h.hexdigest()

def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--batch', choices=sorted(BATCHES), default='pr107'); args = parser.parse_args()
    effort, NAMES, receipt_name = BATCHES[args.batch]
    BASE = C / 'draft_pr_publication_program_20260930/audits' / effort / 'actual_checkpoints/native_prior_disposition_release'
    RECEIPT = A / receipt_name
    require(not RECEIPT.exists(), 'Do not repeat compression')
    start = datetime.datetime.now(datetime.timezone.utc).isoformat()
    free_before = shutil.disk_usage(A).free
    rows = []
    for name in NAMES:
        original = BASE / name; compressed = BASE / (name + '.gz')
        require(original.is_file() and not original.is_symlink() and not compressed.exists(), 'Exact original private file')
        rel = str(original.relative_to(C))
        check = subprocess.Popen(['git', 'ls-files', '--error-unmatch', '--', rel], cwd=C, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        check.communicate()
        require(check.returncode == 1, 'File must be untracked')
        n, original_sha = digest(original)
        with original.open('rb') as source, compressed.open('xb') as destination:
            with gzip.GzipFile(filename=name, mode='wb', fileobj=destination, compresslevel=9, mtime=0) as packed:
                shutil.copyfileobj(source, packed, 1024 * 1024)
            destination.flush(); os.fsync(destination.fileno())
        restored_n, restored_sha = digest(compressed, compressed=True)
        require((restored_n, restored_sha) == (n, original_sha), 'Complete byte-for-byte roundtrip before removing duplicate')
        packed_n, packed_sha = digest(compressed)
        row = {'original_path': rel, 'original_bytes': n, 'original_sha256': original_sha,
               'compressed_path': str(compressed.relative_to(C)), 'compressed_bytes': packed_n, 'compressed_sha256': packed_sha,
               'actual_git_track_check_PID': check.pid, 'actual_git_track_check_exit': check.returncode,
               'roundtrip_verified_before_raw_removal': True, 'file_was_untracked': True}
        rows.append(row)
        # Persist complete recovery information before the raw private duplicate is removed.
        receipt = {'schema': 'pr108-lossless-own-completed-checkpoint-buffer-retention/v1',
                   'actual_operator_PID': os.getpid(), 'UTC_start': start, 'batch': args.batch,
                   'rows': rows, 'research_source_files_modified': False, 'tracked_files_modified': False,
                   'active_native_inputs_modified': False, 'browser_cache_or_credentials_touched': False}
        RECEIPT.write_text(json.dumps(receipt, indent=2) + '\n')
        original.unlink()
    receipt.update({'UTC_end': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                    'logical_bytes_saved': sum(r['original_bytes'] - r['compressed_bytes'] for r in rows),
                    'free_bytes_before': free_before, 'free_bytes_after': shutil.disk_usage(A).free,
                    'restore_utility': 'restore_completed_own_checkpoint_buffers.py', 'restore_batch': args.batch})
    RECEIPT.write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps({k: receipt[k] for k in ['logical_bytes_saved', 'free_bytes_before', 'free_bytes_after']}))

if __name__ == '__main__':
    main()
