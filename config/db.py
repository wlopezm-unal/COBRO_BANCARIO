from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


#definir la url de la base de datos
URL_DATABASE='mysql+pymysql://root:Karmafox07@localhost:3306/database_bank'

#crear motor de la base de datos que se conectara a la url 
engine=create_engine(URL_DATABASE)

#crear una clase
SessionLocal=sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base=declarative_base()



