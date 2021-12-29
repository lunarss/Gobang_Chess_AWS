from __future__ import print_function # Python 2/3 compatibility
import boto3
import json

from boto3.dynamodb.conditions import Key, Attr

from flask import render_template, url_for, redirect, request
from app import webapp

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

class Dynamodb:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    
    def dynamodb_put(self, table, item):
        table = self.dynamodb.Table(table)

        response = table.put_item(
        Item = item
        )

        return response

    def dynamodb_get(self, table, key, projectionExpression):
        table = self.dynamodb.Table(table)

        response = table.get_item(
        Key = key,
            ProjectionExpression = projectionExpression
        )

        data = {}

        if 'Item' in response:
            item = response['Item']
            data.update(item)

        return data

    def dynamodb_delete(self, table, key):
        table = self.dynamodb.Table(table)

        response = table.delete_item(
        Key = key
        )

        return response

    def dynamodb_update(self, table, key, updateExpression, expressionAttributeValues):
        table = self.dynamodb.Table(table)



        response = table.update_item(
        Key = key,
            UpdateExpression = updateExpression,
            ExpressionAttributeValues = expressionAttributeValues
        )

        return response


    def list_all(self, table, projectionExpression):

        table = self.dynamodb.Table(table)


        # FilterExpression=fe,

        response = table.scan(
            ProjectionExpression = projectionExpression,
            )

        records = []

        for i in response['Items']:
            records.append(i)

        while 'LastEvaluatedKey' in response:
            response = table.scan(
                ProjectionExpression=projectionExpression,
                ExclusiveStartKey=response['LastEvaluatedKey']
                )

            for i in response['Items']:
                records.append(i)

        return records

