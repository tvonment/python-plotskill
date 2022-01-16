#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os


class DefaultConfig:
    """ Bot Configuration """

    PORT = 39783
    APP_ID = os.environ.get(
        "MicrosoftAppId", "8064ddb7-fdaf-4085-b408-11f1eba2db93")
    APP_PASSWORD = os.environ.get(
        "MicrosoftAppPassword", "NZn7Q~8cwogleO22Z~.H1ehomo2HC0yOnB3xM")
    APP_TYPE = os.environ.get("MicrosoftAppType", "MultiTenant")

    # Callers to only those specified, '*' allows any caller.
    # Example: os.environ.get("AllowedCallers", ["aaaaaaaa-1111-aaaa-aaaa-aaaaaaaa"])
    ALLOWED_CALLERS = os.environ.get("AllowedCallers", ["*"])
