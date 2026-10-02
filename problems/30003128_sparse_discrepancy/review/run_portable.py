"""Additive portable runner; preserves the frozen review algorithm unchanged."""
import argparse,itertools,json,hashlib,pathlib
from fractions import Fraction as F
ap=argparse.ArgumentParser();ap.add_argument('--packet',type=pathlib.Path,default=pathlib.Path(__file__).resolve().parents[1]);ap.add_argument('--source-root',type=pathlib.Path);args=ap.parse_args();count=0
m=json.loads((args.packet/'MANIFEST.json').read_text())['files']
for name,h in m.items():
 assert hashlib.sha256((args.packet/name).read_bytes()).hexdigest()==h;count+=1
if args.source_root:
 for name,h in json.loads((args.packet/'SOURCE_HASHES.json').read_text()).items():
  assert hashlib.sha256((args.source_root/name).read_bytes()).hexdigest()==h;count+=1
# Run the literal frozen mathematical fixture loop. Only local path/hash setup is replaced.
src=pathlib.Path(__file__).with_name('check_independent.py').read_text();marker='for q,k in '
assert src.count(marker)==1
body=marker+src.split(marker,1)[1]
exec(compile(body,'frozen_review_fixtures','exec'),globals())
