#!/usr/bin/env python3
"""Bounded v1-to-v2 audit from externally anchored immutable ZIP inputs.
No source text or corpus data is used, transmitted, or emitted.
"""
import argparse
import difflib
import hashlib
import json
from pathlib import Path,PurePosixPath
import stat
import subprocess
import sys
import tempfile
import zipfile

if sys.flags.optimize:raise SystemExit('Optimized Python is not supported.')

ANCHORS={
'original':(16695,'d7797a066274ad7a5f7598e711838fa3c2857b9af8a67299d4e3c872d99b8f2d','3f9f39f70e90cb78b8e36d86a80a88dc7bc8100fd29bda09cf25158d615955c8'),
'v2':(19862,'ae94bc32d7727c371299ceefaeea99652ffb0dbee8897af386d1e51cd3012d49','850d3808cbe93e1c5ef2442cc4cafd60c9bec9bf586a2bee07c28553729d1ec8'),
'audit':(24847,'bd2f9f10de48529cc5a8bfbf8458049ee790761fafbb14b4cbeb90bfda167f94','ae9e66d5cb64d8237244ee9aae13db491d4779db764d9d7cf231fec5c9d52786')}
REPORT_SHA='6cdd4a0449328a245e4e210d765823366cca908aa2460c74dd028431e8bc81ae'
REPLACEMENTS=[
(' a>max{x_0,K+6},             b+eta<F(a).',' a>max{x_0+2 log(K+3),K+6},   b+eta<F(a).'),
('These finite approximants converge to the usual dynamic ray on such tails by [FS].','The address bound implies t_s^*:=sup_{j>=0} F^{-j}(|s_(j+1)|)<=x_0. Therefore a>t_s^*+2 log(K+3), and [FS, Lemma 4.4] identifies the locally uniform limit of these finite approximants with the standard dynamic ray.'),
('Increase N until F^N(inf J)>K+6 and F^N(u)>=2, where a parameter neighborhood has |kappa|<=K.','Increase N until F^N(inf J)>max{F^N(u)+2 log(K+3),K+6} and F^N(u)>=2, where a parameter neighborhood has |kappa|<=K. This is possible because inf J>u>0: after finitely many iterates both are at least 2, and their difference then grows at least geometrically.')]

def require(ok,why):
    if not ok:raise RuntimeError(why)

def sha(b):return hashlib.sha256(b).hexdigest()

def archive(path,key):
    raw=path.read_bytes();size,digest,manifest_digest=ANCHORS[key]
    require((len(raw),sha(raw))==(size,digest),'ZIP external anchor '+key)
    with zipfile.ZipFile(path) as z:
        names=z.namelist();require(len(names)==len(set(names)),'duplicate archive member')
        for i in z.infolist():
            p=PurePosixPath(i.filename)
            require(not p.is_absolute() and '..' not in p.parts and str(p)==i.filename,'unsafe ZIP path')
            require(not stat.S_ISLNK(i.external_attr>>16),'archive symlink')
            require(not i.is_dir(),'unexpected archive directory entry')
        data={n:z.read(n) for n in names}
    require(sha(data['MANIFEST.json'])==manifest_digest,'manifest anchor '+key)
    entries=json.loads(data['MANIFEST.json'])['files']
    required=[r['path'] for r in entries]
    require(len(required)==len(set(required)) and set(required)|{'MANIFEST.json'}==set(data),'strict archive manifest inventory')
    for row in entries:require((len(data[row['path']]),sha(data[row['path']]))==(row['bytes'],row['sha256']),'archive member hash')
    return data

def run(original,v2,audit):
    inputs={'original':original,'v2':v2,'audit':audit};data={k:archive(p,k) for k,p in inputs.items()}
    old,new,prior=data['original'],data['v2'],data['audit']
    require(set(new)-set(old)=={'REPORT_MANDATORY.patch','DELTA_PROVENANCE.json'},'added files')
    require(not set(old)-set(new),'removed original payload')
    changed=sorted(n for n in old if old[n]!=new[n]);require(changed==['MANIFEST.json','REPORT.md'],'changed payload scope')
    text=old['REPORT.md'].decode()
    for before,after in REPLACEMENTS:
        require(text.count(before)==1,'replacement not unique')
        text=text.replace(before,after)
    require(text.encode()==new['REPORT.md'],'unexpected mathematical text delta')
    require(sha(new['REPORT.md'])==REPORT_SHA,'corrected report anchor')
    require(new['REPORT_MANDATORY.patch']==prior['REPORT_MANDATORY.patch'],'mandatory patch differs')
    expected_patch=''.join(difflib.unified_diff(old['REPORT.md'].decode().splitlines(True),new['REPORT.md'].decode().splitlines(True),fromfile='author/REPORT.md',tofile='author_v2/REPORT.md')).encode()
    require(new['REPORT_MANDATORY.patch']==expected_patch,'patch not exact full diff')
    changes=[{'operation':tag,'original_lines_one_based':[i1+1,i2],'revised_lines_one_based':[j1+1,j2]} for tag,i1,i2,j1,j2 in difflib.SequenceMatcher(None,old['REPORT.md'].decode().splitlines(),text.splitlines(),autojunk=False).get_opcodes() if tag!='equal']
    require(len(changes)==3 and all(c['operation']=='replace' for c in changes),'line edit count')
    unchanged=sorted(set(old)-{'MANIFEST.json','REPORT.md'})
    require(len(unchanged)==6,'unchanged payload count')
    state=json.loads(new['RESULTS.json'])
    require(state['status']=='unsolved' and state['approaches_used']==5 and state['full_resolution'] is False,'broadened status')
    require(state['novelty_claim'] is False and state['publication_performed'] is False,'broadened claims')
    provenance=json.loads(new['DELTA_PROVENANCE.json'])
    require(provenance['original_payload_modified']==['REPORT.md'],'provenance modified files')
    require(provenance['mandatory_patch']['replacement_count']==3 and provenance['mandatory_patch']['line_changes']==changes,'provenance edit locations')
    require(provenance['corrected_report']=={'bytes':len(new['REPORT.md']),'sha256':sha(new['REPORT.md'])},'provenance report binding')
    for name,key in [('original_author_zip','original'),('original_audit_zip','audit')]:
        require(provenance[name]=={'bytes':ANCHORS[key][0],'sha256':ANCHORS[key][1]},'provenance ZIP binding')
    require(provenance['code_or_retained_controls_changed'] is False and provenance['analyticity_or_endpoint_claim_added'] is False,'provenance scope')
    for record in provenance['unchanged_original_payload']:
        n=record['path'];require(n in unchanged and record['bytes']==len(new[n]) and record['sha256']==sha(new[n]),'provenance unchanged payload')
    replays={}
    with tempfile.TemporaryDirectory(prefix='hairs_v2_delta_') as td:
        for key,files in data.items():
            folder=Path(td)/key;folder.mkdir()
            for name,b in files.items():
                p=folder/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
            p=subprocess.run([sys.executable,'-B',str(folder/'verify.py'),'--expected-manifest',ANCHORS[key][2]],capture_output=True,check=True,timeout=120)
            replays[key]=json.loads(p.stdout)
    # The originals must still have the same external anchors after all replays.
    for key,path in inputs.items():require((len(path.read_bytes()),sha(path.read_bytes()))==ANCHORS[key][:2],'input changed after replay')
    return {'problem_id':5300062,'verdict':'ACCEPT_SCOPED_PARTIAL_V2','general_problem_status':'UNSOLVED','approaches_used':5,
      'corrected_report_sha256':REPORT_SHA,'mandatory_replacements':3,'line_changes':changes,
      'modified_original_files':changed,'unchanged_original_payload_files':unchanged,'added_files':sorted(set(new)-set(old)),
      'all_report_changes_exactly_mandatory':True,'code_and_retained_controls_unchanged':True,'no_broadened_claims':True,
      'provenance_checked':True,'historical_originals_preserved':True,'relocated_replays':replays,
      'bindings':{k:{'zip_bytes':v[0],'zip_sha256':v[1],'manifest_sha256':v[2]} for k,v in ANCHORS.items()},
      'source_content_involved':False,'remote_writes':False,
      'limits':'Bounded mathematical delta acceptance of the repaired interior C-infinity partial, together with the original independent audit. No general analyticity, endpoint, novelty or human-refereeing claim.'}

if __name__=='__main__':
    p=argparse.ArgumentParser()
    for name in ANCHORS:p.add_argument('--'+name,required=True,type=Path)
    a=p.parse_args();print(json.dumps(run(a.original,a.v2,a.audit),indent=2,sort_keys=True))
