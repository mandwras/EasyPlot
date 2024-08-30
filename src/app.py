from flask import Flask, request, render_template, send_file
import pandas as pd
import matplotlib.pyplot as plt
import io
import os

app = Flask(__name__)

# Acceptable temperature ranges
lower_bound = 18.0
upper_bound = 22.0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part", 410
    
    file = request.files['file']
    
    if file.filename == '':
        return "No selected file", 420

    if file and allowed_file(file.filename):
        try:
            # Read the file into a DataFrame
            df = pd.read_csv(file, encoding='latin1')

            # Print the column names for debugging
            print("Columns in the uploaded file:", df.columns)

            # Check if required columns exist
            required_columns = ['Time', 'Celsius(C)']
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                return f"Missing required columns: {', '.join(missing_columns)}", 400

            # Convert 'Celsius(C)' to numeric values
            df['Celsius(C)'] = pd.to_numeric(df['Celsius(C)'], errors='coerce')
            df['Time'] = pd.to_datetime(df['Time'], errors='coerce')

            # Drop rows with NaN values
            df = df.dropna()

            # Check if there are still any rows to plot
            if df.empty:
                return "No valid data to plot after cleaning", 430

            # Check if the temperature is within the acceptable range
            df['Within Range'] = df['Celsius(C)'].between(lower_bound, upper_bound)
            
            # Create the plot
            plt.figure(figsize=(10, 6))
            plt.plot(df['Time'], df['Celsius(C)'], label='Temperature', marker='o')
            plt.fill_between(df['Time'], lower_bound, upper_bound, color='green', alpha=0.1, label='Acceptable Range')
            plt.scatter(df['Time'][df['Within Range']], df['Celsius(C)'][df['Within Range']], color='green', label='Within Range')
            plt.scatter(df['Time'][~df['Within Range']], df['Celsius(C)'][~df['Within Range']], color='red', label='Outside Range')
            plt.xlabel('Time')
            plt.ylabel('Temperature (°C)')
            plt.title('Temperature Readings vs. Time')
            plt.legend()
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            img = io.BytesIO()
            plt.savefig(img, format='png')
            img.seek(0)
            plt.close()
            
            return send_file(img, mimetype='image/png', as_attachment=True, download_name='plot.png')
        
        except pd.errors.EmptyDataError:
            return "Uploaded file is empty", 440
        except pd.errors.ParserError:
            return "Error parsing the file. Ensure it is in CSV format", 450
        except Exception as e:
            return f"An error occurred: {e}", 500
    else:
        return "Invalid file type. Please upload a CSV file.", 460

def allowed_file(filename):
    """Check if the file extension is allowed(IF NEEDED ADD MORE EXT FOR NOW ONLY CSV TXT)."""
    ALLOWED_EXTENSIONS = {'csv', 'txt'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5500, debug=True)