"""Read-only source acquisition; all writes confined to this audit folder."""
import datetime, hashlib, json, pathlib, subprocess

ROOT = pathlib.Path(__file__).resolve().parent
PRIVATE = ROOT / 'private'
PRIVATE.mkdir(exist_ok=True)
ENV = {'PATH':'/usr/bin:/bin','LANG':'C','LC_ALL':'C','TZ':'UTC',
       '__CF_USER_TEXT_ENCODING':'0x1F5:0x0:0x0'}
def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()
def pin(path):
    data = path.read_bytes()
    return {'path':str(path),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
commands = [
    ['/usr/bin/curl','--fail','--location','--silent','--show-error',
     'https://msp.org/ant/2013/7-4/ant-v7-n4-p06-s.pdf','--output',str(PRIVATE/'takagi2013.pdf')],
    ['/opt/homebrew/bin/pdfinfo',str(PRIVATE/'takagi2013.pdf')],
    ['/opt/homebrew/bin/pdftotext','-layout',str(PRIVATE/'takagi2013.pdf'),str(PRIVATE/'takagi2013.txt')],
    ['/opt/homebrew/bin/pdftoppm','-f','22','-l','22','-r','240','-png','-singlefile',str(PRIVATE/'takagi2013.pdf'),str(PRIVATE/'p937')],
    ['/opt/homebrew/bin/pdftoppm','-f','24','-l','25','-r','240','-png',str(PRIVATE/'takagi2013.pdf'),str(PRIVATE/'scope')],
    ['/usr/bin/curl','--fail','--location','--silent','--show-error',
     'https://ems.press/content/serial-article-files/46224','--output',str(PRIVATE/'owr2009.pdf')],
    ['/opt/homebrew/bin/pdfinfo',str(PRIVATE/'owr2009.pdf')],
    ['/opt/homebrew/bin/pdftotext','-layout',str(PRIVATE/'owr2009.pdf'),str(PRIVATE/'owr2009.txt')],
]
receipts=[]
for index, argv in enumerate(commands):
    start=utc()
    p=subprocess.run(argv,cwd=ROOT,env=ENV,capture_output=True,check=False)
    stop=utc()
    for kind,data in [('stdout',p.stdout),('stderr',p.stderr)]:
        (PRIVATE/f'process{index:02d}.{kind}').write_bytes(data)
    receipts.append({'index':index,'argv':argv,'cwd':str(ROOT),'environment':ENV,
                     'started_at':start,'finished_at':stop,'exit_code':p.returncode,
                     'stdout_bytes':len(p.stdout),'stdout_sha256':hashlib.sha256(p.stdout).hexdigest(),
                     'stderr_bytes':len(p.stderr),'stderr_sha256':hashlib.sha256(p.stderr).hexdigest()})
    print(json.dumps({'index':index,'exit_code':p.returncode,'started_at':start,'finished_at':stop}))
    if p.returncode:
        (ROOT/'ACQUISITION_RECEIPTS.json').write_text(json.dumps({'processes':receipts},indent=2)+'\n')
        raise RuntimeError(f'acquisition process {index} failed; private diagnostic preserved')
inputs=[ROOT.parent/'original_head_authentication_20261006'/'SOURCE_STATEMENT.json',
        ROOT.parent/'original_head_authentication_20261006'/'original_attempt'/'CANDIDATE.md',
        ROOT.parent/'original_head_authentication_20261006'/'original_attempt'/'source_record.json',
        ROOT.parent/'original_head_authentication_20261006'/'original_attempt'/'turns.jsonl']
(ROOT/'ACQUISITION_RECEIPTS.json').write_text(json.dumps({'created_at':utc(),'processes':receipts,
  'private_artifacts':[pin(p) for p in sorted(PRIVATE.iterdir()) if p.is_file()],
  'immutable_inputs':[pin(p) for p in inputs]},indent=2)+'\n')
