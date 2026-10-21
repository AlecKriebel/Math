#!/usr/bin/env python3
import json
from pathlib import Path
from record_run import run

root=Path(__file__).resolve().parent
python="/opt/homebrew/bin/python3"
results=[]
for kind,folder,filename,gate in (("author","author_replay","verify.py","author"),
                                  ("independent","old_checker_replay","independent_checks.py","independent"),
                                  ("author_repaired","author_suggested_repair","verify.py","author"),
                                  ("independent_repaired","independent_suggested_repair","independent_checks.py","independent"),
                                  ("initial",".","independent_initial.py","initial")):
    for label,options in (("normal",[]),("optimized",["-O"])):
        results.append(run(kind+"_corrupt_cost_"+label,[python,*options,"corrupt_cost_probe.py",gate,str(root/folder/filename)]))
results.append(run("additional_adversary_normal",[python,"additional_adversary.py"]))
results.append(run("additional_adversary_optimized",[python,"-O","additional_adversary.py"]))
(root/"ADDITIONAL_RUN_INDEX.json").write_text(json.dumps(results,indent=2)+"\n")
