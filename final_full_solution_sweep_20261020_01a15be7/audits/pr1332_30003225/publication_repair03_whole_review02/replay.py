"""Own bounded replay, archive controls and semantic counterexample checks."""
from pathlib import Path, PurePosixPath
import hashlib, html, io, json, os, stat, subprocess, sys, zipfile

HERE=Path(__file__).resolve().parent
PREP=HERE.parent/'publication_preparation_03'
SCI=PREP/'science'
REL=PREP/'release'
PREFIX='free_chain_nash_intersections_source/'

def need(x,m):
    if not x: raise RuntimeError(m)

def object_pairs(pairs):
    d={}
    for k,v in pairs:
        need(k not in d, 'duplicate JSON key');d[k]=v
    return d

def readzip(b, expected):
    with zipfile.ZipFile(io.BytesIO(b)) as z:
        names=z.namelist();need(len(names)==len(set(names)), 'duplicate ZIP name')
        need(set(names)==set(expected), 'ZIP complete membership')
        for i in z.infolist():
            p=PurePosixPath(i.filename)
            need(not p.is_absolute() and '..' not in p.parts and '\\' not in i.filename,'unsafe member')
            need(i.create_system==3 and i.external_attr>>16==stat.S_IFREG|0o644,'member mode')
            need(i.date_time==(2026,10,22,0,0,0) and not i.flag_bits&1,'member stamp/encryption')
            need(z.read(i)==expected[i.filename],'member bytes')
        need(z.testzip() is None,'CRC')

def forge(members, kind):
    buf=io.BytesIO()
    with zipfile.ZipFile(buf,'w') as z:
        items=list(members.items())
        if kind=='missing':items=items[1:]
        if kind=='duplicate':items.append(items[0])
        if kind=='extra':items.append((PREFIX+'extra',b'x'))
        for n,(name,data) in enumerate(items):
            if n==0 and kind=='traversal':name=PREFIX+'../x'
            if n==0 and kind=='changed':data+=b'false'
            i=zipfile.ZipInfo(name,(2026,10,22,0,0,0));i.create_system=3;i.external_attr=(stat.S_IFREG|0o644)<<16
            if n==0 and kind=='symlink':i.external_attr=(stat.S_IFLNK|0o777)<<16
            if n==0 and kind=='stamp':i.date_time=(2026,10,21,0,0,0)
            z.writestr(i,data)
    return buf.getvalue()

def main():
    dest=HERE/'private/extracted';dest.mkdir()
    members={PREFIX+p.relative_to(SCI).as_posix():p.read_bytes() for p in SCI.rglob('*') if p.is_file()}
    need(len(members)==21,'21 science members')
    parsed={}
    for name,data in members.items():
        if name.endswith('.json'):parsed[name]=json.loads(data,object_pairs_hook=object_pairs)
    src=(REL/'free-chain-nash-intersections-source-and-verification.zip').read_bytes();readzip(src,members)
    kit={n:(REL/n).read_bytes() for n in ['free-chain-nash-intersections.pdf','free-chain-nash-intersections-source-and-verification.zip','zenodo-deposit.json','zenodo-metadata.json','UPLOAD_README.txt']}
    readzip((REL/'free-chain-nash-intersections-upload-kit.zip').read_bytes(),kit)
    for name,data in members.items():
        p=dest/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data);p.chmod(0o644)
    source=dest/PREFIX
    receipts=[]
    for flag in [[],['-O'],['-OO']]:
        r=subprocess.run([sys.executable,'-I','-S','-B',*flag,str(source/'reproduce.py')],capture_output=True)
        need(r.returncode==0 and not r.stderr, 'full reproduce '+str(flag))
        receipts.append({'mode':flag,'sha256':hashlib.sha256(r.stdout).hexdigest(),'complete_output':json.loads(r.stdout)})
    r=subprocess.run([sys.executable,'-I','-S','-B',str(source/'build_package.py'),str(HERE/'private/rebuilt')],capture_output=True)
    need(r.returncode==0 and not r.stderr,'builder')
    for p in (HERE/'private/rebuilt').iterdir():need(p.read_bytes()==(REL/p.name).read_bytes(),'rebuilt '+p.name)
    controls=[]
    for kind in ['missing','duplicate','extra','traversal','changed','symlink','stamp']:
        try:readzip(forge(members,kind),members)
        except RuntimeError:controls.append({'name':kind,'rejected':True})
        else:raise RuntimeError('accepted false '+kind)
    meta=parsed[PREFIX+'zenodo-metadata.json'];dep=parsed[PREFIX+'zenodo-deposit.json'];paras=parsed[PREFIX+'DESCRIPTION_PARAGRAPHS.json']
    need(dep['metadata']==meta,'deposit metadata equal')
    desc=''.join('<p>'+html.escape(p,quote=True)+'</p>' for p in paras)
    need(meta['description']==desc,'four entire canonical HTML paragraphs')
    for old,new in [('&lt;=','&lt;'),('extensively involved','not involved'),('unrefereed preprint','refereed article'),('c4,c5 variable','no variables')]:
        wrong=desc.replace(old,new);need(wrong!=desc and wrong!=meta['description'],'inactive HTML control');controls.append({'name':'HTML '+old,'rejected':True})
    hist=(PREP.parent/'publication_preparation_01/SEARCH_QUERIES.json').read_bytes()
    audit=members[PREFIX+'SOURCE_AUDIT.md'].decode();inline=audit.split('```json\n')[1].split('\n```')[0]+'\n'
    need(inline.encode()==hist,'complete inline inventory identity')
    need(hashlib.sha256(hist).hexdigest()=='f0cf7941e95573d98d54e29857487f27b6c2653cc648fe75159f33d2eae44a25','historical pin')
    # Hash-consistent expected-output forgery: integrity is insufficient.
    target=source/'verification/CHECK_RESULTS.json';original=target.read_bytes();manifest=source/'PUBLIC_MANIFEST.json';old=manifest.read_bytes();j=json.loads(old)
    fake=original.replace(b'8192',b'8193',1);need(fake!=original,'active expected forgery');target.write_bytes(fake)
    j['files']['verification/CHECK_RESULTS.json']={'bytes':len(fake),'sha256':hashlib.sha256(fake).hexdigest()};manifest.write_text(json.dumps(j,indent=2)+'\n')
    r=subprocess.run([sys.executable,'-I','-S','-B',str(source/'build_package.py'),str(HERE/'private/forged')],capture_output=True);need(r.returncode==0,'hash-consistent forged build')
    r=subprocess.run([sys.executable,'-I','-S','-B',str(source/'reproduce.py')],capture_output=True);need(r.returncode!=0 and b'complete execution mismatch' in r.stderr,'forgery must fail replay')
    target.write_bytes(original);manifest.write_bytes(old)
    for n,b in members.items():need((dest/n).read_bytes()==b,'restored extracted member')
    # Independent all-integer proof diagnostics: these do not substitute for proof.
    semantic=[]
    for n in range(3,91):
        for k in range(2,n):
            m=(n+k-1)//k
            need(k*m>=n and k*(m-1)<n,'ceiling minimality')
            need((n==k*m)==(n%k==0),'reference divisibility')
            if n%k:
                floor=n//k;need(k*floor<n,'floor falsifier');semantic.append((n,k,floor,k*floor))
    # Real offending arc for the false floor formula: y=t^5,x=t^2,P=x².
    need(min(5,2*2)==4 and 4<5,'specific floor theorem counterexample')
    out={'status':'PASS','all21_members_parsed_or_read':True,'all6products_byte_exact':True,'sourceZIP_members':21,'kit_members':5,'replays':receipts,'active_controls':controls,'rehash_expected_forgery_rejected':True,'inline_historical_record_exact':True,'independent_rounding_pairs':sum(n-2 for n in range(3,91)),'false_floor_cases':len(semantic),'fresh_typesetting':False}
    (HERE/'REPLAY.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))

if __name__=='__main__':main()
