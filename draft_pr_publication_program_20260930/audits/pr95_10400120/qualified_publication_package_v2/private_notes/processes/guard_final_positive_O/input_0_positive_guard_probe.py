from pathlib import Path
import json,runpy,sys
p=Path(sys.argv[1])
d=runpy.run_path(str(p/'verification/run_all.py'))
print(json.dumps(d['guard'](),sort_keys=True))
