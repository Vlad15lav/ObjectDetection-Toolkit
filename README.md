# Object Detection Toolkit
Repository for processing targets in object detection. Usage for custom datasets. 

`TODO: K-means`

## Requirements
```
pip install -U -r requirements.txt
```
If you are using a custom dataset, pay attention to the format of the bounding boxes.</br>
For Pascal VOC is *[x left top, y left top, x bottom right, y bottom right]* `-xyxy`
and for COCO it is *[x left top, y left top, width, height]*, this information is below.</br>
More details - ` python <script>.py --help `

## Analysis Targets
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
    -ImageSets/
        -Layout
	-Main
	    -{train_set_name}.txt
	    -{val_set_name}.txt
	-Segmentation
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
python analysis.py -p VOC2007 -s train -f xml -c 32 96 128 256 -figsize 16 -xyxy
```

### Format Json - COCO
```txt
datasets/
    -train_set_name/
        -*.jpg
    -val_set_name/
        -*.jpg
    -annotations/
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
python analysis.py -p COCO -s train2014 -f json -c 32 96 128 256 -figsize 16
```
#### Pascal VOC 2007 Example
<img src="/img/pascal2007.jpg" alt="drawing" width="600"/>

## Drawing ground truths
```
python drawbox.py -p VOC2007 -s train -f xml -xyxy
```
<img src="/img/pascalgt.png" alt="drawing" width="600"/>

## Convert formats
Convert Pascal VOC format to COCO Json format
```
python convert.py -p VOC2007 -s train -f xml -wformat json -config config/pascal2007 -xyxy
```
