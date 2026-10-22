"""Create an exact deterministic support ZIP only at a new external leaf."""
import sys
sys.dont_write_bytecode = True
import argparse
import json
from common import archive_bytes, digest, fresh, write_new

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--output', required=True)
    a = p.parse_args()
    destination = fresh(a.output)
    raw = archive_bytes()
    write_new(destination, raw)
    print(json.dumps({'bytes':len(raw), 'sha256':digest(raw)}))
