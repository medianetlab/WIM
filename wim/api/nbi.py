from flask_classful import FlaskView
from flask import jsonify, request
import requests
import json

from wim.db.my_db import switches
from wim.db import mongoUtils
from bson.json_util import dumps

class SmView(FlaskView):
	"""
	Class inherited by FlaskView that created the API at route /api/sm
	"""

	route_prefix = '/api/'

	def get(self):
		return jsonify({"about": "This is the slice manager api"})

	def post(self):
		"""
		Create a new WAN Slice
		Get the wsd from the SM
		"""

		with open('wim/of-flows/genesis_normal','rb') as flow:
			headers = {"Accept": "application/xml" , "Content-type" : "application/xml"}
			r = requests.put('http://10.30.0.91:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:619760387514849152/flow-node-inventory:table/1/flow/genesis_normal',
				auth=('admin', 'admin'), data=flow, verify=False, headers=headers)

		return r.content



class AddvimView(FlaskView):
    """
    Class inherited by FlaskView that created the API at route /api/addvim
    """
    route_prefix = '/api/'

    def post(self):
    	"""
    	Receives any added vim from the slice manager
    	"""
    	data = request.json
    	mongoUtils.col_add('vim', data)
    	return "OK"
    	


class TestView(FlaskView):
	"""
	Class inherited by FlaskView that created the API at route /api/test
	"""
	route_prefix = '/api/'
	
	def get(self):
	    # mongoUtils.col_insert('switch_col', switches)
	    # print(mongoUtils.create_index('switch_col',['dpname', 'dpid']), flush=True)
	    return "OK"

