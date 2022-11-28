import requests
import hashlib
import sys

def requesting_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error Fetching: {res.status_code}, check the api and try again')
    return res

def get_passwordleak_count(hashes, hashes_to_check):
    hash = (list.split(":") for list in hashes.text.splitlines())
    for h, count in hash:
        if h == hashes_to_check:
            return count
    return 0

def pwned_api_check(password):
    sha1Password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first_5char, tail = sha1Password[:5], sha1Password[5:]
    response = requesting_api_data(first_5char)
    return get_passwordleak_count(response, tail)

def main(args):
    for password in args:
        count = pwned_api_check(password)
        if count:
            print(f'{password} was found {count} times.... it is a common password, Change it ASAP')
        if count == 0:
            print(f'{password} was NOT found and is a great password. Carry it on!')
    return 'done!'

main(sys.argv[1:])