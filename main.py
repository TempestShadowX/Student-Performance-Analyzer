import csv
import matplotlib.pyplot as plt
import os

PASS_MARK = 50
CSV_FILE = "scores.csv"


def load_data(filename):
    students = []
    with open(filename, newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            # calculate average score across all subjects
            subjects = [key for key in row if key != "name"]
            scores = [int(row[subject]) for subject in subjects]
            average = sum(scores) / len(scores)

            students.append({
                "name": row["name"],
                "scores": scores,
                "subjects": subjects,
                "average": round(average, 2)
            })
    return students


def get_summary(students):
    averages = [s["average"] for s in students]

    highest = max(students, key=lambda s: s["average"])
    lowest = min(students, key=lambda s: s["average"])

    passed = [s for s in students if s["average"] >= PASS_MARK]
    failed = [s for s in students if s["average"] < PASS_MARK]

    overall_avg = round(sum(averages) / len(averages), 2)

    return {
        "total": len(students),
        "overall_avg": overall_avg,
        "highest": highest,
        "lowest": lowest,
        "passed": passed,
        "failed": failed
    }


def print_report(students, summary):
    print("=" * 50)
    print("       STUDENT PERFORMANCE REPORT")
    print("=" * 50)

    print(f"\n{'NAME':<20} {'AVERAGE':<10} {'STATUS'}")
    print("-" * 40)
    for s in students:
        status = "PASS" if s["average"] >= PASS_MARK else "FAIL"
        print(f"{s['name']:<20} {s['average']:<10} {status}")

    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)
    print(f"Total Students   : {summary['total']}")
    print(f"Overall Average  : {summary['overall_avg']}")
    print(f"Highest Score    : {summary['highest']['name']} ({summary['highest']['average']})")
    print(f"Lowest Score     : {summary['lowest']['name']} ({summary['lowest']['average']})")
    print(f"Passed           : {len(summary['passed'])} students")
    print(f"Failed           : {len(summary['failed'])} students")
    pass_rate = round((len(summary['passed']) / summary['total']) * 100, 1)
    print(f"Pass Rate        : {pass_rate}%")

    if summary["failed"]:
        print("\nStudents who failed:")
        for s in summary["failed"]:
            print(f"  - {s['name']} ({s['average']})")


def plot_results(students, summary):
    names = [s["name"].split()[0] for s in students]  # first names only so it fits
    averages = [s["average"] for s in students]
    colors = ["#4CAF50" if avg >= PASS_MARK else "#f44336" for avg in averages]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle("Student Performance Analysis", fontsize=14, fontweight="bold")

    # bar chart for individual scores
    bars = ax1.bar(names, averages, color=colors)
    ax1.axhline(y=PASS_MARK, color="orange", linestyle="--", linewidth=1.5, label=f"Pass mark ({PASS_MARK})")
    ax1.set_title("Average Score per Student")
    ax1.set_ylabel("Average Score")
    ax1.set_xlabel("Students")
    ax1.set_ylim(0, 100)
    ax1.tick_params(axis="x", rotation=45)
    ax1.legend()

    # adding avg score labels on top of the bars
    for bar, avg in zip(bars, averages):
        ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
                 str(avg), ha="center", va="bottom", fontsize=7)

    # poe chart
    passed_count = len(summary["passed"])
    failed_count = len(summary["failed"])
    ax2.pie(
        [passed_count, failed_count],
        labels=[f"Passed ({passed_count})", f"Failed ({failed_count})"],
        colors=["#4CAF50", "#f44336"],
        autopct="%1.1f%%",
        startangle=90
    )
    ax2.set_title("Pass / Fail Breakdown")

    plt.tight_layout()
    plt.savefig("results.png", dpi=150)
    print("\nChart saved as results.png")
    plt.show()


def main():
    if not os.path.exists(CSV_FILE):
        print(f"Error: '{CSV_FILE}' not found. Make sure it's in the same folder.")
        return

    print(f"Loading data from {CSV_FILE}...\n")
    students = load_data(CSV_FILE)
    summary = get_summary(students)

    print_report(students, summary)

    show_chart = input("\nShow chart? (y/n): ").strip().lower()
    if show_chart == "y":
        plot_results(students, summary)


main()