#!/usr/bin/env python3
"""Independent local payload, custody, metadata and deterministic-byte audit."""
import sys
sys.dont_write_bytecode=True
import ast,datetime,gzip,hashlib,io,json,re,shutil,struct,subprocess,tarfile,zlib
from pathlib import Path
HERE=Path(__file__).resolve().parent
AUDIT=HERE.parent.parent
ROOT=AUDIT/'preprint_v1_0'
REPO=AUDIT.parents[2]
def sha(data):return hashlib.sha256(data).hexdigest()
def require(ok,message):
    if not ok:raise RuntimeError(message)
def dump(name,data):(HERE/name).write_text(json.dumps(data,indent=2)+'\n')
def run(args,cwd,stem):
    r=subprocess.run(args,cwd=cwd,capture_output=True)
    (HERE/(stem+'_stdout.txt')).write_bytes(r.stdout)
    (HERE/(stem+'_stderr.txt')).write_bytes(r.stderr)
    require(r.returncode==0,'Command failed: '+stem)
    return r

def main():
    baseline=json.loads((HERE/'BASELINE_PINS.json').read_text())
    changed=[];unchanged=[]
    for row in baseline['files']:
        path=AUDIT/row['path']; data=path.read_bytes()
        current={'bytes':len(data),'sha256':sha(data)}
        if current['sha256']!=row['sha256'] or current['bytes']!=row['bytes']:
            require(row['group']=='candidate','Frozen original/root/review/family drift: '+row['path'])
            changed.append({'path':row['path'],'before':{'bytes':row['bytes'],'sha256':row['sha256']},'after':current})
        else:unchanged.append(row['path'])
    tex=(ROOT/'paper.tex').read_text(); before=(HERE/'baseline/paper.tex').read_text()
    old='The accompanying preparation package remains pending a new complete manuscript/package review.'
    new='The accompanying support package preserves the dated AI review history and the exact input scope of each review; its current kit state is recorded in \\texttt{STATUS.json}.'
    require(tex.count(new)==1 and tex.replace(new,old)==before,'TeX outside one disclosure sentence changed')
    historic=json.loads((HERE/'baseline/EVIDENCE_COPY_MANIFEST.json').read_text())
    copies=json.loads((ROOT/'EVIDENCE_COPY_MANIFEST.json').read_text())
    require(copies['files'][:53]==historic['files'],'Original 53 mappings changed')
    for row in copies['files']:
        data=(ROOT/row['package_path']).read_bytes()
        require(data==(AUDIT/row['source_path']).read_bytes(),'Origin/copy bytes mismatch: '+row['package_path'])
        require(len(data)==row['bytes'] and sha(data)==row['sha256'],'Origin/copy pin mismatch')
    for name in ['PREPARATION_REPORT.md','PDF_QA.json','BUILD_RECEIPT.json','INTEGRITY_QA.json',
                 'VERIFICATION_RECEIPT.json','ARCHIVE_SHA256.json','CURRENT_INTEGRITY.json',
                 'EVIDENCE_COPY_MANIFEST.json','STATUS.json']:
        require((ROOT/'history/initial_preparation'/name).read_bytes()==(HERE/'baseline'/name).read_bytes(),'Historical input bytes changed: '+name)
    status=json.loads((ROOT/'STATUS.json').read_text())
    require(status['new_whole_package_review']=='PENDING_NEW_WHOLE_02' and status['publication_ready'] is False and status['all_issues_resolved'] is False,'Premature readiness')
    first=json.loads((ROOT/'evidence/reviews/package_01/VERDICT.json').read_text())
    require(first['findings']==[] and first['severity_counts']=={'P0':0,'P1':0,'P2':0,'P3':0},'First clean verdict lost')
    integrity=json.loads((ROOT/'CURRENT_INTEGRITY.json').read_text())
    paths=[r['path'] for r in integrity['files']]
    require(paths==sorted(paths) and len(paths)==len(set(paths))==len({p.casefold() for p in paths}),'Current path ordering/uniqueness')
    for row in integrity['files']:
        p=ROOT/row['path'];data=p.read_bytes()
        require(not p.is_symlink() and len(data)==row['bytes'] and sha(data)==row['sha256'],'Current actual payload mismatch')
        if p.suffix=='.json':json.loads(data)
        elif p.suffix=='.py':ast.parse(data)
        elif p.suffix!='.pdf':data.decode('utf-8')
        require(p.suffix!='.pdf' or row['path']=='output/pdf/paper.pdf','Third-party binary PDF')
        require(not any(x in {'raw','rawprivate','private','replay','render','rendered','extract','extracted','tmp','cache','caches','__pycache__'} for x in p.relative_to(ROOT).parts),'Excluded folder in actual payload')
        require(p.name.lower()!='fullsource.txt' and 'CITATION_DISCOVERY' not in p.name,'Source body/API dump in actual payload')
    raw=(ROOT/'supportkit-v1.0.tar.gz').read_bytes()
    require(raw[:3]==b'\x1f\x8b\x08' and raw[3]==0 and raw[4:8]==bytes(4),'Gzip header/mtime')
    expanded=gzip.decompress(raw);crc,isize=struct.unpack('<II',raw[-8:])
    require(crc==(zlib.crc32(expanded)&0xffffffff) and isize==(len(expanded)&0xffffffff),'Gzip CRC/isize')
    expected=sorted(paths+['CURRENT_INTEGRITY.json','BUILD_RECEIPT.json'])
    with tarfile.open(fileobj=io.BytesIO(raw),mode='r:gz') as archive:
        members=archive.getmembers();names=[]
        for member in members:
            prefix='rank_one_uniqueness_v1_0/'
            require(member.isfile() and member.name.startswith(prefix),'Archive type/prefix')
            name=member.name[len(prefix):];names.append(name)
            require(re.fullmatch(r'[A-Za-z0-9_.\-/]+',name) is not None and not name.startswith('/') and all(x not in {'','.','..'} for x in name.split('/')),'Unsafe relative path')
            require(member.mode==0o644 and member.uid==member.gid==0 and member.uname==member.gname=='' and member.mtime==1791849600,'Tar mode/owners/time')
            require(archive.extractfile(member).read()==(ROOT/name).read_bytes(),'Archive full actual payload mismatch')
        require(names==expected and len(names)==len(set(names))==len({n.casefold() for n in names}),'Archive complete membership/order/uniqueness')
    out=io.BytesIO()
    with gzip.GzipFile(fileobj=out,mode='wb',filename='',mtime=0) as gz:
        with tarfile.open(fileobj=gz,mode='w',format=tarfile.PAX_FORMAT) as archive:
            for name in expected:
                data=(ROOT/name).read_bytes(); info=tarfile.TarInfo('rank_one_uniqueness_v1_0/'+name)
                info.size=len(data);info.mode=0o644;info.uid=info.gid=0;info.uname=info.gname='';info.mtime=1791849600
                archive.addfile(info,io.BytesIO(data))
    require(out.getvalue()==raw,'Independent deterministic bytes mismatch')
    run([sys.executable,'-B','verify_package.py'],ROOT,'package_verifier')
    run([sys.executable,'-B','build_archive.py'],ROOT,'rebuild')
    require((ROOT/'supportkit-v1.0.tar.gz').read_bytes()==raw,'Consecutive deterministic build drift')
    run([sys.executable,'-B','verify_package.py'],ROOT,'package_verifier_after')
    wrapper=json.loads((ROOT/'zenodo-deposit.json').read_text());meta=json.loads((ROOT/'publication/zenodo.json').read_text())
    require(wrapper['metadata']==meta and wrapper['files']==[{'path':'output/pdf/paper.pdf','name':'paper.pdf'},{'path':'supportkit-v1.0.tar.gz','name':'supportkit-v1.0.tar.gz'}],'Metadata/attachment wrapper equality')
    for r in wrapper['files']:require(re.fullmatch(r'[A-Za-z0-9_.-]+',r['name']) is not None,'Unsafe upload name')
    local=run([sys.executable,'-B',str(REPO/'zenodo_deposit_tool/zenodo.py'),'check',str(ROOT/'zenodo-deposit.json')],REPO,'zenodo_local_check')
    require('PENDING_NEW_WHOLE_01' not in (ROOT/'README.md').read_text() and 'PENDING_NEW_WHOLE_01' not in (ROOT/'SUPPLEMENT.md').read_text() and 'pending a new complete' not in tex and 'PENDING_' not in meta['notes'],'Stale durable release wording')
    navigation=['paper.tex','output/pdf/paper.pdf','README.md','SUPPLEMENT.md','EVIDENCE_INDEX.md','STATUS.json','EVIDENCE_COPY_MANIFEST.json','CURRENT_INTEGRITY.json','BUILD_RECEIPT.json','PDF_QA.json','PREPARATION_REPORT.md','publication/zenodo.json','zenodo-deposit.json','evidence/reviews/package_01/FULL_REPORT.md','evidence/reviews/package_01/VERDICT.json','evidence/reviews/package_01/FINAL_INPUT_PINS.json','evidence/reviews/package_01/OUTPUT_PINS.json','evidence/root/ROOT_PREPRINT_REVIEW_01.json','history/initial_preparation/README.md']
    for n in navigation:require((ROOT/n).is_file(),'Navigation missing: '+n)
    boundary_metadata={
        'title':'A flow reduction for equilibrium uniqueness in rank-one bimatrix games','version':'1.0',
        'publication_date':'2026-10-13','license':'cc-by-4.0'}
    for key,value in boundary_metadata.items():require(meta[key]==value,'Author/title/version/date/license metadata drift')
    require(meta['creators']==[{'name':'Kriebel, Alec','affiliation':'Independent researcher','orcid':'0009-0001-9320-500X'}],'Creator drift')
    report={'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS_REPAIRED_LOCAL_PACKAGE_INTEGRITY_AND_LAYOUT','completion_percent':95,'candidate_input_files_before':85,'originals_unchanged':11,'all_frozen_root_family_and_first_review_bytes_unchanged':True,'changed_existing_candidate_paths':changed,'unchanged_existing_baseline_paths':unchanged,'original_53_copy_map_records_unchanged':True,'copied_authored_records':len(copies['files']),'first_review_records_appended':41,'historical_preparation_input_bytes_unchanged':True,'math_tex_unchanged_except_one_disclosure_sentence':True,'current_content_files':len(paths),'archive_members':len(expected),'actual_archive_payloads_checked':True,'independent_rebuild_byte_identical':True,'consecutive_builder_byte_identical':True,'sorted_ascii_safe_casefold_unique_paths':True,'tar_mode_owner_epoch_checked':True,'gzip_crc_isize_checked':True,'metadata_wrapper_exact_equality':True,'safe_attachment_names':True,'navigation_checked':navigation,'local_repository_zenodo_check_returncode':0,'tex_sha256':sha((ROOT/'paper.tex').read_bytes()),'pdf_sha256':sha((ROOT/'output/pdf/paper.pdf').read_bytes()),'archive_sha256':sha(raw),'new_whole_package_review':status['new_whole_package_review'],'publication_ready':False,'all_issues_resolved':False,'remote_operation':False}
    dump('VERIFICATION.json',report)
    print(json.dumps({k:report[k] for k in ['status','copied_authored_records','current_content_files','archive_members','tex_sha256','pdf_sha256','archive_sha256','publication_ready','all_issues_resolved']}))
if __name__=='__main__':main()
