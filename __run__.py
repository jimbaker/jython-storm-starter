from backtype.storm import Config, StormSubmitter
from backtype.storm.topology import TopologyBuilder

from excl.plumbing import ExclamationBolt, WordSpout


def get_topology_builder():
    builder = TopologyBuilder();        
    builder.setSpout("words", WordSpout(), 4)
    builder.setBolt("exclaim1", ExclamationBolt(), 2).shuffleGrouping("words")
    builder.setBolt("exclaim2", ExclamationBolt(), 2).shuffleGrouping("exclaim1")
    return builder


def main():
    conf = Config()
    conf.setDebug(True)
    conf.setNumWorkers(2)
    builder = get_topology_builder()
    StormSubmitter.submitTopology("exclamation", conf, builder.createTopology())


main()

