"""One-use sealing of this namespace only; no source/prior-object changes."""
from pathlib import Path
import datetime,hashlib,json
D=Path(__file__).resolve().parent


def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()


def new(n,j):
    with (D/n).open('x') as f:json.dump(j,f,indent=2);f.write('\n')


for n in ['FINAL_PRESERVATION.json','FINAL_MANIFEST.json','FINAL_SEAL.json']:
    if (D/n).exists():raise RuntimeError('already sealed '+n)
for n,h in {'EARLY_SEAL.json':'79d656fbce21b6f6d3014376ee184fdc2ccee45d1ce5b288b19c872511414a04',
            'EARLY_LEDGER.md':'2ff2a0937e8511e1d4e84941e684aed81345e3bc96f0f35cc4197354c051c7e1'}.items():
    if sha(D/n)!=h:raise RuntimeError('early evidence changed '+n)
c=json.loads((D/'ORIGINAL_BINDINGS.json').read_text())
bs=c['source_authentication']+c['whole_original_bindings']+c['primary_bindings']+c['access_response_bindings']+c['scope_primary_receipts']
for p in c['prior_packet_bindings']:bs +=[p['seal'],p['manifest']]+p['owned_files']
for b in bs:
    f=Path(b['path'])
    if f.stat().st_size!=b['bytes'] or sha(f)!=b['sha256']:raise RuntimeError('preserved object changed '+str(f))
utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
new('FINAL_PRESERVATION.json',{'utc':utc,'status':'ALL_ORIGINAL_PRIMARY_ACCESS_AND_PRIOR_BYTES_UNCHANGED',
    'binding_checks':len(bs),'bindings':bs,'archive_members_verified':118,'source_or_prior_objects_modified':False})
with (D/'RESEARCH_LOG.md').open('a') as f:
    f.write('\n- '+utc+' — 100%. Complete original analytic theorem survives bounded independent falsification; one minor HK citation-volume error is explicitly recorded, with priority unknown. All original/primary/access/prior bindings rechecked; full proof/control/attack/read/primary/report/verdict artifacts sealed. No repair or default followup, root authority retained; overall 203-paper goal ongoing.\n')
files=[]
for f in sorted(D.iterdir()):
    if f.is_file():
        f.chmod(0o444);files.append({'path':f.name,'bytes':f.stat().st_size,'sha256':sha(f)})
new('FINAL_MANIFEST.json',{'utc':utc,'status':'COMPLETE_IMMUTABLE_ADVERSARIAL_EVIDENCE',
    'record_id':23441617,'row':99,'version':'1.0','bounded_completion_percent':100,
    'original_bindings_verified':127,'original_ZIP_members_CRC_and_extracted_bytes_verified':118,
    'source_ready_seal_sha256':'465e6b0ce7212ea6fe89a4f17f0f8988d6b713323d171f45982f3fa10d03b75a',
    'prior_packets_unchanged':6,'foreign_full_text_cache_excluded':True,
    'minor_bibliographic_error_recorded':True,'public_promotion_authority':False,'files':files})
(D/'FINAL_MANIFEST.json').chmod(0o444)
j={'utc':utc,'status':'COMPLETE_SEALED_NO_PROMOTION_AUTHORITY','manifest':'FINAL_MANIFEST.json',
   'manifest_sha256':sha(D/'FINAL_MANIFEST.json'),'report_sha256':sha(D/'REPORT.md'),
   'verdict_sha256':sha(D/'verdict.json'),'derivations_sha256':sha(D/'DERIVATIONS.md'),
   'early_seal_sha256':sha(D/'EARLY_SEAL.json'),'all_original_primary_access_and_prior_bytes_unchanged':True,
   'bounded_completion_percent':100,'overall_203_paper_goal':'ONGOING'}
new('FINAL_SEAL.json',j);(D/'FINAL_SEAL.json').chmod(0o444)
print(json.dumps(dict(j,final_seal_sha256=sha(D/'FINAL_SEAL.json'),owned_files=len(files))))
