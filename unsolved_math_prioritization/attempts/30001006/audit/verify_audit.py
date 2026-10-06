#!/usr/bin/env python3
"""Checks this audit against an externally supplied manifest hash."""
import argparse,hashlib,json,pathlib,re,subprocess,sys

def need(ok,msg):
    if not ok:raise RuntimeError(msg)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--expected-manifest',required=True);args=parser.parse_args()
    need(re.fullmatch(r'[0-9a-f]{64}',args.expected_manifest) is not None,'invalid external anchor')
    root=pathlib.Path(__file__).resolve().parent
    mp=root/'MANIFEST.json';need(mp.is_file() and not mp.is_symlink(),'manifest must be a regular file')
    raw=mp.read_bytes();need(hashlib.sha256(raw).hexdigest()==args.expected_manifest,'manifest anchor mismatch')
    m=json.loads(raw);need(set(m)=={'schema','files'} and m['schema']=='exact-file-manifest-v1','invalid schema')
    entries=m['files'];need(isinstance(entries,dict) and entries,'empty manifest')
    need(set(p.name for p in root.iterdir())==set(entries)|{'MANIFEST.json'},'member set mismatch')
    for name,entry in entries.items():
        need(pathlib.Path(name).name==name and name not in {'.','..','MANIFEST.json'},'unsafe member name')
        need(set(entry)=={'bytes','sha256'},'invalid entry schema')
        p=root/name;need(p.is_file() and not p.is_symlink(),'non-regular member')
        b=p.read_bytes();need(len(b)==entry['bytes'] and hashlib.sha256(b).hexdigest()==entry['sha256'],'member digest mismatch: '+name)
    p=subprocess.run([sys.executable,'-B',str(root/'independent_checks.py')],capture_output=True)
    need(p.returncode==0,'independent diagnostics failed')
    need(p.stdout==(root/'independent_results.json').read_bytes(),'independent output differs')
    meta=json.loads((root/'PUBLIC_AUDIT_METADATA.json').read_text())
    need(meta['problem_id']==30001006 and meta['rank']==817,'wrong target')
    need(meta['bridge_verdict']=='ACCEPT_SCOPED_THEOREM','unexpected verdict')
    need(meta['full_problem_solved'] is False,'classification overstated')
    need(meta['fresh_corpus_replay']=='NOT_RUN','corpus provenance overstated')
    print(json.dumps({'status':'PASS','members':len(entries)+1,'independent_diagnostics':'exact byte match','mathematical_certification':False},sort_keys=True))
if __name__=='__main__':
    try:main()
    except Exception as e:print('FAIL: '+str(e),file=sys.stderr);sys.exit(1)
