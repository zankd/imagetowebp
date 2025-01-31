from PIL import Image
import os
import shutil
import torch
from torchvision import transforms, models
import json

def get_file_size_mb(file_path):
    return os.path.getsize(file_path) / (1024 * 1024)

def load_ml_model():
    try:
        print("Loading ResNet50 model...")
        model = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
        model.eval()
        
        # Load ImageNet labels
        labels_path = os.path.join(os.path.dirname(__file__), 'imagenet_labels.json')
        if not os.path.exists(labels_path):
            # Simplified list of common labels
            labels = {
                0: "person",
                1: "landscape",
                2: "animal",
                3: "object",
                4: "building"
            }
        else:
            with open(labels_path, 'r', encoding='utf-8') as f:
                labels = json.load(f)
        
        return model, labels
    except Exception as e:
        print(f"Error loading model: {str(e)}")
        raise

def get_image_type(model, labels, img):
    try:
        # Prepare image for the model
        preprocess = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        
        # Convert to RGB if needed
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        input_tensor = preprocess(img)
        input_batch = input_tensor.unsqueeze(0)
        
        with torch.no_grad():
            output = model(input_batch)
            probabilities = torch.nn.functional.softmax(output[0], dim=0)
        
        # Get top 5 predictions
        _, indices = torch.sort(probabilities, descending=True)
        top_5_indices = indices[:5].tolist()
        
        # Categories for compression type
        landscape_keywords = {'landscape', 'mountain', 'sky', 'sea', 'beach', 'forest', 'nature'}
        person_keywords = {'person', 'face', 'portrait', 'people', 'human'}
        
        # Analyze predictions
        for idx in top_5_indices:
            pred = str(labels.get(str(idx), "")).lower()
            if any(keyword in pred for keyword in person_keywords):
                return "people"
            if any(keyword in pred for keyword in landscape_keywords):
                return "landscape"
        
        return "other"
    except Exception as e:
        print(f"Error analyzing image: {str(e)}")
        return "other"  # default value in case of error

def get_compression_settings(image_type):
    settings = {
        "people": {"quality": 90, "method": 6, "sharp_yuv": True},
        "landscape": {"quality": 75, "method": 4},
        "other": {"quality": 82, "method": 5}
    }
    return settings.get(image_type, settings["other"])

def convert_to_webp():
    try:
        print("Starting conversion process...")
        model, labels = load_ml_model()
        
        files = [f for f in os.listdir('.') if os.path.isfile(f)]
        supported_formats = {'.jpg', '.jpeg', '.png', '.tiff', '.bmp'}
        converted = 0
        total_original_size = 0
        total_webp_size = 0
        
        originals_dir = 'originals'
        if not os.path.exists(originals_dir):
            os.makedirs(originals_dir)
        
        for file in files:
            name, ext = os.path.splitext(file)
            ext = ext.lower()
            
            if ext in supported_formats:
                try:
                    print(f"\nProcessing: {file}")
                    original_size = get_file_size_mb(file)
                    total_original_size += original_size
                    
                    img = Image.open(file)
                    
                    # Detect image type and get settings
                    image_type = get_image_type(model, labels, img)
                    print(f"Detected image type: {image_type}")
                    settings = get_compression_settings(image_type)
                    
                    webp_filename = f"{name}.webp"
                    img.save(webp_filename, 'WebP', **settings)
                    
                    webp_size = get_file_size_mb(webp_filename)
                    total_webp_size += webp_size
                    
                    # Move original to originals folder
                    shutil.move(file, os.path.join(originals_dir, file))
                    
                    converted += 1
                    reduction = ((original_size - webp_size) / original_size) * 100
                    print(f"Converted: {file} -> {webp_filename}")
                    print(f"Reduction: {reduction:.1f}% ({original_size:.1f}MB -> {webp_size:.1f}MB)")
                    
                except Exception as e:
                    print(f"Error processing {file}: {str(e)}")
                    continue
        
        return converted, total_original_size, total_webp_size
    except Exception as e:
        print(f"Error during conversion: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        print("Starting WebP conversion...")
        total_files, original_size, webp_size = convert_to_webp()
        
        if total_files > 0:
            print("\nConversion Summary:")
            print(f"Files converted: {total_files}")
            print(f"Total original size: {original_size:.2f}MB")
            print(f"Total WebP size: {webp_size:.2f}MB")
            print(f"Total reduction: {((original_size - webp_size) / original_size * 100):.1f}%")
            print("\nOriginal files have been moved to the 'originals' folder")
        else:
            print("\nNo images found to convert.")
            print("Supported formats: JPG, JPEG, PNG, TIFF, BMP")
    except Exception as e:
        print(f"\nFatal error: {str(e)}")
        exit(1)
