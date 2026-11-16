"""CC BY 4.0, Alec Kriebel 2026. Explicit own-packet closure only.
Default only reads/reports. --seal requires two exact precreated empty controls.
Rejects every frozen packet. Does not invoke scientific code or any old helper.
"""
from pathlib import Path
import sys
import json
from datetime import datetime, timezone
sys.dont_write_bytecode=True
OWN=Path(__file__).resolve().parent
final=OWN/'FINAL.json'
if final.exists() and final.read_bytes()!=b'{}\n':
    raise ValueError('Frozen packet: sealer may not execute')
args=sys.argv[1:]
if not args:
    print(json.dumps({'status':'READ_ONLY_SEAL_GUARD','writes':0,'explicit_seal_required':True},separators=(',',':')))
elif args!=['--seal']:
    raise ValueError('Only explicit --seal is accepted')
else:
    from check_editorial import audit, inventory, file_pin, require, TERMINALS
    for name in TERMINALS:
        require((OWN/name).is_file() and not (OWN/name).is_symlink() and (OWN/name).read_bytes()==b'{}\n','exact already-created ordinary empty control required')
    result=audit(closing=True)
    now=datetime.now(timezone.utc).isoformat()
    def save(name,obj):
        target=OWN/name
        require(target.parent==OWN and not target.is_symlink(),'own root write only')
        target.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
    save('PAGE_MODEL.json',result['model'])
    save('CONTENT_RECEIPT.json',{'UTC':now,**result['content']})
    save('CUSTODY_RECEIPT.json',{'UTC':now,**result['custody']})
    files,dirs=inventory(OWN)
    payloads={name:meta for name,meta in files.items() if name not in TERMINALS}
    save('OWNED_MANIFEST.json',{'UTC':now,'owned_root':str(OWN),'files':[{'path':name,**meta} for name,meta in payloads.items()],'directories':dirs,'exact_existing_root_terminal_controls':TERMINALS,'subtree_basename_future_or_cache_exclusions':[],'ignored_assets_and_rasters_included':True})
    save('FINAL.json',{'UTC':now,'status':'PRIVATE_EDITORIAL_CANDIDATE_FROZEN','record_id':23133607,'sheet_row':140,'manifest':file_pin(OWN/'OWNED_MANIFEST.json'),'payload_files':len(payloads),'complete_owned_files':len(files),'complete_directories':len(dirs),'exact_existing_root_terminal_controls':TERMINALS,'whole_actual_MAIN':result['model']['whole_actual_MAIN'],'whole_page':result['content']['page'],'whole_head':result['model']['whole_head'],'model':file_pin(OWN/'PAGE_MODEL.json'),'BibTeX':result['content']['BibTeX'],'helpers':result['helpers'],'read_only_default_guard_separate_from_explicit_sealer':True,'assigned_editorial_completion_percent':100,'whole_research_programme_completion_claim':False,'canonical_url':None,'base_url':None,'production_url':None,'AA':None,'follow_up':None,'publication_authority':False,'fact_review_pending_root_handoff':True,'immutable_after_seal':True,'seal_exit_code_observed_externally':True})
    print(json.dumps({'status':'PRIVATE_EDITORIAL_CANDIDATE_FROZEN','FINAL':file_pin(final),'MAIN':result['model']['whole_actual_MAIN'],'files':len(files),'directories':len(dirs)},separators=(',',':')))
