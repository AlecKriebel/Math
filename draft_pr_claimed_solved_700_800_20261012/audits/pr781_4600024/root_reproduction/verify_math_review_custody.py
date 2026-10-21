#!/usr/bin/env python3
"""Mandatory root custody check for the two frozen PR781 mathematical audits.
The symbolic family's historical checker uses removable assertions; this checker
uses explicit exceptions in ordinary and optimized modes and external pins.
"""
from pathlib import Path
import argparse,hashlib,json,stat,os,tempfile
ROOT=Path(__file__).resolve().parent.parent
PINS={"math_automata":"1ecc38a1b833a605a0ef87a937d8cd7d5254d52390b9a98641cf9956aecbb45f",
      "math_symbolic":"7501cc0ac252abc1a3d14ce28f73ee6d8ed81344b68e3f78e4ea7dd430639bcb"}
def need(value,message):
 if not value:raise ValueError(message)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def unique(pairs):
 d={}
 for k,v in pairs:need(k not in d,"duplicate JSON key");d[k]=v
 return d
def nonfinite(value):raise ValueError("nonfinite JSON")
def regular(path):
 need(stat.S_ISREG(path.lstat().st_mode),"nonregular member:"+str(path))
 return path.read_bytes()
def verify(name):
 folder=ROOT/name;mraw=regular(folder/"MANIFEST.json");need(sha(mraw)==PINS[name],"external review manifest pin")
 m=json.loads(mraw,object_pairs_hook=unique,parse_constant=nonfinite)
 if name=="math_automata":expected={k:{"sha256":v} for k,v in m["files"].items()};inputs=m["source_snapshot_sha256"]
 else:expected={v["path"]:v for v in m["authored_files"]};inputs={v["path"]:v["sha256"] for v in m["immutable_inputs"]}
 need(all(Path(k).name==k and k not in {".","..","MANIFEST.json"} for k in expected),"unsafe member name")
 actual={p.name for p in folder.iterdir()};need(actual==set(expected)|{"MANIFEST.json"},"exact review closure")
 for k,v in expected.items():
  raw=regular(folder/k);need(sha(raw)==v["sha256"],"review member hash:"+k)
  if "bytes" in v:need(len(raw)==v["bytes"],"review member bytes:"+k)
 for rel,h in inputs.items():
  p=ROOT/rel;need(p.resolve().is_relative_to(ROOT),"input escape");need(sha(regular(p))==h,"input digest:"+rel)
 return {"review":name,"status":"PASS","authored_files_excluding_manifest":len(expected),"source_inputs":len(inputs),"manifest_sha256":PINS[name]}
if __name__=="__main__":print(json.dumps({"status":"PASS","reviews":[verify(n) for n in PINS],"enforcement":"Explicit exceptions; externally pinned manifests; exact flat regular-file closure; immutable input hashes."},sort_keys=True))
