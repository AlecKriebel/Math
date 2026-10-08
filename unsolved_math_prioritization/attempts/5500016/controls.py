#!/usr/bin/env python3
"""Adversarial tests using a separately trusted, fixed bootstrap.
Run only after external anchor verification. All mutations are in temporary copies.
"""
import copy
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import tempfile
import types


def need(ok,message):
    if not ok:raise ValueError(message)


def dump(o):return json.dumps(o,indent=2,sort_keys=True)+'\n'


def main():
    need(os.getuid()==1000 and os.geteuid()==1000,'UID=EUID=1000')
    need(len(sys.argv)==5,'usage: controls.py TRUSTED_BOOTSTRAP BOOTSTRAP_SHA256 ROOT QUEUE')
    anchor=Path(sys.argv[1]);pin=sys.argv[2];root=Path(sys.argv[3]);queue=Path(sys.argv[4])
    code=anchor.read_bytes();need(hashlib.sha256(code).hexdigest()==pin,'external bootstrap mismatch')
    bm=types.ModuleType('trusted_bootstrap');bm.__file__=str(anchor)
    exec(compile(code,'trusted_bootstrap.py','exec'),bm.__dict__)
    source=(root/'verify_publication.py').read_bytes()
    need(hashlib.sha256(source).hexdigest()==bm.VERIFIER_SHA256 and len(source)==bm.VERIFIER_BYTES,'external verifier pin')
    m=types.ModuleType('trusted_verifier');exec(compile(source,'trusted_verifier.py','exec'),m.__dict__)
    original=m.file_table(root);original_queue=queue.read_bytes()
    rows=[]
    def run(candidate,q,flags=None):
        return subprocess.run([sys.executable,'-I','-S','-B',*(['-O'] if sys.flags.optimize==1 else ['-OO'] if sys.flags.optimize==2 else []),str(anchor),str(candidate),str(q),*(flags or ['--inventory-only'])],capture_output=True,timeout=90)
    good=run(root,queue)
    need(good.returncode==0 and good.stderr==b'','positive anchor control failed')
    positive=m.strict_json(good.stdout)
    need(m.same(positive,m.verify(root,queue,True)),'positive complete typed control mismatch')
    def record(label,p,accepted):
        rows.append({'label':label,'accepted':accepted,'exit_code':p.returncode,'stdout_utf8':p.stdout.decode('utf-8'),'stderr_utf8':p.stderr.decode('utf-8')})
    record('unmodified_complete_delivery',good,True)
    manifest=m.strict_json(original['PUBLICATION_MANIFEST.json'])
    def repin(candidate):
        data=m.strict_json((candidate/'PUBLICATION_MANIFEST.json').read_bytes())
        for r in data['files']:
            f=candidate/r['path']
            if f.is_file():r.update(m.descriptor(f.read_bytes()))
        (candidate/'PUBLICATION_MANIFEST.json').write_text(dump(data))
    changes=[
      ('report_changed',lambda c,q:(c/'author/REPORT.md').write_bytes(b'changed')),
      ('audit_changed',lambda c,q:(c/'audit/AUDIT.md').write_bytes(b'changed')),
      ('acceptance_changed',lambda c,q:(c/'ACCEPTANCE.md').write_bytes(b'changed')),
      ('scope_changed',lambda c,q:(c/'PUBLIC_SCOPE.json').write_bytes(b'{}')),
      ('replay_receipt_changed',lambda c,q:(c/'REPLAY_RESULTS.json').write_bytes(b'{}')),
      ('controls_receipt_changed',lambda c,q:(c/'CONTROL_RESULTS.json').write_bytes(b'{}')),
      ('historical_receipt_changed',lambda c,q:(c/'audit/receipts/EXECUTION_RECEIPT.json').write_bytes(b'{}')),
      ('historical_stdout_changed',lambda c,q:(c/'audit/receipts/author.normal.stdout.json').write_bytes(b'{}')),
      ('historical_stderr_changed',lambda c,q:(c/'audit/receipts/author.normal.stderr.txt').write_bytes(b'warning')),
      ('expected_output_changed',lambda c,q:(c/'audit/EXPECTED_AUDIT_RESULTS.json').write_bytes(b'{}')),
      ('manifest_truncated',lambda c,q:(c/'PUBLICATION_MANIFEST.json').write_bytes(b'{')),
      ('verifier_replaced',lambda c,q:(c/'verify_publication.py').write_bytes(b"print('PASS')\n")),
      ('bootstrap_replaced',lambda c,q:(c/'BOOTSTRAP.py').write_bytes(b"print('PASS')\n")),
      ('controls_replaced',lambda c,q:(c/'controls.py').write_bytes(b"print('PASS')\n")),
      ('queue_first_line_changed',lambda c,q:q.write_bytes(b'sha: changed\n'+original_queue.split(b'\n',1)[1])),
      ('queue_unrelated_byte_changed',lambda c,q:q.write_bytes(original_queue+b'\n')),
      ('queue_target_status_changed',lambda c,q:q.write_bytes(original_queue.replace(b'| exhausted | 5/5 |  | Audited partial results: same-state',b'| solved | 5/5 |  | Audited partial results: same-state'))),
      ('missing_file',lambda c,q:(c/'author/README.md').unlink()),
      ('extra_file',lambda c,q:(c/'unexpected.txt').write_bytes(b'not allowed')),
      ('extra_empty_directory',lambda c,q:(c/'unexpected').mkdir()),
      ('nested_extra_file',lambda c,q:(c/'audit/receipts/extra.txt').write_bytes(b'not allowed')),
      ('symlink_file',lambda c,q:((c/'author/README.md').unlink(),(c/'author/README.md').symlink_to('../REPORT.md'))),
      ('hardlink_file',lambda c,q:((c/'author/README.md').unlink(),os.link(c/'author/REPORT.md',c/'author/README.md'))),
      ('fifo_file',lambda c,q:((c/'author/README.md').unlink(),os.mkfifo(c/'author/README.md'))),
      ('symlink_directory',lambda c,q:((c/'extra').symlink_to('author',target_is_directory=True))),
    ]
    # Mutations plus self-consistent candidate-side rehashes cannot change the fixed external anchor.
    changes += [(label+'_self_consistent_repin',lambda c,q,f=fn:(f(c,q),repin(c))) for label,fn in changes[:10]]
    for label,change in changes:
        with tempfile.TemporaryDirectory(prefix='polygonalization-control-') as tmp:
            t=Path(tmp);candidate=t/'candidate';q=t/'QUEUE.md'
            shutil.copytree(root,candidate);q.write_bytes(original_queue)
            for f in candidate.rglob('*'):f.chmod(0o755 if f.is_dir() else 0o644)
            candidate.chmod(0o755)
            try:
                change(candidate,q)
                for f in candidate.rglob('*'):
                    if f.is_symlink():continue
                    f.chmod(0o555 if f.is_dir() else 0o444)
                candidate.chmod(0o555);q.chmod(0o444)
                p=run(candidate,q);need(p.returncode!=0 and p.stdout==b'','surviving delivery mutation: '+label)
                record(label,p,False)
            finally:
                candidate.chmod(0o755)
                for f in candidate.rglob('*'):
                    if not f.is_symlink():f.chmod(0o755 if f.is_dir() else 0o644)
                q.chmod(0o644)
    units=[]
    def reject(label,fn):
        try:fn()
        except (ValueError,TypeError,UnicodeDecodeError,json.JSONDecodeError) as e:
            units.append({'label':label,'rejected':True,'exception':type(e).__name__})
        else:raise ValueError('surviving schema control: '+label)
    for label,data in [('duplicate_keys',b'{"x":1,"x":2}'),('nested_duplicate',b'{"x":{"y":1,"y":1}}'),('nan',b'{"x":NaN}'),('infinity',b'{"x":Infinity}'),('overflow_float',b'{"x":1e9999}'),('trailing_json',b'{}{}'),('invalid_utf8',b'\xff')]:
        reject(label,lambda d=data:m.strict_json(d))
    for label,edit in [('manifest_extra_key',lambda x:x.update(extra=True)),('manifest_missing_key',lambda x:x.pop('queue')),('manifest_boolean_schema',lambda x:x.update(schema=True)),('manifest_float_id',lambda x:x.update(problem_id=5500016.0)),('manifest_duplicate_row',lambda x:x['files'].append(copy.deepcopy(x['files'][0]))),('manifest_missing_row',lambda x:x['files'].pop()),('manifest_traversal',lambda x:x['files'][0].update(path='../outside')),('manifest_absolute',lambda x:x['files'][0].update(path='/outside')),('manifest_boolean_bytes',lambda x:x['files'][0].update(bytes=True)),('manifest_float_bytes',lambda x:x['files'][0].update(bytes=1.0)),('manifest_negative_bytes',lambda x:x['files'][0].update(bytes=-1)),('manifest_uppercase_hash',lambda x:x['files'][0].update(sha256='A'*64)),('manifest_row_extra_key',lambda x:x['files'][0].update(extra=True)),('manifest_queue_boolean_bytes',lambda x:x['queue'].update(bytes=True))]:
        v=copy.deepcopy(manifest);edit(v);reject(label,lambda v=v:m.manifest_schema(v))
    for label,a,b in [('bool_int',True,1),('float_int',1.0,1),('nested_bool_int',{'a':[True]},{'a':[1]}),('extra_nested_key',{'a':{'x':1,'y':2}},{'a':{'x':1}}),('list_order',[1,2],[2,1]),('list_length',[1],[1,2]),('null_false',None,False)]:
        need(not m.same(a,b),'typed equality weakness');units.append({'label':label,'rejected':True,'exception':'typed_equality_false'})
    need(m.same(m.file_table(root),original) and queue.read_bytes()==original_queue,'original delivery changed')
    result={'schema':1,'problem_id':5500016,'uid':os.getuid(),'euid':os.geteuid(),'original_delivery_unchanged':True,'delivery_controls':rows,'strict_schema_and_type_controls':units,'mathematical_semantic_mutations':'Twelve freshly executed by audit/audit_counting.py, with full records pinned in REPLAY_RESULTS.json.','source_and_corpus_replay':'NOT_RUN'}
    print(dump(result),end='')

if __name__=='__main__':main()
