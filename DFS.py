class State:
    def __init__(self, left_m, left_c, boat, right_m, right_c):
        self.left_m = left_m  # Number of missionaries on the left bank
        self.left_c = left_c  # Number of cannibals on the left bank
        self.boat = boat      # 0 if boat is on the left bank, 1 if on the right bank
        self.right_m = right_m  # Number of missionaries on the right bank
        self.right_c = right_c  # Number of cannibals on the right bank

    def is_valid(self):
        # Check if any bank has negative people or more cannibals than missionaries
        if (self.left_m < 0 or self.left_c < 0 or
            self.right_m < 0 or self.right_c < 0 or
            (self.left_m > 0 and self.left_c > self.left_m) or
            (self.right_m > 0 and self.right_c > self.right_m)):
            return False
        return True

    def is_goal(self):
        return self.left_m == 0 and self.left_c == 0 and self.boat == 0

    def __eq__(self, other):
        return (self.left_m == other.left_m and
                self.left_c == other.left_c and
                self.boat == other.boat and
                self.right_m == other.right_m and
                self.right_c == other.right_c)

    def __hash__(self):
        return hash((self.left_m, self.left_c, self.boat, self.right_m, self.right_c))

def dfs(current_state, visited, path):
    if current_state.is_goal():
        return path  # Return the path to the goal state

    visited.add(current_state)

    # Generate all possible moves
    next_states = get_successors(current_state)
    for next_state in next_states:
        if next_state not in visited:
            result = dfs(next_state, visited, path + [next_state])
            if result:
                return result  # If a solution path is found, return it

    visited.remove(current_state)  # Backtrack
    return None

def get_successors(state):
    successors = []
    if state.boat == 0:  # Boat on the left bank
        # Generate all possible moves from the left to the right
        for dm in range(3):
            for dc in range(3):
                if 1 <= dm + dc <= 2:  # Either one or two people in the boat
                    new_state = State(state.left_m - dm, state.left_c - dc, 1,
                                      state.right_m + dm, state.right_c + dc)
                    if new_state.is_valid():
                        successors.append(new_state)
    else:  # Boat on the right bank
        # Generate all possible moves from the right to the left
        for dm in range(3):
            for dc in range(3):
                if 1 <= dm + dc <= 2:  # Either one or two people in the boat
                    new_state = State(state.left_m + dm, state.left_c + dc, 0,
                                      state.right_m - dm, state.right_c - dc)
                    if new_state.is_valid():
                        successors.append(new_state)
    return successors

def main():
    initial_state = State(3, 3, 0, 0, 0)
    visited = set()
    path = [initial_state]

    solution = dfs(initial_state, visited, path)
    if solution:
        print("Solution found with {} moves:".format(len(solution) - 1))
        for i, state in enumerate(solution):
            if i == 0:
                print("Initial state: {} missionaries, {} cannibals, boat on left side".format(3, 3))
            else:
                missionaries = abs(state.left_m - state.right_m)
                cannibals = abs(state.left_c - state.right_c)
                boat_side = "left" if state.boat == 0 else "right"
                print("Move {}: {} missionaries, {} cannibals, boat on the {} side".format(i, missionaries, cannibals, boat_side))
    else:
        print("No solution found.")

if __name__ == "__main__":
    main()

