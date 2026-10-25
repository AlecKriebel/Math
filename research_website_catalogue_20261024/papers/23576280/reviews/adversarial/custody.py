"""Read-only original/primary/prior custody. Default creates a fresh own receipt;
--verify-only writes nothing. No supplied code, network, extraction or repacking.
"""
from pathlib import Path,PurePosixPath
import datetime,hashlib,json,stat,sys,zipfile
if sys.argv[1:] not in ([],['--verify-only']):raise SystemExit('usage: custody.py [--verify-only]')
D=Path(__file__).resolve().parent;P=D.parents[3];S=P/'papers/23576280/sources'


def sha(b):return hashlib.sha256(b).hexdigest()


def bind(f):
    b=f.read_bytes();return {'path':str(f),'bytes':len(b),'sha256':sha(b)}


def need(ok,msg):
    if not ok:raise RuntimeError(msg)


auth={'SOURCE_READY.json':'f72606f1c0ed7411948e520d534ed397dff4b49731812406369ecbc9001d7e1b',
      'SOURCE_READY_MANIFEST.json':'ba0443c2a5f8001b9916a217c113bd38247695093c12b8cead3aef421c9ae388',
      'SOURCE_READY_SEAL.json':'78a83dd556f77e4b6c003fa16465b64d3a7d8079f1d4d85f450683930b86e56b'}
for n,h in auth.items():need(sha((S/n).read_bytes())==h,'source authentication '+n)
manifest=json.loads((S/'SOURCE_READY_MANIFEST.json').read_text());originals=[]
for b in manifest['files']:
    pp=PurePosixPath(b['path']);need(not pp.is_absolute() and '..' not in pp.parts and str(pp)==b['path'],'original path')
    got=bind(S/pp);need(got['bytes']==b['bytes'] and got['sha256']==b['sha256'],'original bytes '+str(pp));originals.append(got)
need(len(originals)==manifest['file_count']==22,'original count')
ready=json.loads((S/'SOURCE_READY.json').read_text());record=json.loads((S/'record.raw.json').read_text())
latest=json.loads((S/'latest.raw.json').read_text());versions=json.loads((S/'versions.raw.json').read_text())
need(record['id']==latest['id']==23576280 and versions['hits']['total']==1
     and record['metadata']['version']=='1.0.0' and record['metadata']['publication_date']=='2026-10-22'
     and record['created']=='2026-10-22T19:48:22.876250+00:00','actual edition fields')
need(len(record['files'])==len(ready['all_assets'])==2,'two actual file objects')
for a in ready['all_assets']:
    o=a['original_api_file_object'];b=(S/o['key']).read_bytes()
    need(o in record['files'] and o in latest['files'] and len(b)==o['size']==a['bytes'] and sha(b)==a['sha256']
         and 'md5:'+hashlib.md5(b).hexdigest()==o['checksum'],'complete actual public object')
archive=json.loads((S/'archive-members.json').read_text());expected={b['member']:b for b in archive['files']};members=[]
need(len(expected)==12 and not archive['nested_archives'],'flat original archive')
with zipfile.ZipFile(S/'initial-odd-ear-prefix-source-and-verification.zip') as z:
    need(z.testzip() is None,'all original CRCs');seen=set()
    for info in z.infolist():
        pp=PurePosixPath(info.filename)
        need(not info.is_dir() and not pp.is_absolute() and '..' not in pp.parts and str(pp)==info.filename
             and info.filename not in seen and stat.S_IFMT(info.external_attr>>16) in (0,stat.S_IFREG),'safe regular member')
        seen.add(info.filename);b=expected[info.filename];raw=z.read(info);f=S/b['path']
        need(f.resolve().is_relative_to(S.resolve()) and f.read_bytes()==raw and len(raw)==b['bytes']
             and sha(raw)==b['sha256'] and format(info.CRC,'08x')==b['CRC32'],'member bytes')
        members.append({'member':info.filename,'path':str(f),'bytes':len(raw),'sha256':sha(raw),'CRC32':format(info.CRC,'08x')})
need(len(members)==12 and sum(b['bytes'] for b in members)==184923,'complete archive')
E=P/'papers/23576280/reviews/scope';base=E/'cache/primary';primaries=[]
for n,h in {
    'sebo-owr2014.pdf':'2a9385d628b32b5ecb6ae977ef8285bb12e12300cc9d5f94f82803b969425647',
    'benchetrit-sebo-v1.pdf':'b31f829799c84e6dd10815dbfd05260d6c285aadb706d9665a985b01f3cf2292',
    'sharifov2010.pdf':'6c605ddf766397d2b5cb8513c82268115fd7e1fd547407c357ccfb5fb8c5cb58',
    'weighted-connected-v1.pdf':'efc87fe4d5a367d8765c8f5ceff7e7cc9123ccec881ede9ba726ae0039df3253',
    'havet-nisse2019.pdf':'2776400aeb27c9ecdcbe01513535ffd916c4bd24a0120fd597a1f6a6957a7be6',
    'bai-berczi-nalam-v1.pdf':'718124178130bb7e53a0ffde3917ba45476bb8dd7382a78c3a259687b77979a5',
    'ferudun23592264.pdf':'91e18175e559c2362ff357f29c23bed98971c5472b47a8b300187353e7755820',
}.items():
    f=base/n;b=bind(f);need(b['sha256']==h and f.read_bytes().startswith(b'%PDF-'),'actual primary '+n);primaries.append(b)
f=P/'papers/23181280/reviews/scope/cache/primary/karp1972.pdf';b=bind(f)
need(b['sha256']=='778c8b3507620a68154bc74b29810e0de6d2c4dd7ee5d24b84c7e7ba61404b81','unchanged actual Karp facsimile');primaries.append(b)
other=[bind(base/n) for n in ['benchetrit2016-exposition.html','gomes-journal-crossref.raw.json','gomes-journal-landing.html','ferudun23592264-record.raw.json']]
need(other[0]['sha256']=='3e7dcd308339efb9c944b618e616257831110bf95eada732359ad3b58558cbef','author exposition custody')
foreign=json.loads((base/'ferudun23592264-record.raw.json').read_text());foreignbytes=(base/'ferudun23592264.pdf').read_bytes()
need(foreign['id']==23592264 and foreign['metadata']['version']=='1.0'
     and foreign['metadata']['publication_date']=='2026-10-23'
     and foreign['created']=='2026-10-23T10:08:01.525956+00:00','actual contemporary record')
fo=next(o for o in foreign['files'] if o['key']=='OWR-13353-012.pdf')
need(fo['size']==len(foreignbytes)==72386 and fo['checksum']=='md5:'+hashlib.md5(foreignbytes).hexdigest(),'actual contemporary PDF file object')
cross=json.loads((base/'gomes-journal-crossref.raw.json').read_text())['message']
need(cross['DOI']=='10.1016/j.tcs.2025.115149' and cross['volume']=='1036' and cross['article-number']=='115149','journal metadata distinct from body')
prior=[]
for rel,h in {
    'papers/23074543/reviews/adversarial':'289a69d2eb79c2f907b584bf3eb34e16d5e7e04a98669e4052ac87ccfaf49aa7',
    'verification/cfh-independent-code-audit-sol-20261025':'08df6760943ae91c7fb4f22b5bc6952aea2325bc87ae1b1623a47af5dbdb984f',
    'papers/23442760/reviews/adversarial':'97745de4ecdbbfd9cdd465150871285f42a484668e12f88ea4852b48e33e5518',
    'papers/23395703/reviews/adversarial':'cfa3ba1ab7d58027bca29c4e443afc24bd1e5da956107876c9d91f163fcf2ece',
    'papers/23333353/reviews/adversarial':'3956c3c929eecbddc47477ebf48304a1e966bd79decbfa0ae2505682af17bccf',
    'papers/23416806/reviews/adversarial':'00fe18c47d55ba46442a564f5ff2cea87e7a14281e55c581aa1d359c8e76cfd4',
    'papers/23441617/reviews/adversarial':'04d5755dcf9bda962894efc17c6768f4b5dfb87ad6cc4aa7f7898887b295bc48',
}.items():
    d=P/rel;sf=d/'FINAL_SEAL.json';need(sha(sf.read_bytes())==h,'prior seal');j=json.loads(sf.read_text());mf=d/j['manifest']
    need(sha(mf.read_bytes())==j['manifest_sha256'],'prior manifest');fs=json.loads(mf.read_text())['files']
    if isinstance(fs,dict):fs=[dict(v,path=k) for k,v in fs.items()]
    owned=[]
    for x in fs:
        got=bind(d/x['path']);need(got['bytes']==x['bytes'] and got['sha256']==x['sha256'],'prior owned bytes');owned.append(got)
    prior.append({'namespace':str(d),'seal':bind(sf),'manifest':bind(mf),'owned_files':owned})
receipts=[bind(E/n) for n in ['primary-fetch-receipts.json','additional-primary-access-receipts.json','additional-primary-initial-receipt.json','additional-primary-PDF-receipt.json','reused-primary-custody.json']]
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'WHOLE_ORIGINAL_PRIMARY_AND_PRIOR_CUSTODY_VERIFIED',
     'source_authentication':[bind(S/n) for n in auth],'whole_original_bindings':originals,'original_archive_members':members,
     'primary_bindings':primaries,'additional_access_metadata_bindings':other,'scope_primary_receipts':receipts,
     'prior_packet_bindings':prior,'supplied_code_executed':False,'source_or_prior_objects_modified':False}
if sys.argv[1:]!=['--verify-only']:
    with (D/'ORIGINAL_BINDINGS.json').open('x') as f:json.dump(out,f,indent=2);f.write('\n')
print(json.dumps({'originals':len(originals),'ZIP_members':len(members),'actual_primary_PDFs':len(primaries),
                  'prior_packets':len(prior),'prior_owned_files':sum(len(x['owned_files']) for x in prior),'status':out['status']}))
