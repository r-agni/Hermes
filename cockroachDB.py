import os
import psycopg2
import pdf_parser

conn = psycopg2.connect(os.environ["DATABASE_URL"])

pdf_parser.parse("CBC-sample-blood-test-report.pdf")

with conn.cursor() as cur:
    # creating data table on cockroach
    cur.execute("CREATE TABLE data (test STRING, result STRING);")

    # BELOW IS A CLI COMMAND which creates a data bucket on cockroach (remember to replace string after --url with a new database url, i.e. do not use aditya's database)
    ### cockroach userfile upload data.csv /data.csv --certs-dir=certs --url 'postgresql://aditya:XB1A07FP5Gr0jESIsz6tXg@marble-caracal-13324.5xj.cockroachlabs.cloud:26257/defaultdb?sslmode=verify-full'

    # after bucket is created above, load userfile to cockroach
    cur.execute("IMPORT INTO data (test, result) CSV DATA ('userfile://defaultdb.public.userfiles_aditya/data.csv') WITH skip='1';")
    res = cur.fetchall()
    conn.commit()
