from flask_classful import FlaskView
from flask import jsonify, request

from wim.sm.sm import handle_slice

class SmView(FlaskView):
	"""
	Class inherited by FlaskView that created the API at route /api/sdn
	"""

	route_prefix = '/api/'

	def get(self):
		return jsonify({"about": "This is the slice manager api"})

	def post(self):
		"""
		Create a new WAN Slice
		Get the wsd from the SM
		"""

		return jsonify(handle_slice(request.json))