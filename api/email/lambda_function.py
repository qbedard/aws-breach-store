import os
import json
import boto3
from aws_requests_auth.aws_auth import AWSRequestsAuth
from elasticsearch import Elasticsearch, RequestsHttpConnection


def lambda_handler(event, context):
    email = event['pathParameters']['email']
    session = boto3.session.Session()
    credentials = session.get_credentials().get_frozen_credentials()

    es_host = os.environ['ES_HOST']
    awsauth = AWSRequestsAuth(
        aws_access_key=credentials.access_key,
        aws_secret_access_key=credentials.secret_key,
        aws_token=credentials.token,
        aws_host=es_host,
        aws_region=session.region_name,
        aws_service='es'
    )

    es = Elasticsearch(
        hosts=[{'host': es_host, 'port': 443}],
        http_auth=awsauth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection
    )

    es_response = es.search(index='identity', body={
        'query': {
            'constant_score': {
                'filter': {
                    'term': {
                        'email': email
                    }
                }
            }
        }})

    results = []
    for hit in es_response['hits']['hits']:
        results.append(hit['_source'])

    response_body = {'hits': es_response['hits']['total'], 'results': results}

    response = {
        'isBase64Encoded': False,
        'statusCode': 200,
        'headers': {'Access-Control-Allow-Origin': '*',
                    'Content-Type': 'application/json'},
        'body': json.dumps(response_body)
    }

    return response
