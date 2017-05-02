from . import app
from unittest import mock


@mock.patch.object(app, 'update_projection')
@mock.patch.object(app, 'send_email')
def test_replay_events(send_email, update_projection):
    accounts = app.Accounts()

    with mock.patch.object(app, 'update_projection') as update_projection, \
            mock.patch.object(app, 'send_email') as send_email:
        user_id = accounts.genuuid()
        accounts.users.store('Registered', user_id, data={'email': 'joe@doe.com'}, revision=1)
        accounts.users.store('Registered', user_id, data={'email': 'kate@doe.com', 'password': 'secret'}, revision=2)

        assert update_projection.call_args_list == [mock.call(), mock.call()]
        assert send_email.call_args_list == [mock.call(), mock.call()]

    with mock.patch.object(app, 'update_projection') as update_projection, \
            mock.patch.object(app, 'send_email') as send_email:

        accounts.storage.replay_events()

        assert update_projection.call_args_list == [mock.call(), mock.call()]
        assert not send_email.called