from typing import List, Union

import httpx

from pyiikocloudapi.base import BaseAPI
from pyiikocloudapi.exception import ParamSetException, TokenException
from pyiikocloudapi.models import (
    BaseCitiesModel,
    BaseRegionsModel,
    BaseStreetByCityModel,
    CustomErrorModel,
)


class Address(BaseAPI):
    def regions(
        self, organization_ids: List[str], timeout=BaseAPI.DEFAULT_TIMEOUT
    ) -> Union[CustomErrorModel, BaseRegionsModel]:
        """
        Возвращает регионы, доступные пользователю API-login.
        :return:
        """
        #         https://api-ru.iiko.services/api/1/organizations
        if not bool(organization_ids):
            raise ParamSetException(self.__class__.__qualname__, self.regions.__name__, "Пустой список id организаций")

        data = {
            "organizationIds": organization_ids,
        }
        try:
            return self._post_request(
                url="/api/1/regions", data=data, model_response_data=BaseRegionsModel, timeout=timeout
            )
        except httpx.HTTPError as err:
            raise TokenException(
                self.__class__.__qualname__, self.regions.__name__, f"Не удалось получить регионы: \n{err}"
            )
        except TypeError as err:
            raise TypeError(self.__class__.__qualname__, self.regions.__name__, f"Не удалось получить регионы: \n{err}")

    def cities(
        self, organization_ids: List[str], timeout=BaseAPI.DEFAULT_TIMEOUT
    ) -> Union[CustomErrorModel, BaseCitiesModel]:
        """
        Возвращает регионы, доступные пользователю API-login.
        :return:
        """
        #         https://api-ru.iiko.services/api/1/organizations
        if not bool(organization_ids):
            raise ParamSetException(self.__class__.__qualname__, self.cities.__name__, "Пустой список id организаций")

        data = {
            "organizationIds": organization_ids,
        }
        try:
            return self._post_request(
                url="/api/1/cities", data=data, model_response_data=BaseCitiesModel, timeout=timeout
            )

        except httpx.HTTPError as err:
            raise TokenException(
                self.__class__.__qualname__, self.cities.__name__, f"Не удалось получить города: \n{err}"
            )
        except TypeError as err:
            raise TypeError(self.__class__.__qualname__, self.cities.__name__, f"Не удалось получить города: \n{err}")

    def by_city(
        self, organization_id: str, city_id: str, timeout=BaseAPI.DEFAULT_TIMEOUT
    ) -> Union[CustomErrorModel, BaseStreetByCityModel]:
        """
        Возвращает регионы, доступные пользователю API-login.
        :return:
        """
        #         https://api-ru.iiko.services/api/1/organizations

        data = {"organizationId": organization_id, "cityId": city_id}
        try:
            return self._post_request(
                url="/api/1/streets/by_city", data=data, model_response_data=BaseStreetByCityModel, timeout=timeout
            )

        except httpx.HTTPError as err:
            raise TokenException(
                self.__class__.__qualname__, self.by_city.__name__, f"Не удалось получить улицы: \n{err}"
            )
        except TypeError as err:
            raise TypeError(self.__class__.__qualname__, self.by_city.__name__, f"Не удалось получить улицы: \n{err}")
