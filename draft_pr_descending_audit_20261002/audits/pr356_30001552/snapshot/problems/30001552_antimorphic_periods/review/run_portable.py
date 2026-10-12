from pathlib import Path
from itertools import product
from math import gcd
import argparse,hashlib,json
ap=argparse.ArgumentParser();ap.add_argument('--packet',type=Path,default=Path(__file__).resolve().parent.parent);ap.add_argument('--source-root',type=Path);args=ap.parse_args();n=0
for name,h in json.loads((args.packet/'FINAL_AUTHOR_MANIFEST.json').read_text()).items():assert hashlib.sha256((args.packet/name).read_bytes()).hexdigest()==h;n+=1
if args.source_root:
 for name,h in json.loads((args.packet/'SOURCE_HASHES.json').read_text()).items():assert hashlib.sha256((args.source_root/name).read_bytes()).hexdigest()==h;n+=1
source=Path(__file__).with_name('check_independent.py').read_text();marker='for flip in [0,1]:';assert source.count(marker)==1
exec(compile(marker+source.split(marker,1)[1],str(Path(__file__).with_name('check_independent.py')),'exec'),globals())
