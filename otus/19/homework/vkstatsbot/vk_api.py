import logging
import requests


logger = logging.getLogger(__name__)


def encoded_dict(in_dict):
    out_dict = {}
    for k, v in in_dict.items():
        # if isinstance(v, unicode):
        #     v = v.encode('utf8')
        # if isinstance(v, str):
        #     v.decode('utf8')
        out_dict[k] = v
    return out_dict


class VKApiConnector(object):
    __base_url = "https://api.vk.com/method/"
    __v = 5.68
    __resolve_screen_name_method = "utils.resolveScreenName"
    __wall_get_method = "wall.get"
    __user_get_info = "users.get"
    __user_get_friends_list = "friends.get"
    __token = NotImplemented
    __client_id = NotImplemented
    __sleep_time = NotImplemented

    @classmethod
    def config(cls, version, client_id, token, sleep_time=1):
        cls.version = version
        cls.__sleep_time = sleep_time
        cls.__client_id = client_id
        cls.__token = token

    @classmethod
    def __get_base_params(cls):
        return {
            'v': cls.__v,
            'client_id': cls.__client_id,
            'access_token': cls.__token
        }

    @classmethod
    def resolve_screen_name(cls, screen_name):
        try:
            logger.info("Access {} method".format(cls.__resolve_screen_name_method))
            request_params = cls.__get_base_params()
            request_params['screen_name'] = screen_name

            url = '{}{}'.format(cls.__base_url, cls.__resolve_screen_name_method)
            response = requests.post(url, encoded_dict(request_params) if request_params else None)

            if not response.ok:
                logger.error(response.text)
                return

            return response.json()['response']
        except Exception as ex:
            logger.exception(ex)

    @classmethod
    def get_wall(cls, owner_id):
        try:
            logger.info("Access {} method".format(cls.__wall_get_method))
            request_params = cls.__get_base_params()
            request_params['owner_id'] = owner_id
            request_params['count'] = 100
            request_params['filter'] = 'owner'

            url = '{}{}'.format(cls.__base_url, cls.__wall_get_method)
            response = requests.post(url, encoded_dict(request_params) if request_params else None)
            print(response)
            return response


            if not response.ok:
                logger.error(response.text)
                return
            if 'response' in response.json().keys():
                return response.json()['response']
            else:
                return

        except Exception as ex:
            logger.exception(ex)



    @classmethod
    def get_user_info(cls, owner_ids):
        try:
            logger.info("Access {} method".format(cls.__user_get_info))
            request_params = cls.__get_base_params()
            request_params['user_ids'] = owner_ids
            request_params['fields'] = 'sex'

            url = '{}{}'.format(cls.__base_url, cls.__user_get_info)
            response = requests.post(url, encoded_dict(request_params) if request_params else None)
            if not response.ok:
                logger.error(response.text)
                return

        except Exception as ex:
            logger.exception(ex)

    @classmethod
    def get_user_friends_list(cls, owner_id):
        try:
            logger.info("Access {} method".format(cls.__user_get_friends_list))
            request_params = cls.__get_base_params()
            request_params['user_id'] = owner_id

            url = '{}{}'.format(cls.__base_url, cls.__user_get_friends_list)
            response = requests.post(url, encoded_dict(request_params) if request_params else None)

            if not response.ok:
                logger.error(response.text)
                return
            if 'error' in response.json().keys():
                return 
            else:
                return response.json()['response']

        except Exception as ex:
            logger.exception(ex)




