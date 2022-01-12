# -*- coding: utf-8 -*-
"""
    Utilities
    ---------

    Common, helper utility functions shared across the codebase

"""

from enum import Enum


class AwsService(Enum):
    """AWS service supported by function"""

    cloudwatch = "cloudwatch"
    guardduty = "guardduty"


def get_service_url(region: str, service: str) -> str:
    """Get the appropriate service URL for the region

    :param region: name of the AWS region
    :param service: name of the AWS service
    :returns: AWS console url formatted for the region and service provided
    """
    try:
        service_name = AwsService[service].value
        console = "console.aws.amazon.com"

        if region.startswith("us-gov-"):
            console = "console.amazonaws-us-gov.com"

        return f"https://{console}/{service_name}/home?region={region}"

    except KeyError:
        print(f"Service {service} is currently not supported")
        raise
