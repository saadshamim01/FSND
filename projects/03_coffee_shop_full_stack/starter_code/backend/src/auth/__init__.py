

#@app.route('/drinks', methods = ['POST'])
##@requires_auth('post:drinks')
#def create_drinks(self):
#    body = dict(request.form or request.json or request.data)
#    print(body)
#    new_title = body.get('title', None)
#    print(new_title)
#    new_recipe = body.get('recipe', None)
#    print(new_recipe)
#
#    try:
#        drink = Drink(title = new_title, recipe = new_recipe)
#        print(drink)
#        drink.insert()
#        return jsonify({"success": True,
#                        "drinks": drink.long()
#                        }), 200
#    except Exception as e:
#        print(e)
#        abort(422)

#@app.route("/drinks", methods=['POST'])
##@requires_auth("post:drinks")
##def add_drink(token):
#def create_drinks():
#
#    new_title = body.get('title', None)
#    new_recipe = body.get('recipe', None)
#    if request.data:
#    #if dict(request.form or request.json or request.data):
#        body = request.get_json()
#        #new_drink_data = dict(request.form or request.json or request.data)
#        new_drink = Drink(title=new_drink_data['title'], recipe=json.dumps(new_drink_data['recipe']))
#        Drink.insert(new_drink)
#        return jsonify({
#            "success": True,
#            "drink": new_drink.id
#        })
#@app.route("/drinks", methods=['POST'])
#def create_drinks():
#    if dict(request.form or request.json or request.data):
#        new_drink_data = json.loads(request.data.decode('utf-8'))
#        new_drink = Drink(title=new_drink_data['title'], recipe=json.dumps(new_drink_data['recipe']))
#        Drink.insert(new_drink)
#        return jsonify({
#            "success": True,
#            "drink": [new_drink.id]
#        })

#new_drink_data = dict(request.form or request.json or request.data)
        #new_drink = Drink(title= new_title, recipe=json.dumps(new_recipe))


#######################################################
#@app.route('/drinks/<int:id>', methods=['PATCH'])
#
#def update_drink(id):
#    body = request.get_json()
#    new_title = body.get('title', None)
#    new_recipe = body.get('recipe', None)
#    drink = Drink.query.filter(Drink.id == id).one_or_none()
#
#    if drink is None:
#        abort(404)
#    try:
#        #drink.title = new_title
#        if 'title' in body:
#            drink.title=new_title,
#            drink.recipe=json.dumps(new_recipe)
#            drink.update()
#            drinks = Drink.query.order_by(Drink.id.desc()).all()
#            drinks = [drink.long() for drink in drinks]
#            return jsonify({
#                            'success': True,
#                            'drinks': drink.long()
#                            }), 200
##        else:
##            print('Title or recipe not found.')
##            abort(404)
#    except:
#        abort(422)
