from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from connection import Connection
from databaseStructure import CreatingDatabaseStructure

API_CLIENT = '/api/client'

Connection().connect()

CreatingDatabaseStructure.create_structure()