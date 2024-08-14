import json
import os

def generate_html(json_file_path, output_file_path):
    # Read the JSON data
    with open(json_file_path, 'r') as file:
        json_data = json.load(file)
    
    # HTML template
    html_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Prettified AI Risk Repository</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f4f4f4;
            padding: 20px;
        }
        #page-container {
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            padding: 20px;
            max-width: 1000px;
            margin: 0 auto;
        }
        h1 {
            color: #0066cc;
            text-align: center;
            margin-bottom: 20px;
        }
        .intro {
            background-color: #e6f3ff;
            border-left: 5px solid #0066cc;
            padding: 15px;
            margin-bottom: 20px;
            border-radius: 0 4px 4px 0;
        }
        .intro p {
            margin: 0 0 10px 0;
        }
        .intro ul {
            margin: 0;
            padding-left: 20px;
        }
        .disclaimer {
            font-style: italic;
            margin-top: 15px;
            padding: 10px;
            background-color: #fff9e6;
            border-radius: 4px;
        }
        .disclaimer a {
            color: #0066cc;
            text-decoration: none;
        }
        .disclaimer a:hover {
            text-decoration: underline;
        }
        .citation {
            background-color: #e8f5e9;
            border-left: 5px solid #4caf50;
            padding: 15px;
            margin-top: 20px;
            border-radius: 0 4px 4px 0;
            font-size: 0.9em;
        }
        .citation p {
            margin: 0;
        }
        .tree-node {
            margin-left: 20px;
            border-left: 1px solid #ddd;
            padding-left: 15px;
            position: relative;
        }
        .tree-content {
            cursor: pointer;
            user-select: none;
            padding: 10px;
            border-radius: 4px;
            transition: background-color 0.3s ease;
        }
        .tree-content:hover {
            background-color: #f0f0f0;
        }
        .tree-content::before {
            content: '▶';
            color: #666;
            display: inline-block;
            margin-right: 10px;
            transition: transform 0.3s ease;
        }
        .tree-content-open::before {
            transform: rotate(90deg);
        }
        .tree-children {
            display: none;
            margin-top: 5px;
        }
        .tree-children-open {
            display: block;
            animation: fadeIn 0.5s ease-out;
        }
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        .node-header {
            display: flex;
            align-items: baseline;
            flex-wrap: wrap;
        }
        .node-key {
            font-weight: bold;
            margin-right: 10px;
            color: #0066cc;
            font-size: 1.1em;
        }
        .node-title {
            font-weight: 500;
            font-size: 1.1em;
            color: #2c3e50;
            margin-right: 10px;
        }
        .node-details {
            margin-top: 10px;
            background-color: #f9f9f9;
            border-left: 3px solid #0066cc;
            padding: 10px;
            border-radius: 0 4px 4px 0;
        }
        .detail-item {
            margin-bottom: 5px;
        }
        .detail-label {
            font-weight: bold;
            color: #555;
        }
        .tag {
            display: inline-block;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 0.8em;
            margin-right: 5px;
            margin-bottom: 5px;
            color: white;
        }
        .entity-tag { background-color: #3498db; }
        .intent-tag { background-color: #e74c3c; }
        .timing-tag { background-color: #2ecc71; }
        .domain-tag { background-color: #9b59b6; }
        .subdomain-tag { background-color: #f39c12; }
        .quickref-link {
            color: #0066cc;
            text-decoration: none;
        }
        .quickref-link:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div id="page-container">
        <h1>Prettified AI Risk Repository</h1>
        <div class="intro">
            <p><strong>What is the AI Risk Repository?</strong><br>
            The AI Risk Repository has three parts:</p>
            <ul>
                <li>The <strong>AI Risk Database</strong> captures 700+ risks extracted from 43 existing frameworks, with quotes and page numbers.</li>
                <li>The <strong>Causal Taxonomy of AI Risks</strong> classifies how, when, and why these risks occur.</li>
                <li>The <strong>Domain Taxonomy of AI Risks</strong> classifies these risks into seven domains (e.g., "Misinformation") and 23 subdomains (e.g., "False or misleading information").</li>
            </ul>
            <div class="disclaimer">
                <p>This is not a work done by CMU students but rather by MIT. Please support and check out the actual database: <a href="https://airisk.mit.edu/#How-to-use-the-AI-Risk-Repository" target="_blank">https://airisk.mit.edu/#How-to-use-the-AI-Risk-Repository</a></p>
                <p>Our goal was to simply prettify and make it easier to digest.</p>
            </div>
            <div class="citation">
                <p><strong>Reference to Original Work:</strong> Slattery, P., Saeri, A. K., Grundy, E. A. C., Graham, J., Noetel, M., Uuk, R., Dao, J., Pour, S., Casper, S., & Thompson, N. (2024). A systematic evidence review and common frame of reference for the risks from artificial intelligence. http://doi.org/10.13140/RG.2.2.28850.00968</p>
            </div>
        </div>
        <div id="tree-container"></div>
    </div>

    <script>
        const treeData = {json_data};

        function createTreeNode(key, node) {
            const div = document.createElement('div');
            div.className = 'tree-node';
            
            const content = document.createElement('div');
            content.className = 'tree-content';
            
            const header = document.createElement('div');
            header.className = 'node-header';
            
            const keySpan = document.createElement('span');
            keySpan.className = 'node-key';
            keySpan.textContent = key;
            
            const titleSpan = document.createElement('span');
            titleSpan.className = 'node-title';
            titleSpan.textContent = node.value.Title || 'No Title';
            
            header.appendChild(keySpan);
            header.appendChild(titleSpan);

            const tags = ['Entity', 'Intent', 'Timing', 'Domain', 'Sub-domain'];
            tags.forEach(tag => {
                if (node.value[tag] && node.value[tag] !== 'NaN') {
                    const tagSpan = document.createElement('span');
                    tagSpan.className = `tag ${tag.toLowerCase().replace('-', '')}-tag`;
                    tagSpan.textContent = node.value[tag];
                    header.appendChild(tagSpan);
                }
            });

            content.appendChild(header);
            div.appendChild(content);

            const details = document.createElement('div');
            details.className = 'node-details';
            
            const detailItems = [
                {label: 'Risk category', key: 'Risk category'},
                {label: 'Risk subcategory', key: 'Risk subcategory'},
                {label: 'Description', key: 'Description'},
                {label: 'QuickRef', key: 'QuickRef'}
            ];

            detailItems.forEach(item => {
                if (node.value[item.key] && node.value[item.key] !== 'NaN') {
                    const detailItem = document.createElement('div');
                    detailItem.className = 'detail-item';
                    const label = document.createElement('span');
                    label.className = 'detail-label';
                    label.textContent = `${item.label}: `;
                    detailItem.appendChild(label);
                    
                    if (item.key === 'QuickRef' && Array.isArray(node.value[item.key])) {
                        const [name, url] = node.value[item.key];
                        const link = document.createElement('a');
                        link.href = url;
                        link.textContent = name;
                        link.className = 'quickref-link';
                        link.target = '_blank';
                        detailItem.appendChild(link);
                    } else if (Array.isArray(node.value[item.key])) {
                        detailItem.appendChild(document.createTextNode(node.value[item.key].join(', ')));
                    } else {
                        detailItem.appendChild(document.createTextNode(node.value[item.key]));
                    }
                    
                    details.appendChild(detailItem);
                }
            });

            div.appendChild(details);

            if (node.children && Object.keys(node.children).length > 0) {
                const childrenContainer = document.createElement('div');
                childrenContainer.className = 'tree-children';
                
                for (const childKey in node.children) {
                    childrenContainer.appendChild(createTreeNode(childKey, node.children[childKey]));
                }
                
                div.appendChild(childrenContainer);
                
                content.addEventListener('click', (e) => {
                    e.stopPropagation();
                    content.classList.toggle('tree-content-open');
                    childrenContainer.classList.toggle('tree-children-open');
                });
            }

            return div;
        }

        const treeContainer = document.getElementById('tree-container');
        for (const key in treeData) {
            treeContainer.appendChild(createTreeNode(key, treeData[key]));
        }
    </script>
</body>
</html>
    '''
    
    # Replace the placeholder with the actual JSON data
    html_content = html_template.replace('{json_data}', json.dumps(json_data))
    
    # Write the HTML content to the output file
    with open(output_file_path, 'w') as file:
        file.write(html_content)
    
    print(f"HTML file has been generated: {output_file_path}")

# Usage example
if __name__ == "__main__":
    input_json_file = "mit_ai_risk_tree.json"  # Replace with your JSON file path
    output_html_file = "index.html"  # Output HTML file name
    
    # Check if the input file exists
    if not os.path.exists(input_json_file):
        print(f"Error: Input file '{input_json_file}' not found.")
    else:
        generate_html(input_json_file, output_html_file)