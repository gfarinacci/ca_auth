from django.core.exceptions import ObjectDoesNotExist

from identity.account.models import UserAccount
from auth.entities import Credential, CredentialInterface
from auth.usecases import CredentialRepositoryInterface


class DjangoCredentialRepository(CredentialRepositoryInterface):

    def find(self, uuid: 'UUID') -> Credential:
        user = self._find_user_account({'uuid': uuid})
        return self._factory_credential(user)

    def find_by(self, username: str) -> Credential:
        user = self._find_user_account({'username': username})
        return self._factory_credential(user)

    def create(self, credential: CredentialInterface) -> Credential:
        user = UserAccount(
            username=credential.username,
            email=credential.username,
            password=credential.password.value,
            uuid=credential.uuid
        )
        user.save()
        return self._factory_credential(user)

    def update_status(self, credential: CredentialInterface) -> Credential:
        user = self._find_user_account({'uuid': credential.uuid})
        user.is_active = credential.active
        user.save()

        return self._factory_credential(user)

    def update_password(self, credential: CredentialInterface) -> Credential:
        user = self._find_user_account({'uuid': credential.uuid})
        user.password = credential.password.value
        user.save()

        return self._factory_credential(user)

    def _factory_credential(self, user: UserAccount) -> Credential:
        if user:
            return Credential(
                user.username,
                user.password,
                uuid=user.uuid,
                active=user.is_active
            )

    def _find_user_account(self, params: dict) -> UserAccount:
        try:
            user = UserAccount.objects.get(**params)
        except ObjectDoesNotExist:
            return None
        else:
            return user
