#!/usr/bin/env python3
"""Independent normal/-O, relocated, mutation, and optional-input controls."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parent


def need(ok, why):
    if not ok:
        raise ValueError(why)


def rebind(where,name):
    path=where/'MANIFEST.json'
    m=json.loads(path.read_text())
    raw=(where/name).read_bytes()
    m['files'][name]={'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
    path.write_text(json.dumps(m,indent=2,sort_keys=True)+'\n')


def execute(where, optimized, extras=()):
    cmd=[sys.executable]+(['-O'] if optimized else [])+[str(where/'verify_audit.py')]+list(extras)
    return subprocess.run(cmd,cwd=where.parent,text=True,capture_output=True,timeout=120)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--author-zip',type=Path)
    ap.add_argument('--corpora',type=Path,nargs=3)
    ap.add_argument('--source-dir',type=Path)
    args=ap.parse_args()
    extras=[]
    if args.author_zip:
        args.author_zip=args.author_zip.resolve(); extras+=['--author-zip',str(args.author_zip)]
    if args.corpora:
        args.corpora=[p.resolve() for p in args.corpora];extras+=['--corpora']+[str(p) for p in args.corpora]
    if args.source_dir:
        args.source_dir=args.source_dir.resolve();extras+=['--source-dir',str(args.source_dir)]
    cases=[]
    with tempfile.TemporaryDirectory(prefix='independent_bahri_xu_audit_') as td:
        temporary=Path(td)
        relocated=temporary/'relocated'
        shutil.copytree(ROOT,relocated)
        for mode in (False,True):
            r=execute(relocated,mode,extras)
            need(r.returncode==0,'relocated clean failed: '+r.stderr)
            data=json.loads(r.stdout)
            need(data['optimized_python']==mode,'optimization indicator')
            cases.append({'case':'relocated_clean_with_supplied_inputs','optimized':mode,'expected':'PASS','observed':'PASS'})
        mutations=['changed_bytes','missing_file','extra_file','symlink','wrong_verdict','wrong_math_count','duplicate_json_key','nonfinite_json','empty_manifest']
        for mutation in mutations:
            dest=temporary/mutation;shutil.copytree(ROOT,dest)
            name='INDEPENDENT_RESULTS.json'
            if mutation=='changed_bytes':
                with (dest/'AUDIT_REPORT.md').open('a') as f:f.write('\nAlteration.\n')
            elif mutation=='missing_file':(dest/'AUDIT_REPORT.md').unlink()
            elif mutation=='extra_file':(dest/'unexpected.txt').write_text('unexpected')
            elif mutation=='symlink':
                (dest/'AUDIT_REPORT.md').unlink();(dest/'AUDIT_REPORT.md').symlink_to(ROOT/'AUDIT_REPORT.md')
            elif mutation in ['wrong_verdict','wrong_math_count']:
                val=json.loads((dest/name).read_text())
                if mutation=='wrong_verdict':val['verdict']='GENERAL_CONJECTURE_PROVED'
                else:val['math_checks']['line_and_support']['support_one_cases']=0
                (dest/name).write_text(json.dumps(val,indent=2,sort_keys=True)+'\n');rebind(dest,name)
            elif mutation=='duplicate_json_key':
                (dest/name).write_text('{"x":1,"x":2}\n');rebind(dest,name)
            elif mutation=='nonfinite_json':
                (dest/name).write_text('{"x":NaN}\n');rebind(dest,name)
            elif mutation=='empty_manifest':(dest/'MANIFEST.json').write_text('{"schema":1,"files":{}}\n')
            for mode in (False,True):
                r=execute(dest,mode)
                need(r.returncode!=0 and r.stderr.startswith('FAIL:'),'mutation accepted: '+mutation)
                cases.append({'case':mutation,'optimized':mode,'expected':'FAIL','observed':'FAIL'})
        external=[]
        if args.author_zip:
            raw=bytearray(args.author_zip.read_bytes());raw[len(raw)//2]^=1
            bad=temporary/'bad_author.zip';bad.write_bytes(raw)
            external.append(('author_zip_bit_flip',['--author-zip',str(bad)]))
        if args.corpora:
            raw=bytearray(args.corpora[0].read_bytes());raw[-2]^=1
            bad=temporary/'bad_catalog.json';bad.write_bytes(raw)
            external.append(('full_corpus_bit_flip',['--corpora',str(bad)]+[str(p) for p in args.corpora[1:]]))
        if args.source_dir:
            bad=temporary/'bad_pdf_directory';bad.mkdir()
            for name in ['owr2005_29.pdf','xu2006.pdf','chen2021.pdf','lan_lu.pdf','chen2021_journal.pdf']:
                raw=bytearray((args.source_dir/name).read_bytes())
                if name=='owr2005_29.pdf':raw[-1]^=1
                (bad/name).write_bytes(raw)
            external.append(('source_pdf_bit_flip',['--source-dir',str(bad)]))
        for case,argv in external:
            for mode in (False,True):
                r=execute(relocated,mode,argv)
                need(r.returncode!=0 and r.stderr.startswith('FAIL:'),'external mutation accepted: '+case)
                cases.append({'case':case,'optimized':mode,'expected':'FAIL','observed':'FAIL'})
    print(json.dumps({'status':'PASS','case_count':len(cases),'cases':cases},sort_keys=True))


if __name__=='__main__':
    main()
