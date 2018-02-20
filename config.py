from header import Header


class Config(object):

    http_method = 'POST'
    accept = 'application/json'
    content_type = 'application/json'
    metric_query = 'metric=metrics-sla'
    row_id = 'A'
    endpoint = '/api/v1/metrics/annotated/results'
    requested_data_points = 600
    max_data_points = 800
    time_range = 60000
    sleep_interval = 0.1
    request_interval = 1
    number_requests = 60

    headers = {
        Header.content_type: content_type,
        Header.accept: accept
    }
