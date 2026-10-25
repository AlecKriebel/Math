"""Whole-original/primary/prior-packet custody only; no mathematical sampling.

Inspect before running. --verify-only repeats without writes. Default creates a
fresh own receipt. No supplied code, network, extraction or original writes.
"""
from pathlib import Path,PurePosixPath
import datetime,hashlib,json,stat,sys,zipfile

if sys.argv[1:] not in ([],['--verify-only']):raise SystemExit('usage: custody.py [--verify-only]')
D=Path(__file__).resolve().parent;P=D.parents[3];S=P/'papers/23441617/sources'


def sha(b):return hashlib.sha256(b).hexdigest()


def bind(f):
    b=f.read_bytes();return {'path':str(f),'bytes':len(b),'sha256':sha(b)}


def need(ok,msg):
    if not ok:raise RuntimeError(msg)


auth={'SOURCE_READY.json':'90f741c1aa5c9ed2305762ab3cc51d820b87cabd4f07bbf5707b20e1e6cd1aae',
      'SOURCE_READY_MANIFEST.json':'6ecf3402bffe303096da8166ec08ea550dbb2738a2da7e1c261bc7f886ecca9a',
      'SOURCE_READY_SEAL.json':'465e6b0ce7212ea6fe89a4f17f0f8988d6b713323d171f45982f3fa10d03b75a'}
for n,h in auth.items():need(sha((S/n).read_bytes())==h,'source authentication '+n)
mf=json.loads((S/'SOURCE_READY_MANIFEST.json').read_text());originals=[]
for b in mf['files']:
    pp=PurePosixPath(b['path']);need(not pp.is_absolute() and '..' not in pp.parts and str(pp)==b['path'],'original path')
    got=bind(S/pp);need(got['bytes']==b['bytes'] and got['sha256']==b['sha256'],'original bytes '+str(pp));originals.append(got)
need(len(originals)==mf['file_count']==127,'127 originals')
ready=json.loads((S/'SOURCE_READY.json').read_text());record=json.loads((S/'record.raw.json').read_text())
latest=json.loads((S/'latest.raw.json').read_text());versions=json.loads((S/'versions.raw.json').read_text())
need(record['id']==latest['id']==23441617 and versions['hits']['total']==1
     and record['metadata']['version']=='1.0' and record['metadata']['publication_date']=='2026-10-17'
     and record['created']=='2026-10-17T20:15:34.082127+00:00','actual edition metadata')
need(len(record['files'])==len(ready['all_assets'])==2,'two public file objects')
for a in ready['all_assets']:
    o=a['original_api_file_object'];data=(S/o['key']).read_bytes()
    need(o in record['files'] and o in latest['files'] and len(data)==o['size']==a['bytes']
         and sha(data)==a['sha256'] and 'md5:'+hashlib.md5(data).hexdigest()==o['checksum'],'complete actual asset')
archive=json.loads((S/'archive-members.json').read_text());expected={b['member']:b for b in archive['members']};members=[]
need(len(expected)==118 and len(archive['archive_containers'])==1,'archive identities')
with zipfile.ZipFile(S/'Real_Complement_Modulus_Verification_v1.0.zip') as z:
    need(z.testzip() is None,'all CRCs');names=set()
    for info in z.infolist():
        pp=PurePosixPath(info.filename)
        need(not info.is_dir() and not pp.is_absolute() and '..' not in pp.parts and str(pp)==info.filename
             and info.filename not in names and stat.S_IFMT(info.external_attr>>16) in (0,stat.S_IFREG),'safe regular member')
        names.add(info.filename);b=expected[info.filename];raw=z.read(info);f=Path(b['extracted_path'])
        need(f.resolve().is_relative_to(S.resolve()) and f.read_bytes()==raw and len(raw)==b['bytes']
             and sha(raw)==b['sha256'] and format(info.CRC,'08x')==b['CRC32'],'original member exact bytes')
        members.append({'member':info.filename,'extracted_path':str(f),'bytes':len(raw),'sha256':sha(raw),'CRC32':format(info.CRC,'08x')})
need(len(members)==118 and sum(b['bytes'] for b in members)==629704,'complete archive totals')

E=P/'papers/23441617/reviews/scope';base=E/'cache/primary';primaries=[]
for n,h in {
    'hayman-lingham-v2.pdf':'8e28fd4403a07e4e19a9816b7efaafddf9f475d59cf8c34a8255cb03833ed4f0',
    'dnpv-v3.pdf':'9c766906f32852c89caf6b9aec08fd3d6ef134bee939e3bd70046b1b20da5c32',
    'brezis2002.pdf':'f4b17057703636822a06c5c078d968be87fd6e8705d0b9ca95822629a0e95486',
    'heinonen-koskela.pdf':'27edd65a70515fc51bbfe5772feee330f10302e40bf55d9a8296b5742a762e83',
    'hesse1975.pdf':'2e3097cc73232acaeb92a42a7cde3316bee5976b9e8ddf601c8ecfd23cb4f83d',
    'springer-update-members/Hayman_Lingham-updates.pdf':'44d6fe24868b8f4f3ab128f859c3ed1cc2c538bc87ef0b398025e91c2d82497f',
    'ams1982-program.pdf':'ee604288daf554b32050a125762ff372427159e5096dbc4d7193ee88ab1019ff',
}.items():
    f=base/n;b=bind(f);need(b['sha256']==h and f.read_bytes().startswith(b'%PDF-'),'actual primary '+n);primaries.append(b)
other=[]
for n,h in {'springer2019-chapter.html':'917e6a8531378c600efb21bd33e2269e78d0afe1f0ecc63a0dd04d5b098f06b6',
            'springer-updates-response':'18a508f83c8bd21bae2c5ab48b7dae1816a60b65881092f2d6becacdba2d4c84'}.items():
    f=base/n;b=bind(f);need(b['sha256']==h and not f.read_bytes().startswith(b'%PDF-'),'access response '+n);other.append(b)
with zipfile.ZipFile(base/'springer-updates-response') as z:
    need(z.testzip() is None and len(z.infolist())==1,'update transport ZIP')
    need(sha(z.read(z.infolist()[0]))=='44d6fe24868b8f4f3ab128f859c3ed1cc2c538bc87ef0b398025e91c2d82497f','actual update member')
prior=[]
for rel,h in {
    'papers/23074543/reviews/adversarial':'289a69d2eb79c2f907b584bf3eb34e16d5e7e04a98669e4052ac87ccfaf49aa7',
    'verification/cfh-independent-code-audit-sol-20261025':'08df6760943ae91c7fb4f22b5bc6952aea2325bc87ae1b1623a47af5dbdb984f',
    'papers/23442760/reviews/adversarial':'97745de4ecdbbfd9cdd465150871285f42a484668e12f88ea4852b48e33e5518',
    'papers/23395703/reviews/adversarial':'cfa3ba1ab7d58027bca29c4e443afc24bd1e5da956107876c9d91f163fcf2ece',
    'papers/23333353/reviews/adversarial':'3956c3c929eecbddc47477ebf48304a1e966bd79decbfa0ae2505682af17bccf',
    'papers/23416806/reviews/adversarial':'00fe18c47d55ba46442a564f5ff2cea87e7a14281e55c581aa1d359c8e76cfd4',
}.items():
    d=P/rel;sf=d/'FINAL_SEAL.json';need(sha(sf.read_bytes())==h,'prior seal');seal=json.loads(sf.read_text());f=d/seal['manifest']
    need(sha(f.read_bytes())==seal['manifest_sha256'],'prior manifest');fs=json.loads(f.read_text())['files']
    if isinstance(fs,dict):fs=[dict(v,path=k) for k,v in fs.items()]
    owned=[]
    for b in fs:
        got=bind(d/b['path']);need(got['bytes']==b['bytes'] and got['sha256']==b['sha256'],'prior owned evidence');owned.append(got)
    prior.append({'namespace':str(d),'seal':bind(sf),'manifest':bind(f),'owned_files':owned})
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'WHOLE_ORIGINAL_PRIMARY_ACCESS_AND_PRIOR_CUSTODY_VERIFIED',
     'source_authentication':[bind(S/n) for n in auth],'whole_original_bindings':originals,'original_archive_members':members,
     'primary_bindings':primaries,'access_response_bindings':other,'prior_packet_bindings':prior,
     'scope_primary_receipts':[bind(E/n) for n in ['primary-fetch-receipts.json','historical-access-receipts.json']],
     'mathematical_computation_used':False,'supplied_or_historical_code_executed':False,'original_or_prior_object_modified':False}
if sys.argv[1:]!=['--verify-only']:
    with (D/'ORIGINAL_BINDINGS.json').open('x') as f:json.dump(out,f,indent=2);f.write('\n')
print(json.dumps({'originals':len(originals),'archive_members':len(members),'primary_PDFs':len(primaries),
                  'prior_packets':len(prior),'prior_owned_files':sum(len(x['owned_files']) for x in prior),'status':out['status']}))
