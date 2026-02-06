from typing import List, Optional, Union

import httpx

from pyiikocloudapi.base import BaseAPI
from pyiikocloudapi.exception import PostException, TokenException
from pyiikocloudapi.models import (
    BaseCreatedOrderInfoModel,
    ByIdModel,
    CustomErrorModel,
)


class Orders(BaseAPI):
    def order_create(
        self,
        organization_id: str,
        terminal_group_id: str,
        order: dict,
        create_order_settings: Optional[int] = None,
        timeout=BaseAPI.DEFAULT_TIMEOUT,
    ) -> Union[CustomErrorModel, BaseCreatedOrderInfoModel]:
        """"""

        data = {
            "organizationId": organization_id,
            # 'organizationId' instead of 'organizationIds'. 'errorDescription': "Required property 'organizationId' not found in JSON.
            "terminalGroupId": terminal_group_id,
            "order": order,
        }
        if create_order_settings is not None:
            data["createOrderSettings"] = create_order_settings

        try:
            return self._post_request(
                url="/api/1/order/create", data=data, model_response_data=BaseCreatedOrderInfoModel, timeout=timeout
            )
        except httpx.HTTPError as err:
            raise PostException(
                self.__class__.__qualname__, self.order_create.__name__, f"Не удалось создать заказ из за: \n{err}"
            )
        except TypeError as err:
            raise TypeError(
                self.__class__.__qualname__, self.order_create.__name__, f"Не удалось создать заказ из за: \n{err}"
            )

    def order_by_id(
        self,
        organization_ids: List[str],
        order_ids: List[str] = None,
        pos_order_ids: List[str] = None,
        return_external_data_keys: List[str] = None,
        source_keys: list = None,
        timeout=BaseAPI.DEFAULT_TIMEOUT,
    ) -> Union[CustomErrorModel, ByIdModel]:
        """
        Получить заказы по идентификаторам.

        :param organization_ids: Organization IDs
        :param order_ids: list
        :param pos_order_ids: list
        :param return_external_data_keys: list
        :param source_keys:
        :return:
        """
        # https://api-ru.iiko.services/api/1/deliveries/by_id

        data = {
            "organizationIds": organization_ids,
            "orderIds": order_ids,
        }
        if source_keys is not None:
            data["sourceKeys"] = source_keys

        if pos_order_ids is not None:
            data["posOrderIds"] = pos_order_ids

        if return_external_data_keys is not None:
            data["returnExternalDataKeys"] = return_external_data_keys

        try:
            return self._post_request(
                url="/api/1/order/by_id", data=data, model_response_data=ByIdModel, timeout=timeout
            )

        except httpx.HTTPError as err:
            raise TokenException(
                self.__class__.__qualname__, self.order_by_id.__name__, f"Не удалось получить заказы: \n{err}"
            )
        except TypeError as err:
            raise TokenException(self.__class__.__qualname__, self.order_by_id.__name__, f"Не удалось: \n{err}")

    def order_by_table(
        self,
        organization_ids: List[str],
        table_ids: List[str],
        source_keys: List[str] = None,
        statuses: List[str] = None,
        date_from: str = None,
        date_to: str = None,
        timeout=BaseAPI.DEFAULT_TIMEOUT,
    ) -> Union[CustomErrorModel, ByIdModel]:
        """

        :param organization_ids:
        :param table_ids:
        :param source_keys:
        :param statuses:
        :param date_from:
        :param date_to:
        :return:
        """
        # https://api-ru.iiko.services/api/1/deliveries/by_id
        if not isinstance(table_ids, list):
            raise TypeError("type table_ids != list")

        data = {
            "organizationIds": organization_ids,
            "tableIds": table_ids,
        }

        if source_keys is not None:
            if not isinstance(source_keys, list):
                raise TypeError("type source_keys != list")
            data["sourceKeys"] = source_keys

        if statuses is not None:
            if not isinstance(statuses, list):
                raise TypeError("type statuses != list")
            data["statuses"] = statuses

        if date_from is not None:
            if not isinstance(date_from, str):
                raise TypeError("type date_from != str")
            data["dateFrom"] = date_from

        if date_to is not None:
            if not isinstance(date_to, str):
                raise TypeError("type date_to != str")
            data["dateTo"] = date_to

        try:
            return self._post_request(
                url="/api/1/order/by_table", data=data, model_response_data=ByIdModel, timeout=timeout
            )

        except httpx.HTTPError as err:
            raise TokenException(
                self.__class__.__qualname__, self.order_by_table.__name__, f"Не удалось получить заказы: \n{err}"
            )
        except TypeError as err:
            raise TokenException(self.__class__.__qualname__, self.order_by_table.__name__, f"Не удалось: \n{err}")
