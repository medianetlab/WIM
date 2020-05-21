#!/usr/bin/env python

import json
import logging
from bson.json_util import dumps

from wim.utils import mongoUtils

# Create the logger
logger = logging.getLogger(__name__)
stream_handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")
stream_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")
stream_handler.setFormatter(stream_formatter)
logger.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)


def update():
    with open("rules_db.json", mode="r") as rules_file:
        rules = json.load(rules_file)

    mongoUtils.delete_all("rules")
    mongoUtils.add_many("rules", rules)


def index():
    return dumps(mongoUtils.index_col("rules"))
