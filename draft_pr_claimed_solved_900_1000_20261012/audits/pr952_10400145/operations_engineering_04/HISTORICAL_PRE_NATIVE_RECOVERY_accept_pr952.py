#!/usr/bin/env python3
"""PR952 publication operations. Import performs no external operation.

Use a trusted interpreter with -I -S -B and externally authenticated inventory,
freeze and review hashes. This provenance boundary is not an OS sandbox.
"""
import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):
    raise RuntimeError('Invoke with Python -I -S -B before loading this file')
import argparse,base64,copy,hashlib,io,json,os,re,sqlite3,stat,subprocess,zipfile
from pathlib import Path,PurePosixPath
from datetime import datetime,timezone
from urllib.request import Request,urlopen
from urllib.parse import urlsplit
P=Path(__file__).resolve().parent
ROOT=P.parent
A=P/'audits/pr952_10400145'
W=A/'publication/workflow'
D=A/'preprint'
HEAD='989a532ae1d50894190d010a0a02ba8c3d71ee05'
KEY='10400145'
PR=952
QUEUE='unsolved_math_prioritization/QUEUE.md'
STATE='unsolved_math_prioritization/state.json'
HISTORY='unsolved_math_prioritization/history.jsonl'
CATALOG='unsolved_math_prioritization/catalog.json'
RELATED='unsolved_math_prioritization/review_v2/related_target_groups.json'
PREFIX='unsolved_math_prioritization/attempts/'+KEY+'/'
SID='1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20'
HELPERS=['accept_pr952.py','merge_pr952.py','run_pr952_zenodo.py','append_pr952_tracker.py','update_pr952_publication_ledger.py','finalize_pr952_and_gate_next.py']
KIT='zenodo_deposit_tool/zenodo.py'
STATEMENT='87dd83734fc8c51eb132f501c5d05947ed7057268dfba61627fb78f53da10af8'
REVIEW='12e089388884a531bdc98f888e203ec0be06aa637e3ce342ac1e502a7af266f5'
PRIVATE='f7d80d30437d531fe6dab53b567032dd74253872420267b93d466c2aa93a1510'
PDF='habiro-rank-interpolation-v1.0.pdf'
ZIP='habiro-rank-interpolation-verification-v1.0.zip'
TITLE="A first-order obstruction to Habiro's rank interpolation"
INITIAL_FAMILIES=frozenset(['algebra_falsifier_01','quantum_bridge_01','computation_01','classical_priority_01','recent_priority_01'])
INHERITED_FINDING_IDS=frozenset(['R952-ALG-O01', 'R952-ALG-O02', 'R952-BRIDGE-O01', 'R952-BRIDGE-O02', 'R952-BRIDGE-O03', 'REQ-COMP-01', 'REQ-COMP-02', 'OPT-COMP-01', 'OPT-COMP-02', 'OPT-COMP-03', 'CP-R01', 'CP-R02', 'CP-R03', 'CP-001', 'CP-002', 'CP-003', 'CP-004', 'CP-005', 'CP-006', 'CP-G01', 'CP-G02', 'CP-G03', 'CP-G04', 'CP-G05', 'RP-REQ-001', 'RP-OPT-001', 'RP-OPT-002', 'RP-OPT-003'])
KIT_SHA='a91f961bcabadb15f92bb738c3194f0277cd47f1f87167ac8db8eb7c4fd3b9ca'
PRIOR_REPORT_SHA='ad708f96865972507a28c13ba5425c1bf41bb2607c60e5ecfa4197328b629c25'
REQUIRED_ROOT_FINDING_IDS=frozenset(['R952-OPS-ROOT-01'])
PACKAGE_VERIFIER_SHA='ba18bdcd863c3dca65c86be711564527ce19e4c859204b66095e39d366f453d7'
ORIGINAL_RECORDS_SHA='0af77216cf150a263108ad450d1497c342ec577ab624cc046bfcb22cdf14c123'
MAX_FILE=32*1024*1024
READ_ONLY=False
OBSERVATION_OUTPUT=None


def need(ok, label):
    if not ok:
        raise RuntimeError('PR952 guard: ' + label)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def safe(name):
    return (type(name) is str and bool(name) and '\\' not in name and '\0' not in name
            and not PurePosixPath(name).is_absolute()
            and PurePosixPath(name).as_posix() == name
            and all(x not in ('', '.', '..') for x in name.split('/')))


def strict_json(raw):
    def pairs(items):
        result = {}
        for k, v in items:
            need(k not in result, 'duplicate JSON key')
            result[k] = v
        return result
    def bad(value):
        raise RuntimeError('Nonfinite JSON constant: ' + value)
    return json.loads(raw, object_pairs_hook=pairs, parse_constant=bad)


def fingerprint(raw):
    return {'bytes': len(raw), 'sha256': sha(raw)}


def validate_pin(pin):
    need(type(pin) is dict and set(pin) == {'bytes', 'sha256'}
         and type(pin['bytes']) is int and 0 <= pin['bytes'] <= MAX_FILE
         and type(pin['sha256']) is str
         and re.fullmatch('[0-9a-f]{64}', pin['sha256']) is not None,
         'fingerprint schema/cap')


def read_regular(path, cap=MAX_FILE, pin=None):
    """Anchor every repository ancestor; reject FIFO/symlink before reading."""
    path = Path(path)
    try:
        name = path.relative_to(ROOT).as_posix()
    except ValueError as error:
        raise RuntimeError('File outside trusted repository root') from error
    need(safe(name), 'unsafe repository file name')
    if pin is not None:
        validate_pin(pin)
        cap = pin['bytes']
    need(type(cap) is int and 0 <= cap <= MAX_FILE, 'read cap')
    flags = os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK
    fd = os.open(ROOT, flags | os.O_DIRECTORY)
    try:
        parts = name.split('/')
        for part in parts[:-1]:
            next_fd = os.open(part, flags | os.O_DIRECTORY, dir_fd=fd)
            os.close(fd)
            fd = next_fd
        file_fd = os.open(parts[-1], flags, dir_fd=fd)
        try:
            info = os.fstat(file_fd)
            need(stat.S_ISREG(info.st_mode) and info.st_size <= cap,
                 'nonregular or oversized file: ' + name)
            if pin is not None:
                need(info.st_size == pin['bytes'], 'file size changed: ' + name)
            chunks = []
            total = 0
            while total <= cap:
                block = os.read(file_fd, min(1024 * 1024, cap + 1 - total))
                if not block:
                    break
                chunks.append(block)
                total += len(block)
            raw = b''.join(chunks)
            need(len(raw) <= cap, 'file grew beyond cap: ' + name)
            if pin is not None:
                need(fingerprint(raw) == pin, 'file fingerprint changed: ' + name)
            return raw
        finally:
            os.close(file_fd)
    finally:
        os.close(fd)


def load(path):
    return strict_json(read_regular(path, 8 * 1024 * 1024))


def save(path, value, exclusive=False):
    raw = (json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + '\n').encode()
    flags = os.O_WRONLY | os.O_CREAT | os.O_NOFOLLOW
    flags |= os.O_EXCL if exclusive else os.O_TRUNC
    name = Path(path).relative_to(ROOT).as_posix()
    need(safe(name), 'unsafe receipt path')
    directory_flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_NONBLOCK
    directory_fd = os.open(ROOT, directory_flags)
    try:
        parts = name.split('/')
        for part in parts[:-1]:
            next_fd = os.open(part, directory_flags, dir_fd=directory_fd)
            os.close(directory_fd)
            directory_fd = next_fd
        fd = os.open(parts[-1], flags | os.O_NONBLOCK, 0o600, dir_fd=directory_fd)
        with os.fdopen(fd, 'wb') as stream:
            need(stat.S_ISREG(os.fstat(stream.fileno()).st_mode), 'nonregular receipt output')
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        os.fsync(directory_fd)
    finally:
        os.close(directory_fd)


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def utc(value):
    need(type(value) is str, 'timestamp type')
    result = datetime.fromisoformat(value.replace('Z', '+00:00'))
    need(result.tzinfo is not None and result.utcoffset().total_seconds() == 0,
         'timestamp must be explicit UTC')
    return result


def exact(a, b):
    if type(a) is not type(b): return False
    if type(a) is dict: return set(a)==set(b) and all(exact(a[k],b[k]) for k in a)
    if type(a) is list: return len(a)==len(b) and all(exact(x,y) for x,y in zip(a,b))
    return a==b

def run(args, raw=False, **kwargs):
    return subprocess.run(args, cwd=ROOT, check=True, capture_output=True,
                          text=not raw, **kwargs).stdout


def blob(ref, path):
    return run(['git', 'show', ref + ':' + path], raw=True)


def queue_parts(raw, key=KEY):
    lines = raw.splitlines(keepends=True)
    matches = [i for i, line in enumerate(lines) if ('| ' + key + ' /').encode() in line]
    need(len(matches) == 1, 'exactly one selected queue row')
    index = matches[0]
    row = lines[index]
    return b''.join(lines[:index] + lines[index + 1:]), row, index, lines


def claimed_row(raw):
    _, row, _, _ = queue_parts(raw)
    cells = row.decode().split('|')
    need(len(cells) >= 13 and cells[8].strip() == 'claimed_solved'
         and cells[9].strip() == '1/5', 'exact claimed_solved declared1/5 gate')
    return row


def validate_inventory(mapping):
    need(type(mapping) is dict and mapping.get('schema') == 'pr952-operations-v1'
         and type(mapping.get('pr')) is int and mapping['pr'] == PR
         and mapping.get('problem_id') == KEY
         and mapping.get('original_pr_head') == HEAD, 'inventory target/schema')
    records = mapping.get('files')
    expected = {P.relative_to(ROOT).as_posix() + '/' + name for name in HELPERS} | {KIT}
    need(type(records) is dict and set(records) == expected, 'entire seven-file operations inventory required')
    for name, pin in records.items():
        need(safe(name), 'inventory path')
        validate_pin(pin)
        need(0 < pin['bytes'] <= 4 * 1024 * 1024, 'operational dependency size cap')
    need(records[KIT]['sha256']==KIT_SHA,'unchanged standard kit SHA256')
    return records


def capture_inventory(external_pin):
    need(type(external_pin) is str and re.fullmatch('[0-9a-f]{64}', external_pin) is not None,
         'external operations-inventory pin required')
    raw = read_regular(W / 'OPERATIONS_INVENTORY.json', 1024 * 1024)
    need(sha(raw) == external_pin, 'externally pinned operations inventory changed')
    mapping = strict_json(raw)
    records = validate_inventory(mapping)
    captured = {name: read_regular(ROOT / name, pin=pin) for name, pin in records.items()}
    return {'inventory_sha256': external_pin, 'inventory': mapping, 'captured': captured}


def required_record(record, fields, label):
    """Require every documented field and its exact type; additional fields survive."""
    need(type(record) is dict and set(fields) <= set(record), label + ' mandatory keys')
    for name, kind in fields.items():
        need(type(record[name]) is kind, label + ' field type: ' + name)


def raw_json_members(raw):
    text = raw.decode() if type(raw) is bytes else raw
    strict_json(text)
    decoder = json.JSONDecoder()
    pos = text.index('{') + 1
    members = {}
    while True:
        while text[pos].isspace() or text[pos] == ',':
            pos += 1
        if text[pos] == '}':
            break
        start = pos
        name, pos = decoder.raw_decode(text, pos)
        need(type(name) is str and name not in members, 'state member name')
        while text[pos].isspace():
            pos += 1
        need(text[pos] == ':', 'state member colon')
        pos += 1
        while text[pos].isspace():
            pos += 1
        value_start = pos
        _, pos = decoder.raw_decode(text, pos)
        members[name] = {'literal': text[start:pos], 'value_start': value_start, 'value_end': pos}
    return members


def replace_entry(raw, key, value):
    parsed = strict_json(raw)
    members = raw_json_members(raw)
    if key in members:
        item = members[key]
        result = raw[:item['value_start']] + json.dumps(value, indent=2, ensure_ascii=False) + raw[item['value_end']:]
    else:
        index = raw.rfind('}')
        entry = json.dumps(key) + ': ' + json.dumps(value, indent=2, ensure_ascii=False)
        result = raw[:index] + (',\n' if parsed else '\n') + entry + '\n}' + raw[index + 1:]
    changed = strict_json(result)
    need(exact(changed[key], value), 'state target replacement')
    after = raw_json_members(result)
    need({k: v['literal'] for k, v in members.items() if k != key}
         == {k: v['literal'] for k, v in after.items() if k != key}, 'another state member literal changed')
    return result


def explicit_tree(parent, replacements):
    need(set(replacements) == {QUEUE, STATE, HISTORY}, 'only three native paths')
    updates = {}
    for path, text in replacements.items():
        oid = run(['git', 'hash-object', '-w', '--stdin'], input=text).strip()
        entry = run(['git', 'ls-tree', parent, '--', path]).split()
        need(entry[0] == '100644' and entry[1] == 'blob', 'native blob mode')
        cursor = updates
        parts = path.split('/')
        for part in parts[:-1]:
            cursor = cursor.setdefault(part.encode(), {})
        cursor[parts[-1].encode()] = (b'100644', b'blob', oid.encode())
    def rebuild(old, changes):
        entries = {}
        for row in run(['git', 'ls-tree', '-z', old], raw=True).split(b'\0'):
            if row:
                header, name = row.split(b'\t', 1)
                entries[name] = tuple(header.split(b' '))
        for name, value in changes.items():
            if type(value) is dict:
                need(name in entries and entries[name][1] == b'tree', 'native tree ancestor')
                entries[name] = (entries[name][0], b'tree', rebuild(entries[name][2].decode(), value).encode())
            else:
                entries[name] = value
        payload = b''.join(b' '.join(header) + b'\t' + name + b'\0' for name, header in entries.items())
        return run(['git', 'mktree', '-z'], raw=True, input=payload).decode().strip()
    return rebuild(parent, updates)


def remote_main():
    ref=run(['git','ls-remote','origin','refs/heads/main']).split()[0]
    need(re.fullmatch('[0-9a-f]{40}',ref) is not None,'remote main hash')
    if not READ_ONLY:run(['git','fetch','--no-write-fetch-head','origin',ref])
    return ref


def original_check(ref=HEAD):
    raw_records=read_regular(A/'ORIGINAL_FILE_RECORDS.json');need(sha(raw_records)==ORIGINAL_RECORDS_SHA,'original records root pin');records=strict_json(raw_records)
    need(records.get('head')==HEAD and type(records.get('files')) is dict and len(records['files'])==33,'original33 inventory')
    result={}
    for name,pin in records['files'].items():
        need(safe(name) and name.startswith(PREFIX),'original path scope')
        raw=blob(ref,name)
        disk=read_regular(A/'original'/name)
        need(type(pin.get('bytes')) is int and len(raw)==pin['bytes'] and sha(raw)==pin['sha256'] and raw==disk,'original byte identity')
        oid=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
        row=run(['git','ls-tree',ref,'--',name]).strip().split(None,3)
        need(row[:3]==['100644','blob',oid] and oid==pin['git_blob'] and pin['git_mode']=='100644','original Git blob/mode')
        need(stat.S_IMODE((A/'original'/name).lstat().st_mode)==0o644,'original disk0644')
        result[name]={'bytes':len(raw),'sha256':sha(raw),'git_blob':oid,'git_mode':'100644','disk_mode':'0644'}
    return result


def source_gate(parent):
    private=read_regular(A/'source_record_private.txt')
    need(sha(private)==PRIVATE,'private source bytes changed')
    frozen=strict_json(private)
    need(frozen.get('review_hash')==REVIEW and type(frozen.get('prior_research')) is dict and str(frozen.get('problem',{}).get('id'))==KEY,'private source identity')
    prior=frozen['prior_research']
    need(sha(json.dumps(prior,sort_keys=True).encode())==PRIOR_REPORT_SHA,'pinned canonical prior-research report changed')
    problem=frozen['problem']
    need(sha(problem['statement'].encode())==STATEMENT,'nested statement changed')
    database=ROOT/'unsolved_math_prioritization/cache/catalog.sqlite'
    need(database.is_file() and not database.is_symlink(),'source SQLite file')
    with sqlite3.connect(database.as_uri()+'?mode=ro&immutable=1',uri=True) as connection:
        rows=connection.execute('SELECT payload,report FROM records WHERE key=?',(KEY,)).fetchall()
    need(len(rows)==1,'raw SQLite target absent/ambiguous')
    raw_problem,raw_prior=map(strict_json,rows[0])
    need(exact(raw_problem,problem) and exact(raw_prior,prior) and sha(json.dumps([raw_problem,raw_prior],sort_keys=True).encode())==REVIEW,'raw source/prior-report/review reconstruction changed')
    catalog=strict_json(blob(parent,CATALOG))
    targets=[x for x in catalog if str(x.get('id'))==KEY]
    need(len(targets)==1 and targets[0].get('present') is True and targets[0].get('holds')==[] and targets[0].get('statement_hash')==STATEMENT and targets[0].get('review_hash')==REVIEW,'current catalog source/holds changed')
    groups=strict_json(blob(parent,RELATED)).get('groups')
    need(type(groups) is list,'related groups schema')
    member={str(i):g for i,g in enumerate(groups) if KEY in [str(x) for x in g.get('ids',[])]}
    need(member=={},'new related-target membership needs review')
    return {'utc':utc_now(),'remote_main':parent,'statement_sha256':STATEMENT,'review_hash':REVIEW,'raw_sqlite_source_reconstructed_and_matched':True,'private_record_sha256':PRIVATE,'prior_research_sha256':PRIOR_REPORT_SHA,'raw_prior_report_matched_frozen_report':True,'related_target_groups':{},'holds':[]}


def native_safety(parent, allow_event=None):
    """Authenticate CURRENT target state/history; never infer missing history as zero turns."""
    state_raw=blob(parent,STATE); history_raw=blob(parent,HISTORY)
    state=strict_json(state_raw)
    need(type(state) is dict,'native state mapping')
    events=[strict_json(line) for line in history_raw.splitlines() if line.strip()]
    need(all(type(e) is dict for e in events),'history object entries')
    target=[e for e in events if str(e.get('id'))==KEY]
    prior=state.get(KEY)
    if allow_event is None:
        need(KEY not in state and not target,'current native target/history differs from reviewed absent/UNKNOWN baseline; reconcile fresh evidence')
    else:
        need(exact(prior,allow_event) and len(target)==1 and exact(target[0],allow_event),'current native publication state/history differs')
    return {'state_sha256':sha(state_raw),'history_sha256':sha(history_raw),'target_state_absent':KEY not in state,'target_history_entries':len(target),'historical_native_turn_count':'UNKNOWN','new_author_proof_responses':0}


def live_base_pointer(node):
    need(type(node) is dict and type(node.get('baseRef')) is dict,'live base ref metadata missing')
    ref=node['baseRef'];target=ref.get('target')
    need(type(node.get('baseRefName')) is str and bool(node['baseRefName']) and ref.get('name')==node['baseRefName'] and type(target) is dict,'live base ref name/target missing')
    oid=target.get('oid')
    need(type(oid) is str and re.fullmatch('[0-9a-f]{40}',oid) is not None,'live base branch target commit identity')
    return oid


def pr_view(number=PR):
    fields='number,state,isDraft,headRefOid,headRefName,baseRefName,baseRefOid,url'
    if number==PR:fields+=',title,body,mergeCommit,mergedAt,files,mergeable,mergeStateStatus'
    observed=strict_json(run(['gh','pr','view',str(number),'--repo','AlecKriebel/Math','--json',fields]))
    need(type(observed) is dict and observed.get('number')==number,'PR metadata identity')
    query='query($number:Int!){repository(owner:"AlecKriebel",name:"Math"){pullRequest(number:$number){number state isDraft headRefOid headRefName baseRefName baseRefOid url baseRef{name target{oid}}}}}'
    reply=strict_json(run(['gh','api','graphql','-f','query='+query,'-F','number='+str(number)]))
    need(not reply.get('errors'),'live base pointer GraphQL errors')
    node=reply.get('data',{}).get('repository',{}).get('pullRequest')
    bound=('number','state','isDraft','headRefOid','headRefName','baseRefName','url')
    need(type(node) is dict and all(type(node.get(k)) is type(observed.get(k)) and node.get(k)==observed.get(k) for k in bound),'live base pointer PR metadata changed')
    observed['currentBaseRefOid']=live_base_pointer(node)
    return observed


def main_destination(pr,merged=False):
    need(type(pr.get('number')) is int and pr['number']==PR and pr.get('headRefOid')==HEAD and pr.get('baseRefName')=='main' and pr.get('url')==f'https://github.com/AlecKriebel/Math/pull/{PR}','actual PR/head/main destination')
    if merged:
        need(pr.get('state')=='MERGED' and type(pr.get('mergeCommit')) is dict and re.fullmatch('[0-9a-f]{40}',pr['mergeCommit'].get('oid','')) is not None,'actual merged commit')
    else:
        need(pr.get('state')=='OPEN' and type(pr.get('isDraft')) is bool,'PR open/draft type')


def authority(pr,merged=False):
    main_destination(pr,merged)
    fields=['number','state','headRefOid','headRefName','baseRefName','url']
    fields+=['mergeCommit','mergedAt'] if merged else ['isDraft','title','body']
    need(all(k in pr for k in fields),'complete authoritative metadata')
    return {k:pr[k] for k in fields}


def observation_bracket(before,after,merged=False):
    left,right=authority(before,merged),authority(after,merged)
    diff={k:{'before':before.get(k),'after':after.get(k),'before_present':k in before,'after_present':k in after} for k in sorted(set(before)|set(after)) if k not in before or k not in after or not exact(before[k],after[k])}
    return {'utc':utc_now(),'authority_equal':exact(left,right),'before':before,'after':after,'observation_differences':diff}


def numbered_receipt(stem,value):
    for i in range(1,10000):
        path=(OBSERVATION_OUTPUT or W)/(stem+'_'+str(i).zfill(4)+'.json')
        try:save(path,value,exclusive=True);return path
        except FileExistsError:continue
    raise RuntimeError('receipt bound exhausted')


def complete_changed_paths(before):
    """Complete filename-only GraphQL pages bound to a single actual live base."""
    number=before['number']; fields=('number','state','isDraft','headRefOid','headRefName','baseRefName','url','currentBaseRefOid')
    query='query($number:Int!,$cursor:String){repository(owner:"AlecKriebel",name:"Math"){pullRequest(number:$number){number state isDraft headRefOid headRefName baseRefName baseRefOid url baseRef{name target{oid}} changedFiles files(first:100,after:$cursor){nodes{path}pageInfo{hasNextPage endCursor}}}}}'
    paths=[];pages=[];cursor=None;cursors=set();count=None
    for i in range(30):
        args=['gh','api','graphql','-f','query='+query,'-F','number='+str(number)]
        if cursor is not None:args+=['-f','cursor='+cursor]
        response=strict_json(run(args));need(not response.get('errors'),'changed-file GraphQL errors')
        node=response.get('data',{}).get('repository',{}).get('pullRequest');need(type(node) is dict,'changed-file node')
        numbered_receipt('FILENAME_PAGE_OBSERVATION',{'utc':utc_now(),'before':before,'page_number':i+1,'raw_page':node})
        node['currentBaseRefOid']=live_base_pointer(node);pages.append(node)
        need(all(k in node and k in before and exact(node[k],before[k]) for k in fields),'changed-file page head/live base/identity drift')
        n=node.get('changedFiles');need(type(n) is int and 1<=n<=3000 and (count is None or count==n),'complete bounded changed-file count');count=n
        connection=node.get('files');need(type(connection) is dict and set(connection)=={'nodes','pageInfo'} and type(connection['nodes']) is list and 1<=len(connection['nodes'])<=100,'filename connection')
        for item in connection['nodes']:
            need(type(item) is dict and set(item)=={'path'} and safe(item['path']),'canonical filename only')
            paths.append(item['path'])
        need(len(paths)<=count and len(paths)==len(set(paths)) and len(paths)==len({n.casefold() for n in paths}),'duplicate/alias/excess filenames')
        info=connection['pageInfo'];need(type(info) is dict and type(info.get('hasNextPage')) is bool,'pagination schema')
        if not info['hasNextPage']:
            need(len(paths)==count,'incomplete filename pages');return {'paths':paths,'pages':pages,'live_base':before['currentBaseRefOid'],'count':count}
        cursor=info.get('endCursor');need(type(cursor) is str and cursor and cursor not in cursors,'distinct pagination cursor');cursors.add(cursor)
    raise RuntimeError('changed-file page bound exceeded')

def _premerge_gate(freeze,require_draft=False):
    before=pr_view();numbered_receipt('PREMERGE_BEFORE',{'utc':utc_now(),'before':before});main_destination(before)
    need(not require_draft or before['isDraft'] is True,'acceptance still draft')
    need(sha(before['body'].encode())==freeze['pr_description_sha256'],'reviewed PR description changed')
    claimed_row(blob(HEAD,QUEUE));originals=original_check()
    paths=complete_changed_paths(before)
    parent=remote_main();need(parent==before['currentBaseRefOid'],'main changed before source/path gate; restart fresh bracket')
    source=source_gate(parent);native=native_safety(parent)
    base=run(['git','merge-base',HEAD,parent]).strip()
    need(queue_parts(blob(base,QUEUE))[0]==queue_parts(blob(HEAD,QUEUE))[0],'PR alters another queue row')
    need(set(paths['paths'])==set(originals)|{QUEUE},'exact original33 and QUEUE complete filename scope')
    after=pr_view();bracket=observation_bracket(before,after)
    numbered_receipt('PREMERGE_BRACKET',{**bracket,'parent':parent,'paths':paths,'source':source,'native':native})
    need(bracket['authority_equal'],'PR authority changed across source gates')
    need(after['currentBaseRefOid']==parent and remote_main()==parent,'live main changed inside source/path eligibility bracket; restart')
    return {'pr':after,'parent':parent,'source':source,'native':native,'originals':originals,'paths':paths,'bracket':bracket}

def premerge_gate(freeze,require_draft=False):
    try:return _premerge_gate(freeze,require_draft)
    except Exception as error:
        failure={'utc':utc_now(),'error':str(error),'status':'FAIL_OR_INCOMPLETE_NO_CLEAN_CREDIT'}
        try:failure['after_failure']=pr_view()
        except Exception as after_error:failure['after_readback_error']=str(after_error)
        numbered_receipt('PREMERGE_FAILURE',failure)
        raise


def frozen_profile(freeze,base=D):
    name='package/'+freeze['package_verifier']
    raw=read_regular(base/name,pin=freeze['files'][name])
    space={'__name__':'_pr952_authenticated_profile_','__file__':str(base/name)}
    exec(compile(raw,str(base/name),'exec',dont_inherit=True,optimize=0),space)
    return space


def authenticate_evidence(evidence,base,historical=False):
    """Historical candidates authenticate THEIR snapshots, never living evidence.

    Archive every old evidence_files key as base/evidence/REPO_RELATIVE_KEY.
    Private raw-source bodies belong only in private local historical evidence
    storage and must never enter public package, archive or commit allowlists.
    There is no live fallback: absence or drift rejects before profile execution.
    """
    need(type(evidence) is dict and type(historical) is bool,'evidence snapshot schema')
    checked={}
    for name,record in evidence.items():
        need(safe(name),'evidence repo-relative path')
        target=base/'evidence'/name if historical else ROOT/name
        raw=read_regular(target,pin=record)
        checked[name]=fingerprint(raw)
    return checked


def freeze_check(raw,pin,context,base=D,historical=False):
    need(type(pin) is str and re.fullmatch('[0-9a-f]{64}',pin) is not None and sha(raw)==pin,'external freeze SHA256')
    freeze=strict_json(raw)
    required={'schema','created_utc','revision_candidate','pr','problem_id','original_pr_head','operations_inventory_sha256','pr_description_sha256','package_manifest_sha256','package_pdf','package_verifier','files','evidence_files','future_helpers','replay_normalization_ignored','family_authentication','inherited_finding_ids'}
    need(type(freeze) is dict and set(freeze)==required,'exact freeze schema')
    need(freeze['schema']=='pr952-publication-freeze-v1' and type(freeze['pr']) is int and freeze['pr']==PR and freeze['problem_id']==KEY and freeze['original_pr_head']==HEAD,'freeze target')
    need(type(freeze['revision_candidate']) is int and freeze['revision_candidate']>=1 and freeze['replay_normalization_ignored']==[],'freeze revision/no normalization')
    utc(freeze['created_utc'])
    for field in ('operations_inventory_sha256','pr_description_sha256','package_manifest_sha256'):
        need(type(freeze[field]) is str and re.fullmatch('[0-9a-f]{64}',freeze[field]) is not None,'freeze hash schema')
    if historical:
        old=read_regular(base/'OPERATIONS_INVENTORY.json')
        need(sha(old)==freeze['operations_inventory_sha256'],'historical operations inventory')
        inv=validate_inventory(strict_json(old))
        for name,record in inv.items():read_regular(base/'operations'/name,pin=record)
    else:
        need(freeze['operations_inventory_sha256']==context['inventory_sha256'],'freeze/current inventory mismatch')
        inv=context['inventory']['files']
    need(exact(freeze['future_helpers'],{n:inv[(P.relative_to(ROOT)/n).as_posix()] for n in HELPERS}),'all six frozen helper pins')
    files=freeze['files'];evidence=freeze['evidence_files']
    mandatory={PDF,ZIP,'zenodo-deposit.json','package/PACKAGE_MANIFEST.json','FINDING_DISPOSITIONS.json','PR_DESCRIPTION.md','BUILD_RECEIPT.json',*['PACKAGE_REPLAY_'+x+'.json' for x in ['normal','O','OO','env2']]}
    need(type(files) is dict and mandatory<=set(files) and 'FREEZE.json' not in files,'required closed frozen files')
    for name,record in files.items():
        need(safe(name),'freeze relative file')
        read_regular(base/name,pin=record)
    required_evidence={(A/n).relative_to(ROOT).as_posix() for n in ['ORIGINAL_FILE_RECORDS.json','ELIGIBILITY_GATE.json','TARGET_IDENTITY_PREFLIGHT.json','ORIGINAL_SNAPSHOT.json','NATIVE_ACCOUNTING_BASELINE.json','source_record_private.txt']}
    if not historical:required_evidence.add((A/'ROOT_OPERATIONAL_FINDINGS.json').relative_to(ROOT).as_posix())
    families=freeze['family_authentication']
    need(type(families) is dict and set(families)==INITIAL_FAMILIES,'five independently root-authenticated initial families')
    for family,item in families.items():
        required_record(item,{'manifest_path':str,'manifest_sha256':str,'root_authentication_path':str,'root_authentication_sha256':str},'family root authentication')
        need(set(item)=={'manifest_path','manifest_sha256','root_authentication_path','root_authentication_sha256'},'exact family declaration')
        manifest=(A/'reviews'/family/'MANIFEST.json').relative_to(ROOT).as_posix()
        need(item['manifest_path']==manifest,'family-specific manifest path')
        for path_field,hash_field in [('manifest_path','manifest_sha256'),('root_authentication_path','root_authentication_sha256')]:
            name=item[path_field];need(safe(name) and name.startswith(A.relative_to(ROOT).as_posix()+'/'),'family evidence scope')
            need(type(item[hash_field]) is str and re.fullmatch('[0-9a-f]{64}',item[hash_field]),'family root hash')
            required_evidence.add(name)
            need(name in evidence and evidence[name]['sha256']==item[hash_field],'separate root-authenticated family pins')
    need(type(evidence) is dict and required_evidence<=set(evidence),'required private/source/root family anchors')
    authenticate_evidence(evidence,base,historical)
    for family,item in families.items():
        source=(base/'evidence'/item['root_authentication_path']) if historical else ROOT/item['root_authentication_path']
        record=strict_json(read_regular(source,pin=evidence[item['root_authentication_path']]))
        need(record.get('status')=='PASS_BYTES_BEFORE_FULL_REPORT_INTAKE' and record.get('manifest_sha256')==item['manifest_sha256'],'actual root family authentication not a placeholder')
    ids=freeze['inherited_finding_ids']
    need(type(ids) is list and ids and all(type(x) is str and x.strip() for x in ids) and len(ids)==len(set(ids)),'explicit exact nonempty current inherited IDs')
    need(set(ids)==INHERITED_FINDING_IDS,'exact root28 inherited finding IDs')
    need(safe(freeze['package_pdf']) and 'package/'+freeze['package_pdf'] in files,'package PDF path')
    need(safe(freeze['package_verifier']) and 'package/'+freeze['package_verifier'] in files,'package verifier path')
    need(files['package/'+freeze['package_verifier']]['sha256']==PACKAGE_VERIFIER_SHA,'unchanged independently engineered verifier')
    manifest=read_regular(base/'package/PACKAGE_MANIFEST.json',pin=files['package/PACKAGE_MANIFEST.json'])
    need(sha(manifest)==freeze['package_manifest_sha256'],'freeze/package external anchor')
    profile=frozen_profile(freeze,base)
    receipt,_,_=profile['verify'](str(base/'package'),freeze['package_manifest_sha256'])
    doc=strict_json(manifest)
    expected={n:{'bytes':v['bytes'],'sha256':v['sha256']} for n,v in doc['files'].items()}
    expected['PACKAGE_MANIFEST.json']=fingerprint(manifest)
    need({n[8:]:v for n,v in files.items() if n.startswith('package/')}==expected,'freeze/entire closed package map differs')
    archive=read_regular(base/ZIP,pin=files[ZIP])
    profile['inspect_archive'](archive,{n:{**v,'mode':'100644'} for n,v in expected.items()})
    need(read_regular(base/PDF,pin=files[PDF])==read_regular(base/'package'/freeze['package_pdf'],pin=files['package/'+freeze['package_pdf']]),'upload PDF differs from closed package PDF')
    return freeze


def inherited_findings(freeze,base=D):
    mapping=strict_json(read_regular(base/'FINDING_DISPOSITIONS.json',pin=freeze['files']['FINDING_DISPOSITIONS.json']))
    entries=mapping.get('findings',mapping.get('dispositions',mapping)) if type(mapping) is dict else mapping
    if type(entries) is list:
        need(all(type(x) is dict and type(x.get('id')) is str and x['id'] for x in entries),'inherited finding entries')
        ids=[x['id'] for x in entries]
    else:
        need(type(entries) is dict,'inherited finding mapping');ids=list(entries)
    need(len(ids)==len(INHERITED_FINDING_IDS) and set(ids)==INHERITED_FINDING_IDS,'all28 exact current inherited finding IDs separately identifiable')
    return set(ids)


def result_schema(result):
    required_record(result,{'pr':int,'problem_id':str,'original_pr_head':str,'reviewer_agent_id':str,'clean_context':bool,'full_reproducer_completed':bool,'entire_package_review':bool,'started_utc':str,'completed_utc':str,'candidate_revision':int,'candidate_pins':dict,'inspected_helper_hashes':dict,'required_issues':list,'optional_issues':list,'clean_for_preprint':bool,'strongest_verified_theorem':str,'prior_issue_resolution':dict,'inherited_finding_dispositions':dict},'whole-package RESULT')
    gap=result.get('mathematical_remaining_gap_for_stated_theorem','MISSING')
    need('mathematical_remaining_gap_for_stated_theorem' in result and (gap is None or type(gap) is str),'explicit theorem gap')
    need(result['pr']==PR and result['problem_id']==KEY and result['original_pr_head']==HEAD and result['candidate_revision']>=1,'review target/revision')
    need(bool(result['reviewer_agent_id'].strip()) and bool(result['strongest_verified_theorem'].strip()),'reviewer and strongest verified result/limitation')
    need(set(result['candidate_pins'])=={'freeze','manifest','pdf'} and all(type(x) is str and re.fullmatch('[0-9a-f]{64}',x) for x in result['candidate_pins'].values()),'review candidate exact pins')
    complete=all(result[k] for k in ('clean_context','full_reproducer_completed','entire_package_review'))
    note=result.get('nonclean_history')
    if note is not None:
        need(type(note) is dict and set(note)=={'status','explanation','checks_not_passed'} and note['status'] in ('incomplete','failed'),'honest nonclean history schema/status')
        need(type(note['explanation']) is str and bool(note['explanation'].strip()),'honest nonclean history explanation')
        checks=note['checks_not_passed']
        need(type(checks) is list and bool(checks) and all(type(x) is str and x.strip() for x in checks) and len(checks)==len(set(checks)),'honest nonclean unfinished/failed checks')
        need(result['clean_for_preprint'] is False,'nonclean history cannot claim clean')
    need(complete or note is not None,'incomplete completion flags need explicit honest history explanation')
    if result['clean_for_preprint']:
        need(complete and note is None and result['required_issues']==[] and result['optional_issues']==[] and gap is None,'clean claim needs complete entire review without findings/gap')
    return complete


def review_authentication(auth,pins,review_freeze,originals):
    required_record(auth,{'status':str,'utc':str,'original_pr_head':str,'freeze_sha256':str,'package_manifest_sha256':str,'future_helpers':dict,'candidate_files':dict,'originals':dict},'review authentication')
    status=auth['status']
    need(status in ('PASS','FAIL','INCOMPLETE','NOT_RUN'),'review authentication declared status')
    need(auth['original_pr_head']==HEAD and auth['freeze_sha256']==pins['freeze'] and auth['package_manifest_sha256']==pins['manifest'],'review authentication exact declared candidate')
    for field,expected in (('future_helpers',review_freeze['future_helpers']),('candidate_files',review_freeze['files'])):
        observed=auth[field]
        need(set(observed)<=set(expected) and all(exact(value,expected[name]) for name,value in observed.items()),'review authentication positive subset: '+field)
        if status=='PASS':need(exact(observed,expected),'PASS authentication entire '+field)
    need(set(auth['originals'])<=set(originals),'authentication original subset identity')
    if status=='PASS':need(set(auth['originals'])==set(originals),'PASS all33 original authentication')
    for path,item in auth['originals'].items():
        want=originals[path]
        need(type(item) is dict and all(type(item.get(k)) is type(v) and item.get(k)==v for k,v in want.items()) and item.get('archive_mode')=='100644' and item.get('disk_and_archive_match') is True,'positive Git/disk/ZIP original identity')
    if status!='PASS':
        required_record(auth,{'explanation':str,'observations':dict},'non-PASS authentication evidence')
        need(bool(auth['explanation'].strip()),'non-PASS authentication explanation')
        if status=='NOT_RUN':need(not auth['future_helpers'] and not auth['candidate_files'] and not auth['originals'],'NOT_RUN authentication cannot assert completed checks')
    return status=='PASS',utc(auth['utc'])


def review_cold(cold,pins,review_freeze,review_base):
    required_record(cold,{'status':str,'utc':str,'cold_extraction':bool,'package_manifest_sha256':str,'externally_pinned_verifier_sha256':str,'normalized_fields_ignored':list,'modes':list},'cold replay evidence')
    status=cold['status']
    need(status in ('PASS','FAIL','INCOMPLETE','NOT_RUN'),'cold replay declared status')
    need(cold['package_manifest_sha256']==pins['manifest'] and cold['externally_pinned_verifier_sha256']==review_freeze['files']['package/'+review_freeze['package_verifier']]['sha256'],'cold replay exact declared candidate/verifier')
    need(all(type(x) is str and x.strip() for x in cold['normalized_fields_ignored']),'cold replay ignored-field schema')
    modes=cold['modes'];labels=['normal','O','OO','env2'];options=dict(zip(labels,[0,1,2,0]))
    need(len(modes)<=4,'cold replay bounded mode observations')
    seen=[]
    for row in modes:
        required_record(row,{'mode':str},'cold replay mode')
        label=row['mode'];need(label in labels and label not in seen,'cold replay mode identity/duplicate');seen.append(label)
        need(set(('observed_outer_optimization','returncode','receipt'))<=set(row),'cold replay mode observation fields')
        opt,code,receipt=row['observed_outer_optimization'],row['returncode'],row['receipt']
        need((opt is None or (type(opt) is int and 0<=opt<=2)) and (code is None or type(code) is int) and (receipt is None or type(receipt) is dict),'typed actual cold mode observations')
        declared=row.get('status')
        need(declared is None or declared in ('PASS','FAIL','INCOMPLETE','NOT_RUN'),'cold mode declared status')
        if status=='PASS':need(declared in (None,'PASS'),'PASS cold cannot contain a declared non-PASS mode')
        if status=='PASS' or declared=='PASS':
            need(type(opt) is int and opt==options[label] and type(code) is int and code==0 and exact(receipt,load(review_base/('PACKAGE_REPLAY_'+label+'.json'))['receipt']),'PASS mode actual optimization/result/canonical receipt')
        if declared=='NOT_RUN':need(opt is None and code is None and receipt is None,'NOT_RUN mode cannot assert observations')
    if status=='PASS':
        need(seen==sorted(seen,key=labels.index),'PASS cold mode chronology')
        need(cold['cold_extraction'] is True and cold['normalized_fields_ignored']==[] and seen==labels,'PASS independent cold complete four-mode replay')
    else:
        required_record(cold,{'explanation':str,'observations':dict},'non-PASS cold evidence')
        need(bool(cold['explanation'].strip()),'non-PASS cold explanation')
        if status=='NOT_RUN':need(cold['cold_extraction'] is False and modes==[],'NOT_RUN cold replay cannot claim extraction or modes')
    return status=='PASS',utc(cold['utc'])


def review_own_attack(intake,attack,start,end):
    required_record(intake,{'status':str,'initial_attack_sha256':str},'first attack intake')
    need(intake['initial_attack_sha256']==sha(attack),'sealed independent first attack bytes')
    status=intake['status'];need(status in ('OWN_ATTACK_SAVED_BEFORE_PRIOR_ASSESSMENTS','FAIL','INCOMPLETE','NOT_RUN'),'own attack intake status')
    if status=='OWN_ATTACK_SAVED_BEFORE_PRIOR_ASSESSMENTS':
        required_record(intake,{'own_attack_completed_utc':str,'prior_assessments_opened_utc':str},'own attack chronology')
        need(start<=utc(intake['own_attack_completed_utc'])<utc(intake['prior_assessments_opened_utc'])<=end,'first attack predates prior assessments')
        return True
    required_record(intake,{'explanation':str,'observations':dict},'honest incomplete own attack')
    need(bool(intake['explanation'].strip()),'incomplete own attack explanation')
    if status=='NOT_RUN':need(intake.get('own_attack_completed_utc') is None and intake.get('prior_assessments_opened_utc') is None,'NOT_RUN intake no invented chronology')
    return False


def review_check(specs,freeze,freeze_pin,context):
    need(type(specs) is list and len(specs)>=2,'at least2 NEW whole-package reviews')
    need(all(type(s) is str and re.fullmatch(f'{i:02d}:[0-9a-f]{{64}}',s) for i,s in enumerate(specs,1)),'consecutive externally pinned review rounds')
    folder=A/'reviews'
    actual={x.name for x in folder.iterdir() if re.match(r'(?i)^\.*full_package_',x.name) is not None}
    need(actual=={'full_package_'+s.split(':')[0] for s in specs},'all numbered adverse/unfinished reviews must be supplied')
    prior=set();reviewers=set();last_end=None;rows=[];current_clean=[]
    mandatory={'RESULT.json','FULL_AUDIT.md','RESEARCH_LOG.md','AUTHENTICATION_START.json','AUTHENTICATION_END.json','COLD_REPLAY.json','INITIAL_ATTACK.md','PRIOR_ASSESSMENT_INTAKE.json'}
    originals=original_check();inherited=inherited_findings(freeze)
    for index,spec in enumerate(specs,1):
        number,pin=spec.split(':');base=folder/('full_package_'+number)
        raw=read_regular(base/'MANIFEST.json');need(sha(raw)==pin,'external complete review manifest')
        doc=strict_json(raw);records=doc.get('files');allowed=doc.get('explicit_public_allowlist')
        need(type(records) is dict and mandatory<=set(records) and type(allowed) is list and len(allowed)==len(set(allowed)) and set(allowed)==set(records) and 'MANIFEST.json' not in records,'sealed explicit review allowlist')
        captured={n:read_regular(base/n,pin=v) for n,v in records.items() if safe(n)}
        need(len(captured)==len(records) and all(captured[n].strip() for n in mandatory),'review paths/nonempty mandatory artifacts')
        result=strict_json(captured['RESULT.json']);complete=result_schema(result)
        rid=result['reviewer_agent_id'];need(rid not in reviewers,'distinct independent reviewers');reviewers.add(rid)
        start,end=utc(result['started_utc']),utc(result['completed_utc'])
        intake=strict_json(captured['PRIOR_ASSESSMENT_INTAKE.json'])
        intake_ok=review_own_attack(intake,captured['INITIAL_ATTACK.md'],start,end)
        need(start<end and (last_end is None or last_end<start),'sequential NEW review chronology');last_end=end
        pins=result['candidate_pins'];review_base=D;review_freeze=freeze
        if pins['freeze']!=freeze_pin:
            review_base=D/'reviewed_candidates'/('candidate'+str(result['candidate_revision']).zfill(2))
            review_freeze=freeze_check(read_regular(review_base/'FREEZE.json'),pins['freeze'],context,review_base,historical=True)
        need(result['candidate_revision']==review_freeze['revision_candidate'] and pins['manifest']==review_freeze['package_manifest_sha256'] and pins['pdf']==review_freeze['files'][PDF]['sha256'],'entire scientific/operational candidate identity')
        inspected=result['inspected_helper_hashes'];expected=review_freeze['future_helpers']
        need(set(inspected)<=set(expected) and all(exact(value,expected[name]) for name,value in inspected.items()),'partial inspected helper pins must bind exact candidate')
        if complete:need(exact(inspected,expected),'completed review entire inspected helper inventory')
        a_start,t_start=review_authentication(strict_json(captured['AUTHENTICATION_START.json']),pins,review_freeze,originals)
        a_end,t_end=review_authentication(strict_json(captured['AUTHENTICATION_END.json']),pins,review_freeze,originals)
        need(start<=t_start<=t_end<=end,'before/after review timestamps')
        cold_pass,t_cold=review_cold(strict_json(captured['COLD_REPLAY.json']),pins,review_freeze,review_base)
        need(t_start<=t_cold<=t_end,'cold observation outside authentication bracket')
        full_evidence=a_start and a_end and cold_pass and intake_ok
        if not complete or not full_evidence:
            need(result.get('nonclean_history') is not None and result['clean_for_preprint'] is False,'incomplete/failed evidence requires honest nonclean RESULT')
        for issues in (result['required_issues'],result['optional_issues']):
            need(all(type(x) is dict and type(x.get('id')) is str and x['id'] for x in issues),'every required/optional finding ID')
        issue_ids=[x['id'] for x in result['required_issues']+result['optional_issues']]
        need(len(issue_ids)==len(set(issue_ids)),'distinct IDs for every finding within review')
        def verified(mapping,key):
            value=mapping.get(key)
            return type(value) is dict and value.get('verified') is True and type(value.get('evidence')) is str and bool(value['evidence'].strip())
        clean_current=(pins['freeze']==freeze_pin and complete and full_evidence and result['clean_for_preprint'] is True and result.get('nonclean_history') is None)
        if clean_current:
            need(all(verified(result['prior_issue_resolution'],key) for key in prior|REQUIRED_ROOT_FINDING_IDS),'all earlier required/optional and required root operational findings independently dispositioned')
            need(all(verified(result['inherited_finding_dispositions'],key) for key in inherited),'fresh reviewers verify all inherited inherited dispositions')
            need(utc(freeze['created_utc'])<=start,'current review starts after freeze')
            current_clean.append(index)
        else:current_clean=[]
        prior.update(x['id'] for x in result['required_issues']+result['optional_issues'])
        rows.append({'round':index,'manifest_sha256':pin,'completed_utc':result['completed_utc'],'candidate_freeze_sha256':pins['freeze'],'required_issues':result['required_issues'],'optional_issues':result['optional_issues'],'completion_flags':{k:result[k] for k in ('clean_context','full_reproducer_completed','entire_package_review')},'evidence_statuses':{k:strict_json(captured[k])['status'] for k in ('AUTHENTICATION_START.json','AUTHENTICATION_END.json','COLD_REPLAY.json')},'nonclean_history':result.get('nonclean_history'),'eligible_clean_current':clean_current})
    need(len(current_clean)>=2 and current_clean[-1]==len(specs),'at least TWO fresh clean ENTIRE current-package reviews after every fix')
    return rows,result

def candidate_state_check(freeze,pin,context):
    fresh=capture_inventory(context['inventory_sha256'])
    need(fresh['captured']==context['captured'] and exact(fresh['inventory'],context['inventory']),'operations changed at action boundary')
    need(exact(freeze_check(read_regular(D/'FREEZE.json'),pin,fresh),freeze),'whole frozen payload changed at action boundary')


def accepted_review_check(accepted,freeze,context):
    need(exact(load(W/'ACCEPTANCE.json'),accepted),'canonical acceptance changed')
    specs=[f"{r['round']:02d}:"+r['manifest_sha256'] for r in accepted['full_package_reviews']]
    rows,latest=review_check(specs,freeze,accepted['freeze_sha256'],context)
    need(exact(rows,accepted['full_package_reviews']) and latest['strongest_verified_theorem']==accepted['exact_claim'],'accepted entire review chain changed')
    candidate_state_check(freeze,accepted['freeze_sha256'],context)
    # Re-read all sealed review bytes after whole-payload revalidation. No outside
    # service call intervenes before the caller's immediate next action.
    for spec in specs:
        number,pin=spec.split(':');base=A/'reviews'/('full_package_'+number)
        raw=read_regular(base/'MANIFEST.json');need(sha(raw)==pin,'final review seal')
        doc=strict_json(raw)
        for name,record in doc['files'].items():
            need(safe(name),'review closure path');read_regular(base/name,pin=record)
    need({x.name for x in (A/'reviews').iterdir() if re.match(r'(?i)^\.*full_package_',x.name) is not None}=={'full_package_'+s.split(':')[0] for s in specs},'review directory history changed')


def accepted_package(context):
    accepted=load(W/'ACCEPTANCE.json')
    need(accepted.get('schema')=='pr952-whole-package-acceptance-v1' and accepted.get('accepted') is True and accepted.get('pr')==PR and type(accepted['pr']) is int and accepted.get('problem_id')==KEY and accepted.get('original_pr_head')==HEAD and accepted.get('operations_inventory_sha256')==context['inventory_sha256'],'current whole-package acceptance')
    need(exact(accepted.get('required_root_operational_findings'),sorted(REQUIRED_ROOT_FINDING_IDS)),'accepted required root operational findings')
    need(accepted.get('proof_gap','MISSING') is None and accepted.get('all_prior_required_and_optional_findings_resolved') is True and accepted.get('original_declared_turns')=='1/5' and accepted.get('historical_native_turn_count')=='UNKNOWN' and type(accepted.get('new_author_proof_responses')) is int and accepted['new_author_proof_responses']==0,'honest acceptance scope/turns')
    freeze=freeze_check(read_regular(D/'FREEZE.json'),accepted['freeze_sha256'],context)
    need(exact(accepted.get('files'),freeze['files']) and exact(accepted.get('future_helpers'),freeze['future_helpers']),'accepted final payload')
    accepted_review_check(accepted,freeze,context)
    return accepted,freeze


def accept(args,context):
    need(not (W/'ACCEPTANCE.json').exists(),'existing acceptance: never overwrite')
    freeze=freeze_check(read_regular(D/'FREEZE.json'),args.freeze,context)
    before=premerge_gate(freeze,require_draft=True)
    rows,latest=review_check(args.review,freeze,args.freeze,context)
    after=premerge_gate(freeze,require_draft=True)
    accepted={'schema':'pr952-whole-package-acceptance-v1','utc':utc_now(),'accepted':True,'pr':PR,'problem_id':KEY,'original_pr_head':HEAD,'original_declared_turns':'1/5','historical_native_turn_count':'UNKNOWN','author_native_history_authenticated':False,'original_total_attempt_count_known':False,'new_author_proof_responses':0,'operations_inventory_sha256':context['inventory_sha256'],'freeze_sha256':args.freeze,'files':freeze['files'],'future_helpers':freeze['future_helpers'],'package_manifest_sha256':freeze['package_manifest_sha256'],'full_package_reviews':rows,'exact_claim':latest['strongest_verified_theorem'],'proof_gap':None,'all_prior_required_and_optional_findings_resolved':True,'inherited_finding_count':len(inherited_findings(freeze)),'required_root_operational_findings':sorted(REQUIRED_ROOT_FINDING_IDS),'AI_assisted':True,'unrefereed':True,'independent_human_peer_review':False,'formal_machine_proof_certification':False,'priority_limit':'Bounded primary audit with retained access gaps; no novelty, firstness, or current-open certificate.'}
    save(W/'FINAL_ACCEPTANCE_GATE.json',{'utc':utc_now(),'before':before,'after':after})
    candidate_state_check(freeze,args.freeze,context)
    # Revalidate the complete review closure immediately before authoritative approval.
    checked,_=review_check(args.review,freeze,args.freeze,context)
    need(exact(checked,rows),'review chain changed at approval boundary')
    candidate_state_check(freeze,args.freeze,context)
    save(W/'ACCEPTANCE.json',accepted,exclusive=True)
    print(json.dumps({'accepted':True,'pr':PR,'freeze_sha256':args.freeze,'whole_package_reviews':len(rows)}))


def _merged_gate(accepted,freeze):
    saved=load(W/'PR_MERGE_RECEIPT.json');main_destination(saved,merged=True)
    before=pr_view();numbered_receipt('MERGED_BEFORE',{'utc':utc_now(),'before':before});main_destination(before,merged=True)
    need(exact(before['mergeCommit'],saved['mergeCommit']),'merged commit changed')
    commit=before['mergeCommit']['oid'];parent=remote_main()
    if not READ_ONLY:run(['git','fetch','--no-write-fetch-head','origin',commit])
    run(['git','merge-base','--is-ancestor',commit,parent])
    source=source_gate(parent);original_check(commit)
    allowed=None
    if (W/'NATIVE_PUBLICATION_RECEIPT.json').exists():
        native=load(W/'NATIVE_PUBLICATION_RECEIPT.json')
        need(native.get('push_confirmed') is True and native.get('accepted_freeze_sha256')==accepted['freeze_sha256'],'native receipt current freeze')
        allowed=native['published_event']
    native=native_safety(parent,allowed)
    parents=run(['git','show','-s','--format=%P',commit]).split()
    need(len(parents)==2 and parents[1]==HEAD,'ordinary two-parent exact original-head merge')
    need(queue_parts(blob(parents[0],QUEUE))[0]==queue_parts(blob(commit,QUEUE))[0],'merge altered unrelated queue bytes')
    claimed_row(blob(commit,QUEUE))
    after=pr_view();bracket=observation_bracket(before,after,merged=True)
    observed_after=remote_main()
    numbered_receipt('MERGED_BRACKET',{**bracket,'source_parent':parent,'remote_main_after':observed_after,'source':source,'native':native,'parents':parents})
    need(bracket['authority_equal'],'stable merged PR identity changed across readback')
    need(parent==observed_after,'main advanced within merged source/native bracket; restart fresh gate')
    run(['git','merge-base','--is-ancestor',commit,observed_after])
    return {'utc':utc_now(),'baseRefName':'main','actual_PR_readback':after,'merge_commit':commit,'observed_remote_main':parent,'merge_parents':parents,'merge_commit_is_ancestor_of_observed_main':True,'source_gate':source,'native_gate':native,'bracket':bracket}

def merged_gate(accepted,freeze):
    try:return _merged_gate(accepted,freeze)
    except Exception as error:
        failure={'utc':utc_now(),'error':str(error),'status':'FAIL_OR_INCOMPLETE_NO_CLEAN_CREDIT'}
        try:failure['after_failure']=pr_view()
        except Exception as after_error:failure['after_readback_error']=str(after_error)
        numbered_receipt('MERGED_FAILURE',failure)
        raise


def merge(args,context):
    accepted,freeze=accepted_package(context);live=pr_view()
    if live.get('state')!='MERGED':
        need(not (W/'PR_MERGE_INTENT.json').exists(),'uncertain previous merge: exact PR readback only, never repeat')
        gate=premerge_gate(freeze)
        if gate['pr']['isDraft']:
            need(not (W/'PR_READY_INTENT.json').exists(),'previous ready intent with still-draft PR requires reconciliation')
            accepted_review_check(accepted,freeze,context);gate=premerge_gate(freeze)
            save(W/'PR_READY_INTENT.json',{'utc':utc_now(),'expected_head':HEAD,'freeze_sha256':accepted['freeze_sha256'],'gate':gate,'blind_retry_permitted':False},exclusive=True)
            result=subprocess.run(['gh','pr','ready',str(PR),'--repo','AlecKriebel/Math'],cwd=ROOT,capture_output=True,text=True)
            save(W/'PR_READY_ACTION.json',{'utc':utc_now(),'returncode':result.returncode,'stdout':result.stdout,'stderr':result.stderr},exclusive=True)
            ready=pr_view();save(W/'PR_READY_READBACK.json',ready,exclusive=True);main_destination(ready)
            need(ready['isDraft'] is False,'ready outcome unconfirmed: exact readback only')
        accepted_review_check(accepted,freeze,context);gate=premerge_gate(freeze)
        need(gate['pr'].get('mergeable')=='MERGEABLE' and gate['pr']['isDraft'] is False,'fresh premerge MERGEABLE/ready required')
        save(W/'PR_MERGE_INTENT.json',{'utc':utc_now(),'expected_head':HEAD,'freeze_sha256':accepted['freeze_sha256'],'gate':gate,'blind_retry_permitted':False},exclusive=True)
        result=subprocess.run(['gh','pr','merge',str(PR),'--repo','AlecKriebel/Math','--merge','--match-head-commit',HEAD],cwd=ROOT,capture_output=True,text=True)
        save(W/'PR_MERGE_ACTION.json',{'utc':utc_now(),'returncode':result.returncode,'stdout':result.stdout,'stderr':result.stderr},exclusive=True)
        live=pr_view();save(W/'PR_MERGE_ACTION_READBACK.json',live,exclusive=True)
    main_destination(live,merged=True)
    if (W/'PR_MERGE_RECEIPT.json').exists():need(exact(load(W/'PR_MERGE_RECEIPT.json')['mergeCommit'],live['mergeCommit']),'existing merge receipt conflict')
    else:save(W/'PR_MERGE_RECEIPT.json',live,exclusive=True)
    destination=merged_gate(accepted,freeze);accepted_review_check(accepted,freeze,context)
    numbered_receipt('MERGED_PACKET_INTEGRITY',{**destination,'original33_byte_identical':True,'unrelated_queue_bytes_preserved':True,'original_declared_turns':'1/5','historical_native_turn_count':'UNKNOWN','new_author_proof_responses':0})
    print(json.dumps({'state':'MERGED','merge_commit':live['mergeCommit']['oid']}))

def descriptor_check(freeze):
    doc=strict_json(read_regular(D/'zenodo-deposit.json',pin=freeze['files']['zenodo-deposit.json']))
    need(set(doc)=={'metadata','files'} and type(doc['metadata']) is dict and type(doc['files']) is list and len(doc['files'])==2,'exact kit descriptor')
    expected=[]
    for item in doc['files']:
        need(type(item) is dict and set(item)=={'path','name'} and item['path'] in (PDF,ZIP) and item['name']==item['path'],'exact named PDF/archive only')
        pin=freeze['files'][item['path']];read_regular(D/item['path'],pin=pin)
        expected.append({'name':item['name'],'size':pin['bytes'],'sha256':pin['sha256']})
    need({x['name'] for x in expected}=={PDF,ZIP},'two distinct accepted uploads')
    meta=doc['metadata']
    need(meta.get('title')==TITLE and meta.get('version')=='1.0' and meta.get('upload_type')=='publication' and meta.get('publication_type')=='preprint' and meta.get('license')=='cc-by-4.0' and meta.get('creators')==[{'name':'Kriebel, Alec','affiliation':'Independent researcher','orcid':'0009-0001-9320-500X'}],'exact preprint/title/author/license/version')
    text=(str(meta.get('description',''))+' '+str(meta.get('notes',''))).lower()
    need('unrefereed' in text and 'ai' in text and 'human' in text and 'formal' in text and 'novelty' in text,'publication disclosure and bounded claims')
    return doc,expected


def captured_kit(context):
    namespace={'__name__':'_pr952_authenticated_original_kit_','__file__':str(ROOT/KIT)}
    exec(compile(context['captured'][KIT],str(ROOT/KIT),'exec',dont_inherit=True,optimize=0),namespace)
    return namespace


def runtime_upload_copy(freeze):
    runtime=W/'runtime'
    runtime.mkdir(mode=0o700,exist_ok=True)
    need(runtime.is_dir() and not runtime.is_symlink() and stat.S_IMODE(runtime.stat().st_mode)==0o700,'stable private runtime')
    for name in ['zenodo-deposit.json',PDF,ZIP]:
        raw=read_regular(D/name,pin=freeze['files'][name]);target=runtime/name
        try:fd=os.open(target,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o400)
        except FileExistsError:read_regular(target,pin=freeze['files'][name])
        else:
            with os.fdopen(fd,'wb') as stream:stream.write(raw)
            read_regular(target,pin=freeze['files'][name])
    return runtime/'zenodo-deposit.json'


def exact_remote_metadata(deposit,expected):
    need(type(deposit) is dict and type(deposit.get('metadata')) is dict,'remote metadata object')
    need(all(k in deposit['metadata'] and exact(deposit['metadata'][k],v) for k,v in expected.items()),'remote supplied metadata differs; no adapter normalization')
    return deposit


class GuardedZenodoClient:
    """Guard every service boundary and permit at most one create/publish POST."""
    def __init__(self,client,kit,metadata,files,guard,action,ident=None):
        self.client,self.kit,self.metadata,self.files=client,kit,metadata,files
        self.guard,self.action,self.ident=guard,action,ident
        self.created=0;self.published=0;self.normalizations=[]
    def create(self,metadata):
        need(self.action=='stage' and self.ident is None and self.created==0 and exact(metadata,self.metadata),'one new draft only')
        self.guard();save(W/'ZENODO_CREATE_POST_INTENT.json',{'utc':utc_now(),'metadata':metadata,'create_POST_count':1,'blind_retry_permitted':False},exclusive=True);self.created+=1
        result=self.client.create(metadata)
        need(type(result.get('id')) is int and result['id']>0,'created integer ID')
        self.ident=result['id'];save(W/'ZENODO_CREATED_ID.json',{'utc':utc_now(),'id':self.ident,'metadata_sha256':sha(json.dumps(metadata,sort_keys=True).encode()),'blind_retry_permitted':False},exclusive=True);return result
    def get(self,ident):
        need(type(ident) is int and ident>0 and (self.ident is None or ident==self.ident),'exact existing deposition ID')
        self.ident=ident;self.guard();result=self.client.get(ident)
        self.kit['validate_record'](result,ident)
        return exact_remote_metadata(result,self.metadata)
    def upload(self,bucket,entry):
        need(self.action=='stage' and self.ident is not None and entry in self.files,'stage exact authenticated upload')
        self.guard();save(W/('ZENODO_UPLOAD_'+entry['name']+'_INTENT.json'),{'utc':utc_now(),'id':self.ident,'name':entry['name'],'size':entry['size'],'sha256':entry['sha256'],'blind_retry_permitted':False},exclusive=True);return self.client.upload(bucket,entry)
    def update(self,ident,metadata):
        need(self.action=='stage' and ident==self.ident and exact(metadata,self.metadata),'stage exact metadata')
        self.guard();save(W/'ZENODO_METADATA_PUT_INTENT.json',{'utc':utc_now(),'id':ident,'metadata':metadata,'blind_retry_permitted':False},exclusive=True);return self.client.update(ident,metadata)
    def publish(self,ident):
        need(self.action=='publish' and ident==self.ident and self.published==0,'one exact-ID publish POST')
        fresh=self.get(ident);self.kit['verify'](fresh,self.metadata,self.files)
        self.guard()
        if fresh['submitted']:return fresh
        save(W/'ZENODO_PUBLISH_POST_INTENT.json',{'utc':utc_now(),'id':ident,'publish_POST_count':1,'blind_retry_permitted':False},exclusive=True)
        self.published+=1;return self.client.publish(ident)


def validate_zenodo_receipt(receipt,expected,title,action,ident=None):
    need(type(receipt) is dict and receipt.get('environment')=='production' and receipt.get('title')==title and exact(receipt.get('files'),expected),'exact kit receipt metadata/environment/files')
    rid=receipt.get('id');need(type(rid) is int and rid>0 and (ident is None or rid==ident),'actual exact deposition ID')
    if action=='stage':need(receipt.get('state')=='ready_to_publish','unpublished verified stage')
    elif action in ('publish','inspect-public'):
        need(receipt.get('state')=='published' and receipt.get('doi')==f'10.5281/zenodo.{rid}' and receipt.get('record_url')==f'https://zenodo.org/records/{rid}','actual public exact DOI/record')
    else:need(receipt.get('state') in ('published','ready_to_publish'),'inspect state')
    return rid


def bounded_public_get(url,cap):
    parsed=urlsplit(url)
    need(parsed.scheme=='https' and parsed.hostname in ('zenodo.org','doi.org') and not parsed.username and not parsed.password,'public verifier HTTPS host')
    with urlopen(Request(url,headers={'User-Agent':'Math-PR952-public-verifier/1.0'}),timeout=30) as response:
        final=urlsplit(response.url)
        need(final.scheme=='https' and final.hostname=='zenodo.org','public response final Zenodo HTTPS URL')
        raw=response.read(cap+1);need(len(raw)<=cap,'public response size cap')
        return raw,response.url,response.status


def independent_public_verify(receipt,expected):
    rid=receipt['id'];doi=receipt['doi']
    raw,_,code=bounded_public_get(f'https://zenodo.org/api/records/{rid}',1024*1024)
    record=strict_json(raw)
    need(code==200 and str(record.get('id'))==str(rid) and record.get('doi')==doi and record.get('metadata',{}).get('title')==TITLE,'independent public record identity/DOI/title')
    files=record.get('files');need(type(files) is list and len(files)==2 and all(type(x) is dict for x in files) and {x.get('key') for x in files}=={x['name'] for x in expected},'independent public file set')
    checked=[]
    for want in expected:
        name=want['name'];data,final,status=bounded_public_get(f'https://zenodo.org/records/{rid}/files/{name}?download=1',want['size'])
        need(status==200 and len(data)==want['size'] and sha(data)==want['sha256'],'independent public downloaded bytes '+name)
        checked.append({**want,'verified_url':final})
    _,resolved,status=bounded_public_get('https://doi.org/'+doi,1024*1024)
    need(status==200 and urlsplit(resolved).path.rstrip('/')==f'/records/{rid}','independent DOI resolution exact record')
    return {'utc':utc_now(),'id':rid,'doi':doi,'public_record_sha256':sha(raw),'files':checked,'doi_resolved_url':resolved,'no_API_token_sent':True,'confirmed':True}


def zenodo(args,context):
    accepted,freeze=accepted_package(context);destination=merged_gate(accepted,freeze)
    descriptor,expected=descriptor_check(freeze);kit=captured_kit(context)
    runtime=runtime_upload_copy(freeze);metadata,files=kit['load_manifest'](runtime)
    need(exact(metadata,descriptor['metadata']),'actual unchanged kit manifest readback')
    dry=kit['run'](argparse.Namespace(command='check',manifest=runtime,sandbox=False))
    need(exact(dry,{'environment':'production','title':TITLE,'files':expected}),'unchanged kit dry-run')
    numbered_receipt('ZENODO_KIT_DRY_RUN',dry)
    place,state=kit['local_state'](runtime.resolve(),'production')
    action=args.action;ident=state.get('id') if state else None
    saved_id=load(W/'ZENODO_CREATED_ID.json') if (W/'ZENODO_CREATED_ID.json').exists() else None
    if saved_id is not None:
        need(type(saved_id.get('id')) is int and saved_id['id']>0 and saved_id.get('metadata_sha256')==sha(json.dumps(metadata,sort_keys=True).encode()),'durable created ID/metadata linkage')
        need((W/'ZENODO_CREATE_POST_INTENT.json').exists(),'saved ID without create intent')
        need(ident is None or ident==saved_id['id'],'kit state ID differs from durable created ID')
        ident=saved_id['id']
    else:need(state is None,'kit state has no authenticated durable create ID; explicit account reconciliation required')
    need(ident is None or (type(ident) is int and ident>0),'persisted exact existing ID')
    if action=='stage':
        need(state is None and saved_id is None and not (W/'ZENODO_CREATE_POST_INTENT.json').exists(),'new stage only: reconcile prior exact saved ID, never create replacement')
    else:need(saved_id is not None,'inspect/publish requires durable exact created ID')
    if action=='publish':
        stage=load(W/'ZENODO_STAGE.json');validate_zenodo_receipt(stage,expected,TITLE,'stage',ident)
        need(state is not None and state['id']==ident,'publish same stable kit state')
    intent_path=W/('ZENODO_'+action.upper()+'_INTENT.json')
    intent={'utc':utc_now(),'action':action,'pr':PR,'original_pr_head':HEAD,'accepted_freeze_sha256':accepted['freeze_sha256'],'operations_inventory_sha256':context['inventory_sha256'],'descriptor_sha256':freeze['files']['zenodo-deposit.json']['sha256'],'repository_kit_sha256':context['inventory']['files'][KIT]['sha256'],'runtime_manifest':runtime.relative_to(ROOT).as_posix(),'merged_commit':destination['merge_commit'],'merged_base':'main','destination_readback':destination,'existing_deposition_id':ident,'blind_retry_permitted':False}
    if action in ('stage','publish'):save(intent_path,intent,exclusive=True)
    else:numbered_receipt('ZENODO_INSPECT_INTENT',intent)
    def guard():
        merged_gate(accepted,freeze);accepted_review_check(accepted,freeze,context)
        for name in ['zenodo-deposit.json',PDF,ZIP]:read_regular(runtime.parent/name,pin=freeze['files'][name])
    guard()
    client=GuardedZenodoClient(kit['ZenodoClient']('production',kit['token_for']('production')),kit,metadata,files,guard,action,ident)
    try:
        if action=='inspect' and state is None:
            # GET the durable exact returned ID first; never list/search/create.
            observed=client.get(ident);kit['verify'](observed,metadata,files)
            kit['save_state'](place,{'manifest':str(runtime.resolve()),'environment':'production','id':ident})
        receipt=kit['run'](argparse.Namespace(command=action,manifest=runtime,sandbox=False,confirm_id=ident,check_doi=False),client=client)
        validate_zenodo_receipt(receipt,expected,TITLE,action,ident)
    except Exception as error:
        numbered_receipt('ZENODO_'+action.upper()+'_FAILURE',{**intent,'error':str(error),'exact_observed_id':client.ident,'create_POST_count':client.created,'publish_POST_count':client.published,'instruction':'GET exact durable saved ID only. No repeated mutation. Lost create response without any returned ID requires explicit account reconciliation.'})
        raise
    receipt['adapter_metadata_normalizations']=[]
    receipt['accepted_freeze_sha256']=accepted['freeze_sha256'];receipt['operations_inventory_sha256']=context['inventory_sha256'];receipt['merged_commit']=destination['merge_commit']
    guard()
    if action in ('stage','publish'):save(W/('ZENODO_'+action.upper()+'.json'),receipt,exclusive=True)
    else:
        numbered_receipt('ZENODO_INSPECT_OBSERVATION',receipt);save(W/'ZENODO_INSPECT.json',receipt)
        # Recovery is GET-only and requires the exact durable corresponding intent.
        if receipt['state']=='ready_to_publish' and (W/'ZENODO_STAGE_INTENT.json').exists() and not (W/'ZENODO_STAGE.json').exists():
            recovered={**receipt,'recovered_by_exact_saved_ID_GET':True};save(W/'ZENODO_STAGE.json',recovered,exclusive=True)
        if receipt['state']=='published' and (W/'ZENODO_PUBLISH_INTENT.json').exists() and not (W/'ZENODO_PUBLISH.json').exists():
            published_intent=load(W/'ZENODO_PUBLISH_INTENT.json')
            need(published_intent.get('existing_deposition_id')==ident and published_intent.get('accepted_freeze_sha256')==accepted['freeze_sha256'],'exact publish intent reconciliation')
            save(W/'ZENODO_PUBLISH.json',{**receipt,'recovered_by_exact_saved_ID_GET':True},exclusive=True)
    if receipt['state']=='published':
        public=independent_public_verify(receipt,expected);guard();numbered_receipt('ZENODO_PUBLIC_OBSERVATION',public);save(W/'ZENODO_PUBLIC_VERIFICATION.json',public)
    print(json.dumps({'action':action,'id':receipt['id'],'state':receipt['state'],'doi':receipt.get('doi')}))

def valid_tracker_range(value):
    match=re.fullmatch(r"'Math Puzzles'!A([1-9][0-9]*):D\1",value) if type(value) is str else None
    return match is not None and int(match[1])>=2


def publication_links(accepted,freeze,tracker=None,native=None):
    descriptor,expected=descriptor_check(freeze)
    stage=load(W/'ZENODO_STAGE.json');published=load(W/'ZENODO_PUBLISH.json');inspection=load(W/'ZENODO_INSPECT.json')
    rid=validate_zenodo_receipt(stage,expected,TITLE,'stage')
    for receipt in (published,inspection):
        validate_zenodo_receipt(receipt,expected,TITLE,'inspect-public',rid)
        need(receipt.get('accepted_freeze_sha256')==accepted['freeze_sha256'] and receipt.get('operations_inventory_sha256')==accepted['operations_inventory_sha256'],'publication/current freeze operations linkage')
    merge=load(W/'PR_MERGE_RECEIPT.json');main_destination(merge,merged=True)
    intent=load(W/'ZENODO_PUBLISH_INTENT.json')
    need(intent.get('accepted_freeze_sha256')==accepted['freeze_sha256'] and intent.get('operations_inventory_sha256')==accepted['operations_inventory_sha256'] and intent.get('descriptor_sha256')==freeze['files']['zenodo-deposit.json']['sha256'] and intent.get('merged_base')=='main' and intent.get('merged_commit')==merge['mergeCommit']['oid'] and published.get('merged_commit')==merge['mergeCommit']['oid'] and inspection.get('merged_commit')==merge['mergeCommit']['oid'],'publish intent exact approved main merge')
    public=load(W/'ZENODO_PUBLIC_VERIFICATION.json')
    need(public.get('confirmed') is True and type(public.get('id')) is int and public['id']==rid and public.get('doi')==published['doi'] and public.get('no_API_token_sent') is True and [{k:x[k] for k in ('name','size','sha256')} for x in public.get('files',[])]==expected,'independent public file/DOI verification')
    if tracker is not None:
        need(tracker.get('confirmed') is True and tracker.get('readback_matches') is True and type(tracker.get('pr')) is int and tracker['pr']==PR and tracker.get('problem_id')==KEY and tracker.get('original_pr_head')==HEAD and tracker.get('accepted_freeze_sha256')==accepted['freeze_sha256'] and tracker.get('merge_commit')==merge['mergeCommit']['oid'] and tracker.get('merged_base')=='main' and tracker.get('doi')==published['doi'] and tracker.get('zenodo_record_id')==rid and tracker.get('spreadsheet_id')==SID and tracker.get('gid')==1254632077 and tracker.get('tab_title')=='Math Puzzles' and valid_tracker_range(tracker.get('updated_range')),'tracker exact publication/target linkage')
        saved=load(W/'TRACKER_READBACK.json')
        need(saved.get('range')==tracker['updated_range'] and saved.get('values')==[tracker.get('row')] and tracker.get('row')==tracker_row(published),'four-column exact tracker readback')
    if native is not None:
        event=native.get('published_event',{})
        need(tracker is not None and native.get('push_confirmed') is True and event.get('id')==KEY and event.get('doi')==published['doi'] and event.get('accepted_freeze_sha256')==accepted['freeze_sha256'] and event.get('merged_commit')==merge['mergeCommit']['oid'] and event.get('tracker_range')==tracker['updated_range'],'native event exact DOI/freeze/merge/tracker linkage')
    return published,merge


def gws(args):
    return strict_json(run(['gws',*args]))


def publication_note(publication):
    return ("10400145 / AMR-103-0145. "+TITLE+". "
        "First-order algebraic obstruction to the literal rank interpolation statement; the exact scope and quantum-topological input are stated in the paper. "
        "Bounded primary priority audit with retained access gaps; novelty, firstness and current openness unestablished. "
        "Extensive AI assistance; unrefereed; no independent human peer review or formal proof certification. "
        "All33 original files preserved. PR-declared1/5 retained separately; native history and total historical count UNKNOWN; zero new author proof responses. "
        "https://github.com/AlecKriebel/Math/pull/952 DOI "+publication['doi'])

def tracker_row(publication):
    return ['https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf','', 'https://doi.org/'+publication['doi'],publication_note(publication)]

def duplicate_tracker(values,row):
    need(type(values) is list and values and values[0]==['Original Problem','Solution Chat URL','DOI','Notes'],'exact four tracker headers')
    # Match problem identity, DOI, title or PR anchor: a different
    # DOI/title for this same target requires reconciliation, never a second row.
    anchors=[KEY,'AMR-103-0145',TITLE.lower(),'github.com/AlecKriebel/Math/pull/952',row[2]]
    hits=[(i+1,r) for i,r in enumerate(values[1:],1) if any(any(a.lower() in str(v).lower() for a in anchors) for v in r)]
    if hits:
        need(len(hits)==1 and hits[0][1]==row,'existing target/DOI row differs: reconcile, do not append')
        return hits[0][0]
    return None


def tracker_append(args,context):
    accepted,freeze=accepted_package(context);merged_gate(accepted,freeze)
    publication,merge=publication_links(accepted,freeze);row=tracker_row(publication)
    meta=gws(['sheets','spreadsheets','get','--params',json.dumps({'spreadsheetId':SID,'fields':'sheets.properties'})])
    matches=[x.get('properties') for x in meta.get('sheets',[]) if x.get('properties',{}).get('sheetId')==1254632077]
    need(len(matches)==1 and matches[0].get('title')=='Math Puzzles','exact spreadsheet gid/title')
    table="'Math Puzzles'!A:D"
    existing=gws(['sheets','spreadsheets','values','get','--params',json.dumps({'spreadsheetId':SID,'range':table})])
    save(W/'tracker_existing_rows_private.json',existing)
    index=duplicate_tracker(existing.get('values'),row)
    if index:
        updated=f"'Math Puzzles'!A{index}:D{index}";response={'recovered_existing_identical_row':True}
    else:
        need(not (W/'TRACKER_APPEND_INTENT.json').exists(),'uncertain prior append with no exact row: reconcile without repeating')
        params={'spreadsheetId':SID,'range':table,'valueInputOption':'RAW','insertDataOption':'INSERT_ROWS'}
        save(W/'TRACKER_APPEND_INTENT.json',{'utc':utc_now(),'params':params,'row':row,'accepted_freeze_sha256':accepted['freeze_sha256'],'blind_retry_permitted':False},exclusive=True)
        merged_gate(accepted,freeze);accepted_review_check(accepted,freeze,context)
        response=gws(['sheets','spreadsheets','values','append','--params',json.dumps(params),'--json',json.dumps({'values':[row]})])
        save(W/'TRACKER_APPEND_RESPONSE.json',response)
        updates=response.get('updates',{})
        need(type(updates.get('updatedRows')) is int and updates['updatedRows']==1 and type(updates.get('updatedCells')) is int and updates['updatedCells']==4,'exact appended row dimensions')
        updated=updates.get('updatedRange')
    need(valid_tracker_range(updated),'single quoted A:D data row')
    readback=gws(['sheets','spreadsheets','values','get','--params',json.dumps({'spreadsheetId':SID,'range':updated})])
    need(readback.get('range')==updated and readback.get('values')==[row],'exact appended/recovered row readback')
    save(W/'TRACKER_READBACK.json',readback)
    # A second full-table read catches an intervening duplicate, without writing.
    final=gws(['sheets','spreadsheets','values','get','--params',json.dumps({'spreadsheetId':SID,'range':table})])
    need(duplicate_tracker(final.get('values'),row)==int(re.search(r'A([0-9]+):',updated)[1]),'duplicate/intervening row conflict')
    receipt={'utc':utc_now(),'confirmed':True,'readback_matches':True,'pr':PR,'problem_id':KEY,'original_pr_head':HEAD,'merged_base':'main','merge_commit':merge['mergeCommit']['oid'],'accepted_freeze_sha256':accepted['freeze_sha256'],'zenodo_record_id':publication['id'],'doi':publication['doi'],'spreadsheet_id':SID,'gid':1254632077,'tab_title':'Math Puzzles','updated_range':updated,'row':row,'append_result':response,'cli':'Google Workspace CLI gws'}
    accepted_review_check(accepted,freeze,context);save(W/'TRACKER_RECEIPT.json',receipt)
    publication_links(accepted,freeze,receipt)
    print(json.dumps({'confirmed':True,'updated_range':updated,'doi':publication['doi']}))


def native_event(accepted,publication,merge,tracker):
    # Import the conservative PR-declared counter to avoid the native renderer's
    # missing-field default0. It is NOT an authenticated native per-turn count;
    # do not create candidate_turn or historical proof-attempt events.
    return {'at':utc_now(),'id':KEY,'status':'preprint_published','note':publication_note(publication),'doi':publication['doi'],'pr':PR,'event':'audited_imported_candidate_publication','event_id':f"pr952_zenodo{publication['id']}_v1.0",'statement_hash':STATEMENT,'review_hash':REVIEW,'original_declared_turns':'1/5','turns_used':1,'turns_used_basis':'Imported immutable PR declaration1/5; native per-turn count is not authenticated','historical_native_turn_count':'UNKNOWN','original_total_attempt_count_known':False,'author_native_history_authenticated':False,'new_author_proof_responses':0,'proof_search_turns_added_by_audit':0,'turn_limit':5,'turn_count_status':'PR_declared1of5_not_independently_reconstructed','original_pr_head':HEAD,'accepted_freeze_sha256':accepted['freeze_sha256'],'merged_commit':merge['mergeCommit']['oid'],'merged_base':'main','zenodo_record_id':publication['id'],'tracker_range':tracker['updated_range'],'priority_limit':'Bounded search with access gaps; novelty, firstness and current openness unestablished','AI_assisted':True,'unrefereed':True,'independent_human_peer_review':False,'formal_machine_proof_certification':False}


def native_replacements(queue,state,history,event):
    """Return exact narrow replacements; every unrelated original byte survives."""
    claimed_row(queue)
    _,old,index,lines=queue_parts(queue)
    cells=old.decode().rstrip('\r\n').split('|')
    cells[8]=' preprint_published '
    cells[11]=' '+cells[11].strip()+' '+event['note'].replace('|','/')+' '
    cells[12]=f" [{event['doi']}](https://doi.org/{event['doi']}) "
    ending='\r\n' if old.endswith(b'\r\n') else '\n' if old.endswith(b'\n') else ''
    revised=('|'.join(cells)+ending).encode();lines[index]=revised;new_queue=b''.join(lines)
    need(queue_parts(queue)[0]==queue_parts(new_queue)[0],'unrelated QUEUE bytes changed')
    before=old.decode().rstrip('\r\n').split('|');after=revised.decode().rstrip('\r\n').split('|')
    need(all(before[i]==after[i] for i in range(len(before)) if i not in (8,11,12)),'another target QUEUE cell changed')
    new_state=replace_entry(state.decode(),KEY,event).encode()
    # Appended separator is new data; the old history remains an exact prefix.
    new_history=history+(b'' if not history or history.endswith(b'\n') else b'\n')+json.dumps(event,ensure_ascii=False,allow_nan=False).encode()+b'\n'
    need(new_history.startswith(history),'history prefix changed')
    return {QUEUE:new_queue,STATE:new_state,HISTORY:new_history}


def native_write(args,context):
    need(not (W/'NATIVE_PUBLICATION_RECEIPT.json').exists(),'native receipt exists: readback/reconcile')
    accepted,freeze=accepted_package(context);merged_gate(accepted,freeze)
    tracker=load(W/'TRACKER_RECEIPT.json');publication,merge=publication_links(accepted,freeze,tracker)
    # Persist a per-attempt intent BEFORE object creation or push. An uncertain
    # push is read back by exact commit before deciding whether a retry is safe.
    for attempt in range(1,7):
        intent_path=W/f'NATIVE_PUBLICATION_CAS_{attempt:02d}_INTENT.json'
        if intent_path.exists():
            intent=load(intent_path);prepared=load(W/f'NATIVE_PUBLICATION_CAS_{attempt:02d}_PREPARED.json');commit=prepared.get('commit');intent={**intent,**prepared}
            need(type(commit) is str,'existing native intent requires explicit exact-commit reconciliation')
            if (W/f'NATIVE_PUBLICATION_CAS_{attempt:02d}_DEFINITIVE_RACE.json').exists():
                race=load(W/f'NATIVE_PUBLICATION_CAS_{attempt:02d}_DEFINITIVE_RACE.json');need(race.get('not_pushed_commit')==commit,'CAS race exact commit');continue
            observed=remote_main()
            probe=subprocess.run(['git','merge-base','--is-ancestor',commit,observed],cwd=ROOT,capture_output=True)
            need(probe.returncode==0,'prior native intent not confirmed: reconcile; never blindly repush')
            event=intent['published_event'];native_safety(observed,event)
            receipt={**intent,'push_confirmed':True,'observed_remote_main':observed,'recovered_by_exact_commit_readback':True}
            save(W/'NATIVE_PUBLICATION_RECEIPT.json',receipt,exclusive=True);return
        destination=merged_gate(accepted,freeze);parent=destination['observed_remote_main']
        safety=native_safety(parent);claimed_row(blob(parent,QUEUE))
        event=native_event(accepted,publication,merge,tracker)
        replacements=native_replacements(blob(parent,QUEUE),blob(parent,STATE),blob(parent,HISTORY),event)
        # Persist the exact planned input before Git object creation.
        save(intent_path,{'utc':utc_now(),'parent':parent,'published_event':event,'replacement_pins':{name:fingerprint(raw) for name,raw in replacements.items()},'accepted_freeze_sha256':accepted['freeze_sha256'],'attempt':attempt,'blind_retry_permitted':False},exclusive=True)
        # No Git index, checkout, branch, local HEAD or configuration is used.
        tree=explicit_tree(parent,{p:r.decode() for p,r in replacements.items()})
        changed=run(['git','diff','--name-only',parent,tree]).splitlines()
        need(set(changed)=={QUEUE,STATE,HISTORY},'exactly three native publication paths')
        commit=run(['git','commit-tree',tree,'-p',parent],input='Record verified PR952 preprint with original declared turns and UNKNOWN historical native count\n').strip()
        intent={'utc':utc_now(),'parent':parent,'commit':commit,'paths':changed,'published_event':event,'source_gate':destination['source_gate'],'native_safety':safety,'accepted_freeze_sha256':accepted['freeze_sha256'],'attempt':attempt,'blind_retry_permitted':False}
        save(W/f'NATIVE_PUBLICATION_CAS_{attempt:02d}_PREPARED.json',intent,exclusive=True)
        accepted_review_check(accepted,freeze,context)
        push=subprocess.run(['git','push','--force-with-lease=refs/heads/main:'+parent,'origin',commit+':refs/heads/main'],cwd=ROOT,capture_output=True,text=True)
        save(W/f'NATIVE_PUBLICATION_CAS_{attempt:02d}_ACTION.json',{'utc':utc_now(),'returncode':push.returncode,'stdout':push.stdout,'stderr':push.stderr})
        observed=remote_main()
        check=subprocess.run(['git','merge-base','--is-ancestor',commit,observed],cwd=ROOT,capture_output=True)
        if check.returncode==0:
            native_safety(observed,event)
            receipt={**intent,'push_confirmed':True,'observed_remote_main':observed,'other_queue_state_history_bytes_preserved':True,'checkout_index_HEAD_untouched':True}
            save(W/'NATIVE_PUBLICATION_RECEIPT.json',receipt,exclusive=True)
            print(json.dumps({'commit':commit,'doi':publication['doi'],'original_declared_turns':'1/5','historical_native_turn_count':'UNKNOWN','new_author_proof_responses':0}));return
        definitive=('stale info' in push.stderr or 'non-fast-forward' in push.stderr or 'fetch first' in push.stderr)
        need(push.returncode!=0 and definitive and observed!=parent,'native push uncertain/non-CAS failure: inspect exact commit; no blind repeat')
        save(W/f'NATIVE_PUBLICATION_CAS_{attempt:02d}_DEFINITIVE_RACE.json',{'utc':utc_now(),'not_pushed_commit':commit,'observed_remote_main':observed,'repeat_requires_fresh_source_native_gate':True})
    raise RuntimeError('Six definite main races; native ledger remains pending')


def native_verify(publication,merge,tracker,accepted,native):
    commit,parent=native['commit'],native['parent'];observed=remote_main()
    run(['git','merge-base','--is-ancestor',commit,observed]);run(['git','merge-base','--is-ancestor',merge['mergeCommit']['oid'],commit])
    need(run(['git','show','-s','--format=%P',commit]).strip()==parent,'native actual single parent')
    need(set(run(['git','diff','--name-only',parent,commit]).splitlines())=={QUEUE,STATE,HISTORY},'native exact actual path scope')
    event=native['published_event'];expected=native_replacements(blob(parent,QUEUE),blob(parent,STATE),blob(parent,HISTORY),event)
    need(all(blob(commit,name)==raw for name,raw in expected.items()),'native actual exact narrow byte replacements')
    native_safety(parent);native_safety(observed,event);source_gate(observed)
    need(event.get('historical_native_turn_count')=='UNKNOWN' and event.get('original_declared_turns')=='1/5' and type(event.get('new_author_proof_responses')) is int and event['new_author_proof_responses']==0 and type(event.get('turns_used')) is int and event['turns_used']==1 and event.get('turns_used_basis')=='Imported immutable PR declaration1/5; native per-turn count is not authenticated' and 'candidate_turn' not in event,'honest declared-counter import without fabricated author-turn events')
    original_check(merge['mergeCommit']['oid'])
    return {'utc':utc_now(),'actual_original33_preserved':True,'all_other_queue_state_history_bytes_preserved':True,'native_commit_on_current_remote_main':observed,'original_declared_turns':'1/5','historical_native_turn_count':'UNKNOWN','new_author_proof_responses':0,'confirmed':True}


def next_identity(old,before):
    number=before.get('number');need(type(number) is int and PR<number<=1000,'next range953..1000')
    record=complete_changed_paths(before);paths=record['paths']
    ids={m[1] for name in paths if (m:=re.fullmatch(r'unsolved_math_prioritization/attempts/([0-9]+)/.+',name))}
    need(len(ids)==1,'next target filename identity absent/ambiguous');key=ids.pop()
    need(all(name==QUEUE or name.startswith('unsolved_math_prioritization/attempts/'+key+'/') for name in paths),'next changed filename scope')
    return key

def gate_next(inventory):
    """Only live PR metadata and immutable QUEUE rows; no excluded mathematics."""
    need(type(inventory) is list,'inventory list')
    skipped=[];selected=None
    for old in sorted((x for x in inventory if PR<x['number']<=1000),key=lambda x:x['number']):
        number=old['number'];before=pr_view(number)
        if before.get('state')!='OPEN' or before.get('isDraft') is not True:
            skipped.append({'pr':number,'action':'SKIP_NOT_OPEN_DRAFT','math_source_read':False});continue
        head=before.get('headRefOid');need(type(head) is str and re.fullmatch('[0-9a-f]{40}',head),'next immutable head')
        key=next_identity(old,before)
        # GraphQL text is sufficient for QUEUE; avoids REST quota and object/cache mutation.
        query='query($expr:String!){repository(owner:"AlecKriebel",name:"Math"){object(expression:$expr){... on Blob{text isBinary byteSize oid}}}}'
        response=strict_json(run(['gh','api','graphql','-f','query='+query,'-f','expr='+head+':'+QUEUE]))
        obj=response.get('data',{}).get('repository',{}).get('object')
        need(type(obj) is dict and obj.get('isBinary') is False and type(obj.get('text')) is str,'immutable next QUEUE text')
        queue=obj['text'].encode();need(type(obj.get('byteSize')) is int and len(queue)==obj['byteSize'],'next QUEUE byte size')
        _,row,_,_=queue_parts(queue,key);cells=row.decode().split('|');status=cells[8].strip()
        after=pr_view(number)
        fields=('number','state','isDraft','headRefOid','headRefName','baseRefName','url','currentBaseRefOid')
        need(all(k in before and k in after and exact(before[k],after[k]) for k in fields),'next PR identity/live base changed across status-only gate')
        if status!='claimed_solved':
            skipped.append({'pr':number,'problem_id':key,'status':status,'action':'SKIP_STATUS_ONLY','math_source_read':False});continue
        need(before.get('baseRefName')=='main','next claimed target main destination')
        selected={'number':number,'problem_id':key,'headRefOid':head,'baseRefName':'main','status':status,'queue_row_sha256':sha(row.rstrip(b'\r\n')),'gate_utc':utc_now(),'math_source_read':False,'snapshot_not_yet_created':True};break
    return skipped,selected


def finalize_pr_metadata(accepted,freeze,publication,merge,tracker,context):
    template=read_regular(D/'PR_DESCRIPTION.md',pin=freeze['files']['PR_DESCRIPTION.md']).decode()
    body=template.rstrip()+"\n\n## Published preprint\n\n"+f"Alec Kriebel, **{TITLE}**, version1.0. [DOI](https://doi.org/{publication['doi']}); [Zenodo record]({publication['record_url']}).\n\n"+f"The exact published PDF and verification archive were independently downloaded and checked. Tracker {tracker['updated_range']} was read back in the Math Puzzles tab. Original PR head `{HEAD}`; actual main merge `{merge['mergeCommit']['oid']}`.\n\n"+f"Release freeze SHA256: `{accepted['freeze_sha256']}`. PACKAGE_MANIFEST.json SHA256: `{freeze['package_manifest_sha256']}`. Entry verifier SHA256: `{freeze['files']['package/'+freeze['package_verifier']]['sha256']}`. {len(accepted['full_package_reviews'])} NEW whole-package review rounds are separately sealed; the final two clean reviews authenticate this exact current package.\n"
    title='10400145: published Habiro rank interpolation obstruction'
    current=pr_view();main_destination(current,merged=True)
    if current.get('body')!=body or current.get('title')!=title:
        need(sha(current['body'].encode())==freeze['pr_description_sha256'],'live body changed from reviewed original; reconcile before metadata edit')
        need(not (W/'PR_FINAL_METADATA_INTENT.json').exists(),'prior metadata intent: read back exact outcome, no repeat')
        path=W/'PR_PUBLISHED_BODY.md'
        fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
        with os.fdopen(fd,'w') as stream:stream.write(body)
        save(W/'PR_FINAL_METADATA_INTENT.json',{'utc':utc_now(),'title':title,'body_sha256':sha(body.encode()),'merged_commit':merge['mergeCommit']['oid'],'blind_retry_permitted':False},exclusive=True)
        accepted_review_check(accepted,freeze,context)
        merged_gate(accepted,freeze)
        boundary=pr_view();main_destination(boundary,merged=True)
        need(boundary.get('title')==current.get('title') and boundary.get('body')==current.get('body') and exact(boundary['mergeCommit'],merge['mergeCommit']),'metadata changed before edit boundary')
        result=subprocess.run(['gh','pr','edit',str(PR),'--repo','AlecKriebel/Math','--title',title,'--body-file',str(path)],cwd=ROOT,capture_output=True,text=True)
        save(W/'PR_FINAL_METADATA_ACTION.json',{'utc':utc_now(),'returncode':result.returncode,'stdout':result.stdout,'stderr':result.stderr})
    actual=pr_view();main_destination(actual,merged=True)
    need(actual.get('title')==title and actual.get('body')==body and actual['mergeCommit']==merge['mergeCommit'],'actual final PR metadata readback')
    accepted_review_check(accepted,freeze,context)
    save(W/'PR_PUBLISHED_METADATA.json',actual)


def finalize(args,context):
    accepted,freeze=accepted_package(context);merged_gate(accepted,freeze)
    tracker=load(W/'TRACKER_RECEIPT.json');native=load(W/'NATIVE_PUBLICATION_RECEIPT.json')
    publication,merge=publication_links(accepted,freeze,tracker,native)
    public=independent_public_verify(publication,descriptor_check(freeze)[1]);save(W/'ZENODO_PUBLIC_VERIFICATION_FINAL.json',public)
    readback=gws(['sheets','spreadsheets','values','get','--params',json.dumps({'spreadsheetId':SID,'range':tracker['updated_range']})])
    need(readback.get('range')==tracker['updated_range'] and readback.get('values')==[tracker['row']],'fresh actual tracker exact row')
    native_result=native_verify(publication,merge,tracker,accepted,native)
    record={'utc':utc_now(),'pr':PR,'problem_id':KEY,'outcome':'accepted_merged_preprint_published','original_pr_head':HEAD,'merge_commit':merge['mergeCommit']['oid'],'merged_base':'main','doi':publication['doi'],'record_url':publication['record_url'],'tracker_range':tracker['updated_range'],'native_ledger_commit':native['commit'],'native_ledger_readback_confirmed':True,'original_declared_turns':'1/5','historical_native_turn_count':'UNKNOWN','new_author_proof_responses':0,'priority_limit':'Bounded primary audit with retained access gaps; no novelty/firstness/current-open certificate','AI_and_peer_review':'Extensive AI assistance; unrefereed; no independent human review or formal proof certification','full_package_review_count':len(accepted['full_package_reviews']),'clean_final_review_manifest_sha256':accepted['full_package_reviews'][-1]['manifest_sha256'],'accepted_freeze_sha256':accepted['freeze_sha256'],'all_prior_required_and_optional_findings_resolved':True}
    save(W/'PUBLICATION_FINAL_VERIFICATION.json',native_result);save(W/'PUBLICATION_RECORD.json',record)
    finalize_pr_metadata(accepted,freeze,publication,merge,tracker,context)
    state=load(P/'CURRENT_STATE.json');inventory=load(P/'inventory.json')
    already=PR in state['completed_prs']
    need(state.get('active_pr') in (PR,None) or already,'another active research target')
    if already:
        matches=[x for x in state['completed_results'] if x.get('pr')==PR]
        need(len(matches)==1 and matches[0].get('doi')==publication['doi'] and matches[0].get('native_ledger_commit')==native['commit'],'existing final record conflicts')
        accepted_review_check(accepted,freeze,context)
        print(json.dumps({'already_finalized':True,'next_pr':state.get('active_pr')}));return
    skipped,selected=gate_next(inventory)
    completed=sorted([*state['completed_results'],record],key=lambda x:x['pr'])
    state.update(utc=utc_now(),completed_results=completed,completed_prs=[x['pr'] for x in completed],published_prs=[x['pr'] for x in completed if x['outcome']=='accepted_merged_preprint_published'],active_pr=selected['number'] if selected else None,active_problem_id=selected['problem_id'] if selected else None,next_pr=selected['number'] if selected else None,active_pr_completion_estimate_percent=0,phase='post_PR952_status_only_gate',shard_completion_estimate_percent=100*len(completed)/len(state['eligible_prs']))
    # Drop PR952-specific phase metadata before a new target is allowed to start.
    for name in ['active_original_head','original_candidate_turns','review_families','priority_families','publication_disposition','priority_status','full_package_reviews','active_candidate_revision','active_freeze_sha256','active_package_manifest_sha256','new_priority_research_positive_turns','known_effort_positive_turns','new_mechanism_status','portable_release_tooling']:
        state.pop(name,None)
    if selected:state['active_original_head']=selected['headRefOid']
    for item in inventory:
        if item['number']==PR:item.update(disposition=record['outcome'],doi=publication['doi'],tracker_range=tracker['updated_range'])
    accepted_review_check(accepted,freeze,context)
    save(W/'POST_PR952_STATUS_GATES.json',{'utc':utc_now(),'skipped':skipped,'next_eligible':selected,'math_source_read':False,'ascending_range':[953,1000]})
    save(P/'CURRENT_STATE.json',state);save(P/'inventory.json',inventory)
    for path in [P/'RESEARCH_LOG.md',A/'RESEARCH_LOG.md']:
        with path.open('a') as stream:stream.write(f"\n{utc_now()} — PR952 workflow100%; shard {state['shard_completion_estimate_percent']:.2f}%. Actual main merge {merge['mergeCommit']['oid']}; DOI {publication['doi']}; tracker {tracker['updated_range']}; native {native['commit']}. Exact readbacks verified; original declared1/5 retained separately, historical native count UNKNOWN, zero new author proof responses.\n")
    print(json.dumps({'PR952':record,'next_pr':state.get('active_pr'),'status_only_skips':skipped}))


def readonly_preflight(args,context):
    """Actual source/original/native/path validation; no acceptance or mutation."""
    global READ_ONLY,OBSERVATION_OUTPUT
    target=Path(args.observation_dir)
    need(target.is_absolute(),'observation directory must be absolute')
    name=target.relative_to(ROOT).as_posix();need(safe(name),'observation directory inside repository')
    for protected in (W,D,A/'original'):
        need(target!=protected and not target.is_relative_to(protected) and not protected.is_relative_to(target),'observation output cannot redirect authoritative paths')
    flags=os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW|os.O_NONBLOCK
    fd=os.open(ROOT,flags)
    try:
        for part in name.split('/'):
            child=os.open(part,flags,dir_fd=fd);os.close(fd);fd=child
    finally:os.close(fd)
    READ_ONLY=True;OBSERVATION_OUTPUT=target
    freeze=freeze_check(read_regular(D/'FREEZE.json'),args.freeze,context)
    gate=premerge_gate(freeze,require_draft=True)
    candidate_state_check(freeze,args.freeze,context)
    receipt={'utc':utc_now(),'status':'PASS_READONLY_PREFLIGHT','original_pr_head':HEAD,'freeze_sha256':args.freeze,'operations_inventory_sha256':context['inventory_sha256'],'package_manifest_sha256':freeze['package_manifest_sha256'],'gate':gate,'Git_network_fetch_performed':False,'service_mutations':0,'acceptance_authority':False,'review_credit':False}
    numbered_receipt('READONLY_PREFLIGHT',receipt)
    print(json.dumps(receipt,sort_keys=True))


def operation(action,args,context):
    need(sys.flags.optimize==0,'nonoptimized operation worker')
    need(not READ_ONLY or action=='preflight','read-only observer cannot perform operation')
    need(run(['git','symbolic-ref','--short','HEAD']).strip()=='main','shared checkout stays main')
    {'preflight':readonly_preflight,'accept':accept,'merge':merge,'zenodo':zenodo,'tracker':tracker_append,'native':native_write,'finalize':finalize}[action](args,context)


def entry(action):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--operations-sha256', required=True)
    if action == 'accept':
        parser.add_argument('--freeze', required=True)
        parser.add_argument('--review', action='append')
        parser.add_argument('--preflight-only', action='store_true')
        parser.add_argument('--observation-dir')
    if action == 'zenodo':
        parser.add_argument('action', choices=['stage', 'publish', 'inspect'])
    args = parser.parse_args()
    if action=='accept':
        if args.preflight_only:
            need(type(args.observation_dir) is str,'preflight requires own observation directory');action='preflight'
        else:need(bool(args.review) and args.observation_dir is None,'acceptance requires complete externally sealed review list')
    context = capture_inventory(args.operations_sha256)
    # Every repository dependency is authenticated BEFORE a copied-byte worker
    # starts. -I -S -B gives an actual optimization0 worker even if this trusted
    # entry point was invoked with -O/-OO/PYTHONOPTIMIZE.
    bundle = {'action': action, 'args': vars(args),
              'inventory_sha256': context['inventory_sha256'], 'inventory': context['inventory'],
              'captured': {name: base64.b64encode(raw).decode('ascii') for name, raw in context['captured'].items()}}
    bootstrap = ('import argparse,base64,json,sys; '
                 'b=json.loads(sys.stdin.buffer.read()); '
                 'c={"inventory_sha256":b["inventory_sha256"],"inventory":b["inventory"],'
                 '"captured":{n:base64.b64decode(v,validate=True) for n,v in b["captured"].items()}}; '
                 'p=sys.argv[1]; n={"__name__":"_pr952_authenticated_core_","__file__":p,"__package__":None}; '
                 'exec(compile(c["captured"][sys.argv[2]],p,"exec",dont_inherit=True,optimize=0),n); '
                 'n["operation"](b["action"],argparse.Namespace(**b["args"]),c)')
    core = str((P / 'accept_pr952.py').relative_to(ROOT))
    result = subprocess.run([sys.executable, '-I', '-S', '-B', '-c', bootstrap,
                             str(P / 'accept_pr952.py'), core], cwd=ROOT,
                            input=json.dumps(bundle).encode())
    raise SystemExit(result.returncode)


if __name__=="__main__":
    entry("accept")
