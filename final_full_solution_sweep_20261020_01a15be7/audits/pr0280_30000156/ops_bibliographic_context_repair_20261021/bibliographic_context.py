#!/usr/bin/env python3
"""Embedded proposal: literal, unique, same-cell OWR bibliography context only."""
# Embedded after _decode in ops_binding; re/ascii_lower/_bounded_token supplied.
_SHORT_CODE=re.compile(r'(?<![a-z0-9.])10/')
_OWR_CONTEXT=re.compile(r'(?<![a-z0-9_])owr[ \t]+(?P<token>10/(?P<year>[0-9]{4}))')
_OWR_SOURCE_HINT=re.compile(r'(?<![a-z0-9.])10\.4171/owr(?:/|$)')
_OWR_SOURCE=re.compile(r'10\.4171/owr/(?P<year>[0-9]{4})/(?P<report>[1-9][0-9]*)')
_BARE_SHORT_RESOLVER=re.compile(r'(?<![a-z0-9._@/-])(?:www\.)?shortdoi\.org\.*(?=[:/]|$)[^\s<>"\']*',re.I|re.ASCII)


def _unresolved_short_resolver(value):
    """Known resolver hosts with unknown aliases stay review-only.

    This deliberately makes no claim about route reachability or a valid code
    alphabet. Full numeric DOI-prefix paths remain with the DOI recognizer.
    """
    if re.search(r'(?<![a-z0-9+.-])[a-z][a-z0-9+.-]*:/(?!/)(?:www\.)?(?:shortdoi|doi)\.org(?=[:./\\%\]]|$)',ascii_lower(value)):
        return True
    candidates=[m.group(0) for m in _URL_CANDIDATE.finditer(value)]
    candidates+=['https://'+m.group(0) for m in _BARE_SHORT_RESOLVER.finditer(value)]
    for token in candidates:
        try:parsed=urlsplit(token.rstrip(_URL_TRAILING));host=ascii_lower(parsed.hostname or '').rstrip('.')
        except ValueError:
            if re.search(r'[/@\[](?:www\.)?(?:shortdoi|doi)\.org',ascii_lower(token)):
                return True
            continue
        if ('\\' in parsed.netloc or '%' in parsed.netloc) and re.search(r'(?:^|[@\[])(?:www\.)?(?:shortdoi|doi)\.org(?=[:./\\%\]]|$)',ascii_lower(parsed.netloc)):
            return True
        if host in {'shortdoi.org','www.shortdoi.org'}:return True
        if host in {'doi.org','dx.doi.org'}:
            path=_decode(parsed.path,True)
            parts=[]
            for part in path.split('/'):
                if part in {'','.'}:continue
                if part=='..':
                    if not parts:return True
                    parts.pop()
                else:parts.append(part)
            if len(parts)<2 or not re.fullmatch(r'10\.[0-9]+',parts[0]):return True
    return False


def _unresolved_short_code(value):
    """Mask one qualified *literal* report token, then detect all other codes.

    This does not infer a shortDOI alphabet, resolve an alias, or exempt any
    target DOI/record identity. Duplicate contexts/source hints fail closed.
    """
    literal=ascii_lower(value)
    contexts=[m for m in _OWR_CONTEXT.finditer(literal)
              if _bounded_token(literal,m.start('token'),m.end('token'))]
    sources=[m for m in _OWR_SOURCE.finditer(literal)
             if _bounded_token(literal,m.start(),m.end())]
    hints=list(_OWR_SOURCE_HINT.finditer(literal))
    decoded_sources=literal
    for unused in range(8):
        decoded=_decode(decoded_sources,False)
        if decoded==decoded_sources:break
        decoded_sources=decoded
    decoded_hints=list(_OWR_SOURCE_HINT.finditer(ascii_lower(decoded_sources)))
    candidate=value
    if (len(contexts)==len(sources)==len(hints)==len(decoded_hints)==1
            and contexts[0].group('year')==sources[0].group('year')
            and sources[0].group('report')=='10'):
        first,last=contexts[0].span('token')
        candidate=value[:first]+(' '*(last-first))+value[last:]
    # Do not let literal contextual recognition exempt an encoded, nested or
    # additional short code anywhere else in this same cell.
    for unused in range(8):
        decoded=_decode(candidate,False)
        if decoded==candidate:break
        candidate=decoded
    return bool(_SHORT_CODE.search(ascii_lower(candidate)))
