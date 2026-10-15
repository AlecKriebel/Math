from pathlib import Path
import importlib.util,json,re,datetime,hashlib
D=Path(__file__).resolve().parent;P=D.parent
s=importlib.util.spec_from_file_location('scope',P/'audits/pr156_30005432/prepare_scoped_merge.py')
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
out=[]
for number in range(165,181):
 r=m.api('pulls/'+str(number));head=r['head']['sha']
 match=re.search(r'(\d{6,9})\s*:',r['title']);m.require(match is not None,'Cannot identify exact problem without reading math')
 problem=match.group(1);queue=m.body_at('unsolved_math_prioritization/QUEUE.md',head).decode()
 rows=[l for l in queue.splitlines() if '| '+problem+' /' in l];m.require(len(rows)==1,'Status row not unique')
 cells=rows[0].split('|');m.require(len(cells)==14,'QUEUE schema changed')
 status=cells[8].strip();effort=cells[9].strip()
 result={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'PR':number,'URL':r['html_url'],'title':r['title'],'head':head,'problem_id':problem,'state':r['state'],'draft':r['draft'],'created_at':r['created_at'],'original_head_QUEUE_row':rows[0],'literal_status':status,'effort':effort,'original_head_QUEUE_sha256':hashlib.sha256(queue.encode()).hexdigest(),'eligible':r['state']=='open' and r['draft'] and status=='claimed_solved','mathematical_contents_read':False,'mathematical_audit_or_repair_started':False,'PR_or_native_files_modified':False,'status_only_intake':True}
 m.save(D/('PR'+str(number)+'_STATUS_ONLY.json'),result);out.append(result);print(json.dumps({'PR':number,'problem_id':problem,'status':status,'effort':effort,'head':head,'eligible':result['eligible']}),flush=True)
 if result['eligible']:break
m.save(D/'INTAKE_SUMMARY.json',{'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'after_completed_PR':164,'fully_completed_count':32,'published_count':18,'status_only':True,'rows':out,'next_eligible':next((r for r in out if r['eligible']),None),'all_nonclaimed_cases_untouched':True,'MAIN_writer_authority':False,'goal_complete':False})
(D/'RESEARCH_LOG.md').write_text('# Ordered status-only intake after PR164\n\n'+datetime.datetime.now(datetime.timezone.utc).isoformat()+' — Intake batch complete100%; overall32/dated99=32.32%,18published. Only titles, original-head QUEUE status and metadata read. All nonclaimed submissions untouched; no mathematical findings or disposition actions on skipped cases. Next eligible mathematical audit not yet started. No MAIN writer authority.\n')

