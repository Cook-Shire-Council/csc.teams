"""Vocabularies for csc.teams addon."""

from plone import api
from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary


@provider(IVocabularyFactory)
def users_vocabulary(context):
    """Vocabulary of users showing fullname, sorted alphabetically.

    Returns users in format:
        Token: username (e.g., 'adams')
        Value: username
        Title: Full Name (CN) (e.g., 'Adam Smith')
    """
    users_list = []

    # Get all users
    users = api.user.get_users()

    for user in users:
        username = user.getId()
        fullname = user.getProperty('fullname', '') or username

        users_list.append({
            'username': username,
            'fullname': fullname,
        })

    # Sort alphabetically by fullname
    users_list.sort(key=lambda x: x['fullname'].lower())

    # Create vocabulary terms
    terms = [
        SimpleTerm(
            value=user['username'],
            token=user['username'],
            title=user['fullname']
        )
        for user in users_list
    ]

    return SimpleVocabulary(terms)
