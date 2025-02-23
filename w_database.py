import sqlite3

class Database():
    # Constructor
    def __init__(self, dbName):
        # Create/Connect to databse
        self.conn = sqlite3.connect(dbName)

        # Obtain reference to cursor
        self.cursor = self.conn.cursor()

        # Create table if it doesn't exist
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS weather
                 (city text, temp real, desc text)''')

        # Save changes
        self.conn.commit()
        return

    # Adds/updates entry
    def update_weather(self, weather):
        # Check if entry already exists
        if(self.check_weather(weather.city)):
            # Update existing entry
            self.cursor.execute("UPDATE weather SET temp = " + str(weather.temp) + ", desc = '" + weather.desc + "' WHERE city = '" + weather.city + "'")
        else:
            # Create new entry
            self.cursor.execute("INSERT INTO weather (city, temp, desc) VALUES ('" + weather.city + "'," + str(weather.temp) + ",'" + weather.desc + "')")

        # Save changes
        self.conn.commit()
        return

    # Checks whether entry exists in db
    def check_weather(self, city):
        # Fetch records
        self.cursor.execute("SELECT city FROM weather WHERE city = '" + city + "'")
        records = self.cursor.fetchall()

        # Check results
        if(len(records) < 1):
            return False
        else:
            return True

    # Returns list of all cities in db
    def get_cities(self):
        # Fetch records
        self.cursor.execute("SELECT city FROM weather")
        cities_tuples = self.cursor.fetchall()
        
        #Clean up records
        cities_clean = [''.join(i) for i in cities_tuples]
        
        #Return result
        return cities_clean

    # Closes database connection
    def shutdown(self):
        self.conn.close();