#!/usr/bin/env python3
"""Retrieve exact original ESI payload and replay original source-enabled wrapper."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, subprocess, sys
A=Path(__file__).resolve().parent
RUN=A/'root_replay_private/source_manifest_001'
def sha(b): return hashlib.sha256(b).hexdigest()
def utc(): return datetime.now(timezone.utc).isoformat()
def run(label,argv,cwd):
    start=utc(); p=subprocess.run(argv,cwd=cwd,capture_output=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
    end=utc()
    (RUN/(label+'.stdout')).write_bytes(p.stdout)
    (RUN/(label+'.stderr')).write_bytes(p.stderr)
    rec=dict(argv=argv,cwd=str(cwd),started_utc=start,completed_utc=end,exit_code=p.returncode,
             stdout=dict(path=label+'.stdout',bytes=len(p.stdout),sha256=sha(p.stdout)),
             stderr=dict(path=label+'.stderr',bytes=len(p.stderr),sha256=sha(p.stderr)))
    (RUN/(label+'.execution.json')).write_text(json.dumps(rec,indent=2)+'\n')
    return p,rec
def main():
    assert not RUN.exists(); RUN.mkdir(parents=True)
    p,download=run('esi',['curl','--fail','--silent','--show-error','--location','--max-time','45',
                            'https://www.esi.ac.at/preprints/esi2075.pdf'],A)
    assert p.returncode==0,download
    assert len(p.stdout)==1544891 and sha(p.stdout)=='0628d7a9acb61435d6513d919966502821ee8a38f4a9ec0a49f8e55264af1dd4'
    aliases=RUN/'sources';aliases.mkdir()
    (aliases/'bardet-keller-zweimueller.pdf').write_bytes(p.stdout)
    (aliases/'owr2009-49.pdf').write_bytes((A/'root_sources_private/owr2009_49.pdf').read_bytes())
    (aliases/'bkz-arxiv.pdf').write_bytes((A/'root_sources_private/bkz_arxiv_v1.pdf').read_bytes())
    original=A/'snapshot/problems/30001370_basin_boundaries'
    manifest=json.loads((original/'SOURCE_MANIFEST.json').read_bytes())
    for row in manifest['files']:
        b=(aliases/row['name']).read_bytes()
        assert (len(b),sha(b))==(row['bytes'],row['sha256'])
    copy=A/'root_replay_private/candidate_001/execution_copy'
    wrapper,rec=run('wrapper',[sys.executable,'-B',str(copy/'verify_packet.py'),'--source-dir',str(aliases)],copy)
    assert wrapper.returncode==0 and not wrapper.stderr,rec
    result=json.loads(wrapper.stdout)
    assert result['status']=='PASS'
    out={'utc':utc(),'status':'PASS_ALL_THREE_ORIGINAL_SOURCE_PAYLOADS_AND_SOURCE_ENABLED_REPLAY',
         'native_runs':[download,rec],'wrapper_result':result,'source_manifest_files':manifest['files'],
         'scope':'Exact source bytes and original wrapper reproduction. This does not assert every distinct PDF is the final journal version or a proof of historical novelty.'}
    (A/'ROOT_SOURCE_MANIFEST_REPLAY_RECEIPT.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'status':out['status'],'source_files':3},indent=2))
if __name__=='__main__': main()
