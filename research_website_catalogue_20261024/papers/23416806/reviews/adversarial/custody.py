"""Read-only authentication of whole original objects, recursive ZIPs and prior seals.

Default creates a fresh receipt here. --verify-only does not write. No supplied
code, network requests, extraction, archive changes or historical text reading.
"""
from pathlib import Path, PurePosixPath
import datetime
import hashlib
import io
import json
import stat
import sys
import zipfile

if sys.argv[1:] not in ([], ['--verify-only']):
    raise SystemExit('usage: custody.py [--verify-only]')
D=Path(__file__).resolve().parent
P=D.parents[3]
S=P/'papers/23416806/sources'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def bind(f):
    data=f.read_bytes()
    return {'path':str(f),'bytes':len(data),'sha256':sha(data)}


def require(ok,msg):
    if not ok:
        raise RuntimeError(msg)


auth={
    'SOURCE_READY.json':'603d9a23bf5876d12fd7d0b6caf50f9e16e5734380383c7afa61b2c560dff5c3',
    'SOURCE_READY_MANIFEST.json':'3c7cd9ceed22172150ce17fe8139d7218811f2186d0ae84078279b59f8aa449e',
    'SOURCE_READY_SEAL.json':'b4edc6ba13576ce2329a9fe55af07eb39b77c729021ed83e879a2f6ef1b712da',
}
for n,h in auth.items():
    require(sha((S/n).read_bytes())==h,'source authority mismatch '+n)
manifest=json.loads((S/'SOURCE_READY_MANIFEST.json').read_text())
originals=[]
for b in manifest['files']:
    pp=PurePosixPath(b['path'])
    require(not pp.is_absolute() and '..' not in pp.parts and str(pp)==b['path'],'noncanonical original')
    got=bind(S/pp)
    require(got['bytes']==b['bytes'] and got['sha256']==b['sha256'],'original mismatch '+str(pp))
    originals.append(got)
require(len(originals)==manifest['file_count']==195,'original count')
ready=json.loads((S/'SOURCE_READY.json').read_text())
record=json.loads((S/'record.raw.json').read_text())
latest=json.loads((S/'latest.raw.json').read_text())
versions=json.loads((S/'versions.raw.json').read_text())
require(record['id']==latest['id']==23416806 and record['metadata']['version']=='1.0'
        and record['metadata']['publication_date']=='2026-10-16'
        and record['created']=='2026-10-16T11:30:08.825717+00:00'
        and versions['hits']['total']==1,'actual metadata mismatch')
require(len(record['files'])==len(ready['all_assets'])==2,'public file-object count')
for a in ready['all_assets']:
    obj=a['original_api_file_object']
    require(obj in record['files'] and obj in latest['files'],'public file object changed')
    data=(S/obj['key']).read_bytes()
    require(len(data)==obj['size']==a['bytes'] and sha(data)==a['sha256']
            and 'md5:'+hashlib.md5(data).hexdigest()==obj['checksum'],'public object bytes')

archive=json.loads((S/'archive-members.json').read_text())
expected={(b['container'],b['member']):b for b in archive['members']}
require(len(expected)==186,'recursive member identities')
outer=(S/'source-and-verification.zip').read_bytes()
container_data={'source-and-verification.zip':outer}
members=[]
containers=[]
for c in archive['archive_containers']:
    name=c['container']
    if name not in container_data:
        parent,member=name.rsplit('::',1)
        with zipfile.ZipFile(io.BytesIO(container_data[parent])) as z:
            container_data[name]=z.read(member)
    data=container_data[name]
    require(len(data)==c['bytes'] and sha(data)==c['sha256'],'container bytes '+name)
    containers.append({'name':name,'bytes':len(data),'sha256':sha(data)})
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        require(z.testzip() is None,'ZIP CRC '+name)
        names=set()
        for info in z.infolist():
            pp=PurePosixPath(info.filename)
            require(not info.is_dir() and not pp.is_absolute() and '..' not in pp.parts
                    and str(pp)==info.filename and info.filename not in names
                    and stat.S_IFMT(info.external_attr>>16) in (0,stat.S_IFREG),'unsafe regular member')
            names.add(info.filename)
            b=expected[(name,info.filename)]
            raw=z.read(info)
            path=Path(b['extracted_path'])
            require(path.resolve().is_relative_to(S.resolve()),'extracted path outside original root')
            require(path.read_bytes()==raw and len(raw)==b['bytes'] and sha(raw)==b['sha256']
                    and format(info.CRC,'08x')==b['CRC32'],'member mismatch '+info.filename)
            members.append({'container':name,'member':info.filename,'extracted_path':str(path),
                            'bytes':len(raw),'sha256':sha(raw),'CRC32':format(info.CRC,'08x')})
require(len(members)==186 and len(containers)==4 and sum(x['bytes'] for x in members)==815561,'recursive totals')
require(sum(x['container']=='source-and-verification.zip' for x in members)==150,'outer members')

base=P/'papers/23416806/reviews/scope'
primaries=[]
for name,h in {
    'prz2014.pdf':'0031cabde0d3f0878efad9d992470cef3b0a9ad5834bf1c48d99a0724b5eb424',
    'boyle2007.pdf':'0aa7722ba25a0468a83a1fd30e9fbf91c8bc77419cee58eb1447469019c7d98a',
    'dykstra2007.pdf':'f2c17cddb60fa6b0ad669cc85f6f7efb4d9298fa03854e5c85aacd8ed3b2d928',
    'ballier-v1.pdf':'a8ffd9af631424355e977769f578d48bb0fc38cc2590ab3ff26f7b441a75d94d',
}.items():
    f=base/'cache/primary'/name;b=bind(f)
    require(b['sha256']==h and f.read_bytes().startswith(b'%PDF-'),'primary mismatch '+name)
    primaries.append(b)
failed=[]
f=base/'cache/primary/ballier-final.pdf'
if f.exists():
    require(not f.read_bytes().startswith(b'%PDF-'),'failed journal response unexpectedly PDF')
    failed.append(dict(bind(f),actual_PDF=False,counted_as_primary_body=False))

prior=[]
for rel,h in {
    'papers/23074543/reviews/adversarial':'289a69d2eb79c2f907b584bf3eb34e16d5e7e04a98669e4052ac87ccfaf49aa7',
    'verification/cfh-independent-code-audit-sol-20261025':'08df6760943ae91c7fb4f22b5bc6952aea2325bc87ae1b1623a47af5dbdb984f',
    'papers/23442760/reviews/adversarial':'97745de4ecdbbfd9cdd465150871285f42a484668e12f88ea4852b48e33e5518',
    'papers/23395703/reviews/adversarial':'cfa3ba1ab7d58027bca29c4e443afc24bd1e5da956107876c9d91f163fcf2ece',
    'papers/23333353/reviews/adversarial':'3956c3c929eecbddc47477ebf48304a1e966bd79decbfa0ae2505682af17bccf',
}.items():
    d=P/rel;sealfile=d/'FINAL_SEAL.json'
    require(sha(sealfile.read_bytes())==h,'prior seal '+rel)
    seal=json.loads(sealfile.read_text());mf=d/seal['manifest']
    require(sha(mf.read_bytes())==seal['manifest_sha256'],'prior manifest')
    files=json.loads(mf.read_text())['files']
    if isinstance(files,dict):files=[dict(v,path=k) for k,v in files.items()]
    owned=[]
    for b in files:
        got=bind(d/b['path'])
        require(got['bytes']==b['bytes'] and got['sha256']==b['sha256'],'prior owned evidence')
        owned.append(got)
    prior.append({'namespace':str(d),'seal':bind(sealfile),'manifest':bind(mf),'owned_files':owned})

receipt={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
         'status':'ALL_ORIGINAL_RECURSIVE_ARCHIVE_PRIMARY_AND_PRIOR_OBJECTS_VERIFIED',
         'source_authentication':[bind(S/n) for n in auth], 'whole_original_bindings':originals,
         'archive_containers':containers,'archive_member_occurrences':members,
         'primary_bindings':primaries,'failed_response_bindings':failed,'prior_packet_bindings':prior,
         'scope_primary_receipt':bind(base/'primary-fetch-receipts.json'),
         'source_or_prior_objects_modified':False,'supplied_code_executed':False}
if sys.argv[1:] != ['--verify-only']:
    with (D/'ORIGINAL_BINDINGS.json').open('x') as f:
        json.dump(receipt,f,indent=2);f.write('\n')
print(json.dumps({'originals':len(originals),'member_occurrences':len(members),'containers':len(containers),
                  'actual_primary_PDFs':len(primaries),'prior_packets':len(prior),
                  'prior_owned_files':sum(len(x['owned_files']) for x in prior),'status':receipt['status']}))
