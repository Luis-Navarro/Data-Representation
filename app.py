from flask import Flask, jsonify, abort, request

app = Flask(__name__)

records=[{"id":1, "fruit":"orange", "origin":"Spain", "price":2.50},
{"id":2, "fruit":"apple", "origin":"Ireland", "price":1.50},
{"id":3, "fruit":"pineapple", "origin":"Venezuela", "price":3.75},
{"id":4, "fruit":"banana", "origin":"Morocco", "price":1.25}
]
nextId=5

@app.route('/', methods=['GET'])
def index():
    return "<h1>Hello, World!</h1><p>This site is an API as part of Data Representation assignement for Higher Diploma in Data Analysis in GMIT</p><p>Created by Luis Navarro. December 2019</p>"
	
# Get all records
# curl "http://127.0.0.1:5000/records"
@app.route('/records')
def getAll():
	return jsonify(records)

# Get records by Id
# curl "http://127.0.0.1:5000/records/1"
@app.route('/records/<int:id>')
def findfById(id):
	foundFruit= list(filter(lambda b: b['id']==id, records))
	if len(foundFruit)==0:
		return jsonify({}), 204
	return jsonify(foundFruit[0])

# Create new record and append to list
# curl -i -H "Content-Type:application/json" -X POST -d "{\"fruit\":\"mandarina\",\"origin\":\"France\",\"price\":3.20}" http://127.0.0.1:5000/records

@app.route('/records', methods=['POST'])
def create():
	global nextId
	if not request.json:
		abort(400)
	fruit = {
			"id": nextId,
			"fruit": request.json['fruit'],
			"origin": request.json['origin'],
			"price": request.json['price'],
			}
	nextId+=1
	records.append(fruit)
	return jsonify(fruit)
	
# Update exisitng record by allocating and then overwriting
# 	
@app.route('/records/<int:id>', methods=['PUT'])
def update(id):
	foundRecords= list(filter(lambda t:t['id']==id, records))
	if len(foundRecord)==0:
		abort(404)
	foundRecord=foundRecords[0]
	if not request.json:
		abort(400)
	reqJson=request.json
	if 'price' in reqJson and (type(reqJson['price'])!= float or type(reqJson['price'])!= int):
		abort(400)
	if 'fruit' in reqJson:
		foundRecord['fruit']=reqJson['fruit']
	if 'origin' in reqJson:
		foundRecord['origin']=reqJson['origin']
	if 'price' in reqJson:
		foundRecord['price']=reqJson['price']
	return jsonify(foundRecord)


# Delete records
@app.route('/records/<int:id>', methods=['DELETE'])
def delete(id):
	foundRecords= list(filter(lambda t:t['id']==id, records))
	if len(foundRecord)==0:
		abort(404)
	fruit.delete(foundRecord[0])
	return jsonify({"done": True})

if __name__ == '__main__':
    app.run(debug=True)