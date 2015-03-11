import time, datetime,json
from flask import request
from .models import Distraction, Location, User
from . import app, db, locationresolver,utils
from .apis import api, APIError, APIValueError
from bson.son import SON
from django.contrib.gis.measure import Distance

EARTH_RADIUS_METERS = 6378137;

@app.route('/api/v1/sec/distractions',  methods=['POST'])
@api
def add_distraction():
    form = request.form
    da = Distraction()
    da.title = form.get('title', None)
    da.description = form.get('description', None)
    da.pay_type = int(form.get('paytype', '0'))
    da.create_user_id = int(form['createuser'])
    da.start_time = form['starttime']
    da.create_time = int(utils.timestamp_ms())
    
    address = form['address'];
    longitude = int(form.get('longitude', 0.0))
    lantitude = int(form.get('lantitude', 0.0))
    da.dst_loc = locationresolver.resolve(address, longitude, lantitude)
    da.save()
    return da.to_api(False), 0

def append_distance(da, distance):
    da['_id'] = str(da['_id'])
    da['farawayMeters'] = round(distance)
    uin = da['createUserId']
    del da['createUserId']
    user = User.objects.get(uin=uin)
    da['createUserInfo'] = {'uin' : uin,
                        'name' : user.name,
                        'headerImgUrl' : user.avatarId,
                        'sexType': user.sexType}
    return da

            
@app.route('/api/v1/sec/distractions',  methods=['get'])
@api
def nearby():
    args = request.args
    address = args.get('address', None);
    longitude = float(args.get('longitude', 0.0))
    latitude = float(args.get('latitude', 0.0))
    location = locationresolver.resolve(address, longitude, latitude)
    distance = float(args.get('distanceMeters', '50000.0'))
    per_num = int(args.get("maxItemPerPage", "10"))
    from_index = int(args.get("fromIndex", "0"))
    cmd = SON()
    cmd['geoNear'] = Distraction._get_collection_name()
    cmd['near'] = location.location
    cmd['maxDistance'] = distance/EARTH_RADIUS_METERS
    cmd['distanceMultiplier'] =EARTH_RADIUS_METERS 
    cmd['spherical'] = True
    dacol = Distraction.objects._collection
    cmd_rs = dacol.database.command(cmd)
    results = cmd_rs['results']
    if(from_index > len(results)):
        raise APIError(-1, from_index, 'start index is great than total')
    
    results = results[from_index:from_index+per_num]
    dalist = [append_distance(result['obj'], result['dis']) for result in results]
    page = utils.paginate_list(dalist, from_index, per_num)
    return page, 0
    
    
        