from ..storages import LocalMemoryStorage
from ..storages import Storage
from cq import events
from datetime import datetime
from freezegun import freeze_time
from unittest import mock
import pytest


# Base `Event` class tests.

def test_assigns_all_properties():
    d = datetime.utcnow()
    e = events.Event(id='evt', aggregate_id='agg', ts=d, name='evt_name', data=None)

    assert e.id == 'evt'
    assert e.aggregate_id == 'agg'
    assert e.ts == d


@freeze_time('2000-1-1')
@mock.patch.object(events, 'genuuid', return_value='evt_uuid')
def test_default_values_fields(_):
    e = events.Event(aggregate_id='agg', name='evt_name')

    assert e.id == 'evt_uuid'
    assert e.aggregate_id == 'agg'
    assert e.ts == datetime(2000, 1, 1)


@freeze_time('2000-1-1')
@mock.patch.object(events, 'genuuid', return_value='evt_uuid')
def test_serialize_event(_):
    d = datetime.utcnow()
    e = events.Event(id='evt', aggregate_id='agg', ts=d, name='evt_name', data=None)

    assert e.serialize() == {
        'id': 'evt',
        'aggregate_id': 'agg',
        'data': None,
        'name': 'Event',
        'ts': '2000-01-01T00:00:00+00:00'
    }


class SampleEvent(events.Event):
    schema_class = None


def test_serialize_no_schema():
    e = SampleEvent(aggregate_id='1')
    with pytest.raises(AttributeError) as exc:
        e.serialize()

    assert "SampleEvent.schema_class not defined." in str(exc.value)


# TODO: How should deserialization work?
# def test_deserialize_event():
#     data = {
#         'id': 'evt',
#         'aggregate_id': 'agg',
#         'data': None,
#         'name': 'evt_name',
#         'ts': '2000-01-01T00:00:00'
#     }
#
#     event = deserialize(data)

# More complex tests against event data nesting & serialization

class DataSchema(events.Schema):
    name = events.fields.Str(required=True)
    email = events.fields.Str(required=True)
    age = events.fields.Integer(required=True, type=int)


class UserRegisteredSchema(events.EventSchema):
    data = events.fields.Nested(DataSchema, required=True)


class UserRegisteredData:
    def __init__(self, name, email, age):
        self.name = name
        self.email = email
        self.age = age


class UserRegistered(events.Event):
    schema_class = UserRegisteredSchema


@freeze_time('2000-1-1')
def test_complex_serialization():
    data = UserRegisteredData(name='John', email='john.doe@gmail.com', age=20)
    e = UserRegistered(id='evt', aggregate_id='agg', data=data)

    assert e.serialize() == {
        'id': 'evt',
        'aggregate_id': 'agg',
        'name': 'UserRegistered',
        'ts': '2000-01-01T00:00:00+00:00',
        'data': {
            'name': 'John',
            'email': 'john.doe@gmail.com',
            'age': 20
        }
    }
