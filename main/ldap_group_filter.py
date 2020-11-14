from django_python3_ldap.utils import format_search_filters
import os

def custom_format_search_filters(ldap_fields):
    ldap_fields["memberOf"] = os.getenv("LDAP_GROUP_FILTER")
    search_filters = format_search_filters(ldap_fields)
    search_filters.append(os.getenv("LDAP_GROUP_FILTER_LIST"))
    return search_filters