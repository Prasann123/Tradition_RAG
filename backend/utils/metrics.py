import time
from functools import wraps

# A simple decorator for timing functions
def time_agent_node(func):
    @wraps(func)
    def wrapper(state):
        start_time = time.time()
        # Run the original agent function
        result_state = func(state)
        end_time = time.time()
        
        duration = end_time - start_time
        print(f"--- METRIC: Node '{func.__name__}' took {duration:.2f} seconds. ---")

        
        return result_state
    return wrapper