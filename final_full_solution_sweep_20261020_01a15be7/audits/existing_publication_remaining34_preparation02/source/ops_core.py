"""Read-only metadata/identity primitives. Import is inert; no network or writes."""
from pathlib import Path
import datetime as dt
import hashlib,html,json,re,time,unicodedata,urllib.parse,urllib.request,urllib.error
from functools import lru_cache
UA='Math-publication-accounting/1.0 (read-only metadata audit; https://github.com/AlecKriebel/Math)'
RETRY_STATUSES={429,502,503,504}
class GateError(RuntimeError):pass
def require(ok,message):
    if not ok:raise GateError(message)
def typed_equal(left, right):
    """Exact JSON types and recursive values; bool never equals a number."""
    if type(left) is not type(right):
        return False
    if type(left) is dict:
        if not all(type(k) is str for k in left) or not all(type(k) is str for k in right):
            return False
        return left.keys() == right.keys() and all(typed_equal(left[k], right[k]) for k in left)
    if type(left) is list:
        return len(left) == len(right) and all(typed_equal(a, b) for a, b in zip(left, right))
    if type(left) is float:
        import math
        return math.isfinite(left) and math.isfinite(right) and left.hex() == right.hex()
    return type(left) in (str, int, bool, type(None)) and left == right


PR1198_MONOTONE_VIEW_COUNTERS = frozenset({
    ('stats', 'unique_views'), ('stats', 'version_unique_views'),
    ('stats', 'version_views'), ('stats', 'views')
})


def compare_1198_record(expected, current):
    """Proposed policy: full typed equality except four exact monotone counters.

    Neither raw object is altered. Return every allowed changed leaf for capture.
    Missing/extra fields, including unknown stats fields, are never projected out.
    """
    require(type(expected) is dict and type(current) is dict, '1198 record object required')
    require(type(expected.get('stats')) is dict and type(current.get('stats')) is dict,
            '1198 stats object required')
    for path in PR1198_MONOTONE_VIEW_COUNTERS:
        require(path[1] in expected['stats'] and path[1] in current['stats'],
                '1198 required view counter missing')
    changes = []
    def walk(old, new, path):
        if path in PR1198_MONOTONE_VIEW_COUNTERS:
            require(type(old) is int and type(new) is int and 0 <= old <= new,
                    '1198 view counters must be exact nonnegative monotone integers')
            if new != old:
                changes.append({'path': '/' + '/'.join(path), 'old': old, 'new': new})
            return
        require(type(old) is type(new), '1198 full-record type changed at ' + repr(path))
        if type(old) is dict:
            require(all(type(k) is str for k in old) and all(type(k) is str for k in new)
                    and old.keys() == new.keys(), '1198 full-record key set changed at ' + repr(path))
            for key in sorted(old):
                walk(old[key], new[key], path + (key,))
        elif type(old) is list:
            require(len(old) == len(new), '1198 full-record list length changed at ' + repr(path))
            for index, (a, b) in enumerate(zip(old, new)):
                walk(a, b, path + (str(index),))
        else:
            require(typed_equal(old, new), '1198 full-record value changed at ' + repr(path))
    walk(expected, current, ())
    return changes


def sha(data):return hashlib.sha256(data).hexdigest()
def canonical(value):return json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def decoded(value):
    s=str(value)
    for unused in range(8):
        normalized=unicodedata.normalize('NFKD',s)
        normalized=''.join(c for c in normalized if unicodedata.category(c)!='Cf')
        n=html.unescape(urllib.parse.unquote(normalized))
        if n==s:break
        s=n
    s=unicodedata.normalize('NFKD',s).casefold()
    return ''.join(c for c in s if unicodedata.category(c) not in {'Mn','Cf'})
def folded(value):return ''.join(c for c in decoded(value) if c.isalnum())
def words(value):return re.sub(r'[^\w]+',' ',decoded(value)).strip()
def row_sha(row):return sha(canonical(row+['']*(43-len(row))))
def parse_original_ids(row_a):
    out=[]
    patterns=[r'(?:^|/\s*|\band\s+)(\d{4,8})(?=\s*(?:/|—))',r'\b(?:OWR|AMR)-\d+-\d+\b',r'\bAIM-COMBINATORICS-\d+\b',r'\bOWR\d+/\d{4}(?:\s+pp?\.\s*\d+(?:[–-]\d+)?)?',r'\bAIM\s+Problem\s*\d+(?:\.\d+)?',r'\bOhtsuki\s+Conjecture\s*\d+(?:\.\d+)?',r'\b(?:EP|Erd[oőö]s)\s*\d{1,4}(?![0-9A-Za-z])',r'\bErd[oőö]s\s*1948\s*Problem\s*II\b',r'\bOEIS\s+A\d{6}\b',r'\bKP-\d+\.\d+\b']
    for pattern in patterns:
        for m in re.finditer(pattern,row_a,re.I):
            v=m.group(1) if m.lastindex else m.group()
            if v not in out:out.append(v)
    return out


# A known arXiv family is an exact identifier, never punctuation-stripped digits.
_ARXIV_MODERN=r'[0-9]{2}(?:0[1-9]|1[0-2])\.[0-9]{4,5}'
_ARXIV_LEGACY=r'[a-z][a-z0-9]*(?:[.-][a-z0-9]+)*/[0-9]{2}(?:0[1-9]|1[0-2])[0-9]{3}'
_ARXIV_BASE='(?:'+_ARXIV_MODERN+'|'+_ARXIV_LEGACY+')'
_ARXIV_SUFFIX=r'(?:v[1-9][0-9]*)?(?:\.pdf)?'
_ARXIV_TOKEN=re.compile(r'(?<![a-z0-9])(?P<base>'+_ARXIV_BASE+')'+_ARXIV_SUFFIX+r'(?![a-z0-9]|\.[a-z0-9])')

def canonical_arxiv_identifier(value):
    """Exact DOI/URL/bare alias to base ID; versions stay in the same family."""
    s=decoded(value).strip()
    s=re.sub(r'^(?:https?://(?:dx\.)?doi\.org/)?10\.48550/arxiv\.','',s)
    s=re.sub(r'^https?://(?:export\.)?arxiv\.org/(?:abs|pdf|html|src)/','',s)
    s=re.sub(r'^arxiv\s*[:.]?\s*','',s)
    match=re.fullmatch(r'(?P<base>'+_ARXIV_BASE+')'+_ARXIV_SUFFIX+r'/?',s)
    return match.group('base') if match else None

def arxiv_identifiers_in_text(value):
    text=decoded(value)
    # The adopted rows also use arXiv2509.22849 without a colon.
    text=re.sub(r'\barxiv\s*[:.]?\s*(?='+_ARXIV_BASE+')','arxiv:',text)
    return {m.group('base') for m in _ARXIV_TOKEN.finditer(text)}

def expected_same_paper_arxiv_ids(accepted_item):
    values=[accepted_item['doi'],*accepted_item.get('same_paper_alternate_dois',[]),accepted_item['selected_source']['url']]
    values += [a['value'] for a in accepted_item['identity_leads']
               if a['kind'] in {'same_paper_doi','same_paper_arxiv','reviewed_identity_lead'}]
    return sorted({x for v in values if (x:=canonical_arxiv_identifier(v))})

# Known associated PRs are source-identity leads, not mathematical duplicate proofs.
# decoded() already handles case, compatibility Unicode, format characters and
# bounded repeated HTML/percent decoding; this parser does not change it.
_PR_DECIMAL = r'[0-9]+'
_PR_NUMBER_END = r'(?!\w|\.[0-9])'
_PR_LABELLED = re.compile(
    r'(?<!\w)(?:pr|pull\s+request)\s*(?::\s*)?(?:#\s*)?'
    r'(?P<number>'+_PR_DECIMAL+r')'+_PR_NUMBER_END)
_PR_PROJECT_URL = re.compile(
    r'(?<!\w)https?://(?:www\.)?github\.com/aleckriebel/math/pull/'
    r'(?P<number>'+_PR_DECIMAL+r')'+_PR_NUMBER_END)
_PR_ALIAS_URL = re.compile(
    r'https?://(?:www\.)?github\.com/aleckriebel/math/pull/'
    r'(?P<number>'+_PR_DECIMAL+r')/?')

def associated_pr_alias_number(value):
    """Canonical project URL alias to its positive integer PR identity."""
    match=_PR_ALIAS_URL.fullmatch(decoded(value).strip())
    number=int(match.group('number')) if match else 0
    return number if number>0 else None

def associated_pr_numbers_in_text(value):
    """Only explicit PR/pull-request labels or this project's full PR URLs.

    Match the whole decimal token before comparing integer identities. This
    accepts leading-zero spelling but never truncates10070 to1007. Bare numbers
    and numbers embedded in longer words or decimal continuations are excluded.
    """
    text=decoded(value)
    return {number for pattern in (_PR_LABELLED,_PR_PROJECT_URL)
            for match in pattern.finditer(text)
            if (number:=int(match.group('number')))>0}


@lru_cache(maxsize=4096)
def _identity_context(text):
    """Memoize a pure parse of exact text, never an external observation."""
    d=decoded(text)
    f=''.join(c for c in d if c.isalnum())
    w=' '+re.sub(r'[^\w]+',' ',d).strip()+' '
    return d,f,w,arxiv_identifiers_in_text(d),associated_pr_numbers_in_text(d)


def identity_hits(rows,item):
    result=[]
    aliases=[(alias,canonical_arxiv_identifier(alias['value'])) for alias in item['identity_leads']]
    for number,row in enumerate(rows[1:],2):
        text=' '.join(map(str,row));d,f,w,arxiv_ids,pr_ids=_identity_context(text);matched=[]
        for alias,arxiv in aliases:
            value=alias['value'];kind=alias['kind']
            pr_number=associated_pr_alias_number(value)
            if kind=='pr_reference':require(pr_number is not None,'Malformed associated PR URL alias')
            if pr_number is not None:ok=pr_number in pr_ids
            elif arxiv is not None:ok=arxiv in arxiv_ids
            elif kind in {'catalog_id','record_id'}:ok=bool(re.search(r'(?<!\d)'+re.escape(value)+r'(?!\d)',d))
            elif kind=='author':ok=(' '+words(value)+' ') in w
            else:ok=folded(value) in f
            if ok:matched.append(alias)
        if matched:result.append({'row':number,'row_sha256_43_columns':row_sha(row),'matched':matched})
    return result

# Only explicit operational registry fields are omitted. Unknown bibliographic
# fields, references, all relations, dates and versions remain bound by default.
CROSSREF_OPERATIONAL={'indexed','deposited','score','is-referenced-by-count','reference-count','references-count'}
DATACITE_OPERATIONAL={'created','registered','published','updated','viewCount','downloadCount','citationCount','referenceCount','partCount','partOfCount','versionCount','versionOfCount'}
def registry_identity(payload,kind):
    if kind=='crossref':
        require(payload.get('status')=='ok' and isinstance(payload.get('message'),dict),'Crossref shape')
        return {k:v for k,v in payload['message'].items() if k not in CROSSREF_OPERATIONAL}
    require(kind=='datacite' and isinstance(payload.get('data',{}).get('attributes'),dict),'DataCite shape')
    return {k:v for k,v in payload['data']['attributes'].items() if k not in DATACITE_OPERATIONAL}
def registry_authors(payload,kind):
    attrs=payload['message'] if kind=='crossref' else payload['data']['attributes']
    out=[]
    for a in attrs.get('author',attrs.get('creators',[])):
        full=a.get('name') or ' '.join(a.get(k,'') for k in (['given','family'] if kind=='crossref' else ['givenName','familyName'])).strip()
        family=a.get('family') or a.get('familyName') or (full.split(',')[0] if ',' in full else full.split()[-1] if full else '')
        for v in [full,family]:
            if v and v not in out:out.append(v)
    return out

def read_url(url,capture_dir,label,allowed=(200,),attempts=3):
    """Only GET. Bounded retries for listed HTTP statuses and request/read exceptions; never a write."""
    require(attempts in (1,2,3),'Retry bound')
    capture_dir.mkdir(parents=True,exist_ok=True)
    for attempt in range(1,attempts+1):
        at=dt.datetime.now(dt.timezone.utc).isoformat();retry_after=None
        try:
            request=urllib.request.Request(url,headers={'User-Agent':UA,'Accept':'*/*'})
            with urllib.request.urlopen(request,timeout=40) as r:
                data=r.read();status=r.status;final_url=r.url;ctype=r.headers.get('Content-Type')
        except urllib.error.HTTPError as e:
            data=e.read();status=e.code;final_url=e.url;ctype=e.headers.get('Content-Type');retry_after=e.headers.get('Retry-After')
        except Exception as e:
            rec={'url':url,'at':at,'attempt':attempt,'error':repr(e),'read_only':True}
            (capture_dir/(label+f'_attempt{attempt}.json')).write_text(json.dumps(rec,indent=2)+'\n')
            if attempt==attempts:raise GateError('Read failed; preserved '+label) from e
            time.sleep(2*attempt);continue
        rec={'url':url,'at':at,'attempt':attempt,'status':status,'final_url':final_url,'bytes':len(data),'sha256':sha(data),'content_type':ctype,'read_only':True}
        (capture_dir/(label+f'_attempt{attempt}.bin')).write_bytes(data)
        (capture_dir/(label+f'_attempt{attempt}.json')).write_text(json.dumps(rec,indent=2)+'\n')
        if status in allowed:return data,rec
        if status not in RETRY_STATUSES or attempt==attempts:raise GateError('HTTP gate failed '+label+' status'+str(status)+'; no weakening or write')
        delay=2*attempt
        if retry_after and retry_after.isdigit():delay=max(delay,min(int(retry_after),10))
        time.sleep(delay)
    raise GateError('Unreachable read state')


def resolver_identity(url,doi):
    """Retain unknown URL fields; normalize only observed Springer cookie UUID."""
    parsed=urllib.parse.urlsplit(url)
    if (parsed.scheme=='https' and parsed.netloc=='link.springer.com'
            and urllib.parse.unquote(parsed.path).casefold()=='/article/'+doi.casefold()
            and not parsed.fragment):
        fields=urllib.parse.parse_qs(parsed.query,keep_blank_values=True)
        if (set(fields)=={'error','code'} and fields['error']==['cookies_not_supported']
                and len(fields['code'])==1
                and re.fullmatch(r'[0-9a-fA-F]{8}(?:-[0-9a-fA-F]{4}){3}-[0-9a-fA-F]{12}',fields['code'][0])):
            return urllib.parse.urlunsplit((parsed.scheme,parsed.netloc,parsed.path,
                   'error=cookies_not_supported&code=EPHEMERAL-UUID',''))
    return url


def strict_json(raw):
    def unique(pairs):
        obj={}
        for key,value in pairs:
            require(key not in obj,'Duplicate JSON key')
            obj[key]=value
        return obj
    def reject(value):raise GateError('Nonfinite JSON number')
    result=json.loads(raw,object_pairs_hook=unique,parse_constant=reject)
    require(typed_equal(result,result),'Non-JSON recursive type or nonfinite value')
    return result

def recursive_identity_hits(value,item):
    """Same exact aliases/PR grammar for every recursive key and value."""
    require(typed_equal(value,value),'Malformed recursive JSON evidence')
    texts=[]
    def walk(v):
        if type(v) is dict:
            for k,x in v.items():texts.append(k);walk(x)
        elif type(v) is list:
            for x in v:walk(x)
        elif type(v) is str:texts.append(v)
        else:texts.append(json.dumps(v,allow_nan=False))
    walk(value)
    # A word-bearing boundary prevents a PR label or identity fragment from
    # being assembled across two distinct JSON fields. Every key/value remains
    # present, and the exact same known-alias grammar runs once over the whole.
    combined='\x00__B1_JSON_FIELD_BOUNDARY__\x00'.join(texts)
    found=identity_hits([[],[combined]],item)
    return found[0]['matched'] if found else []
