def tag_reader(raw_tags: str):
    """

    :param str raw_tags:
    :return list:
    >>> tag_reader('presenilin-1 presenilin-2')
    {'presenilin-1', 'presenilin-2'}
    >>> tag_reader('“Bouchard microaneurysms”')
    {'Bouchard microaneurysms'}
    >>> tag_reader('astrocytoma “Rosenthal fibers”')
    {'astrocytoma', 'Rosenthal fibers'}
    >>> tag_reader('“Frontotemporal dementia” TDP-43')
    {'Frontotemporal dementia', 'TDP-43'}
    """
    output = set()
    tag = ''
    do_purge = True
    for char in raw_tags:
        if char == '“':
            do_purge = False
        elif char == '”':
            do_purge = True
        elif char == '\"':
            do_purge = not do_purge
        elif char == ' ' and do_purge:
            output.add(tag)
            tag = ''
        else:
            tag += char

    if tag != '':
        output.add(tag)

    return output


def to_raw_tags(tags: iter):
    """

    :param iter tags:
    :return str:
    >>> to_raw_tags(['presenilin-1', 'presenilin-2'])
    'presenilin-1 presenilin-2'
    >>> to_raw_tags(['Bouchard microaneurysms'])
    '“Bouchard microaneurysms”'
    >>> to_raw_tags(['astrocytoma', 'Rosenthal fibers'])
    'astrocytoma “Rosenthal fibers”'
    >>> to_raw_tags(['Frontotemporal dementia', 'TDP-43'])
    '“Frontotemporal dementia” TDP-43'
    """
    if isinstance(tags, str):
        tags = tags.split(' ')

    formatted_tags = set()
    for entry in set(tags):
        if ' ' in entry or '\"' in entry:
            entry = '“{}”'.format(entry.replace('\"', '\\\"'))
        formatted_tags.add(entry)

    return ' '.join(formatted_tags)
