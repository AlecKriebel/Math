#!/usr/bin/env python3
"""Read/copy only; creates an offline private mirror, never repository mutations."""
from pathlib import Path
import argparse,datetime,hashlib,json,re
if not globals().get('_PR1131_SOURCE_VERIFIED',False):raise RuntimeError('Use externally verified bootstrap')
from ops_common import OPS,AUDIT,REPO,PRIVATE,package,proposal
EXPECTED=_PR1131_EXECUTION['operations_sha256']
BOOT=_PR1131_EXECUTION['bootstrap_sha256']
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(b):return {'bytes':len(b),'sha256':sha(b)}
def prepare(label):
    if re.fullmatch(r"[A-Za-z0-9_-]{1,64}",label) is None:raise RuntimeError("Invalid private fixture label")
    raw=(OPS/'OPERATIONS_MANIFEST.json').read_bytes()
    if sha(raw)!=EXPECTED:raise RuntimeError('Target seal changed')
    manifest=json.loads(raw)
    package();proposal()
    output_root=PRIVATE
    label='repair03_'+label+'_'+__import__('uuid').uuid4().hex
    mirror=output_root/label/'Math';mirror.mkdir(parents=True,exist_ok=False)
    inventory={}
    def copy(source):
        b=source.read_bytes();dest=mirror/source.relative_to(REPO);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(b)
        if dest.read_bytes()!=b:raise RuntimeError('Copy failure')
        inventory[str(source.relative_to(REPO))]=pin(b)
    for n,p in manifest['files'].items():
        if pin((OPS/n).read_bytes())!=p:raise RuntimeError('Target changed '+n)
        copy(OPS/n)
    copy(OPS/'OPERATIONS_MANIFEST.json')
    if sha((OPS/'bootstrap.py').read_bytes())!=BOOT:raise RuntimeError('Wrong bootstrap')
    copy(REPO/'zenodo_deposit_tool/zenodo.py')
    science=json.loads((AUDIT/'ROOT_SCIENTIFIC_CLEARANCE.json').read_bytes())
    for n in {'ROOT_SCIENTIFIC_CLEARANCE.json','PACKAGE_FREEZE_01.json','reviews/package01/FINAL_REVIEW_MANIFEST.json','reviews/package02/MANIFEST.json',*science['root_acceptance_pins']}:
        copy(AUDIT/n)
    source=json.loads((AUDIT/'publication/SOURCE_MANIFEST.json').read_bytes());freeze=json.loads((AUDIT/'PACKAGE_FREEZE_01.json').read_bytes())
    for n in set(source)|set(freeze['frozen_six'])|{'SOURCE_MANIFEST.json'}:copy(AUDIT/'publication'/n)
    for n in ['ledger.json','pr.json','gate.json',*[f'account_{c}_page_{i}.json' for c in 'ab' for i in range(1,10)]]:
        copy(OPS/'private/live_8e3a39143bb740ef9053274be751a820'/n)
    for n in json.loads((OPS/'NATIVE_SCHEMA_REFERENCE.json').read_bytes())['captures']:
        b=(OPS/'private/repair_native_reference'/n).read_bytes()
        if pin(b)!={k:json.loads((OPS/'NATIVE_SCHEMA_REFERENCE.json').read_bytes())['captures'][n][k] for k in ['bytes','sha256']}:raise RuntimeError('Schema reference changed')
        copy(OPS/'private/repair_native_reference'/n)
    receipt={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'target_manifest':pin(raw),'bootstrap_sha256':BOOT,'mirror':str(mirror),'files':inventory,'no_credentials_copied':True,'external_reads':0,'external_mutations':0}
    out=output_root/label/'COPY_RECEIPT.json';out.write_text(json.dumps(receipt,indent=2)+'\n')
    return mirror,receipt
def main():
    p=argparse.ArgumentParser();p.add_argument('label');a=p.parse_args();m,r=prepare(a.label);print(json.dumps({'mirror':str(m),'files_copied':len(r['files']),'manifest':r['target_manifest'],'external_mutations':0}))

if __name__=='__main__':main()
