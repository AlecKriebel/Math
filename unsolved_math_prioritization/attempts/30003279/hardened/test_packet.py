#!/usr/bin/env python3
"""Cross-mode, relocated read-only replay and genuine hostile package controls."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

class TestError(Exception):pass

def need(ok,why):
    if not ok:raise TestError(why)

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def run(root,pin,flags,cwd):
    env=dict(os.environ);env['PYTHONDONTWRITEBYTECODE']='1'
    return subprocess.run([sys.executable,*flags,'-B',str(root/'verify_packet.py'),'--root',str(root),'--manifest-sha256',pin],cwd=cwd,env=env,capture_output=True)

def rewrite_manifest(root):
    p=root/'MANIFEST.json';m=json.loads(p.read_text())
    for row in m['files']:
        q=root/row['path']
        row['bytes']=q.stat().st_size;row['sha256']=digest(q)
    p.write_text(json.dumps(m,indent=2)+'\n')
    return digest(p)

def main():
    a=argparse.ArgumentParser();a.add_argument('--manifest-sha256',required=True);a=a.parse_args()
    source=Path(__file__).resolve().parent
    positive=[];negative=[]
    with tempfile.TemporaryDirectory(prefix='lattice-circle-controls-') as temp:
        temp=Path(temp);cwd=temp/'unrelated-working-directory';cwd.mkdir()
        for label,flags in [('normal',[]),('O',['-O']),('OO',['-OO'])]:
            p=run(source,a.manifest_sha256,flags,cwd)
            need(p.returncode==0,'original positive failed '+label+': '+p.stdout.decode()+p.stderr.decode());positive.append(label+' original')
            relocated=temp/('readonly-'+label);shutil.copytree(source,relocated)
            before={q.name:digest(q) for q in relocated.iterdir()}
            for q in relocated.iterdir():q.chmod(0o444)
            relocated.chmod(0o555)
            try:
                p=run(relocated,a.manifest_sha256,flags,cwd)
                need(p.returncode==0,'read-only positive failed '+label+': '+p.stdout.decode()+p.stderr.decode())
                after={q.name:digest(q) for q in relocated.iterdir()}
                need(before==after,'relocated packet changed');positive.append(label+' read-only relocated')
            finally:
                relocated.chmod(0o755)
                for q in relocated.iterdir():q.chmod(0o644)
            for case in ['changed proof','missing file','extra file','malformed manifest','duplicate entry','traversal entry','boolean byte count','rebound false scope old pin','rebound false scope new pin','rebound malformed claims','rebound false point','symlink member','rebound false expected results','boolean schema','floating schema','duplicate manifest key','duplicate claims key','floating Fibonacci norm','floating Fibonacci point','floating balanced point','nonfinite claims number']:
                root=temp/(label+'-'+case.replace(' ','_'));shutil.copytree(source,root);pin=a.manifest_sha256
                mf=root/'MANIFEST.json'
                if case=='changed proof':(root/'REPORT.md').write_text('false proof\n')
                elif case=='missing file':(root/'REPORT.md').unlink()
                elif case=='extra file':(root/'extra.txt').write_text('unexpected')
                elif case=='malformed manifest':mf.write_text('{');pin=digest(mf)
                elif case in ['duplicate entry','traversal entry','boolean byte count']:
                    m=json.loads(mf.read_text())
                    if case=='duplicate entry':m['files'].append(dict(m['files'][0]))
                    elif case=='traversal entry':m['files'][0]['path']='../outside'
                    else:m['files'][0]['bytes']=True
                    mf.write_text(json.dumps(m));pin=digest(mf)
                elif case.startswith('rebound false scope'):
                    c=json.loads((root/'CLAIMS.json').read_text());c['full_problem_solved']=True;(root/'CLAIMS.json').write_text(json.dumps(c))
                    newpin=rewrite_manifest(root)
                    if case.endswith('new pin'):pin=newpin
                elif case=='rebound malformed claims':(root/'CLAIMS.json').write_text('{');pin=rewrite_manifest(root)
                elif case=='rebound false point':
                    c=json.loads((root/'CLAIMS.json').read_text());c['three_point_witness']['points'][0][0]+=1;(root/'CLAIMS.json').write_text(json.dumps(c));pin=rewrite_manifest(root)
                elif case=='symlink member':
                    external=temp/(label+'-external-report');shutil.copy2(root/'REPORT.md',external);(root/'REPORT.md').unlink();(root/'REPORT.md').symlink_to(external)
                elif case=='rebound false expected results':(root/'CHECK_RESULTS.json').write_text('{}\n');pin=rewrite_manifest(root)
                elif case in ['boolean schema','floating schema']:
                    m=json.loads(mf.read_text());m['schema']=True if case=='boolean schema' else 1.0
                    mf.write_text(json.dumps(m));pin=digest(mf)
                elif case=='duplicate manifest key':
                    mf.write_text(mf.read_text().replace('"schema": 1,','"schema": 0, "schema": 1,',1));pin=digest(mf)
                elif case=='duplicate claims key':
                    cp=root/'CLAIMS.json';cp.write_text(cp.read_text().replace('"problem_id": 30003279,','"problem_id": 0, "problem_id": 30003279,',1));pin=rewrite_manifest(root)
                elif case in ['floating Fibonacci norm','floating Fibonacci point','floating balanced point']:
                    cp=root/'CLAIMS.json';c=json.loads(cp.read_text())
                    if case=='floating Fibonacci norm':c['four_point_witness']['n']=float(c['four_point_witness']['n'])
                    else:
                        key='four_point_witness' if case=='floating Fibonacci point' else 'general_sample'
                        c[key]['points'][0][0]=float(c[key]['points'][0][0])
                    cp.write_text(json.dumps(c));pin=rewrite_manifest(root)
                elif case=='nonfinite claims number':
                    cp=root/'CLAIMS.json';cp.write_text(cp.read_text().replace('"route_count": 5,','"route_count": NaN,',1));pin=rewrite_manifest(root)
                p=run(root,pin,flags,cwd)
                need(p.returncode!=0,'mutant accepted: '+label+' '+case)
                negative.append(label+' '+case)
    print(json.dumps({'verdict':'PASS_PORTABLE_AND_HOSTILE_CONTROLS','positive_runs':positive,'negative_runs':negative,'positive_count':len(positive),'negative_count':len(negative),'read_only_packet_bytes_unchanged':True},sort_keys=True,indent=2))
    return 0
if __name__=='__main__':raise SystemExit(main())
