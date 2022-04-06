from flask import Blueprint, jsonify, request, abort, Response
from datetime import datetime, timedelta
from supabase_client import Client
import requests



REQUEST_API = Blueprint('request_api', __name__)
ip_url = "https://ifconfig.co/ip"


url= 'https://tlagwlowvabyydvzipai.supabase.co'
key= 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRsYWd3bG93dmFieXlkdnppcGFpIiwicm9sZSI6ImFub24iLCJpYXQiOjE2NDY3NjY2MDksImV4cCI6MTk2MjM0MjYwOX0.jicG5Cyvw7wW7Sw_lkHQVqv6cEogH0YJzR_GrL7HEXM'
supabase = Client( 
	api_url=url,
	api_key=key
)


def make_return(response):
	ip = requests.get(ip_url).text
	data = {
		"source_ip":ip,
		"source_name":"delivery Service ",
		"response":response
	}
	return jsonify(data)

def get_blueprint():
    """Return the blueprint for the main app module"""
    return REQUEST_API



@REQUEST_API.route('/delivery',methods=['POST','GET'])
async def handle_all_delivery():
    if request.method=="GET":
        error , data = await(supabase.table("delivery").select("*").query())
        return make_return(data)
    elif request.method=="POST":
        error, result = await(supabase.table("delivery").insert([request.get_json()]))
        return make_return(result)

@REQUEST_API.route('/loyalty',methods=['GET'])
async def get_loyalty():
    error, data = await(supabase.table("loyalty").select("*").query())
    return make_return(data)

@REQUEST_API.route("/loyalty/<uid>", methods=["PUT", "GET"])
async def handle_loyalty(uid):
    if request.method == "GET":
        error , data = await(supabase.table("loyalty").select("*").eq('username',uid).query())
        return make_return(data)
    else:
        return make_return("ok")
