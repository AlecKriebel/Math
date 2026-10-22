#!/usr/bin/env python3
"""Read-only, standard-library integrity checks. No mathematical certification."""
import argparse
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import zipfile

CHECKPOINT = '59cd9cd2f409118e98636472194d6e7bdc7895c1'

def need(ok, message):
    if not ok:
        raise ValueError(message)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def fingerprint(data):
    return {'bytes': len(data), 'sha256': digest(data)}

def pairs(items):
    out = {}
    for key, value in items:
        need(key not in out, 'duplicate JSON key')
        out[key] = value
    return out

def bad_constant(value):
    raise ValueError('nonfinite JSON: ' + value)

def parse(data):
    return json.loads(data, object_pairs_hook=pairs, parse_constant=bad_constant)

def path_ok(name):
    need(type(name) is str and name and '\\' not in name and '\x00' not in name, 'bad path type')
    p = PurePosixPath(name)
    need(not p.is_absolute() and not {'..', '.'}.intersection(p.parts) and str(p) == name, 'unsafe path')
    need(all(x not in ('', '.', '..') for x in name.split('/')), 'noncanonical path')
    return name

def pin_ok(pin):
    need(type(pin) is dict and set(pin) == {'bytes', 'sha256'}, 'pin shape')
    need(type(pin['bytes']) is int and pin['bytes'] >= 0, 'pin size type')
    need(type(pin['sha256']) is str and re.fullmatch('[0-9a-f]{64}', pin['sha256']) is not None, 'pin digest')

def git_blob(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()

def git_tree(entries):
    data = b''
    for e in sorted(entries, key=lambda e: e['path'].encode() + (b'/' if e['type'] == 'tree' else b'')):
        mode = e['mode'].lstrip('0')
        data += mode.encode() + b' ' + e['path'].encode() + b'\0' + bytes.fromhex(e['sha'])
    return hashlib.sha1(b'tree ' + str(len(data)).encode() + b'\0' + data).hexdigest()

def safe_zip(data):
    z = zipfile.ZipFile(io.BytesIO(data))
    names = z.namelist()
    need(len(names) == len(set(names)) == len({x.casefold() for x in names}), 'duplicate ZIP name')
    for e in z.infolist():
        path_ok(e.filename)
        need(not e.is_dir() and not e.flag_bits & 1 and stat.S_IFMT(e.external_attr >> 16) in (0, stat.S_IFREG), 'unsafe ZIP member')
    need(z.testzip() is None, 'ZIP CRC')
    return z

def closed_source(data, count):
    z = safe_zip(data)
    manifest = parse(z.read('SOURCE_MANIFEST.json'))
    need(type(manifest) is dict and len(z.namelist()) == count and len(manifest) == count - 1, 'archive counts')
    need(set(z.namelist()) == set(manifest) | {'SOURCE_MANIFEST.json'}, 'archive closure')
    for name, pin in manifest.items():
        path_ok(name); pin_ok(pin)
        need(fingerprint(z.read(name)) == pin, 'archive payload fingerprint')
    return z

def metadata_equal(native, provider, n):
    need(type(native) is dict and len(native) == 12, 'native metadata fields')
    for key, value in native.items():
        actual = provider['resource_type']['type'] if key == 'upload_type' else provider['resource_type']['subtype'] if key == 'publication_type' else provider['license']['id'] if key == 'license' else provider[key]
        if actual != value:
            need(n == 1119 and key == 'description' and actual.replace('’', "'") == value.replace('’', "'"), 'native metadata mismatch')

def walk(root):
    files, dirs = {}, []
    need(root.is_dir() and not root.is_symlink(), 'root directory')
    for base, subdirs, names in os.walk(root, followlinks=False):
        for name in subdirs + names:
            p = Path(base) / name
            need(not p.is_symlink(), 'symlink node')
            rel = str(p.relative_to(root)); path_ok(rel)
            if p.is_dir():
                dirs.append(rel)
            else:
                need(p.is_file() and stat.S_ISREG(p.stat().st_mode), 'special node')
                files[rel] = fingerprint(p.read_bytes())
    return files, sorted(dirs)

def verify(root, anchor):
    need(re.fullmatch('[0-9a-f]{64}', anchor) is not None, 'external digest required')
    mb = (root / 'MANIFEST.json').read_bytes(); need(digest(mb) == anchor, 'external manifest digest')
    m = parse(mb)
    need(m['schema_version'] == 1 and m['checkpoint'] == CHECKPOINT and m['range'] == [1111,1120], 'manifest scope')
    need(set(m['public_files']) == {'.gitignore','REPORT.md','RESEARCH_LOG.md','CHECK_RESULTS.json','verify_artifact.py'}, 'public closure')
    for name, pin in m['public_files'].items():
        path_ok(name); pin_ok(pin); need(fingerprint((root / name).read_bytes()) == pin, 'public pin')
    pp = m['private_manifest']; need(pp['path'] == 'private/INPUT_MANIFEST.json', 'private manifest path')
    pin_ok({k:pp[k] for k in ('bytes','sha256')})
    pb = (root / pp['path']).read_bytes(); need(fingerprint(pb) == {k:pp[k] for k in ('bytes','sha256')}, 'private manifest pin')
    pm = parse(pb); need(pm['schema_version'] == 1, 'private schema')
    for name, pin in pm['files'].items(): path_ok(name); pin_ok(pin)
    pf,pd = walk(root / 'private')
    expected = dict(pm['files']); expected['INPUT_MANIFEST.json'] = fingerprint(pb)
    need(pf == expected and pd == pm['directories'], 'private closed inventory')
    af,ad = walk(root)
    ef = dict(m['public_files']); ef['MANIFEST.json'] = fingerprint(mb)
    ef['MANIFEST.sha256'] = fingerprint((anchor + '  MANIFEST.json\n').encode())
    ef.update({'private/'+k:v for k,v in expected.items()})
    need(af == ef and ad == sorted(['private'] + ['private/'+x for x in pd]), 'whole tree closure')
    R = root / 'private'
    def j(name): return parse((R/name).read_bytes())
    commit=j('remote_commit.json');rt=j('remote_root_tree.json');et=j('remote_effort_tree.json')
    need(commit['sha']==CHECKPOINT and commit['tree']['sha']==rt['sha']==git_tree(rt['tree']), 'Git root tree')
    need(not et['truncated'] and not rt['truncated'], 'truncated Git tree')
    need(next(x['sha'] for x in rt['tree'] if x['path']=='final_full_solution_sweep_20261020_01a15be7')==et['sha'], 'effort tree binding')
    child={}; treeoids={'':et['sha']}
    for e in et['tree']:
        parent,_,name=e['path'].rpartition('/'); child.setdefault(parent,[]).append({**e,'path':name})
        if e['type']=='tree': treeoids[e['path']]=e['sha']
    for name,oid in treeoids.items(): need(git_tree(child.get(name,[]))==oid, 'recursive Git tree')
    index={x['path']:x for x in et['tree']}
    pins=j('FROZEN_PINS.json');need(len(pins)==43,'frozen count')
    for p in pins:
        b=(R/'frozen'/path_ok(p['path'])).read_bytes()
        need(index[p['path']]['sha']==p['git_oid']==git_blob(b) and fingerprint(b)=={k:p[k] for k in ('bytes','sha256')},'checkpoint frozen blob')
    journal=[parse(x) for x in (R/'frozen/dispositions.jsonl').read_bytes().splitlines()]
    need([x['pr'] for x in journal]==list(range(9,1121)), 'journal sequence')
    state=j('frozen/STATE.json');need(state['next_pr']==1121 and state['last_completely_processed_pr']==1120,'checkpoint cursor')
    inv={x['number']:x for x in j('frozen/rest_inventory.json')['pull_requests']}
    identities=j('IDENTITY_RESULTS.json');need([c['pr'] for c in identities['cases']]==list(range(1111,1121)), 'case sequence')
    total=0
    for c in identities['cases']:
        n=c['pr']; live=j(f'original/{n}/LIVE.json');fresh=j(f'final_live/{n}.json');cache=j(f'original/{n}/CACHE.json');blobs=j(f'original/{n}/BLOBS.json')
        for a in [live,fresh]: need((a['head']['sha'],a['base']['sha'],digest(a['body'].encode()),a['state'],a['merged'],a['draft'])==(c['head'],c['base'],c['body_sha256'],c['state'],c['merged'],c['draft']),'live identity')
        need(c['head']==inv[n]['headRefOid'] and c['base']==inv[n]['baseRefOid'] and digest(inv[n]['body'].encode())==c['body_sha256'],'inventory identity')
        need(len(blobs)==c['paths'] and len({x['path'] for x in blobs})==len(blobs),'complete path count')
        need({x['path'] for x in blobs}==set(cache['changed_paths']), 'cache complete paths')
        cm={x['filename']:x['sha'] for x in cache['files']}
        for p in blobs:
            need(PurePosixPath(p['path']).name!='QUEUE.md','unexpected QUEUE path')
            b=(R/f'original/{n}'/path_ok(p['path'])).read_bytes()
            need(type(p['git_oid']) is str and re.fullmatch('[0-9a-f]{40}',p['git_oid']) is not None,'nonnull Git identity')
            need(git_blob(b)==p['git_oid']==cm[p['path']] and fingerprint(b)=={k:p[k] for k in ('bytes','sha256')},'actual head blob')
        d=j(f'frozen/PR{n}_DISPOSITION.json'); need(d==journal[n-9] and d['current_classification']==c['classification'],'journal disposition')
        total+=len(blobs)
    need(total==81,'actual head count')
    sheet=j('sheet.json');finalsheet=j('final_sheet.json');need(sheet['values']==finalsheet['values'] and len(sheet['values'])==180,'sheet readback')
    need(sheet['values'][0]==['Original Problem','Solution Chat URL','DOI','Notes'],'sheet schema')
    for n,record,row,count,stem in [(1118,23440943,153,29,'totally-mixed-face-posets'),(1119,23441523,155,98,'vdf-testing-gap')]:
        P=R/f'pub{n}';api=j(f'pub{n}/record.json');latest=j(f'pub{n}/final_record.json')
        need(api['id']==record and api['state']=='done' and api['submitted'] is True and api['doi']=='10.5281/zenodo.'+str(record),'published provider')
        need(api['metadata']==latest['metadata'] and api['files']==latest['files'] and latest['state']=='done','provider readback')
        need({x['key'] for x in api['files']}=={stem+'.pdf',stem+'-source-and-verification.zip'},'provider files closure')
        for f in api['files']:
            data=(P/path_ok(f['key'])).read_bytes();need(len(data)==f['size'] and f['checksum']=='md5:'+hashlib.md5(data).hexdigest(),'provider payload')
        z=closed_source((P/(stem+'-source-and-verification.zip')).read_bytes(),count)
        need(z.read('output/pdf/'+stem+'.pdf')==(P/(stem+'.pdf')).read_bytes(),'embedded PDF')
        meta=parse(z.read('zenodo-metadata.json'));metadata_equal(meta,api['metadata'],n)
        need(meta==j(f'pub{n}/zenodo-deposit.json')['metadata'],'native wrapper')
        kit=safe_zip((P/'output/zenodo-upload-kit.zip').read_bytes())
        need(set(kit.namelist())=={stem+'.pdf',stem+'-source-and-verification.zip','README.md','zenodo-metadata.json','zenodo-deposit.json'},'kit closure')
        for name in [stem+'.pdf',stem+'-source-and-verification.zip','README.md','zenodo-metadata.json']:need(kit.read(name)==(P/name).read_bytes(),'kit payload')
        dep=parse(kit.read('zenodo-deposit.json'));need(dep['metadata']==meta and {x['path'] for x in dep['files']}=={stem+'.pdf',stem+'-source-and-verification.zip'},'portable deposit')
        prov=parse(z.read('PROVENANCE.json'));head=j(f'original/{n}/LIVE.json')['head']['sha'];need(prov['source_head_sha']==head,'publication head')
        if n==1118:
            originals=prov['pinned_original_inputs'];need(len(originals)==8,'eight original input pins')
            for p in originals:need(fingerprint((R/f'original/{n}'/p['path']).read_bytes())=={k:p[k] for k in ('bytes','sha256')},'published original pins')
        else:
            for name in ['PROOF.md','SOURCE_METADATA.json','SOURCE_REVIEW.md']:need(z.read('audit/inputs/'+name)==(R/f'original/{n}/unsolved_math_prioritization/attempts/30004127'/name).read_bytes(),'original archive copy')
        need([i for i,v in enumerate(sheet['values'],1) if len(v)>2 and v[2]=='https://doi.org/'+api['doi']]==[row],'unique DOI row')
        need(f'/pull/{n}' in ' '.join(sheet['values'][row-1]) and str(prov['problem_id']) in ' '.join(sheet['values'][row-1]),'result row identity')
        gate=j(f'pub{n}/postfreeze/ACCEPTANCE_GATE.json'); rounds=[2,3] if n==1118 else [1,2]
        bindings=next(x for x in j('POSTFREEZE_BINDING_RESULTS.json')['results'] if x['pr']==n)
        for rnd in rounds:
            D=P/f'postfreeze/reviews/package_round{rnd}'; g=gate['whole_package_reviews'][f'round{rnd}'];need(digest((D/'REPORT.md').read_bytes())==g['report_sha256'],'review report binding')
            if n==1118:
                b=(D/'ARTIFACT_RECEIPT.json').read_bytes();need(digest(b)==g['receipt_sha256'],'receipt gate');d=parse(b);mapping=d['frozen_package_unchanged'] if rnd==2 else d['operative_files']
            else:
                b=(D/'ARTIFACT_MANIFEST.json').read_bytes();need(digest(b)==g['manifest_sha256'],'manifest gate');d=parse(b);mp=d['artifacts'] if rnd==1 else d['files']
                for name in ['REPORT.md','FROZEN_INPUT_RECEIPT.json','FINAL_INTEGRITY_CHECK.json']:need(fingerprint((D/name).read_bytes())==mp[name],'review record pin')
                d=parse((D/'FROZEN_INPUT_RECEIPT.json').read_bytes());mapping=d['publication_files'] if rnd==1 else {x['path']:x['actual'] for x in d['files']}
            for name,pin in bindings['files'].items():
                local=stem+'.pdf' if name.startswith('output/pdf/') else stem+'-source-and-verification.zip' if name=='output/'+stem+'-source-and-verification.zip' else name
                need(fingerprint((P/local).read_bytes())==pin==mapping[name],'successive current freeze binding')
    for name in ['POSTFREEZE_PINS.json','EXTRA_POSTFREEZE_PINS.json']:
        a=j(name);a=a['pins'] if type(a) is dict else a
        for p in a:
            b=(R/path_ok(p['local'])).read_bytes();need(git_blob(b)==p['git_oid'] and fingerprint(b)=={k:p[k] for k in ('bytes','sha256')},'immutable postfreeze blob')
    for p in j('sources/FETCH_RECEIPTS.json'):
        need(p['status']==200 and fingerprint((R/'sources'/(p['name']+'.pdf')).read_bytes())=={k:p[k] for k in ('bytes','sha256')},'primary source capture')
    extra=j('sources/EXTRA_FETCH_RECEIPT.json');need(extra['status']==200 and fingerprint((R/'sources/dr2015.pdf').read_bytes())=={k:extra[k] for k in ('bytes','sha256')},'original billiard source')
    for p in j('VISUAL_PINS.json'):need(digest((R/path_ok(p['image'])).read_bytes())==p['sha256'],'image pin')
    check=j('FINAL_RECHECK.json');need(check['compaction']['files']==446 and check['compaction']['bytes']==49297496 and check['compaction']['full_retained_inventory_equal'] is True,'compaction observation')
    return {'status':'pass','checkpoint':CHECKPOINT,'range':[1111,1120],'public_payloads':len(m['public_files']),'private_payloads':len(pm['files']),'actual_head_files':81,'frozen_journal_rows':1112,'published_records':2,'manifest_sha256':anchor,'scope':'Closed captured-byte custody and stated identity bindings only; not proof, priority, current-world state or human peer review.'}

def self_test():
    passed=[]
    def reject(label,fn):
        try: fn()
        except (ValueError,KeyError,TypeError,zipfile.BadZipFile):passed.append(label);return
        raise RuntimeError('guard accepted false input: '+label)
    for label,value in [('duplicate','{"a":1,"a":2}'),('NaN','{"a":NaN}'),('Infinity','{"a":Infinity}')]:reject(label,lambda v=value:parse(v))
    for value in ['/abs','../escape','a/../b','./a','a//b','a\\b','','a\x00b']:
        reject('path:'+repr(value),lambda v=value:path_ok(v))
    for value in [{'bytes':True,'sha256':'0'*64},{'bytes':-1,'sha256':'0'*64},{'bytes':0,'sha256':'x'*64},{'bytes':0,'sha256':'0'*64,'extra':0}]:reject('pin:'+repr(value),lambda v=value:pin_ok(v))
    reject('bad zip',lambda:safe_zip(b'bad'))
    for names in [['a','a'],['A','a'],['../escape'],['dir/']]:
        b=io.BytesIO()
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            with zipfile.ZipFile(b,'w') as z:
                for name in names:z.writestr(name,b'x')
        reject('zip:'+repr(names),lambda v=b.getvalue():safe_zip(v))
    need(parse('{"a":1}')=={'a':1} and path_ok('a/b')=='a/b','positive JSON/path')
    pin_ok({'bytes':0,'sha256':digest(b'')})
    need(git_blob(b'')=='e69de29bb2d1d6434b8b29ae775ad8c2e48c5391' and git_tree([])=='4b825dc642cb6eb9a060e54bf8d69288fbee4904','known Git positives')
    return {'status':'pass','negative_controls':len(passed),'labels':passed,'positive_controls':5,'scope':'JSON/path/pin/ZIP guard controls only; no package mathematical programs executed.'}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path);p.add_argument('--manifest-sha256');p.add_argument('--self-test',action='store_true');a=p.parse_args()
    if a.self_test: result=self_test()
    else:
        need(a.root is not None and a.manifest_sha256 is not None,'root and external anchor required')
        result=verify(a.root,a.manifest_sha256)
    print(json.dumps(result,sort_keys=True,separators=(',',':')))
