"""Correct relative closed-ADVERSE links for each current presentation depth."""
import datetime as dt, hashlib, json, os
from pathlib import Path
F=Path(__file__).absolute().parent; ADV=F.parent/'current_source_adversary_family/REPORT.md'
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
    assert __debug__ and F.name=='current_preparation_family_v2'
    changes=[]
    for p in sorted(F.rglob('*.md')):
        if 'original_archive' in p.relative_to(F).parts:continue
        before=p.read_bytes();text=before.decode();needle='[ADVERSE SOURCE report](../current_source_adversary_family/REPORT.md)'
        if needle not in text:continue
        target=os.path.relpath(ADV,p.parent);after=text.replace(needle,'[ADVERSE SOURCE report]('+target+')').encode()
        assert (p.parent/target).resolve()==ADV.resolve() and ADV.is_file()
        if after!=before:
            p.write_bytes(after);changes.append({'path':p.relative_to(F).as_posix(),'before_sha256':sha(before),'after_sha256':sha(after),'resolved_ADVERSE_report':str(ADV)})
    o={'schema':'PR47_SOURCE_V2_CURRENT_ADVERSE_LINK_QUALIFICATION_v1','created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'actual_authoring_pid':os.getpid(),'changes':changes,'production_import_compile_or_execution':False,'future_acceptance_approved':False}
    with (F/'FINAL_LINK_QUALIFICATION.json').open('x') as h:json.dump(o,h,indent=2);h.write('\n');h.flush();os.fsync(h.fileno())
    print(json.dumps({'status':'CURRENT_ADVERSE_RELATIVE_LINKS_RESOLVE','changed_current_presentations':len(changes),'original_archive_changed':False,'production_executed':False}))
if __name__=='__main__':main()
