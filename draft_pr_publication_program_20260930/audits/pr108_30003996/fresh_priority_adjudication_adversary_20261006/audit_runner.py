import sys,subprocess,json,hashlib,os
from pathlib import Path
from datetime import datetime,timezone
W=Path(__file__).resolve().parent
A=W.parent
F={
 'owr':A/'primary_sources_20261006/owr.pdf',
 'ccz':A/'priority_martin_integer_lift_20261006/private/ccz2010.pdf',
 'friesen':A/'priority_martin_integer_lift_20261006/private/friesen2019.pdf',
 'owa':A/'priority_martin_integer_lift_20261006/private/owa2017.pdf',
 'jlrk':A/'priority_classical_tree_mechanisms_20261006/_private/jlrk1977_cwi.stdout',
 'ocst':A/'priority_classical_tree_mechanisms_20261006/_private/ocst2016.stdout',
 'shared':A/'priority_classical_tree_mechanisms_20261006/_private/shared2016.stdout',
 'reload':A/'priority_classical_tree_mechanisms_20261006/_private/mincca2013.stdout',
 'rainbow':A/'priority_classical_tree_mechanisms_20261006/_private/rainbow2024.stdout',
 'scale':A/'priority_exact_question_history_20261006/private/scale_free_2005.13703v1.pdf',
 'routing':A/'priority_exact_question_history_20261006/private/routing_2021.pdf',
 'neusupp':A/'priority_martin_integer_lift_20261006/private/neurips2022_supp.pdf',
 'gm':A/'priority_martin_integer_lift_20261006/private/goemans_myung1993.pdf',
}
def utc():return datetime.now(timezone.utc).isoformat().replace('+00:00','Z')
mode,key=sys.argv[1:3]; src=F[key]
if mode=='info':cmd=['pdfinfo',str(src)]
elif mode=='pages':cmd=['pdftotext','-f',sys.argv[3],'-l',sys.argv[4],'-layout',str(src),'-']
else:raise SystemExit('mode')
start=utc(); p=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=p.communicate();end=utc()
label='_'.join(sys.argv[1:]); op=W/'private'/f'{label}.stdout';ep=W/'private'/f'{label}.stderr';op.write_bytes(out);ep.write_bytes(err)
rec={'label':label,'start_utc':start,'end_utc':end,'operator_pid':os.getpid(),'child_pid':p.pid,'argv':cmd,'exit_code':p.returncode,'source_path':str(src),'source_bytes':src.stat().st_size,'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'stdout_file':str(op.relative_to(W)),'stdout_bytes':len(out),'stdout_sha256':hashlib.sha256(out).hexdigest(),'stderr_file':str(ep.relative_to(W)),'stderr_bytes':len(err),'stderr_sha256':hashlib.sha256(err).hexdigest(),'interpretation':'Actual extraction/display; audit read claims must separately distinguish complete displayed sections and truncation.'}
with (W/'EXECUTION_RECEIPTS.jsonl').open('a') as f:f.write(json.dumps(rec)+'\n')
print(json.dumps(rec))
display='\n'.join(' '.join(line.split()) for line in out.decode('utf-8','replace').splitlines()) if '--compact' in sys.argv else out.decode('utf-8','replace')
if '--compact' in sys.argv:(W/'private'/f'{label}.display.txt').write_text(display+'\n')
print(display)
if err:print(err.decode('utf-8','replace'))
raise SystemExit(p.returncode)
