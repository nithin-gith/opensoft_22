from flask import Blueprint, jsonify, request, abort, Response
from datetime import datetime, timedelta
from supabase_client import Client
import prometheus_client
import requests
import requests

ip_url = "https://ifconfig.co/ip"



REQUEST_API = Blueprint('request_api', __name__)

url= 'https://tlagwlowvabyydvzipai.supabase.co'
key= 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRsYWd3bG93dmFieXlkdnppcGFpIiwicm9sZSI6ImFub24iLCJpYXQiOjE2NDY3NjY2MDksImV4cCI6MTk2MjM0MjYwOX0.jicG5Cyvw7wW7Sw_lkHQVqv6cEogH0YJzR_GrL7HEXM'
supabase = Client( 
	api_url=url,
	api_key=key
)


def make_return(response):
    ip = requests.get(ip_url).text
    data ={
            "source_ip":ip,
            "source_name":"datacenter",
            "response":response
            }
    return data


def get_blueprint():
    """Return the blueprint for the main app module"""
    return REQUEST_API


ONE_ORDER = {
    'title': u'Good Book',
    'email': u'testuser1@test.com',
    'timestamp': (datetime.today() - timedelta(1)).timestamp()
}




@REQUEST_API.route('/orders', methods=['GET', 'POST'])
async def get_records():
    if request.method == 'GET':
        error, result = await(supabase.table("order").limit(30).select("*").query())
        return jsonify(make_return(result))
    else:
        error, result = await(supabase.table("order").insert([request.get_json()]))
        return jsonify(make_return(result))


@REQUEST_API.route('/orders/<id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
async def handle_order(id):
    if request.method == "GET":
        error, data = await supabase.table("order").select("*").eq('id',id).query()
        if(error):
            data=error
        return jsonify(make_return(data))
    elif request.method == "PUT":
        return jsonify(make_return("ok"))
    elif request.method == "DELETE":
        error, data = await supabase.table("order").delete({'id':id})
        
        return jsonify(make_return(data))
    else:
        return jsonify(make_return("not ok"))

@REQUEST_API.route('/user',methods=['POST'])
def handle_create_user():
    if request.method=="POST":
        return supabase.table("user").insert(request.get_json())


@REQUEST_API.route('/user/login',methods=['GET'])
def handle_login():
    # cur.execute('SELECT version()')
    if request.method=="POST":
        return "ok"

@REQUEST_API.route('/user/logout',methods=['GET'])
def handle_logout():
    if request.method=="POST":
        return "ok"


@REQUEST_API.route('/user/<userid>',methods=['GET', 'PUT', 'DELETE'])
async def handle_user(userid):
    if request.method=="GET":
        error, data = await (supabase.table("user").select("*").eq('id',id).query())
        return jsonify(data)
    elif request.method=="PUT":
        return "ok"
    elif request.method=="DELETE":
        error, data = await supabase.table("user").delete({'id':id})
        return jsonify(data)



@REQUEST_API.route('/delivery',methods=['POST','GET'])
async def handle_all_delivery():
    if request.method=="GET":
        error , data = await(supabase.table("delivery").select("*").query())
        return jsonify(make_return(data))
    elif request.method=="POST":
        error, result = await(supabase.table("delivery").insert([request.get_json()]))
        return jsonify(make_return(result))


@REQUEST_API.route('/delivery/<deliveryid>',methods=['GET', 'PUT', 'DELETE'])
async def handle_delivery(deliveryid):
    if request.method=="GET":
        error, data = await (supabase.table("delivery").select("*").eq('id',deliveryid).query())
        return jsonify(make_return(data))
    elif request.method=="PUT":
        return jsonify(make_return("ok"))
    elif request.method=="DELETE":
        error, data = await supabase.table("delivery").delete({'id':deliveryid})
        return jsonify(make_return(data))

@REQUEST_API.route('/loyalty',methods=['GET'])
async def get_loyalty():
    error, data = await(supabase.table("loyalty").select("*").query())
    return jsonify(make_return(data))

@REQUEST_API.route("/loyalty/<uid>", methods=["PUT", "GET"])
async def handle_loyalty(uid):
    if request.method == "GET":
        error , data = await(supabase.table("loyalty").select("*").eq('username',uid).query())
        return jsonify(make_return(data))
    else:
        return jsonify("ok")

CONTENT_TYPE_LATEST = str('text/plain; version=0.0.4; charset=utf-8')

@REQUEST_API.route('/metrics', methods=['GET'])
async def metrics():
    return Response(prometheus_client.generate_latest(), mimetype=CONTENT_TYPE_LATEST)
