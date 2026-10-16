#!/usr/bin/env python3
"""Replay unchanged input verifiers in temporary extractions, never in freezes."""
from pathlib import Path
import argparse, hashlib, json, os, subprocess, sys, tempfile
sys.dont_write_bytecode=True
from verify_delta import ANCHORS, AUTHOR, AUDIT, V2, AUTHOR_NAMES, AUDIT_NAMES, parse, require

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--input-dir',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    files={}
    for name,(size,digest) in ANCHORS.items():
        raw=(args.input_dir/name).read_bytes()
        require(len(raw)==size and hashlib.sha256(raw).hexdigest()==digest,'input anchor')
        files[name]=parse(raw,AUDIT_NAMES if name==AUDIT else AUTHOR_NAMES)
    records=[]
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
    with tempfile.TemporaryDirectory(prefix='reinforcement-v2-replay-') as tmp:
        for name in (AUTHOR,V2,AUDIT):
            root=Path(tmp)/name.removesuffix('.zip');root.mkdir()
            for relative,raw in files[name].items():
                target=root/relative;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw)
            commands=([['code/verify_manifest.py'],['code/verify_algebra.py'],['code/verify_manifest.py']]
                      if name!=AUDIT else [['code/replay_audit.py','--author-zip',str((args.input_dir/AUTHOR).resolve())]])
            for command in commands:
                run=subprocess.run([sys.executable,'-B',*command],cwd=root,env=env,text=True,capture_output=True,timeout=90)
                require(run.returncode==0,'replay failed: '+run.stderr)
                records.append({'archive':name,'script':command[0],'status':'PASS','result':json.loads(run.stdout)})
            # Algebra replay must not rewrite even its result to different bytes.
            require({p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}==set(files[name]),'replay changed file set')
            for relative,raw in files[name].items():require((root/relative).read_bytes()==raw,'replay changed bytes: '+relative)
    out={'status':'PASS','replays':records,'all_replayed_files_byte_identical_after_execution':True,
         'frozen_inputs_modified':False,'scope':'Replay and integrity only; independent targeted mathematical review is in REPORT.md'}
    args.output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
