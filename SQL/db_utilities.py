
def check_chars_table(sql_conn):
    if 'Characters' not in sql_conn.table_names('main'):
        sql_conn.create_table('main',
                              table='Characters',
                              column_data=['char_name',
                                           'user_id',
                                           'species',
                                           'age',
                                           'height',
                                           'pronouns',
                                           'booksmarts',
                                           'streetsmarts',
                                           'muscle',
                                           'acrobatics',
                                           'speed',
                                           'appeal'],
                              primary_key='char_id')
