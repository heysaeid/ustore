from django.test.runner import DiscoverRunner
from django.conf import settings
from redis import Redis 

class UnitTstRunner(DiscoverRunner):

    def teardown_databases(self, old_config, **kwargs):
        r = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
        r.flushdb()