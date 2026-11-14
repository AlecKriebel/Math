"""One explicit old69 suite plus paired138 renderings, no persistent old tree."""
from pathlib import Path
import datetime, hashlib, json, shutil, subprocess, sys
E=Path(__file__).resolve().parent;OLD=E.parent;P=OLD.parents[1];LIVE=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public');PY=sys.executable
frozen=json.loads((OLD/'FROZEN_INPUT_SET.json').read_bytes());ids=frozen['old_configured_record_ids_in_order']
if len(ids)!=69 or len(set(ids))!=69 or set(ids)&{'23217863','23146753'}:raise ValueError('explicit old69')
if (E/'COMPATIBILITY.json').exists():raise RuntimeError('one-time campaign already recorded')
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
cmd=[PY,'-B',str(E/'run.py'),str(E/'final-content-check.stage.py'),*ids,'--site',str(LIVE),'--output-dir',str(E),'--output-stem','old69-content']
suite=subprocess.run(cmd,capture_output=True,text=True)
(E/'old69-content.stdout').write_text(suite.stdout);(E/'old69-content.stderr').write_text(suite.stderr)
receipt={'started_utc':start,'explicit_ids':ids,'old_content_suite':{'command':cmd,'exit':suite.returncode,'stderr':suite.stderr},'renderer_comparisons':[],'no_blanket_fixture_campaign':True,'no_stale_baseline_replay':True}
if suite.returncode!=0:
 (E/'COMPATIBILITY_FAILED.json').write_text(json.dumps(receipt,indent=2)+'\n');raise RuntimeError('old69 content suite failed; do not continue')
for rid in ids:
    runs=[];payloads=[]
    for name,source in [('installed',OLD/'inputs/render_page.py'),('proposed',E/'render_page.proposed.py')]:
        root=E/'compatibility-scratch'/name;site=root/'research';site.mkdir(parents=True,exist_ok=True)
        for shared in ['index.html','sitemap.xml']:shutil.copyfile(LIVE/'research'/shared,site/shared)
        text=source.read_text().replace('ROOT = Path(__file__).resolve().parents[1]',f'ROOT = Path({str(P)!r})').replace("SITE = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public/research')",f'SITE = Path({str(site)!r})')
        script=E/('compatibility-'+name+'.py');script.write_text(text)
        command=[PY,'-B',str(E/'run.py'),str(script),rid];r=subprocess.run(command,capture_output=True,text=True)
        runs.append({'variant':name,'command':command,'exit':r.returncode,'stdout':r.stdout,'stderr':r.stderr})
        payloads.append({str(f.relative_to(root)):f.read_bytes() for f in sorted(root.rglob('*')) if f.is_file()})
        if r.returncode!=0:
            receipt['renderer_failure']={'record':rid,'runs':runs};(E/'COMPATIBILITY_FAILED.json').write_text(json.dumps(receipt,indent=2)+'\n');raise RuntimeError('renderer failed '+rid)
    same=payloads[0]==payloads[1]
    record={'record':rid,'runs':runs,'full_output_bytes_equal':same,'files_compared':[{'path':key,'bytes':len(payloads[0][key]),'sha256':hashlib.sha256(payloads[0][key]).hexdigest()} for key in payloads[0]]}
    receipt['renderer_comparisons'].append(record)
    if not same:
        receipt['status']='FAIL';(E/'COMPATIBILITY_FAILED.json').write_text(json.dumps(receipt,indent=2)+'\n');raise RuntimeError('paired bytes differ '+rid)
    shutil.rmtree(E/'compatibility-scratch')
    print('paired',rid,flush=True)
receipt.update({'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'old_content_suite_runs':1,'old_configured_checked':69,'paired_renderer_processes':138,'full_output_byte_comparisons':69,'all_equal':True,'status':'PASS','manual_pilot_separate':True,'old_asset_fixtures_retained':False})
(E/'COMPATIBILITY.json').write_text(json.dumps(receipt,indent=2,ensure_ascii=False)+'\n');print('PASS explicitold69 content + paired138 renderers')
