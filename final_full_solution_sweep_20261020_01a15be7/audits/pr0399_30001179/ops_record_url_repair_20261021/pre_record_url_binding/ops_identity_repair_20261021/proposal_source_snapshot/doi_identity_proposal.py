#!/usr/bin/env python3
"""PROPOSAL ONLY: ASCII DOI comparison plus conservative encoded-identity leads.

No string recognized here proves publication/result equivalence. Literal DOI
names and percent-encoded unreserved ASCII octets have narrow normalization;
reserved/nested encodings, record URLs and fragments are review leads only.
All leads block an automatic duplicate mutation. No network or filesystem I/O.
"""
import re

_ASCII_LOWER=str.maketrans('ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz')
_UNRESERVED=frozenset('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~')
_TERMINATORS=frozenset(")]}>\"',;:!?&#")
_PERCENT=re.compile(r'%([0-9A-Fa-f]{2})')
_NAME=re.compile(r'10\.5281/zenodo\.([0-9]+)')
_FRAGMENT=re.compile(r'zenodo\.([0-9]+)')
_RECORD=re.compile(r'https?://(?:www\.)?zenodo\.org/(?:api/)?records?/([0-9]+)')


def ascii_lower(value):
    return value.translate(_ASCII_LOWER)


def _bounded_token(text,start,end):
    if start and (text[start-1].isalnum() or text[start-1] in '._'):
        return False
    rest=text[end:]
    if not rest:
        return True
    first=rest[0]
    if first=='.':
        tail=rest.lstrip('.')
        return not tail or tail[0].isspace() or tail[0] in _TERMINATORS
    return first.isspace() or first in _TERMINATORS


def _names(text):
    lowered=ascii_lower(text)
    return {'10.5281/zenodo.'+m.group(1) for m in _NAME.finditer(lowered)
            if _bounded_token(lowered,m.start(),m.end())}


def _review_names(text):
    lowered=ascii_lower(text)
    result={'10.5281/zenodo.'+m.group(1) for m in _FRAGMENT.finditer(lowered)
            if _bounded_token(lowered,m.start(),m.end()) and (not m.start() or lowered[m.start()-1]!='/')}
    for match in _RECORD.finditer(lowered):
        rest=lowered[match.end():]
        if _bounded_token(lowered,match.start(),match.end()) or rest.startswith('/files/'):
            # Leading-zero record-URL IDs are only conservative aliases/leads;
            # leading zeros in an actual DOI suffix are never discarded.
            result.add('10.5281/zenodo.'+str(int(match.group(1))))
    return result


def _decode(text,unreserved_only):
    def replace(match):
        character=chr(int(match.group(1),16))
        return character if not unreserved_only or character in _UNRESERVED else match.group(0)
    return _PERCENT.sub(replace,text)


def inspect_identity(value):
    if not isinstance(value,str):
        raise RuntimeError('DOI identity input must be text')
    if len(value)>1_000_000:
        raise RuntimeError('DOI identity text exceeds review bound')
    normalized=_decode(value,True)
    canonical=_names(value)|_names(normalized)
    review=_review_names(value)|_review_names(normalized)
    current=value
    depth_limited=False
    for count in range(8):
        decoded=_decode(current,False)
        if decoded==current:
            break
        current=decoded
        review|=_names(current)|_review_names(current)
    else:
        depth_limited=_decode(current,False)!=current
    malformed=False
    for token in re.findall(r'\S+',current):
        lowered=ascii_lower(token)
        if any(hint in lowered for hint in ['10.5281','zenodo.','doi.org','zenodo.org']):
            if re.search(r'%(?![0-9A-Fa-f]{2})',token):
                malformed=True
    return {'canonical_names':frozenset(canonical),'review_names':frozenset(review-canonical),
            'ambiguous_encoding':depth_limited or malformed or bool(
                re.search(r'(?<![a-z0-9.])10/[a-z0-9]+(?:$|[\s?#.,;)])',ascii_lower(current))
                or re.search(r'https?://(?:www\.)?shortdoi\.org(?:/|$)',ascii_lower(current))
                or re.search(r'https?://(?:dx\.)?doi\.org/[a-z][a-z0-9]*(?:$|[\s?#.,;)])',ascii_lower(current))),
            'scope':'Lexical identity/dedup leads only; reserved/nested encodings are not certified URI equivalence.'}


def zenodo_doi_leads(value):
    result=inspect_identity(value)
    if result['ambiguous_encoding']:
        raise RuntimeError('Unresolved DOI/URL encoding requires root identity review')
    return result['canonical_names']|result['review_names']


def target_in_row(row,identifier,family_ids=()):
    if type(identifier) is not int or identifier<=0:
        raise RuntimeError('Expected target record ID must be an exact positive integer')
    if not isinstance(row,(list,tuple)):
        raise RuntimeError('Identity row must be a sequence of text cells')
    ids={identifier}
    for value in family_ids:
        if type(value) is not int or value<=0:raise RuntimeError('Malformed family ID requires root review')
        ids.add(value)
    targets={'10.5281/zenodo.'+str(value) for value in ids}
    # Evaluate every cell so a later unresolved encoding cannot be hidden by an
    # earlier match. This recognizer never writes a canonically rewritten row.
    identities=[zenodo_doi_leads(value) for value in row]
    return any(targets & names for names in identities)


def record_identity_ids(record,identifier):
    """Target/concept/typed version-parent IDs are conservative family leads only."""
    def integer(value):
        if type(value) is int and value>0:return value
        if isinstance(value,str) and re.fullmatch('[1-9][0-9]*',value):return int(value)
        raise RuntimeError('Malformed recognized record-family identity requires root review')
    if not isinstance(record,dict) or integer(record.get('id'))!=identifier:
        raise RuntimeError('Expected record-family identity missing')
    result={identifier}
    if record.get('conceptrecid') is not None:result.add(integer(record['conceptrecid']))
    if record.get('conceptdoi') is not None:
        value=record['conceptdoi']
        match=re.fullmatch(r'10\.5281/zenodo\.([1-9][0-9]*)',ascii_lower(value)) if isinstance(value,str) else None
        if not match:raise RuntimeError('Unparsed concept DOI requires root identity review')
        result.add(int(match.group(1)))
    metadata=record.get('metadata',{})
    relations=metadata.get('relations',{})
    if not isinstance(relations,dict):raise RuntimeError('Unparsed record relations require root identity review')
    versions=relations.get('version',[])
    if not isinstance(versions,list):raise RuntimeError('Unparsed version relations require root identity review')
    for version in versions:
        parent=version.get('parent') if isinstance(version,dict) else None
        if not isinstance(parent,dict) or parent.get('pid_type')!='recid':
            raise RuntimeError('Unparsed version parent requires root identity review')
        result.add(integer(parent.get('pid_value')))
    if record.get('parent') is not None:
        parent=record['parent']
        if not isinstance(parent,dict) or 'id' not in parent:raise RuntimeError('Unparsed parent record requires root review')
        result.add(integer(parent['id']))
    return sorted(result)
