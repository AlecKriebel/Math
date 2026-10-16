"""Read-only sealed-package integrity and supplementary replay checks."""
from pathlib import Path
import hashlib,json,stat,zipfile,subprocess,sys,shutil
from datetime import datetime,timezone

OWN=Path(__file__).resolve().parent
PKG=OWN.parent/'publication_package_v2'
EXT=OWN/'private_work'

def pin(p):
    b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def check(p,record):
    assert pin(p)=={'bytes':record['bytes'],'sha256':record['sha256']},str(p)
def dump(name,value):
    (OWN/name).write_text(json.dumps(value,indent=2,sort_keys=True)+'\n')

def main():
    utc=datetime.now(timezone.utc).isoformat()
    top={p.name:pin(p) for p in sorted(PKG.iterdir())}
    assert len(top)==14
    assert sorted(json.loads((PKG/'SAFE_ALLOWLIST.json').read_text())['files'])==list(top)
    seal=json.loads((PKG/'PACKAGE_SEAL.json').read_text())
    assert set(seal['files'])==set(top)-{'PACKAGE_SEAL.json'}
    for name,record in seal['files'].items():check(PKG/name,record)
    for p in PKG.iterdir():assert stat.S_IMODE(p.stat().st_mode)==0o444
    archive=[]
    with zipfile.ZipFile(PKG/'verification-package.zip') as z:
        names=z.namelist();assert len(names)==len(set(names))==78
        assert z.testzip() is None
        for info in z.infolist():
            name=info.filename;rel=Path(name)
            assert not rel.is_absolute() and '..' not in rel.parts and '\\' not in name
            assert not name.endswith('/') and not stat.S_ISLNK(info.external_attr>>16)
            assert not any(s in rel.parts for s in ('private_sources','private_work','.git','__pycache__'))
            data=z.read(name);assert data==(EXT/name).read_bytes()
            data.decode('utf8')
            archive.append({'path':name,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'stored_mode':oct(stat.S_IMODE(info.external_attr>>16)),'format':'JSON parsed' if name.endswith('.json') else 'authored UTF-8 source/prose'})
        inventory=json.loads(z.read('ARCHIVE_INVENTORY.json'))
        assert set(inventory['files'])==set(names)-{'ARCHIVE_INVENTORY.json'}
        for name,record in inventory['files'].items():check(EXT/name,record)
    for name in ('ARCHIVE_INVENTORY.json','LICENSE.txt','README.md','SOURCE_REFERENCES.json','seven_plane_gin.tex','verify_package.py'):
        assert (PKG/name).read_bytes()==(EXT/name).read_bytes()
    manifests=[];allowlists=[]
    for p in sorted(EXT.rglob('*.json')):
        data=json.loads(p.read_text())
        if p.name=='HASH_MANIFEST.json':
            items=data['files'];items=items.items() if isinstance(items,dict) else [(x['path'],x) for x in items]
            items=list(items)
            for name,record in items:check(p.parent/name,record)
            manifests.append({'path':str(p.relative_to(EXT)),'pins_checked':len(items)})
        if p.name=='SAFE_ALLOWLIST.json':
            names=data.get('files',data.get('safe_files'))
            assert set(names)=={x.name for x in p.parent.iterdir() if x.is_file()}
            allowlists.append({'path':str(p.relative_to(EXT)),'exact_file_count':len(names)})
    mathgate=json.loads((EXT/'audits/ROOT_MATHEMATICAL_GATE_01.json').read_text())
    for family,entry in mathgate['three_new_independent_audit_families'].items():
        for name,record in entry['safe_files'].items():check(EXT/'audits'/family/name,record)
    gate=json.loads((EXT/'audits/ROOT_PRIORITY_GATE_01.json').read_text())
    for name,record in gate['audit_safe_files'].items():check(EXT/'audits/priority_audit_01'/name,record)
    old=json.loads((EXT/'audits/ROOT_WHOLE_PACKAGE_REVIEW_01_ACCEPTANCE.json').read_text())
    for name,record in old['review_safe_files'].items():check(EXT/'audits/whole_package_adversary_01'/name,record)
    # All nested executable outputs not included among the five root replays.
    extra=[]
    for folder,script,saved in [('polar_syzygy_audit_01','verify_polar_algebra.py','EXACT_POLAR_CERTIFICATES.json'),('generic_initial_source_audit_01','independent_scalar_and_boundary_check.py','INDEPENDENT_CHECKS.json'),('whole_package_adversary_01','independent_controls.py','INDEPENDENT_CONTROLS.json')]:
        d=EXT/'audits'/folder
        result=subprocess.run([sys.executable,'-E','-S','-B','-P',str(d/script)],cwd=OWN,capture_output=True,text=True,check=True)
        assert json.loads(result.stdout)==json.loads((d/saved).read_text())
        extra.append({'script':folder+'/'+script,'exact_saved_JSON_match':True})
    # Demonstrate standalone __file__ dependency location and hash guard on copies.
    d=OWN/'private_work_tamper'/'audits';(d/'priority_audit_01').mkdir(parents=True,exist_ok=True);(d/'extra_priority_controls_01').mkdir(exist_ok=True)
    src=EXT/'audits/extra_priority_controls_01';dst=d/'extra_priority_controls_01'
    for name in ('check_nine_factor_examples.py','NN_SIMIS_SECTIONAL_CERTIFICATE.json','WALTHER_SECTIONAL_CERTIFICATE.json'):shutil.copyfile(src/name,dst/name)
    dependency=EXT/'audits/priority_audit_01/compare_known_examples.py'
    target=d/'priority_audit_01/compare_known_examples.py';shutil.copyfile(dependency,target)
    cmd=[sys.executable,'-E','-S','-B','-P',str(dst/'check_nine_factor_examples.py'),'--verify']
    good=subprocess.run(cmd,cwd=OWN,capture_output=True,text=True,check=True);assert json.loads(good.stdout)['verified']
    target.write_bytes(target.read_bytes()+b'\n# deliberate private-copy guard control\n')
    bad=subprocess.run(cmd,cwd=OWN,capture_output=True,text=True)
    assert bad.returncode!=0 and 'AssertionError' in bad.stderr and not bad.stdout
    # Before/after extraction bytes and membership are identical.
    assert sorted(str(p.relative_to(EXT)) for p in EXT.rglob('*') if p.is_file())==sorted(x['path'] for x in archive)
    for row in archive:check(EXT/row['path'],row)
    for name,record in top.items():check(PKG/name,record)
    matrix=json.loads((EXT/'audits/priority_audit_01/EVIDENCE_MATRIX.json').read_text())
    queries=json.loads((EXT/'audits/priority_audit_01/QUERY_LOG.json').read_text())
    assert len(matrix['primary_sources'])==36
    assert sum(len(x['queries']) for x in queries['batches'])==120
    dump('REVIEWED_INPUT_PINS.json',{'UTC':utc,'package':'publication_package_v2','files':top,'all_files_mode':'0444','unchanged_after_replay':True})
    dump('ARCHIVE_INSPECTION.json',{'UTC':utc,'entries':archive,'entries_count':len(archive),'payload_hashes':77,'duplicates_or_unsafe_paths':False,'all_UTF8_authored_payload':True,'nested_manifests':manifests,'exact_nested_allowlists':allowlists,'all_Root_gate_safe_file_pins_match':True,'dated_v1_review_not_asserted_to_cover_v2':True,'all_extracted_files_unchanged':True,'source_records':36,'query_records':120})
    dump('SUPPLEMENTARY_REPLAY_CHECKS.json',{'UTC':utc,'three_extra_programs':extra,'standalone_supplement_from_other_cwd_passed':True,'tampered_private_dependency_rejected_before_execution':True,'package_inputs_and_extraction_unchanged':True})
    print(json.dumps({'top_files':14,'archive_entries':78,'payload_hashes':77,'nested_manifests_checked':len(manifests),'extra_replays':len(extra),'supplement_hash_guard_rejects_tamper':True,'inputs_unchanged':True}))
if __name__=='__main__':main()
