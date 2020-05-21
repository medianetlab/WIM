# -*- coding: utf-8 -*-

"""
Module that implements the resources /slice and /slices for the nbi
"""

import logging
from bson.json_util import dumps

from flask_restful import Resource
from flask import request, jsonify

# Mongo DB and models have been replaced by neo4j db
from wim.utils import mongoUtils, kafkaUtils


# Create the logger
logger = logging.getLogger(__name__)
stream_handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")
stream_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")
stream_handler.setFormatter(stream_formatter)
logger.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)


class SliceApi(Resource):
    """
    The resource for the /slice api
    """

    def get(self, _id):
        """
        Find the slice from the database based on the id and return it
        If not found, return 404 error
        """
        _slice = mongoUtils.get("slice", _id)
        return (_slice, 200) if _slice else (f"Slice {_id} was not found", 404)

    def post(self, _id):
        """
        Create a new slice and store it in the database
        """
        args = request.json
        args["_id"] = _id
        if mongoUtils.get("slice", _id):
            return f"Slice {_id} already exists"
        producer = kafkaUtils.create_producer()
        wim_message = {"action": "create", "data": args}
        producer.send("wan-slice", value=wim_message)
        return (f"Creating Slice {_id}", 201)

    def delete(self, _id):
        """
        Delete an existing slice
        If not found, return 404 error
        """
        _slice = mongoUtils.get("slice", _id)
        if _slice:
            producer = kafkaUtils.create_producer()
            wim_message = {"action": "delete", "data": _id}
            producer.send("wan-slice", value=wim_message)
            return (f"Terrminating Slice {_id}", 200)
        else:
            return (f"Slice {_id} was not found", 404)


class SliceListApi(Resource):
    """
    The resource for the /slices API
    """

    def get(self):
        """
        Return a list with all the slices
        """
        slice_list = list(mongoUtils.index_col("slice"))
        return slice_list, 200
