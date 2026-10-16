"""Hash primary papers and private chronology in place; never copy their bodies."""
from pathlib import Path
from datetime import datetime, timezone
import base64, gzip, hashlib, json, zipfile

O=Path(__file__).resolve().parent;C=O.parent;B=C/'preprint';D=C/'initial_review_20261016'
G=D/'priority_classical_general_01/private_reading';A=D/'priority_author_updates_01/private_reading'
P=C.parent/'pr210_5100033/initial_review_20261015'
def pin(p):
    raw=p.read_bytes();return dict(path=str(p),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
primary=[]
for folder,names in [
 (G,['kls_cyclic_II_v1.pdf','kls_cyclic_II_v1.txt','kls_cyclic_II.pdf','kls_cyclic_II.txt','ks_landen.pdf','ks_landen.txt','ast_revisited_v2.pdf','ast_revisited_v2.txt','bt_reznik_v2.pdf','bt_reznik_v2.txt','chavez_areas_final.pdf','chavez_areas_final.txt']),
 (A,['invariants_v1.pdf','invariants_v1.txt','invariants_v11.txt','original_published.txt','stachel_published.txt','ferudun14_v10.pdf','ferudun14_v10.txt','ferudun_v11_main.tex','ferudun_v10_main.tex','ferudun14_v11_source.zip','ferudun14_v10_source.zip','zenodo23088516.json','zenodo23087221.json','dlmf22_4.html','dlmf22_8.html']),
 (P/'private_reading',['invariants_v11.pdf','invariants_final.pdf','stachel_published.pdf']),
 (P/'priority_author_updates_01/private_reading',['ferudun14_v11.pdf']),
 (P/'priority_classical_general_01/private_reading',['ks_pramana_final_ias.txt'])]:
    for name in names:primary.append(pin(folder/name))
versions=[]
for label,record,pdf,archive in [
 ('1.0','23087221',A/'ferudun14_v10.pdf',A/'ferudun14_v10_source.zip'),
 ('1.1','23088516',P/'priority_author_updates_01/private_reading/ferudun14_v11.pdf',A/'ferudun14_v11_source.zip')]:
    obj=json.loads((A/('zenodo'+record+'.json')).read_text());files={f['key']:f for f in obj['files']}
    for p,key in [(pdf,'main.pdf'),(archive,'arxiv_source.zip')]:
        assert p.stat().st_size==files[key]['size'] and hashlib.md5(p.read_bytes()).hexdigest()==files[key]['checksum'].removeprefix('md5:')
    with zipfile.ZipFile(archive) as z:
        members=[dict(path=i.filename,bytes=i.file_size,sha256=hashlib.sha256(z.read(i)).hexdigest()) for i in z.infolist()]
        tex=[i for i in z.namelist() if i.endswith('main.tex')];assert len(tex)==1
        main=z.read(tex[0]);assert main==(A/('ferudun_v'+label.replace('.','')+'_main.tex')).read_bytes()
    versions.append(dict(version=label,DOI=obj['doi'],concept_DOI=obj['conceptdoi'],provider_created=obj['created'],pdf=pin(pdf),source_archive=pin(archive),source_members=members,actual_provider_MD5_match=True,full_exact_center_theorem_in_v11=label=='1.1'))

chron=json.loads((D/'priority_public_chronology_01/PUBLIC_CHRONOLOGY_OBSERVATIONS.json').read_text())
captures=[];texts=[];proof_match=[];nodes=[]
target_sha='4f2eac23212f3fdf1c0c17ba79081e6dc9790907d1725c7359e9461052eabfc2'
def walk(o):
    if isinstance(o,dict):
        nodes.append(o)
        if o.get('encoding')=='base64' and isinstance(o.get('content'),str):
            decoded=base64.b64decode(o['content'])
            if hashlib.sha256(decoded).hexdigest()==target_sha:proof_match.append(dict(bytes=len(decoded),sha256=target_sha,native_blob=o.get('sha')))
        for x in o.values():walk(x)
    elif isinstance(o,list):
        for x in o:walk(x)
    elif isinstance(o,str) and o.lstrip().startswith(('{','[')):
        try:parsed=json.loads(o)
        except (ValueError,TypeError):return
        walk(parsed)
for r in chron['raw_capture_pins']:
    p=D/'priority_public_chronology_01'/r['path'];stored=p if p.exists() else p.with_suffix(p.suffix+'.gz')
    data=gzip.decompress(stored.read_bytes()) if stored.suffix=='.gz' else stored.read_bytes()
    assert len(data)==r['bytes'] and hashlib.sha256(data).hexdigest()==r['sha256']
    texts.append(data.decode());walk(json.loads(data));captures.append(dict(declared_path=r['path'],actual_retained=pin(stored),uncompressed_bytes=len(data),uncompressed_sha256=hashlib.sha256(data).hexdigest()))
assert proof_match,'Actual captured GitHub proof body must match original bytes'
combined='\n'.join(texts)
for required in ['2026-10-01T05:35:19Z','2026-10-01T05:48:56Z','ffe123ee3b525fd4f6c11c2f9eac89b8f3cea6fe','d9f8fbf8cbf6f48cde01d05e7ea39dc7a551a843']:
    assert required in combined
checks=[n for n in nodes if n.get('created_at')=='2026-10-01T05:35:19Z' and n.get('head_sha')=='ffe123ee3b525fd4f6c11c2f9eac89b8f3cea6fe']
assert len(checks)>=2
assert any(n.get('created_at')=='2026-10-01T05:48:56Z' and n.get('number')==209 for n in nodes)

# Verify original and additive author seals and the first whole-package review,
# without adopting those reviews' conclusions as scientific premises.
seals=[]
for p in sorted((B/'verification/audits').glob('*/AUTHORED_MANIFEST.json')):
    obj=json.loads(p.read_text());rows=obj.get('files',obj.get('payloads'));base=p.parent
    for r in rows:
        actual=pin(base/r['path']);assert actual['bytes']==r['bytes'] and actual['sha256']==r['sha256']
    seals.append(dict(manifest=pin(p),payloads=len(rows),all_declared_payloads_match=True))
for p in [B/'verification/audits/priority_author_updates_01/AUTHORED_MANIFEST_SUPPLEMENT_TIMESTAMP_CORRECTION.json',C/'whole_package_adversary_01/AUTHORED_MANIFEST_SUPPLEMENT_REPORT_CORRECTION.json']:
    obj=json.loads(p.read_text());base=p.parent;rows=[obj['original_manifest'],*obj['original_payloads_unchanged'],*obj['supplemental_payloads']]
    for r in rows:
        actual=pin(base/r['path']);assert actual['bytes']==r['bytes'] and actual['sha256']==r['sha256']
    seals.append(dict(manifest=pin(p),payloads=len(rows),all_declared_payloads_match=True))

bad=B/'verification/audits/physical_geometry_adversary_01/FAILED_PROBE_01_COMPLETE.json.gz'
recovery=json.loads((bad.parent/'FAILED_PROBE_RECOVERY.json').read_text());raw=gzip.decompress(bad.read_bytes())
assert len(raw)==72751==recovery['original_uncompressed_bytes']
assert hashlib.sha256(raw).hexdigest()==recovery['original_full_output_sha256']=='b74725bfa1ff239c31f73443898644c6fcf29cc044de4f30edc32c2c75333dbb'

result=dict(utc=datetime.now(timezone.utc).isoformat(),status='PASS',primary_read_in_place=primary,Ferudun_versions=versions,chronology_capture_pins=captures,captured_original_proof_matches=proof_match,actual_server_receipt_checks=len(checks),actual_PR_created_at='2026-10-01T05:48:56Z',checked_seals=seals,failed_physical_output_recovery=dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),lossless=True),limitations='Retained authenticated source and provider observations, not a new worldwide search or proof of historical public visibility/firstness/independent non-derivation. Primary papers and private bodies are read in place and not duplicated. Published KS PDF was not authenticated anew; retained extraction is separately identified.')
(O/'SOURCE_EVIDENCE.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(dict(status='PASS',primary_files=len(primary),versions=len(versions),raw_chronology_captures=len(captures),proof_match_count=len(proof_match),seals=len(seals),lossless_failed_output_bytes=len(raw)),indent=2))
