from pathlib import Path
from fractions import Fraction as F
from itertools import permutations
import argparse,json,hashlib
ap=argparse.ArgumentParser();ap.add_argument('--packet',type=Path,default=Path(__file__).resolve().parent.parent);ap.add_argument('--source-root',type=Path);args=ap.parse_args();n=0
for f,h in json.loads((args.packet/'FINAL_AUTHOR_MANIFEST.json').read_text()).items():assert hashlib.sha256((args.packet/f).read_bytes()).hexdigest()==h;n+=1
if args.source_root:
 for manifest in ['SOURCE_HASHES.json','ADDITIONAL_SOURCE_HASHES.json']:
  for f,h in json.loads((args.packet/manifest).read_text()).items():assert hashlib.sha256((args.source_root/f).read_bytes()).hexdigest()==h;n+=1
source=Path(__file__).with_name('check_independent.py').read_text();marker='# Exact valuation inequalities';assert source.count(marker)==1
exec(compile(marker+source.split(marker,1)[1],str(Path(__file__).with_name('check_independent.py')),'exec'),globals())
