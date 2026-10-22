#!/usr/bin/env python3
"""Independent adversarial replay. Deliberate resealed metadata gaps are recorded, not hidden."""
import sys
sys.dont_write_bytecode=True
import argparse
import hashlib
import io
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import zipfile
import independent_verify as iv

def require(ok,msg):
 if not ok:raise ValueError(msg)

def run(script,args,opt,cwd):
 p=subprocess.run([sys.executable]+(['-O'] if opt else [])+[str(script)]+args,cwd=cwd,capture_output=True,text=True,timeout=180)
 if p.returncode==0:
  return p,json.loads(p.stdout)
 return p,None

def reseal(root):
 m={'schema':'sha256-byte-inventory-v1','files':{}}
 for p in sorted(root.iterdir()):
  if p.name!='MANIFEST.json' and p.is_file():
   raw=p.read_bytes();m['files'][p.name]={'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
 (root/'MANIFEST.json').write_text(json.dumps(m,sort_keys=True,indent=2)+'\n')

def edit(root,file,key,value):
 p=root/file;d=json.loads(p.read_text());d[key]=value;p.write_text(json.dumps(d,sort_keys=True,indent=2)+'\n');reseal(root)

def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--author-zip',required=True)
 parser.add_argument('--inputs',nargs=3);parser.add_argument('--pdf-inputs',nargs=4);a=parser.parse_args()
 raw=Path(a.author_zip).read_bytes();md=iv.frozen(raw)
 source=Path(__file__).resolve().parent
 rejections=[];observations=[];baselines=[];archive_checks=[];source_checks=[]
 with tempfile.TemporaryDirectory(prefix='navier_independent_') as t:
  t=Path(t);z=t/'author.zip';z.write_bytes(raw)
  with zipfile.ZipFile(io.BytesIO(raw)) as zz:zz.extractall(t/'original')
  original=t/'original'/'navier_30000801'
  for opt in (False,True):
   mode='optimized' if opt else 'normal'
   # Self-written checker and frozen author are both relocated under unrelated paths.
   rel=t/(mode+'_relocation');rel.mkdir();shutil.copy(source/'independent_verify.py',rel/'independent_verify.py')
   p,d=run(rel/'independent_verify.py',['--author-zip',str(z)],opt,t)
   require(p.returncode==0 and d['full_resolution'] is False,'independent relocation failed')
   p,d=run(original/'verify.py',[],opt,t)
   require(p.returncode==0 and d['exact_control_count']==17,'author baseline failed')
   baselines.append({'mode':mode,'relocated_independent_checker':'PASS','relocated_author_checker':'PASS'})
   claims={
    'operator':'Delta','laplacian_sign':'minus_sum_second_derivatives',
    'nonlinearity':'lambda*u^2*exp(2*u^2)',
    'lambda':'arbitrary_spatial_coefficient',
    'bubble_rhs_coefficient':48,
    'fundamental_log_pi_squared_denominator':16,
    'pohozaev_mass_pi_squared_denominator':8,
    'full_resolution':0,
    'checks_prove_global_PDE_claim':True,
    'extra_hypotheses_proved_from_target':True,
    'novelty_claim':True,
    'substantive_approaches':4}
   for j,(key,value) in enumerate(claims.items()):
    dst=t/(mode+'_claim_'+str(j));shutil.copytree(original,dst);edit(dst,'claims.json',key,value)
    p,d=run(dst/'verify.py',[],opt,t);require(p.returncode!=0 and '"status": "FAIL"' in p.stderr,'accepted claim mutation: '+key)
    rejections.append({'mode':mode,'case':'resealed_'+key,'status':'REJECTED'})
   for j,kind in enumerate(('manifest_duplicate_key','claim_duplicate_key','manifest_as_symlink','extra_directory','truncated_json','modified_verifier')):
    dst=t/(mode+'_structural_'+str(j));shutil.copytree(original,dst)
    if kind=='manifest_duplicate_key':
     p=dst/'MANIFEST.json';s=p.read_text();p.write_text(s.replace('"schema":','"schema": "sha256-byte-inventory-v1", "schema":',1))
    elif kind=='claim_duplicate_key':
     p=dst/'claims.json';s=p.read_text();p.write_text(s.replace('"dimension":','"dimension": 4, "dimension":',1));reseal(dst)
    elif kind=='manifest_as_symlink':
     p=dst/'MANIFEST.json';p.unlink();p.symlink_to(original/'MANIFEST.json')
    elif kind=='extra_directory':(dst/'unlisted').mkdir()
    elif kind=='truncated_json':
     (dst/'claims.json').write_text('{');reseal(dst)
    elif kind=='modified_verifier':
     p=dst/'verify.py';p.write_text(p.read_text()+'\n# altered byte identity\n')
    p,d=run(dst/'verify.py',[],opt,t);require(p.returncode!=0 and '"status": "FAIL"' in p.stderr,'accepted structural mutation: '+kind)
    rejections.append({'mode':mode,'case':kind,'status':'REJECTED'})
   # These are deliberate demonstrations of checker scope, not acceptance requirements.
   for j,kind in enumerate(('catalog_rank','unverified_pdf_digest')):
    dst=t/(mode+'_scope_'+str(j));shutil.copytree(original,dst)
    p=dst/'PUBLIC_METADATA.json';d=json.loads(p.read_text())
    if kind=='catalog_rank':d['catalog_rank']=999
    else:d['inspected_pdfs'][0]['sha256']='0'*64
    p.write_text(json.dumps(d,sort_keys=True,indent=2)+'\n');reseal(dst)
    p,d=run(dst/'verify.py',[],opt,t);require(p.returncode==0,'scope observation changed: '+kind)
    observations.append({'mode':mode,'case':kind,'author_checker':'ACCEPTS_RESEALED_MUTATION','interpretation':'The published external ZIP pin rejects modified bytes; author metadata validation alone is not comprehensive.'})
  for label,paths,checker in [('corpus',a.inputs,iv.corpus_replay),('pdf',a.pdf_inputs,iv.pdf_replay)]:
   if paths is None:continue
   paths=[str(Path(p).resolve()) for p in paths]
   checker(paths,md)
   for j,path in enumerate(paths):
    b=bytearray(Path(path).read_bytes());b[len(b)//2]^=1
    bad=t/(label+'_corrupted_'+str(j));bad.write_bytes(b)
    modified=paths[:];modified[j]=str(bad)
    try:checker(modified,md)
    except ValueError as e:
     require('corpus identity:' in str(e) or 'PDF bytes/hash:' in str(e),'unexpected source rejection')
     source_checks.append({'type':label,'input_index':j,'same_byte_count':True,'status':'REJECTED_BY_HASH'})
    else:raise ValueError('source corruption accepted')
  changed=bytearray(raw);changed[len(changed)//2]^=1
  variants={'single_bit_corruption':bytes(changed),'truncated_zip':raw[:-1],'trailing_bytes':raw+b'X','wrong_archive':b'PK\x03\x04'}
  for name,b in variants.items():
   try:iv.frozen(b)
   except ValueError as e:
    require(str(e)=='external author ZIP identity mismatch','unexpected corruption outcome')
    archive_checks.append({'case':name,'status':'REJECTED_BY_EXTERNAL_PIN'})
   else:raise ValueError('corruption accepted: '+name)
 print(json.dumps({'status':'PASS','additional_author_mutation_rejections':len(rejections),'external_archive_corruption_rejections':len(archive_checks),'source_corruption_rejections':len(source_checks),'source_checks':source_checks,'scope_observations':observations,'baseline_and_relocation':baselines,'rejections':rejections,'archive_checks':archive_checks,'full_resolution':False},indent=2,sort_keys=True))

if __name__=='__main__':
 try:main()
 except Exception as e:
  print(json.dumps({'status':'FAIL','error':str(e)}),file=sys.stderr);sys.exit(1)
