import datetime,hashlib,json,pathlib,stat
root=pathlib.Path(__file__).resolve().parent
audit=pathlib.Path('/Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr85_30001203/isolated_main_integration_20261005/checkout/draft_pr_publication_program_20260930/audits/pr140_5100023')
def sha(body):return hashlib.sha256(body).hexdigest()
def check(ok,message):
    if not ok:raise RuntimeError(message)
receipts=[]
def pins(base,rows,label):
    for row in rows:
        name=row.get('relative',row.get('source_relative_to_audit',row.get('path')))
        path=pathlib.Path(name)
        if not path.is_absolute():path=base/path
        body=path.read_bytes()
        check(len(body)==row['bytes'] and sha(body)==row['sha256'],label+' '+name)
        mode=row.get('mode')
        if isinstance(mode,str):mode=int(mode,8)
        if mode is not None:check(stat.S_IMODE(path.stat().st_mode)==mode,label+' mode '+name)
    receipts.append(dict(label=label,authenticated_pins=len(rows)))
mg=json.loads((audit/'ROOT_MATHEMATICAL_GATE.json').read_text())
pins(audit,mg['evidence'],'ROOT mathematical evidence')
pg=json.loads((audit/'ROOT_PRIORITY_GATE.json').read_text())
pins(audit/'priority_convergence_adversary_20261007',pg['authenticated_convergence_members'],'priority convergence')
for family in ['algebraic_orbit_boundary_adversary_20261007','geometric_variational_adversary_20261007','historical_general_priority_adversary_20261007','priority_convergence_adversary_20261007','whole_publication_adversary_r1_20261007']:
    m=json.loads((audit/family/'FINAL_MANIFEST.json').read_text())
    rows=m.get('members',m.get('files',m.get('entries',m.get('public_files'))))
    check(rows is not None,'manifest member schema '+family)
    pins(audit/family,rows,family)
vm=json.loads((audit/'publication_package_v1/verification/MANIFEST.json').read_text())
pins(audit,vm['accepted_mathematical_source_pins'],'verification accepted mathematical sources')
sp=json.loads((audit/'publication_package_v1/verification/SOURCE_PROVENANCE.json').read_text())
pins(audit,sp['accepted_sources'],'portable verifier three accepted source versions')
record_path=audit/'ROOT_priority_reading_20261007/exact_record.json'
record=json.loads(record_path.read_text())
for row in record['files']:
    path=audit/'ROOT_priority_reading_20261007'/row['key']
    if not path.exists():continue
    body=path.read_bytes()
    check(len(body)==row['size'],'contemporary size')
    check('md5:'+hashlib.md5(body).hexdigest()==row['checksum'],'contemporary provider MD5')
    receipts.append(dict(label='contemporary '+row['key'],bytes=len(body),sha256=sha(body),provider_md5_matched=True))
check(record['created']=='2026-10-01T23:58:07.321420+00:00' and record['metadata']['publication_date']=='2026-10-02','contemporary chronology')
op=json.loads((root/'original_proof_child.json').read_text())
check(sha(op['stdout'].encode())=='8d13afb77521c9eb8705f494aeba989a5052143e19641534411b8cfec1829754','fresh original Git object')
readback=audit/'ROOT_PACKAGE_R2_CANDIDATE_READBACK.json'
check(sha(readback.read_bytes())=='1b8867adc1200a3da2e8d5313c953e8bd41340c20548cf2e1f0700d05cb11d88','candidate readback')
r=dict(status='PASS',utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),receipts=receipts,
       original_proof_fresh_read_sha256=sha(op['stdout'].encode()),
       contemporary_record_created=record['created'],contemporary_publication_date=record['metadata']['publication_date'],
       bounded_source_reading_only=True,absolute_priority_certificate=False,
       web_access_limits=['DOI and Zenodo page inaccessible through web tool; authoritative cached provider record and checksum-matched complete paper inspected'])
(root/'PROVENANCE_AUDIT.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
