import json
import logging
from datetime import date, datetime, timedelta
from typing import List, Optional, Union

import httpx

from pyiikocloudapi._http import process_response
from pyiikocloudapi.exception import CheckTimeToken, SetSession, TokenException
from pyiikocloudapi.models import (
    BaseOrganizationsModel,
    CustomErrorModel,
    OrganizationModel,
)


class AsyncBaseAPI:
    DEFAULT_TIMEOUT = "15"

    def __init__(
        self,
        api_login: str,
        session: Optional[httpx.AsyncClient] = None,
        debug: bool = False,
        base_url: str = None,
        working_token: str = None,
        base_headers: dict = None,
        logger: Optional[logging.Logger] = None,
        return_dict: bool = False,
        *args,
        **kwargs,
    ):
        """

        :param api_login: login api iiko cloud
        :param session: session object (httpx.AsyncClient)
        :param debug: logging dict response
        :param base_url: url iiko cloud api
        :param working_token: Initialize an object based on a working token, that is, without requesting a new one
        :param base_headers: base header for request in iiko cloud api
        :param logger: your object Logger
        :param return_dict: return a dictionary instead of models
        """

        if session is not None:
            self.__session = session
        else:
            self.__session = httpx.AsyncClient()

        self.__api_login = api_login
        self.__token: Optional[str] = None
        self.__debug = debug
        self.__time_token: Optional[date] = None
        self.__organizations_ids_model: Optional[BaseOrganizationsModel] = None
        self.__organizations_ids: Optional[List[str]] = None
        self.__strfdt = "%Y-%m-%d %H:%M:%S.000"
        self.__return_dict = return_dict
        self.logger = logger if logger is not None else logging.getLogger()

        self.__base_url = "https://api-ru.iiko.services" if base_url is None else base_url
        self.__headers = (
            {
                "Content-Type": "application/json",
                "Timeout": "45",
            }
            if base_headers is None
            else base_headers
        )

        self.__token_initialized = False
        if working_token is not None:
            self.__set_token(working_token)
            self.__token_initialized = True

        self.__last_data = None

    async def ensure_token(self):
        """Lazy token initialization. Call before first request."""
        if not self.__token_initialized:
            await self._async_get_access_token()
            self.__token_initialized = True

    def check_status_code_token(self, code: Union[str, int]):
        # NOTE: This method is intentionally a no-op. Kept for backward compatibility.
        # Status code handling is done by the retry loop in _post_request.
        if str(code) == "401" or str(code) == "400" or str(code) == "408" or str(code) == "500":
            pass

    async def check_token_time(self) -> bool:
        """
        Проверка на время жизни маркера доступа
        :return: Если прошло 15 мин будет запрошен токен и метод вернёт True, иначе вернётся False
        """
        fifteen_minutes_ago = datetime.now() - timedelta(minutes=15)
        time_token = self.__time_token
        try:
            if time_token <= fifteen_minutes_ago:
                await self._async_get_access_token()
                return True
            else:
                return False
        except TypeError:
            raise CheckTimeToken(
                self.__class__.__qualname__,
                self.check_token_time.__name__,
                "Не запрошен Token и не присвоен объект типа datetime.datetime",
            )

    @property
    def organizations_ids_models(self) -> Optional[List[OrganizationModel]]:
        return self.__organizations_ids_model

    @property
    def organizations_ids(self) -> Optional[List[str]]:
        return self.__organizations_ids

    @property
    def last_data(self) -> Optional[List[str]]:
        return self.__last_data

    @property
    def session_s(self) -> httpx.AsyncClient:
        """Вывести сессию"""
        return self.__session

    @session_s.setter
    def session_s(self, session: httpx.AsyncClient = None):
        """Изменение сессии"""
        if session is None:
            raise SetSession(
                self.__class__.__qualname__, self.session_s.__name__, "Не присвоен объект типа httpx.AsyncClient"
            )
        else:
            self.__session = session

    @property
    def time_token(self):
        return self.__time_token

    @property
    def api_login(self) -> str:
        return self.__api_login

    @property
    def token(self) -> str:
        return self.__token

    @property
    def base_url(self):
        return self.__base_url

    @base_url.setter
    def base_url(self, value: str):
        self.__base_url = value

    @property
    def strfdt(self):
        return self.__strfdt

    @strfdt.setter
    def strfdt(self, value: str):
        self.__strfdt = value

    @property
    def headers(self):
        return self.__headers

    @headers.setter
    def headers(self, value: str):
        self.__headers = value

    @property
    def return_dict(self):
        return self.__return_dict

    @return_dict.setter
    def return_dict(self, value: bool):
        self.__return_dict = value

    @property
    def timeout(self):
        return self.__headers.get("Timeout")

    @timeout.setter
    def timeout(self, value: int):
        self.__headers.update({"Timeout": str(value)})

    @timeout.deleter
    def timeout(self):
        self.__headers.update({"Timeout": str(self.DEFAULT_TIMEOUT)})

    def __set_token(self, token):
        self.__token = token
        self.__headers["Authorization"] = f"Bearer {self.token}"
        self.__time_token = datetime.now()

    async def access_token(self):
        """Получить маркер доступа"""
        data = json.dumps({"apiLogin": self.api_login})
        try:
            result = await self.session_s.post(
                f"{self.__base_url}/api/1/access_token",
                content=data,
                headers={"Content-Type": "application/json"},
                timeout=float(self.DEFAULT_TIMEOUT),
            )

            response_data: dict = json.loads(result.content)
            if response_data.get("errorDescription") is not None:
                raise TypeError(f"{response_data=}")

            if response_data.get("token") is not None:
                self.__set_token(response_data.get("token", ""))
            else:
                raise TokenException(
                    self.__class__.__qualname__, self.access_token.__name__, f"No token in response: {response_data}"
                )

        except httpx.HTTPError as err:
            raise TokenException(
                self.__class__.__qualname__, self.access_token.__name__, f"Не удалось получить маркер доступа: \n{err}"
            )
        except TypeError as err:
            raise TokenException(
                self.__class__.__qualname__, self.access_token.__name__, f"Не удалось получить маркер доступа: \n{err}"
            )

    async def _post_request(
        self,
        url: str,
        data: dict = None,
        timeout=DEFAULT_TIMEOUT,
        model_response_data=None,
        model_error=CustomErrorModel,
    ):
        await self.ensure_token()
        if data is None:
            data = {}
        if timeout != self.DEFAULT_TIMEOUT:
            self.timeout = timeout
        self.logger.info(f"{url=}, {data=}, {model_response_data=}, {model_error=}")

        try:
            for attempt in range(2):
                response = await self.session_s.post(
                    f"{self.base_url}{url}", content=json.dumps(data), headers=self.headers, timeout=float(timeout)
                )
                if response.status_code == 401 and attempt == 0:
                    await self._async_get_access_token()
                    continue

                if self.__debug:
                    try:
                        self.logger.debug(
                            f"Входные данные:\n{response.request.url=}\n{response.request.content=}\n{response.request.headers=}\n\nВыходные данные:\n{response.headers=}\n{response.content=}\n\n"
                        )
                    except Exception as err:
                        self.logger.debug(f"{err=}")

                response_data = process_response(
                    response_content=response.content,
                    response_status_code=response.status_code,
                    return_dict=self.__return_dict,
                    model_response_data=model_response_data,
                    model_error=model_error,
                )
                self.__last_data = response_data
                return response_data
        finally:
            if timeout != self.DEFAULT_TIMEOUT:
                del self.timeout

    async def _async_get_access_token(self):
        out = await self.access_token()
        if isinstance(out, CustomErrorModel):
            raise TokenException(
                self.__class__.__qualname__, self.access_token.__name__, f"Не удалось получить маркер доступа: \n{out}"
            )

    def __convert_org_data(self, data: BaseOrganizationsModel):
        self.__organizations_ids = data.__list_id__()

    async def organizations(
        self,
        organization_ids: List[str] = None,
        return_additional_info: bool = None,
        include_disabled: bool = None,
        timeout=DEFAULT_TIMEOUT,
    ) -> Union[CustomErrorModel, BaseOrganizationsModel]:
        """
        Возвращает организации, доступные пользователю API-login.
        :param organization_ids: Organizations IDs which have to be returned. By default - all organizations from apiLogin.
        :param return_additional_info: A sign whether additional information about the organization should be returned (RMS version, country, restaurantAddress, etc.), or only minimal information should be returned (id and name).
        :param include_disabled: Attribute that shows that response contains disabled organizations.
        :return:
        """
        data = {}
        if organization_ids is not None:
            data["organizationIds"] = organization_ids
        if return_additional_info is not None:
            data["returnAdditionalInfo"] = return_additional_info
        if include_disabled is not None:
            data["includeDisabled"] = include_disabled
        try:
            response_data = await self._post_request(
                url="/api/1/organizations", data=data, model_response_data=BaseOrganizationsModel, timeout=timeout
            )
            if isinstance(response_data, BaseOrganizationsModel):
                self.__convert_org_data(data=response_data)
            if self.return_dict:
                self.__organizations_ids = [org.get("id") for org in response_data.get("organizations", [])]
            return response_data

        except httpx.HTTPError as err:
            raise TokenException(
                self.__class__.__qualname__, self.organizations.__name__, f"Не удалось получить организации: \n{err}"
            )
        except TypeError as err:
            raise TypeError(
                self.__class__.__qualname__, self.organizations.__name__, f"Не удалось получить организации: \n{err}"
            )

    async def close(self):
        await self.session_s.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self.close()
