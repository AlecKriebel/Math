#!/usr/bin/env python3
"""Read-only actual-GWS + complete owned-deposition pagination, including empty terminal."""
if not globals().get('_PR1131_SOURCE_VERIFIED',False):
    raise RuntimeError('Use the externally SHA-verified source bootstrap; direct helper imports are forbidden')
import argparse
import http.client
from urllib.parse import unquote, urlsplit, urlencode
import uuid
from ops_common import *

def resolver_policy(text):
    """Recognize resolver authorities, not path substrings of unrelated hosts.
    Homepages carry no DOI identity. Nonhome short aliases and dotted/malformed
    resolver authorities require review; a long DOI is only a lexical lead.
    """
    hosts=re.compile(r'(?:(?:www|dx)\.)*(?:doi|shortdoi)\.org\.*',re.I)
    for token in re.findall(r'[^\s<>\[\]{}()\"\x27]+',text):
        token=token.rstrip('.,;:!?')
        candidates=[token]
        # Handles typed prefixes such as DOI:https:// without confusing a
        # doi.org substring inside an unrelated HTTP authority/path.
        candidates += [token[m.start():] for m in re.finditer(r'[A-Za-z][A-Za-z0-9+.-]*://',token)]
        for candidate in candidates:
            malformed=False
            if candidate.startswith('//'):parsed=urlsplit(candidate)
            elif re.match(r'[A-Za-z][A-Za-z0-9+.-]*://',candidate):parsed=urlsplit(candidate)
            elif re.match(r'[A-Za-z][A-Za-z0-9+.-]*:',candidate):
                rest=candidate.split(':',1)[1];parsed=urlsplit('//'+rest.lstrip('/'));malformed=True
            else:parsed=urlsplit('//'+candidate)
            host=parsed.hostname
            if isinstance(parsed.username,str) and hosts.fullmatch(parsed.username) is not None and (not isinstance(host,str) or hosts.fullmatch(host) is None):
                raise RuntimeError('Official-looking DOI resolver userinfo requires root review')
            if not isinstance(host,str) or hosts.fullmatch(host) is None:continue
            home=parsed.path in {'','/'} and not parsed.query and not parsed.fragment
            if home:continue
            need(not malformed and parsed.scheme in {'','http','https'} and parsed.username is None and parsed.password is None,'Malformed/non-HTTP DOI resolver reference requires root review')
            need(not host.endswith('.') and parsed.port in {None,80,443},'Terminal-dot/ported DOI resolver reference requires root review')
            need(host in {'doi.org','www.doi.org','dx.doi.org','www.dx.doi.org'},'Short DOI resolver alias requires root review')
            need(re.fullmatch(r'/10\.[0-9]{4,9}/[^\s]+',parsed.path) is not None,'DOI resolver short alias requires root review')

def identities(text):
    """Conservative leads only. Unfamiliar official routes/short aliases fail closed."""
    need(isinstance(text,str) and len(text)<=1_000_000,'Invalid identity cell')
    current=text
    for _ in range(8):
        nxt=unquote(current)
        if nxt==current:break
        current=nxt
    else:need(unquote(current)==current,'Deep encoded DOI alias requires root review')
    resolver_policy(current)
    # A typed OWR report10/year citation with pages and matching source DOI
    # is bibliography, not a bare short DOI. Mask only that exact report span.
    masked=list(current)
    citation=re.compile(r'(?<![A-Za-z0-9_])OWR[ \t]+(?P<report>10)/(?P<year>(?:19|20)[0-9]{2})[ \t]+pp\.?[ \t]*(?P<first>[1-9][0-9]*)[-–](?P<last>[1-9][0-9]*)',re.I)
    for match in citation.finditer(current):
        if int(match.group('first'))<=int(match.group('last')) and re.search(r'10\.4171/owr/'+match.group('year')+r'/10(?:$|[\s.,;:/?#])',current,re.I):
            a,b=match.start('report'),match.end('year');masked[a:b]=' '*(b-a)
    need(not re.search(r'(?<![A-Za-z0-9.])10/[A-Za-z0-9]+(?:$|[\s?#.,;)])',''.join(masked)),'Bare short DOI requires root review')
    need(not re.search(r'zenodo\.(?:%|[+-])',current,re.I),'Malformed Zenodo DOI requires root review')
    found={int(m.group(1)) for m in re.finditer(r'zenodo\.([0-9]+)',current,re.I)}
    need(0 not in found,'Nonpositive Zenodo identity requires root review')
    for token in re.findall(r'\S*zenodo\.org\S*',current,re.I):
        token=token.strip('()[]{}<>,;\'".');parsed=urlsplit(token if '://' in token else 'https://'+token)
        # Exact official host only; lookalikes are not certified record aliases.
        need(parsed.hostname in {'zenodo.org','www.zenodo.org'},'Ambiguous official-looking Zenodo authority/route requires root review')
        need(parsed.scheme in {'http','https'} and not parsed.username and parsed.port in {None,443,80},'Ambiguous official Zenodo authority')
        match=re.fullmatch(r'/(?:records?|api/records)/([1-9][0-9]*)(?:/(?:files|export|draft|versions|citations|references|communities|preview|files-archive)(?:/.*)?)?/?',parsed.path)
        need(match is not None,'Unknown official Zenodo record route requires root review')
        found.add(int(match.group(1)))
    return found

def row_ids(row):
    allids=[identities(cell) for cell in row]
    return set().union(*allids)

def projection(record):
    need(isinstance(record,dict) and type(record.get('id')) is int and record['id']>0 and isinstance(record.get('metadata'),dict) and isinstance(record.get('files'),list),'Malformed owned deposition')
    return {k:record.get(k) for k in ['id','submitted','state','doi','conceptdoi','conceptrecid','metadata','files']}

def family_ids(record):
    result={record['id']}
    def add(v):
        need(type(v) is int and v>0 or isinstance(v,str) and re.fullmatch('[1-9][0-9]*',v),'Malformed concept ID');result.add(int(v))
    if record.get('conceptrecid') is not None:add(record['conceptrecid'])
    if record.get('conceptdoi') is not None:
        s=record['conceptdoi'];need(isinstance(s,str) and re.fullmatch(r'10\.5281/zenodo\.[1-9][0-9]*',s),'Malformed concept DOI');add(s.rsplit('.',1)[1])
    for v in record.get('metadata',{}).get('relations',{}).get('version',[]):
        need(isinstance(v,dict) and isinstance(v.get('parent'),dict) and v['parent'].get('pid_type')=='recid','Unparsed version relation')
        add(v['parent'].get('pid_value'))
    need(len(result)<=2,'Contradictory record family');return sorted(result)

def read_owned_pages(raw,label):
    token=zenodo.token_for('production');allrecords={};pages=[]
    for page in range(1,10001):
        target='/api/deposit/depositions?'+urlencode({'page':page,'size':25,'sort':'mostrecent'})
        conn=http.client.HTTPSConnection('zenodo.org',timeout=60)
        try:
            conn.request('GET',target,headers={'Authorization':'Bearer '+token,'Accept':'application/json','User-Agent':zenodo.USER_AGENT})
            response=conn.getresponse();body=response.read(16*1024*1024+1)
            need(response.status==200 and len(body)<=16*1024*1024,'Owned account GET failed; no body/token printed')
            values=strict_json(body);need(isinstance(values,list) and len(values)<=25,'Owned pagination must return a list <=25')
            durable(raw/(label+'_page_'+str(page)+'.json'),values)
        finally:conn.close()
        pages.append({'page':page,'count':len(values),'http_body_sha256':sha(body),'http_bytes':len(body),'captured_json_sha256':digest(values),'capture_file_sha256':sha((raw/(label+'_page_'+str(page)+'.json')).read_bytes())})
        for record in values:
            projection(record);identifier=record['id'];need(identifier not in allrecords,'Pagination duplicate ID; recollect read-only');allrecords[identifier]=record
        if not values:
            need(allrecords and 23408971 in allrecords,'Owned-account known-record positive control missing')
            return allrecords,pages
    raise RuntimeError('Account pagination lacks empty terminal page')

def collect(phase,head,identifier=None,cleared=None,allow_target=False):
    need(phase in {'before_integration','before_ready','before_merge','before_stage','before_publish','before_ledger'},'Unknown live phase')
    need(identifier is None or type(identifier) is int and identifier>0,'Invalid target deposition ID')
    pkg=package();proposal();start=stamp();operation=uuid.uuid4().hex;raw=PRIVATE/('live_'+operation);raw.mkdir(mode=0o700)
    sheet,rows=gws_read();durable(raw/'ledger.json',sheet)
    for row in rows:row_ids(row)
    first,pages_a=read_owned_pages(raw,'account_a');records,pages_b=read_owned_pages(raw,'account_b')
    need({k:digest(projection(v)) for k,v in first.items()}=={k:digest(projection(v)) for k,v in records.items()},'Owned account changed across full enumerations; recollect read-only')
    md5s={hashlib.md5(pkg['flat'][name]).hexdigest() for name in ['finite-warm-thresholds.pdf','finite-warm-thresholds-source-and-verification.zip']}
    matches={k:v for k,v in records.items() if PATTERN.search(json.dumps(projection(v),ensure_ascii=False)) or any(str(f.get('checksum','')).removeprefix('md5:').lower() in md5s for f in v['files'])}
    families=[]
    if identifier is not None:
        need(identifier in records,'Expected owned deposition missing');families=family_ids(records[identifier])
        for k in families:
            if k in records:matches[k]=records[k]
    leads=[{'id':k,'identity_sha256':digest(projection(v))} for k,v in sorted(matches.items()) if k!=identifier]
    ledgerleads=[{'row':i,'values_sha256':digest(row),'values':row} for i,row in enumerate(rows,1) if PATTERN.search(' '.join(row)) or set(families)&row_ids(row)]
    states=[]
    for path in sorted((REPO/'.zenodo-state').glob('*.json')):
        data=path.read_bytes();value=strict_json(data)
        if PATTERN.search(json.dumps(value,ensure_ascii=False)) or identifier is not None and value.get('id')==identifier:
            states.append({'path':path.relative_to(REPO).as_posix(),'sha256':sha(data),'id':value.get('id')})
    pr=gh('pulls/1131');validate_pr(pr,head,phase in {'before_stage','before_publish','before_ledger'})
    main=gh('git/ref/heads/main')['object']['sha'];durable(raw/'pr.json',pr)
    row=draft_row(identifier) if identifier is not None and allow_target else None
    targets=[v for v in ledgerleads if set(families)&row_ids(v['values'])]
    if cleared is not None:
        allowed={e['id']:e['identity_sha256'] for e in cleared['distinct_account_leads']}
        need(len(allowed)==len(cleared['distinct_account_leads']) and identifier not in allowed and not set(families)&set(allowed),'Contradictory account exemptions')
        need(all(allowed.get(e['id'])==e['identity_sha256'] for e in leads),'New/changed owned-account lead requires root review')
        need(all(k in records and digest(projection(records[k]))==v for k,v in allowed.items()),'Root distinct account projection changed/missing')
        exempt=set(cleared['distinct_ledger_row_sha256'])
        need(len(exempt)==len(cleared['distinct_ledger_row_sha256']),'Duplicate ledger exemption')
        need(all(digest(v['values']) not in exempt for v in targets),'Target identity contradicts distinct-row exemption')
        need(all(v['values']==row if v in targets and row is not None else v['values_sha256'] in exempt for v in ledgerleads),'New/changed ledger lead requires root review')
        need(len(targets)<=1 and (not targets or row is not None and targets[0]['values']==row),'Existing target row differs/duplicates')
        current=[v for v in states if v['id']==identifier] if identifier is not None else []
        unrelated=[v for v in states if v not in current]
        need(unrelated==cleared['distinct_local_state_files'],'New/changed local deposit state requires root reconciliation')
        if identifier is None:need(not current,'Unexpected target draft state')
    receipt={'at_start':start,'at_end':stamp(),'phase':phase,'head':head,'main':main,'target_id':identifier,'family_ids':families,'account_total':len(records),'account_pages_a':pages_a,'account_pages_b':pages_b,'empty_terminal_both':True,'account_leads':leads,'ledger_leads':ledgerleads,'ledger_sha256':digest(rows),'local_states':states,'private_capture':str(raw),'read_only':True}
    fresh(start);durable(raw/'gate.json',receipt)
    return receipt,records,rows

def draft_row(identifier):
    need(type(identifier) is int and identifier>0,'Exact record ID required')
    template=strict_json((OPS/'LEDGER_ROW_TEMPLATE.json').read_bytes())
    need(isinstance(template,list) and len(template)==4 and all(isinstance(v,str) for v in template),'Four ledger cells required')
    return [v.replace('{RECORD_ID}',str(identifier)) for v in template]

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--phase',required=True);p.add_argument('--expected-pr-head',required=True);p.add_argument('--deposit-id',type=int)
    a=p.parse_args();g,_,_=collect(a.phase,a.expected_pr_head,a.deposit_id)
    print(json.dumps({k:g[k] for k in ['phase','account_total','empty_terminal_both','account_leads','ledger_sha256','private_capture','read_only']},indent=2))
if __name__=='__main__':main()
