#!/usr/bin/env python3
"""Replay frozen mathematical checks with -I -S -B in every descendant."""
import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):
    raise SystemExit('REJECT: use the externally pinned bootstrap with -I -S -B')
import argparse,hashlib,json,shlex,subprocess,tempfile
from pathlib import Path
def need(ok,msg):
    if not ok:raise ValueError(msg)
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--expected-manifest',required=True);a=ap.parse_args()
    root=Path(__file__).absolute().parent
    need(hashlib.sha256((root/'PUBLICATION_MANIFEST.json').read_bytes()).hexdigest()==a.expected_manifest,'publication pin')
    meta=json.loads((root/'PUBLICATION_METADATA.json').read_text());acc=json.loads((root/'audit/ACCEPTANCE.json').read_text())
    need(meta['status']=='unsolved' and meta['turns']=='5/5' and meta['universal_solution'] is False and meta['candidate_realizability'] is False,'publication scope')
    need(acc['verdict']=='ACCEPTED_PARTIAL_UNRESOLVED' and acc['approaches_used']==5 and acc['correction_required'] is False,'acceptance scope')
    need('target' in (root/'SCOPE_CLARIFICATION.md').read_text() and 'source' in (root/'SCOPE_CLARIFICATION.md').read_text(),'scope clarification')
    with tempfile.TemporaryDirectory(prefix='minimal torus interpreter ') as td:
        shim=Path(td)/'isolated-python'
        # Preserve optimize mode and enforce no-site for every nested archived
        # subprocess without modifying any archived source byte.
        shell='#!/bin/sh\nopt=""\nwhile [ "$#" -gt 0 ]; do\n case "$1" in\n -I|-S|-B) shift ;;\n -O) opt="-O"; shift ;;\n -*) echo "unsupported interpreter option" >&2; exit 2 ;;\n *) break ;;\n esac\ndone\nexec '+shlex.quote(sys.executable)+' -I -S -B $opt '+shlex.quote(str(root/'isolated_runner.py'))+' "$0" "$@"\n'
        shim.write_text(shell);shim.chmod(0o700)
        commands=[('author',root/'author/verify_bundle.py',['--root',str(root/'author'),'--manifest',str(root/'manifests/MINIMAL_TORUS_30001702_EXTERNAL_MANIFEST.json')]),('audit',root/'audit/verify_audit.py',['--root',str(root/'audit'),'--manifest',str(root/'manifests/MINIMAL_TORUS_30001702_AUDIT_EXTERNAL_MANIFEST.json'),'--author-root',str(root/'author'),'--author-manifest',str(root/'manifests/MINIMAL_TORUS_30001702_EXTERNAL_MANIFEST.json'),'--author-archive',str(root/'archives/MINIMAL_TORUS_30001702_AUTHOR_SAFE_FREEZE.zip')])]
        result=[]
        for label,script,args in commands:
            p=subprocess.run([str(shim),'-I','-S','-B']+(['-O'] if sys.flags.optimize else [])+[str(script),*args],cwd=td,capture_output=True,text=True,timeout=600)
            need(p.returncode==0 and p.stderr=='','replay failure '+label+': '+p.stderr)
            r=json.loads(p.stdout);need(r['verified'] is True,'unverified '+label)
            if label=='audit':need(r['author_controls_replayed'] is True,'missing controls')
            result.append({'role':label,'output_sha256':hashlib.sha256(p.stdout.encode()).hexdigest(),'verified':True})
    print(json.dumps({'status':'PASS','problem_id':30001702,'mathematical_status':'PARTIAL_UNRESOLVED','optimized':bool(sys.flags.optimize),'all_descendants_isolated_no_site_no_bytecode':True,'original_author_controls_executions':78,'original_expected_negative':72,'original_trust_boundary_acceptances':2,'replays':result},sort_keys=True,indent=2))
if __name__=='__main__':main()
