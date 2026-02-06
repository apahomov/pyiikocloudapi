from typing import List, Union

import httpx

from pyiikocloudapi.base import BaseAPI
from pyiikocloudapi.exception import TokenException
from pyiikocloudapi.models import (
    BaseComboCalculateModel,
    BaseComboModel,
    BaseMenuByIdModel,
    BaseMenuModel,
    BaseNomenclatureModel,
    CheckStopListsResponse,
    CustomErrorModel,
    StopListsResponse,
)


class Menu(BaseAPI):
    def nomenclature(
        self, organization_id: str, start_revision: int = None, timeout=BaseAPI.DEFAULT_TIMEOUT
    ) -> Union[CustomErrorModel, BaseNomenclatureModel]:
        data = {
            "organizationId": organization_id,
        }
        if start_revision is not None:
            data["startRevision"] = start_revision

        try:
            return self._post_request(
                url="/api/1/nomenclature", data=data, model_response_data=BaseNomenclatureModel, timeout=timeout
            )
        except httpx.HTTPError as err:
            raise TokenException(
                self.__class__.__qualname__, self.nomenclature.__name__, f"Не удалось получить номенклатуру: \n{err}"
            )
        except TypeError as err:
            raise TypeError(
                self.__class__.__qualname__, self.nomenclature.__name__, f"Не удалось получить номенклатуру: \n{err}"
            )

    def menu(self, timeout=BaseAPI.DEFAULT_TIMEOUT) -> Union[CustomErrorModel, BaseMenuModel]:
        try:
            return self._post_request(url="/api/2/menu", model_response_data=BaseMenuModel, timeout=timeout)
        except httpx.HTTPError as err:
            raise TokenException(
                self.__class__.__qualname__,
                self.menu.__name__,
                f"Не удалось получить внешние меню с ценовыми категориями: \n{err}",
            )
        except TypeError as err:
            raise TypeError(
                self.__class__.__qualname__,
                self.menu.__name__,
                f"Не удалось получить внешние меню с ценовыми категориями: \n{err}",
            )

    def menu_by_id(
        self,
        external_menu_id: str,
        organization_ids: List[str],
        price_category_id: str = None,
        timeout=BaseAPI.DEFAULT_TIMEOUT,
    ) -> Union[CustomErrorModel, BaseMenuByIdModel]:

        data = {
            "externalMenuId": external_menu_id,
            "organizationIds": organization_ids,
        }

        if price_category_id is not None:
            data["priceCategoryId"] = price_category_id

        try:
            return self._post_request(
                url="/api/2/menu/by_id", data=data, model_response_data=BaseMenuByIdModel, timeout=timeout
            )
        except httpx.HTTPError as err:
            raise TokenException(
                self.__class__.__qualname__,
                self.menu_by_id.__name__,
                f"Не удалось получить внешнее меню по ID.: \n{err}",
            )
        except TypeError as err:
            raise TypeError(
                self.__class__.__qualname__,
                self.menu_by_id.__name__,
                f"Не удалось получить внешнее меню по ID.: \n{err}",
            )

    def stop_lists(
        self,
        organization_ids: List[str],
        return_size: bool = False,
        terminal_groups_ids: List[str] = None,
        timeout=BaseAPI.DEFAULT_TIMEOUT,
    ) -> Union[CustomErrorModel, StopListsResponse]:

        data = {
            "organizationIds": organization_ids,
            "returnSize": return_size,
        }

        if terminal_groups_ids is not None:
            data["terminalGroupsIds"] = terminal_groups_ids

        try:
            return self._post_request(
                url="/api/1/stop_lists", data=data, model_response_data=StopListsResponse, timeout=timeout
            )
        except httpx.HTTPError as err:
            raise TokenException(
                self.__class__.__qualname__,
                self.stop_lists.__name__,
                f"Не удалось получить товары, которых нет в наличии: \n{err}",
            )
        except TypeError as err:
            raise TypeError(
                self.__class__.__qualname__,
                self.stop_lists.__name__,
                f"Не удалось получить товары, которых нет в наличии: \n{err}",
            )

    def stop_lists_check(
        self, organization_id: str, terminal_group_id: str, items: dict, timeout=BaseAPI.DEFAULT_TIMEOUT
    ) -> Union[CustomErrorModel, CheckStopListsResponse]:
        """"""

        data = {"organizationId": organization_id, "terminalGroupId": terminal_group_id, "items": items}

        try:
            return self._post_request(
                url="/api/1/stop_lists/check", data=data, model_response_data=CheckStopListsResponse, timeout=timeout
            )
        except httpx.HTTPError as err:
            raise TokenException(
                self.__class__.__qualname__,
                self.stop_lists_check.__name__,
                f"Не удалось проверить товары в списке отсутствующих на складе.: \n{err}",
            )
        except TypeError as err:
            raise TypeError(
                self.__class__.__qualname__,
                self.stop_lists_check.__name__,
                f"Не удалось проверить товары в списке отсутствующих на складе.: \n{err}",
            )

    def combo(self, organization_id: str, timeout=BaseAPI.DEFAULT_TIMEOUT) -> Union[CustomErrorModel, BaseComboModel]:

        data = {
            "organizationId": organization_id,
        }

        try:
            return self._post_request(
                url="/api/1/combo", data=data, model_response_data=BaseComboModel, timeout=timeout
            )
        except httpx.HTTPError as err:
            raise TokenException(
                self.__class__.__qualname__, self.combo.__name__, f"Не удалось получить комбо: \n{err}"
            )
        except TypeError as err:
            raise TypeError(self.__class__.__qualname__, self.combo.__name__, f"Не удалось получить комбо: \n{err}")

    def combo_calculate(
        self, organization_id: str, items: dict, timeout=BaseAPI.DEFAULT_TIMEOUT
    ) -> Union[CustomErrorModel, BaseComboCalculateModel]:

        data = {
            "items": items,
            "organizationId": organization_id,
        }

        try:
            return self._post_request(
                url="/api/1/combo/calculate", data=data, model_response_data=BaseComboCalculateModel, timeout=timeout
            )
        except httpx.HTTPError as err:
            raise TokenException(
                self.__class__.__qualname__, self.combo_calculate.__name__, f"Не удалось получить расчёт комбо: \n{err}"
            )
        except TypeError as err:
            raise TypeError(
                self.__class__.__qualname__, self.combo_calculate.__name__, f"Не удалось получить расчёт комбо: \n{err}"
            )
