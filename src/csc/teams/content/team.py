"""Team content type - reference-based user listing."""

from plone.autoform import directives
from plone.supermodel import model
from zope import schema
from zope.interface import implementer


class ITeam(model.Schema):
    """Schema for Team content type.

    A team is a collection of user references that displays live
    data from LDAP/memberdata.
    """

    # Team members selection - List field with custom vocabulary
    # The widget is automatically a multi-select for List fields
    members = schema.List(
        title='Team Members',
        description='Select users to include in this team (hold Ctrl/Cmd to select multiple).',
        value_type=schema.Choice(vocabulary='csc.teams.UsersVocabulary'),
        required=False,
    )

    # Team description - using Text instead of RichText to avoid the AttributeError
    description = schema.Text(
        title='Description',
        description='Description of this team or group',
        required=False,
    )

    # Display options
    model.fieldset(
        'display',
        label='Display Options',
        fields=['show_portraits', 'show_contact_info', 'show_job_info', 'show_manager', 'sort_by']
    )

    show_portraits = schema.Bool(
        title='Show Portraits',
        description='Display user portrait images',
        default=True,
        required=False,
    )

    show_contact_info = schema.Bool(
        title='Show Contact Information',
        description='Display email, phone, and mobile',
        default=True,
        required=False,
    )

    show_job_info = schema.Bool(
        title='Show Job Information',
        description='Display job title and department',
        default=True,
        required=False,
    )

    show_manager = schema.Bool(
        title='Show Manager',
        description='Display manager name',
        default=False,
        required=False,
    )

    sort_by = schema.Choice(
        title='Sort By',
        description='How to order team members',
        values=['fullname', 'job_title', 'department', 'none'],
        default='fullname',
        required=False,
    )


@implementer(ITeam)
class Team:
    """Team content type."""
