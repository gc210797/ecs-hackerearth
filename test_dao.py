#!/usr/bin/env python3

import dao
import utils

ds = dao.DSActions('data', 'users', 'http://localhost:8000')


def test_get_books():
    resp = ds.get_books("%s=%s" % ("title", "Madame Bovary"), 1)
    print(resp)
    assert len(resp['Items']) <= 20


def test_add_book():
    resp = ds.add_book(utils.convert_to_dynamodb(
        bookID="4009", title="test", authors="test", price=2))
    print(resp)
    assert resp['ResponseMetadata']['HTTPStatusCode'] == 200


def test_update_book():
    resp = ds.update_book(4009, {'authors': 'Jack the gsd'})
    print(resp)
    assert resp['ResponseMetadata']['HTTPStatusCode'] == 200


def test_get_book():
    resp = ds.get_book(4009)
    print(resp)
    assert resp['ResponseMetadata']['HTTPStatusCode'] == 200


def test_add_favourite():
    resp = ds.add_favourite(1, 4009)
    print(resp)
    assert resp['ResponseMetadata']['HTTPStatusCode'] == 200


def test_get_favourite():
    resp = ds.get_favourite(1)
    print(resp)
    assert resp[0] == '4009'


def test_boto3_key():
    from boto3.dynamodb.conditions import Key
    print(Key('test').eq('1'))
    assert 0 == 0


def test_remove_favourite():
    resp = ds.remove_favourite(1, 4009)
    print(resp)
    assert resp['ResponseMetadata']['HTTPStatusCode'] == 200
