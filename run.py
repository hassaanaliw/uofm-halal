from halal import app, db, models, database
import config
app.run(host='0.0.0.0', port=config.PORT, debug=True)
