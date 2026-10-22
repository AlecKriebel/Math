#!/usr/bin/env python3
"""Omit a newly selected authored record containing embedded raw command streams."""
import sys
sys.dont_write_bytecode=True
import prepare_terminal as p
def main():
    q=p.T/'selected/ROOT_REPAIR_REVIEW_01.json';old=p.pin(q)
    reason='ROOT repair-adoption record contains embedded raw command stderr streams; retain its exact source locator and hash only. ROOT whole02 adoption is distributed separately. No raw stream redistribution.'
    copies=p.load(p.T/'COPIES.json');copies['entries']=[r for r in copies['entries'] if r['copy_path']!=q.relative_to(p.K).as_posix()];p.write(p.T/'COPIES.json',copies)
    c=p.load(p.T/'CUSTODY.json')
    for row in c['entries']:
        if row.get('copy_path')==q.relative_to(p.K).as_posix():
            row.pop('copy_path');row.update(decision='EXCLUDED',reason=reason)
    p.write(p.T/'CUSTODY.json',c)
    s=p.load(p.T/'STAGE_RESOLUTION.json')
    for row in s['entries']:
        if row['portable_resolution'].get('path')==q.relative_to(p.K).as_posix():
            row['portable_resolution']={'state':'INDIVIDUAL_OMISSION','reason':reason}
    # Compact only this new authored index; its full individual rows remain present.
    p.put(p.T/'STAGE_RESOLUTION.json',(p.json.dumps(s,separators=(',',':'))+'\n').encode())
    q.unlink()
    p.write(p.F/'EVIDENCE_SELECTION_REFINEMENT.json',{'utc':p.datetime.datetime.now(p.datetime.timezone.utc).isoformat(),'status':'OWN_DRAFT_SELECTION_REFINED_BEFORE_HANDOFF','source_locator':'ROOT_REPAIR_REVIEW_01.json',**old,'reason':reason,'original_record_unchanged':True,'earlier_131_command_pass_applies_to_previous_draft_archive_only':True})
if __name__=='__main__':main()
