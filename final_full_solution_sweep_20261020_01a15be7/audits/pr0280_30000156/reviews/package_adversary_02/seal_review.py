#!/usr/bin/env python3
"""Comprehensive seal of this review's artifact tree; excludes only itself as data."""
from pathlib import Path
import datetime,hashlib,json
BASE=Path(__file__).resolve().parent
MANIFEST=BASE/'AUTHORED_FILE_MANIFEST.json'

def main():
    files=[]
    for p in sorted(BASE.rglob('*')):
        if p==MANIFEST:continue
        if p.is_symlink():raise RuntimeError('Unexpected review symlink: '+str(p))
        if p.is_file():
            name=p.relative_to(BASE).as_posix();data=p.read_bytes()
            if name.startswith(('bound/','archive/','bound_ops/')):role='bound_input_copy'
            elif name.startswith('renders/') or name.startswith('PDF_PAGE_'):role='rendered_reading_evidence'
            else:role='review_authored_code_report_or_result'
            files.append({'path':name,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'role':role})
    value={'schema':1,'sealed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'scope':'Complete assigned expanded review tree: every authored code/report/result, all bound release/archive/operations copies and all six generated page renders. Only this manifest file is excluded; the sealing script itself is included. Full third-party bodies and raw service bodies are not here.',
        'assigned_review_completion_percent':100,'overall_verdict':'REPAIR_REQUIRED_FOR_OPERATIONAL_HELPERS',
        'scientific_five_file_package':'PASS_NO_ADDITIONAL_DEFECT_FOUND','findings':['P280-OPS-01','P280-OPS-02'],'files':files}
    MANIFEST.write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
    for item in files:
        p=BASE/item['path']
        if p.stat().st_size!=item['bytes'] or hashlib.sha256(p.read_bytes()).hexdigest()!=item['sha256']:raise RuntimeError('Seal verification failed')
    print(json.dumps({'files':len(files),'manifest_bytes':MANIFEST.stat().st_size,
        'manifest_sha256':hashlib.sha256(MANIFEST.read_bytes()).hexdigest(),'all_entries_verified':True},indent=2))

if __name__=='__main__':main()
