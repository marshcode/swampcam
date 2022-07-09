def execute_pipeline(pipeline_actions, captures):

    for action in pipeline_actions:
        captures = action(captures)

    return captures