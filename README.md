# Dask + Flask: Visualizing Data Step-by-Step

This repository provides a step-by-step approach to integrate Dask with Flask to visualize data efficiently. Dask is a flexible parallel computing library for analytics, while Flask is a lightweight web framework for building web applications in this case it used for authentication, session and cookies management.

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.8+
- pip (Python package manager)
- Dask (`pip install dask`)
- Flask (`pip install flask`)
- Pandas (`pip install pandas`)
- Matplotlib or Plotly for visualization (`pip install matplotlib plotly`)

## Step 1: Set Up the Project Structure

Organize your project directory:

```
project-name/
├── app.py
├── templates/
│   └── index.html
├── static/
│   └── style.css
└── README.md
```

## Step 2: Install Required Dependencies

Run the following command to install all required Python packages:

```bash
pip install flask dask pandas matplotlib plotly
```

## Step 3: Create the Flask Application (`app.py`)

Here is an example of a Flask application using Dask to process data and visualize it:

```python
from flask import Flask, render_template, request, jsonify
import dask.dataframe as dd
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if not file:
        return "No file uploaded!", 400

    # Read the CSV file using Dask
    dask_df = dd.read_csv(file)

    # Perform a sample computation (e.g., column mean)
    means = dask_df.mean().compute()

    # Create a simple visualization
    fig, ax = plt.subplots()
    means.plot(kind='bar', ax=ax)
    ax.set_title('Mean of Columns')

    # Convert plot to PNG image
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()

    return render_template('index.html', plot_url=plot_url)

if __name__ == '__main__':
    app.run(debug=True)
```

## Step 4: Create the HTML Template (`templates/index.html`)

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dask + Flask Visualization</title>
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>
    <h1>Upload Your Dataset</h1>
    <form action="/upload" method="post" enctype="multipart/form-data">
        <input type="file" name="file" accept=".csv">
        <button type="submit">Upload</button>
    </form>

    {% if plot_url %}
    <h2>Visualization</h2>
    <img src="data:image/png;base64,{{ plot_url }}" alt="Plot">
    {% endif %}
</body>
</html>
```

## Step 5: Add Styling (Optional: `static/style.css`)

```css
body {
    font-family: Arial, sans-serif;
    text-align: center;
    margin: 20px;
}

h1 {
    color: #333;
}

form {
    margin: 20px;
}

img {
    max-width: 100%;
    height: auto;
}
```

## Step 6: Run the Application

Run the Flask application using:

```bash
python app.py
```

Open your web browser and navigate to `http://127.0.0.1:5000`. You can upload a CSV file to visualize data.

## Step 7: Extend Functionality

- **Add More Visualizations**: Use Plotly or other libraries for interactive plots.
- **Handle Larger Datasets**: Leverage Dask's distributed computing capabilities.
- **Deploy the Application**: Use services like Heroku, AWS, or Docker for deployment.

## Conclusion

This setup provides a simple yet powerful framework to leverage Dask and Flask for data visualization. Extend and customize it to meet your project needs.
