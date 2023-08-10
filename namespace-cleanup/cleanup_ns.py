import argparse
import datetime
import pytz
import re
import requests
import json
from kubernetes import client, config

def check_for_old_namespaces(client, days):
    to_ignore = ['ccert', 'cert-manager', 'default','ingress-nginx', 'kube-node-lease', 'kube-public', 'kube-system', 'pipe-master-pool']
    to_report = []
    v1 = client.CoreV1Api()
    current_time = datetime.datetime.now(pytz.UTC)

    # Get all namespaces
    namespaces = v1.list_namespace().items

    for namespace in namespaces:
        namespace_creation_time = namespace.metadata.creation_timestamp
        age = current_time - namespace_creation_time

        if age.days >= days and namespace.metadata.name not in to_ignore:
            # print(f"Namespace matches with the criteria: {namespace.metadata.name}")
            to_report.append(namespace.metadata.name)
    
    return to_report

def get_issue_details(issue_id):
    # Construct the URL for the issue endpoint
    issue_url = f"{JIRA_BASE_URL}issue/{issue_id}"
    
    # Set up basic authentication
    auth = (JIRA_EMAIL, JIRA_TOKEN)
    
    try:
        # Make the API request
        response = requests.get(issue_url, auth=auth, headers={"Content-Type": "application/json"})
        
        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            assignee_name = data['fields']['assignee']['displayName']
            print(f"Assigne for issue {issue_id} is {assignee_name}")
            return assignee_name
        else:
            print(f"Failed to retrieve issue details. Status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


def main():
    reporting_data = dict()
    parser = argparse.ArgumentParser(description='Delete Kubernetes namespaces older than a certain number of days with a specified name regex.')
    parser.add_argument('days', type=int, help='Number of days to consider namespaces as old')
    args = parser.parse_args()

    # Load the Kubernetes config from the default location
    config.load_kube_config()


    # Delete old namespaces with the specified name regex
    to_report = check_for_old_namespaces(client, args.days)
    for namespace in to_report:
        assignee_name = get_issue_details("PIPE-"+namespace[1:])
        if assignee_name != None:
            reporting_data[namespace] = assignee_name
        else:
            reporting_data[namespace] = "Couldn't find an assigne"

    
    formatted_dict = "\n".join([f"{key}: {value}" for key, value in reporting_data.items()])
    
    message_string = f"""Namespaces to delete :
    {formatted_dict}
    These namespaces are older than {args.days} days"""

    print(message_string)

if __name__ == "__main__":
    main()
