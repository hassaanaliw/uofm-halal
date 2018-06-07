from halal import app, db, models, database
import config
<<<<<<< HEAD
=======

database.build_database()
print("**** Built Database ****")
>>>>>>> 58f1e37fde4609cfa1021e4aa9ec0b3d7df364c2
app.run(host='0.0.0.0', port=config.PORT, debug=True)
