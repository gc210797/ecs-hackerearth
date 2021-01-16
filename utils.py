#!/usr/bin/env python3


def convert_to_dynamodb(**kwargs):
    ret = {}
    for key, value in kwargs.items():
        ret[key] = {
            'S': str(value)
        }

    return ret
