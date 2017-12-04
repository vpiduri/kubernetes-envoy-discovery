import os
from distutils.util import strtobool

from flask import Flask
from flask_marshmallow import Marshmallow


app = Flask(__name__)
# Allow trailing, or no trailing slashes
app.url_map.strict_slashes = False
# Is Envoy running as an internal k8s service?
app.config['internal_k8s_envoy'] = strtobool(os.environ.get('INTERNAL_K8S_ENVOY', 'True'))
ma = Marshmallow(app)

from envoy_discovery_service.v1.blueprint import v1_blueprint  # noqa

app.register_blueprint(v1_blueprint, url_prefix='/v1')
