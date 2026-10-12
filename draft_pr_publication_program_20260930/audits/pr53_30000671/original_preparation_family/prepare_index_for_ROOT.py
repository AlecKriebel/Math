"""SOURCE preparation freeze: leaves MANIFEST.json absent for ROOT."""
import datetime,hashlib,json,os,pathlib,stat
F=pathlib.Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
    for rel in ['MANIFEST.json','FIXED_PAYLOAD_INDEX.json','READY.json']:assert not (F/rel).exists()
    assert not any(p.is_symlink() for p in [F,*F.parents,*F.rglob('*')])
    for p in F.rglob('*'):
        if p.is_file():os.chmod(p,0o444)
        elif p.is_dir():os.chmod(p,0o755)
        else:raise AssertionError(str(p))
    os.chmod(F,0o755)
    rows=[]
    dirs=['.']
    for p in sorted(F.rglob('*')):
        rel=p.relative_to(F).as_posix()
        if p.is_dir():dirs.append(rel)
        else:
            b=p.read_bytes();rows.append({'path':rel,'bytes':len(b),'sha256':sha(b),'mode':'0444'})
    idx={'schema':'pr53-original-prepared-index/v1','files':rows,'directories':sorted(dirs),'no_native_files_in_payload':True,'private_reference_is_not_publication_content':True}
    ib=(json.dumps(idx,indent=2)+'\n').encode();(F/'FIXED_PAYLOAD_INDEX.json').write_bytes(ib);os.chmod(F/'FIXED_PAYLOAD_INDEX.json',0o444)
    ready={'schema':'pr53-original-source-ready/v1','recorded_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'head':'d49a1bd56d8cc268159331e5ce868e258a32bb58','scope':'original-only source preparation','fixed_index_sha256':sha(ib),'report_sha256':sha((F/'REPORT.md').read_bytes()),'source_qualifications_sha256':sha((F/'SOURCE_PRECISION_QUALIFICATIONS.md').read_bytes()),'prepared_payload_files_including_index_and_ready':len(rows)+2,'prepared_total_bytes_excluding_index_and_ready':sum(x['bytes'] for x in rows),'manifest_absent_at_handoff':True,'root_approval':False,'mathematical_acceptance':False,'original_substantive_attempts':0,'new_proof_attempt_responses':0,'independently_reconstructed_counterexample':False,'full_2008_article_read':False,'required_operative_precision_repairs':['absent raw prior report key; non-NULL SQL text {}','PR body must mention final QUEUE.md change'],'future_root_closure':'/usr/bin/python3 -B close_for_ROOT.py','future_separate_readback':'/usr/bin/python3 -B verify_closed_readonly.py ACTUAL_MANIFEST_SHA256'}
    (F/'READY.json').write_text(json.dumps(ready,indent=2)+'\n');os.chmod(F/'READY.json',0o444)
    from closed_scope_common import verify_prepared
    _,_,count=verify_prepared(False)
    print(json.dumps({'status':'SOURCE_READY_UNCLOSED','payload_files':len(rows)+2,'payload_bytes_excluding_index_ready':sum(x['bytes'] for x in rows),'actual_complete_capture_objects':count,'manifest_absent':not (F/'MANIFEST.json').exists(),'root_approval':False,'fixed_index_sha256':sha(ib)}))
if __name__=='__main__':main()
