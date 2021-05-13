"""GIGServer."""
import time

from flask import Flask
from flask_caching import Cache

from utils.sysx import log_metrics
import gig.ents
import gig.nearby
import gig.ext_data

DEFUALT_CACHE_TIMEOUT = 1

log_metrics()
app = Flask(__name__)
cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})
cache.init_app(app)

# ----------------------------------------------------------------
# Handlers
# ----------------------------------------------------------------


@app.route('/')
@cache.cached(timeout=DEFUALT_CACHE_TIMEOUT)
def index():
    """Index."""
    return log_metrics()


@app.route('/entity/<string:entity_id>')
@cache.cached(timeout=DEFUALT_CACHE_TIMEOUT)
def entity(entity_id):
    """Get entity."""
    return gig.ents.get_entity(entity_id)


@app.route('/entity_ids/<string:entity_type>')
@cache.cached(timeout=DEFUALT_CACHE_TIMEOUT)
def entity_ids(entity_type):
    """Get entity IDs."""
    return {
        'entity_ids': gig.ents.get_entity_ids(entity_type),
    }


@app.route('/nearby/<string:latlng_str>')
@cache.cached(timeout=DEFUALT_CACHE_TIMEOUT)
def nearby(latlng_str):
    """Get places near latlng."""
    lat, _, lng = latlng_str.partition(',')
    lat_lng = (float)(lat), (float)(lng)
    return {
        'nearby_entity_info_list': gig.nearby.get_nearby_entities(lat_lng),
    }


@app.route(
    '/ext_data/<string:data_group>/<string:table_id>/<string:entity_id>'
)
@cache.cached(timeout=DEFUALT_CACHE_TIMEOUT)
def ext_data(data_group, table_id, entity_id):
    """Get extended data."""
    return gig.ext_data.get_table_data(data_group, table_id, [entity_id])
