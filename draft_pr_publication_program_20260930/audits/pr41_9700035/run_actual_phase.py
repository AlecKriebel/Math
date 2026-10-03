"""ROOT dispatches one explicitly selected phase with inspected immutable pins."""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys

A = Path(__file__).resolve().parent
R = A.parents[2]
H = A / 'acceptance_preparation_family_v2'
SOURCES = {'preflight':('integrate_reviewed_partial.py','288119d8236e19616645c3d9c18dc6bc53ddd10623fb5bcb89ade2a1e88b77bf'),
           'overlay':('integrate_reviewed_partial.py','288119d8236e19616645c3d9c18dc6bc53ddd10623fb5bcb89ade2a1e88b77bf'),
           'prepush':('integrate_reviewed_partial.py','288119d8236e19616645c3d9c18dc6bc53ddd10623fb5bcb89ade2a1e88b77bf'),
           'finalize':('integrate_reviewed_partial.py','288119d8236e19616645c3d9c18dc6bc53ddd10623fb5bcb89ade2a1e88b77bf'),
           'mirror':('state_mirror_reconciliation.py','38b24733b5e257598e7db20c5a32d590ca0c87e529fdfeb3d31ffd7252e46de6'),
           'post':('verify_post_acceptance.py','48b78bfd9f24025e0aa2530e59493ccfcddba0f7890dcacbf8efa38efadfd1cc')}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('phase', choices=SOURCES)
    parser.add_argument('runtime_sha256')
    parser.add_argument('--merge-queue-preimage-sha256')
    args = parser.parse_args()
    p = A / 'ROOT_ACCEPTANCE_RUNTIME_INPUTS.json'; raw = p.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == args.runtime_sha256
    config = json.loads(raw)
    helper, source_sha = SOURCES[args.phase]
    flags = ['--execute', '--preparation-manifest-sha256', config['preparation_manifest_sha256']]
    assert set(config['inputs']) == {'final-plan','final-receipt','final-manifest','reconciliation-capture','previous-mirror','previous-post','fresh-preimage','root-bindings'}
    for name, row in config['inputs'].items():
        assert hashlib.sha256((R / row['path']).read_bytes()).hexdigest() == row['sha256']
        flags += ['--'+name, row['path'], '--'+name+'-sha256', row['sha256']]
    if args.phase in ('preflight','overlay','prepush','finalize'): flags.append(args.phase)
    if args.phase == 'overlay':
        assert args.merge_queue_preimage_sha256
        flags += ['--merge-queue-preimage-sha256',args.merge_queue_preimage_sha256]
    else: assert args.merge_queue_preimage_sha256 is None
    argv = ['/usr/bin/python3','-B',str(A/'capture_actual_helper.py'),
            'root_integration_'+args.phase+'_actual_capture',str(H/helper),source_sha,'--',*flags]
    return subprocess.call(argv,cwd=A)


if __name__ == '__main__': sys.exit(main())
