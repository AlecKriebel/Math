"""Scope-only identity/reader/abstract evidence; never runs submitted programs."""
from pathlib import Path
import datetime, hashlib, io, json, re, stat, tarfile, zipfile

HERE = Path(__file__).resolve().parent
BASE = HERE.parent.parent
SOURCE = BASE / 'sources'
sha = lambda b: hashlib.sha256(b).hexdigest()
now = lambda: datetime.datetime.now(datetime.timezone.utc).isoformat()
def save(name, value):
    (HERE/name).write_text(json.dumps(value, indent=2, ensure_ascii=False)+'\n')

receipt = json.loads((SOURCE/'receipt.json').read_text())
record = json.loads((SOURCE/'record.json').read_text())
queue_file = BASE.parent.parent/'reconciliation/queue.json'
queue = json.loads(queue_file.read_text())
entry = next(r for r in queue['queue'] if str(r['record_id']) == '23328912')
save('queue_identity.json', {'queue_sha256':sha(queue_file.read_bytes()), 'entry':entry})
expected = {r['filename']:(r['expected_bytes'],r['expected_md5']) for r in entry['sources']}
expected.update({r['filename']:(r['filesize'],r['checksum'].removeprefix('md5:')) for r in entry['supporting_files']})
rows=[]
for r in receipt['files']:
    data=(SOURCE/r['name']).read_bytes()
    api=next(x for x in record['files'] if x['key']==r['name'])
    md5=hashlib.md5(data).hexdigest()
    ok=(len(data)==r['bytes']==api['size']==expected[r['name']][0] and sha(data)==r['sha256'] and md5==r['md5']==api['checksum'].removeprefix('md5:')==expected[r['name']][1])
    if not ok: raise ValueError('Asset identity mismatch: '+r['name'])
    rows.append({'path':r['name'],'bytes':len(data),'md5':md5,'sha256':sha(data),'api_and_queue_match':True})
if sha((SOURCE/'record.json').read_bytes())!=receipt['record_sha256']: raise ValueError('Metadata changed')

members=[]
for a in receipt['archives']:
    with zipfile.ZipFile(SOURCE/a['name']) as z:
        listed={m['member']:m for m in a['members']}
        names=set()
        for info in z.infolist():
            p=Path(info.filename)
            if p.is_absolute() or '..' in p.parts or stat.S_ISLNK(info.external_attr>>16): raise ValueError('Unsafe member')
            if info.is_dir(): continue
            if info.filename in names:raise ValueError('Duplicate member')
            names.add(info.filename)
            data=z.read(info)
            extracted=SOURCE/a['extraction_root']/info.filename
            if data!=extracted.read_bytes() or sha(data)!=listed[info.filename]['sha256']:raise ValueError('Extracted mismatch')
            ispdf=data.lstrip().startswith(b'%PDF-')
            iszip=zipfile.is_zipfile(io.BytesIO(data))
            istar=False
            try:
                with tarfile.open(fileobj=io.BytesIO(data),mode='r:*') as t: istar=True
            except tarfile.ReadError: pass
            members.append({'archive':a['name'],'member':info.filename,'extracted_path':str(extracted.relative_to(BASE)), 'bytes':len(data),'sha256':sha(data),'pdf_magic':ispdf,'nested_zip':iszip,'nested_tar':istar,'matches_original_member':True})
        if names!=set(listed):raise ValueError('Archive inventory mismatch')
if any(r['pdf_magic'] or r['nested_zip'] or r['nested_tar'] for r in members):raise ValueError('Additional reader/archive requires review')
save('archive_reader_scan.json',{'created_utc':now(),'regular_members':len(members),'additional_reader_pdfs':[],'nested_archives':[],'member_byte_comparison':True,'members':members})

texpath=SOURCE/'published-source/aim_5_2_source/preprint.tex'
tex=texpath.read_text()
abstract=re.search(r'\\begin\{abstract\}\s*(.*?)\s*\\end\{abstract\}',tex,re.S).group(1)
(HERE/'abstract_original.tex').write_text(abstract+'\n')
plain=abstract.replace('$','').replace('\\CAT(0)','CAT(0)').replace('\\mapsto','→').replace('~',' ')
plain=' '.join(plain.split())
(HERE/'abstract_original.txt').write_text(plain+'\n')
save('abstract_receipt.json',{'source_tex':str(texpath.relative_to(BASE)), 'source_tex_sha256':sha(texpath.read_bytes()),'main_pdf_sha256':rows[0]['sha256'],'main_pdf_page':1,'complete_original_abstract':True,'normalizations':['TeX math delimiters removed','CAT macro expanded','mapsto rendered as arrow','nonbreaking space and whitespace normalized'],'word_count_whitespace':len(plain.split()),'tex_sha256':sha((HERE/'abstract_original.tex').read_bytes()),'plain_sha256':sha((HERE/'abstract_original.txt').read_bytes())})
readers=json.loads((HERE/'reader_document_map.json').read_text())
readers['all_reader_pdfs_read']=True
readers['archive_reader_scan']='archive_reader_scan.json'
readers['additional_reader_pdfs']=[]
readers['documents'][0].update({'pages_read':[1,2,3,4,5,6],'rendered_pages_visually_inspected':[1,2,3,4,5,6],'scope_only':True})
save('reader_document_map.json',readers)
save('final_integrity.json',{'checked_utc':now(),'record_sha256':receipt['record_sha256'],'asset_count':len(rows),'archive_member_count':len(members),'all_public_files_match_fresh_api_and_frozen_queue':True,'all_extracted_members_match_original_zips':True,'submitted_programs_executed':False,'originals_unchanged':True,'assets':rows})
print(json.dumps({'assets':len(rows),'members':len(members),'reader_pdfs':1,'pages':6,'abstract_words':len(plain.split()),'submitted_programs_executed':False},indent=2))
