#!/usr/bin/env python3
"""Read-only independent archive, manifest, reference and provenance audit."""
from pathlib import Path, PurePosixPath
import hashlib, json, zipfile, re, datetime, argparse
_HERE=Path(__file__).resolve()
_CANDIDATES=[_HERE.parents[2]/'publication', *_HERE.parents]
BASE=next((p for p in _CANDIDATES if (p/'run_checks.py').is_file() and (p/'PACKAGE_MANIFEST.json').is_file()), None)
if BASE is None: raise RuntimeError('Cannot locate the publication package')

def digest(data): return hashlib.sha256(data).hexdigest()
def demand(ok,msg):
    if not ok: raise RuntimeError(msg)
def pinned(path,row):
    data=path.read_bytes(); demand(digest(data)==row['sha256'],'hash '+str(path));
    size=row.get('bytes',row.get('size'))
    if size is not None:demand(len(data)==size,'size '+str(path))
    return {'path':str(path.relative_to(BASE)),'sha256':digest(data),'bytes':len(data)}
def main():
    archive=BASE/'full_stress_stratifications_source_verification_v1.zip'
    manifest=json.loads((BASE/'PACKAGE_MANIFEST.json').read_text())
    entries=manifest['files']; paths=[r['path'] for r in entries]
    demand(len(paths)==len(set(paths)),'manifest duplicates')
    inventory=[pinned(BASE/r['path'],r) for r in entries]
    with zipfile.ZipFile(archive) as z:
        names=z.namelist();demand(len(names)==len(set(names)),'archive duplicates')
        demand(z.testzip() is None,'archive CRC')
        prefix='full_stress_stratifications_v1/'
        for name in names:
            p=PurePosixPath(name);demand(name.startswith(prefix) and not p.is_absolute() and '..' not in p.parts,'unsafe name')
        expected={prefix+p for p in paths}|{prefix+'PACKAGE_MANIFEST.json'}
        demand(set(names)==expected,'archive inventory')
        for name in names:demand(z.read(name)==(BASE/name[len(prefix):]).read_bytes(),'archive byte identity '+name)
        archive_receipt={'entries':len(names),'sha256':digest(archive.read_bytes()),'all_entry_bytes_equal_local':True,'crc_pass':True,'exact_manifest_inventory':True}
    historical=[];omitted=[]
    for label in ('package_review_01','package_review_02'):
        folder=BASE/'evidence'/label
        rows=json.loads((folder/'REVIEW_OUTPUT_MANIFEST.json').read_text())['files']
        for row in rows:
            p=folder/row['name']
            if p.exists():historical.append(pinned(p,row))
            else:omitted.append({'stage':label,'name':row['name'],'role':'historical stage output, not claimed included by current archive manifest'})
    original=json.loads((BASE/'evidence/SUBMITTED_PINS.json').read_text())
    demand(original['head_commit']=='f333d06cc161b1b8ae8422bf413ed1ffae31e614','submitted commit identity')
    for row in original['files']:
        name=row['relative'];p=None
        if name in ('REPORT.md','ACCEPTANCE.md','STATUS.json'):p=BASE/'evidence/submitted'/name
        elif name in ('check_collision_witness.py','independent_kernel_check.py'):p=BASE/'checks'/name
        elif name.endswith('.reference.stdout') or name.endswith('.reference.stderr'):
            trial=BASE/'evidence/original_reference'/name
            if trial.exists():p=trial
        if p is not None:historical.append(pinned(p,row))
    math=json.loads((BASE/'evidence/INDEPENDENT_MATHEMATICAL_INPUT_PINS.json').read_text())
    math_map={'REVIEW.md':'evidence/INDEPENDENT_MATHEMATICAL_REVIEW.md','VERDICT.json':'evidence/INDEPENDENT_MATHEMATICAL_VERDICT.json','independent_exact_check.py':'checks/independent_exact_check.py','exact_check.stdout.json':'expected/independent_exact_check.json'}
    for row in math['files']:
        if row['name'] in math_map:historical.append(pinned(BASE/math_map[row['name']],row))
    priority=json.loads((BASE/'evidence/PRIORITY_REVIEW_PINS.json').read_text())
    priority_map={'REVIEW.md':'PRIORITY_AUDIT.md','VERDICT.json':'PRIORITY_VERDICT.json','QUERY_LOG.md':'PRIORITY_QUERY_LOG.md','SOURCE_AUDIT.json':'PRIORITY_SOURCE_AUDIT.json'}
    for row in priority['files']:
        name=PurePosixPath(row['path']).name
        if name in priority_map:historical.append(pinned(BASE/'evidence'/priority_map[name],row))
    nav=[]
    for file in ('README.md','SUPPLEMENT.md','evidence/README.md'):
        text=(BASE/file).read_text()
        for _,url in re.findall(r'\[([^\]]*)\]\(([^)]+)\)',text):
            if url.startswith(('https:','http:','#')):continue
            p=(BASE/file).parent/url.split('#')[0]
            demand(p.exists(),'navigation '+file+' '+url);nav.append({'from':file,'to':url})
    meta=json.loads((BASE/'metadata.json').read_text());deposit=json.loads((BASE/'zenodo-deposit.json').read_text())
    demand(meta==deposit['metadata'],'metadata API identity')
    for f in deposit['files']:demand((BASE/f['path']).is_file(),'deposit upload path')
    demand(meta['publication_type']=='preprint' and meta['creators'][0]['orcid']=='0009-0001-9320-500X','metadata type/author')
    env=json.loads((BASE/'evidence/EXECUTION_ENVIRONMENT.json').read_text());demand(env['recorded_execution_system']=='Darwin','recorded macOS identity')
    return {'status':'PASS','timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'archive':archive_receipt,'manifest_files':len(entries),'historical_counterpart_hashes_checked':len(historical),'historical_counterparts':historical,'historical_outputs_omitted_as_disclosed':omitted,'portable_relative_links_checked':len(nav),'links':nav,'metadata_identical':True,'deposit_inputs_exist':True,'recorded_environment':env,'inventory':inventory,'limits':'Verifies included byte identities and declared provenance mappings; omitted third-party source bodies or historical permissions are not recreated.'}
if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path);args=parser.parse_args()
    result=main()
    if args.output: args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('inventory','historical_counterparts','links')},indent=2))
