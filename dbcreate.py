from werkzeug.security import generate_password_hash
from venus import db, create_app
import os,json
from venus.models import IDCounter, User, Tag, Topic, Scenic, RecommendFeed, Distraction, HotFocus

    

#迁移老数据库
def migrate_db():
    pass

def init_user():
    uinCounter = IDCounter(key='uin', value='10000')
    uinCounter.save();
    
    user = User(uin=101, name='admin101', phone='13760480101', _password=generate_password_hash('123456'), role=User.ADMIN, avatar_id='http://www.funnycity.cn/venus/api/v1/image/header1')
    user.save()
    user = User(uin=102, name='admin102', phone='13760480102', _password=generate_password_hash('123456'), role=User.ADMIN, avatar_id='http://www.funnycity.cn/venus/api/v1/image/header2')
    user.save()
    user = User(uin=103, name='admin103', phone='13760480103', _password=generate_password_hash('123456'), role=User.ADMIN, avatar_id='http://www.funnycity.cn/venus/api/v1/image/header3')
    user.save()
    
def init_tag():
    tag = Tag(name='榜单', created_by=101, scope='of', subject = 'album')
    tag.save()
    tag = Tag(name='今日推荐', created_by=101, scope='of', subject = 'album')
    tag.save()
    tag = Tag(name='小编推荐', created_by=101, scope='of', subject = 'album')
    tag.save()
    
    tag = Tag(name='自然风景', created_by=101, scope='of', subject = 'scenic')
    tag.save()
    tag = Tag(name='人文古迹', created_by=101, scope='of', subject = 'scenic')
    tag.save()
    tag = Tag(name='商家', created_by=101, scope='of', subject = 'scenic')
    tag.save()
    
    tag = Tag(name='发呆', created_by=101, scope='pu', subject = 'scenic')
    tag.save()  
    tag = Tag(name='情侣约会', created_by=101, scope='pu', subject = 'scenic')
    tag.save()
    tag = Tag(name='拍照',created_by=101, scope='pu', subject = 'scenic')
    tag.save()
    tag = Tag(name='遛娃', created_by=101, scope='pu', subject = 'scenic')
    tag.save()
    tag = Tag(name='看美女', created_by=101, scope='pu', subject = 'scenic')
    tag.save()
    tag = Tag(name='看球赛', created_by=101, scope='pu', subject = 'scenic')
    tag.save()

    tag = Tag(name='户外活动', created_by=101, scope='of', subject = 'distraction')
    tag.save() 
    tag = Tag(name='朋友聚会', created_by=101, scope='of', subject = 'distraction')
    tag.save()
    tag = Tag(name='优惠券', created_by=101, scope='of', subject = 'distraction')
    tag.save()
    
    tag = Tag(name='徒步/穿越', created_by=101, scope='pu', subject = 'distraction')
    tag.save() 
    tag = Tag(name='爬山', created_by=101, scope='pu', subject = 'distraction')
    tag.save() 
    tag = Tag(name='钓鱼', created_by=101, scope='pu', subject = 'distraction')
    tag.save()  
    tag = Tag(name='采摘', created_by=101, scope='pu', subject = 'distraction')
    tag.save()
    tag = Tag(name='农家乐', created_by=101, scope='pu', subject = 'distraction')
    tag.save()
    
def init_topic():
    topic = Topic(name='#美女最多的酒吧#', created_by=101, subject = 'scenic')
    topic.save()  
    topic = Topic(name='#最豪华的水疗会所#', created_by=101,  subject = 'scenic')
    topic.save()
    topic = Topic(name='#风景这边独好#', created_by=101, subject = 'scenic')
    topic.save()
        
def init_hotspot():
    scenic_tags = Tag.objects(subject='scenic', scope='pu')
    for tag in scenic_tags:
        focus=HotFocus(focus=tag)
        focus.save()
        
    scenic_topic = Topic.objects(subject='scenic')
    for topic in scenic_topic:
        focus=HotFocus(focus=topic)
        focus.save()
        
def init_scenic_feed():
    scenic_data_base = 'venus/static/data/scenic'
    scenic_list = os.listdir(path=scenic_data_base)
    topic = Topic.objects.get(name='#风景这边独好#')
    for name in scenic_list:
        file = open(os.path.join(scenic_data_base, name), encoding='utf-8')
        scenic = Scenic.from_json(file.read())
        file.close()
        scenic.topic = topic
        scenic.tag_list=[tag for tag in Tag.objects(scope='pu', subject='scenic')]
        scenic.save()
        
def init_distraction_feed():
    da_data_base = 'venus/static/data/distraction'
    da_list = os.listdir(path=da_data_base)
    for name in da_list:
        file = open(os.path.join(da_data_base, name), encoding='utf-8')
        distraction = Distraction.from_json(file.read())
        file.close()
        distraction.tag_list=[tag for tag in Tag.objects(scope='pu', subject='distraction')]
        distraction.save()

 
def init_recommend_feed():
    scenics = Scenic.objects() 
    for scenic in scenics:
        recommend = RecommendFeed(feedid=str(scenic.id), subject='scenic')
        recommend.save() 
    
    distractions = Distraction.objects() 
    for distraction in distractions:
        recommend = RecommendFeed(feedid=str(distraction.id), subject='distraction')
        recommend.save()
        
def create_all():
    version = IDCounter(key='db_version', value=1)
    version.save()
    init_user()
    init_tag()
    init_topic()
    init_hotspot()
    init_scenic_feed()
    init_distraction_feed()
    init_recommend_feed()

if __name__ == "__main__":
    app = create_app('settings_dev.py')
    db.init_app(app)
    create_all()