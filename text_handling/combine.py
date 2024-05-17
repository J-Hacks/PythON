import os
def combine_sql_files():
    sql_files = [file for file in os.listdir('.') if file.endswith('.sql')]
    sql_files.sort()
    combined_sql = ""
    sp_number = 1
    for sql_file in sql_files:
        with open(sql_file, 'r') as file:
            sql_content = file.read()
        sql_content_with_comment = f'''/*##################################################################################
        -- NAME: {sql_file}, SP Number: {sp_number}\n/*###################################################################################\n{sql_content}\n\n'''
        combined_sql += sql_content_with_comment
        sp_number += 1
    with open('combined_sql.sql', 'w') as combined_file:
        combined_file.write(combined_sql)
combine_sql_files()
 