# import needed labraries
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, CityDB, User

engine = create_engine('sqlite:///Catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create dummy user
User1 = User(name="admin", email="assirims2015@gmail.com")
session.add(User1)
session.commit()

# Create dummy cities data
city1 = CityDB(city_name="Riyadh City",
               region="Centeral Region",
               coverUrl="""http://www.worldbank.org/content/dam/photos/780x439/2016/oct/gcc-Saudiarabia-Riyadh.jpg""",
               description="Riyadh City", category="Centeral Region", user_id=1)

session.add(city1)
session.commit()

city2 = CityDB(city_name="Jeddah City",
               region="West Region",
               coverUrl="""http://www.sainternational.us/Portals/0/WebSitesCreative_PostIt/401/dea17e12-c54a-4c52-88d7-1ee17a086add.jpg""",
               description="Jeddah City", category="West Region", user_id=1)

session.add(city2)
session.commit()

city3 = CityDB(city_name="Abha City",
               region="Southern Region",
               coverUrl="""https://i0.wp.com/www.thepinktarha.com/ksa/wp-content/uploads/2018/03/Abha-KSA.jpg""",
               description="Abha City", category="Southern Region", user_id=1)

session.add(city3)
session.commit()

city4 = CityDB(city_name="Tabuk City",
               region="Northern Region",
               coverUrl="""http://www.hotelroomsearch.net/im/city/tabuk-saudi-arabia-11.jpg""",
               description="Tabuk City", category="Northern Region", user_id=1)

session.add(city4)
session.commit()

city5 = CityDB(city_name="Dammam City",
               region="Eastern Region",
               coverUrl="""https://cloud.lovindublin.com/images/uploads/2017/10/_blogWide/Screen-Shot-2017-10-15-at-5.48.47-PM.png""",
               description="Dammam City", category="Eastern Region", user_id=1)

session.add(city5)
session.commit()
