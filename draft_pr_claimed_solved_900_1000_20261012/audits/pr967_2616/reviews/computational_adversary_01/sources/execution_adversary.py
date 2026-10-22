"""Fresh black-box hostile fixtures, actual writes/readbacks and import controls."""
from pathlib import Path
import copy, datetime, hashlib, json, os, platform, shutil, subprocess, sys, time

HERE=Path(__file__).resolve().parent.parent
PACK=HERE/'fixtures/replay_packet'
VERIFY_SHA='b805650e49c5096f0fe368653122989c1087f59447871a5cb6fc32843d6983d1'
BOOT_SHA='054dbe643ad4f78f13ea0595e4cab5379d438a33ab2fd2f6aed9f5125d9dcb57'
AUTHOR_MANIFEST='31bd2aed10d96d5ada5344531e2207dd4388c8cb1328e3c448ac89be5b78ec8c'

def sha(b):return hashlib.sha256(b).hexdigest()
def require(ok,msg):
    if not ok:raise RuntimeError(msg)

def main():
    public=PACK/'author/public';external=PACK/'author/external'
    for p,pin in [(public/'verify.py',VERIFY_SHA),(external/'bootstrap.py',BOOT_SHA),(external/'MANIFEST.json',AUTHOR_MANIFEST)]:
        require(sha(p.read_bytes())==pin,'independent execution pin')
    raw=(public/'fixtures.json').read_bytes();obj=json.loads(raw)
    hostile=HERE/'fixtures/new_hostile_imports';hostile.mkdir()
    sentinel=HERE/'fixtures/HOSTILE_IMPORT_EXECUTED'
    evil="open("+repr(str(sentinel))+",'wb').write(b'owned hostile module executed')\nraise RuntimeError('intentional owned hostile module')\n"
    for name in ['json.py','pathlib.py','hashlib.py','math.py','subprocess.py','tarfile.py','sitecustomize.py','usercustomize.py']:
        (hostile/name).write_text(evil)
    env=dict(os.environ)
    env.update(TMPDIR=str(HERE/'tmp'),TMP=str(HERE/'tmp'),TEMP=str(HERE/'tmp'),PYTHONPATH=str(hostile),
               PYTHONSTARTUP=str(hostile/'sitecustomize.py'),PYTHONDONTWRITEBYTECODE='1')
    receipts=[]
    def run(label,argv,stdin=b'',expected=None):
        start=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic()
        p=subprocess.run(argv,input=stdin,capture_output=True,cwd=hostile,env=env,timeout=60)
        row=dict(label=label,launch_utc=start,elapsed_seconds=time.monotonic()-t,argv=argv,
                 cwd=str(hostile),stdin_bytes=len(stdin),stdin_sha256=sha(stdin),returncode=p.returncode,
                 stdout=p.stdout.decode(errors='replace'),stderr=p.stderr.decode(errors='replace'))
        with (HERE/'receipts/new_execution_commands.jsonl').open('a') as f:
            f.write(json.dumps(row)+'\n')
        if expected is not None:
            row['expected_accept']=expected
            require((p.returncode==0)==expected,'unexpected acceptance: '+label)
        receipts.append(row)
        return p
    # A real successful local write from a hostile import is the positive
    # control; no external process/network behavior is included in that module.
    run('active_hostile_import_control',[sys.executable,'-S','-B','-c','import json'])
    require(sentinel.read_bytes()==b'owned hostile module executed','hostile import positive control did not write')
    sentinel.unlink()
    probe=HERE/'fixtures/write_probe';probe.mkdir();file=probe/'existing';file.write_bytes(b'base')
    with file.open('ab') as f:f.write(b'+append')
    require(file.read_bytes()==b'base+append','write positive readback')
    (probe/'new').write_bytes(b'new');require((probe/'new').read_bytes()==b'new','create positive readback')
    file.chmod(0o444);(probe/'new').chmod(0o444);probe.chmod(0o555)
    denied=[]
    try:
        for path in [file,probe/'not_created']:
            try:
                with path.open('ab') as f:f.write(b'forbidden')
            except PermissionError as e:denied.append(dict(path=path.name,errno=e.errno,error=str(e)))
            else:raise RuntimeError('read-only OS write unexpectedly allowed')
        require(file.read_bytes()==b'base+append' and not (probe/'not_created').exists(),'denial readback')
    finally:
        probe.chmod(0o755)
        for p in probe.iterdir():p.chmod(0o644)
    variants=[]
    for key,value in obj.items():
        for kind,bad in [('true',True),('false',False),('float',float(value)),('negative',-1),
                         ('off_by_one',value+1),('string',str(value)),('null',None),('list',[value]),('object',{'value':value})]:
            v=dict(obj);v[key]=bad;variants.append((key+':'+kind,json.dumps(v).encode()))
        missing=dict(obj);del missing[key];variants.append((key+':missing',json.dumps(missing).encode()))
        text=json.dumps(obj,separators=(',',':'))
        # Duplicate every exact field, including a duplicate expressed by an
        # escaped Unicode first character: JSON must normalize before checking.
        extra=json.dumps(key)+':'+str(value)
        variants.append((key+':duplicate',(text[:-1]+','+extra+'}').encode()))
        escaped='"\\u%04x%s"'%(ord(key[0]),key[1:])
        variants.append((key+':escaped_duplicate',(text[:-1]+','+escaped+':'+str(value)+'}').encode()))
    for label,value in [('nan','NaN'),('positive_infinity','Infinity'),('negative_infinity','-Infinity'),
                        ('overflow_float','1e99999'),('huge_integer','9'*10000)]:
        variants.append((label,raw.replace(b'"problem_id": 2616',b'"problem_id": '+value.encode())))
    variants.extend([('empty',b''),('invalid_utf8',b'\xff'),('trailing',raw+b'{}'),('array_root',b'[]'),
                     ('null_root',b'null'),('oversize_whitespace',b' '*65537),
                     ('valid_json_oversize',raw+b' '*(65537-len(raw))),
                     ('deep_array',b'['*2000+b'0'+b']'*2000)])
    outcomes=[]
    for label,flags in [('normal',[]),('O',['-O']),('OO',['-OO'])]:
        cmd=[sys.executable,'-I','-S','-B',*flags,str(public/'verify.py'),'--stdin']
        good=run(label+':positive',cmd,raw,True)
        run(label+':maximum_accepted_size',cmd,raw+b' '*(65536-len(raw)),True)
        malformed=[]
        for case,payload in variants:
            p=run(label+':'+case,cmd,payload,False)
            try:structured=json.loads(p.stderr).get('ok') is False
            except (ValueError,AttributeError):structured=False
            malformed.append(dict(label=case,structured=structured))
        bootcmd=[sys.executable,'-I','-S','-B',*flags,str(external/'bootstrap.py'),str(public),
                 str(external/'MANIFEST.json'),AUTHOR_MANIFEST,label]
        run(label+':external_bootstrap',bootcmd,expected=True)
        require(not sentinel.exists(),'hostile import executed under isolation')
        outcomes.append(dict(mode=label,positive=json.loads(good.stdout),rejected=len(malformed),
                             unstructured_rejections=[v['label'] for v in malformed if not v['structured']]))
    result=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),host=dict(uid=os.getuid(),euid=os.geteuid(),
                executable=sys.executable,python=sys.version,platform=platform.platform()),
                actual_readonly_denials=denied,positive_write_and_create_readbacks=True,
                active_hostile_import_positive_control=True,isolated_import_marker_absent=True,
                modes=outcomes,command_receipt='new_execution_commands.jsonl',command_count=len(receipts),
                scope='Owned local file/process controls only; no network requests; no compromised-host or concurrent-race security claim.')
    (HERE/'receipts/new_execution_adversary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
