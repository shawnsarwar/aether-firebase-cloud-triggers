#!/usr/bin/env python

# Copyright (C) 2020 by eHealth Africa : http://www.eHealthAfrica.org
#
# See the NOTICE file distributed with this work for additional information
# regarding copyright ownership.
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# 'AS IS' BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

import pytest

from .fixtures import *  # noqa
# from .aether_functions import *  # noqa
from .app.fb_utils import halve_iterable, sanitize_topic
from .app.config import get_kafka_config, kafka_admin_uses, get_kafka_admin_config
from .app.hash import make_hash


@pytest.mark.unit
def test__kafka_config():
    _conf = get_kafka_config()
    for k in kafka_admin_uses.keys():
        assert(_conf.get(k) is not None)
    _conf = get_kafka_admin_config()
    assert(set(_conf.keys()) == set(kafka_admin_uses.keys()))


@pytest.mark.parametrize('test,expected', [
    ('%topic', '_topic'),
    ('Someother.topic', 'Someother.topic'),
    ('a_third&option', 'a_third_option')
])
@pytest.mark.unit
def test__sanitize_topic_name(test, expected):
    assert(sanitize_topic(test) == expected)


@pytest.mark.unit
def test__fixture(simple_payload):
    assert(True)


@pytest.mark.unit
def test__event_reverse():
    evt = EventType.WRITE
    db = DatabaseType.CFS
    descriptor = event_from_type(db, evt)
    t_db, t_evt = info_from_event(descriptor)
    assert(evt is t_evt)
    assert(db is t_db)


@pytest.mark.unit
def test__contextualize(simple_entity):
    gen = simple_entity(10)
    evt = EventType.WRITE
    db = DatabaseType.CFS
    for e in gen:
        res = contextualize(e, evt, db)
        assert(
            res.get('context').get('eventType') == event_from_type(db, evt)
        )
        assert(
            res.get('data').get('body') == e.payload['body']
        )


@pytest.mark.unit
def test__halve_iterable():
    a = [1, 2, 3, 4, 5]
    b, c = halve_iterable(a)
    assert(len(b) == 3)
    assert(len(c) == 2)


@pytest.mark.unit
def test__hash():
    _type_a = 'a'
    _type_b = 'b'
    doc_a = {'a': 'value', 'list': [1, 2, 3]}
    doc_b = {'a': 'value', 'list': [2, 1, 3]}
    doc_c = {'a': 'value', 'list': [2, 1]}
    assert(make_hash(_type_a, doc_a) == make_hash(_type_a, doc_a))
    assert(make_hash(_type_a, doc_a) != make_hash(_type_b, doc_a))
    assert(make_hash(_type_a, doc_a) == make_hash(_type_a, doc_b))
    assert(make_hash(_type_a, doc_a) != make_hash(_type_a, doc_c))