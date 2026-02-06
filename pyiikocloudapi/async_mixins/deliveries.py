import uuid
from datetime import datetime
from typing import List, Optional, Union

import httpx

from pyiikocloudapi.async_base import AsyncBaseAPI
from pyiikocloudapi.decorators import experimental
from pyiikocloudapi.exception import PostException, TokenException
from pyiikocloudapi.models import (
    BaseCreatedDeliveryOrderInfoModel,
    BaseResponseModel,
    ByDeliveryDateAndSourceKeyAndFilter,
    ByDeliveryDateAndStatusModel,
    CustomErrorModel,
)


class AsyncDeliveries(AsyncBaseAPI):
    async def delivery_create(
        self,
        organization_id: str,
        order: dict,
        terminal_group_id: str = None,
        create_order_settings: Optional[int] = None,
        timeout=AsyncBaseAPI.DEFAULT_TIMEOUT,
    ) -> Union[CustomErrorModel, BaseCreatedDeliveryOrderInfoModel]:
        """"""
        data = {
            "organizationId": organization_id,
            "order": order,
        }
        if terminal_group_id is not None:
            data["terminalGroupId"] = terminal_group_id

        if create_order_settings is not None:
            data["createOrderSettings"] = {"transportToFrontTimeout": create_order_settings}

        try:
            return await self._post_request(
                url="/api/1/deliveries/create",
                data=data,
                model_response_data=BaseCreatedDeliveryOrderInfoModel,
                timeout=timeout,
            )
        except httpx.HTTPError as err:
            raise PostException(
                self.__class__.__qualname__, self.delivery_create.__name__, f"Не удалось создать заказ из за: \n{err}"
            )
        except TypeError as err:
            raise TypeError(
                self.__class__.__qualname__, self.delivery_create.__name__, f"Не удалось создать заказ из за: \n{err}"
            )

    async def update_order_delivery_status(
        self,
        organization_id: str,
        order_id: str,
        delivery_status: str = "Delivered",
        delivery_date: datetime = None,
        timeout=AsyncBaseAPI.DEFAULT_TIMEOUT,
    ):
        """
        :param organization_id: Organization ID
        :param order_id: Order ID.
        :param delivery_status: Enum: "Waiting" "OnWay" "Delivered", Delivery status. Can be only switched between these three statuses.
        :param delivery_date: The date and time when the order was received by the guest (Local for delivery terminal). This field must be filled in only if the order is transferred to the "Delivered" status.

        :return:
        """
        if delivery_date is None:
            delivery_date = datetime.now()
        if not isinstance(delivery_date, datetime):
            raise TypeError("delivery_date != datetime")
        data = {
            "organizationId": organization_id,
            "orderId": order_id,
            "deliveryStatus": delivery_status,
        }
        if delivery_status == "Delivered":
            data["deliveryDate"] = delivery_date.strftime(self.strfdt)
        try:
            return await self._post_request(
                url="/api/1/deliveries/update_order_delivery_status",
                data=data,
                model_response_data=BaseResponseModel,
                timeout=timeout,
            )
        except httpx.HTTPError as err:
            raise TokenException(
                self.__class__.__qualname__,
                self.update_order_delivery_status.__name__,
                f"Не удалось изменить статус: \n{err}",
            )
        except TypeError as err:
            raise TokenException(
                self.__class__.__qualname__, self.update_order_delivery_status.__name__, f"Не удалось: \n{err}"
            )

    async def confirm(self, organization_id: List[str], order_id: str, timeout=AsyncBaseAPI.DEFAULT_TIMEOUT):
        """
        Подвердить статус доставки заказа

        :param organization_id: Organization ID
        :param order_id: Order ID.
        :return: dict response
        """
        data = {
            "organizationIds": organization_id,
            "orderId": order_id,
        }

        try:
            return await self._post_request(
                url="/api/1/deliveries/confirm", data=data, model_response_data=BaseResponseModel, timeout=timeout
            )

        except httpx.HTTPError as err:
            raise TokenException(
                self.__class__.__qualname__, self.confirm.__name__, f"Не удалось изменить статус: \n{err}"
            )
        except TypeError as err:
            raise TokenException(self.__class__.__qualname__, self.confirm.__name__, f"Не удалось: \n{err}")

    async def cancel_confirmation(
        self, organization_id: List[str], order_id: str, timeout=AsyncBaseAPI.DEFAULT_TIMEOUT
    ):
        """
        Отменить подтверждение доставки

        :param organization_id: Organization ID
        :param order_id: Order ID.
        :return: dict response
        """
        data = {
            "organizationIds": organization_id,
            "orderId": order_id,
        }

        try:
            return await self._post_request(
                url="/api/1/deliveries/cancel_confirmation",
                data=data,
                model_response_data=BaseResponseModel,
                timeout=timeout,
            )

        except httpx.HTTPError as err:
            raise TokenException(
                self.__class__.__qualname__, self.cancel_confirmation.__name__, f"Не удалось изменить статус: \n{err}"
            )
        except TypeError as err:
            raise TokenException(self.__class__.__qualname__, self.cancel_confirmation.__name__, f"Не удалось: \n{err}")

    async def by_delivery_date_and_status(
        self,
        organization_id: List[str],
        delivery_date_from: Union[datetime, str],
        delivery_date_to: Union[datetime, str] = None,
        statuses: list = None,
        source_keys: list = None,
        timeout=AsyncBaseAPI.DEFAULT_TIMEOUT,
    ) -> Union[ByDeliveryDateAndStatusModel, CustomErrorModel]:
        """


        :param organization_id:
        :param delivery_date_from: datetime or "%Y-%m-%d %H:%M:%S.%f". Order delivery date (Local for delivery terminal). Lower limit.
        :param delivery_date_to: datetime or "%Y-%m-%d %H:%M:%S.%f". Order delivery date (Local for delivery terminal). Upper limit.
        :param statuses: Items Enum: "Unconfirmed", "WaitCooking", "ReadyForCooking", "CookingStarted", "CookingCompleted", "Waiting", "OnWay", "Delivered", "Closed", "Cancelled",  Allowed order statuses.
        :param source_keys:Source keys.
        :return:
        """
        data = {
            "organizationIds": organization_id,
        }
        if isinstance(delivery_date_from, datetime):
            data["deliveryDateFrom"] = delivery_date_from.strftime(self.strfdt)
        elif isinstance(delivery_date_from, str):
            data["deliveryDateFrom"] = delivery_date_from

        if delivery_date_to is not None:
            if isinstance(delivery_date_to, datetime):
                data["deliveryDateTo"] = delivery_date_to.strftime(self.strfdt)
            elif isinstance(delivery_date_to, str):
                data["deliveryDateTo"] = delivery_date_to
            else:
                raise TypeError("type delivery_date_to != datetime or str")

        if statuses is not None:
            if not isinstance(statuses, list):
                raise TypeError("type statuses != list")
            data["statuses"] = statuses

        if source_keys is not None:
            if not isinstance(source_keys, list):
                raise TypeError("type source_keys != list")
            data["sourceKeys"] = source_keys

        try:
            return await self._post_request(
                url="/api/1/deliveries/by_delivery_date_and_status",
                data=data,
                model_response_data=ByDeliveryDateAndStatusModel,
                timeout=timeout,
            )

        except httpx.HTTPError as err:
            raise TokenException(
                self.__class__.__qualname__,
                self.by_delivery_date_and_status.__name__,
                f"Не удалось получить заказы: \n{err}",
            )
        except TypeError as err:
            raise TokenException(
                self.__class__.__qualname__, self.by_delivery_date_and_status.__name__, f"Не удалось: \n{err}"
            )

    @experimental("будет дописан в будущем!")
    async def by_revision(self, timeout=AsyncBaseAPI.DEFAULT_TIMEOUT):
        pass

    @experimental("будет дописан в будущем!")
    async def by_delivery_date_and_phone(self, timeout=AsyncBaseAPI.DEFAULT_TIMEOUT):
        pass

    async def by_delivery_date_and_source_key_and_filter(
        self,
        organization_id: List[str],
        terminal_group_ids: Optional[List[Union[str, uuid.UUID]]] = None,
        delivery_date_from: Optional[str] = None,
        delivery_date_to: Optional[str] = None,
        statuses: Optional[List[str]] = None,
        has_problem: Optional[bool] = None,
        order_service_type: Optional[str] = None,
        search_text: Optional[str] = None,
        time_to_cooking_error_timeout: Optional[int] = None,
        cooking_timeout: Optional[int] = None,
        sort_property: Optional[str] = None,
        sort_direction: Optional[str] = None,
        rows_count: Optional[int] = None,
        source_keys: Optional[List[str]] = None,
        order_ids: Optional[List[Union[str, uuid.UUID]]] = None,
        timeout=AsyncBaseAPI.DEFAULT_TIMEOUT,
    ) -> Union[ByDeliveryDateAndSourceKeyAndFilter, CustomErrorModel]:
        """

        :param organization_id: List
        :param terminal_group_ids: List of terminal groups IDs.
        :param delivery_date_from: Order delivery date (Local for delivery terminal). Lower limit.
        :param delivery_date_to: Order delivery date (Local for delivery terminal). Upper limit.
        :param statuses: Enum: "Unconfirmed" "WaitCooking" "ReadyForCooking" "CookingStarted" "CookingCompleted" "Waiting" "OnWay" "Delivered" "Closed" "Cancelled", Array of strings (iikoTransport.PublicApi.Contracts.Deliveries.Common.DeliveryStatus) Nullable
        :param has_problem: If true, delivery has a problem
        :param order_service_type: Order service type. Enum: "DeliveryByCourier" "DeliveryByClient"
        :param search_text: Value for search. Used for prefix search.
        :param time_to_cooking_error_timeout: Error timeout for status time to cooking, in seconds.
        :param cooking_timeout: Expected cooking time, in seconds.
        :param sort_property:  Enum: ("Number", "CompleteBefore", "Sum", "Customer", "Courier", "Status"),  Sorting property.
        :param sort_direction: Enum: ("Ascending", "Descending"),  Sorting direction.
        :param rows_count: Maximum number of items returned.
        :param source_keys: Source keys.
        :param order_ids: Order IDs
        :return:
        """

        data = {
            "organizationIds": organization_id,
        }

        if terminal_group_ids is not None:
            if not isinstance(terminal_group_ids, list):
                raise TypeError("type terminal_group_ids != list")
            data["terminalGroupIds"] = terminal_group_ids

        if delivery_date_from is not None:
            if not isinstance(delivery_date_from, str):
                raise TypeError("type delivery_date_from != str")
            data["deliveryDateFrom"] = delivery_date_from

        if delivery_date_to is not None:
            if not isinstance(delivery_date_to, str):
                raise TypeError("type delivery_date_to != str")
            data["deliveryDateTo"] = delivery_date_to

        if statuses is not None:
            if not isinstance(statuses, list):
                raise TypeError("type statuses != list")
            data["statuses"] = statuses

        if has_problem is not None:
            if not isinstance(has_problem, bool):
                raise TypeError("type has_problem != list")
            data["hasProblem"] = has_problem

        if order_service_type is not None:
            if not isinstance(order_service_type, str):
                raise TypeError("type order_service_type != str")
            data["orderServiceType"] = order_service_type

        if search_text is not None:
            if not isinstance(search_text, str):
                raise TypeError("type search_text != str")
            data["searchText"] = search_text

        if time_to_cooking_error_timeout is not None:
            if not isinstance(time_to_cooking_error_timeout, int):
                raise TypeError("type time_to_cooking_error_timeout != int")
            data["timeToCookingErrorTimeout"] = time_to_cooking_error_timeout

        if cooking_timeout is not None:
            if not isinstance(cooking_timeout, int):
                raise TypeError("type cooking_timeout != int")
            data["cookingTimeout"] = cooking_timeout

        if sort_property is not None:
            if not isinstance(sort_property, str):
                raise TypeError("type sort_property != str")
            data["sortProperty"] = sort_property

        if sort_direction is not None:
            if not isinstance(sort_direction, str):
                raise TypeError("type sort_direction != str")
            data["sortDirection"] = sort_direction

        if rows_count is not None:
            if not isinstance(rows_count, int):
                raise TypeError("type rows_count != int")
            data["rowsCount"] = rows_count

        if source_keys is not None:
            if not isinstance(source_keys, list):
                raise TypeError("type source_keys != list")
            data["sourceKeys"] = source_keys

        if order_ids is not None:
            if not isinstance(order_ids, list):
                raise TypeError("type order_ids != list")
            data["orderIds"] = order_ids

        try:
            return await self._post_request(
                url="/api/1/deliveries/by_delivery_date_and_source_key_and_filter",
                data=data,
                model_response_data=ByDeliveryDateAndSourceKeyAndFilter,
                timeout=timeout,
            )

        except httpx.HTTPError as err:
            raise TokenException(
                self.__class__.__qualname__,
                self.by_delivery_date_and_source_key_and_filter.__name__,
                f"Не удалось получить заказы: \n{err}",
            )
        except TypeError as err:
            raise TokenException(
                self.__class__.__qualname__,
                self.by_delivery_date_and_source_key_and_filter.__name__,
                f"Не удалось: \n{err}",
            )
