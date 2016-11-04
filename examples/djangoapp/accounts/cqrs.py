from .entities import User
from django.contrib.auth.hashers import make_password
from django.http import Http404
from ses.app import EventSourcingApplication
from ses.exceptions import SesError
from ses.contrib.django.shortcuts import get_entity_or_404


class WrongPassword(SesError):
    pass


class AccountsApp(EventSourcingApplication):
    WrongPassword = WrongPassword

    def __init__(self):
        super().__init__()
        self.repo = self.get_repo_for_entity(User)

    def register(self, email, password):
        uuid = self.gen_uuid()
        self.storage.book_unique('user', email, entity_id=uuid)
        return self.repo.store('User.Registered', uuid, data={
            'email': email,
            'encoded_password': make_password(password),
            'activation_token': self.gen_uuid(),
        })

    def activate_with_token(self, user_id, token):
        user = get_entity_or_404(self.repo, user_id)
        assert not user.is_active
        assert user.activation_token == token
        return self.repo.store('User.ActivatedWithToken', user_id)

    def activate(self, user_id):
        user = get_entity_or_404(self.repo, user_id)
        assert not user.is_active
        return self.repo.store('User.Activated', user_id)

    def inactivate(self, user_id):
        user = get_entity_or_404(self.repo, user_id)
        assert user.is_active
        return self.repo.store('User.Inactivated', user_id)

    def obtain_auth_token(self, user_id):
        user = get_entity_or_404(self.repo, user_id)
        auth_token = self.gen_uuid()
        self.storage.book_unique('user_token', auth_token, entity_id=user_id)
        assert user.is_active is True, "User %s is inactive" % user.email
        return self.repo.store('User.ObtainedAuthToken', user.id, data={'auth_token': auth_token})

    def get_by_email(self, email):
        entity_id = self.storage.get_unique('user', email)
        if not entity_id:
            raise self.repo.DoesNotExist
        return self.repo.get_entity(entity_id)

    def get_by_email_or_404(self, email):
        try:
            return self.get_by_email(email)
        except self.repo.DoesNotExist:
            raise Http404

    def get_user_by_token(self, token):
        user_id = self.storage.get_unique('user_token', token)
        if user_id is None:
            return None
        else:
            return self.repo.get_entity(user_id)


app = AccountsApp()