"""Utility functions for csc.teams addon."""

import logging
import re

logger = logging.getLogger(__name__)


def extract_cn_from_dn(dn):
    """Extract the CN (Common Name) from an LDAP Distinguished Name.

    Example:
        CN=Scott Johnson,OU=Workshop,OU=Depot,... -> Scott Johnson

    Args:
        dn: LDAP Distinguished Name string

    Returns:
        Common Name (CN) value, or empty string if no CN found
    """
    if not dn:
        return ''

    # Match CN= followed by anything until the next comma or end of string
    match = re.match(r'^CN=([^,]+)', dn, re.IGNORECASE)
    if match:
        return match.group(1)

    # If no CN found, return empty string
    return ''


def get_user_manager_name(member):
    """Get the manager's display name from a member's manager DN.

    Args:
        member: IMemberData or member wrapper object

    Returns:
        Manager's name (CN extracted from DN), or empty string
    """
    manager_dn = getattr(member, 'manager', '')
    return extract_cn_from_dn(manager_dn)
