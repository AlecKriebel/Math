"""Check actual package registry without schema inference, plus corruption probes."""
from pathlib import Path, PurePosixPath
import copy, hashlib, importlib.util, json
R=Path(__file__).resolve().parent;A=R.parents[1];P=A/'publication';root=R/'_local/extracted'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def require(x,msg):
    if not x:raise RuntimeError(msg)
context=json.loads((A/'CURRENT_PR1262_CONTEXT.json').read_text());registries=[]
require(len(context['authored_freezes'])==13,'explicit13 count')
for reg in context['authored_freezes']:
    require(sha(root/reg['path'])==reg['sha256'],'outside nested anchor')
    obj=json.loads((root/reg['path']).read_text());entries=obj[reg['entries_key']];names=[]
    for entry in entries:
        selected=entry[reg['path_key']];name=PurePosixPath(selected)
        require(not name.is_absolute() and '..' not in name.parts,'relative selected membership')
        f=root/reg['base']/selected;require(f.stat().st_size==entry[reg['size_key']] and sha(f)==entry['sha256'],'selected member binding')
        names.append(selected)
    require(len(names)==len(set(names)),'duplicate')
    registries.append({'manifest':reg['path'],'selected_schema':[reg[k] for k in ['entries_key','path_key','size_key']],'members':len(names),'all_selected_bytes_matched':True})
spec=importlib.util.spec_from_file_location('actual_portable',root/'verify.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
anchors=json.loads((P/'BUILD_RECEIPT.json').read_text())['verification_anchors']
def verify():return v.verify(root,anchors['manifest'],anchors['context'],anchors['snapshot'])
checks=[]
def fails(label,fn):
    try:fn()
    except ValueError as e:checks.append({'label':label,'rejection':str(e)});return
    raise RuntimeError('Unexpected acceptance '+label)
fails('wrong_outside_root_anchor',lambda:v.verify(root,'0'*64,anchors['context'],anchors['snapshot']))
fails('wrong_outside_context_anchor',lambda:v.verify(root,anchors['manifest'],'0'*64,anchors['snapshot']))
fails('wrong_outside_snapshot_anchor',lambda:v.verify(root,anchors['manifest'],anchors['context'],'0'*64))
for rel in ['current_edition/PROOF.md','reviews/fourier_adversary/AUTHORED_MANIFEST.json','original_submitted/README.md','verify.py']:
    p=root/rel;old=p.read_bytes();p.write_bytes(old+b'\nCORRUPTED\n')
    try:fails('corrupt_'+rel,verify)
    finally:p.write_bytes(old)
extra=root/'UNLISTED.txt';extra.write_text('not in package')
try:fails('unlisted_member',verify)
finally:extra.unlink()
require(verify()['status']=='PASS','restored package')
for name in ['ACCEPTANCE.json','SOURCES.json','VERIFICATION.json']:
    current=json.loads((root/'current_edition'/name).read_text());require(current['historical_submitted_record_20261011']==json.loads((root/'original_submitted'/name).read_text()),'exact parsed historical wrapper')
require(len(context['diagnostic_replays'])==2 and all(x['mode']=='normal_O_OO' and x['comparison']=='json_exact' for x in context['diagnostic_replays']),'two exact replay contract')
metadata=json.loads((P/'zenodo-deposit.json').read_text());require(set(metadata['metadata'])==v.FIELDS and metadata['metadata']==context['metadata'],'exact11 current metadata')
print(json.dumps({'status':'PASS','explicit_registries':registries,'corruption_controls':checks,'three_historical_wrappers_exact':True,'metadata11_exact':True,'only_two_automatic_exact_diagnostics':True,'fixture_scope':'Only actual extracted scratch bytes altered/restored; production inputs untouched.'},indent=2))
