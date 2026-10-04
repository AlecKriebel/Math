"""Revise authored contract text to completed genuine ROOT schema; no production execution."""
from pathlib import Path
import datetime as dt, json
F=Path(__file__).absolute().parent
def main():
    for n in ['EXECUTION_CONTRACT.md','ROOT_REPRODUCTION_PREREQUISITES.md']:
        p=F/n; t=p.read_text(); t=t.replace('root_original_actual_reproduction/ROOT_REPRODUCTION_RESULT.json','root_original_actual_reproduction/ROOT_CURRENT_REPRODUCTION_SUMMARY.json')
        t=t.replace('The reproduction directory must first close under a self-only manifest','The reproduction directory has now closed under schema pr47-root-original-complete-reproduction-self-only-closure/v1,219+self payload files,46 relative directories,full0444, manifest SHA71109d8643eeff305b9e8200e2e7be0e62e79ad1cc7ad8a22b4456f5a108d278. The builder requires those exact closed bytes and a self-only manifest')
        t=t.replace('Its existing result schema is pr47-root-original-complete-reproduction/v1.','The completed current summary schema is pr47-root-current-complete-reproduction-summary/v1; its entire_reproduction_result retains the byte/type-equivalent underlying pr47-root-original-complete-reproduction/v1 result. The genuine ROOT summary/current audit are substantive evidence with future_acceptance_approvedfalse, not prospective ROOT approvals.')
        t=t.replace('No unfinished ROOT evidence is pinned as closed here.','The closed ROOT219 is fixed in ROOT_FIXED_EVIDENCE.json, including its separate4-member actual closure capture child72331. No unfinished ROOT evidence is pinned as closed.')
        t=t.replace('The builder compares full byte/type equality for every saved result and all helper captures.','The builder compares full byte/type equality for every saved result, all3 helper captures and33 actual Git children. Raw/prior full149266659 bytes and15458 SQL rows retain the complete checks, literalnull and keyABSENT/{} distinction.')
        p.write_text(t)
    with (F/'SOURCE_PREPARATION_RESEARCH_LOG.md').open('a') as h: h.write('\n'+dt.datetime.now(dt.timezone.utc).isoformat()+' — Preparation80%; discovery0%; actual freeze0%. Genuine ROOT219+self/46dirs closure child72331 received and fully byte/mode-inspected by own child79478. Current summary/raw/review schemas pinned honestly; realROOT future acceptance remains false. Production builder/operator authored as text only, with incremental inner/prepublication-prefix chronology and final ROOT read after child exit.\n')
    print(json.dumps({'status':'SOURCE_PRECISION_CONTRACT_UPDATED','ROOT_approval':None,'production_import_compile_or_execution':False}))
if __name__=='__main__': main()
