# WebP Image Converter

## Description
This project is a Python-based WebP image converter that utilizes a machine learning model (ResNet50) to classify images before applying optimized compression settings. The script identifies whether an image contains people, landscapes, or other objects and adjusts WebP compression parameters accordingly to maintain quality while reducing file size.

## Features
- **Automatic Image Classification**: Uses a pre-trained ResNet50 model to categorize images into "people," "landscape," or "other."
- **Optimized Compression Settings**: Applies different WebP compression parameters based on image type.
- **Batch Conversion**: Converts multiple images at once.
- **Supports Multiple Formats**: Works with JPG, JPEG, PNG, TIFF, and BMP formats.
- **File Size Reduction**: Moves original files to an "originals" folder and saves optimized WebP versions.
- **Windows Batch Script**: Includes a `.bat` file to check dependencies and run the conversion process.

## Installation
### Requirements
- Python 3.x

## Usage
### Running the Converter
#### Python Script (Cross-Platform):
```sh
python webp_converterIN.py
```
#### Windows Batch Script:
Run `webp_converter.bat`, which:
- Checks for Python and dependencies
- Installs missing dependencies if needed
- Executes the Python script

### Output
- Converted WebP images will be saved in the same directory.
- Original images will be moved to the `originals` folder.
- Displays a summary of the compression results.

## Example Output
```
Starting WebP conversion...
Processing: image1.jpg
Detected image type: people
Converted: image1.jpg -> image1.webp
Reduction: 45.2% (2.3MB -> 1.2MB)

Conversion Summary:
Files converted: 10
Total original size: 23.5MB
Total WebP size: 12.1MB
Total reduction: 48.5%
Original files have been moved to the 'originals' folder.
```

## License
This project is open-source under the MIT License.
