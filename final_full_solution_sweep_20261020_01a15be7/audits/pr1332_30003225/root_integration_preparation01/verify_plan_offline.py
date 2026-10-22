"""Independent offline decoding and falsification of the dated integration plan.

No service or Git command. Only the verification receipt is written here.
This validates a plan; it never applies one or grants action authority.
"""
from pathlib import Path, PurePosixPath
import base64
import copy
import gzip
import hashlib
import io
import json
import re
import sys

P = Path(__file__).resolve().parent
PROJECT = 'unsolved_math_prioritization/attempts/30003225'
QUEUE = 'unsolved_math_prioritization/QUEUE.md'


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def oid(kind, data, algorithm='sha1'):
    return hashlib.new(algorithm, kind.encode()+b' '+str(len(data)).encode()+b'\0'+data).hexdigest()


def digest(data):
    return hashlib.sha256(data).hexdigest()


def canonical_gzip(data):
    stream = io.BytesIO()
    with gzip.GzipFile(fileobj=stream, filename='', mode='wb', compresslevel=9, mtime=0) as f:
        f.write(data)
    return stream.getvalue()


def decode_gzip(raw):
    b = gzip.decompress(raw)
    require(raw == canonical_gzip(b), 'noncanonical gzip wrapper/extra members')
    return b


def parse_tree(raw):
    rows = []
    pos = 0
    while pos < len(raw):
        split = raw.index(b' ', pos)
        zero = raw.index(b'\0', split)
        mode, name = raw[pos:split].decode(), raw[split+1:zero].decode()
        require(len(raw) >= zero+21 and '/' not in name and name not in ('.', '..'), 'tree binary framing')
        require(mode in ('40000', '100644', '100755', '120000', '160000'), 'tree mode')
        rows.append((name, mode, raw[zero+1:zero+21].hex()))
        pos = zero+21
    require(len({x[0] for x in rows}) == len(rows), 'duplicate tree child')
    require(rows == sorted(rows, key=lambda x: x[0].encode()+(b'/' if x[1]=='40000' else b'')), 'Git tree ordering')
    return rows


def normalized(entries):
    return {x['path']:(x['mode'].lstrip('0'),x['sha']) for x in entries}


def api_blob(sha):
    j = json.loads(gzip.decompress((P/'private/api'/('blob_'+sha+'.json.gz')).read_bytes()))
    b = base64.b64decode(j['content'])
    require(j['sha']==sha and len(b)==j['size'] and oid('blob',b)==sha, 'actual original blob identity')
    return b


def actual_queue_row(b):
    lines = b.splitlines(keepends=True)
    hits = [i for i,x in enumerate(lines) if b'| 30003225 / OWR-14754-011 |' in x]
    require(len(hits)==1, 'unique target row')
    i = hits[0]
    return lines, i, lines[i].split(b'|')


def validate_selection(rows, bodies, expected):
    require(len(rows)==len(expected) and {x['path'] for x in rows}==set(expected), 'selected complete path set')
    require(len({x['path'] for x in rows})==len(rows), 'duplicate selected paths')
    for x in rows:
        path = x['path']; b = bodies[path]
        require(x['mode']=='100644', 'selected mode must preserve actual regular0644')
        require(x['bytes']==len(b) and x['sha256']==digest(b), 'selected content digest')
        require(x['git_blob_sha1']==oid('blob',b) and x['git_object_sha256']==oid('blob',b,'sha256'), 'selected canonical Git hashes')
        require(b==expected[path], 'hash-consistent selected content differs from authenticated source')


def validate_queue(new, main, original_head):
    ml, mi, mc = actual_queue_row(main)
    nl, ni, nc = actual_queue_row(new)
    _, _, hc = actual_queue_row(original_head)
    require(mi==ni and len(ml)==len(nl), 'QUEUE line structure')
    require(all(x==y for i,(x,y) in enumerate(zip(ml,nl)) if i!=mi), 'unselected QUEUE bytes changed')
    require(all(x==y for i,(x,y) in enumerate(zip(mc,nc)) if i not in (8,9,11)), 'unselected target row fields changed')
    require(nc[8]==hc[8] and nc[9]==hc[9], 'original Status/Turns changed')
    f = hc[11]; trailing = f[len(f.rstrip(b' \t')):]
    require(nc[11]==f.rstrip(b' \t')+b' [Publication package](attempts/30003225/PUBLICATION.md).'+trailing, 'Findings suffix differs')


def preserve(before, after, allowed):
    require({k:v for k,v in before.items()if k not in allowed}=={k:v for k,v in after.items()if k not in allowed}, 'unselected ancestor siblings changed')


def base_gate(plan, current):
    require(current==plan['dated_main_commit'], 'HOLD: remote main changed; refresh QUEUE/project/ancestors')


def rejected(name, action):
    try:
        action()
    except (RuntimeError,ValueError,KeyError):
        return {'name':name,'status':'rejected'}
    raise RuntimeError('false plan accepted: '+name)


def main():
    require(sys.argv[1:] in ([], ['--readonly']), 'usage: verify_plan_offline.py [--readonly]')
    manifest = json.loads((P/'SELECTED_PAYLOAD_MANIFEST.json').read_text())
    plan = json.loads((P/'DATED_INTEGRATION_PLAN.json').read_text())
    c = json.loads((P/'COMPUTED_TREES.json').read_text())
    original = json.loads((P/'ORIGINAL_PR_SCOPE.json').read_text())
    q = json.loads((P/'QUEUE_RECONCILIATION.json').read_text())
    rows = manifest['entries']; bodies = {}; compressed_payloads = set()
    for x in rows:
        raw = (P/x['payload']).read_bytes(); b = decode_gzip(raw)
        require(len(raw)==x['gzip_bytes'] and digest(raw)==x['gzip_sha256'] and raw[:10].hex()==x['gzip_header_hex'], 'gzip identity')
        compressed_payloads.add(x['payload']); bodies[x['path']] = b
    require(compressed_payloads=={x.relative_to(P).as_posix()for x in(P/'private/selected_payloads').iterdir()}, 'selected payload namespace')
    expected = {}
    for x in original['actual_original_blobs']:
        b = api_blob(x['git_blob_sha1'])
        require(len(b)==x['bytes'] and digest(b)==x['sha256'] and x['mode']=='100644', 'original modes/content')
        if x['path']!=QUEUE:
            expected[x['path']] = b
    require(len(expected)==7, 'seven original readers')
    for folder, target in [('release','publication'),('science','publication/source')]:
        for f in sorted((P.parent/'publication_preparation_03'/folder).rglob('*')):
            if f.is_file():expected[PROJECT+'/'+target+'/'+f.relative_to(P.parent/'publication_preparation_03'/folder).as_posix()] = f.read_bytes()
    expected[PROJECT+'/PUBLICATION.md'] = (P/'PUBLICATION.md').read_bytes()
    expected[QUEUE] = bodies[QUEUE]
    require(len(expected)==36 and len(compressed_payloads)==32, 'actual path/blob counts')
    validate_selection(rows,bodies,expected)
    main_queue, original_queue = api_blob(q['current_main_queue_blob']), api_blob(q['original_head_queue_blob'])
    validate_queue(bodies[QUEUE],main_queue,original_queue)
    # Decode every actual binary tree independently, then compare declarations.
    computed_by_oid = {}
    for path, t in c['trees'].items():
        raw = (P/t['payload']).read_bytes(); b = decode_gzip(raw); parsed = parse_tree(b)
        require(oid('tree',b)==t['tree_sha1'] and oid('tree',b,'sha256')==t['git_object_sha256'], 'computed Git tree identity')
        require(len(b)==t['raw_bytes'] and digest(b)==t['raw_sha256'] and digest(raw)==t['gzip_sha256'], 'computed tree digest')
        require({n:(m,h)for n,m,h in parsed}==normalized(t['entries']), 'binary tree differs from declared entries')
        computed_by_oid[t['tree_sha1']] = parsed
    project = {}
    def walk(sha,prefix=''):
        require(sha in computed_by_oid,'project tree missing explicit descendant')
        for name,mode,h in computed_by_oid[sha]:
            if mode=='40000':walk(h,prefix+name+'/')
            else:project[PROJECT+'/'+prefix+name] = (mode,h)
    walk(c['project_tree'])
    require(project=={x['path']:(x['mode'],x['git_blob_sha1'])for x in rows if x['path']!=QUEUE}, 'project flattened selected paths differ')
    preserved = []
    for path, allowed in [('',{'unsolved_math_prioritization'}),('unsolved_math_prioritization',{'attempts','QUEUE.md'}),('unsolved_math_prioritization/attempts',{'30003225'})]:
        # Original ancestor IDs are the unchanged child objects in the dated main tree.
        if not path:old_sha = c['original_main_root_tree']
        else:
            old_sha = c['original_main_root_tree']
            for component in path.split('/'):
                old = json.loads(gzip.decompress((P/'private/api'/('tree_'+old_sha+'.json.gz')).read_bytes()))
                old_sha = next(x['sha']for x in old['tree']if x['path']==component)
        old = json.loads(gzip.decompress((P/'private/api'/('tree_'+old_sha+'.json.gz')).read_bytes()))
        before, after = normalized(old['tree']), normalized(c['trees'][path]['entries'])
        preserve(before,after,allowed);preserved.append({'path':path or '/', 'unselected_siblings':len(set(before)-allowed)})
    pointer = expected[PROJECT+'/PUBLICATION.md'].decode()
    require('10.5281/' not in pointer and '2678–2681' in pointer and 'older 18/44-check' in pointer, 'pointer publication/history bounds')
    for link in re.findall(r'\]\(([^)]+)\)',pointer):
        if not link.startswith(('https://','http://')):require(str(PurePosixPath(PROJECT)/link)in expected,'unusable pointer link '+link)
    # Material false-plan controls use only copies in memory.
    controls = []
    wrong = copy.deepcopy(rows);wrong[0]['mode']='100755'
    controls.append(rejected('changed_actual_file_mode',lambda:validate_selection(wrong,bodies,expected)))
    private = copy.deepcopy(rows);private.append(dict(rows[0],path=PROJECT+'/private/.gitignore'))
    controls.append(rejected('unselected_private_file',lambda:validate_selection(private,bodies,expected)))
    controls.append(rejected('missing_original_reader',lambda:validate_selection(rows[1:],bodies,expected)))
    forged = dict(bodies);name=PROJECT+'/ACCEPTANCE.md';forged[name]+=b'forged historical check\n';forged_rows=copy.deepcopy(rows)
    for x in forged_rows:
        if x['path']==name:x.update(bytes=len(forged[name]),sha256=digest(forged[name]),git_blob_sha1=oid('blob',forged[name]),git_object_sha256=oid('blob',forged[name],'sha256'))
    controls.append(rejected('hash_consistent_original_reader_forgery',lambda:validate_selection(forged_rows,forged,expected)))
    bad_queue=bodies[QUEUE].replace(b'Budget',b'CorruptBudget',1)
    require(bad_queue!=bodies[QUEUE],'active QUEUE mutation')
    controls.append(rejected('unselected_QUEUE_bytes_modified',lambda:validate_queue(bad_queue,main_queue,original_queue)))
    before=normalized(json.loads(gzip.decompress((P/'private/api'/('tree_'+c['original_main_root_tree']+'.json.gz')).read_bytes()))['tree']);after=normalized(c['trees']['']['entries']);fake=dict(after);n=next(n for n in before if n!='unsolved_math_prioritization');fake[n]=(fake[n][0],rows[0]['git_blob_sha1'])
    require(fake!=after,'active root sibling mutation');controls.append(rejected('unselected_root_sibling_replaced',lambda:preserve(before,fake,{'unsolved_math_prioritization'})))
    controls.append(rejected('advanced_main_requires_HOLD',lambda:base_gate(plan,'0'*40)))
    raw=(P/rows[0]['payload']).read_bytes();bad=bytearray(raw);bad[4]=1
    require(gzip.decompress(bytes(bad))==gzip.decompress(raw),'active wrapper-only mutation')
    controls.append(rejected('nonzero_gzip_mtime_with_same_body',lambda:decode_gzip(bytes(bad))))
    duplicate_groups = {}
    for x in rows:duplicate_groups.setdefault(x['git_blob_sha1'],[]).append(x['path'])
    result={'status':'PASS','selected_paths':len(rows),'unique_blobs':len(compressed_payloads),
            'selected_logical_bytes':sum(x['bytes']for x in rows),'unique_blob_body_bytes':sum(len(bodies[paths[0]])for paths in duplicate_groups.values()),
            'selected_gzip_allocated_bytes':sum((P/x).stat().st_blocks*512 for x in compressed_payloads),
            'duplicate_blob_path_groups':[v for v in duplicate_groups.values()if len(v)>1],
            'all36_names_modes_bytes_and_both_Git_hashes_checked':True,'all7_computed_binary_trees_independently_decoded':True,
            'project_tree':c['project_tree'],'dated_root_tree':c['proposed_root_tree'],'ancestor_preservation':preserved,
            'pointer_relative_links_and_no_solution_DOI_checked':True,'eight_active_false_plan_controls':controls,
            'no_network_or_Git_command':True,'service_actions':0,'action_authority':False}
    if not sys.argv[1:]:
        (P/'OFFLINE_PLAN_VERIFICATION.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
