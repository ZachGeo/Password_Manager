
sql_query_table_person = """
    CREATE TABLE person (
        username VARCHAR(50),
        password VARCHAR(250) NOT NULL,
        PRIMARY KEY (username),
        CONSTRAINT valid_username CHECK (username ~* '^[A-Za-z0-9_.-]{2,50}$'),
        CONSTRAINT valid_password CHECK (password ~* '^(?=.*[!@#$%^&*-+_])(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,250}$')
    );
"""

sql_query_table_login_data = """
    CREATE TABLE login_data (
        username VARCHAR(100) NOT NULL,
        password VARCHAR(100) NOT NULL,
        email VARCHAR(80),
        url VARCHAR(200) NOT NULL,
        app_name VARCHAR(100),
        person_username VARCHAR(50),
        CONSTRAINT fk_login_data_user FOREIGN KEY (person_username)
        REFERENCES person (username) ON DELETE CASCADE,
        CONSTRAINT proper_email 
        CHECK (email ~* '^[A-Za-z0-9_.-]+[@][A-Za-z0-9_.-]+[.][A-Za-z]+$')
    );
"""

sql_query_insert_record_person = """
    INSERT INTO person (username, password) VALUES (%s, %s) 
    ON CONFLICT (username) DO NOTHING;
"""

sql_query_check_password_person = """
    SELECT password FROM person WHERE username = %s;
"""

sql_query_check_username_person = """
    SELECT EXISTS (
        SELECT 1 FROM person WHERE username = %s);
"""

sql_query_create_password = """
    INSERT INTO login_data 
    (username, password, email, url, app_name, person_username)
    VALUES (%s, %s, %s, %s, %s, %s)
"""

sql_query_select_added_data = """
    SELECT * FROM login_data WHERE person_username = %s AND app_name = %s
"""

sql_query_select_data_based_on_email = """
    SELECT username, password, app_name FROM login_data 
    WHERE person_username = %s AND email = %s
"""

sql_query_select_data_based_on_app = """
    SELECT username, password FROM login_data 
    WHERE person_username = %s AND app_name = %s
"""

sql_query_delete_data_based_on_user = """
    DELETE FROM login_data WHERE person_username = %s
"""

sql_query_all_data_user = """
    SELECT username, password, email, url, app_name FROM login_data 
    WHERE person_username = %s
"""