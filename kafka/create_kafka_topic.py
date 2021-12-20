from kafka.admin import KafkaAdminClient, NewTopic
import json

config_file = "kafka_topics_config.json"
with open(config_file, "r") as f:
    config = json.load(f)

client_id = config["client_id"]
bootstrap_servers = config["bootstrap_servers"]

admin_client = KafkaAdminClient(
    bootstrap_servers=bootstrap_servers, 
    client_id=client_id
)
num_partitions = 1
replication_factor = 1

topic_list = []
for topic in config["topic"]:
    name = topic["name"]
    num_partitions = topic["num_partitions"]
    replication_factor = topic["replication_factor"]
    topic_list.append(NewTopic(name=name, num_partitions=num_partitions, replication_factor=replication_factor))

admin_client.create_topics(new_topics=topic_list, validate_only=False)
print(f"all topics from config file {config_file} created")