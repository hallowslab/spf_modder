VALID_LIST=[
    'top-domain.tld.  60      IN      TXT     "v=spf1 +a +mx +ip4:123.45.678.90 +ip4:12.345.678.900 +include:spf.domain.tld ~all"',
    'domain.tld.      14400   IN      TXT     "v=spf1 ip4:123.45.678.90 +a +mx +ip4:12.345.678.900 +ip4:12.345.123.456 +ip4:12.345.432.1 include:_spf.google.com include:domain.tld ~all"'
    'domain.tl.  14400   IN      TXT     "v=spf1 +a +mx +ip4:123.45.123.45 ~all"'
]