#!/usr/bin/env python3
"""Read immutable prepared/pushed/merged objects and exact target bindings only."""
from pathlib import Path
import argparse,datetime,hashlib,json,subprocess,types
A=Path(__file__).absolute().parent
s=A/'prepare_integration.py';M=types.ModuleType('_root_integration');M.__file__=str(s);exec(compile(s.read_bytes(),str(s),'exec'),M.__dict__)
def require(v,why):
 if not v:raise ValueError(why)
def git(*args):return subprocess.check_output(['git',*args],cwd=M.REPO)
def main():
 p=argparse.ArgumentParser();p.add_argument('--receipt',default='INTEGRATION_PREPARED_RECEIPT.json');p.add_argument('--commit');p.add_argument('--output',required=True);x=p.parse_args()
 r=json.loads((A/x.receipt).read_text());c=x.commit or r['integration_commit'];doi=r['doi']
 inputs=M.publication_inputs(A/'publication',doi,A/'ZENODO_PUBLICATION_RECEIPT.json',A/'ZENODO_POST_PUBLICATION_INSPECTION.json')
 files=M.build_publication(inputs,doi,r['prepared_utc']);expected={M.PREFIX+n:d for n,d in inputs['original'].items()}|{M.PUB_PREFIX+n:d for n,d in files.items()}
 for name,data in expected.items():require(git('show',c+':'+name)==data,'actual bytes differ '+name)
 require(git('ls-tree','-r','-z',c,'--',M.PREFIX)==git('ls-tree','-r','-z',M.ORIGINAL,'--',M.PREFIX),'native24 blob/mode mismatch')
 pub_paths={z.split(b'\t',1)[1].decode() for z in git('ls-tree','-r','-z',c,'--',M.PUB_PREFIX).split(b'\0') if z}
 require(pub_paths=={M.PUB_PREFIX+n for n in files},'publication inventory differs')
 main_queue=git('show',r['main_base']+':'+M.QPATH);wanted,patch=M.patch_queue(main_queue,doi,inputs['snapshot']['queue_row']);actual=git('show',c+':'+M.QPATH)
 _,_,line,_=M.queue_row(actual);_,_,wantline,_=M.queue_row(wanted);require(line==wantline,'merged target row mismatch')
 if c==r['integration_commit']:require(actual==wanted,'integration changed other queue bytes')
 changed={n.decode() for n in git('diff','--name-only','-z',r['main_base'],r['integration_commit']).split(b'\0') if n}
 require(changed==set(expected)|{M.QPATH},'prepared change allowlist mismatch')
 require({n:hashlib.sha256(d).hexdigest() for n,d in files.items()}==r['publication_sha256'],'receipt publication pin mismatch')
 info=json.loads(files['PUBLICATION.json']);confirmed=json.loads(inputs['receipt_bytes'][0])['verified_utc']
 require(info['publication_confirmed_utc']==confirmed and info['integration_prepared_utc']==r['prepared_utc'] and 'published_utc' not in info,'timestamp labels wrong')
 report={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','commit':c,'tree':git('rev-parse',c+'^{tree}').decode().strip(),'prepared_commit':r['integration_commit'],'base':r['main_base'],'changed_paths_from_preparation_base':len(changed),'native_files':len(inputs['original']),'publication_files':len(files),'all_exact_bytes_and_native_modes_verified':True,'queue_selected_line':line.decode().rstrip('\r\n'),'only_selected_three_queue_cells_in_prepared_tree':patch,'publication_confirmed_utc':confirmed,'integration_prepared_utc':r['prepared_utc'],'published_eleven_files_unchanged':True,'read_only':True}
 (A/x.output).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:report[k] for k in ('status','commit','tree','native_files','publication_files','changed_paths_from_preparation_base')}))
if __name__=='__main__':main()
