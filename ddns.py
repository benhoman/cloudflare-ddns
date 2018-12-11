import json
import os
import requests


def get_ip():
    url = 'http://ip.42.pl/raw'
    response = requests.get(url)
    return str(response.text)


def get_cloudflare_ip(url, headers):
    response = requests.get(url, headers=headers)
    response_data = response.json()
    return str(response_data["result"]["content"])


def set_cloudflare_ip(url, headers, current_ip):
    payload = {
            'type': 'A',
            'name': record_name,
            'content': current_ip
            }
    response = requests.put(URL, headers=headers, data=json.dumps(payload))
    print(response.status_code)


def do_ddns():
    zone_id = os.environ.get('ZONE_ID')
    record_id = os.environ.get('RECORD_ID')
    api_key = os.environ.get('API_KEY')
    user_email = os.environ.get('USER_EMAIL')
    record_name = os.environ.get('RECORD_NAME')
    url = 'https://api.cloudflare.com/client/v4/zones/%(zone_id)s/dns_records/%(record_id)s' % {'zone_id': zone_id, 'record_id': record_id}
    headers = {
            'X-Auth-Email': user_email,
            'X-Auth-Key': api_key,
            'Content-Type': 'application/json'
            }

    # Get Host IP Address
    current_ip = get_ip()
    # Get Cloudflare DNS Record IP Address
    cloudflare_ip = get_cloudflare_ip(url, headers)

    # If IP Address is the same do nothing
    if current_ip == cloudflare_ip:
        print("IP has not changed. Doing Nothing")
    else:
        print("IP has changed. Updating IP to: %(current_ip)s" % {'current_ip': current_ip})
        set_cloudflare_ip(url, headers, current_ip)


if __name__ == '__main__':
    do_ddns()
