'''
Installations required -
pip install cloud-sql-python-connector["pymysql"] SQLAlchemy
pip install google-cloud-secret-manager
'''
#Import required dependencies
from google.cloud.sql.connector import Connector
import sqlalchemy
from sqlalchemy import text

# Function to get CloudSQL instance password from Secret Manager
def access_secret_version(project_id, secret_id, version_id):
    """
    Access the payload for the given secret version if one exists. The version
    can be a version number as a string (e.g. "5") or an alias (e.g. "latest").
    """

    # Import the Secret Manager client library.
    from google.cloud import secretmanager

    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the secret version.
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"

    # Access the secret version.
    response = client.access_secret_version(request={"name": name})
    # Print the secret payload.
    # snippet is showing how to access the secret material.
    payload = response.payload.data.decode("UTF-8")
    return payload

# Function call to get DB password ino a local varaiable  
db_password = access_secret_version('rcc-game-result', 'cloudsql_pwd','1')

# initialize Connector object
connector = Connector()

# function to return the database connection
def getconn():
    conn= connector.connect(
        "rcc-game-result:europe-west10:rcc-sql",
        "pymysql",
        user="tianmin",
        password=db_password,
        db="rcc"
    )
    return conn
    
# create connection pool
pool = sqlalchemy.create_engine(
    "mysql+pymysql://",
    creator=getconn,
)



# interact with Cloud SQL database using connection pool
def insert_row():
    with pool.connect() as db_conn:
        
        # Drop Table
        drop_query = "DROP TABLE IF EXISTS basic_dtls"
        db_conn.execute(sqlalchemy.text(drop_query))
        # Create Table
        create_query = "CREATE TABLE basic_dtls(idn INT, name VARCHAR(200))"
        db_conn.execute(sqlalchemy.text(create_query))
    
        # insert statement (DML statement for data load)
        insert_stmt = sqlalchemy.text(
        "INSERT INTO basic_dtls VALUES (1, 'Jack')")
        db_conn.execute(insert_stmt)
        db_conn.commit()
    
        # query database
        result = db_conn.execute(sqlalchemy.text("SELECT * from basic_dtls")).fetchall()
    
        # Do something with the results
        for row in result:
            print(row)
    
        # Dropping Table
        # db_conn.execute(sqlalchemy.text("DROP TABLE basic_dtls"))
#insert_row()