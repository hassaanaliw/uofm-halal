from halal import app, db, models, database
import config

database.build_database()
print("**** Built Database ****")
app.run(host='0.0.0.0', port=config.PORT, debug=True)
