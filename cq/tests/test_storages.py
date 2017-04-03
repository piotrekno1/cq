from ..genuuid import genuuid
from ..storages import LocalMemoryStorage
from ..storages import Storage
from ..events import Schema
from cq import events
from datetime import datetime
from unittest import mock
import pytest


class UserRegistered(events.Event):
    pass


class UserActivated(events.Event):
    pass


@pytest.fixture
def local_storage():
    return LocalMemoryStorage()


@mock.patch('cq.storages.genuuid', lambda: 'EVENT_ID')
@mock.patch('cq.storages.publish')
def test_store(publish):
    storage = Storage()
    evt = UserRegistered(aggregate_id='aggregate_id')

    with mock.patch.object(storage, 'append') as append:
        storage.store(evt)

    append.assert_called_once_with(evt)
    publish.assert_called_once_with(evt)


def test_local__append(local_storage):
    joe_registered = UserRegistered(aggregate_id='JOE_ID', data={'name': 'joe'})
    jane_registered = UserRegistered(aggregate_id='JANE_ID', data={'name': 'jane'})
    joe_activated = UserActivated(aggregate_id='JOE_ID')

    local_storage.store(joe_registered)
    local_storage.store(jane_registered)
    local_storage.store(joe_activated)

    assert local_storage.events == [joe_registered, jane_registered, joe_activated]


def test_local__get_events(local_storage):
    joe_registered = UserRegistered(aggregate_id='JOE_ID', data={'name': 'joe'})
    jane_registered = UserRegistered(aggregate_id='JANE_ID', data={'name': 'jane'})
    joe_activated = UserActivated(aggregate_id='JOE_ID')

    local_storage.store(joe_registered)
    local_storage.store(jane_registered)
    local_storage.store(joe_activated)

    assert local_storage.get_events('JOE_ID') == [joe_registered, joe_activated]
    assert local_storage.get_events('JANE_ID') == [jane_registered]


def test_local__book_unique(local_storage):
    local_storage.book_unique('user_email', 'joe@doe.com', 'JOE_ID')
    assert local_storage.has_unique('user_email', 'joe@doe.com') is True
    assert local_storage.get_unique('user_email', 'joe@doe.com') == 'JOE_ID'


def test_local__book_unique_fails_for_duplicate(local_storage):
    local_storage.book_unique('user_email', 'joe@doe.com', 'JOE_ID')

    with pytest.raises(Storage.DuplicatedItemError):
        local_storage.book_unique('user_email', 'joe@doe.com', 'JOE_ID2')

    # first value should not be overridden
    assert local_storage.get_unique('user_email', 'joe@doe.com') == 'JOE_ID'
