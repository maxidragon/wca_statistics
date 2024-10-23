import os
import importlib.util
import mysql.connector
import datetime

GITHUB_URL = "https://github.com/maxidragon/wca_statistics"

db = mysql.connector.connect(
    host="localhost",
    user="root",
    database="wca_development"
)

today_str = datetime.datetime.now().strftime("%d %B %Y")

markdown_entries = []

def execute_query_from_file(filepath, db):
    spec = importlib.util.spec_from_file_location("module.name", filepath)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    result, headers, title = module.execute(db)
    markdown_content = convert_to_markdown(result, headers, title)
    markdown_entries.append(
        {
            "path": filepath.replace("statistics/", ""),
            "title": title,
        }
    )
    save_markdown_file(filepath, markdown_content)

def convert_to_markdown(data, headers, title):
    metadata_rows = f'---\nlayout: default\ntitle: {title}\n---\n'
    title_row = f"## {title}\n"
    date_row = f"*Generated on {today_str}*\n"
    header_row = "| " + " | ".join(headers) + " |\n"
    separator_row = "| " + " | ".join(['---' for _ in headers]) + " |\n"
    
    data_rows = ""
    for row in data:
        data_rows += "| " + " | ".join(str(value) for value in row) + " |\n"
    
    return metadata_rows + title_row + date_row + header_row + separator_row + data_rows

def save_markdown_file(filepath, content):
    filename = os.path.basename(filepath).replace(".py", ".md")
    output_path = os.path.join("output", filename)
    
    os.makedirs("output", exist_ok=True)
    
    with open(output_path, "w") as f:
        f.write(content)

def generate_index_page(markdown_entries):
    index_content = ""

    for item in markdown_entries:
        index_content += f"- [{item['title']}](/{item['path'].replace('.py', '.md')})\n"
    
    index_content += "\n"
    index_content += "## About\n"
    index_content += 'This site is open-source. You can find the source code [here](https://github.com/maxidragon/wca_statistics).\n\n'
    with open("output/index.md", "w") as f:
        f.write(index_content)

def main():
    stats_dir = "statistics/"
    
    for filename in os.listdir(stats_dir):
        if filename.endswith(".py"):
            filepath = os.path.join(stats_dir, filename)
            print(f"Processing {filepath}...")
            
            execute_query_from_file(filepath, db)

    sorted_entries = sorted(markdown_entries, key=lambda x: x["title"])
    generate_index_page(sorted_entries)
    print("All files processed!")

if __name__ == "__main__":
    main()
