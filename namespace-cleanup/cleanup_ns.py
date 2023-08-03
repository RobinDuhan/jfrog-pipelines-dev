pipelines:
  - name: clean_old_namespaces
    steps:
      - name: run_python_cleanup_script
        type: Bash
        configuration:
          environmentVariables:
            age_to_delete:
              default: 10
              description: Deletes namespaces older than age_to_delete
              allowCustom: true
            name_regex:
              default: "a*"
              description: Deletes namespaces older matching the regex provided
              allowCustom: true
          integrations:
            - name: test_kubernetes
        execution:
          onExecute:
            - "cd namespace-cleanup && pip3 install -r requirements.txt"
            - "python3 ../cleanup_ns.py $age_to_delete $name_regex"

