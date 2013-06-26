import time

from backtype.storm import Config, LocalCluster
from backtype.storm.tuple import Fields, Values
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

    cluster = LocalCluster()
    builder = get_topology_builder()
    cluster.submitTopology("exclamation", conf, builder.createTopology())
    time.sleep(100000)
    cluster.killTopology("exclamation")
    cluster.shutdown()


if __name__ == "__main__":
    main()





