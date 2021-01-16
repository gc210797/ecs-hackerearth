#!/usr/bin/env python3

import boto3


class DSActions:
    def __init__(self, book_table, user_table, endpoint_url=None):
        self.db = boto3.client('dynamodb', endpoint_url=endpoint_url)
        self.book_table = book_table
        self.user_table = user_table

    def get_books(self, filter, page_size, starting_token=None):
        paginator = self.db.get_paginator('scan')
        key, value = filter.split('=')
        response = paginator.paginate(TableName=self.book_table,
                                      PaginationConfig={
                                          'MaxItems': str(page_size),
                                          'StartingToken': starting_token
                                      },
                                      FilterExpression="%s = :value" % (key),
                                      ExpressionAttributeValues={
                                          ':value': {
                                              'S': value
                                          }
                                      }).build_full_result()
        return response

    def get_book(self, id):
        return self.db.get_item(TableName=self.book_table, Key={
            'bookID': {
                'S': str(id)
            }
        })

    def add_book(self, params):
        return self.db.put_item(TableName=self.book_table,
                                Item=params)

    def update_book(self, id, params):
        attr_updates = {}
        key = {
            'bookID': {
                'S': str(id)
            }
        }
        for k, v in params.items():
            attr_updates[k] = {
                'Value': {
                    'S': v
                }
            }

        return self.db.update_item(TableName=self.book_table,
                                   Key=key, AttributeUpdates=attr_updates,
                                   ReturnValues='UPDATED_NEW')

    def get_favourite(self, user_id):
        books = self.db.get_item(TableName=self.user_table, Key={
            'user_id': {
                'S': str(user_id)
            }
        })

        return [self.get_book(book)['Item']
                for book in books['Item']['books']['SS']]

    def add_favourite(self, user_id, book_id):
        key = {
            'user_id': {
                'S': str(user_id)
            }
        }
        attr_update = {
            'books': {
                'Value': {
                    'SS': [str(book_id)]
                },
                'Action': 'ADD'
            }
        }
        return self.db.update_item(TableName=self.user_table,
                                   Key=key, AttributeUpdates=attr_update,
                                   ReturnValues='UPDATED_NEW')

    def remove_favourite(self, user_id, book_id):
        key = {
            'user_id': {
                'S': str(user_id)
            }
        }
        attr_update = {
            'books': {
                'Value': {
                    'SS': [str(book_id)]
                },
                'Action': 'DELETE'
            }
        }
        return self.db.update_item(TableName=self.user_table, Key=key,
                                   AttributeUpdates=attr_update,
                                   ReturnValues='UPDATED_NEW')
