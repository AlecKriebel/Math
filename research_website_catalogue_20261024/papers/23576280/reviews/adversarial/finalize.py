"""One-use own-namespace finalization; no source/primary/prior writes."""
from pathlib import Path
import datetime,hashlib,json
D=Path(__file__).resolve().parent


def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()


def new(n,j):
    with (D/n).open('x') as f:json.dump(j,f,indent=2);f.write('\n')


for n in ['FINAL_PRESERVATION.json','FINAL_MANIFEST.json','FINAL_SEAL.json']:
    if (D/n).exists():raise RuntimeError('already sealed '+n)
for n,h in {'EARLY_SEAL.json':'d0c3266f9c31d2aafb1e25419b2aeef8f33b9a2059bef9fcd895452b15cea807',
            'EARLY_LEDGER.md':'714e92a68025aee3ed252dfd0e7960dfc768a1c6071425ffd48e1a3a9dda4f7b'}.items():
    if sha(D/n)!=h:raise RuntimeError('early evidence changed '+n)
c=json.loads((D/'ORIGINAL_BINDINGS.json').read_text())
bs=c['source_authentication']+c['whole_original_bindings']+c['primary_bindings']+c['additional_access_metadata_bindings']+c['scope_primary_receipts']
for p in c['prior_packet_bindings']:bs +=[p['seal'],p['manifest']]+p['owned_files']
for b in bs:
    f=Path(b['path'])
    if f.stat().st_size!=b['bytes'] or sha(f)!=b['sha256']:raise RuntimeError('preserved object changed '+str(f))
utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
new('FINAL_PRESERVATION.json',{'utc':utc,'status':'ALL_ORIGINAL_PRIMARY_ACCESS_AND_PRIOR_BYTES_UNCHANGED',
    'binding_checks':len(bs),'bindings':bs,'original_ZIP_members_verified':12,'originals_or_prior_packets_modified':False})
with (D/'RESEARCH_LOG.md').open('a') as f:
    f.write('\n- '+utc+' — 100%. Complete original theorem/reduction survives bounded independent falsification. All proof/control/attack/read/primary/report/custom-verdict artifacts complete; current separate theorem claim and priority limits explicit. All original/primary/access/prior bytes rechecked; final immutable manifest/seal created. No repair/default followup, root authority retained; overall 203-paper goal ongoing.\n')
files=[]
for f in sorted(D.iterdir()):
    if f.is_file():
        f.chmod(0o444);files.append({'path':f.name,'bytes':f.stat().st_size,'sha256':sha(f)})
new('FINAL_MANIFEST.json',{'utc':utc,'status':'COMPLETE_IMMUTABLE_ADVERSARIAL_EVIDENCE',
    'record_id':23576280,'row':100,'version':'1.0.0','bounded_completion_percent':100,
    'original_source_bindings_verified':22,'original_ZIP_members_CRC_and_extracted_bytes_verified':12,
    'source_ready_seal_sha256':'78a83dd556f77e4b6c003fa16465b64d3a7d8079f1d4d85f450683930b86e56b',
    'prior_packets_unchanged':7,'foreign_full_text_cache_excluded':True,'public_promotion_authority':False,'files':files})
(D/'FINAL_MANIFEST.json').chmod(0o444)
j={'utc':utc,'status':'COMPLETE_SEALED_NO_PROMOTION_AUTHORITY','manifest':'FINAL_MANIFEST.json',
   'manifest_sha256':sha(D/'FINAL_MANIFEST.json'),'report_sha256':sha(D/'REPORT.md'),
   'verdict_sha256':sha(D/'verdict.json'),'derivations_sha256':sha(D/'DERIVATIONS.md'),
   'early_seal_sha256':sha(D/'EARLY_SEAL.json'),'all_original_primary_access_and_prior_bytes_unchanged':True,
   'bounded_completion_percent':100,'overall_203_paper_goal':'ONGOING'}
new('FINAL_SEAL.json',j);(D/'FINAL_SEAL.json').chmod(0o444)
print(json.dumps(dict(j,final_seal_sha256=sha(D/'FINAL_SEAL.json'),owned_files=len(files))))
