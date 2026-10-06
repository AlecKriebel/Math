from pathlib import Path
import datetime, hashlib, json, os, subprocess, urllib.request

A = Path(__file__).resolve().parent
D = A / 'root_priority_20261006'
D.mkdir(exist_ok=True)
S = D / 'private_sources'
S.mkdir(exist_ok=True)
url = 'https://pagesperso.g-scop.grenoble-inp.fr/~szigetiz/OCG/13.C-Szigeti.pdf'
start = datetime.datetime.now(datetime.timezone.utc).isoformat()
with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent':'Independent mathematical priority verification'}), timeout=40) as r:
    body, resolved, content_type = r.read(), r.url, r.headers.get('Content-Type')
if not body.startswith(b'%PDF-'):
    raise RuntimeError('Retrieved source is not PDF')
pdf = S / 'chapoullie_szigeti_2022.pdf'
pdf.write_bytes(body)
commands = [
    ['/opt/homebrew/bin/pdftotext','-layout',str(pdf),str(S/'chapoullie_szigeti_2022.txt')],
    ['/opt/homebrew/bin/pdftoppm','-f','11','-l','12','-scale-to','1800','-png',str(pdf),str(S/'theorem13')]
]
processes = []
for argv in commands:
    p = subprocess.Popen(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    processes.append({'PID':p.pid,'argv':argv,'exit_code':p.returncode,'stdout_sha256':hashlib.sha256(stdout).hexdigest(),'stderr':stderr.decode()})
    if p.returncode:
        raise RuntimeError(stderr.decode())
record = {'UTC_start':start,'UTC_end':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_operator_PID':os.getpid(),'requested_url':url,'resolved_url':resolved,'content_type':content_type,'file':str(pdf),'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest(),'processes':processes,'private_material_not_selected_for_public_checkpoint':True}
(D/'PRIMARY_RETRIEVAL.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({k:record[k] for k in ('UTC_end','actual_operator_PID','bytes','sha256')}))
