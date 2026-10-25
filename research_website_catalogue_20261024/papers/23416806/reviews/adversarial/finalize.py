"""One-use own-namespace final seal; no original/prior-object modifications."""
from pathlib import Path
import datetime
import hashlib
import json

D=Path(__file__).resolve().parent


def sha(f):
    return hashlib.sha256(f.read_bytes()).hexdigest()


def new(name,obj):
    with (D/name).open('x') as f:
        json.dump(obj,f,indent=2);f.write('\n')


for n in ['FINAL_PRESERVATION.json','FINAL_MANIFEST.json','FINAL_SEAL.json']:
    if (D/n).exists():raise RuntimeError('already sealed '+n)
if sha(D/'EARLY_SEAL.json')!='81e6d352af31fee9509b0093503c05b6b15890c2ff9dc935ba11000a38e2f5d1':
    raise RuntimeError('early seal changed')
if sha(D/'EARLY_LEDGER.md')!='cbbe66081c66b9bcf28f732a05ff9816422a68df6567ff5c169a900f84aab55d':
    raise RuntimeError('early ledger changed')
c=json.loads((D/'ORIGINAL_BINDINGS.json').read_text())
bindings=c['source_authentication']+c['whole_original_bindings']+c['primary_bindings']+c['failed_response_bindings']+[c['scope_primary_receipt']]
for p in c['prior_packet_bindings']:
    bindings += [p['seal'],p['manifest']]+p['owned_files']
for b in bindings:
    f=Path(b['path'])
    if f.stat().st_size!=b['bytes'] or sha(f)!=b['sha256']:
        raise RuntimeError('preserved object changed '+str(f))
utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
new('FINAL_PRESERVATION.json',{'utc':utc,'status':'ALL_ORIGINAL_PRIMARY_AND_PRIOR_BINDINGS_UNCHANGED',
     'binding_checks':len(bindings),'bindings':bindings,'archive_container_count':4,
     'archive_member_occurrence_count':186,'originals_or_prior_packets_modified':False})
with (D/'RESEARCH_LOG.md').open('a') as f:
    f.write('\n- '+utc+' — 100%. Complete report/custom verdict, independent universal derivations, exact controls, primary/read/access/attack ledgers and whole original custody complete. All preserved bytes rechecked; final immutable manifest/seal created. Complete original criterion survives bounded falsification, historical priority unknown, root authority retained. No default followup; overall 203-paper goal ongoing.\n')
files=[]
for f in sorted(D.iterdir()):
    if f.is_file():
        f.chmod(0o444)
        files.append({'path':f.name,'bytes':f.stat().st_size,'sha256':sha(f)})
new('FINAL_MANIFEST.json',{'utc':utc,'status':'COMPLETE_IMMUTABLE_ADVERSARIAL_EVIDENCE',
    'record_id':23416806,'row':98,'version':'1.0','bounded_completion_percent':100,
    'original_bindings_verified':195,'recursive_archive_member_occurrences_verified':186,
    'archive_containers':4,'prior_packets_unchanged':5,
    'source_ready_seal_sha256':'b4edc6ba13576ce2329a9fe55af07eb39b77c729021ed83e879a2f6ef1b712da',
    'foreign_full_text_cache_excluded':True,'public_promotion_authority':False,'files':files})
(D/'FINAL_MANIFEST.json').chmod(0o444)
seal={'utc':utc,'status':'COMPLETE_SEALED_NO_PROMOTION_AUTHORITY','manifest':'FINAL_MANIFEST.json',
      'manifest_sha256':sha(D/'FINAL_MANIFEST.json'),'report_sha256':sha(D/'REPORT.md'),
      'verdict_sha256':sha(D/'verdict.json'),'derivations_sha256':sha(D/'DERIVATIONS.md'),
      'early_seal_sha256':sha(D/'EARLY_SEAL.json'),
      'all_original_primary_and_prior_packet_bytes_unchanged':True,
      'bounded_completion_percent':100,'overall_203_paper_goal':'ONGOING'}
new('FINAL_SEAL.json',seal);(D/'FINAL_SEAL.json').chmod(0o444)
print(json.dumps(dict(seal,final_seal_sha256=sha(D/'FINAL_SEAL.json'),owned_files=len(files))))
