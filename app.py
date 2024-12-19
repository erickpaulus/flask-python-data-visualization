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
