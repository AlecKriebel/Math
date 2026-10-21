"""Exercise authenticated archive/integrity routines with new owned hostile cases."""
from pathlib import Path
import copy,datetime,hashlib,io,json,os,shutil,sys,tarfile

HERE=Path(__file__).resolve().parent.parent
PACK=HERE/'fixtures/replay_packet'
PIN='cff4f5e102973803175b304b3cd472dd6f28d3843eac7bbacac809b1a9bde7de'
MPIN='0bb884f5c4ae98204a5455e78c5c869905457a21021e86040c58e8e2f01a3ab4'
BPIN='128bfd14af0273eb4bd850ae95be8a0cbe908795c0032c003894809d733575b5'

def sha(raw):return hashlib.sha256(raw).hexdigest()
def require(ok,msg):
    if not ok:raise RuntimeError(msg)

def main():
    raw=(PACK/'verify_publication.py').read_bytes()
    require(sha(raw)==PIN,'verifier independent pin')
    namespace={'__name__':'authenticated_archive_test_module'}
    exec(compile(raw,'<externally-authenticated-verifier>','exec'),namespace)
    snapshot,parsed=namespace['integrity'](PACK,MPIN,BPIN)
    rows=[]
    def outcome(label,operation,should_accept):
        try:operation()
        except (ValueError,OSError,TypeError,KeyError,tarfile.TarError) as e:
            accepted=False;error=type(e).__name__+': '+str(e)
        else:accepted=True;error=None
        rows.append(dict(label=label,accepted=accepted,expected_accept=should_accept,error=error))
        require(accepted==should_accept,'unexpected archive/binding result: '+label)
    def archive(kind):
        buffer=io.BytesIO()
        global_pax={'comment':'owned audit metadata'} if kind=='global_pax' else None
        with tarfile.open(fileobj=buffer,mode='w:gz',format=tarfile.PAX_FORMAT if 'pax' in kind else tarfile.USTAR_FORMAT,
                          pax_headers=global_pax) as package:
            for name in ['public','external']:
                if kind=='missing_directory' and name=='external':continue
                info=tarfile.TarInfo(name);info.type=tarfile.DIRTYPE;info.mode=0o555
                if kind=='directory_has_payload' and name=='external':info.size=1
                package.addfile(info,io.BytesIO(b'x') if info.size else None)
            for name in sorted(namespace['AUTHOR']):
                data=snapshot['author/'+name];info=tarfile.TarInfo(name);info.size=len(data);info.mode=0o444
                if name=='public/REPORT.md':
                    if kind=='parent_traversal':info.name='../REPORT.md'
                    elif kind=='absolute':info.name='/public/REPORT.md'
                    elif kind=='double_separator':info.name='public//REPORT.md'
                    elif kind=='dot_segment':info.name='public/./REPORT.md'
                    elif kind=='backslash':info.name='public\\REPORT.md'
                    elif kind=='symlink':info.type=tarfile.SYMTYPE;info.linkname='../escape';info.size=0
                    elif kind=='hardlink':info.type=tarfile.LNKTYPE;info.linkname='public/README.md';info.size=0
                    elif kind=='fifo':info.type=tarfile.FIFOTYPE;info.size=0
                    elif kind=='character_device':info.type=tarfile.CHRTYPE;info.size=0
                    elif kind=='local_pax':info.pax_headers={'comment':'owned extra metadata'}
                    elif kind=='changed_body':data=b'X'+data[1:]
                    elif kind=='mode_change':info.mode=0o4777
                package.addfile(info,io.BytesIO(data) if info.isreg() else None)
            if kind=='duplicate_directory':
                info=tarfile.TarInfo('public');info.type=tarfile.DIRTYPE;package.addfile(info)
            if kind=='duplicate_file':
                info=tarfile.TarInfo('public/REPORT.md');info.size=1;package.addfile(info,io.BytesIO(b'x'))
        data=buffer.getvalue()
        if kind=='trailing_nonarchive_bytes':data+=b'owned trailing bytes ignored by tar parser'
        return data
    kinds=['baseline','missing_directory','directory_has_payload','parent_traversal','absolute','double_separator',
           'dot_segment','backslash','symlink','hardlink','fifo','character_device','local_pax','global_pax',
           'changed_body','duplicate_directory','duplicate_file','mode_change','trailing_nonarchive_bytes']
    for kind in kinds:
        data=archive(kind)
        outcome('archive_helper:'+kind,lambda data=data:namespace['archive'](data,snapshot,'author/',namespace['AUTHOR']),
                kind in ['baseline','mode_change','trailing_nonarchive_bytes'])
    for label,data in [('duplicate_nested',b'{"a":{"b":1,"b":2}}'),('nan',b'{"a":NaN}'),
                       ('infinity',b'{"a":Infinity}'),('float_overflow',b'{"a":1e9999}')]:
        outcome('strict_parser:'+label,lambda data=data:namespace['parse'](data),False)
    # Exercise accepted-evidence pins AFTER recomputing a self-consistent
    # mutable publication manifest and supplying its new hash to integrity.
    work=HERE/'fixtures'/('binding_mode_'+str(sys.flags.optimize));work.mkdir()
    def repin(target):
        m=json.loads((target/'PUBLICATION_MANIFEST.json').read_bytes())
        for row in m['files']:
            b=(target/row['path']).read_bytes();row.update(bytes=len(b),sha256=sha(b))
        b=(json.dumps(m,indent=2)+'\n').encode();(target/'PUBLICATION_MANIFEST.json').write_bytes(b)
        return sha(b)
    for label in ['report_repin','archive_mode_repin','archive_trailing_repin','audit_receipt_repin',
                  'disk_mode_only','regular_hardlink_alias','wrapper_doc_repin']:
        target=work/label;shutil.copytree(PACK,target)
        if label=='report_repin':
            p=target/'author/public/REPORT.md';p.write_bytes(b'X'+p.read_bytes()[1:])
        elif label=='archive_mode_repin':(target/'expansive_group_2616_frozen.tar.gz').write_bytes(archive('mode_change'))
        elif label=='archive_trailing_repin':(target/'expansive_group_2616_frozen.tar.gz').write_bytes(archive('trailing_nonarchive_bytes'))
        elif label=='audit_receipt_repin':(target/'audit_2/INDEPENDENT_RESULTS.json').write_bytes(b'{}\n')
        elif label=='disk_mode_only':(target/'author/public/REPORT.md').chmod(0o777)
        elif label=='regular_hardlink_alias':
            p=target/'audit_2/AUTHOR_HARNESS_RERUN.json';p.unlink();os.link(target/'author/external/TEST_RESULTS.json',p)
        elif label=='wrapper_doc_repin':
            p=target/'README.md';p.write_bytes(p.read_bytes()+b'\nOwned audit metadata.\n')
        mpin=repin(target)
        outcome('integrity:'+label,lambda target=target,mpin=mpin:namespace['integrity'](target,mpin,BPIN),
                label in ['disk_mode_only','regular_hardlink_alias','wrapper_doc_repin'])
        if label=='wrapper_doc_repin':
            # The actual outer bootstrap pins MPIN; passing the historical
            # external pin must reject even otherwise unpinned wrapper docs.
            outcome('integrity:wrapper_doc_original_pin',lambda:namespace['integrity'](target,MPIN,BPIN),False)
    # No extraction ever occurs; these archive modes cannot grant permissions.
    result=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),optimization=sys.flags.optimize,
                actual_authenticated_functions=True,archive_extracted=False,observations=rows,
                exact_archive_hash_still_required_by_integrity=True,
                scope='Fixed external bootstrap anchor remains essential. Helpers accept arbitrary regular-file modes/hardlink aliases; low-level tar reader ignores trailing bytes and does not enforce modes. Full accepted archive bytes are independently pinned.')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
