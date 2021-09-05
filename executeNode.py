import time
import createSegment as cs

path = ".\segmentApi\gmc_node"
target_path = 'segmentApi\segmentApi_template.json'

start = time.time()
cs.getSegment(path, target_path)
print("Time took: ", time.time() - start)