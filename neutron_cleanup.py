import requests
import json
import exceptions
SUCCESS = 1
FAILURE = 0
CREATED = 201
ACCEPTED = 202
UN_AUTH = 401
DELETED = 204
CONFLICT = 409


class NeutronCleaner():
    def __init__(self, controller_ip="localhost", username="admin",
                 password=None, tenant="admin", port="5000"):
        self.controller_ip = controller_ip
        self.userName = username
        self.password = password
        self.tenantName = tenant
        self.authPort = port
        self.protocol = 'http'
        self.session = requests.Session()
        self.token = self._get_token()
        self.token_header = {'Content-Type': 'application/json',
                             'Accept': 'application/json',
                             'User-Agent': 'python-neutronclient',
                             'X-Auth-Token': '%s' % self.token}
        self.tenantId = self._get_tenant_id()

    def _get_token(self):
        try:
            url = "%s://%s:%s/v2.0/tokens" % (self.protocol,
                                              self.controller_ip,
                                              self.authPort)
            print url
            headers = {'Content-Type': 'application/json',
                       'Accept': 'application/json',
                       'User-Agent': 'python-keystoneclient'}
            data = '{"auth": {"tenantName": "%s", '\
                   '"passwordCredentials":{"username": "%s", "password":'\
                   '"%s"}}}' % (self.tenantName, self.userName, self.password)
            print data

            resp = self.session.post(url,
                                     data=data,
                                     headers=headers, timeout=10.0)
            if resp.status_code == requests.codes.ok:
                token = json.loads(resp.text)["access"]["token"]["id"]
                return token
            if resp.status_code == UN_AUTH:
                exit()
        except exceptions.Exception as e:
            print e
            exit()

    def _get_tenant_id(self):
        url = self.get_url('tenants')
        resp = self.session.get(url,
                                headers=self.token_header,
                                timeout=10.0)
        resp_body = json.loads(resp.text)
        print resp_body
        tenant_id = resp_body['tenants'][0]['id']
        print tenant_id
        return tenant_id

    def get_url(self, resource):
        if resource in ['ports', 'routers', 'networks']:
            auth_port = '9696'
            url_str = "%s://%s:%s/v2.0/%s.json"
        if resource in ['tenants']:
            auth_port = '35357'
            url_str = "%s://%s:%s/v2.0/%s"
        if resource in ['servers']:
            auth_port = '8774'
            return "%s://%s:%s/v2/%s/%s/detail" % (self.protocol,
                                                   self.controller_ip,
                                                   auth_port,
                                                   self.tenantId,
                                                   resource)
        return url_str % (self.protocol,
                          self.controller_ip,
                          auth_port, resource)

    def cleanup_resources(self, *args):
        for arg in args:
            print arg
            url = self.get_url(arg)
            print url
            try:
                resp = self.session.get(url,
                                        headers=self.token_header,
                                        timeout=10.0)
                if resp.status_code == requests.codes.ok:
                    resources = json.loads(resp.text)
                    print resources
                    i = 0
                    resource_list = []
                    while i != len(resources[arg]):
                        resource_list.append(str(resources[arg][i]["id"]))
                        print resource_list
                        i += 1
                    print "LEN", len(resource_list)
                    print resource_list
                elif resp.status_code == UN_AUTH:
                    print "Unauthorized Access"
                    exit()
                for resource in resource_list:
                    print "resource %s %s " % (arg, resource)
                    if arg not in ['servers']:
                        durl = url.split('.json')[0]+'/'+resource+".json"
                    else:
                        durl = url.split('detail')[0]+'/'+resource
                        print durl
                    resp = self.session.delete(durl,
                                               headers=self.token_header,
                                               timeout=10.0)
                    if resp.status_code == requests.codes.ok:
                        pass
                    if resp.status_code == UN_AUTH:
                        print "Unauthorized Access"
                        exit()
            except exceptions.Exception as e:
                    print e
                    print "Unable To Reach Host %s" % self.controller_ip
                    exit()


def main():
    obj = NeutronCleaner('10.101.1.40', 'admin', 'noir0123', 'admin')
    obj.cleanup_resources('servers', 'ports', 'routers', 'networks')


if __name__ == '__main__':
    main()
