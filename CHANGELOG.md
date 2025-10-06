# Changelog

All notable changes to csc.teams will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.10] - 2025-10-06

### Added
- Plone 6 static resource registration using `plone:static` directive
- CSS link directly in template for reliable loading across environments
- registry.xml for resource registration with Plone resource registry
- Default profile image support (default_profile.png)
- Member info wrapper div for flexbox layout
- Grid layout with 450px minimum card width for side-by-side display

### Changed
- Portrait URL namespace from `++resource++` to `++plone++` (fixes nginx reverse proxy issues)
- Template structure: portrait on left, member info on right (desktop)
- Removed duplicate team description (Plone renders it automatically from Dublin Core)

### Fixed
- Static resources not loading when accessed via nginx reverse proxy
- Portrait images not displaying for anonymous users
- CSS not being applied to team view

## [1.0.6] - 2025-10-06

### Added
- Custom user vocabulary showing fullname sorted alphabetically
- Comprehensive error handling and logging in vocabulary
- User deduplication logic for users in both LDAP and local sources
- Fallback to `acl_users.getUsers()` if `api.user.get_users()` returns empty

### Changed
- User retrieval method from `api.user.get_users()` to `acl_users.searchUsers()`
- Vocabulary now includes all LDAP users (159 users)

### Fixed
- Empty Team Members dropdown (vocabulary not displaying any users)
- Duplicate user error for users existing in both LDAP and local sources

## [1.0.3] - 2025-10-06

### Fixed
- `ConstraintNotSatisfied` error when adding teams
- Removed invalid widget parameters (`multiple`, `size`) from SelectFieldWidget

### Changed
- Simplified members field to use default List field widget (auto-generates multi-select)

## [1.0.0] - 2025-10-06

### Added
- Initial release of csc.teams addon
- Team content type with user reference storage
- Live LDAP data fetching for team members
- Custom vocabulary for user selection
- Display options: portraits, contact info, job info, manager
- Sorting options: fullname, job_title, department, none
- LDAP attribute support: phone, mobile, department, job_title, manager
- Manager DN to CN extraction utility
- Accessibility features (ARIA labels, semantic HTML)
- Responsive CSS with mobile support
- Print styles for team member cards

### Dependencies
- Requires cook.whs.barceloneta v1.0.24+ for LDAP attribute mappings
- Plone 6.1+
- pas.plugins.ldap for LDAP integration

[1.0.10]: https://github.com/Cook-Shire-Council/csc.teams/compare/v1.0.6...v1.0.10
[1.0.6]: https://github.com/Cook-Shire-Council/csc.teams/compare/v1.0.3...v1.0.6
[1.0.3]: https://github.com/Cook-Shire-Council/csc.teams/compare/v1.0.0...v1.0.3
[1.0.0]: https://github.com/Cook-Shire-Council/csc.teams/releases/tag/v1.0.0
