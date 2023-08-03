import argparse
import datetime
import pytz
import re
from kubernetes import client, config

def delete_old_namespaces(client, days, name_regex):
    v1 = client.CoreV1Api()
    current_time = datetime.datetime.now(pytz.UTC)

    # Get all namespaces
    namespaces = v1.list_namespace().items

    for namespace in namespaces:
        namespace_creation_time = namespace.metadata.creation_timestamp
        age = current_time - namespace_creation_time

        # Check if the namespace name matches the regex pattern
        if name_regex.match(namespace.metadata.name):
            # Check if the namespace is older than the specified number of days
            if age.days >= days:
                print(f"Deleting namespace: {namespace.metadata.name}")
                v1.delete_namespace(namespace.metadata.name)
            else:
                print(f"Namespace \"{namespace.metadata.name}\" is not older than {days}")
        else:
            print(f"Namespace \"{namespace.metadata.name}\" doesn't match the Regex {name_regex}")

def main():
    parser = argparse.ArgumentParser(description='Delete Kubernetes namespaces older than a certain number of days with a specified name regex.')
    parser.add_argument('days', type=int, help='Number of days to consider namespaces as old')
    parser.add_argument('name_regex', type=str, help='Regular expression to match the namespace name')
    args = parser.parse_args()

    # Load the Kubernetes config from the default location
    config.load_kube_config()

    # Compile the regex pattern
    name_regex = re.compile(args.name_regex)

    # Delete old namespaces with the specified name regex
    delete_old_namespaces(client, args.days, name_regex)

if __name__ == "__main__":
    main()
