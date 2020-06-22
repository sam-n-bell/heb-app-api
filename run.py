from hebapp import create_app
from hebapp.config import ProductionConfig
from dotenv import load_dotenv
load_dotenv()
import os

app = create_app(ProductionConfig)

if __name__ == '__main__':
    debug_config = os.getenv("DEBUG")
    if debug_config is None:
        debug_config = False
    else:
        debug_config = True
    
    app.run(debug=debug_config)
