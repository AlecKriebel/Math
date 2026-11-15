"""Pure offline custody only: no project imports, subprocess, science, network or writes."""
from pathlib import Path, PurePosixPath
import hashlib
import json
import stat
import zipfile

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent.parent / 'sources'
checks = 0

def need(ok, label):
    global checks
    checks += 1
    if not ok:
        raise RuntimeError(label)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def J(path):
    return json.loads(Path(path).read_text())

def same(a,b):
    if type(a) is not type(b): return False
    if isinstance(a,dict): return list(a)==list(b) and all(same(a[k],b[k]) for k in a)
    if isinstance(a,list): return len(a)==len(b) and all(same(x,y) for x,y in zip(a,b))
    return a==b

def pin(path,n,h):
    need(not path.is_symlink() and path.is_file(), 'nonregular file: '+str(path))
    body=path.read_bytes()
    need(len(body)==n and sha(body)==h, 'byte/hash pin: '+str(path))
    return body

def namespace(root):
    need(root.is_dir() and not root.is_symlink() and root.resolve()==root, 'invalid namespace root')
    files,dirs=[],[]
    for path in root.rglob('*'):
        need(not path.is_symlink(), 'namespace symlink')
        if path.is_file(): files.append(path.relative_to(root).as_posix())
        elif path.is_dir(): dirs.append(path.relative_to(root).as_posix())
        else: raise RuntimeError('nonregular namespace member')
    return sorted(files),sorted(dirs)

def main():
    m=J(HERE/'INPUT_MANIFEST.json')
    need(sha((SOURCE/'SOURCE_READY.json').read_bytes())=='daf4295ead3b1f6c626bef12d6bb1f6796688aee7a56f04b5abd4f80c5d073f9','READY authority')
    need(sha((SOURCE/'SOURCE_READY_SEAL.json').read_bytes())=='47b3874516ef61b804e27e8980c013a6cae36edc9934c273938c73dcdff3ce24','source seal authority')
    for row in m['files']: pin(Path(row['path']),row['bytes'],row['SHA256'])
    fs,ds=namespace(SOURCE)
    need(fs==sorted(r['relative'] for r in m['files']),'complete source namespace including all nested terminal names')
    need(ds==m['exact_relative_directories'],'complete source directory namespace')
    isolated=HERE/'native-isolated';im=J(HERE/'ISOLATED_INPUT_MANIFEST.json')
    for row in im['files']:
        body=pin(isolated/row['isolated_relative_path'],row['bytes'],row['SHA256'])
        need(body==Path(row['source_path']).read_bytes(),'whole isolated/original equality')
    fi,di=namespace(isolated)
    need(fi==fs and di==ds,'complete unchanged isolated source namespace')
    objects=J(HERE/'NATIVE_OBJECT_READ.json')['whole_original_object_copies']
    for row in objects:
        body=pin(Path(row['copy_path']),row['bytes'],row['SHA256'])
        need(body==Path(row['source_path']).read_bytes(),'raw native object original bytes')
        need(same(json.loads(body),J(row['source_path'])),'whole native object types/key/list order/null/history')
    ready=J(SOURCE/'SOURCE_READY.json');archive=J(SOURCE/'ARCHIVE_CUSTODY.json')
    need(len(archive['containers'])==4 and len(archive['regular_payload_occurrences'])==243,'complete recursive archive counts')
    occurrence_count=0;expanded=0
    for container in archive['containers']:
        inp=Path(container['input_path']);pin(inp,container['input_bytes'],container['input_SHA256'])
        with zipfile.ZipFile(inp) as z:
            infos=z.infolist();members=container['members']
            need(len(infos)==len(members),'complete central member list')
            need([i.filename for i in infos]==[r['original_member_name'] for r in members],'original central/member order')
            need(len({i.filename.casefold() for i in infos})==len(infos),'no archive duplicate/case names')
            need(z.comment.hex()==container['original_archive_comment_hex'],'whole archive comment')
            for ordinal,(info,row) in enumerate(zip(infos,members)):
                path=PurePosixPath(info.filename)
                need(not path.is_absolute() and '..' not in path.parts and not info.is_dir(),'safe regular payload name')
                need(stat.S_ISREG(info.external_attr>>16),'regular archive native mode')
                body=z.read(info)
                need(body==pin(Path(row['extracted_path']),row['bytes'],row['SHA256']),'whole extracted payload/CRC equality')
                need(row['ordinal_zero_based']==ordinal and row['container_id']==container['container_id'],'payload occurrence identity')
                observed=[format(info.CRC,'08x'),info.compress_size,info.compress_type,info.external_attr,info.create_system,info.flag_bits,list(info.date_time)]
                declared=[row[k] for k in ['CRC32','compressed_bytes','compression_method','native_external_attr','native_create_system','native_flags','native_date_time']]
                need(same(observed,declared),'all native payload metadata fields')
                occurrence_count+=1;expanded+=len(body)
    need(occurrence_count==243 and expanded==1256656,'whole expanded payload occurrences/bytes')
    need(ready['embedded_PDFs']==[],'no invented embedded reader')
    native=J(SOURCE/'record.response.body');latest=J(SOURCE/'latest.response.body.redirect-01')
    need(same(native,latest),'whole record/latest typed identity')
    need((SOURCE/'record.response.body').read_bytes()==(SOURCE/'latest.response.body.redirect-01').read_bytes(),'record/latest original raw equality')
    versions=J(SOURCE/'versions-page001.response.body');expected=dict(native);expected['swh']=None
    need(len(versions['hits']['hits'])==1 and same(versions['hits']['hits'][0],expected),'whole version hit and original swh null distinction')
    need(versions['hits']['total']==1 and 'next' not in versions['links'],'one exhaustive version list')
    files=J(SOURCE/'files.response.body')
    need(type(files['entries']) is list and files['order']==[] and files['default_preview'] is None,'native files list/empty/null shapes')
    need(len(files['entries'])==len(native['files'])==len(ready['all_native_assets_in_original_order'])==2,'complete native asset cardinality')
    for entry,api,a in zip(files['entries'],native['files'],ready['all_native_assets_in_original_order']):
        need(same(api,a['original_api_file_object']) and same(entry,a['whole_original_native_files_entry']),'whole original native asset objects')
        body=pin(Path(a['path']),a['bytes'],a['SHA256'])
        need(body==Path(a['transport_body_path']).read_bytes(),'whole asset/transport raw body')
        need(hashlib.md5(body).hexdigest()==api['checksum'].split(':')[1],'native MD5')
    need([a['key'] for a in native['files']]==['source-and-verification.zip','paper.pdf'],'original native ZIP/PDF order')
    need(ready['printed_date'] is None and ready['printed_version'] is None and ready['mathematical_PDF_TeX_or_pixels_read'] is False,'source historical unread/null flags preserved')
    for seal_name,manifest_name in [('INITIAL_SEAL.json','INITIAL_OWNED_MANIFEST.json')]:
        seal=J(HERE/seal_name)
        need(sha((HERE/manifest_name).read_bytes())==seal['INITIAL_OWNED_MANIFEST_SHA256'],'initial seal manifest')
        for row in J(HERE/manifest_name)['files']:pin(HERE/row['path'],row['bytes'],row['SHA256'])
    for row in J(HERE/'INDEPENDENT_PROOF_TEST_FREEZE.json')['files']:pin(HERE/row['path'],row['bytes'],row['SHA256'])
    replay=J(HERE/'NATIVE_REPLAY.json')
    for row in replay['runs']:
        actual=row['whole_stdout'];err=row['whole_stderr'];exp=row['original_expected']
        body=pin(Path(actual['path']),actual['bytes'],actual['SHA256'])
        original=pin(Path(exp['path']),exp['bytes'],exp['SHA256'])
        need(body==original and same(json.loads(body),exp['whole_literal_object']) and same(json.loads(body),json.loads(original)),'whole actual/expected stdout bytes and typed object')
        need(pin(Path(err['path']),err['bytes'],err['SHA256'])==b'' and row['exit_code']==0,'whole native stderr/exit')
    need((HERE/'NATIVE_NORMAL.stdout.json').read_bytes()==(HERE/'NATIVE_OPTIMIZED.stdout.json').read_bytes(),'whole actual normal/optimized output equality')
    ledger=J(HERE/'PRIMARY_BODY_READ_LEDGER.json')
    for row in ledger['actual_body_files']:pin(Path(row['path']),row['bytes'],row['SHA256'])
    if (HERE/'VERDICT.json').exists():
        verdict=J(HERE/'VERDICT.json')
        need(same(verdict['whole_original_SOURCE_READY'],ready),'entire original READY embedded in literal custom verdict')
        need(verdict['canonical_url'] is None and verdict['AA'] is None and verdict['publication_authority'] is False,'publication authority remains unassigned')
    sealed=False
    if (HERE/'OWNED_MANIFEST.json').exists():
        owned=J(HERE/'OWNED_MANIFEST.json')
        for row in owned['files']:pin(HERE/row['path'],row['bytes'],row['SHA256'])
        f,d=namespace(HERE)
        need(set(f)=={r['path'] for r in owned['files']}|{'OWNED_MANIFEST.json','SEAL.json'},'entire own namespace; exact root controls only')
        need(d==owned['exact_relative_directories'],'entire own directory namespace')
        need(sha((HERE/'OWNED_MANIFEST.json').read_bytes())==J(HERE/'SEAL.json')['OWNED_MANIFEST_SHA256'],'final owned manifest seal')
        sealed=True
    print(json.dumps({'status':'PASS_PURE_CUSTODY_NO_SCIENTIFIC_REPLAY','checks':checks,'source_files':len(fs),'isolated_files':len(fi),
                      'whole_native_objects':len(objects),'archive_containers':4,'regular_payload_occurrences':occurrence_count,
                      'expanded_bytes':expanded,'native_replay_modes_checked':2,'own_final_seal_checked':sealed,
                      'project_imports':False,'subprocess':False,'scientific_execution':False,'network':False,'writes':False},indent=2))

if __name__=='__main__':main()
