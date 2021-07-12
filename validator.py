import opentest
import os
import sys

def read_ints(s):
    return [int(i) for i in s.split(' ')]

def read_output(output_dir, test_num):
  path = output_dir + "/test_" + str(test_num) + ".out"
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
    b, s, r, m, cap, rs, slots, dist, p, serves, d = opentest.open_test(input_dir+"/"+test_file)
    
    #Read output and make sure it's in the right format
    if not os.path.isfile(output_dir + "test_" + str(test_num) + ".out"):
      print('Missing test: '+ str(test_num))
      missing_tests += 1
      continue
    matchings, output = read_output(output_dir, test_num)

    if len(output) != matchings:
      print('Error in test '+str(test_num)+"invalid number of matchings")
      print("Expected: " + str(matchings), 'Found: '+str(len(output)))
      continue
  
    #Apply constraints on output
    
    #Domain constraint  
    for matching in output:
      request = matching[0]
      branch = matching[1]
      slot = matching[2]
      counter = matching[3]
      
      if not(request >= 1 and request <= r):
        print('Error in test '+str(test_num)+" Matching request no. "+ str(request)+" request number is out of range!")
        continue
      
      if not( branch >=1 and branch <= b):
        print('Error in test '+str(test_num)+" Matching request no. "+ str(request)+" branch number is out of range!")
        continue
      
      if not(counter >= 1 and counter <= cap[branch - 1]):
        print('Error in test '+str(test_num)+" Matching request no. "+ str(request)+" counter number does not exist in this branch")
        continue
      
      if not(dist[request-1][branch-1] <= d):
        print('Error in test '+str(test_num)+ " Matching request no. "+ str(request)+ " exceeds the max distance")
        continue
      
      if not(serves[branch - 1][counter - 1][int(rs[request -1 ])] == 1):
        print('Error in test '+str(test_num)+ " Matching request no. "+ str(request)+ " the counter in the branch does not serve the matched service")
        continue
      
      if not(slots[int(rs[request - 1])][branch - 1] + slot -1 <= s[branch - 1]) :
        print('Error in test '+str(test_num)+ " Matching request no. "+ str(request)+ " slots needed for matching exceed working hours")
        continue
      
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
  