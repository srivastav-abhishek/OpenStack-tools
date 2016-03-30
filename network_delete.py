import requests
import json
import exceptions
import time
SUCCESS = 1
FAILURE = 0
CREATED = 201
ACCEPTED = 202
UN_AUTH = 401
DELETED = 204
CONFLICT = 409
userName = 'admin'
password = 'f6b53b58af604644'
tenantName = 'admin'
authPort ='5000'
protocol = 'http'
hostIp = '10.160.1.3'
postCred = '{"auth": {"tenantName": "%s", "passwordCredentials": {"username": "%s", "password": "%s"}}}' % (tenantName, userName, password)
url = "%s://%s:%s/v2.0/tokens" % (protocol, hostIp, authPort)
headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'User-Agent': 'python-keystoneclient'}
session = requests.Session()
try:
	resp = session.post(url, data=postCred, headers=headers, timeout=10.0)
	if resp.status_code == requests.codes.ok:
		token = json.loads(resp.text)["access"]["token"]["id"]
		#print token
	if resp.status_code == UN_AUTH:
		#print "Unauthorized Access"
		exit()
except exceptions.Exception as e:
	#print e
	#print "Unable To Reach Host %s" % hostIp
	exit()
#print "Token value : ", token
#headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'User-Agent':'python-keystoneclient', 'X-Auth-Token':'%s' % token}
headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'User-Agent':'python-neutronclient', 'X-Auth-Token':'%s' % token}
#postCred = {"tenant": {"enabled": true, "name": "test", "description": null}}
#postCred = '{"tenant": {"enabled": true, "name": "te6s121t1", "description": null}}'
authPort = '9696'
url = "%s://%s:%s/v2.0/networks.json" % (protocol, hostIp, authPort)
#print 'url '+url
author = (userName,password)
i=0
net_list = []
try:
	
	resp = session.get(url, headers=headers,  timeout=10.0)
	#print "Response ", resp.text
	if resp.status_code == requests.codes.ok:
	    networks = json.loads(resp.text)
	    while i!=len(networks["networks"]):
	        net_list.append(str(networks["networks"][i]["id"]))
	        i += 1
	    print "LEN",len(net_list)
	    print net_list
	elif resp.status_code == UN_AUTH:
			print "Unauthorized Access"
			exit()
except exceptions.Exception as e:
	print e
	print "Unable To Reach Host %s" % hostIp
	exit()
			

headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'User-Agent':'python-neutronclient', 'X-Auth-Token':'%s' % token}
url =  'http://10.160.1.3:9696/v2.0/networks/'

try:
    for net in net_list:
	print "net",net
	durl = url+net+".json"
	print url
        resp = session.delete(durl, headers=headers,  timeout=10.0)
        #print "Response Neutron ", resp.text
        if resp.status_code == requests.codes.ok:
                #LOG.info('TENANT RESPONSE: %s',json.loads)
                #print json.loads(resp.text)
		pass
        if resp.status_code == UN_AUTH:
                        print "Unauthorized Access"
                        exit()
except exceptions.Exception as e:
        print e
        print "Unable To Reach Host %s" % hostIp
        exit()
