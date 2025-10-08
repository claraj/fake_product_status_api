import random 

# the totally top secret keys are palindromic numbers at least 10 characters long. 
# generate working keys 

base = [ str(random.randint(0, 9)) for _ in range(10) ]
base_backwards = list(reversed(base))
list_numbers = base + base_backwards

key = ''.join(list_numbers)
print(key)