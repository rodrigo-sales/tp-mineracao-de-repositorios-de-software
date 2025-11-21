from analyzer.coupling_analyzer import analyze_coupling


def test_analyze_coupling_empty():
	source_code = ""
	assert analyze_coupling(source_code) == 0.0

def test_analyze_coupling_stdlib_only():
	source_code = """
			import os
			import sys
			import re
			from datetime import datetime

			def foo():
			print(os.getcwd())
		"""
	score = analyze_coupling(source_code)
	assert score < 1.0 

def test_analyze_coupling_external_imports():
	source_code = """
			import numpy as np
			import pandas
			from flask import Flask
		"""
	score = analyze_coupling(source_code)
	assert score >= 1.5

def test_analyze_coupling_internal_dependencies():
	source_code = """
			def helper_func():
			pass

			class MyClass:
			pass

			def main():
			helper_func()
			helper_func()  # Segunda chamada conta como dependência
			obj = MyClass()
			obj2 = MyClass() # Segunda chamada conta como dependência
		"""
	score = analyze_coupling(source_code)
	assert score > 0.0

def test_analyze_coupling_max_cap():
	lots_of_imports = "\n".join([f"import lib_{i}" for i in range(50)])
	score = analyze_coupling(lots_of_imports)
	assert score == 10.0