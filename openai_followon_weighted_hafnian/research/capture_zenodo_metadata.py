"""Read-only evidence capture through the repository Zenodo client; no mutations."""
import argparse, datetime, json, runpy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
TOOL=ROOT.parent/'zenodo_deposit_tool/zenodo.py'

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--output',required=True)
    args=parser.parse_args()
    api=runpy.run_path(str(TOOL),run_name='zenodo_evidence')
    manifest=ROOT/'zenodo-deposit.json'
    metadata,files=api['load_manifest'](manifest)
    state_path,state=api['local_state'](manifest,'production')
    if not state: raise RuntimeError('No project-local production deposit state')
    client=api['ZenodoClient']('production',api['token_for']('production'))
    deposit=client.get(state['id'])
    api['validate_record'](deposit,state['id'])
    normalizations=api['verify'](deposit,metadata,files)
    remote=api['server_files'](deposit)
    receipt={
        'verified_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'environment':'production','id':deposit['id'],
        'submitted':deposit['submitted'],'doi':deposit.get('doi'),
        'reserved_doi':deposit.get('metadata',{}).get('prereserve_doi'),
        'metadata':deposit['metadata'],'metadata_normalizations':normalizations,
        'remote_files':{name:{k:f[k] for k in ('filename','filesize','checksum') if k in f}
                        for name,f in remote.items()},
        'verified_local_files':[{k:f[k] for k in ('name','size','sha256','md5')} for f in files],
        'scope':'read-only metadata and remote MD5/size verification; reserved DOI is not publication'}
    Path(args.output).write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))

if __name__=='__main__': main()
