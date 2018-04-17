from urllib import parse


def update_url_query_params(url, **query_params):
    url_parts = list(parse.urlparse(url))

    query = dict(parse.parse_qsl(url_parts[4]))
    query.update(query_params)

    url_parts[4] = parse.urlencode(query)
    return parse.urlunparse(url_parts)
