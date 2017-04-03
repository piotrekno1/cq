import uuid
from .genuuid import genuuid
from datetime import datetime
from marshmallow import Schema
from marshmallow import fields


def isoformat(format, dt):
    return dt.isoformat()


def get_datetime(val=None):
    if not val:
        return datetime.utcnow()
    return val


def get_id():
    return genuuid()


class EventSchema(Schema):
    """
    Base event class that specifies must have event fields.
    """
    id = fields.Str(required=True, default=get_id)
    aggregate_id = fields.Str(required=True)
    name = fields.Str(required=True)
    ts = fields.DateTime(
        required=True,
        # use `get_datetime` is ts is not provided on init
        default=get_datetime,
        # use `get_datetime` if `ts=None` on init
        format='iso'
    )

    data = fields.Nested(Schema, required=False)


class Event:
    schema_class = EventSchema

    def __init__(self, aggregate_id, id=None, name=None, ts=None, data=None):
        self.id = id or get_id()
        self.ts = ts or get_datetime()
        self.aggregate_id = aggregate_id
        self.data = data

    def serialize(self):
        if not self.schema_class:
            raise AttributeError("%s.schema_class not defined." % self.get_name())

        schema = self.schema_class(strict=True)
        result = schema.dump(self)
        result.data['name'] = self.get_name()
        return result.data

    def get_name(self):
        return self.__class__.__qualname__

    def __str__(self):
        return '%s | %s | %s' % (self.get_name(), self.aggregate_id, self.ts)
