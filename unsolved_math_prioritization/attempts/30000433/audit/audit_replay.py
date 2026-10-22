#!/usr/bin/env python3
"""Replay the immutable author archive and the independent correction supplement."""
import argparse, hashlib, importlib.util, json, pathlib, re, shutil, subprocess, sys, tempfile, zipfile
ROOT=pathlib.Path(__file__).resolve().parent
PIN='b64c3b92a96f180b51d22ddd343e9458fc7181f7d8117d5117a4b6a7215dcdf7'
MPIN='ac8006591dde3c8d85cbf2bc47dcb375f7b572107c159bc9a4118e16b8ed0873'
MEMBERS={'APPROACHES.json','MANIFEST.json','MATHEMATICAL_NOTE.md','README.md','REPLAY_REPORT.json','SOURCE_AUDIT.md','SOURCE_METADATA.json','results.json','test_replay.py','verify.py'}

def need(c,msg):
    if not c:raise ValueError(msg)
def run(cmd,cwd):
    r=subprocess.run(cmd,cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,timeout=120)
    need(r.returncode==0,'replay failed: '+r.stderr)
    return json.loads(r.stdout)
def apply_diff(original,diff):
    source=original.splitlines(True);lines=diff.splitlines(True);out=[];pos=0;i=2
    while i<len(lines):
        m=re.match(r'@@ -(\d+)(?:,\d+)? \+\d+(?:,\d+)? @@',lines[i]);need(m is not None,'bad hunk')
        start=int(m.group(1))-1;need(start>=pos,'overlapping hunks');out.extend(source[pos:start]);pos=start;i+=1
        while i<len(lines) and not lines[i].startswith('@@ '):
            l=lines[i];tag=l[0];text=l[1:]
            need(tag in ' +-','unsupported diff record')
            if tag in ' -':need(pos<len(source) and source[pos]==text,'patch context mismatch');pos+=1
            if tag in ' +':out.append(text)
            i+=1
    out.extend(source[pos:]);return ''.join(out)
def main():
    ap=argparse.ArgumentParser();ap.add_argument('author_zip',type=pathlib.Path);args=ap.parse_args()
    raw=args.author_zip.read_bytes();need(len(raw)==21187 and hashlib.sha256(raw).hexdigest()==PIN,'wrong author archive')
    summary={'schema':1,'author_archive_anchor':'pass','clean_author_replays':0,'author_test_driver_runs':0,'semantic_rejections_per_driver':[],'integrity_rejections_per_driver':[],'independent_replays':0,'patched_replays':0,'quotient_guard_negative_controls':0,'status':'pass','full_source_solved':False,'approaches_used':4}
    with tempfile.TemporaryDirectory(prefix='independent_edge_audit_') as td:
        top=pathlib.Path(td);f=top/'immutable author';f.mkdir()
        with zipfile.ZipFile(args.author_zip) as z:
            need(set(z.namelist())==MEMBERS and len(z.namelist())==len(MEMBERS),'wrong archive inventory')
            z.extractall(f)
        baseline=json.loads((f/'results.json').read_text())
        for opt in ([],['-O']):
            r=run([sys.executable]+opt+[str(f/'verify.py'),'--manifest-sha256',MPIN],top);need(r==baseline,'author replay disagreement');summary['clean_author_replays']+=1
            r=run([sys.executable]+opt+[str(f/'test_replay.py')],top)
            need(r['semantic_mutations_rejected']==16 and r['integrity_mutations_rejected']==4,'author driver coverage mismatch')
            summary['author_test_driver_runs']+=1;summary['semantic_rejections_per_driver'].append(r['semantic_mutations_rejected']);summary['integrity_rejections_per_driver'].append(r['integrity_mutations_rejected'])
        independent=top/'relocated independent checker.py';shutil.copyfile(ROOT/'independent_audit.py',independent)
        expected=json.loads((ROOT/'INDEPENDENT_RESULTS.json').read_text())
        for opt in ([],['-O']):
            r=run([sys.executable]+opt+[str(independent),str(f)],top);need(r==expected,'independent output mismatch');summary['independent_replays']+=1
        patched=top/'patched author';shutil.copytree(f,patched)
        (patched/'verify.py').write_text(apply_diff((f/'verify.py').read_text(),(ROOT/'verify_quotient_guard.patch').read_text()))
        # Old external author pin must not validate modified code.
        rejection=subprocess.run([sys.executable,str(patched/'verify.py'),'--manifest-sha256',MPIN],cwd=top,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,timeout=120)
        need(rejection.returncode!=0 and 'file hash mismatch: verify.py' in rejection.stderr,'patch incorrectly validates against old author pin')
        summary['old_anchor_rejects_patched_code']=True
        for opt in ([],['-O']):
            r=run([sys.executable]+opt+[str(patched/'verify.py')],top);need(r==baseline,'patch changed mathematical results');summary['patched_replays']+=1
        spec=importlib.util.spec_from_file_location('patched_author',patched/'verify.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
        a,b,im={0,1,2},{3,4,5},{3:0,4:1,5:2}
        v.check_boundary_quotient([(0,1,2,6),(3,4,5,7)],a,b,im)
        for ts in [[(0,6,7,8),(3,6,9,10)],[(0,6,7,8),(3,6,7,9)],[(0,6,7,8),(3,6,7,8)],[(0,3,6,7)]]:
            try:v.check_boundary_quotient(ts,a,b,im)
            except v.Invalid:summary['quotient_guard_negative_controls']+=1
            else:raise ValueError('unsafe quotient accepted')
    print(json.dumps(summary,sort_keys=True,indent=2))
if __name__=='__main__':main()
