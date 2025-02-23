import pandas as pd
from pulp import LpMinimize, LpProblem, LpVariable, lpSum

def run_optimization(file_path):
    try:
        # Step 1: Read Excel File
        df = pd.read_excel(file_path)

        # Step 2: Define Lot Names
        lot_names = [
            "LOT-1 TNSO", "LOT-2 TAPSO", "LOT-3 BSO", "LOT-4 UPSO-II", "LOT-5 IOAOD", 
            "LOT-6 KASO", "LOT-7 UPSO-I", "LOT-8 MSO", "LOT-9 GSO", "LOT-10 RSO",
            "LOT-11 PSO", "LOT-12 DSO", "LOT-13 KESO", "LOT-14 MPSO", "LOT-15 OSO", "LOT-16 WBSO"
        ]

        # Step 3: Update Column Names
        df.columns = ["Bidder ID"] + lot_names + ["Capacity", "Turnover Capacity"]

        # Step 4: Extract Data
        bidders = df["Bidder ID"].tolist()
        capacities = dict(zip(df["Bidder ID"], df["Capacity"]))
        turnover_capacities = dict(zip(df["Bidder ID"], df["Turnover Capacity"]))

        # Step 5: Extract Valid Bids
        bids = []
        for _, row in df.iterrows():
            bidder = row["Bidder ID"]
            for lot in lot_names:
                cost = row[lot]
                if pd.notna(cost) and cost != "-":
                    bids.append((bidder, lot, float(cost)))  # Store as (bidder, lot, cost)

        # Step 6: Define Decision Variables
        x = {(i, j): LpVariable(f"x_{i}_{j}", cat="Binary") for (i, j, _) in bids}

        # Step 7: Define Optimization Problem
        problem = LpProblem("Minimize_Assignment_Cost", LpMinimize)

        # Objective Function: Minimize Total Cost
        problem += lpSum(cost * x[i, j] for (i, j, cost) in bids)

        # Constraint: Each Lot Must Be Assigned to Exactly One Bidder
        for j in lot_names:
            problem += lpSum(x[i, j] for i in bidders if (i, j) in x) == 1

        # Constraint: Each Bidder Cannot Exceed Capacity
        for i in bidders:
            problem += lpSum(x[i, j] for j in lot_names if (i, j) in x) <= capacities.get(i, 0)

        # Constraint: Each Bidder Cannot Exceed Turnover Capacity (NEW)
        for i in bidders:
            total_turnover = lpSum(cost * x[i, j] for (bidder, j, cost) in bids if bidder == i)
            problem += total_turnover <= turnover_capacities.get(i, float("inf"))  # If missing, assume no limit

        # Step 8: Solve the Problem
        problem.solve()

        # Step 9: Process Results
        bids_dict = {(i, j): cost for (i, j, cost) in bids}
        assignments = []

        for (i, j) in x:
            if x[i, j].value() == 1:
                assignments.append({"bidder": i, "lot": j, "cost": bids_dict[(i, j)]})

        return {"assignments": assignments}

    except Exception as e:
        return {"error": str(e)}
