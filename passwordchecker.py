import requests
import hashlib
import sys

#request for password api data
def request_api_data(query_char):
    url = ('https://api.pwnedpasswords.com/range/' + query_char)
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching: {res.status_code}, check the api and try again')
    return res

# def read_res(response):
#     print(response.text)

def get_password_leaks_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0

#api password check and then hash the password
def pwned_api_check(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_char)
    return get_password_leaks_count(response, tail)


#Read password from a file
def main(my_file):
    with open('pwd.txt', mode='r') as my_file:
        for password in my_file:
            count = pwned_api_check(password)
            pass_lent = '*' * len(password)
            if count:
                print(f'{pass_lent} was found {count} times... you should probably change your password!')
            else:
                print(f'{pass_lent} was not found. Carry on!')
        return 'done'

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))

