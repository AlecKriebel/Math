import datetime,hashlib,json,pathlib,subprocess
R=pathlib.Path(__file__).resolve().parent
D=pathlib.Path('/Users/alec/.cache/codex-pr65-priority-20261004/status_family_20261004')
def utc(): return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='microseconds')
for n in ['nicolau_contractive2026_fresh','ivrii_nicolau2025_fresh','bampouras_nicolau2026_fresh']:
    src=D/(n+'.pdf'); dest=D/(n+'.txt')
    argv=['pdftotext','-layout',str(src),str(dest)]
    start=utc();p=subprocess.Popen(argv,cwd=R,stdout=subprocess.PIPE,stderr=subprocess.PIPE);pid=p.pid;out,err=p.communicate();end=utc()
    (D/(n+'.extract.stdout')).write_bytes(out);(D/(n+'.extract.stderr')).write_bytes(err)
    receipt={'name':n+'.extract','child_pid':pid,'argv':argv,'cwd':str(R),'started_utc':start,'ended_utc':end,'exit_code':p.returncode,'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'output_sha256':hashlib.sha256(dest.read_bytes()).hexdigest() if dest.is_file() else None,'stdout_path':str(D/(n+'.extract.stdout')),'stderr_path':str(D/(n+'.extract.stderr')),'stdout_sha256':hashlib.sha256(out).hexdigest(),'stderr_sha256':hashlib.sha256(err).hexdigest()}
    (R/(n+'.extract.receipt.json')).write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt))
    if p.returncode: continue
    pages=dest.read_text().split('\f')
    print(n, 'FORMFEED_SEGMENTS',len(pages))
    for term in ['Holland','5.51','Kahane','Aleksandrov','Blaschke','explicit','Zygmund']:
        print('TERM',term,[(i+1, [l for l in pg.splitlines() if term.lower() in l.lower()]) for i,pg in enumerate(pages) if term.lower() in pg.lower()])
