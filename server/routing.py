import bcrypt
from flask_jwt_extended import create_access_token

from server.resources.base import BaseResource
from server.schemas import (
    ResourceSchema,
    RegisterSchema,
    AuthSchema,
    UserInfoSchema,
    UserListSchema,
    UserSocialTokensSchema,
)

from server.resources.utils import (
    provide_db_session,
    schematic_response,
    schematic_request,
    with_user_id,
    authorized,
)

from server.database.managers import (
    SensorManager,
    ObjectManager,
    ControllerManager,
    UserManager,
    UserInfoManager,
    UserSocialTokensManager,
)

from server.validation.schema import (
    RegisterRequestSchema,
    AuthRequestSchema,
    UserInfoRequestSchema,
)

from server.errors import InvalidArgumentError


class Registration(BaseResource):
    @provide_db_session
    @schematic_request(RegisterRequestSchema())
    @schematic_response(RegisterSchema())
    def post(self, request_obj=None):
        login = request_obj['login']
        pwd = request_obj['password'].encode('utf-8')

        pwd_hash = bcrypt.hashpw(pwd, bcrypt.gensalt()).decode('utf-8')

        user = UserManager(self.db_session).save_new(login, pwd_hash)

        return {'token': create_access_token(identity={'email': login, 'id': user.id})}, 201


class Auth(BaseResource):
    @provide_db_session
    @schematic_request(AuthRequestSchema())
    @schematic_response(AuthSchema())
    def post(self, request_obj=None):
        login = request_obj['login']
        pwd = request_obj['password'].encode('utf-8')

        user = UserManager(self.db_session).get_by_login(login)

        if bcrypt.checkpw(pwd, user.pwd_hash.encode('utf-8')):
            return {'token': create_access_token(identity={'email': login, 'id': user.id})}

        raise InvalidArgumentError(message='invalid password')


class User(BaseResource):
    @authorized
    @provide_db_session
    @schematic_response(UserInfoSchema())
    @with_user_id()
    def get(self, user_id=None):
        return UserInfoManager(self.db_session).get_by_user_id(user_id)

    @authorized
    @provide_db_session
    @schematic_request(UserInfoRequestSchema())
    @schematic_response(UserInfoSchema())
    @with_user_id(True)
    def patch(self, user_id=None, request_obj=None):
        return UserInfoManager(self.db_session).update(user_id, request_obj)


class UserTokens(BaseResource):
    @authorized
    @provide_db_session
    @schematic_response(UserSocialTokensSchema())
    @with_user_id()
    def get(self, user_id=None):
        return UserSocialTokensManager(self.db_session).get_by_user_id(user_id)

    @authorized
    @provide_db_session
    @schematic_request(UserSocialTokensSchema())
    @schematic_response(UserSocialTokensSchema())
    @with_user_id(True)
    def patch(self, user_id=None, request_obj=None):
        return UserSocialTokensManager(self.db_session).update(user_id, request_obj)


class Users(BaseResource):
    @provide_db_session
    @schematic_response(UserListSchema())
    def get(self):
        return {'users': UserInfoManager(self.db_session).get_all(True)}


class ObjectsResource(BaseResource):
    @authorized
    @provide_db_session
    @schematic_response(ResourceSchema())
    def get(self):
        sensors = SensorManager(self.db_session).get_all()
        objects = ObjectManager(self.db_session).get_all()
        controllers = ControllerManager(self.db_session).get_all()

        return {
            'objects': objects,
            'controllers': controllers,
            'sensors': sensors,
        }


class AllObjectsInfoResource(BaseResource):
    @authorized
    @provide_db_session
    @schematic_response(ResourceSchema())
    def get(self):
        objects = ObjectManager(self.db_session).get_all()
        sensors = SensorManager(self.db_session).get_all()
        controllers = ControllerManager(self.db_session).get_all()

        return {
            'objects': objects,
            'sensors': sensors,
            'controllers': controllers
        }


def register_routes(app):
    app.register_route(Auth, 'sign_in', '/sign_in')
    app.register_route(Registration, 'sign_up', '/sign_up')
    app.register_route(ObjectsResource, 'objects', '/objects')
    app.register_route(User, 'user_info_self', '/user/info')
    app.register_route(Users, 'users_list', '/user/list')
    app.register_route(UserTokens, 'user_social_tokens', '/user_social_tokens')
