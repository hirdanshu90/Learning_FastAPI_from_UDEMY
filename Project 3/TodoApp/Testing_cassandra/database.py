from cassandra.cluster import Cluster

# Connect to the Cassandra cluster
cluster = Cluster(['127.0.0.1'])  # Replace with your cluster's IP addresses
session = cluster.connect()

# Create the keyspace (if it doesn't exist)
session.execute("""
    CREATE KEYSPACE IF NOT EXISTS my_keyspace
    WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 3};
""")

# Switch to the keyspace
session.set_keyspace('my_keyspace')

# Create the users table (if it doesn't exist)
session.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id UUID PRIMARY KEY,
        name TEXT,
        email TEXT,
        age INT
    );
""")
