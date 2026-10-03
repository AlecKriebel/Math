#!/usr/bin/env python3
"""Consolidate byte-identical large tree streams in completed successful runs.

All stream paths and bytes are retained through hard links. Failed-run directories,
primary sources, public files and active outputs are never touched. Future gate
runs must use fresh OWN directories, as required by the sealed README.
"""
import datetime,hashlib,json,os,pathlib
ROOT=pathlib.Path(__file__).parents[2]
HERE=pathlib.Path(__file__).parent
SUCCESS_ROOTS=['private/final_gate','private/live_acceptance/historical_refresh_assessment',
               'private/live_acceptance/round2_prepared']
def main():
    canonical={};changes=[];saved=0;already_shared=[];skipped_non_git=0
    for name in SUCCESS_ROOTS:
        for p in sorted((ROOT/name).rglob('*.stdout')):
            if p.stat().st_size < 1024*1024:continue
            data=p.read_bytes()
            # Complete ls-tree streams start with Git mode/kind metadata and are NUL-separated.
            if not data.startswith((b'100644 blob ',b'100755 blob ',b'120000 blob ')) or b'\0' not in data:
                skipped_non_git+=1;continue
            digest=hashlib.sha256(data).hexdigest();key=(len(data),digest)
            if key not in canonical:canonical[key]=p;continue
            original=canonical[key]
            assert original.read_bytes()==data
            if p.stat().st_ino==original.stat().st_ino:
                already_shared.append({'path':p.relative_to(ROOT).as_posix(),'canonical_path':original.relative_to(ROOT).as_posix(),'bytes':len(data),'sha256':digest});continue
            temporary=p.with_name(p.name+'.deduplicate_tmp');assert not temporary.exists()
            os.link(original,temporary);temporary.replace(p)
            assert p.read_bytes()==data and p.stat().st_ino==original.stat().st_ino
            changes.append({'path':p.relative_to(ROOT).as_posix(),'canonical_path':original.relative_to(ROOT).as_posix(),
                            'bytes':len(data),'sha256':digest,'full_bytes_and_path_preserved':True})
            saved+=len(data)
    receipt={'recorded_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
             'approved_completed_success_roots':SUCCESS_ROOTS,'duplicates_consolidated':len(changes),
             'duplicated_bytes_consolidated':saved,'changes':changes,'failed_streams_touched':0,
             'primary_source_files_touched':0,'sealed_public_files_touched':0,'stream_bytes_removed':0,
             'all_original_private_stream_paths_retained':True}
    receipt['already_shared_identical_pairs']=already_shared
    receipt['skipped_non_git_streams_untouched']=skipped_non_git
    (HERE/'storage_cleanup_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    stream=json.dumps({k:receipt[k] for k in ['duplicates_consolidated','duplicated_bytes_consolidated','stream_bytes_removed','failed_streams_touched']},sort_keys=True)+'\n'
    (HERE/'storage_cleanup.stdout').write_text(stream);(HERE/'storage_cleanup.stderr').write_bytes(b'')
    print(stream,end='')
if __name__=='__main__':main()
