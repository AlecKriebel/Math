"""Advance local bookkeeping after the verified native row170 transition."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
sha = lambda b: hashlib.sha256(b).hexdigest()
progress = P / 'PROGRESS.json'
assert sha(progress.read_bytes()) == 'b494638fe5212cb5ff891ba84a350736dbb3c4d1b2d8934f6c30cf6b94360b63'
receipt_rel = 'verification/sheet-pentagon-pass145-20261117/FINAL_READBACK.json'
raw = (P / receipt_rel).read_bytes()
receipt = json.loads(raw)
assert receipt['status'] == 'NATIVE_TRACKER_PASS145_READBACK_VERIFIED'
assert receipt['reviewed_or_deferred'] == 145 and receipt['untargeted_whole_cells_exact'] == 252
adoption = P / 'verification/root-checkpoint-bbfb-adoption-20261117.json'
assert sha(adoption.read_bytes()) == '03dfe6887e354d396936581f9c507aee392f9890cd964a237410fd9a52365285'
old_queue_rel = 'reconciliation/current-native-queue-20261117-pass144-d4.json'
q = json.loads((P / old_queue_rel).read_bytes())
rows = [r for r in q['queue'] if r['current_native_sheet_row'] == 170]
assert len(rows) == 1 and rows[0]['record_id'] == 23137834 and rows[0]['native_status'] == 'In review — full manuscript'
rows[0]['native_status'] = 'Reviewed — preparing page'
now = datetime.now(timezone.utc).isoformat()
q.update(UTC=now, inherited_native_identity_snapshot=old_queue_rel,
         source_native_cell_snapshots='verification/sheet-pentagon-pass145-20261117',
         source_latest_native_status_snapshot='verification/sheet-pentagon-pass145-20261117/AFTER_CELLS.packed.json',
         source_final_native_readback=receipt_rel,
         latest_fresh_native_identity_range='Full List!W170:AD170',
         new_fresh_identity_check='W170:AD170 confirms23137834; all247 status cells read with coordinates; whole203identity reconciliation inherited, not freshly repeated',
         all203_identities_freshly_read_this_step=False,
         note='Onlypentagonrow170 advanced topreparing.145reviewed137PASS8defer58remain. Native123verified10deployed4preparing6inreview50queued2holds8defer. Priorqueue preserved; exactnativepacked snapshots/metadatareadback retained.')
queue_rel = 'reconciliation/current-native-queue-20261117-pass145-pentagon.json'
with (P / queue_rel).open('x') as f:
    f.write(json.dumps(q, indent=2, ensure_ascii=False) + '\n')
d = json.loads(progress.read_bytes())
for key in ('in_review_record_ids', 'reviews_complete_awaiting_root_disposition_record_ids'):
    d[key] = [x for x in d[key] if str(x) != '23137834']
if '23137834' not in d['editorial_preparing_or_awaiting_root_record_ids']:
    d['editorial_preparing_or_awaiting_root_record_ids'].append('23137834')
d.update(updated_utc=now, pending_other_eligible_works=58, reviewed_or_deferred_percent=145/203*100,
         root_cleared_preparation_count=4, full_goal_partition=receipt['full_column_status_counts'],
         local_scientific_dispositions_pending_tracker=[], current_native_queue=queue_rel,
         sheet_status_receipt=receipt_rel, native_tracker_latest_readback=receipt_rel,
         latest_math_checkpoint='bbfb7abf5c56e3f8d090e125784ff357138076fb',
         last_scoped_Math_checkpoint='bbfb7abf5c56e3f8d090e125784ff357138076fb',
         latest_math_checkpoint_root_adoption='verification/root-checkpoint-bbfb-adoption-20261117.json',
         latest_math_checkpoint_root_adoption_SHA256=sha(adoption.read_bytes()),
         note='Nativeandscientific145/203:137PASS8defer58remain (71.428571%).123verified+10deployed-awaitingactualdisplay+4preparing+6inreview+50queued+2holds+8defer. PentagonfulloriginalPASSrootreviewcheckpointedbbfb; nativeAB170/AD170readbackverified; AAblank/ACwholepreserved. Programmeactive/incomplete.')
d['root170_full_scientific_disposition']['native_transition_pending'] = False
d['native_sheet_review145_final'] = {'path': receipt_rel, 'bytes': len(raw), 'SHA256': sha(raw),
    'reviewed_or_deferred':145, 'passes':137, 'deferred':8, 'remaining':58, 'record':23137834,
    'AA_blank':True, 'native_version_cell_preserved':True, 'native_readback_verified':True}
progress.write_text(json.dumps(d, indent=2, ensure_ascii=False) + '\n')
with (P / 'RESEARCH_LOG.md').open('a') as f:
    f.write('\n\n'+now+' — Pentagon full-original PASS145 checkpoint bbfb7abf independently read/adopted: all56packetfiles individualmodes/bytes exact,64closures175keys,224programme-only paths,159remote siblings/docs and nativeM/W/public803/387 exact; one dry/push0, sixguard/auditruns0. Native row170 AB/AD only advanced to preparing:252untargetedwholecells and2targetnonvaluefields/all8metadata exact, AC whole and AAblank/alloldAD retained. Native/scientific145of203=71.428571%,137PASS8defer58remain. Public123verified10displaypending4preparing; goalactive/incomplete. Queue145 carries onlyfresh170identity/all247statuses, other203identity evidence inherited.\n')
print(json.dumps({'status':'LOCAL_BOOKKEEPING_MATCHES_NATIVE145','progress_SHA256':sha(progress.read_bytes()),'queue':queue_rel,'queue_SHA256':sha((P/queue_rel).read_bytes()),'native_final_bytes':len(raw),'native_final_SHA256':sha(raw)}))
