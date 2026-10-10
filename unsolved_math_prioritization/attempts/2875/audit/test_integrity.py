"""Adversarial static checks. No mathematical theorem is tested by this program."""
import argparse
import copy
import io
import json
import stat
import warnings
import zipfile
from pathlib import Path
import verify_package as v
import verify_source_pins as sources


def blob(obj):
    return (json.dumps(obj,indent=2,sort_keys=True)+'\n').encode()

def archive(rows):
    out = io.BytesIO()
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', UserWarning)
        with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED) as z:
            for name, data, mode in rows:
                i = zipfile.ZipInfo(name,date_time=(2026,10,6,0,0,0)); i.create_system=3
                i.external_attr=mode<<16; i.compress_type=zipfile.ZIP_DEFLATED
                z.writestr(i,data)
    return out.getvalue()

def test(root):
    files = {p.name:p.read_bytes() for p in root.iterdir() if p.is_file()}
    v.check_core(files)
    rejected = []
    def reject(name, fn):
        try:
            fn()
        except (ValueError,KeyError,TypeError,UnicodeDecodeError,zipfile.BadZipFile):
            rejected.append(name)
            return
        raise RuntimeError('accepted negative control: '+name)
    def changed(name, data):
        out = dict(files); out[name] = data; return out
    for name in v.PINS:
        reject('corrupt_'+name, lambda name=name: v.check_core(changed(name,files[name]+b'x')))
        out=dict(files);del out[name]
        reject('missing_'+name,lambda out=out:v.check_core(out))
    acceptance = v.parse(files['ACCEPTANCE.json'])
    for field, value in [('decision','PENDING'),('status','solved'),('turns_used',5),('full_problem_solved',True),
        ('full_problem_refuted',True),('novelty_claim',True),('worldwide_open_status_certified',True),
        ('original_preserved',False),('publication_performed',True),('mathematical_proof_machine_certified',True),
        ('analytical_mathematical_audit_completed',False),('accepted_external_manifest_sha256','0'*64)]:
        item=copy.deepcopy(acceptance);item[field]=value
        reject('acceptance_'+field,lambda item=item:v.check_core(changed('ACCEPTANCE.json',blob(item))))
    require_type=copy.deepcopy(acceptance);require_type['turns_used']=4.0
    reject('acceptance_wrong_numeric_type',lambda:v.check_core(changed('ACCEPTANCE.json',blob(require_type))))
    source=v.parse(files['SOURCE_PIN_RESULTS.json'])
    for label,mutate in [
        ('pending',lambda x:x.update(status='PENDING')),
        ('false_pin',lambda x:x['source_checks'][0].update(matches_expected=False)),
        ('wrong_pdf_hash',lambda x:x['source_checks'][-1].update(sha256='0'*64)),
        ('wrong_pair',lambda x:x.update(complete_pair_sha256='0'*64)),
        ('missing_source',lambda x:x['source_checks'].pop()),
        ('wrong_report_claim',lambda x:x.update(associated_report_empty=False))]:
        item=copy.deepcopy(source);mutate(item)
        reject('source_evidence_'+label,lambda item=item:v.check_core(changed('SOURCE_PIN_RESULTS.json',blob(item))))
    inspection=v.parse(files['SOURCE_INSPECTION.json']);inspection['primary_sources'][0]['pdf_readable']=False
    reject('false_pdf_inspection_evidence',lambda:v.check_core(changed('SOURCE_INSPECTION.json',blob(inspection))))
    patch=v.parse(files['PATCH_REPLAY.json']);patch['status']='PENDING'
    reject('pending_patch_replay',lambda:v.check_core(changed('PATCH_REPLAY.json',blob(patch))))
    reject('duplicate_json_key',lambda:v.parse(b'{"a":1,"a":2}'))
    reject('private_material_marker',lambda:v.check_core(changed('INDEPENDENT_AUDIT.md',b'/work'+b'space/private')))
    mode=stat.S_IFREG|0o644
    with zipfile.ZipFile(io.BytesIO(files['AUTHOR_SAFE_FREEZE.zip'])) as z:
        rows=[(n,z.read(n),mode) for n in v.AUTHOR_NAMES]
    cases={
        'missing_member':rows[:-1],
        'extra_member':rows+[('extra.txt',b'x',mode)],
        'duplicate_member':rows+[rows[0]],
        'reordered_members':list(reversed(rows)),
        'symlink_member':[(rows[0][0],rows[0][1],stat.S_IFLNK|0o644)]+rows[1:],
        'executable_member':[(rows[0][0],rows[0][1],stat.S_IFREG|0o755)]+rows[1:],
        'traversal_member':[('../README.md',rows[0][1],mode)]+rows[1:],
    }
    for label, vals in cases.items():
        reject('structural_'+label,lambda vals=vals:v.unpack(archive(vals),v.AUTHOR_NAMES))
    # Same byte counts with deliberately false bytes exercise SHA checks, not merely size tests.
    for label,(size,_) in sources.PINS.items():
        reject('source_same_size_corruption_'+label,lambda label=label,size=size:sources.check_pin(label,b'\0'*size))
    # Build an adversarial envelope fixture around the actual pinned core. Synthetic reports
    # below exist only for this software test and never count as final replay evidence.
    fixture=dict(files)
    fixture['ARTIFACT_TEST_RESULTS.json']=blob({'status':'PASS'})
    fixture['REPLAY_RESULTS.json']=blob({'status':'PASS','normal_optimized_source_results_equal':True,'patch_replay_pass':True})
    v.require(all(n in fixture for n in v.NAMES),'test script/core inventory')
    def envelope(items):
        ab=archive([(n,items[n],mode) for n in v.NAMES])
        mb=blob({'archive':{'bytes':len(ab),'sha256':v.sha(ab)},'files':[{'path':n,'bytes':len(items[n]),'sha256':v.sha(items[n])} for n in v.NAMES],
            'decision':v.DECISION,'problem_id':2875})
        return ab,mb,v.sha(mb)
    ab,mb,pin=envelope(fixture);v.verify_archive(ab,mb,pin)
    reject('outer_manifest_corruption',lambda:v.verify_archive(ab,mb+b' ',pin))
    reject('outer_archive_corruption',lambda:v.verify_archive(ab+b'x',mb,pin))
    reject('outer_wrong_trust_pin',lambda:v.verify_archive(ab,mb,'0'*64))
    for label,target in [('pending_test_report','ARTIFACT_TEST_RESULTS.json'),('pending_replay_report','REPLAY_RESULTS.json')]:
        bad=dict(fixture);obj=v.parse(bad[target]);obj['status']='PENDING';bad[target]=blob(obj)
        a,m,p=envelope(bad)
        reject(label,lambda a=a,m=m,p=p:v.verify_archive(a,m,p))
    return {'status':'PASS','rejected_count':len(rejected),'negative_controls_rejected':rejected,
        'scope':'Static integrity and evidence-consistency controls only; includes an explicit synthetic outer-envelope fixture. No mathematical proof is certified.'}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',default=str(Path(__file__).resolve().parent))
    a=p.parse_args();print(json.dumps(test(Path(a.root)),indent=2,sort_keys=True))

if __name__=='__main__':
    main()
