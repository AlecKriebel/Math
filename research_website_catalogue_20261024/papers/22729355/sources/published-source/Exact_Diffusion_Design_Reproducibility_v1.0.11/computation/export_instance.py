#!/usr/bin/env python3
"""Export exact flagship regression instances."""
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"independent_verifier"))
from core import reaction_list, selected

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("m",type=int); ap.add_argument("--out",type=Path,required=True); args=ap.parse_args()
    m=args.m; rs=reaction_list(m); r,d,ell=selected(m)
    obj={
      "m":m,
      "species":[f"X{i}" for i in range(1,m+1)]+["Z"],
      "reactions":[{"label":x.label,"source":list(x.y),"target":list(x.yp)} for x in rs],
      "flux_parameters":{"a":"1","b":"1"},
      "equilibrium":["1"]*(m+1),
      "diffusion":[str(x) for x in d],
      "right_vector":[str(x) for x in r],
      "left_vector":[str(x) for x in ell],
      "unit_contrast":str(max(d)/min(d)),
    }
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(obj,indent=2)+"\n")
    print(args.out)
if __name__=="__main__": main()
