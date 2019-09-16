from bridge import token_header, make_request, base_uri

def post_new_article(data):
    return make_request(
        url=base_uri+'/articles/new',
        headers=token_header,
        data=data
    )