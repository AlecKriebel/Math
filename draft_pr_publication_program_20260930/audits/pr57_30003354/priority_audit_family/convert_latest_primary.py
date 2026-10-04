from pathlib import Path
import datetime as dt,hashlib,json,os,subprocess
F=Path(__file__).absolute().parent;C=F.parent/'private_primary_reading_cache/priority_audit_family'
rows=[]
for name in ['banakh_belegradek_jstage','mateljevic_endpoint_arxiv','plotnikov_russian','peters_1987']:
    p=C/(name+'.pdf');out=C/(name+'.layout.txt')
    assert p.is_file() and not out.exists()
    cmd=['/opt/homebrew/bin/pdftotext','-layout',str(p),str(out)]
    z=dict(argv=cmd,caller_pid=os.getpid(),started_utc=dt.datetime.now(dt.timezone.utc).isoformat(),pdf_sha256=hashlib.sha256(p.read_bytes()).hexdigest())
    child=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE);a,b=child.communicate()
    z.update(child_pid=child.pid,exit_code=child.returncode,finished_utc=dt.datetime.now(dt.timezone.utc).isoformat(),complete_stdout_utf8=a.decode(),complete_stderr_utf8=b.decode(),output_bytes=out.stat().st_size if out.exists() else None,output_sha256=hashlib.sha256(out.read_bytes()).hexdigest() if out.exists() else None)
    rows.append(z)
with (F/'LATEST_PRIMARY_TEXT_CONVERSION.json').open('x') as f:json.dump(dict(schema='pr57-priority-actual-text-conversion/v1',source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),rows=rows),f,indent=2);f.write('\n')
print(json.dumps(dict(caller_pid=os.getpid(),completed=len(rows),all_exit_zero=all(z['exit_code']==0 for z in rows))))
