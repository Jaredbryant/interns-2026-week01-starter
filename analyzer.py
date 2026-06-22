import csv
from datetime import datetime

DATA = "/workspace/interns-2026-week01-starter/data/spot_patrol_data.csv"


def load_data(filename):
    try:
        with open(filename) as file:
            reader = csv.DictReader(file)
            rows = list(reader)
        return rows
    except FileNotFoundError:
        print("ERROR: CSV file not found.")
        return []
    except Exception as e:
        print(f"ERROR loading file: {e}")
        return []


def mission_summary(rows):
    laps = set()
    waypoints = set()
    sensors = set()

    for row in rows:
        laps.add(row["lap"])
        waypoints.add(row["waypoint"])
        sensors.add(row["sensor_id"])

    return {
        "total_readings": len(rows),
        "laps": len(laps),
        "waypoints": len(waypoints),
        "sensor_types": len(sensors)
    }


def find_faults(rows):
    faults = []

    for row in rows:
        if row["status"] != "OK":
            faults.append(row)

    return faults

def sensor_averages(rows):
    sensor_data = {}

    for row in rows:
        sensor = row["sensor_id"]
        value = float(row["value"])

        if sensor not in sensor_data:
            sensor_data[sensor] = []

        sensor_data[sensor].append(value)

    averages = {}

    for sensor, values in sensor_data.items():
        averages[sensor] = sum(values) / len(values)

    return averages
def write_report(summary, faults, averages):
    try:
        with open("/workspace/interns-2026-week01-starter/mission_report.txt.txt", "w") as file:

            file.write("SPOT PATROL MISSION REPORT\n")
            file.write("=" * 30 + "\n")

            timestamp = datetime.now()

            file.write(f"Generated: {timestamp}\n\n")

            file.write("MISSION SUMMARY\n")
            file.write("-" * 20 + "\n")
            file.write(f"Total readings: {summary['total_readings']}\n")
            file.write(f"Unique laps: {summary['laps']}\n")
            file.write(f"Unique waypoints: {summary['waypoints']}\n")
            file.write(f"Unique sensor types: {summary['sensor_types']}\n\n")

            file.write("FAULT DETECTION\n")
            file.write("-" * 20 + "\n")

            for fault in faults:
                file.write(
                    f"{fault['timestamp']} "
                    f"{fault['waypoint']} "
                    f"{fault['sensor_id']} "
                    f"{fault['value']} "
                    f"{fault['unit']} "
                    f"{fault['status']}\n"
                )

            file.write(f"\nTotal faults: {len(faults)}\n\n")

            file.write("PER-SENSOR AVERAGES\n")
            file.write("-" * 20 + "\n")

            sorted_averages = sorted(
                averages.items(),
                key=lambda sensor: sensor[1],
                reverse=True
            )

            for sensor, average in sorted_averages:
                file.write(f"{sensor}: {average:.2f}\n")

        print("\nmission_report.txt created successfully.")

    except Exception as e:
        print(f"ERROR writing report: {e}")


def main():
    rows = load_data(DATA)
    print(f"Rows loaded: {len(rows)}")

    summary = mission_summary(rows)

    print("Mission Summary")
    print(f"Total readings: {summary['total_readings']}")
    print(f"Unique laps: {summary['laps']}")
    print(f"Unique waypoints: {summary['waypoints']}")
    print(f"Unique sensor types: {summary['sensor_types']}")

    faults = find_faults(rows)

    print("\nFault Detection")
    for fault in faults:
        print(
            fault["timestamp"],
            fault["waypoint"],
            fault["sensor_id"],
            fault["value"],
            fault["unit"],
            fault["status"]
        )

    print(f"Total faults: {len(faults)}")
    
    averages = sensor_averages(rows)

    print("\nPer-Sensor Averages")

    sorted_averages = sorted(
        averages.items(),
        key=lambda item: item[1],
        reverse=True
    )

    for sensor, average in sorted_averages:
        print(f"{sensor}: {average:.2f}")
        
    write_report(summary, faults, averages)


if __name__ == "__main__":
    main()
