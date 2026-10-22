#!/usr/bin/env python3
"""Conservative official Zenodo URI leads, not a resolver/equivalence oracle."""
from urllib.parse import urlsplit

# This code is embedded in ops_binding. Its ascii_lower/_decode/re names are
# provided by that module. No network, DNS, redirects or filesystem operations.
_URL_CANDIDATE=re.compile(r'(?:[A-Za-z][A-Za-z0-9+.-]*:)?//[^\s<>\"\']+')
_BARE_ZENODO=re.compile(r'(?<![A-Za-z0-9._@-])(?:www\.)?zenodo\.org\.*(?=[:/]|$)[^\s<>\"\']*',re.I|re.ASCII)
_MALFORMED_OFFICIAL_SCHEME=re.compile(r'(?<![A-Za-z0-9+.-])[A-Za-z][A-Za-z0-9+.-]*:/(?!/)(?:www\.)?zenodo\.org(?=[:./\\%\]]|$)[^\s<>\"\']*',re.I|re.ASCII)
_URL_TRAILING='.,;!)]}'


def _official_record_urls(text):
    result=set()
    if _MALFORMED_OFFICIAL_SCHEME.search(text):
        raise RuntimeError('Malformed official Zenodo scheme requires root identity review')
    candidates=[m.group(0) for m in _URL_CANDIDATE.finditer(text)]
    # A bare official hostname/path is a review-only reference, never a claim
    # of URI equivalence. Do not reinterpret a hostname embedded in another URL.
    for match in _BARE_ZENODO.finditer(text):
        if match.start() and text[match.start()-1] in '/':continue
        candidates.append('https://'+match.group(0))
    for raw in candidates:
        token=raw.rstrip(_URL_TRAILING)
        official_hint=bool(re.search(r'(?:^|[/@\[])\s*(?:www\.)?zenodo\.org(?=[:./\\%\]]|$)',ascii_lower(token)))
        try:
            parsed=urlsplit(token)
            host=parsed.hostname
        except ValueError as error:
            if official_hint:raise RuntimeError('Malformed official Zenodo URL requires root identity review') from error
            continue
        host=ascii_lower(host or '')
        if '%' in host and _decode(host,True).rstrip('.') in {'zenodo.org','www.zenodo.org'}:
            raise RuntimeError('Encoded official Zenodo authority requires root identity review')
        if host.rstrip('.') not in {'zenodo.org','www.zenodo.org'}:
            # Browser/URL-parser disagreements around backslash or encoded
            # authority syntax are unresolved, not silent absence of a lead.
            if official_hint and ('\\' in parsed.netloc or '%' in parsed.netloc or not parsed.netloc):
                raise RuntimeError('Ambiguous official Zenodo authority requires root identity review')
            continue
        if host.endswith('..') or parsed.username is not None or parsed.password is not None:
            raise RuntimeError('Ambiguous official Zenodo hostname/userinfo requires root identity review')
        scheme=ascii_lower(parsed.scheme)
        if scheme not in {'','http','https'}:
            raise RuntimeError('Unsupported official Zenodo transport requires root identity review')
        try:port=parsed.port
        except ValueError as error:
            raise RuntimeError('Malformed official Zenodo port requires root identity review') from error
        if parsed.netloc.endswith(':') or (port is not None and port!=({'http':80,'https':443}.get(scheme,443))):
            raise RuntimeError('Unverified official Zenodo port requires root identity review')
        path=_decode(parsed.path,True)
        if '\\' in path or any(ord(c)<32 or ord(c)==127 for c in path) or '%' in path:
            raise RuntimeError('Ambiguous official Zenodo path encoding requires root identity review')
        parts=[]
        for part in path.split('/'):
            if part in {'','.'}:continue
            if part=='..':
                if not parts:raise RuntimeError('Official Zenodo path escapes root; identity review required')
                parts.pop()
            else:parts.append(part)
        # Case-variant route spellings and slash normalization are merely
        # conservative references. We do not assert that every such URI routes.
        lowered=[ascii_lower(part) for part in parts]
        offset=2 if len(parts)>1 and lowered[:2]==['api','records'] else 1
        if (not parts or (offset==1 and lowered[0] not in {'record','records'})
                or len(parts)<=offset or not re.fullmatch('[0-9]+',parts[offset])):
            raise RuntimeError('Unresolved official Zenodo route requires root identity review')
        # The WHOLE ASCII path segment is a record-number lead. No substring,
        # Unicode digit conversion, DOI-suffix integer coercion or query ID.
        if len(parts[offset])>64 or int(parts[offset])<=0:
            raise RuntimeError('Unbounded/zero official record ID requires root identity review')
        result.add('10.5281/zenodo.'+str(int(parts[offset])))
        # Every remaining subresource stays a lead for this record; an export,
        # files or future subroute is not silently considered a different result.
    return result
