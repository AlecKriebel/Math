from pathlib import Path
import datetime,json
R=Path(__file__).resolve().parent
base=(R/'streams/entire_literal_base_queue.stdout').read_bytes()
actual=(R/'streams/actual_blob_0.stdout').read_bytes()
old=base.splitlines(keepends=True);new=actual.splitlines(keepends=True)
assert len(old)==len(new)==1966
assert b'2303016 / AMR-022-3016' in old[405] and b'2303016 / AMR-022-3016' in new[405]
expected=old[405].replace(b'| queued | 0/5 |',b'| already_solved | 1/5 |')
assert expected==new[405] and base.replace(old[405],expected,1)==actual
bad_lines=list(new);bad_lines[405]=new[405].replace(b'| already_solved | 1/5 |',b'| already_solved | 2/5 |')
bad=b''.join(bad_lines)
assert bad!=actual and [i+1 for i,(a,b) in enumerate(zip(new,bad_lines)) if a!=b]==[406]
rejected=False
try:
    assert base.replace(old[405],expected,1)==bad
except AssertionError:
    rejected=True
assert rejected
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS exact target-row negative rejected','changed_physical_line':406,'changed_pipe_cell':9,'rejected_wrong_target_turn':rejected,'original_negative_label_clarification':'The original driver control named wrong target queue turn cell replaces the first globally matching status/turn pattern, which is row26, so it actually rejects an unrelated-row turn alteration. That intact execution remains a valid whole-queue preservation negative; this additional check explicitly changes only target line406 cell9.'}
(R/'QUEUE_NEGATIVE_CLARIFICATION.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
