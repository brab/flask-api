import os

from backend.backend import create_app

site_name = os.environ.get('SITE_NAME', 'Local')
app = create_app(site_name)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
