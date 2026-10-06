

import random
import time
import platform
import subprocess
import matplotlib.pyplot as plt
import os
import math
import struct
import tempfile

# ------------------------------------------------------------
# Settings
# ------------------------------------------------------------

DEFAULT_LIST_SIZE = 20
MIN_VALUE = 1
MAX_VALUE = 100
ANIMATION_DELAY = 0.10
SOUND_ENABLED = True
LOW_FREQUENCY = 200
HIGH_FREQUENCY = 1200


# ------------------------------------------------------------
# Sound Functions
# ------------------------------------------------------------


def value_to_frequency(value):
    clamped_val = max(MIN_VALUE, min(MAX_VALUE, value))
    normalized = (clamped_val - MIN_VALUE) / (MAX_VALUE - MIN_VALUE)
    return LOW_FREQUENCY + normalized * (HIGH_FREQUENCY - LOW_FREQUENCY)






def play_value_sound(value):
    if not SOUND_ENABLED:
        return
    freq = value_to_frequency(value)
    duration_sec = 0.15
    sample_rate = 44100

    try:
        os_name = platform.system()

        if os_name == "Windows":
            import winsound

            winsound.Beep(int(freq), int(duration_sec * 1000))

        elif os_name == "Darwin":  
            num_samples = int(sample_rate * duration_sec)
            pcm_data = bytearray()
            for i in range(num_samples):
                sample = int(
                    32767 * 0.3 * math.sin(2 * math.pi * freq * i / sample_rate)
                )
                pcm_data.extend(struct.pack("<h", sample))
            data_size = len(pcm_data)
            header = struct.pack(
                "<4sI4s4sIHHIIHH4sI",
                b"RIFF",
                36 + data_size,
                b"WAVE",
                b"fmt ",
                16,
                1,
                1,
                sample_rate,
                sample_rate * 2,
                2,
                16,
                b"data",
                data_size,
            )
            with tempfile.NamedTemporaryFile(
                suffix=".wav", delete=False
            ) as temp_wav:
                temp_wav.write(header + pcm_data)
                temp_wav_path = temp_wav.name

            try:
                subprocess.run(
                    ["afplay", temp_wav_path],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    check=False,
                )
            finally:
                if os.path.exists(temp_wav_path):
                    os.remove(temp_wav_path)

        elif os_name == "Linux":
            subprocess.run(
                ["aplay", "-q"],
                input=pcm_data,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False,
            )

    except Exception:
        pass


# ------------------------------------------------------------
# Utility Functions
# ------------------------------------------------------------

def generate_list(size=DEFAULT_LIST_SIZE):
    mylist = [random.randint(MIN_VALUE, MAX_VALUE) for i in range(size)]
    return mylist



def draw_list(values, title="Sorting"):
    """
    Draw the current list as a bar graph.

    You do not need to modify this function unless you want to
    experiment with the visualization.
    """
    plt.clf()

    plt.bar(range(len(values)), values)

    plt.title(title)
    plt.xlabel("Index")
    plt.ylabel("Value")

    plt.pause(ANIMATION_DELAY)


# ------------------------------------------------------------
# Sorting Algorithms
# ------------------------------------------------------------

def selection_sort(values):

    n = len(values)

    for i in range(n):
        min = i

        for j in range(i + 1, n):
            if values[j] < values[min]:
                min = j

        values[i], values[min] = values[min], values[i]

        draw_list(values)
        play_value_sound(values[i])

    draw_list(values)
    return values


def bubble_sort(values):

    n = len(values)
    for i in range(n):
        swapped = False

        for j in range(0, n - i - 1 ):
            if values[j] > values[j + 1]:
                values[j] , values[j + 1] = values[j + 1], values[j]
                draw_list(values)
                play_value_sound(values)
                swapped = True
        if not swapped:
            break
        

def insertion_sort(values):

    n = len(values)

    for i in range(1, n):
        current = values[i]
        j = i - 1

        while j >= 0 and values[j] > current:
            values[j + 1] = values[j]
            j -= 1

        values[j + 1] = current
        draw_list(values)
        play_value_sound(values[i])
    draw_list(values)
    return values


def merge(left, right):
    newlist = []
    i = 0
    j = 0

    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            newlist.append(left[i])
            i += 1
        else:
            newlist.append(right[j])
            j += 1

    newlist += left[i:] + right[j:]

    return newlist


def merge_sort(values):
    n = len(values)

    if n <= 1:
        return values

    half = n // 2

    left = values[0:half]
    right = values[half:]

    left = merge_sort(left)
    right = merge_sort(right)

    merged = merge(left, right)

    draw_list(merged)

    return merged


def quick_sort(values):

    n = len(values)

    if n <= 1:
        return values

    point = n // 2
    pivot = values[point]

    left = []
    right = []

    for i in range(n):
        if i == point:
            continue

        if values[i] < pivot:
            left.append(values[i])
        else:
            right.append(values[i])

    left = quick_sort(left)
    right = quick_sort(right)

    sorted_values = left + [pivot] + right

    for i in range(len(sorted_values)):
        values[i] = sorted_values[i]
        draw_list(values)
        play_value_sound(values[i])

    return values
# -------------------------------
# -----------------------------
# Algorithm Explanations / Pseudocode
# ------------------------------------------------------------

def print_selection_info():

    print("Start with the first index and make it the minimum. Then look to the right and compare each value. If you find a value that is smaller than the current minimum, make that value the new minimum. Continue looking until you reach the end of the list. Then swap the minimum value with the value at the starting index.")

    print("1. Find the length of the list.")
    print("2. Start at the first position.")
    print("3. Make the starting position the minimum.")
    print("4. Look through all the values to the right.")
    print("5. If you find a smaller value, make its index the new minimum.")
    print("6. Once you reach the end, swap the minimum with the starting position.")
    print("7. Move to the next position and repeat.")


    
def print_bubble_info():

    print("Start the beggining of the list and compare the number next to if. If it needs to be swapped then do it, if not move on the next. Always comparing i to i + 1.")
    print("1. Start at the first position.")
    print("2. Compare the current value with the value next to it.")
    print("3. If the current value is larger, swap the two values.")
    print("4. Move to the next position.")
    print("5. Continue until you reach the end of the list.")
    print("6. Repeat the process because the largest unsorted value will move to the end.")
    print("7. Continue until the list is sorted.")


def print_insertion_info():

    print("Start at the second index and treat the value there as the current value. Compare it with the values to its left. If a value to the left is larger, shift that value one position to the right. Continue moving left until you find the correct position for the current value. Insert the current value there, then move to the next index and repeat until the list is sorted.")

    print("1. Find the length of the list.")
    print("2. Start at the second position because the first value is already considered sorted.")
    print("3. Save the current value.")
    print("4. Compare the current value with the values to its left.")
    print("5. If a value to the left is larger, shift it one position to the right.")
    print("6. Continue moving left until you find the correct position.")
    print("7. Place the current value in that position.")
    print("8. Move to the next position and repeat until the list is sorted.")


def print_merge_info():

    print("Start by splitting the list into two smaller lists. Continue splitting each list in half until every list contains only one value. Then begin merging the smaller lists back together. Compare the first values of the two lists and place the smaller value into the new list. Continue comparing and adding values until both lists have been merged. Repeat this process until the entire list is sorted.")

    print("1. Find the length of the list.")
    print("2. If the list has one or zero values, it is already sorted.")
    print("3. Split the list into two halves.")
    print("4. Recursively split each half until each list contains one value.")
    print("5. Compare the first values of the two lists.")
    print("6. Add the smaller value to the new sorted list.")
    print("7. Continue comparing values until one list is empty.")
    print("8. Add the remaining values from the other list.")
    print("9. Continue merging the lists until the entire list is sorted.")


def print_quick_info():

    print("Start by choosing one value as the pivot. Then look at every other value and separate them into two groups. Values smaller than the pivot go to the left, and values greater than or equal to the pivot go to the right. Recursively quick sort the left and right groups. Finally, combine the sorted left group, the pivot, and the sorted right group to create the sorted list.")

    print("1. Find the length of the list.")
    print("2. If the list has one or zero values, it is already sorted.")
    print("3. Choose a value to use as the pivot.")
    print("4. Create a left list and a right list.")
    print("5. Compare each value to the pivot.")
    print("6. Put values smaller than the pivot into the left list.")
    print("7. Put values greater than or equal to the pivot into the right list.")
    print("8. Recursively quick sort the left and right lists.")
    print("9. Combine the sorted left list, the pivot, and the sorted right list.")
    print("10. Return the sorted list.")


def print_info_menu():
    print()
    print("ALGORITHM INFORMATION")
    print()
    print("1. Selection Sort")
    print("2. Bubble Sort")
    print("3. Insertion Sort")
    print("4. Merge Sort")
    print("5. Quick Sort")
    print("6. Return to Main Menu")
    print()


def algorithm_info_menu():
    while True:

        print_info_menu()

        choice = input("Choice: ").strip()

        if choice == "1":
            print_selection_info()

        elif choice == "2":
            print_bubble_info()

        elif choice == "3":
            print_insertion_info()

        elif choice == "4":
            print_merge_info()

        elif choice == "5":
            print_quick_info()

        elif choice == "6":
            break

        else:
            print("Invalid choice. Please enter a number from 1 through 6.")


# ------------------------------------------------------------
# Menu
# ------------------------------------------------------------

def print_menu():
    print()
    print("SORTING VISUALIZER")
    print()
    print("1. Generate New Random List")
    print("2. Selection Sort")
    print("3. Bubble Sort")
    print("4. Insertion Sort")
    print("5. Merge Sort")
    print("6. Quick Sort")
    print("7. Algorithm Information / Pseudocode")
    print("8. Exit")
    print()


def main():

    # Interactive plotting allows the graph to update repeatedly.
    plt.ion()

    values = generate_list()

    while True:

        print()
        print("Current List:")
        print(values)

        print_menu()

        choice = input("Choice: ").strip()

        if choice == "1":
            values = generate_list()
            draw_list(values, "New Random List")

        elif choice == "2":
            working_list = values.copy()
            draw_list(working_list, "Selection Sort")
            selection_sort(working_list)
            print("Sorted List:")
            print(working_list)

        elif choice == "3":
            working_list = values.copy()
            draw_list(working_list, "Bubble Sort")
            bubble_sort(working_list)
            print("Sorted List:")
            print(working_list)

        elif choice == "4":
            working_list = values.copy()
            draw_list(working_list, "Insertion Sort")
            insertion_sort(working_list)
            print("Sorted List:")
            print(working_list)

        elif choice == "5":
            working_list = values.copy()
            draw_list(working_list, "Merge Sort")

            # You may need to modify this section depending on
            # how you implement merge_sort().
            result = merge_sort(working_list)

            if result is not None:
                working_list = result

            print("Sorted List:")
            print(working_list)

        elif choice == "6":
            working_list = values.copy()
            draw_list(working_list, "Quick Sort")

            result = quick_sort(working_list)

            if result is not None:
                working_list = result

            print("Sorted List:")
            print(working_list)

        elif choice == "7":
            algorithm_info_menu()

        elif choice == "8":
            print("Goodbye.")
            break

        else:
            print("Invalid choice. Please enter a number from 1 through 8.")

    plt.ioff()
    plt.close()


if __name__ == "__main__":
    main()
