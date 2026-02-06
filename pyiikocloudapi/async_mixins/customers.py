from typing import Optional, Union

import httpx

from pyiikocloudapi.async_base import AsyncBaseAPI
from pyiikocloudapi.exception import PostException
from pyiikocloudapi.models import (
    CustomerCreateOrUpdateModel,
    CustomerInfoModel,
    CustomerProgramAddResponse,
    CustomErrorModel,
    TypeRCI,
    WalletHoldResponse,
)


class AsyncCustomers(AsyncBaseAPI):
    async def customer_info(
        self, organization_id: str, identifier: str, type: str, timeout=AsyncBaseAPI.DEFAULT_TIMEOUT
    ) -> Union[CustomerInfoModel, CustomErrorModel]:
        """

        :param organization_id:
        :param identifier: Depending on type
        :param type: phone or  cardTrack or cardNumber or email or id
        :return:
        """
        data = {
            "organizationId": organization_id,
            "type": type,
        }
        if type == TypeRCI.phone.value:
            data[TypeRCI.phone.value] = identifier
        elif type == TypeRCI.card_track.value:
            data[TypeRCI.card_track.value] = identifier
        elif type == TypeRCI.card_number.value:
            data[TypeRCI.card_number.value] = identifier
        elif type == TypeRCI.email.value:
            data[TypeRCI.email.value] = identifier
        elif type == TypeRCI.id.value:
            data[TypeRCI.id.value] = identifier

        try:
            return await self._post_request(
                url="/api/1/loyalty/iiko/customer/info",
                data=data,
                model_response_data=CustomerInfoModel,
                timeout=timeout,
            )

        except httpx.HTTPError as err:
            raise PostException(
                self.__class__.__qualname__,
                self.customer_info.__name__,
                f"Не удалось получить информацию о клиенте: \n{err}",
            )
        except TypeError as err:
            raise PostException(self.__class__.__qualname__, self.customer_info.__name__, f"Не удалось: \n{err}")

    async def customer_create_or_update(
        self,
        organization_id: str,
        phone: Optional[str] = None,
        card_track: Optional[str] = None,
        card_number: Optional[str] = None,
        name: Optional[str] = None,
        middle_name: Optional[str] = None,
        sur_name: Optional[str] = None,
        birthday: Optional[str] = None,
        email: Optional[str] = None,
        sex: Optional[str] = None,
        consent_status: Optional[str] = None,
        should_receive_promo_actions_info: Optional[bool] = None,
        referrer_id: Optional[str] = None,
        user_data: Optional[str] = None,
        id: str = None,
        timeout=AsyncBaseAPI.DEFAULT_TIMEOUT,
    ):

        data = {
            "organizationId": organization_id,
        }
        if id is not None:
            data["id"] = id
        if phone is not None:
            data["phone"] = phone
        if card_track is not None:
            data["cardTrack"] = card_track
        if card_number is not None:
            data["cardNumber"] = card_number
        if name is not None:
            data["name"] = name
        if middle_name is not None:
            data["middleName"] = middle_name
        if sur_name is not None:
            data["surName"] = sur_name
        if birthday is not None:
            data["birthday"] = birthday
        if email is not None:
            data["email"] = email
        if sex is not None:
            data["sex"] = sex
        if consent_status is not None:
            data["consentStatus"] = consent_status
        if should_receive_promo_actions_info is not None:
            data["shouldReceivePromoActionsInfo"] = should_receive_promo_actions_info
        if referrer_id is not None:
            data["referrerId"] = referrer_id
        if user_data is not None:
            data["userData"] = user_data

        try:
            return await self._post_request(
                url="/api/1/loyalty/iiko/customer/create_or_update",
                data=data,
                model_response_data=CustomerCreateOrUpdateModel,
                timeout=timeout,
            )

        except httpx.HTTPError as err:
            raise PostException(
                self.__class__.__qualname__,
                self.customer_create_or_update.__name__,
                f"Не удалось создать или обновить клиента: \n{err}",
            )
        except TypeError as err:
            raise PostException(
                self.__class__.__qualname__, self.customer_create_or_update.__name__, f"Не удалось: \n{err}"
            )

    async def customer_program_add(
        self, customer_id: str, program_id: str, organization_id: str, timeout=AsyncBaseAPI.DEFAULT_TIMEOUT
    ):

        data = {
            "customerId": customer_id,
            "programId": program_id,
            "organizationId": organization_id,
        }
        try:
            return await self._post_request(
                url="/api/1/loyalty/iiko/customer/program/add",
                data=data,
                model_response_data=CustomerProgramAddResponse,
                timeout=timeout,
            )

        except httpx.HTTPError as err:
            raise PostException(
                self.__class__.__qualname__,
                self.customer_program_add.__name__,
                f"Не удалось подключить клиента к программе: \n{err}",
            )
        except TypeError as err:
            raise PostException(self.__class__.__qualname__, self.customer_program_add.__name__, f"Не удалось: \n{err}")

    async def customer_card_add(
        self, customer_id: str, card_track: str, card_number, organization_id: str, timeout=AsyncBaseAPI.DEFAULT_TIMEOUT
    ):

        data = {
            "customerId": customer_id,
            "cardTrack": card_track,
            "cardNumber": card_number,
            "organizationId": organization_id,
        }
        try:
            return await self._post_request(
                url="/api/1/loyalty/iiko/customer/card/add", data=data, model_response_data=None, timeout=timeout
            )

        except httpx.HTTPError as err:
            raise PostException(
                self.__class__.__qualname__,
                self.customer_card_add.__name__,
                f"Не удалось подключить карту клиенту: \n{err}",
            )
        except TypeError as err:
            raise PostException(self.__class__.__qualname__, self.customer_card_add.__name__, f"Не удалось: \n{err}")

    async def customer_card_delete(
        self, customer_id: str, card_track: str, organization_id: str, timeout=AsyncBaseAPI.DEFAULT_TIMEOUT
    ):

        data = {
            "customerId": customer_id,
            "cardTrack": card_track,
            "organizationId": organization_id,
        }
        try:
            return await self._post_request(
                url="/api/1/loyalty/iiko/customer/card/remove", data=data, model_response_data=None, timeout=timeout
            )

        except httpx.HTTPError as err:
            raise PostException(
                self.__class__.__qualname__,
                self.customer_card_delete.__name__,
                f"Не удалось подключить карту клиенту: \n{err}",
            )
        except TypeError as err:
            raise PostException(self.__class__.__qualname__, self.customer_card_delete.__name__, f"Не удалось: \n{err}")

    async def customer_wallet_hold(
        self,
        customer_id: str,
        wallet_id: str,
        sum: Union[int, float],
        organization_id: str,
        transaction_id: Optional[str] = None,
        comment: Optional[str] = None,
        timeout=AsyncBaseAPI.DEFAULT_TIMEOUT,
    ):

        data = {
            "customerId": customer_id,
            "walletId": wallet_id,
            "sum": sum,
            "organizationId": organization_id,
        }
        if transaction_id is not None:
            data["transactionId"] = transaction_id
        if comment is not None:
            data["comment"] = comment

        try:
            return await self._post_request(
                url="/api/1/loyalty/iiko/customer/wallet/hold",
                data=data,
                model_response_data=WalletHoldResponse,
                timeout=timeout,
            )

        except httpx.HTTPError as err:
            raise PostException(
                self.__class__.__qualname__,
                self.customer_wallet_hold.__name__,
                f"Не удалось подключить карту клиенту: \n{err}",
            )
        except TypeError as err:
            raise PostException(self.__class__.__qualname__, self.customer_wallet_hold.__name__, f"Не удалось: \n{err}")

    async def customer_wallet_cancel_hold(
        self, organization_id: str, transaction_id: str, timeout=AsyncBaseAPI.DEFAULT_TIMEOUT
    ):

        data = {
            "organizationId": organization_id,
            "transactionId": transaction_id,
        }

        try:
            return await self._post_request(
                url="/api/1/loyalty/iiko/customer/wallet/cancel_hold",
                data=data,
                model_response_data=None,
                timeout=timeout,
            )

        except httpx.HTTPError as err:
            raise PostException(
                self.__class__.__qualname__,
                self.customer_wallet_cancel_hold.__name__,
                f"Не удалось подключить карту клиенту: \n{err}",
            )
        except TypeError as err:
            raise PostException(
                self.__class__.__qualname__, self.customer_wallet_cancel_hold.__name__, f"Не удалось: \n{err}"
            )

    async def customer_wallet_topup(
        self,
        customer_id: str,
        wallet_id: str,
        sum: Union[int, float],
        organization_id: str,
        comment: Optional[str] = None,
        timeout=AsyncBaseAPI.DEFAULT_TIMEOUT,
    ):
        """
        Refill balance.
        Refill customer balance.
        :param customer_id: Customer id.
        :param wallet_id: Wallet id.
        :param sum: Sum of balance change. Must be possible.
        :param organization_id: Organization id.
        :param comment: Comment. Can be null.
        :param timeout:
        :return: dict response
        """

        data = {
            "customerId": customer_id,
            "walletId": wallet_id,
            "sum": sum,
            "organizationId": organization_id,
        }
        if comment is not None:
            data["comment"] = comment
        try:
            return await self._post_request(
                url="/api/1/loyalty/iiko/customer/wallet/topup", data=data, model_response_data=None, timeout=timeout
            )

        except httpx.HTTPError as err:
            raise PostException(
                self.__class__.__qualname__,
                self.customer_wallet_topup.__name__,
                f"Не удалось подключить карту клиенту: \n{err}",
            )
        except TypeError as err:
            raise PostException(
                self.__class__.__qualname__, self.customer_wallet_topup.__name__, f"Не удалось: \n{err}"
            )

    async def customer_wallet_chargeoff(
        self,
        customer_id: str,
        wallet_id: str,
        sum: Union[int, float],
        organization_id: str,
        comment: Optional[str] = None,
        timeout=AsyncBaseAPI.DEFAULT_TIMEOUT,
    ):
        """
        Withdraw balance.
        Withdraw customer balance.
        :param customer_id: Customer id.
        :param wallet_id: Wallet id.
        :param sum: Sum of balance change. Must be possible.
        :param organization_id: Organization id.
        :param comment: Comment. Can be null.
        :param timeout:
        :return: dict response
        """

        data = {
            "customerId": customer_id,
            "walletId": wallet_id,
            "sum": sum,
            "organizationId": organization_id,
        }
        if comment is not None:
            data["comment"] = comment
        try:
            return await self._post_request(
                url="/api/1/loyalty/iiko/customer/wallet/chargeoff",
                data=data,
                model_response_data=None,
                timeout=timeout,
            )

        except httpx.HTTPError as err:
            raise PostException(
                self.__class__.__qualname__,
                self.customer_wallet_chargeoff.__name__,
                f"Не удалось подключить карту клиенту: \n{err}",
            )
        except TypeError as err:
            raise PostException(
                self.__class__.__qualname__, self.customer_wallet_chargeoff.__name__, f"Не удалось: \n{err}"
            )
