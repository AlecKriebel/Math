#!/usr/bin/env python3
from pathlib import Path
import datetime,hashlib,json,stat
r=Path(__file__).resolve().parent
utc=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat().replace('+00:00','Z')
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
closed=utc()
log=r/'RESEARCH_LOG.md';log.write_text(log.read_text()+'\n## '+closed+' — 100% of bounded GENERAL-route audit; closure\n\nBounded independent audit complete, including source comparisons, checkable derivations, reproducible exact check, read ledger, full native capture custody, measured source seal and final report. This is100% of this assigned bounded route, not100% of global historical priority. All-period E/M remains no-located-full-prior within this route; even E is old; generic method is old; negative C is a short implication of old primary results. ROOT reserves authentication, independent verification and adjudication. STOP-WRITING after this sealing operation: no more filesystem writes without explicit ROOT reopening.\n')
stop=r/'STOP_WRITING.md';stop.write_text('# Explicit independent closure\n\nClosed UTC: '+closed+'\n\nCompletion estimate:100% of the assigned bounded GENERAL-route audit. Worldwide priority remains unresolved; this does not mark every research/discovery goal complete.\n\nNo other priority report was read before closure. ROOT is responsible for custody authentication, direct decisive-source verification and integrated adjudication. This report authorizes no merge or publication.\n\n**STOP-WRITING:** this agent makes no more filesystem writes after the final seal in this operation unless ROOT explicitly reopens the route. Raw primary PDFs, extracted texts, OCR and source-page renders remain private. No outside individual was contacted; no other chat was messaged; no shared original/snapshot/index/ref was mutated.\n\nSeal coverage excludes only SOURCE_SEAL.json and SOURCE_SEAL.sha256 to avoid self-reference. The separate checksum file seals the manifest; its measured mode/hash are printed in the native completion output. All prior audit artifacts, including this closure and the sealing script, are measured in the manifest.\n')
for p in sorted(r.rglob('*')):
 if p.is_file():p.chmod(0o600)
 elif p.is_dir():p.chmod(0o700)
r.chmod(0o700)
records=[]
for q in sorted((r/'custody').glob('*.json')):
 v=json.loads(q.read_text());records.extend(v if isinstance(v,list) else [v])
for v in records:
 if 'argv' not in v:continue
 assert v['exit_code']==0
 for k in ['stdout','stderr']:
  assert h(Path(v[k+'_file']))==v[k+'_sha256']
 if 'artifact' in v:
  assert h(Path(v['artifact']))==v['sha256']
  assert stat.S_IMODE(Path(v['artifact']).stat().st_mode)==0o600
files=[]
for p in sorted(r.rglob('*')):
 if p.is_file() and p.name not in ['SOURCE_SEAL.json','SOURCE_SEAL.sha256']:
  files.append({'path':str(p.relative_to(r)),'sha256':h(p),'bytes':p.stat().st_size,'mode':oct(stat.S_IMODE(p.stat().st_mode))})
dirs=[{'path':'.','mode':oct(stat.S_IMODE(r.stat().st_mode))}]+[{'path':str(p.relative_to(r)),'mode':oct(stat.S_IMODE(p.stat().st_mode))} for p in sorted(r.rglob('*')) if p.is_dir()]
manifest={'closed_utc':closed,'scope':'Independent bounded GENERAL-route priority audit PR305/problem5100034; no worldwide-firstness or publication authorization','criteria_sha256':h(r/'CRITERIA_FREEZE.md'),'excluded_self_reference':['SOURCE_SEAL.json','SOURCE_SEAL.sha256'],'native_operation_records':sum('argv' in v for v in records),'native_retrieval_records':sum('requested_url' in v for v in records),'distinct_native_source_artifacts':len(set(v['artifact'] for v in records if 'artifact' in v)),'files':files,'directories':dirs}
p=r/'SOURCE_SEAL.json';p.write_text(json.dumps(manifest,indent=2)+'\n');p.chmod(0o600)
q=r/'SOURCE_SEAL.sha256';q.write_text(h(p)+'  SOURCE_SEAL.json\n');q.chmod(0o600)
print(json.dumps({'closed_utc':closed,'files_sealed':len(files),'native_operation_records':manifest['native_operation_records'],'native_retrieval_records':manifest['native_retrieval_records'],'distinct_native_source_artifacts':manifest['distinct_native_source_artifacts'],'directory_modes':dirs,'seal_file':str(p),'seal_sha256':h(p),'seal_mode':oct(stat.S_IMODE(p.stat().st_mode)),'checksum_file':str(q),'checksum_sha256':h(q),'checksum_mode':oct(stat.S_IMODE(q.stat().st_mode)),'report_sha256':h(r/'FULL_PRIORITY_REPORT.md'),'writes_complete':True},indent=2))
