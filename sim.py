import tongits

def main():
    ### Just a reminder of the tests:

    # p1riskLevel = 0 with 9 testcases (100 simulations each testcase)
    # p2riskLevel = 0.5 with 9 testcases (100 simulations each testcase)
    # p3riskLevel = 1 with 9 testcases (100 simulations each testcase)
    
    # 2700 simulations total

    i = 0
    for p1riskLevel in [0, 0.5, 1]:
        for p2riskLevel in [0, 0.5, 1]:
            for p3riskLevel in [0, 0.5, 1]:
                for i in range(100):
                    winner = tongits.RunTongitsSim(p1riskLevel, p2riskLevel, p3riskLevel)
                    print("Test", i + 1, "with Risk Levels", [p1riskLevel, p2riskLevel, p3riskLevel], "Winner is player", winner)

if __name__ == "__main__":
    main()