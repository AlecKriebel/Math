"""A separate ROOT process performs complete readback after ROOT closure."""
import json
import os
from packet_common import HERE, SELF, row, validate

def main():
    index, ready, files = validate(True)
    mf = json.loads((HERE / SELF).read_text())
    assert os.getpid() != mf['actual_closer_pid']
    print(json.dumps({'status': 'PASS_ROOT_READ_CLOSED_PRODUCT_VOLUME_ADVERSARY',
                      'actual_reader_pid': os.getpid(), 'file_count_including_self_manifest': len(files),
                      'self_manifest_sha256': row(HERE / SELF)['sha256']}, sort_keys=True))

if __name__ == '__main__':
    main()
