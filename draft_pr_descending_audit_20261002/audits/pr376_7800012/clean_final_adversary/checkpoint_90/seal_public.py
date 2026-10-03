"""Bounded owned-report/code/stream allowlist; private inputs are always excluded."""
import pathlib,json,hashlib,datetime
R=pathlib.Path(__file__).parent
names=['BASELINE_SEALED.md','BASELINE_SEALED.sha256','MATHEMATICAL_VERDICT_SEALED.md','MATHEMATICAL_VERDICT_SEALED.sha256','POST_SEAL_CORROBORATION.md','RESEARCH_LOG.md','REPRODUCTION.md','AUDIT_GATE.json','PROVENANCE_CERTIFICATE.json','FULL_HESSIAN.json','FULL_FOURIER_BLOCKS.json','independent_hessian.py','independent_universal.py','independent_boundary.py','provenance.py','seal_public.py']
names+=sorted(str(p.relative_to(R)) for p in (R/'streams').iterdir() if p.is_file() and p.suffix in ['.stdout','.stderr'])
entries=[]
for name in names:
 assert not name.startswith(('tmp/','private_')) and '..' not in pathlib.PurePosixPath(name).parts
 p=R/name;assert p.is_file() and not p.is_symlink();b=p.read_bytes()
 entries.append(dict(path=name,bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),kind='full_stream' if name.startswith('streams/') else 'owned_audit_code' if name.endswith('.py') else 'owned_audit_report_or_certificate'))
gate=json.loads((R/'AUDIT_GATE.json').read_text())
obj=dict(problem_id=7800012,pr=376,at=datetime.datetime.now(datetime.timezone.utc).isoformat(),audit_completion_percent=gate['audit_completion_percent'],mathematical_verdict=gate['mathematical_verdict'],publication_status=gate['publication_status'],bounded_allowlist=True,excluded=['PUBLIC_MANIFEST.json itself (no circular hash)','all tmp/ private candidate inputs','all primary downloads/raw/extracts/renders','all root/sibling audit artifacts'],files=entries)
(R/'PUBLIC_MANIFEST.json').write_text(json.dumps(obj,indent=2)+'\n')
print(json.dumps(dict(status='PASS_BOUNDED_ALLOWLIST',files=len(entries),percent=obj['audit_completion_percent'],publication_status=obj['publication_status'])))
