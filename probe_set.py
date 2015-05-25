#select * from description, detection where description.detection_id=detection.id and x<753 and y>121 and h>30;

#select * from description, detection where description.detection_id=detection.id and not(x<753 and y>121) and h>30;