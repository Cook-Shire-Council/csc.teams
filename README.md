# csc.teams

Team listing addon for Cook Shire Council Plone sites.

## Features

- **Team content type**: Create teams by selecting Plone users
- **LDAP integration**: Automatically displays user data from Active Directory
- **User picker**: Searchable, auto-complete user selection interface
- **Flexible display**: Configure what information to show (portraits, contact info, job titles, etc.)
- **Read-only**: Single source of truth - displays live data from member properties
- **Reusable**: Works across multiple sites with independent styling

## Installation

1. Add `csc.teams` to your buildout eggs
2. Run buildout
3. Install via Site Setup → Add-ons

## Usage

1. Create a **Team** content item
2. Use the user picker to select team members
3. Configure display options
4. The team will automatically display current user information from LDAP/memberdata

## Styling

The addon provides base styling that can be overridden per-site using CSS customizations.
