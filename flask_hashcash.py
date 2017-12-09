from functools import wraps
from flask import request, abort, session, jsonify, make_response
from string import hexdigits

import hashlib, time, random

def _generate_puzzle():
	return ''.join(random.choice(hexdigits) for _ in range(25)) 

def _wrong_solution_response():
	# you can do things here like ban user for some time
	# also consider saving time of puzzle generation and limit generations/sec per user
	return make_response('Wrong hashcash solution')

# main decorator
def validate_work(difficulty = 5,wrong_solution_response=_wrong_solution_response,\
				  generate_puzzle = _generate_puzzle):
	def decorator(f):
		@wraps(f)
		def decorated_function(*args, **kwargs):

			if 'hashcash_puzzle' not in session:
				# in case user doesn't have puzzle - generate it
				puzzle = generate_puzzle()
				session['hashcash_puzzle'] = puzzle # store in session
				resp = wrong_solution_response()
				resp.set_cookie('hashcash_puzzle', puzzle) # send out as cookie
				return resp

			puzzle = session['hashcash_puzzle']
			solution = request.cookies.get('hashcash_solution', '')

			# verify solution
			plain = '{}{}'.format(puzzle,solution)

			hash = hashlib.new('sha1',plain).digest()
			bin_hash = ''.join([bin(ord(c))[2:].zfill(8) for c in hash]) # convert to binary

			# check that the hash start whith *difficulty* of zeros 
			if bin_hash[:difficulty] != '0' * difficulty:
				resp = wrong_solution_response()
				resp.set_cookie('hashcash_puzzle', puzzle) # resend puzzle. just in case 
				return resp

			# at this point solution is verified 
			resp = f(*args, **kwargs) # endpoint response
			if type(resp) in [str,unicode]:
				resp = make_response(resp)

			# generate new puzzle
			puzzle = generate_puzzle()
			session['hashcash_puzzle'] = puzzle # store in session
			# stuff new puzzle into cookies
			resp.set_cookie('hashcash_puzzle', puzzle)
			resp.set_cookie('hashcash_solution', '', expires=0)
			return resp
		return decorated_function
	return decorator

