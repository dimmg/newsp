from unidecode import unidecode


def slugify(string):
    """
    Slugifies a string.
    :param string: string to be slugified
    :return: slugified string
    :rtype: str
    """
    ascii_repr = unidecode(string)
    str_ = ' '.join(ascii_repr.split())

    return str_.lower().replace(' ', '-')


def paginated_response(items, total, offset, limit):
    """
    Generates paginated response.
    :param items: items to be paginated
    :param total: total count of items to be paginated
    :param offset: pagination offset
    :param limit: pagination limit
    :return: 
    """
    return {
        'items': items,
        'pagination': {
            'limit': limit,
            'offset': offset,
            'total': total
        }
    }
