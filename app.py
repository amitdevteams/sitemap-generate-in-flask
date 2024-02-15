import sys
import logging
import asyncio
from flask import Flask, render_template, request
from pysitemap import crawler

app = Flask(__name__)

def run_crawler(root_url):
    # Set up event loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # Call the crawler function
    try:
        if "--iocp" in sys.argv:
            logging.info('using iocp')
            el = asyncio.ProactorEventLoop()
            asyncio.set_event_loop(el)

        crawler(root_url, out_file='sitemap.xml')
        return 'Sitemap generated successfully'
    except Exception as e:
        app.logger.error(f'Error generating sitemap: {str(e)}')
        return f'Error generating sitemap: {str(e)}'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_sitemap', methods=['POST'])
def generate_sitemap():
    root_url = request.form.get('url')
    if root_url:
        return run_crawler(root_url)
    else:
        return 'Invalid URL'

if __name__ == '__main__':
    app.run(debug=True)
