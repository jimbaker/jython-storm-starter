import random
import time

from backtype.storm.topology.base import BaseBasicBolt, BaseRichBolt, BaseRichSpout
from backtype.storm.tuple import Fields, Values



words = ["alice", "bob", "charles", "dana", "edward", "frances"]


class WordSpout(BaseRichSpout):

    def open(self, conf, context, collector):
        self._collector = collector

    def nextTuple(self):
        time.sleep(0.001)
        self._collector.emit(Values([random.choice(words)]))

    def declareOutputFields(self, declarer):
        declarer.declare(Fields(["word"]))

# would be nice to have a twitter spout; but probably best to use thrift for that



class ExclamationBolt(BaseBasicBolt):

    def prepare(self, conf, context, collector):
        self._collector = collector

    def execute(self, t):
        self._collector.emit(t, Values([t.getString(0) + " - nahhhh!!!"]))
        # self._collector.ack(t)

    def declareOutputFields(self, declarer):
        declarer.declare(Fields(["word"]))




