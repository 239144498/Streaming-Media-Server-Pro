import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.starlette import StarletteIntegration

from .config import config

sentry_sdk.init(
    dsn="https://12ff5d8b96484788be20f0f17362f084@o4503953349279744.ingest.sentry.io/4504005849579520",
    traces_sample_rate=1.0,
    send_default_pii=True,
    integrations=[
        StarletteIntegration(transaction_style="endpoint"),
        FastApiIntegration(transaction_style="endpoint"),
    ],
)
