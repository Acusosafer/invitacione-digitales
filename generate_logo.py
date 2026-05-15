import asyncio
from playwright.async_api import async_playwright

async def generate_logo():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <link href="https://fonts.googleapis.com/css2?family=Syne:wght@800&family=Inter:wght@800&display=swap" rel="stylesheet">
        <style>
            body {
                margin: 0;
                padding: 40px;
                background: transparent;
                display: flex;
                align-items: center;
                justify-content: center;
                width: 800px;
                height: 400px;
            }
            .logo-container {
                text-align: center;
            }
            .shimmer-text {
                font-family: 'Syne', sans-serif;
                font-weight: 800;
                font-size: 52px;
                background: linear-gradient(125deg, #ff3b6f, #ff8ad4, #c471ff);
                -webkit-background-clip: text;
                color: transparent;
                margin-bottom: 15px;
                line-height: 1;
            }
            .neon-oficial {
                font-family: 'Inter', sans-serif;
                font-weight: 800;
                font-size: 24px;
                letter-spacing: 12px;
                text-transform: uppercase;
                color: #ffffff;
                text-shadow: 0 0 5px #ff3b6f, 0 0 10px #ff3b6f, 0 0 20px #c471ff, 0 0 40px #c471ff;
            }
        </style>
    </head>
    <body>
        <div class="logo-container" id="logo">
            <div class="shimmer-text">Invitaciones Digitales</div>
            <div class="neon-oficial">OFICIAL</div>
        </div>
    </body>
    </html>
    """
    
    with open("temp_logo.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(f"file:///{__file__.replace('generate_logo.py', 'temp_logo.html').replace(chr(92), '/')}")
        # wait for fonts to load
        await page.evaluate('document.fonts.ready')
        
        element = await page.query_selector('#logo')
        await element.screenshot(path='logo.png', omit_background=True)
        await browser.close()

asyncio.run(generate_logo())
