from django_sharding_library.sharding_functions import BaseBucketingStrategy


class UserGroupBucketingStrategy(BaseBucketingStrategy):
    def __init__(self, shard_group, databases, max_range):
        super().__init__(shard_group)
        self.shards = self.get_shards(databases)
        self.max_range = max_range

    def pick_shard(self, shard_key):
        shard_key = int(shard_key)
        return self.shards[shard_key % self.max_range]

    def get_shard(self, shard_key):
        return self.pick_shard(shard_key)