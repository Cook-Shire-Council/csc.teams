"""Vocabularies for csc.teams addon."""

import logging
from plone import api
from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

logger = logging.getLogger(__name__)


@provider(IVocabularyFactory)
def users_vocabulary(context):
    """Vocabulary of users showing fullname, sorted alphabetically.

    Returns users in format:
        Token: username (e.g., 'adams')
        Value: username
        Title: Full Name (CN) (e.g., 'Adam Smith')
    """
    users_list = []

    try:
        # Get portal and acl_users
        portal = api.portal.get()
        acl_users = portal.acl_users

        # Use searchUsers to get ALL users including LDAP
        # Empty search with no criteria returns all users
        user_results = acl_users.searchUsers()

        logger.info(f"Got {len(user_results) if user_results else 0} users from acl_users.searchUsers()")

        for user_info in user_results:
            try:
                # user_info is a dict with keys like 'userid', 'login', 'pluginid'
                username = user_info.get('userid') or user_info.get('id')

                if not username:
                    logger.warning(f"Skipping user with no username: {user_info}")
                    continue

                # Get the actual user object to retrieve properties
                user = api.user.get(username=username)
                if not user:
                    logger.warning(f"Could not get user object for: {username}")
                    continue

                # Get fullname property
                fullname = user.getProperty('fullname', '')

                # If no fullname, use username
                if not fullname:
                    fullname = username

                users_list.append({
                    'username': username,
                    'fullname': fullname,
                })
            except Exception as e:
                logger.error(f"Error processing user {user_info}: {e}")
                continue

        # Deduplicate users by username (keep first occurrence)
        seen_usernames = set()
        unique_users = []
        for user in users_list:
            if user['username'] not in seen_usernames:
                seen_usernames.add(user['username'])
                unique_users.append(user)
            else:
                logger.debug(f"Skipping duplicate user: {user['username']}")

        # Sort alphabetically by fullname
        unique_users.sort(key=lambda x: x['fullname'].lower())

        logger.info(f"Returning vocabulary with {len(unique_users)} unique users (from {len(users_list)} total)")

        # Create vocabulary terms
        terms = [
            SimpleTerm(
                value=user['username'],
                token=user['username'],
                title=user['fullname']
            )
            for user in unique_users
        ]

        return SimpleVocabulary(terms)

    except Exception as e:
        logger.error(f"Error creating users vocabulary: {e}", exc_info=True)
        # Return empty vocabulary rather than crash
        return SimpleVocabulary([])
