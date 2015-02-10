# encoding: utf-8

GENERAL_TEMPLATE = """
# WARNING! This file was automatically generated: do not modify it.
{indexes}
{searchd}
"""

SEARCH_TEMPLATE = """
searchd
{{
    listen = 9306:mysql41
    pid_file = {pid_file}
}}
"""

INDEX_TEMPLATE = """
source {index_name}
{{
    sql_db = {database_name}
    sql_pass = {database_password}
    sql_user = {database_user}
    sql_host = {database_host}
    sql_query_pre = SET CHARACTER_SET_RESULTS=utf8
    sql_query = {query}
    {fields}
    type = {source_type}
}}
index {index_name}
{{
    path = {index_path}
    charset_type = utf-8
    source = {index_name}
    type = plain
}}
"""
