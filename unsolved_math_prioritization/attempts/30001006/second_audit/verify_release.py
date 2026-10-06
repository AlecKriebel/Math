#!/usr/bin/env python3
"""Verify a second-audit release against an externally pinned manifest hash."""
import argparse,hashlib,json,pathlib,re,subprocess,sys


def need(ok,message):
    if not ok:raise RuntimeError(message)


def main():
    p=argparse.ArgumentParser();p.add_argument('--expected-manifest',required=True);a=p.parse_args()
    need(re.fullmatch('[0-9a-f]{64}',a.expected_manifest) is not None,'invalid manifest anchor')
    root=pathlib.Path(__file__).resolve().parent;mp=root/'MANIFEST.json'
    need(mp.is_file() and not mp.is_symlink(),'manifest must be regular')
    raw=mp.read_bytes();need(hashlib.sha256(raw).hexdigest()==a.expected_manifest,'manifest anchor mismatch')
    m=json.loads(raw);need(set(m)=={'schema','files'} and m['schema']=='exact-file-manifest-v1','invalid manifest schema')
    entries=m['files'];need(isinstance(entries,dict) and entries,'empty manifest')
    need(set(x.name for x in root.iterdir())==set(entries)|{'MANIFEST.json'},'member set mismatch')
    for name,meta in entries.items():
        need(pathlib.Path(name).name==name and name not in {'.','..','MANIFEST.json'},'unsafe member')
        need(set(meta)=={'bytes','sha256'},'invalid entry')
        f=root/name;need(f.is_file() and not f.is_symlink(),'nonregular member')
        b=f.read_bytes();need(len(b)==meta['bytes'] and hashlib.sha256(b).hexdigest()==meta['sha256'],'member hash mismatch: '+name)
    r=subprocess.run([sys.executable,'-B',str(root/'independent_stress_checks.py')],capture_output=True)
    need(r.returncode==0,'stress diagnostics failed')
    need(r.stdout==(root/'stress_results.json').read_bytes(),'stress replay differs')
    meta=json.loads((root/'PUBLIC_SECOND_AUDIT_METADATA.json').read_text())
    need(meta['problem_id']==30001006 and meta['rank']==817,'wrong target')
    need(meta['bridge_verdict']=='ACCEPT_SCOPED_THEOREM' and meta['full_problem_solved'] is False,'incorrect scope')
    need(meta['fresh_corpus_replay']=='PASS' and meta['first_audit_frozen_fields_preserved'] is True,'incorrect provenance status')
    print(json.dumps({'status':'PASS','members':len(entries)+1,'independent_diagnostic_replay':'exact byte match','mathematical_certification':False,'external_corpora_replayed_by_this_command':False},sort_keys=True))

if __name__=='__main__':
    try:main()
    except Exception as e:print('FAIL: '+str(e),file=sys.stderr);sys.exit(1)
