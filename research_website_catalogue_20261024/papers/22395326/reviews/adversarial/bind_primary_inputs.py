"""Hash actual primary inputs and selected inert archive interfaces, without execution."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,tarfile
D=Path(__file__).resolve().parent;P=D.parents[3];E=P/'papers/22395326/reviews/scope'
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()
def req(c,m):
    if not c:raise RuntimeError(m)
def bind(p,expected=None):
    p=Path(p);r={'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p)}
    if expected:req(r['sha256']==expected,'primary drift: '+str(p))
    return r
receipts=[];bodies=[];code=[]
for name in ['primary-custody.json','foreign-primary-fetch-receipts.json','additional-primary-receipts.json','primary-interface-code-custody.json']:
    receipts.append(bind(E/name))
for row in json.loads((E/'primary-custody.json').read_text())['primary_bodies']:
    bodies.append(bind(row['actual_original_pdf_path'],row['sha256']))
    bodies.append(bind(row['extraction_path'],row['extraction_sha256']))
for name in ['foreign-primary-fetch-receipts.json','additional-primary-receipts.json']:
    for row in json.loads((E/name).read_text()):
        bodies.append(bind(row['body_path'],row['sha256']))
        bodies.append(bind(row.get('extraction_path',row.get('text_path')),row.get('extraction_sha256',row.get('text_sha256'))))
for row in json.loads((E/'primary-interface-code-custody.json').read_text())['members']:
    code.append(bind(row['cache_path'],row['SHA256']))
jc=P/'papers/22395326/reviews/analytic/cache'
for name in ['verify.sh','verifiers/run_gate.py','verifiers/internal_math_gates.py']:
    code.append(bind(jc/'jc-selected'/name))
archives=[bind(jc/'stc_jc_sharp_boundary_atlas_certificates_v1.1.7.tar.gz','ffcce5398c8be387d6d808620fc939490f31ac41fb48592e22608cf0e7b05db4')]
k3=P/'papers/22178672/sources/K3P_Level2_Full_Reproducibility_v1.0.0.tar.gz'
archives.append(bind(k3,'4f84417f40b4e5ddae80b36d87dc7bb6d00389a573a58d0b82a2592c9f7c6403'))
selected=[]
with tarfile.open(k3,'r:gz') as archive:
    for name,expected in [('K3P_SHARPNESS_KRAWCZYK_CERTIFICATE.json','8187174b3e0c0b3a0a55fa32595c211811c357dc223ada7a74b3033f7cae3941'),('K3P_SHARPNESS_TOPOLOGY_ALL_N_CERTIFICATE.json','aa08837777445541398bed943881405530c9b5bb4f0451794a4b56b289beabc7'),('K3P_SHARPNESS_REPLAY_MANIFEST.json','1a1c76fb43f4cd4769bd83a3e37fef1eec7edee2e9e8ac1ca83d95b096dc191f'),('independent_krawczyk_replay.py','0b0cd56fa481a11b67a9129cf68a4b851fc88f0735cb78d223ca0b6af4cc7ffc')]:
        m=archive.getmember('k3p_level2_reproducibility/sharpness/'+name);req(m.isfile(),'regular selected member')
        blob=archive.extractfile(m).read();h=hashlib.sha256(blob).hexdigest();req(h==expected,'selected sharpness drift')
        selected.append({'archive':str(k3),'member':m.name,'bytes':len(blob),'sha256':h,'full_foreign_copy_written':False})
result={'utc':datetime.now(timezone.utc).isoformat(),'transport_custody_receipts':receipts,'actual_PDF_and_extraction_bindings':bodies,'selected_interface_bindings':code,'original_archive_bindings':archives,'selected_sharpness_members':selected,'all_match_supplied_raw_bindings':True,'scope':'Hash verification does not claim full reading or execution. Exact reading boundaries are in READ_LEDGER.md; archive payloads were not copied or modified.'}
(D/'PRIMARY_BINDINGS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'PDFs_and_extracts':len(bodies),'interface_files':len(code),'archives':len(archives),'sharpness_selected_members':len(selected),'all_match':True}))
