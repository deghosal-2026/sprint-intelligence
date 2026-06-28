import os
from api.app import create_app

app = create_app()
port = int(os.getenv("PORT", 5001))
app.run(host="0.0.0.0", port=port, debug=False)
