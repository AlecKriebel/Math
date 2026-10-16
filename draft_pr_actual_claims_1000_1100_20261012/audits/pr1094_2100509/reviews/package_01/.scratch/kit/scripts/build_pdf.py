import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
sys.dont_write_bytecode=True
from safety import ROOT, require, verify_payload, fresh_output, create_output_dir, json_bytes

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--out-dir',required=True);parser.add_argument('--tectonic',default='tectonic');args=parser.parse_args()
    output=fresh_output(args.out_dir,True);verify_payload()
    compiler=shutil.which(args.tectonic)
    require(compiler is not None,'tectonic compiler unavailable')
    # All copied source, compiler products, stdout, stderr and receipt are in
    # one previously absent directory. No external output path is delegated.
    output=create_output_dir(output)
    (output/'paper.tex').write_bytes((ROOT/'paper.tex').read_bytes())
    env=dict(os.environ);env['SOURCE_DATE_EPOCH']='1792022400';env['FORCE_SOURCE_DATE']='1'
    completed=subprocess.run([compiler,'--keep-logs','paper.tex'],cwd=output,env=env,capture_output=True)
    (output/'compiler.stdout.txt').write_bytes(completed.stdout)
    (output/'compiler.stderr.txt').write_bytes(completed.stderr)
    require(completed.returncode==0,'tectonic compilation failed; inspect fresh output directory')
    pdf=output/'paper.pdf';require(pdf.is_file() and not pdf.is_symlink(),'compiler did not create regular PDF')
    log=(output/'paper.log').read_text(errors='replace')
    require('Overfull' not in log,'overfull TeX box; inspect fresh output directory')
    receipt={'status':'PASS','compiler':subprocess.check_output([compiler,'--version'],text=True).strip(),
             'overfull_boxes':0,'pdf_bytes':pdf.stat().st_size,
             'layout_review_required':'Every newly changed PDF page must be visually inspected.'}
    (output/'BUILD_RECEIPT.json').write_bytes(json_bytes(receipt));print(json.dumps(receipt,sort_keys=True))
if __name__=='__main__': main()
