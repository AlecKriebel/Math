"""Own source refinement only: immutable dated Git rows differ from fresh authority."""
from pathlib import Path
import json,hashlib,difflib,datetime as dt,os
H=Path(__file__).resolve().parent;A=H.parent;OLD=A/'acceptance_preparation_family';p=H/'pr42_guards.py'
raw=p.read_bytes();text=raw.decode();before_sha=hashlib.sha256(raw).hexdigest()
start=text.index('    # Four historical native preimages are read in full, never broadly excluded.')
end=text.index('    verdict=parse(bound(inputs[',start)
new='''    # Exactly four archived native rows use the immutable actual freeze Git
    # bodies, independently of fresh current authority or preflight bytes.
    historical={'draft_pr_publication_program_20260930/inventory.json','unsolved_math_prioritization/QUEUE.md','unsolved_math_prioritization/state.json','unsolved_math_prioritization/history.jsonl'}
    dated_capture=load(A/'root_current_freeze_actual_capture/CAPTURE.json')
    require(dated_capture['main_head_before']==dated_capture['main_head_after']=='c61dc0cb572de281b871264819c8b80d647d0373','Actual immutable historical freeze Git anchor required')
    dated_head=dated_capture['main_head_before']
    dated_native={z['path']:z for z in rows(dated_capture['native13_before'])}
    require(set(dated_native)==NATIVE and len(dated_native)==13 and equal(dated_capture['native13_before'],dated_capture['native13_after']),'Exact historical freeze13 reference rows required')
    foreign=whole['foreign_files_individually_pinned_and_excluded'];require(type(foreign) is list and len(foreign)==925,'Exact925 individually pinned foreign inputs')
    literal_names=set();canonical_names=set();historical_checked=set()
    for z in foreign:
        keyset(z,{'path','bytes','sha256','classification'},'Whole individual foreign reference')
        require(type(z['path']) is str and z['path'] not in literal_names,'Duplicate literal foreign row identity')
        literal_names.add(z['path'])
        canonical=resolve_foreign_literal(z['path'])
        n=canonical.relative_to(R).as_posix();canonical_names.add(n)
        if n in historical:
            captured=dated_native[n]
            require(type(z['bytes']) is int and z['bytes']==captured['bytes'] and z['sha256']==captured['sha256'],'Each historical row must equal its actual freeze13 reference')
            entries=git_bytes('ls-tree','-z',dated_head,'--',n).decode().split('\\0')
            require(len(entries)==2 and entries[-1]=='','Exactly one immutable historical Git blob required')
            fields,literal=entries[0].split('\\t');mode,kind,blob=fields.split()
            require(mode=='100644' and kind=='blob' and literal==n,'Historical Git native body must be the exact regular tracked path')
            raw=git_bytes('show',dated_head+':'+n);historical_checked.add(n)
        else:raw=canonical.read_bytes()
        require(type(z['bytes']) is int and len(raw)==z['bytes'] and sha(raw)==digest(z['sha256']),'Entire individually bound historical/current foreign input differs: '+z['path'])
    require(len(literal_names)==925 and NATIVE<=canonical_names and historical_checked==historical,'Exact925 literal identities, native13 and historical4 required; no omitted row')
'''
text=text[:start]+new+text[end:];p.write_text(text)
info=json.loads((H/'REPAIR_INPUTS.json').read_bytes());info['second_repair_utc']=dt.datetime.now(dt.timezone.utc).isoformat();info['second_repair_author_pid']=os.getpid()
info['second_repair']='Exactly four dated native925 rows are verified from immutable actual Git freeze c61 and full actual freeze13 references, separately from fresh current preflight authority. All other921 rows remain individually live checked.'
info['dated_native_freeze_head']='c61dc0cb572de281b871264819c8b80d647d0373';info['source_before_second_repair_sha256']=before_sha;info['source_after_second_repair_sha256']=hashlib.sha256(text.encode()).hexdigest()
(H/'REPAIR_INPUTS.json').write_text(json.dumps(info,indent=2)+'\n')
delta=''.join(difflib.unified_diff((OLD/'pr42_guards.py').read_text().splitlines(True),text.splitlines(True),fromfile='preserved_V1/pr42_guards.py',tofile='adjacent_V2/pr42_guards.py'))
(H/'SOURCE_REPAIR_DELTA.patch').write_text(delta)
print(json.dumps({'actual_pid':os.getpid(),'status':'SOURCE_ONLY_DATED_NATIVE4_REPAIR_AUTHORED','proposed_sources_imported_compiled_executed':False,'source_before_sha256':before_sha,'source_after_sha256':info['source_after_second_repair_sha256']}))
