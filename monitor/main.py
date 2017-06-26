from apscheduler.schedulers.background import BackgroundScheduler
from app import MONITOR_CONF


class Mointor(object):

    [item for item in MONITOR_CONF.MONITOR_ITEM]