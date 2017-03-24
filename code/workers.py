#!/usr/bin/env python
#-*- coding: utf8 -*-
"""
module_name, package_name, ClassName, 
method_name, ExceptionName, function_name, 
GLOBAL_CONSTANT_NAME, global_var_name, 
instance_var_name, function_parameter_name, 
local_var_name
"""
from Queue import *
from threading import Thread
import time

class Worker(Thread):
	def __init__(self, tasks):
		Thread.__init__(self)
		self.tasks = tasks
		self.daemon = True
		self.start()

	def run(self):
		while True:
			func, args, kargs = self.tasks.get()
			try:
				func(*args, **kargs)
				#time.sleep(.1)
			except Exception as e:
				print(e)
			finally:
				self.tasks.task_done()

class ThreadPool:
	def __init__(self, num_threads):
		self.tasks = Queue(num_threads)
		self.workers = [Worker(self.tasks) for _ in range(num_threads)]

	def add_task(self, func, *args, **kargs):
		self.tasks.put((func, args, kargs))

	def map(self, func, args_list):
		for args in args_list:
			self.add_task(func, *args)

	def wait_completion(self):
		self.tasks.join()
