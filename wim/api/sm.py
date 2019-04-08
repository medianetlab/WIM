from flask_classful import FlaskView
from flask import jsonify, request

class SmView(FlaskView):
	"""
	Class inherited by FlaskView that created the API at route /api/sdn
	"""

	route_prefix = '/api/'

	def get(self):
		return jsonify({"about": "This is the slice manager api"})