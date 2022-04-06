from flask import Blueprint, jsonify, request, abort, Response
from datetime import datetime, timedelta
from supabase_client import Client
import requests
import socket


REQUEST_API = Blueprint('request_api', __name__)
ip_url = "https://ifconfig.co/ip"

url= 'https://tlagwlowvabyydvzipai.supabase.co'
key= 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRsYWd3bG93dmFieXlkdnppcGFpIiwicm9sZSI6ImFub24iLCJpYXQiOjE2NDY3NjY2MDksImV4cCI6MTk2MjM0MjYwOX0.jicG5Cyvw7wW7Sw_lkHQVqv6cEogH0YJzR_GrL7HEXM'
supabase = Client( 
	api_url=url,
	api_key=key
)


def make_return(response):
	ip = socket.gethostname()
	data={
		"source_ip":ip,
		"source_name":"orders service",
		"response":response
	}
	return jsonify(data)

def get_blueprint():
    """Return the blueprint for the main app module"""
    return REQUEST_API




@REQUEST_API.route('/orders', methods=['GET', 'POST'])
async def get_records():
    if request.method == 'GET':
        error, result = await(supabase.table("order").limit(30).select("*").query())
        return make_return(result)
    else:
        error, result = await(supabase.table("order").insert([request.get_json()]))
        return make_return(result)


@REQUEST_API.route('/orders/<id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
async def handle_order(id):
    if request.method == "GET":
        error, data = await supabase.table("order").select("*").eq('id',id).query()
        if(error):
            data=error
        return make_return(data)
    elif request.method == "PUT":
        return make_return("ok")
    elif request.method == "DELETE":
        error, data = await supabase.table("order").delete({'id':id})
        
        return make_return(data)
    else:
        return make_return("not ok")
