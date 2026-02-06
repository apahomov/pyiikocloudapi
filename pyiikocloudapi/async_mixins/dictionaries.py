from typing import List, Union

import httpx

from pyiikocloudapi.async_base import AsyncBaseAPI
from pyiikocloudapi.exception import ParamSetException, TokenException
from pyiikocloudapi.models import (
    BaseCancelCausesModel,
    BaseDiscountsModel,
    BaseOrderTypesModel,
    BasePaymentTypesModel,
    BaseRemovalTypesModel,
    BaseTipsTypesModel,
    CustomErrorModel,
)


class AsyncDictionaries(AsyncBaseAPI):
    async def cancel_causes(
        self, organization_ids: List[str], timeout=AsyncBaseAPI.DEFAULT_TIMEOUT
    ) -> Union[CustomErrorModel, BaseCancelCausesModel]:
        if not bool(organization_ids):
            raise ParamSetException(
                self.__class__.__qualname__, self.cancel_causes.__name__, "Пустой список id организаций"
            )
        data = {
            "organizationIds": organization_ids,
        }
        try:
            return await self._post_request(
                url="/api/1/cancel_causes", data=data, model_response_data=BaseCancelCausesModel, timeout=timeout
            )
        except httpx.HTTPError as err:
            raise TokenException(
                self.__class__.__qualname__,
                self.cancel_causes.__name__,
                f"Не удалось получить причины отмены доставки: \n{err}",
            )
        except TypeError as err:
            raise TypeError(
                self.__class__.__qualname__,
                self.cancel_causes.__name__,
                f"Не удалось получить причины отмены доставки: \n{err}",
            )

    async def order_types(
        self, organization_ids: List[str], timeout=AsyncBaseAPI.DEFAULT_TIMEOUT
    ) -> Union[CustomErrorModel, BaseOrderTypesModel]:
        if not bool(organization_ids):
            raise ParamSetException(
                self.__class__.__qualname__, self.order_types.__name__, "Пустой список id организаций"
            )
        data = {
            "organizationIds": organization_ids,
        }
        try:
            return await self._post_request(
                url="/api/1/deliveries/order_types", data=data, model_response_data=BaseOrderTypesModel, timeout=timeout
            )
        except httpx.HTTPError as err:
            raise TokenException(
                self.__class__.__qualname__, self.order_types.__name__, f"Не удалось получить типы заказа: \n{err}"
            )
        except TypeError as err:
            raise TypeError(
                self.__class__.__qualname__, self.order_types.__name__, f"Не удалось получить типы заказа: \n{err}"
            )

    async def discounts(
        self, organization_ids: List[str], timeout=AsyncBaseAPI.DEFAULT_TIMEOUT
    ) -> Union[CustomErrorModel, BaseDiscountsModel]:
        if not bool(organization_ids):
            raise ParamSetException(
                self.__class__.__qualname__, self.discounts.__name__, "Пустой список id организаций"
            )
        data = {
            "organizationIds": organization_ids,
        }
        try:
            return await self._post_request(
                url="/api/1/discounts", data=data, model_response_data=BaseDiscountsModel, timeout=timeout
            )
        except httpx.HTTPError as err:
            raise TokenException(
                self.__class__.__qualname__, self.discounts.__name__, f"Не удалось получить скидки/надбавки: \n{err}"
            )
        except TypeError as err:
            raise TypeError(
                self.__class__.__qualname__, self.discounts.__name__, f"Не удалось получить скидки/надбавки: \n{err}"
            )

    async def payment_types(
        self, organization_ids: List[str], timeout=AsyncBaseAPI.DEFAULT_TIMEOUT
    ) -> Union[CustomErrorModel, BasePaymentTypesModel]:
        if not bool(organization_ids):
            raise ParamSetException(
                self.__class__.__qualname__, self.payment_types.__name__, "Пустой список id организаций"
            )
        data = {
            "organizationIds": organization_ids,
        }
        try:
            return await self._post_request(
                url="/api/1/payment_types", data=data, model_response_data=BasePaymentTypesModel, timeout=timeout
            )
        except httpx.HTTPError as err:
            raise TokenException(
                self.__class__.__qualname__, self.payment_types.__name__, f"Не удалось получить типы оплаты: \n{err}"
            )
        except TypeError as err:
            raise TypeError(
                self.__class__.__qualname__, self.payment_types.__name__, f"Не удалось получить типы оплаты: \n{err}"
            )

    async def removal_types(
        self, organization_ids: List[str], timeout=AsyncBaseAPI.DEFAULT_TIMEOUT
    ) -> Union[CustomErrorModel, BaseRemovalTypesModel]:
        if not bool(organization_ids):
            raise ParamSetException(
                self.__class__.__qualname__, self.removal_types.__name__, "Пустой список id организаций"
            )
        data = {
            "organizationIds": organization_ids,
        }
        try:
            return await self._post_request(
                url="/api/1/removal_types", data=data, model_response_data=BaseRemovalTypesModel, timeout=timeout
            )
        except httpx.HTTPError as err:
            raise TokenException(
                self.__class__.__qualname__, self.removal_types.__name__, f"Не удалось получить removal_types: \n{err}"
            )
        except TypeError as err:
            raise TypeError(
                self.__class__.__qualname__, self.removal_types.__name__, f"Не удалось получить removal_types: \n{err}"
            )

    async def tips_types(self, timeout=AsyncBaseAPI.DEFAULT_TIMEOUT) -> Union[CustomErrorModel, BaseTipsTypesModel]:
        try:
            return await self._post_request(
                url="/api/1/tips_types", model_response_data=BaseTipsTypesModel, timeout=timeout
            )
        except httpx.HTTPError as err:
            raise TokenException(
                self.__class__.__qualname__,
                self.tips_types.__name__,
                f"Не удалось получить подсказки для группы api-logins rms: \n{err}",
            )
        except TypeError as err:
            raise TypeError(
                self.__class__.__qualname__,
                self.tips_types.__name__,
                f"Не удалось получить подсказки для группы api-logins rms: \n{err}",
            )
