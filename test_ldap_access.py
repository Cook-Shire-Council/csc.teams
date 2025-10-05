#!/usr/bin/env python
"""Test script to verify LDAP attribute access patterns.

Run this in Plone's bin/instance debug shell to test:
    bin/instance debug
    >>> execfile('test_ldap_access.py')
"""

from plone import api

# Test with a known user (adjust username as needed)
TEST_USERNAME = 'admin'  # Change to actual LDAP user

print("=" * 60)
print("LDAP Attribute Access Test")
print("=" * 60)

try:
    # Get user
    user = api.user.get(username=TEST_USERNAME)
    if not user:
        print(f"ERROR: User '{TEST_USERNAME}' not found")
        exit(1)

    print(f"\n✓ User found: {TEST_USERNAME}")
    print(f"  User object type: {type(user)}")

    # Method 1: Direct user properties
    print("\n--- Method 1: user.getProperty() ---")
    print(f"  fullname: {user.getProperty('fullname', 'N/A')}")
    print(f"  email: {user.getProperty('email', 'N/A')}")

    # Method 2: Get user wrapper
    print("\n--- Method 2: user.getUser() ---")
    member = user.getUser()
    print(f"  Member type: {type(member)}")

    # Method 3: Get memberdata
    print("\n--- Method 3: portal_memberdata ---")
    portal = api.portal.get()
    memberdata = portal.portal_memberdata.wrapUser(user)
    print(f"  Memberdata type: {type(memberdata)}")

    # Try to get LDAP attributes
    print("\n--- LDAP Attributes (via getattr) ---")
    attrs_to_test = ['phone', 'mobile', 'telephoneNumber', 'department',
                     'job_title', 'title', 'manager', 'distinguishedName']

    for attr in attrs_to_test:
        # Try member object
        value_member = getattr(member, attr, None)
        # Try memberdata object
        value_memberdata = getattr(memberdata, attr, None)

        if value_member or value_memberdata:
            print(f"  {attr}:")
            if value_member:
                print(f"    member.{attr} = {value_member}")
            if value_memberdata:
                print(f"    memberdata.{attr} = {value_memberdata}")

    # Method 4: Check if there's a direct LDAP plugin
    print("\n--- Method 4: LDAP Plugin Access ---")
    acl_users = portal.acl_users
    print(f"  Available plugins: {list(acl_users.objectIds())}")

    # Look for LDAP plugin
    for plugin_id in acl_users.objectIds():
        plugin = getattr(acl_users, plugin_id, None)
        if plugin and 'ldap' in plugin_id.lower():
            print(f"  Found LDAP plugin: {plugin_id} ({type(plugin)})")

    print("\n" + "=" * 60)
    print("Test completed. Review output above.")
    print("=" * 60)

except Exception as e:
    print(f"\nERROR: {e}")
    import traceback
    traceback.print_exc()
