"""Browser views for csc.teams addon."""

import logging

from plone import api
from Products.Five.browser import BrowserView

from ..utils import extract_cn_from_dn

logger = logging.getLogger(__name__)


class TeamView(BrowserView):
    """View for displaying team members with live LDAP data."""

    def get_team_members(self):
        """Get member info for all users in self.context.members.

        Returns:
            List[dict]: List of member data dictionaries with structure:
            {
                'username': 'johnsmith',
                'fullname': 'John Smith',
                'email': 'john.smith@cook.qld.gov.au',
                'phone': '07 4000 1234',
                'mobile': '0400 123 456',
                'job_title': 'WHS Officer',
                'department': 'Safety',
                'manager_name': 'Jane Doe',
                'portrait_url': '/portal_memberdata/portraits/johnsmith',
            }
        """
        members = []
        member_usernames = getattr(self.context, 'members', None) or []

        for username in member_usernames:
            user_data = self._get_user_data(username)
            if user_data:
                members.append(user_data)
            else:
                logger.warning(f"Could not retrieve data for user: {username}")

        # Sort according to context.sort_by
        return self._sort_members(members)

    def _get_user_data(self, username):
        """Fetch live data from Plone user + memberdata.

        Args:
            username: The username to fetch data for

        Returns:
            dict: User data dictionary, or None if user not found
        """
        try:
            user = api.user.get(username=username)
            if not user:
                logger.warning(f"User not found: {username}")
                return None

            # Get standard user properties (works with LDAP)
            # Based on cook.whs.barceloneta theme LDAP configuration:
            # - phone maps to telephoneNumber in AD
            # - mobile maps to mobile in AD
            # - department maps to department in AD
            # - job_title maps to title in AD (job position)
            # - manager maps to manager in AD (DN)
            fullname = user.getProperty('fullname', '') or username
            email = user.getProperty('email', '')
            phone = user.getProperty('phone', '')
            mobile = user.getProperty('mobile', '')
            job_title = user.getProperty('job_title', '')  # LDAP: title -> job_title
            department = user.getProperty('department', '')

            # Get manager DN and extract name
            # Manager is stored as full DN in AD (e.g., "CN=Jane Doe,OU=...")
            manager_dn = user.getProperty('manager', '')
            manager_name = extract_cn_from_dn(manager_dn) if manager_dn else ''

            return {
                'username': username,
                'fullname': fullname,
                'email': email,
                'phone': phone,
                'mobile': mobile,
                'job_title': job_title,
                'department': department,
                'manager_name': manager_name,
                'portrait_url': self._get_portrait_url(username),
            }

        except Exception as e:
            logger.error(f"Error fetching data for user {username}: {e}", exc_info=True)
            return None

    def _get_portrait_url(self, username):
        """Get portrait URL from portal_memberdata or default.

        Args:
            username: The username to get portrait for

        Returns:
            str: URL to portrait image
        """
        try:
            portal = api.portal.get()
            portraits = portal.portal_memberdata.portraits

            if username in portraits:
                return f"{portal.absolute_url()}/portal_memberdata/portraits/{username}"

        except AttributeError:
            logger.debug("No portrait collection available")

        # Return custom default profile image
        portal = api.portal.get()
        return f"{portal.absolute_url()}/++resource++csc.teams/default_profile.png"

    def _sort_members(self, members):
        """Sort members according to context.sort_by.

        Args:
            members: List of member data dictionaries

        Returns:
            List[dict]: Sorted list of members
        """
        sort_by = getattr(self.context, 'sort_by', 'fullname')

        if sort_by == 'none':
            return members

        # Map sort field to dictionary key
        key_map = {
            'fullname': 'fullname',
            'job_title': 'job_title',
            'department': 'department',
        }

        sort_key = key_map.get(sort_by, 'fullname')

        try:
            return sorted(members, key=lambda m: m.get(sort_key, '').lower())
        except Exception as e:
            logger.error(f"Error sorting members by {sort_by}: {e}")
            return members
