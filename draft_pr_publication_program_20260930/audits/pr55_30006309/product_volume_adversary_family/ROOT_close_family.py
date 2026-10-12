"""ROOT alone may run this after personal mathematical and SOURCE reading."""
import argparse
import json
import os
from packet_common import HERE, SELF, row, validate, timestamp

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root-read-assertion', required=True)
    args = parser.parse_args()
    assert args.root_read_assertion.strip()
    assert not (HERE / SELF).exists()
    index, ready, files = validate(False)
    # SOURCE builder already froze only owned payload files. No native, Git or
    # remote state is modified; external references are read only.
    assert all(row(p)['mode'] == 0o444 for p in files)
    mf = {'schema': 'pr55-product-volume-adversary-self-manifest/v1', 'utc': timestamp(),
          'actual_closer_pid': os.getpid(), 'ROOT_execution_assertion': args.root_read_assertion,
          'ROOT_personal_read_not_inferred_from_integrity': True,
          'prepared_files': len(files), 'files': [row(p) for p in files],
          'directories': index['directories'], 'index_sha256': row(HERE / 'INDEX.json')['sha256'],
          'ready_sha256': row(HERE / 'READY.json')['sha256'],
          'native_acceptance_authority': False, 'Git_or_remote_action_authority': False}
    with (HERE / SELF).open('x') as f:
        f.write(json.dumps(mf, indent=2) + '\n')
    (HERE / SELF).chmod(0o444)
    validate(True)
    print(json.dumps({'status': 'PASS_ROOT_CLOSED_PRODUCT_VOLUME_ADVERSARY', 'actual_closer_pid': os.getpid(),
                      'self_manifest': row(HERE / SELF)}, sort_keys=True))

if __name__ == '__main__':
    main()
