import subprocess
import json
import asyncio

import json
import sys

import json
import markdown2




scriptcontentpart = """function populateNavbar(content) {
            const navbarList = document.querySelector('#navbar .navlist');
            navbarList.innerHTML = '';

            content.forEach(item => {
                const listItem = document.createElement('li');
                const link = document.createElement('a');
                link.classList.add('nav-link');
                //link.href = `#${item.link}`;
                //link.href = 
                link.href = '/Users/ciscorrr/Documents/CisStuff/curr/CacheNova/Backend/htmldatacluster/' + item.link + ".html";
                link.textContent = item.title;
                listItem.appendChild(link);
                navbarList.appendChild(listItem);
            });
        }

        populateNavbar(navbarContent);

        document.getElementById('toggleNav').addEventListener('click', function() {
            document.getElementById('navbar').classList.toggle('active');
        });"""

def convert_markdown_to_html(markdown_path, navbar_content):
    # Read the Markdown file
    with open(markdown_path, 'r', encoding='utf-8') as file:
        markdown_content = file.read()

    # Convert Markdown to HTML
    html_content = markdown2.markdown(markdown_content, extras=["mathjax"])

    # Serialize navbar_content to JSON
    navbar_content_json = json.dumps(navbar_content)

    # HTML template with JavaScript for navbar
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdn.freecodecamp.org/testable-projects-fcc/v1/bundle.js"></script>
        <link href='https://fonts.googleapis.com/css?family=Aldrich' rel='stylesheet'>
        <link href='https://fonts.googleapis.com/css?family=Asap' rel='stylesheet'>
        <link rel="stylesheet" href="one.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.1/css/all.min.css">
        <meta content="width=device-width, initial-scale=1, shrink-to-fit=no" name="viewport">
        <title></title>
        <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
        <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    </head>
    <body>
        
        <main id="main-doc">
            {html_content}
        </main>

        <nav id="navbar">
            <ul class="navlist">
                <!-- Dynamic navbar content here -->
            </ul><br>
        </nav><br>

        <script>
        const navbarContent = {navbar_content_json};
        {scriptcontentpart}
        </script>
        <script src="one.js"></script>
        
    </body>
    </html>
    """

    # Determine the new HTML file path and write the final HTML content
    # Determine the new HTML file path
    md_name = markdown_path.split('/')
    md_name[-1] = md_name[-1].replace('.md', '.html')  # Change the extension to .html
    md_name[-2] = 'htmldatacluster'  # Change the directory to htmldatacluster
    html_file_path = '/'.join(md_name)

    # Write the final HTML content to the new file
    with open(html_file_path, "w", encoding='utf-8') as file:
        file.write(html_template)
    return html_file_path

def convplease(path, navbarcontent):
    html_file_path = convert_markdown_to_html(path, navbarcontent)
    return html_file_path

