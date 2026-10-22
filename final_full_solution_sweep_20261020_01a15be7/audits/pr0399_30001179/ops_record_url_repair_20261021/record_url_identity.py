"""Conservative official Zenodo URI route classification, never HTTP equivalence.
Embedded into existing ops_binding.py; no new canonical module dependency.
"""
_URI_TOKEN=re.compile(r'''(?<![a-z0-9+._/@-])[a-z][a-z0-9+.-]{0,63}(?::|//)[^\s<>"\[\]{}()]+|//[^\s<>"\[\]{}()]+|(?<![a-z0-9._/@-])(?:www\.)?zenodo\.org(?=$|[.:/%?#\\\s<>"\[\]{}()\x27])(?:[.:/%?#\\][^\s<>"\[\]{}()]*)?''')
_ZENODO_HOSTS=frozenset({'zenodo.org','www.zenodo.org'})
_URL_TRAILING=frozenset('.,;:!?)]}\'')


def _url_uncertain(reason):
    raise RuntimeError('Unresolved official Zenodo URL requires root identity review: '+reason)


def _official_uri_authority(token):
    """Return a strict recognized authority/path parse, or None for another host."""
    from urllib.parse import urlsplit
    raw_token=token
    token=_decode(token,True)
    while token and token[-1] in _URL_TRAILING:token=token[:-1]
    bare=any(token==host or any(token.startswith(host+separator) for separator in '/:?#.') for host in _ZENODO_HOSTS)
    if re.match(r'[a-z][a-z0-9+.-]*//(?:www\.)?zenodo\.org(?:[/:?#.]|$)',token):
        _url_uncertain('scheme missing colon')
    scheme_match=None if bare else re.match(r'([a-z][a-z0-9+.-]*):',token)
    scheme=scheme_match.group(1) if scheme_match else None
    if scheme_match:
        rest=token[scheme_match.end():]
        if not rest.startswith('//'):
            # Recognized official-looking malformed URI, not an arbitrary URL
            # path containing this domain. No authority is guessed from a path.
            if any(rest.lstrip('/\\').startswith(host) for host in _ZENODO_HOSTS) or re.match(r'[^/]*@(?:www\.)?zenodo\.org(?:[/:?#.]|$)',rest):
                _url_uncertain('missing authority delimiter')
            return None
        rest=rest[2:]
        parse_text=token
    elif token.startswith('//'):
        rest=token[2:];parse_text=token
    else:
        rest=token;parse_text='//'+token
    authority=re.split(r'[/#?]',rest,1)[0]
    if not authority and any(rest.lstrip('/\\').startswith(host) for host in _ZENODO_HOSTS):
        _url_uncertain('empty official authority')
    userinfo,at,hostport=authority.rpartition('@')
    if not at:hostport=authority
    if hostport.startswith('['):
        if any(host in hostport for host in _ZENODO_HOSTS):_url_uncertain('bracketed official hostname')
        return None
    host,colon,port=hostport.partition(':')
    official=host in _ZENODO_HOSTS
    dotted=host.rstrip('.') in _ZENODO_HOSTS and not official
    if not official and not dotted:
        # A real nonofficial host remains nonofficial, including suffix/prefix
        # lookalikes. An exact official-looking userinfo is ambiguous, not a
        # target record on the actual foreign host.
        if at and any(re.search(r'(?<![a-z0-9._-])'+re.escape(h)+r'(?![a-z0-9._-])',userinfo) for h in _ZENODO_HOSTS):
            _url_uncertain('official-looking userinfo on another authority')
        if any(host.startswith(h) and len(host)>len(h) and (ord(host[len(h)])<33 or host[len(h)] in '\\%[]') for h in _ZENODO_HOSTS):
            _url_uncertain('control character in official-looking authority')
        return None
    if len(token)>16384:_url_uncertain('URI exceeds bounded review length')
    raw_rest=raw_token.split('://',1)[1] if '://' in raw_token else raw_token[2:] if raw_token.startswith('//') else raw_token
    if '%' in re.split(r'[/#?]',raw_rest,1)[0]:_url_uncertain('encoded official authority')
    if dotted:_url_uncertain('trailing-dot authority')
    if at:_url_uncertain('userinfo on official authority')
    if scheme not in {None,'http','https'}:_url_uncertain('unsupported scheme')
    if colon:
        if not re.fullmatch('[0-9]+',port):_url_uncertain('malformed port')
        default='80' if scheme=='http' else '443'
        if (port.lstrip('0') or '0')!=default:_url_uncertain('nondefault or unknown port')
    if any(ord(c)<33 or ord(c)==127 for c in token) or '\\' in token:
        _url_uncertain('control character or backslash')
    try:parsed=urlsplit(parse_text)
    except ValueError:_url_uncertain('unparseable authority')
    if parsed.netloc!=authority:_url_uncertain('authority parse changed')
    return parsed


def _zenodo_record_reference(token):
    parsed=_official_uri_authority(token)
    if parsed is None:return None
    path=parsed.path
    if not path.startswith('/'):_url_uncertain('missing absolute record path')
    # Removing dot segments and repeated separators only classifies review
    # leads. It does not certify redirect behavior or generic URI equivalence.
    parts=[]
    for part in path.split('/'):
        if part in {'','.'}:continue
        if part=='..':
            if parts:parts.pop()
            else:_url_uncertain('path escapes root')
        else:parts.append(part)
    if parts and parts[0] in {'record','records'}:offset=1
    elif len(parts)>1 and parts[:2]==['api','records']:offset=2
    else:_url_uncertain('unknown official route')
    if len(parts)<=offset:_url_uncertain('missing record ID')
    identifier=parts[offset]
    if not re.fullmatch('[0-9]+',identifier) or len(identifier)>128:
        _url_uncertain('record ID is not a bounded whole ASCII integer')
    identifier=identifier.lstrip('0') or '0'
    if identifier=='0':_url_uncertain('nonpositive record ID')
    tail=parts[offset+1:]
    if tail:
        resource=tail[0]
        if resource=='files':
            pass  # File collection or descendants remain parent-record leads.
        elif resource=='export':
            if len(tail)!=2 or not re.fullmatch('[a-z0-9][a-z0-9._-]{0,127}',tail[1]):
                _url_uncertain('malformed export route')
        elif resource in {'draft','versions','citations','references','communities','preview','files-archive'}:
            pass  # Explicit parent-record subresource class; not theorem identity.
        else:_url_uncertain('unknown record subresource')
    return '10.5281/zenodo.'+identifier


def _official_record_url_leads(text):
    # Nonoverlapping whole URI tokens prevent capturing an official-looking
    # substring from a foreign URL's authority, path or query. Only ASCII case
    # is translated; no Unicode hostname/path folding is used.
    lowered=ascii_lower(text)
    names=set()
    # Whole-token authority precheck handles even long bare userinfo without
    # scanning arbitrary hostname substrings or an unbounded prefix regex.
    for token in re.findall(r'''[^\s<>"\[\]{}()]+''',lowered):
        if '@' in token:_official_uri_authority(token)
    for match in _URI_TOKEN.finditer(lowered):
        name=_zenodo_record_reference(match.group(0))
        if name is not None:names.add(name)
    return names


_BOUND_OWR_CITATION=re.compile(r'(?<![a-z0-9_])owr[ \t]+(?P<report>10)/(?P<year>(?:19|20)[0-9]{2})[ \t]+pp\.?[ \t]*(?P<first>[1-9][0-9]{0,5})[ \t]*[-–][ \t]*(?P<last>[1-9][0-9]{0,5})(?=$|[\s.,;:])')
_SHORT_NAME=re.compile(r'(?<![a-z0-9.])10/[a-z0-9]+(?:$|[\s?#.,;)])')


def _unresolved_short_name(text):
    lowered=ascii_lower(text)
    masked=list(lowered)
    for match in _BOUND_OWR_CITATION.finditer(lowered):
        if int(match.group('last'))<int(match.group('first')):continue
        source=r'(?<![a-z0-9.])10\.4171/owr/'+match.group('year')+'/'+match.group('report')
        if not any(_bounded_token(lowered,item.start(),item.end()) for item in re.finditer(source,lowered)):continue
        # Only the typed report-number/year span is ordinary bibliography.
        # Every other short name or resolver URI in this cell remains visible.
        start=match.start('report');end=match.end('year')
        masked[start:end]=' '*(end-start)
    return bool(_SHORT_NAME.search(''.join(masked)))
