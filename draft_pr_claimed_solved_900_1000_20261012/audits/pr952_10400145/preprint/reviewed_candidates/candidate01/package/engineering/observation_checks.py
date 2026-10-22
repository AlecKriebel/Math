#!/usr/bin/env python3
"""Pure offline predicates for future PR952 adapters. No I/O/service mutations.

These checks are implementation support, not a complete promotion authority.
The adapter must externally authenticate source/freeze/reviews before each use.
"""
import re
HEAD='989a532ae1d50894190d010a0a02ba8c3d71ee05'
HEX40=re.compile(r'[0-9a-f]{40}\Z')
class Reject(ValueError):pass

def need(ok,label):
    if not ok:raise Reject(label)

def exact(a,b):
    if type(a) is not type(b):return False
    if type(a) is dict:return set(a)==set(b) and all(exact(a[k],b[k]) for k in a)
    if type(a) is list:return len(a)==len(b) and all(exact(x,y) for x,y in zip(a,b))
    return a==b

def differences(before,after):
    need(type(before) is dict and type(after) is dict,'observations must be mappings')
    return {k:{'before':before.get(k),'after':after.get(k),'present_before':k in before,'present_after':k in after} for k in sorted(set(before)|set(after)) if k not in before or k not in after or not exact(before[k],after[k])}

def live_base(node):
    need(type(node) is dict and type(node.get('baseRef')) is dict,'live baseRef required')
    b=node['baseRef'];need(b.get('name')==node.get('baseRefName') and type(b.get('target')) is dict,'live baseRef name/target')
    oid=b['target'].get('oid');need(type(oid) is str and HEX40.fullmatch(oid),'live baseRef.target oid required')
    return oid

def authority(node,merged=False):
    need(type(node) is dict and type(node.get('number')) is int and node['number']==952,'PR952 identity')
    need(node.get('headRefOid')==HEAD and node.get('baseRefName')=='main','immutable head/main')
    fields=['number','state','headRefOid','baseRefName','url']
    if merged:
        need(node.get('state')=='MERGED' and type(node.get('mergeCommit')) is dict,'merged state/commit')
        oid=node['mergeCommit'].get('oid');need(type(oid) is str and HEX40.fullmatch(oid),'merge oid')
        fields+=['mergeCommit','mergedAt']
    else:
        need(node.get('state')=='OPEN' and type(node.get('isDraft')) is bool,'open/draft field')
        fields+=['isDraft','headRefName','title','body']
    need(all(k in node for k in fields),'complete authority fields')
    for k in fields:
        if k not in ('number','isDraft','mergeCommit'):need(type(node[k]) is str,'authority scalar '+k)
    return {k:node[k] for k in fields}

def bracket(before,after,merged=False):
    """Retain computed observations; do not treat them as merged PR identity.

    Return a record even on authority drift. Caller persists it BEFORE raising.
    Premerge source/path eligibility must separately bind the same live base.
    """
    left=authority(before,merged);right=authority(after,merged)
    return {'authority_equal':exact(left,right),'authority_differences':differences(left,right),'all_observation_differences':differences(before,after),'before':before,'after':after}

def require_fresh_mergeable(node):
    authority(node);need(node.get('mergeable')=='MERGEABLE','fresh MERGEABLE required immediately before actual merge')

def complete_paths(pages,before,after):
    """All changed-path metadata pages at actual stable live baseRef.target.

    No mathematical file bodies are accepted or read. baseRefOid is retained as
    observation only, and never substituted for the current branch pointer.
    """
    need(type(pages) is list and 0<len(pages)<=30,'bounded complete pages')
    fields=('number','state','isDraft','headRefOid','headRefName','baseRefName','url')
    need(all(k in before and k in after and exact(before[k],after[k]) for k in fields),'PR metadata bracket drift')
    base=live_base(before);need(live_base(after)==base,'live base advanced: restart complete path gate')
    count=None;paths=[];cursors=set()
    for index,page in enumerate(pages):
        need(type(page) is dict and all(k in page and exact(page[k],before[k]) for k in fields),'page PR authority drift')
        need(live_base(page)==base,'page live base drift')
        n=page.get('changedFiles');need(type(n) is int and 1<=n<=3000 and (count is None or count==n),'stable changedFiles count');count=n
        files=page.get('files');need(type(files) is dict and set(files)=={'nodes','pageInfo'},'files connection schema')
        nodes=files['nodes'];need(type(nodes) is list and 1<=len(nodes)<=100,'nodes bound')
        for entry in nodes:
            need(type(entry) is dict and set(entry)=={'path'},'only path metadata allowed')
            name=entry['path'];need(type(name) is str and re.fullmatch(r'[A-Za-z0-9_./-]+',name) and not name.startswith('/') and all(x not in ('','.','..') for x in name.split('/')),'canonical changed path')
            paths.append(name)
        need(len(paths)<=count and len(paths)==len(set(paths)) and len(paths)==len({x.casefold() for x in paths}),'duplicate/alias/excess changed paths')
        info=files['pageInfo'];need(type(info) is dict and set(info)=={'hasNextPage','endCursor'} and type(info['hasNextPage']) is bool,'pagination schema')
        if index<len(pages)-1:
            cursor=info['endCursor'];need(info['hasNextPage'] is True and type(cursor) is str and cursor and cursor not in cursors,'complete distinct pagination cursor');cursors.add(cursor)
        else:need(info['hasNextPage'] is False and len(paths)==count,'missing final page or incomplete count')
    return {'live_base_oid':base,'paths':paths,'declared_count':count,'before':before,'after':after,'pages':pages}

def next_target_identity(path_record):
    paths=path_record['paths'];ids={m[1] for p in paths if (m:=re.fullmatch(r'unsolved_math_prioritization/attempts/([0-9]+)/.+',p))}
    need(len(ids)==1,'ambiguous/absent target path identity')
    key=next(iter(ids));prefix='unsolved_math_prioritization/attempts/'+key+'/'
    need(all(p.startswith(prefix) or p=='unsolved_math_prioritization/QUEUE.md' for p in paths),'unexpected changed-path scope')
    return key

def native_absence(state,history):
    need(type(state) is dict and type(history) is list and all(type(x) is dict for x in history),'native schemas')
    need('10400145' not in state and all(str(x.get('id'))!='10400145' for x in history),'current target native baseline changed')
    return {'current_target_state':'ABSENT','current_target_history_entries':0,'historical_native_turn_count':'UNKNOWN','historical_native_count_authenticated':False,'imported_declaration':'1/5','new_author_proof_responses':0,'candidate_turn_synthesized':False}
