import random
import time

from backtype.storm.topology.base import BaseRichBolt, BaseRichSpout
from backtype.storm.tuple import Fields, Values
from clamp import PackageProxy

__all__ = ["WordSpout", "ExclamationBolt"]


words = ["alice", "bob", "charles", "dana", "edward", "frances"]


class WordSpout(BaseRichSpout):

    __proxymaker__ = PackageProxy("otter")

    def open(self, conf, context, collector):
        self._collector = collector

    def nextTuple(self):
        time.sleep(0.001)
        self._collector.emit(Values([random.choice(words)]))

    def declareOutputFields(self, declarer):
        declarer.declare(Fields(["word"]))


class ExclamationBolt(BaseRichBolt):

    __proxymaker__ = PackageProxy("otter")

    def prepare(self, conf, context, collector):
        self._collector = collector

    def execute(self, t):
        self._collector.emit(t, Values([t.getString(0) + " - nahhhh!!!"]))
        self._collector.ack(t)

    def declareOutputFields(self, declarer):
        declarer.declare(Fields(["word"]))
