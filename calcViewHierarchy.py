# Software licensed by the MIT License of Open Source (https://opensource.org/licenses/MIT)

import pyhdb
import urllib
from http.server import BaseHTTPRequestHandler, HTTPServer

# Change here the connection parameters for your HANA System
host = "0.0.0.0"
port = 30041
user = "USER"
pwsd = "PASSWORD"

# Recursive function to get all the dependencies from a view. It returns a JSON ready so the D3.js UI can render a hierarchy graph
def getDependent(view,parent,type,cursor,cache):
	if view not in cache:
		sql = 'SELECT BASE_OBJECT_NAME, BASE_OBJECT_TYPE FROM "PUBLIC"."OBJECT_DEPENDENCIES" WHERE DEPENDENT_OBJECT_NAME = \'' + view + '\' AND BASE_OBJECT_TYPE IN (\'VIEW\',\'TABLE\') AND DEPENDENCY_TYPE = 1';
		cursor.execute(sql)
		cache[view] = cursor.fetchall()
	result = cache[view]
	node = {}
	node['name'] = view
	node['parent'] = parent
	node['value'] = 10			# Standard size choosen
	node['type'] = 'black'		# Standard color choosen 
	if type == 'VIEW':
		node['level'] = 'red' 	# Meaning views
	else:
		node['level'] = 'green'	# Meaning tables
	if len(result) > 0:
		node['children'] = []
		for i in range(len(result)):
			node['children'].append(getDependent(result[i][0],view,result[i][1],cursor,cache))
			
	print('Hierarchy processed: ',node['name'])
	return node

# Open the connection to HANA DB and saves the result in a file at the same folder
def viewHierarchy(view):
	connection = pyhdb.connect(host = host, port = port, user = user, password = pwsd )
	cursor = connection.cursor()
	f = open('resultCalcViewHierarchy.json', 'w')
	f.write(str(getDependent(view,'null','VIEW',cursor,{})).replace("'",'"'))
	f.close()
	connection.close()
	
# If you want just wanna call the function withou the UI comment everything below and run this:
# viewHierarchy('<path>/<view>')

# Just a simple handler and HTTP Server set up
class MyHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		if '/calcViewHierarchy' in self.path:
			p = self.path.split("?")
			path = p[0][1:].split("/")
			params = {}
			if len(p) > 1:
				params = urllib.parse.parse_qs(p[1], True, True)
			print('Starting Hierarchy JSON with ',params['object'][0])
			viewHierarchy(params['object'][0])
			print('Finished Hierarchy JSON')

		if '/viewHierarchy' in self.path:
			f = open('viewHierarchy.html','rb')
			self.send_response(200)
			self.send_header('Content-type','text-html')
			self.end_headers()
			self.wfile.write(f.read())
			f.close()

		if self.path == '/resultCalcViewHierarchy':
			f = open('resultCalcViewHierarchy.json','rb')
			self.send_response(200)
			self.wfile.write(f.read())
			f.close()

def run():
  print('http server is starting...')
  httpd = HTTPServer(("", 5000), MyHandler)
  print('http server is running...')
  httpd.serve_forever()
  
if __name__ == '__main__':
  run()   