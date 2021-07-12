import opentest
import os
import sys

def read_ints(s):
    return [int(i) for i in s.split(' ')]

def read_output(test_num):
  path = "./testset_" + str(1) + "_output" + "/test_" + str(test_num) + ".out"
  f = open(path, "r")
  matchings = int(f.readline()[0])
  output = []
  for i in range(matchings):
    output.append(read_ints(f.readline().rstrip(' \n')))  
  return  matchings, output

if __name__ == '__main__':
  input_dir = sys.argv[1]
  output_dir = sys.argv[2]
  
  total_tests, passed_tests, missing_tests = 0, 0, 0
  for test_file in sorted(os.listdir(input_dir), key = lambda x: int(x.split("_")[1].split(".")[0])):
    test_num = int(test_file.split("_")[1].split(".")[0])
    
    #Read input
    b, s, r, m, cap, rs, slots, dist, p, serves, d = opentest.open_test(test_num)
    
    #Read output and make sure it's in the right format
    if not os.path.isfile(output_dir + "test_" + str(test_num) + ".out"):
      print('Missing test: '+ str(test_num))
      missing_tests += 1
      continue
    matchings, output = read_output(test_num)

    if len(output) != matchings:
      print('Error in test '+str(test_num)+"invalid number of matchings")
      print("Expected: " + str(matchings), 'Found: '+str(len(output)))
      continue
  
    #Apply constraints on output
    
    #Domain constraint  
    error = False
    falsy_matches = []
    for matching in output:
      request = matching[0]
      branch = matching[1]
      slot = matching[2]
      counter = matching[3]
      
      if not (request >= 1 and request <= r \
        and branch >=1 and branch <= b \
        and slot >= 1 and slot <= s[branch - 1] \
        and counter >= 1 and counter <= cap[branch - 1] \
        and dist[request-1][branch-1] <= d \
        and serves[branch - 1][counter - 1][int(rs[request -1 ])] == 1 \
        and slots[int(rs[request - 1])][branch - 1] + slot -1 <= s[branch - 1]) :
            falsy_matches.append(request)
            error = True
            break
    if error: 
      print('Error in test '+str(test_num)+" invalid variable domain in matching request no." + str(falsy_matches))
    #Each customer is handled at most once
    requests = [row[0] for row in output]
    branches = [row[1] for row in output]
    slots = [row[2] for row in output]
    counters = [row[3] for row in output]
    
    resquests_set = set(requests)
    if len(requests) != len(resquests_set):
      print('Error in test '+str(test_num)+' A request was handled twice')
      continue
    
    #No two requests are being handled at the same counter at the same time
    for matching in output:
      request1 = matching[0]
      branch1 = matching[1]
      slot1 = matching[2]
      counter1 = matching[3]
      for other_matching in output:
        request2 = other_matching[0]
        branch2 = other_matching[1]
        slot2 = other_matching[2]
        counter2 = other_matching[3]
        if request1 != request2:
          if (branch1 == branch2 and slot1 == slot2 and counter1 == counter2):
            print('Error in test '+str(test_num)+' Two requests are being handled at the same counter at the same time')
            continue
        
        
      
    
    
    
    #No two requests are being handled at the same counter twice

    
    passed_tests += 1
  failed_tests = total_tests - passed_tests - missing_tests
  print('-----------------------')
  print(passed_tests)  
  