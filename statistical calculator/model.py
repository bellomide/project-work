import statistics
import os

def is_prime(n):

    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n):
    
    if n < 2:
        return False
    factors_sum = sum(i for i in range(1, n) if n % i == 0)
    return factors_sum == n

def analyze_number(n):
    
    return {
        "Number": n,
        "Even/Odd": "Even" if n % 2 == 0 else "Odd",
        "Prime": is_prime(n),
        "Perfect": is_perfect(n),
        "Positive/Negative": "Positive" if n >= 0 else "Negative"
    }

if __name__ == "__main__":
    print("📢 Welcome to Number Analyzer Pro+")
    numbers = []

    while True:
        try:
            raw = input("Enter a number (or type 0 or q to finish): ").strip()
            if raw.lower() == 'q':
                print("Exiting input (q received).")
                break
            num = int(raw)
            if num == 0:
                break
            numbers.append(num)
        except ValueError:
            print("⚠️ Please enter a valid integer (or 0/q to finish).")


    print("\n=== ANALYSIS RESULT ===")
    results = [analyze_number(n) for n in numbers]

    for r in results:
        print(f"{r['Number']} ➤ {r['Even/Odd']} | Prime: {r['Prime']} | Perfect: {r['Perfect']} | {r['Positive/Negative']}")


    mean_val = median_val = None
    mode_display = "N/A"

    if numbers:
        print("\n=== STATISTICS SUMMARY ===")
        try:
            mean_val = statistics.mean(numbers)
            median_val = statistics.median(numbers)
            mode_list = statistics.multimode(numbers)  
            mode_display = ", ".join(str(m) for m in mode_list)
        except statistics.StatisticsError as e:
            print("⚠️ Statistics error:", e)
            mode_display = "N/A"

        print(f"Total Numbers: {len(numbers)}")
        if mean_val is not None:
            print(f"Mean: {mean_val:.2f}")
            print(f"Median: {median_val:.2f}")
            print(f"Mode(s): {mode_display}")
    else:
        print("No numbers entered!")


    save = input("\nDo you want to save this report? (yes/no): ").strip().lower()
    if save == 'yes':
        
        default_dir = "reports"
        os.makedirs(default_dir, exist_ok=True)
        suggested_name = "number_analysis_report.txt"
        user_filename = input(f"Enter filename (press Enter to use '{suggested_name}'): ").strip()
        if user_filename == "":
            user_filename = suggested_name

        user_filename = os.path.basename(user_filename)
        if not user_filename.lower().endswith('.txt'):
            user_filename += '.txt'

        full_path = os.path.join(default_dir, user_filename)

        try:
            with open(full_path, "w", encoding="utf-8") as f:
                f.write("NUMBER ANALYZER PRO+ REPORT\n\n")
                if results:
                    for r in results:
                        f.write(f"{r['Number']}   {r['Even/Odd']} | Prime: {r['Prime']} | Perfect: {r['Perfect']} | {r['Positive/Negative']}\n")
                else:
                    f.write("No numbers were entered.\n")

        
                if numbers and mean_val is not None:
                    f.write("\n=== STATISTICS SUMMARY ===\n")
                    f.write(f"Total: {len(numbers)}\n")
                    f.write(f"Mean: {mean_val:.2f}\n")
                    f.write(f"Median: {median_val:.2f}\n")
                    f.write(f"Mode(s): {mode_display}\n")
            print(f"✅ Report saved as '{full_path}'")
        except PermissionError:
            print("❌ Permission denied: cannot write file to that location. Try a different filename or run the program with permission to create files.")
        except FileNotFoundError:
            print("❌ File path not found. Ensure the directory exists or choose a different filename.")
        except Exception as e:
            print("❌ An unexpected error occurred while saving the report:", e)
    else:
        print("Report not saved.")