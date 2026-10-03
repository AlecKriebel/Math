"""Complete SOURCE V2 version qualification; no production execution."""
import datetime as dt, hashlib, json, os
from pathlib import Path
F=Path(__file__).absolute().parent
def need(v,m):
    if not v: raise ValueError(m)
def sha(b): return hashlib.sha256(b).hexdigest()
def main():
    need(__debug__ and F.name=='current_preparation_family_v2','Distinct V2 only')
    changes=[]
    for n in ['CURRENT_QUEUE_PATCH.json','operative_proposal/readiness.json','operative_proposal/review/verdict.json']:
        p=F/n; before=p.read_bytes(); o=json.loads(before)
        o.update(operative_preparation_directory=F.name,source_preparation_version=2,closed_adverse_source_manifest_sha256='ed0aba6a7a42e752012399daed24d460e25108afd7b66c89ee1907473eb76a85',mandatory_SOURCE_V1_null_capture_defect_repaired_in_source_text=True,new_different_clean_SOURCE_adversary='PENDING',production_import_compile_or_execution=False,future_acceptance_approved=False)
        if 'schema' in o: o['schema']=o['schema'].removesuffix('_v1')+'_v2'
        after=(json.dumps(o,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode(); p.write_bytes(after); changes.append({'path':n,'before_bytes':len(before),'before_sha256':sha(before),'after_bytes':len(after),'after_sha256':sha(after)})
    p=F/'prepare_current_packet.py'; before=p.read_bytes(); text=before.decode()
    marker="common={'schema':'PR47_CURRENT_CORRECTED_UNRESOLVED_v1','id':2849"
    need(text.count(marker)==1,'Single generated current metadata marker')
    new="common={'schema':'PR47_CURRENT_CORRECTED_UNRESOLVED_v2','operative_preparation_directory':FAMILY,'source_preparation_version':2,'closed_adverse_source_manifest_sha256':'ed0aba6a7a42e752012399daed24d460e25108afd7b66c89ee1907473eb76a85','old_SOURCE_V1_promoted':False,'id':2849"
    after=text.replace(marker,new).encode(); p.write_bytes(after); changes.append({'path':p.name,'before_bytes':len(before),'before_sha256':sha(before),'after_bytes':len(after),'after_sha256':sha(after)})
    o={'schema':'PR47_SOURCE_V2_FINAL_VERSION_QUALIFICATION_v1','created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'actual_private_authoring_pid':os.getpid(),'exact_changes':changes,'production_import_compile_or_execution':False,'new_different_clean_SOURCE_adversary':'PENDING','future_acceptance_approved':False}
    with (F/'FINAL_VERSION_QUALIFICATION.json').open('x') as h:json.dump(o,h,indent=2,ensure_ascii=False,allow_nan=False);h.write('\n');h.flush();os.fsync(h.fileno())
    with (F/'SOURCE_PREPARATION_RESEARCH_LOG.md').open('a') as h:h.write('\n'+o['created_utc']+' — SOURCE V2 qualifications95%; actual freeze0%; target discovery0%. Current operative/readiness/review/queue proposal and generated metadata explicitly bind version2 and the closed ADVERSE source. Earlier literal authoring and private controls remain dated receipts; final text requires a separately captured final private check. Original1/5,new0,audit0; genuine ROOT prerequisites and new independent reviews pending.\n');h.flush();os.fsync(h.fileno())
    print(json.dumps({'status':'SOURCE_V2_VERSION_QUALIFICATIONS_COMPLETE','builder_sha256':sha(after),'production_executed':False}))
if __name__=='__main__': main()
