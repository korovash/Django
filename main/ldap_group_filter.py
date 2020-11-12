from django_python3_ldap.utils import format_search_filters

def custom_format_search_filters(ldap_fields):
    ldap_fields["memberOf"] = "CN=print_mon_django_user,OU=print_mon,OU=Roles,DC=dvfu,DC=ru"
    search_filters = format_search_filters(ldap_fields)
    search_filters.append("(|(memberOf=CN=print_mon_django_administrator,OU=print_mon,OU=Roles,DC=dvfu,DC=ru)(memberOf=CN=print_mon_django_user,OU=print_mon,OU=Roles,DC=dvfu,DC=ru))")
    return search_filters