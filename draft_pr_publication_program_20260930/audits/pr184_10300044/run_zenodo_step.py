"""Run the repository's exact uploader on the cleared unchanged packet."""
from pathlib import Path
import hashlib,json,subprocess,sys
A=Path(__file__).resolve().parent;R=Path('/Users/alec/Documents/Math');PY='/opt/homebrew/opt/python@3.14/bin/python3.14'
g=json.loads((A/'ROOT_PUBLICATION_GATE.json').read_text())
if g['status']!='READY_FOR_AUTHORIZED_PUBLICATION':raise RuntimeError('No publication gate')
P=A/g['package_name']
for n,x in g['payloads'].items():
 if hashlib.sha256((P/n).read_bytes()).hexdigest()!=x['SHA256']:raise RuntimeError('Reviewed payload drift '+n)
action=sys.argv[1];names={'check':'ZENODO_LOCAL_CHECK.json','stage':'ZENODO_STAGE_READBACK.json','inspect':'ZENODO_DRAFT_READBACK.json','publish':'ZENODO_PUBLICATION_READBACK.json','inspect-published':'ZENODO_POSTPUBLICATION_INSPECTION.json'}
if action not in names:raise RuntimeError('Unknown action')
args=[PY,'-E','-S','-B','-P',str(R/'zenodo_deposit_tool/zenodo.py'),'inspect' if action=='inspect-published' else action,str(P/'zenodo-deposit.json')]
if action=='publish':
 stage=json.loads((A/'ZENODO_STAGE_READBACK.json').read_text());ident=str(stage['id'])
 if len(sys.argv)!=3 or sys.argv[2]!=ident:raise RuntimeError('Exact actual draft ID required')
 args+=['--confirm-id',ident]
if action=='inspect-published':args+=['--check-doi']
result=subprocess.run(args,cwd=R,capture_output=True,timeout=300);(A/names[action]).write_bytes(result.stdout);(A/(names[action]+'.stderr.txt')).write_bytes(result.stderr)
if result.returncode:raise RuntimeError('Uploader returned error; inspect saved redacted result and existing deposit state before another mutation')
j=json.loads(result.stdout);print(json.dumps({k:j[k] for k in ['id','state','doi','doi_url','record_url','metadata_normalizations','doi_resolution','receipt_saved'] if k in j}))
