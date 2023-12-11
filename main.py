import numpy as np
from fastapi import FastAPI, Query
from typing import List
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

def initial_feasible_basic_solution(grid, supply, demand):
    startR, startC = 0, 0
    ans = 0

    while startR < len(supply) and startC < len(demand):
        if supply[startR] <= demand[startC]:
            ans += supply[startR] * grid[startR, startC]
            demand[startC] -= supply[startR]
            startR += 1
        else:
            ans += demand[startC] * grid[startR, startC]
            supply[startR] -= demand[startC]
            startC += 1

    return ans

# Example usage:
# grid = np.array([[3, 1, 7, 4], [2, 6, 5, 9], [8, 3, 3, 2]])
# supply = np.array([300, 400, 500])
# demand = np.array([250, 350, 400, 200])

# result = initial_feasible_basic_solution(grid, supply, demand)
# print("The initial feasible basic solution is", result)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/calculate")
def Calculate(grid1: List[int] = Query(...), grid2: List[int] = Query(...), grid3: List[int] = Query(...), supply: List[int] = Query(...), demand: List[int] = Query(...)):

    grid = np.array([grid1, grid2, grid3], dtype=int)  # Convert to NumPy array with integer type
    supply = np.array(supply, dtype=int)
    demand = np.array(demand, dtype=int)

    result = initial_feasible_basic_solution(grid, supply, demand)

    return {
            "grid":grid.tolist(),
            "supply":supply.tolist(),
            "demand":demand.tolist(),
            "result": result.tolist(),
            }  # Convert NumPy integer to regular Python integer

@app.get("/gui", response_class=HTMLResponse)
def GUI():
    return """
<!DOCTYPE html>
<html lang="en">

<head>
    <!-- Meta tags for character set and viewport -->
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FastAPI Calculator</title>
    <!-- Include Tailwind CSS -->
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
</head>

<body class="bg-gray-800 text-white">

    <div class="container mx-auto p-4">

        <!-- Title -->
        <h1 class="text-4xl mb-8">FastAPI Calculator</h1>

        <!-- Calculator Form -->
        <form id="calcForm" class="mb-8">

<!-- Row 1 Input Fields -->
<div class="mb-4 grid grid-cols-4 gap-4">
    <label for="grid1" class="sr-only">Row 1:</label>
    <input type="number" name="grid1" class="w-full p-2 bg-gray-700 text-white" placeholder="Enter value for Column 1" required>
    <input type="number" name="grid1" class="w-full p-2 bg-gray-700 text-white" placeholder="Enter value for Column 2" required>
    <input type="number" name="grid1" class="w-full p-2 bg-gray-700 text-white" placeholder="Enter value for Column 3" required>
    <input type="number" name="grid1" class="w-full p-2 bg-gray-700 text-white" placeholder="Enter value for Column 4" required>
</div>

<!-- Row 2 Input Fields -->
<div class="mb-4 grid grid-cols-4 gap-4">
    <label for="grid2" class="sr-only">Row 2:</label>
    <input type="number" name="grid2" class="w-full p-2 bg-gray-700 text-white" placeholder="Enter value for Column 1" required>
    <input type="number" name="grid2" class="w-full p-2 bg-gray-700 text-white" placeholder="Enter value for Column 2" required>
    <input type="number" name="grid2" class="w-full p-2 bg-gray-700 text-white" placeholder="Enter value for Column 3" required>
    <input type="number" name="grid2" class="w-full p-2 bg-gray-700 text-white" placeholder="Enter value for Column 4" required>
</div>

<!-- Row 3 Input Fields -->
<div class="mb-4 grid grid-cols-4 gap-4">
    <label for="grid3" class="sr-only">Row 3:</label>
    <input type="number" name="grid3" class="w-full p-2 bg-gray-700 text-white" placeholder="Enter value for Column 1" required>
    <input type="number" name="grid3" class="w-full p-2 bg-gray-700 text-white" placeholder="Enter value for Column 2" required>
    <input type="number" name="grid3" class="w-full p-2 bg-gray-700 text-white" placeholder="Enter value for Column 3" required>
    <input type="number" name="grid3" class="w-full p-2 bg-gray-700 text-white" placeholder="Enter value for Column 4" required>
</div>

<!-- Supply Input Fields -->
<div class="mb-4 grid grid-cols-3 gap-4">
    <label for="supply" class="sr-only">Supply:</label>
    <input type="number" name="supply" class="w-full p-2 bg-gray-700 text-white" placeholder="Enter supply for Column 1" required>
    <input type="number" name="supply" class="w-full p-2 bg-gray-700 text-white" placeholder="Enter supply for Column 2" required>
    <input type="number" name="supply" class="w-full p-2 bg-gray-700 text-white" placeholder="Enter supply for Column 3" required>
</div>

<!-- Demand Input Fields -->
<div class="mb-4 grid grid-cols-4 gap-4">
    <label for="demand" class="sr-only">Demand:</label>
    <input type="number" name="demand" class="w-full p-2 bg-gray-700 text-white" placeholder="Enter demand for Column 1" required>
    <input type="number" name="demand" class="w-full p-2 bg-gray-700 text-white" placeholder="Enter demand for Column 2" required>
    <input type="number" name="demand" class="w-full p-2 bg-gray-700 text-white" placeholder="Enter demand for Column 3" required>
    <input type="number" name="demand" class="w-full p-2 bg-gray-700 text-white" placeholder="Enter demand for Column 4" required>
</div>

            <!-- Calculate Button -->
            <button type="button" onclick="calculate()"
                class="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-700 focus:outline-none focus:shadow-outline-blue active:bg-blue-800">
                Calculate
            </button>
        </form>

        <!-- Result Display -->
        <div id="result" class="text-xl"></div>

    </div>

    <!-- JavaScript for Calculation -->
    <script>
        async function calculate() {
            // Collect input values for each row and supply/demand
            const grid1 = Array.from(document.getElementsByName('grid1'), e => e.value).join('&grid1=');
            const grid2 = Array.from(document.getElementsByName('grid2'), e => e.value).join('&grid2=');
            const grid3 = Array.from(document.getElementsByName('grid3'), e => e.value).join('&grid3=');

            const supply = Array.from(document.getElementsByName('supply'), e => e.value).join('&supply=');
            const demand = Array.from(document.getElementsByName('demand'), e => e.value).join('&demand=');

            // Construct the URL for the calculation
            const url = `/calculate?grid1=${grid1}&grid2=${grid2}&grid3=${grid3}&supply=${supply}&demand=${demand}`;

            // Fetch data from the server and update the result
            const response = await fetch(url);
            const result = await response.json();

            document.getElementById("result").innerText = `Result: ${result.result}`;
        }
    </script>

</body>

</html>

"""