# Object Detection Toolkit
Repository for processing targets in object detection. Usage for custom datasets. 

`TODO: Draw ground truths, K-means`

## Requirements
```
pip install -U -r requirements.txt
```

## Analysis targets
Support for the following bounding box formats:
### Format XML - Pascal VOC
```txt
datasets/
    -JPEGImages-{train_set_name}/
        -*.jpg
    -JPEGImages-{val_set_name}/
        -*.jpg
    -annotations
        -*.xml
```

```xml
<annotation>
	<folder>VOC2007</folder>
	<filename>000005.jpg</filename>
	<source>
		<database>The VOC2007 Database</database>
	</source>
	<size>
		<width>500</width>
		<height>375</height>
		<depth>3</depth>
	</size>
	<segmented>0</segmented>
	<object>
		<name>chair</name>
		<pose>Rear</pose>
		<truncated>0</truncated>
		<difficult>0</difficult>
		<bndbox>
			<xmin>263</xmin>
			<ymin>211</ymin>
			<xmax>324</xmax>
			<ymax>339</ymax>
		</bndbox>
	</object>
</annotation>
```
Analysis of dataset:
```
python analysis.py -p VOC2007 -f xml -c 32 96 128 256 -figsize 16 -xyxy
```

### Format Json - COCO
```txt
datasets/
    -train_set_name/
        -*.jpg
    -val_set_name/
        -*.jpg
    -annotations
        -instances_{train_set_name}.json
        -instances_{val_set_name}.json
```

```json
// The main block in instances_{sample}.json
{
  "info": info,
  "licenses": [licenses],
  "categories": [category],
  "images": [image],
  "annotations": [annotation]
}

// Images block
"images": [
  {
    "id": 1,
    "width": 512,
    "height": 512,
    "file_name": "1.jpg",
    "date_captured": "2020-04-14 01:45:18.567975",
    "license": 1
  }
  {
    "id": 2,
    "width": 512,
    "height": 512,
    "file_name": "2.jpg",
    "date_captured": "2020-04-14 01:46:19.732156",
    "license": 1
  }
]

// Annotations block
"annotations": [
  {
    "id": 5,
    "image_id": 1,
    "category_id": 2,
    "iscrowd": 0,
    "area": 15376.0,
    "bbox": [244.0, 242.0, 124.0, 124.0],
    "segmentation": [[244.0, 242.0, 368.0, 242.0, 368.0, 366.0, 244.0, 366.0]]
   }
]
```

Analysis of dataset:
```
python analysis.py -p COCO -f json -c 32 96 128 256 -figsize 16
```
<img src="/img/pascal2007.jpg" alt="drawing" width="550"/>
