#!/usr/bin/env python3
import json
from pathlib import Path
from record_run import run

root=Path(__file__).resolve().parent
python="/opt/homebrew/bin/python3"
results=[]
for kind,folder in (("author","author_replay"),("author_repaired","author_suggested_repair")):
    for label,options in (("normal",[]),("optimized",["-O"])):
        results.append(run(kind+"_cycle_"+label,[python,*options,"cycle_guard_probe.py",str(root/folder/"verify.py")]))
(root/"CYCLE_RUN_INDEX.json").write_text(json.dumps(results,indent=2)+"\n")
