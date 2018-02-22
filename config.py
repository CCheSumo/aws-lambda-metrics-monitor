from header import Header


class Config(object):
    x_sumo_source = 'metris_sla_aws_lambda_source'
    x_sumo_host = 'metrics_sla_aws_lambda_host'
    x_sumo_category = 'metrics_sla_lambda_category'
    http_method = 'POST'
    accept = 'application/json'
    content_type = 'application/json'
    metric_query = 'metric=metrics-sla'
    row_id = 'A'
    endpoint = '/api/v1/metrics/annotated/results'
    requested_data_points = 600
    max_data_points = 800
    # 5 sec, 30 sec, 1 min, 1h, 24h
    query_ranges = [5000, 30000, 60000, 3600000]
    sla_latency_max = 60000
    sleep_interval = 0.1
    request_interval = 1
    number_requests = 60

    query_headers = {
        Header.content_type: content_type,
        Header.accept: accept
    }

    send_logs_headers = {
        Header.content_encoding: 'deflate',
        Header.x_sumo_source: 'metris_sla_aws_lambda_source',
        Header.x_sumo_host: 'metrics_sla_aws_lambda_host',
        Header.x_sumo_category: 'metrics_sla_lambda_category'
    }

    send_metrics_headers = dict(send_logs_headers)
    send_metrics_headers.update({Header.content_type: 'application/vnd.sumologic.carbon2'})
