#!/usr/bin/python
# -*- coding: utf-8 -*-

# config.py: configuration data of this app
#   - other modules should read config from here
#   - the config is first read from a json file
#   - env variables may override (in docker setup etc)

import sys
import os
import redis
import json

# first load config from a json file,
srvconf = json.load(open(os.environ["PYSRV_CONFIG_PATH"]))

# then override with env variables
for k, v in os.environ.items():
    if k.startswith("PYSRV_"):
        print("env override ", k)
        srvconf[k] = v

# grand switch to production!
IS_PRODUCTION = bool(srvconf['PYSRV_IS_PRODUCTION'] or False)

# local dev is simply my mac
IS_LOCAL_DEV = "darwin" in sys.platform and not IS_PRODUCTION
# IS_LOCAL_DEV = False

print("\nCONFIG: prod={},localdev={} ({})\n".format(
    IS_PRODUCTION, IS_LOCAL_DEV, srvconf["name"]))

# database config
DATABASE_HOST = srvconf['PYSRV_DATABASE_HOST']
DATABASE_NAME = srvconf['PYSRV_DATABASE_NAME']
DATABASE_USER = srvconf['PYSRV_DATABASE_USER']
DATABASE_PASSWORD = srvconf['PYSRV_DATABASE_PASSWORD']


# Flask + session config
# http://flask.pocoo.org/docs/1.0/config/
# https://pythonhosted.org/Flask-Session/
redishost = srvconf['PYSRV_REDIS_HOST']

flask_config = dict(
    # app config
    TESTING = IS_LOCAL_DEV,
    SECRET_KEY = None, # we have server-side sessions

    # session config - hardcoded to Redis
    SESSION_TYPE = 'redis',
    SESSION_REDIS = redis.from_url('redis://{}:6379'.format(redishost)),
    SESSION_COOKIE_NAME = "mycookie",
    SESSION_COOKIE_SECURE = not IS_LOCAL_DEV, # require https?
    SESSION_COOKIE_HTTPONLY = True, # don't allow JS cookie access
    SESSION_KEY_PREFIX = 'pysrv',
    PERMANENT_SESSION_LIFETIME = 60*60*24*30, # 1 month
    SESSION_COOKIE_DOMAIN = srvconf['PYSRV_DOMAIN_NAME'] if not IS_LOCAL_DEV else None,
)
