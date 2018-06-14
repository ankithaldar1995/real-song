from flask import Flask, request, jsonify
import boto3
import GET_img
import json

app = Flask(__name__)

def get_labels(thumbImg, client):

	labels = []

	if len(thumbImg) == 0:
		return labels

	img_size = GET_img.get_image_from_url(thumbImg)

	try:
		resp = client.detect_labels(Image={'Bytes': img_size}, MinConfidence=60.0)

		for label in resp['Labels']:
			labels.append(label['Name'])

	except Exception as err:
		labels.append("err")
		err = str(err)
		labels.append(err)
		return labels

	return labels

# @app.route("/", methods=["POST"])
def feed(event, context):
    print(event, context)
    data = event["bodyParameters"]

    with open("cre") as file:
        for line in file:
			if line[0] == 'A':
				ACCESS_KEY = line
			else:
				SECRET_KEY = line

	ACCESS_KEY = ACCESS_KEY[:len(ACCESS_KEY) - 1]
	print(ACCESS_KEY, SECRET_KEY)
	client = boto3.client('rekognition', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY, region_name="us-west-2")
	print(ACCESS_KEY, SECRET_KEY, "ASDASDASDAS")

	form = []

	for iterator in range(0, len(data)):

		unit = {}
		mageId = data[iterator]["mageId"]
		thumbImg = data[iterator]["thumbImg"]

		if len(thumbImg) == 0:
			continue
		
		union = []

		for link in thumbImg:
			labels = get_labels(link, client)
			if labels[0] == "err":
				unit["error"] = []
				unit["error"].append(labels[1])
			elif len(union) == 0:
				union = labels
			else:
				for label in labels:
					if label not in union:
						union.append(label)
		
		unit["mageId"] = mageId
		unit["tags"] = union

		form.append(unit)

    response = {
        "statusCode": res.status_code,
        "body": jsonify(form)
    }

    return response


# if __name__ == "__main__":
# 	app.run(debug=True)

# Output
# [
# 	{
#     error: (If occured)
# 		mageID: 
# 		tags: [a, b, c, ...]
# 	}
# 	...
# ]
