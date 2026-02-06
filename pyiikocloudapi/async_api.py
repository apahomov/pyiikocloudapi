from pyiikocloudapi.async_base import AsyncBaseAPI  # noqa: F401

# Backward compatibility re-exports
from pyiikocloudapi.async_mixins import *  # noqa: F403
from pyiikocloudapi.async_mixins import (
    AsyncAddress,
    AsyncCommands,
    AsyncCustomers,
    AsyncDeliveries,
    AsyncDeliveryRestrictions,
    AsyncDictionaries,
    AsyncDiscountPromotion,
    AsyncEmployees,
    AsyncMenu,
    AsyncNotifications,
    AsyncOrders,
    AsyncTerminalGroup,
    AsyncWebHook,
)


# Preserve MRO order from original code
class AsyncIikoTransport(
    AsyncOrders,
    AsyncDeliveries,
    AsyncEmployees,
    AsyncAddress,
    AsyncDeliveryRestrictions,
    AsyncTerminalGroup,
    AsyncMenu,
    AsyncDictionaries,
    AsyncDiscountPromotion,
    AsyncCommands,
    AsyncNotifications,
    AsyncCustomers,
    AsyncWebHook,
):
    pass
