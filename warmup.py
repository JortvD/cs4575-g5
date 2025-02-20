import random
import math
import concurrent.futures
import os
import time

class Warmup:
	def calculate_pi_batch(self, batch_size, seed):
		inside_circle = 0
		random.seed(seed)
		for _ in range(batch_size):
			x = random.random()
			y = random.random()
			if math.sqrt(x**2 + y**2) <= 1.0:
				inside_circle += 1
		return inside_circle

	def run(self, index=0):
		total_points = 0
		inside_circle = 0
		batch_size = 20_000_000
		num_threads = os.cpu_count()
		n_batches = num_threads * 200
		start_time = time.time()
		i = 0
		with concurrent.futures.ProcessPoolExecutor(max_workers=num_threads) as executor:
			futures = [executor.submit(self.calculate_pi_batch, batch_size, n_batches * index + i) for i in range(n_batches)]
			for future in concurrent.futures.as_completed(futures):
				inside_circle += future.result()
				total_points += batch_size
				pi_estimate = (inside_circle / total_points) * 4
				i+=1
				if i % num_threads == 0:
					end_time = time.time()
					print(f'Current estimate of Pi: {pi_estimate} ({future.result()} of {inside_circle}, {batch_size} of {total_points})')
					print(f'Time elapsed: {end_time - start_time} seconds')
					print(f'Performance: {total_points / (end_time - start_time)} points per second')


if __name__ == '__main__':
	Warmup().run()
	print("Warmup done")