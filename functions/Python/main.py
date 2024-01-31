import logging


def handler(event, context):
    logger = logging.getLogger()
    logger.info('Hello from main.py')

    '''Event Functionalities'''
    data = event.get_data()  # event data
    time = event.get_time()  # event occurred time
    action = event.get_action()
    source_details = event.get_source()
    source_entity_id = event.get_source_entity_id()
    event_bus_details = event.get_event_bus_details()
    project_details = event.get_project_details()

    '''Context Functionalities'''
    # remaining_execution_time_ms = context.get_remaining_execution_time_ms()
    # max_execution_time_ms = context.get_max_execution_time_ms()
    # context.close_with_failure()
    context.close_with_success()
