import re
from unicodedata import normalize as ucnorm, category
from unidecode import unidecode


SLUG_RE = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')


def slugify(text, delimiter='-'):
    '''\
    Generate an ascii only slug from the text that can be
    used in urls or as a name.
    '''
    result = []
    for word in SLUG_RE.split(unicode(text).lower()):
        result.extend(unidecode(word).split())
    return unicode(delimiter.join(result))


def normalize_token(text):
    """ Simplify a piece of text to generate a more canonical
    representation. This involves lowercasing, stripping trailing
    spaces, removing symbols, diacritical marks (umlauts) and
    converting all newlines etc. to single spaces.
    """
    if not isinstance(text, unicode):
        text = unicode(text)
    text = text.lower()
    decomposed = ucnorm('NFKD', text)
    filtered = []
    for char in decomposed:
        cat = category(char)
        if cat.startswith('C'):
            filtered.append(' ')
        elif cat.startswith('M'):
            # marks, such as umlauts
            continue
        elif cat.startswith('Z'):
            # newlines, non-breaking etc.
            filtered.append(' ')
        elif cat.startswith('S') or cat.startswith('P'):
            # symbols, such as currency
            continue
        else:
            filtered.append(char)
    text = u''.join(filtered)
    while '  ' in text:
        text = text.replace('  ', ' ')
    text = text.strip()
    return ucnorm('NFKC', text)


def reverse_normalize(text):
    if not isinstance(text, unicode):
        text = unicode(text)
    decomposed = ucnorm('NFKD', text)
    filtered = []
    for char in decomposed:
        cat = category(char)
        if cat.startswith('Z'):
            # newlines, non-breaking etc.
            filtered.append(' ')
        elif cat.startswith('S') or cat.startswith('P'):
            # symbols, such as currency
            continue
        else:
            filtered.append(char)
    text = u''.join(filtered)
    while '  ' in text:
        text = text.replace('  ', ' ')
    text = ucnorm('NFKC', text).strip().split(' ')
    return ' '.join(reversed(text))


def normalize_text(text):
    """ This is vaguely stolen from:
    http://code.google.com/p/google-refine/wiki/ClusteringInDepth
    """
    text = text.strip().lower()
    text = normalize_token(text)
    tokens = text.split()
    tokens = sorted(set(tokens))
    return " ".join(tokens)
