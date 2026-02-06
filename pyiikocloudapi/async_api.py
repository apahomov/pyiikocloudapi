from pyiikocloudapi.async_base import AsyncBaseAPI  # noqa: F401
from pyiikocloudapi.async_mixins import (
    AsyncWebHook,
    AsyncCommands,
    AsyncDictionaries,
    AsyncDiscountPromotion,
    AsyncMenu,
    AsyncTerminalGroup,
    AsyncAddress,
    AsyncDeliveryRestrictions,
    AsyncOrders,
    AsyncDeliveries,
    AsyncNotifications,
    AsyncEmployees,
    AsyncCustomers,
)

# Backward compatibility re-exports
from pyiikocloudapi.async_mixins import *  # noqa: F401, F403


# Preserve MRO order from original code
class AsyncIikoTransport(AsyncOrders, AsyncDeliveries, AsyncEmployees, AsyncAddress,
                         AsyncDeliveryRestrictions, AsyncTerminalGroup, AsyncMenu,
                         AsyncDictionaries, AsyncDiscountPromotion, AsyncCommands,
                         AsyncNotifications, AsyncCustomers, AsyncWebHook):
    pass
