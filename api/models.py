from django.db import models
from django.apps import apps

from django_sharding_library.decorators import model_config, shard_storage_config
from django_sharding_library.models import TableStrategyModel
from django_sharding_library.fields import TableShardedIDField

# Create your models here.

# @shard_storage_config()
@model_config(database='default')   # 샤딩하지 않을 모델을 위한 설정
class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(null=False, blank=False, unique=True, max_length=128)

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        managed = True
        db_table = 'users'
        app_label = 'api'


@model_config(database='default')
class PostIDs(TableStrategyModel):   # 샤드된 각각의 Post에게 고유의 ID를 부여하기 위한 모델
    """
    IDs For sharded Posts
    """

    class Meta:
        managed = True
        db_table = 'post_ids'
        app_label = 'api'


@model_config(shard_group='user_group')
class Post(models.Model):
    id = TableShardedIDField(primary_key=True, source_table_name='api.PostIDs')   # 샤드된 Post들이 고유의 ID를 갖게 됨.
    title = models.CharField(null=False, blank=False, unique=True, max_length=128)
    user_id = models.BigIntegerField(null=False, blank=False)   # 자동으로 테이블을 복제시키는 방법을 몰라서 일단 수동으로 넣는 것으로..(라이브러리에서는 지원 안 함.)

    def get_shard(self):   # 각 Post가 자신의 버켓팅 전략에 맞게 샤드를 갖고 올 수 있도록 get_shard 메소드를 작성. 샤딩할 모델에는 get_shard 메소드를 반드시 작성해야 함.
        shard_group = getattr(self, 'django_sharding__shard_group')
        django_sharding_app = apps.get_app_config('django_sharding')
        bucketer = django_sharding_app.get_bucketer(shard_group)

        return bucketer.get_shard(self.user_id)

    class Meta:
        managed = True
        db_table = 'posts'
        app_label = 'api'