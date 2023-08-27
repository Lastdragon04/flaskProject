import re


def SQL_defend(SQL_sentence):
    pattern = re.compile(
        r"(%27)|(\')|(\-\-)|(%23)|(#)|"  # Regex for detection of SQL meta-characters
        r"\w*((%27)|(\'))\s+((%6F)|o|(%4F))((%72)|r|(%52))\s*|"  # Modified regex for detection of SQL meta-characters eg: ' or 1 = 1' detect word 'or',
        r"((%3D)|(=))[^\n]*((%27)|(\')|(\-\-)|(%3B)|(;))"  # Regex for typical SQL Injection attack eg: '= 1 --'
        r"((%27)|(\'))union|"  # Regex for detecting SQL Injection with the UNION keyword
        r"((%27)|(\'))select|"  # Regex for detecting SQL Injection with the UNION keyword
        r"((%27)|(\'))insert|"  # Regex for detecting SQL Injection with the UNION keyword
        r"((%27)|(\'))update|"  # Regex for detecting SQL Injection with the UNION keyword
        r"((%27)|(\'))drop",  # Regex for detecting SQL Injection with the UNION keyword
        re.IGNORECASE,
    )
    print(SQL_sentence)
    r = pattern.search(SQL_sentence)
    if r:
        return False
    else:
        return True
