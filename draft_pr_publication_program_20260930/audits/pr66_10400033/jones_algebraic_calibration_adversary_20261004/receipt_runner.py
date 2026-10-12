import subprocess,pathlib,datetime,json,hashlib,os,sys
ROOT=pathlib.Path(__file__).resolve().parent

def run(label,argv,cwd=None):
    directory=ROOT/"receipts"/label
    directory.mkdir(parents=True,exist_ok=True)
    body_directory=directory
    if label.startswith('primary_read_'):
        body_directory=pathlib.Path('/Users/alec/.cache/codex-pr66-audit-20261004/jones_algebraic')/label
        body_directory.mkdir(parents=True,exist_ok=True)
    start=datetime.datetime.now(datetime.timezone.utc).isoformat()
    working=str(pathlib.Path(cwd or ROOT).resolve())
    child=subprocess.Popen(argv,cwd=working,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    pid=child.pid
    stdout,stderr=child.communicate()
    stop=datetime.datetime.now(datetime.timezone.utc).isoformat()
    (body_directory/"stdout.txt").write_bytes(stdout)
    (body_directory/"stderr.txt").write_bytes(stderr)
    receipt={"argv":argv,"pid":pid,"cwd":working,"utc_started":start,"utc_ended":stop,"exit_code":child.returncode,"stdout":{"path":str(body_directory/"stdout.txt"),"bytes":len(stdout),"sha256":hashlib.sha256(stdout).hexdigest()},"stderr":{"path":str(body_directory/"stderr.txt"),"bytes":len(stderr),"sha256":hashlib.sha256(stderr).hexdigest()}}
    (directory/"receipt.json").write_text(json.dumps(receipt,indent=2)+"\n")
    print(json.dumps(receipt))
    print(stdout.decode(errors="replace"))
    print(stderr.decode(errors="replace"),file=sys.stderr)
    return child.returncode

if __name__=="__main__":
    raise SystemExit(run(sys.argv[1],sys.argv[2:]))
