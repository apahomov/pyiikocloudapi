from typing import List, Union

import httpx

from pyiikocloudapi.async_base import AsyncBaseAPI
from pyiikocloudapi.exception import ParamSetException, TokenException
from pyiikocloudapi.models import (
    BaseDeliveryRestrictionsModel,
    CustomErrorModel,
    DeliveryRestrictionsAllowedModel,
)


class AsyncDeliveryRestrictions(AsyncBaseAPI):
    async def delivery_restrictions(
        self, organization_ids: List[str], timeout=AsyncBaseAPI.DEFAULT_TIMEOUT
    ) -> Union[CustomErrorModel, BaseDeliveryRestrictionsModel]:
        if not bool(organization_ids):
            raise ParamSetException(
                self.__class__.__qualname__, self.delivery_restrictions.__name__, "Пустой список id организаций"
            )
        data = {
            "organizationIds": organization_ids,
        }

        try:
            return await self._post_request(
                url="/api/1/delivery_restrictions",
                data=data,
                timeout=timeout,
                model_response_data=BaseDeliveryRestrictionsModel,
            )
        except httpx.HTTPError as err:
            raise TokenException(
                self.__class__.__qualname__,
                self.delivery_restrictions.__name__,
                f"Не удалось получить список ограничений доставки: \n{err}",
            )
        except TypeError as err:
            raise TypeError(
                self.__class__.__qualname__,
                self.delivery_restrictions.__name__,
                f"Не удалось получить список ограничений доставки: \n{err}",
            )

    async def dr_allowed(
        self,
        organization_ids: List[str],
        is_courier_delivery: bool,
        delivery_address: dict = None,
        order_location: dict = None,
        order_items: dict = None,
        delivery_date: str = None,
        delivery_sum: float = None,
        discount_sum: float = None,
        timeout=AsyncBaseAPI.DEFAULT_TIMEOUT,
    ) -> Union[CustomErrorModel, DeliveryRestrictionsAllowedModel]:
        """
        Get suitable terminal groups for delivery restrictions.
        :param organization_ids:
        :param is_courier_delivery:
        :param delivery_address:
        :param order_location:
        :param order_items:
        :param delivery_date:
        :param delivery_sum:
        :param discount_sum:
        :param timeout:
        :return:
        """
        if not bool(organization_ids):
            raise ParamSetException(
                self.__class__.__qualname__, self.dr_allowed.__name__, "Пустой список id организаций"
            )
        data = {
            "organizationIds": organization_ids,
            "isCourierDelivery": is_courier_delivery,
        }
        if delivery_address is not None:
            data["deliveryAddress"] = delivery_address
        if order_location is not None:
            data["orderLocation"] = order_location
        if order_items is not None:
            data["orderItems"] = order_items
        if delivery_date is not None:
            data["deliveryDate"] = delivery_date
        if delivery_sum is not None:
            data["deliverySum"] = delivery_sum
        if discount_sum is not None:
            data["discountSum"] = discount_sum
        try:
            return await self._post_request(
                url="/api/1/delivery_restrictions/allowed",
                data=data,
                timeout=timeout,
                model_response_data=DeliveryRestrictionsAllowedModel,
            )
        except httpx.HTTPError as err:
            raise TokenException(
                self.__class__.__qualname__,
                self.dr_allowed.__name__,
                f"Не удалось получить подходящие группы терминалов для ограничения доставки: \n{err}",
            )
        except TypeError as err:
            raise TypeError(
                self.__class__.__qualname__,
                self.dr_allowed.__name__,
                f"Не удалось получить подходящие группы терминалов для ограничения доставки: \n{err}",
            )
