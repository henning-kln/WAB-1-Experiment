from analyze_csv import analyze_csv

def main():
    filename = '5/test.csv'
    average_age, average_points = analyze_csv(filename)
    print(f"Durchschnittsalter: {average_age:.2f}")
    print(f"Durchschnittliche Punkte: {average_points:.2f}")

if __name__ == "__main__":
    main()