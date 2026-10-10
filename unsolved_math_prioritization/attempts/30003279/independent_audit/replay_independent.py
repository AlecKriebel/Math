#!/usr/bin/env python3
"""Independent cross-mode, relocation, mutation and frozen-integrity harness."""
import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

class ControlError(Exception):pass

def need(x,s):
    if not x:raise ControlError(s)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def object_pairs(pairs):
    out={}
    for k,v in pairs:
        need(k not in out,'duplicate key');out[k]=v
    return out
def strict(t):return json.loads(t,object_pairs_hook=object_pairs,parse_constant=lambda x:(_ for _ in ()).throw(ControlError('nonfinite number')))
def inventory(root,pin):
    need(digest(root/'MANIFEST.json')==pin,'external manifest pin')
    m=strict((root/'MANIFEST.json').read_text())
    need(type(m) is dict and set(m)=={'schema','files'} and type(m['schema']) is int and m['schema']==1 and type(m['files']) is list,'manifest schema')
    seen=set()
    for row in m['files']:
        need(type(row) is dict and set(row)=={'path','bytes','sha256'},'entry schema')
        name=row['path'];need(type(name) is str and name not in seen and name!='MANIFEST.json' and Path(name).name==name,'member name');seen.add(name)
        p=root/name;need(p.is_file() and not p.is_symlink(),'regular member')
        need(type(row['bytes']) is int and row['bytes']==p.stat().st_size and row['sha256']==digest(p),'member hash')
    need({p.name for p in root.iterdir()}==seen|{'MANIFEST.json'},'exact inventory')
    return {p.name:digest(p) for p in root.iterdir()}
def invoke(script,flags,args,cwd):
    env=dict(os.environ);env['PYTHONDONTWRITEBYTECODE']='1'
    return subprocess.run([sys.executable,*flags,'-B',str(script),*args],cwd=cwd,env=env,capture_output=True)
def rebind(root):
    p=root/'MANIFEST.json';m=json.loads(p.read_text())
    for row in m['files']:
        q=root/row['path'];row['bytes']=q.stat().st_size;row['sha256']=digest(q)
    p.write_text(json.dumps(m,indent=2)+'\n');return digest(p)
def mutate(c,name):
    x=copy.deepcopy(c)
    if name=='floating Fibonacci norm':x['four_point_witness']['n']=float(x['four_point_witness']['n'])
    elif name=='floating Fibonacci point':x['four_point_witness']['points'][0][0]=float(x['four_point_witness']['points'][0][0])
    elif name=='floating balanced point':x['general_sample']['points'][0][0]=float(x['general_sample']['points'][0][0])
    elif name=='boolean problem id':x['problem_id']=True
    elif name=='floating route count':x['route_count']=5.0
    elif name=='false solved claim':x['full_problem_solved']=True
    elif name=='false novelty claim':x['novelty_claim']=True
    elif name=='false all-parameters claim':x['all_triple_parameters_admissible']=True
    elif name=='false triple point':x['three_point_witness']['points'][0][0]+=1
    elif name=='missing Fibonacci factor':x['four_point_witness']['n']//=34
    elif name=='repeated balanced point':x['general_sample']['points'][1]=x['general_sample']['points'][0]
    elif name=='missing key':del x['route_count']
    elif name=='extra key':x['unexpected']=0
    elif name=='nonfinite value':x['route_count']=float('nan')
    text=json.dumps(x)
    if name=='duplicate key':text=text.replace('"problem_id": 30003279,','"problem_id": 0, "problem_id": 30003279,',1)
    elif name=='malformed JSON':text='{'
    return text

def main():
    a=argparse.ArgumentParser();a.add_argument('--original',type=Path,required=True);a.add_argument('--pin',required=True);a.add_argument('--hardened',type=Path,required=True);a.add_argument('--hardened-pin',required=True);v=a.parse_args()
    checker=Path(__file__).resolve().with_name('independent_checks.py');before=inventory(v.original,v.pin);hardened_before=inventory(v.hardened,v.hardened_pin)
    c=strict((v.original/'CLAIMS.json').read_text());positives=[];negatives=[];original_holes=[];hardened_rejections=[];outputs=[]
    cases=['floating Fibonacci norm','floating Fibonacci point','floating balanced point','boolean problem id','floating route count','false solved claim','false novelty claim','false all-parameters claim','false triple point','missing Fibonacci factor','repeated balanced point','missing key','extra key','nonfinite value','duplicate key','malformed JSON']
    holes=['floating Fibonacci norm','floating Fibonacci point','floating balanced point','duplicate key','boolean schema','floating schema','duplicate manifest key']
    with tempfile.TemporaryDirectory(prefix='independent-lattice-audit-') as td:
        temp=Path(td);cwd=temp/'unrelated';cwd.mkdir()
        for label,flags in [('normal',[]),('O',['-O']),('OO',['-OO'])]:
            r=invoke(checker,flags,['--claims',str(v.original/'CLAIMS.json')],cwd);need(r.returncode==0,'independent original failure '+label+str(r.stdout));outputs.append(r.stdout);positives.append(label+' original')
            readonly=temp/('readonly-'+label);readonly.mkdir();shutil.copy2(checker,readonly/checker.name);shutil.copy2(v.original/'CLAIMS.json',readonly/'CLAIMS.json')
            rb={p.name:digest(p) for p in readonly.iterdir()}
            for p in readonly.iterdir():p.chmod(0o444)
            readonly.chmod(0o555)
            try:
                r=invoke(readonly/checker.name,flags,['--claims',str(readonly/'CLAIMS.json')],cwd)
                need(r.returncode==0 and r.stdout==outputs[0],'readonly failure');need(rb=={p.name:digest(p) for p in readonly.iterdir()},'readonly changed');positives.append(label+' readonly relocated')
            finally:
                readonly.chmod(0o755)
                for p in readonly.iterdir():p.chmod(0o644)
            for name in cases:
                f=temp/'claims.json';f.write_text(mutate(c,name));r=invoke(checker,flags,['--claims',str(f),'--validate-only'],cwd)
                need(r.returncode!=0,'independent malformed accepted '+label+' '+name);negatives.append(label+' '+name)
            for name in holes:
                for version,src in [('original',v.original),('hardened',v.hardened)]:
                    root=temp/(label+'-'+version+'-'+name.replace(' ','_'));shutil.copytree(src,root)
                    mf=root/'MANIFEST.json'
                    if name in ['boolean schema','floating schema']:
                        m=json.loads(mf.read_text());m['schema']=True if name=='boolean schema' else 1.0;mf.write_text(json.dumps(m));pin=digest(mf)
                    elif name=='duplicate manifest key':
                        mf.write_text(mf.read_text().replace('"schema": 1,','"schema": 0, "schema": 1,',1));pin=digest(mf)
                    else:(root/'CLAIMS.json').write_text(mutate(c,name));pin=rebind(root)
                    r=invoke(root/'verify_packet.py',flags,['--root',str(root),'--manifest-sha256',pin],cwd)
                    if version=='original':need(r.returncode==0,'expected original permissiveness not reproduced');original_holes.append(label+' '+name)
                    else:need(r.returncode!=0,'hardened malformed accepted');hardened_rejections.append(label+' '+name)
    need(all(x==outputs[0] for x in outputs),'optimization-dependent independent output')
    need(before==inventory(v.original,v.pin),'original packet changed')
    need(hardened_before==inventory(v.hardened,v.hardened_pin),'hardened packet changed')
    result={'verdict':'PASS_INDEPENDENT_CROSS_MODE_AND_REGRESSIONS','original_manifest_sha256':v.pin,'hardened_manifest_sha256':v.hardened_pin,'independent_positive_runs':positives,'independent_negative_runs':negatives,'original_rebound_permissive_cases':original_holes,'hardened_rejections':hardened_rejections,'positive_count':len(positives),'negative_count':len(negatives),'reproduced_original_holes':len(original_holes),'hardened_regression_rejections':len(hardened_rejections),'normal_O_OO_outputs_identical':True,'original_packet_bytes_unchanged':True,'hardened_packet_bytes_unchanged':True,'read_only_relocated_bytes_unchanged':True,'independent_math_result':json.loads(outputs[0])}
    print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':main()
