from urllib.parse import urljoin
import json
import os
import requests
import urllib3
from ansible.module_utils.basic import AnsibleModule


def run_module():
    # for access ticket
    csrf_token = ""
    ticket = ""

    home_dir = os.environ.get('HOME')
    path_to_token_file = os.path.join(home_dir, "proxmox_token.yml")

    # all parameters from ansible module
    ans_vars = {}

    module_args = dict(
        # for connection
        api_host=dict(type='str', required=True),  # ProxmoxVE host IP\FQDN
        api_password=dict(type='str', required=True, no_log=True),
        api_port=dict(type='str', required=False, default='8006'),
        api_user=dict(type='str', required=True),  # required format: name@realm
        # other
        append=dict(type='bool', required=False),
        comment=dict(type='str', required=False),
        delete=dict(type='bool', required=False),
        email=dict(type='str', required=False),
        enable=dict(type='bool', required=False),
        expire=dict(type='int', required=False),
        firstname=dict(type='str', required=False),
        groupid=dict(type='str', required=False),
        groups=dict(type='str', required=False),
        lastname=dict(type='str', required=False),
        password=dict(type='str', required=False, no_log=True),
        path=dict(type='str', required=False),
        privs=dict(type='str', required=False),
        privsep=dict(type='bool', required=False),
        propagate=dict(type='bool', required=False),
        resource=dict(type='str', required=False),
        roleid=dict(type='str', required=False),
        roles=dict(type='str', required=False),
        state=dict(type='str', required=True),
        tokenid=dict(type='str', required=False),
        tokens=dict(type='str', required=False),
        userid=dict(type='str', required=False),  # required format: name@realm
        users=dict(type='str', required=False),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # working...
    # disable insecure request warnings
    urllib3.disable_warnings()

    # copy all incoming parameters
    ans_vars.update(module.params)

    # specify ProxmoxVE host IP\FQDN and port
    host = ans_vars['api_host']
    port = ans_vars['api_port']

    # base URL for ProxmoxVE API
    api_entry_point = "https://" + host + ":" + port + "/api2/json/access/"

    # URLs for requests
    url_acl = urljoin(api_entry_point, "acl")
    url_groups = urljoin(api_entry_point, "groups/")
    url_groupid = urljoin(url_groups, ans_vars['groupid'])
    url_roles = urljoin(api_entry_point, "roles/")
    url_roleid = urljoin(url_roles, ans_vars['roleid'])
    url_users = urljoin(api_entry_point, "users/")
    url_userid = urljoin(url_users, ans_vars['userid']) + "/"
    url_token = urljoin(url_userid, "token/")
    url_tokenid = urljoin(url_token, ans_vars['tokenid'])

    # URL and parameters for access ticket request
    url = urljoin(api_entry_point, "ticket")
    request_params = {
        "username": ans_vars['api_user'],
        "password": ans_vars['api_password']
    }

    # get access ticket
    response = requests.post(url, params=request_params, verify=False, timeout=3)
    if response.status_code == 200:
        access_ticket = json.loads(response.text)
        csrf_token = access_ticket['data']['CSRFPreventionToken']
        ticket = access_ticket['data']['ticket']

    # open session
    session = requests.Session()
    session.cookies.set('PVEAuthCookie', ticket)

    # headers
    api_headers = {
        'CSRFPreventionToken': csrf_token
    }

    # get state
    state = ans_vars['state']

    # bool is not what it seems
    # errors":{"delete":"type check (''boolean'') failed - got ''True''"},
    # "message":"Parameter verification failed.\n"}
    # :sh1t: :angry: :fire:
    for k, v in ans_vars.items():
        if isinstance(v, bool):
            if v:
                ans_vars[k] = 1
            else:
                ans_vars[k] = 0

    # show section
    if state == "show":
        # show roles list or role info
        if ans_vars['resource'] == "roles":
            if ans_vars['roleid']:
                url = url_roleid
            else:
                url = url_roles

        # show groups list or group info
        elif ans_vars['resource'] == "groups":
            if ans_vars['groupid']:
                url = url_groupid
            else:
                url = url_groups

        # show token list or token info
        elif ans_vars['resource'] == "token":
            if ans_vars['tokenid']:
                url = url_tokenid
            else:
                url = url_token

        # show users list or user info
        elif ans_vars['resource'] == "users":
            if ans_vars['userid']:
                url = url_userid
            else:
                url = url_users

        # show acl
        elif ans_vars['resource'] == "acl":
            url = url_acl

        response = session.get(url, headers=api_headers, verify=False)

    # delete section
    if state == "absent":
        # delete token
        if ans_vars['tokenid'] and ans_vars['userid']:
            url = url_token
            response = session.get(url, headers=api_headers, verify=False)
            if ans_vars['tokenid'] in response.text:
                url = url_tokenid

        # delete user
        elif ans_vars['userid']:
            url = url_users
            response = session.get(url, headers=api_headers, verify=False)
            if ans_vars['userid'] in response.text:
                url = url_userid

        # delete group
        elif ans_vars["groupid"]:
            url = url_groups
            response = session.get(url, headers=api_headers, verify=False)
            if ans_vars["groupid"] in response.text:
                url = url_groupid

        # delete role
        elif ans_vars['roleid']:
            url = url_roles
            response = session.get(url, headers=api_headers, verify=False)
            if ans_vars['roleid'] in response.text:
                url = url_roleid

        response = session.delete(url, headers=api_headers, verify=False)

    # create section
    if state == "present":
        # create role
        if ans_vars['roleid']:
            url = url_roles
            response = session.get(url, headers=api_headers, verify=False)
            if ans_vars['roleid'] not in response.text:
                request_params = {
                    "roleid": ans_vars['roleid'],  # required
                    "privs": ans_vars['privs']
                }

        # create group
        elif ans_vars["groupid"]:
            url = url_groups
            response = session.get(url, headers=api_headers, verify=False)
            if ans_vars["groupid"] not in response.text:
                request_params = {
                    "groupid": ans_vars["groupid"],  # required
                    "comment": ans_vars['comment']
                }

        # create token
        elif ans_vars['tokenid'] and ans_vars['userid']:
            url = url_token
            response = session.get(url, headers=api_headers, verify=False)
            if ans_vars['tokenid'] not in response.text:
                url = url_tokenid
                request_params = {
                    "comment": ans_vars['comment'],
                    "expire": ans_vars['expire'],
                    "privsep": ans_vars['privsep']
                }

        # create user
        elif ans_vars['userid']:
            url = url_users
            if ans_vars['userid'] not in response.text:
                request_params = {
                    "userid": ans_vars['userid'],  # required
                    "append": ans_vars['append'],
                    "comment": ans_vars['comment'],
                    "email": ans_vars['email'],
                    "enable": ans_vars['enable'],
                    "expire": ans_vars['expire'],
                    "firstname": ans_vars['firstname'],
                    "groups": ans_vars['groups'],
                    "lastname": ans_vars['lastname'],
                    "password": ans_vars['password']
                }

        response = session.post(url, params=request_params, headers=api_headers, verify=False)

    # update section
    if state == "update":
        # update role
        if ans_vars['roleid']:
            url = url_roles
            response = session.get(url, headers=api_headers, verify=False)
            if ans_vars['roleid'] in response.text:
                url = url_roleid
                request_params = {
                    "append": ans_vars['append'],
                    "privs": ans_vars['privs']
                }

        # update group info
        elif ans_vars['groupid']:
            url = url_groups
            response = session.get(url, headers=api_headers, verify=False)
            if ans_vars["groupid"] in response.text:
                url = url_groupid
                request_params = {
                    "groupid": ans_vars['groupid'],
                    "comment": ans_vars['comment']
                }

        # update token
        elif ans_vars['tokenid'] and ans_vars['userid']:
            url = url_token
            response = session.get(url, headers=api_headers, verify=False)
            if ans_vars['tokenid'] in response.text:
                url = url_tokenid
                request_params = {
                    "comment": ans_vars['comment'],
                    "expire": ans_vars['expire'],
                    "privsep": ans_vars['privsep']
                }

        # renew password
        elif ans_vars['password'] and ans_vars['userid']:
            url = url_users
            response = session.get(url, headers=api_headers, verify=False)
            if ans_vars['userid'] in response.text:
                url = urljoin(api_entry_point, "password")
                request_params = {
                    "password": ans_vars['password'],
                    "userid": ans_vars['userid']
                }

        # update user info
        elif ans_vars['userid']:
            url = url_users
            response = session.get(url, headers=api_headers, verify=False)
            if ans_vars['userid'] in response.text:
                url = url_userid
                request_params = {
                    "userid": ans_vars['userid'],  # required
                    "append": ans_vars['append'],
                    "comment": ans_vars['comment'],
                    "email": ans_vars['email'],
                    "enable": ans_vars['enable'],
                    "expire": ans_vars['expire'],
                    "firstname": ans_vars['firstname'],
                    "groups": ans_vars['groups'],
                    "lastname": ans_vars['lastname'],
                }

        # change permissions
        elif ans_vars['path']:
            url = url_acl
            request_params = {
                "path": ans_vars['path'],  # required
                "roles": ans_vars['roles'],  # required
                "delete": ans_vars['delete'],
                "groups": ans_vars['groups'],
                "propagate": ans_vars['propagate'],
                "tokens": ans_vars['tokens'],
                "users": ans_vars['users']
            }

        response = session.put(url, params=request_params, headers=api_headers, verify=False)

    # gather token info
    if "full-tokenid" in response.text:
        token = json.loads(response.text)
        token_id = token['data']['full-tokenid']
        token_secret = token['data']['value']

        # write token into file
        with open(path_to_token_file, "w", encoding="utf-8") as file:
            file.write("---\n")
            file.write("token_id: " + token_id + "\n")
            file.write("token_secret: " + token_secret + "\n")

    module.exit_json(output=response.text)


def main():
    run_module()


if __name__ == '__main__':
    main()