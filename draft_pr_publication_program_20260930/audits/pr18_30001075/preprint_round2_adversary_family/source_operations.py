#!/usr/bin/env python3
"""Actual read-only PDF decoding/rendering captures; foreign bodies remain ignored."""
from pathlib import Path
import datetime,hashlib,json,os,subprocess,sys,time
if sys.flags.optimize:raise RuntimeError('Nonoptimized controller required')
r=Path(__file__).resolve().parent;p=r/'tmp/private'
def h(f):
 b=f.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def capture(label,argv,inp,glob):
 folder=r/'captures'/label;folder.mkdir(exist_ok=False)
 (folder/'controller.py').write_bytes(Path(__file__).read_bytes())
 obj={'UTC_prelaunch':utc(),'actual_controller_pid':os.getpid(),'optimization':sys.flags.optimize,'python':sys.version,'argv':argv,'cwd':str(r),'input':{'path':str(inp),**h(inp)},'controller':h(Path(__file__))}
 (folder/'PRELAUNCH.json').write_text(json.dumps(obj,indent=2)+'\n');t=time.perf_counter()
 with (folder/'stdout.txt').open('wb') as out,(folder/'stderr.txt').open('wb') as err:
  child=subprocess.Popen(argv,cwd=r,stdout=out,stderr=err)
  obj['actual_child_pid']=child.pid;obj['UTC_launch_return']=utc();(folder/'LAUNCH.json').write_text(json.dumps(obj,indent=2)+'\n');obj['returncode']=child.wait()
 obj['UTC_end']=utc();obj['runtime_seconds']=time.perf_counter()-t
 obj['stdout']=h(folder/'stdout.txt');obj['stderr']=h(folder/'stderr.txt');obj['input_unchanged']=h(inp)==obj['input']|{'path':str(inp)} if False else h(inp)=={k:v for k,v in obj['input'].items() if k!='path'}
 obj['outputs']=[{'path':str(f.relative_to(r)),**h(f)} for f in sorted(p.glob(glob))]
 (folder/'CAPTURE.json').write_text(json.dumps(obj,indent=2)+'\n')
 if obj['returncode'] or not obj['input_unchanged']:raise RuntimeError('Captured failed read-only source operation '+label)
 return obj
paper=r.parent/'preprint_v1/common_tangent_nullness.pdf'
recs=[]
recs.append(capture('actual-paper-info',['/opt/homebrew/bin/pdfinfo',str(paper)],paper,'captured-paper*.png'))
recs.append(capture('actual-paper-render',['/opt/homebrew/bin/pdftoppm','-r','100','-png',str(paper),str(p/'captured-paper')],paper,'captured-paper*.png'))
for n in range(1,9):
 if (p/f'paper-{n}.png').read_bytes()!=(p/f'captured-paper-{n}.png').read_bytes():raise RuntimeError('New render differs from personally inspected render')
for stem,first,last,label in [('ems',76,76,'ems'),('simon',13,13,'simon-density'),('simon',26,27,'simon-rademacher'),('simon',32,34,'simon-area'),('cheong2024',18,20,'article-topology'),('topve2011',11,11,'historical-question')]:
 inp=p/(stem+'.pdf');prefix='captured-'+label
 recs.append(capture('actual-'+label+'-render',['/opt/homebrew/bin/pdftoppm','-f',str(first),'-l',str(last),'-r','100','-png',str(inp),str(p/prefix)],inp,prefix+'*.png'))
for stem in ['ems','simon','cheong2024','topve2011']:
 inp=p/(stem+'.pdf');out=p/('captured-'+stem+'.txt')
 recs.append(capture('actual-'+stem+'-text',['/opt/homebrew/bin/pdftotext','-layout',str(inp),str(out)],inp,'captured-'+stem+'.txt'))
 if (p/(stem+'.txt')).read_bytes()!=out.read_bytes():raise RuntimeError('Captured extraction differs from personally read extraction')
(r/'SOURCE_OPERATION_AUDIT.json').write_text(json.dumps({'UTC':utc(),'actual_pid':os.getpid(),'operations':recs,'original_inspected_paper_renders_byte_identical':True,'all_personally_read_extractions_byte_identical':True,'private_body_domain':'tmp/private, ignored by tracked root tmp/ rule','scope':'Actual decoding/rendering; personal reading attested separately. Reused bodies are not newly downloaded.'},indent=2)+'\n')
print(json.dumps({'operations':len(recs),'child_pids':[q['actual_child_pid'] for q in recs],'all_pass':True},indent=2))
