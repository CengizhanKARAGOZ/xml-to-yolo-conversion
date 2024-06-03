import os
import xml.etree.ElementTree as ET

# Folder paths
input_dir = 'C:\\Users\\cengi\\OneDrive\\Masaüstü\\Oturum_2_Etiketler\\VY2_5'  
output_dir = 'C:\\Users\\cengi\\OneDrive\\Masaüstü\\Last_dt_labels\\VY2_5'  
  
# Create output folders if they don't exist
os.makedirs(output_dir, exist_ok=True)

# List of classes
classes = [""]

# Convert annotations to YOLO format
def convert(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)

# Iterate through all files in the input directory and convert them to YOLO format
for filename in os.listdir(input_dir):
    if not filename.endswith('.xml'):
        continue
    tree = ET.parse(os.path.join(input_dir, filename))
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)
    
    txt_filename = os.path.join(output_dir, filename.replace('.xml', '.txt'))
    with open(txt_filename, 'w') as f:
        for obj in root.iter('object'):
            cls = obj.find('name').text
            if cls not in classes:
                continue
            cls_id = classes.index(cls)
            xmlbox = obj.find('bndbox')
            b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text),
                 float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
            bb = convert((w, h), b)
            f.write(f"{cls_id} {' '.join([str(a) for a in bb])}\n")
