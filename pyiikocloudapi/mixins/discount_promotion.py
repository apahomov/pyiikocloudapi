from typing import Union

import httpx

from pyiikocloudapi.base import BaseAPI
from pyiikocloudapi.exception import TokenException, ParamSetException
from pyiikocloudapi.models import (
    CustomErrorModel,
    SeriesWithNotActivatedCoupon,
    BaseCouponInfo,
)


class DiscountPromotion(BaseAPI):
    def coupons_series(self, organization_id: str) -> Union[
        CustomErrorModel, SeriesWithNotActivatedCoupon]:
        if not bool(organization_id):
            raise ParamSetException(self.__class__.__qualname__,
                                    self.coupons_series.__name__,
                                    f"Отсутствует аргумент id организации")
        data = {
            "organizationId": organization_id,
        }
        try:
            return self._post_request(
                url="/api/1/loyalty/iiko/coupons/series",
                data=data,
                model_response_data=SeriesWithNotActivatedCoupon,
            )
        except httpx.HTTPError as err:
            raise TokenException(self.__class__.__qualname__,
                                 self.coupons_series.__name__,
                                 f"Не удалось получить промокоды: \n{err}")
        except TypeError as err:
            raise TypeError(self.__class__.__qualname__,
                            self.coupons_series.__name__,
                            f"Не удалось получить промокоды: \n{err}")

    def coupons_info(self, organization_id: str, number: str, series: str = None) -> Union[
        CustomErrorModel, BaseCouponInfo]:
        if not bool(organization_id):
            raise ParamSetException(self.__class__.__qualname__,
                                    self.coupons_info.__name__,
                                    f"Отсутствует аргумент id организации")
        data = {
            "number": number,
            "series": series,
            "organizationId": organization_id,
        }
        try:
            return self._post_request(
                url="/api/1/loyalty/iiko/coupons/info",
                data=data,
                model_response_data=BaseCouponInfo,
            )
        except httpx.HTTPError as err:
            raise TokenException(self.__class__.__qualname__,
                                 self.coupons_info.__name__,
                                 f"Не удалось получить промокоды: \n{err}")
        except TypeError as err:
            raise TypeError(self.__class__.__qualname__,
                            self.coupons_info.__name__,
                            f"Не удалось получить промокоды: \n{err}")
