import subprocess,json,base64,pathlib,datetime,sys
p=pathlib.Path(__file__).resolve().parent
r=json.loads(subprocess.check_output(['gh','api','repos/AlecKriebel/Math/pulls/411']))
b=json.loads(subprocess.check_output(['gh','api','repos/AlecKriebel/Math/contents/unsolved_math_prioritization/QUEUE.md?ref='+r['head']['sha']]))
t=base64.b64decode(b['content']).decode(); rows=[x for x in t.splitlines() if '6800014 / AMR-067-0014' in x]
receipt={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'number':r['number'],'state':r['state'],'draft':r['draft'],'merged':r['merged'],'merged_at':r['merged_at'],'head':{'ref':r['head']['ref'],'sha':r['head']['sha']},'queue_blob':b['sha'],'selected_rows':rows,'local_branch':subprocess.check_output(['git','branch','--show-current']).decode().strip()}
receipt['passed']=r['state']=='open' and r['draft'] and not r['merged'] and r['head']['sha']=='ac8b960bdda61c154cc30d7e3aba70389a9b139e' and r['head']['ref']=='research/ricci-pinching-6800014' and b['sha']=='81f397cb34eeb6ce1d3c828992abc0969ab2d74d' and len(rows)==1 and 'claimed_solved' in rows[0] and '2/5' in rows[0]
(p/sys.argv[1]).write_text(json.dumps(receipt,indent=2)+'\n'); print(json.dumps(receipt,indent=2));assert receipt['passed'], 'STOP: scope metadata changed or gate incomplete'
