"""Interfaces for csc.teams."""

from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class ICSCTeamsLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""
