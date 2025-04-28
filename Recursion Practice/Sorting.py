from random import randint
from tkinter import *
from time import sleep

Z = 400

tk = Tk()
c = Canvas(tk, width=Z, height=Z)
c.pack()



def get_shade(darkness):
    # Ensure darkness is within the range of 0 to 100
    darkness = max(0, min(100, darkness))
    # Map the darkness value to a range from 128 (light gray) to 0 (black)
    gray_value = int(128 * (1 - darkness / 100))  # Darker shades only
    return f"#{gray_value:02x}{gray_value:02x}{gray_value:02x}"  # Return hex color code



def display(nums):
    c.delete("all")
    w = Z / len(nums)
    for i, num in enumerate(nums):
        c.create_rectangle(i*w, Z, i*w+w, Z*(num/max(nums)), fill = get_shade(num), width = 0)
    sleep(.25)
    tk.update()

def insertion(nums):
    for i, num in enumerate(nums[:]):
        j = i
        while j > 0 and num < nums[j-1]:
            temp = nums[j-1]
            nums[j-1] = num
            nums[j] = temp
            j -= 1
            
            #
            display(nums)
            #
        
def selection(nums):
    for i in range(len(nums)):
        val = min(nums[i:])
        j = i + nums[i:].index(val)
        temp = nums[i]
        nums[i] =  val
        nums[j] = temp
        display(nums)


# can't really display mergesort in the same way because it doesn't stay as one big group or change one thing at a time
def merge(nums):
    if len(nums) < 2:
        return
    midi = len(nums)//2
    left = nums[:midi]
    right = nums[midi:]
    merge(left)
    merge(right)
    
    nums.clear()
    while left and right:
        if left[0] < right[0]:
            nums.append(left.pop(0))
        else:
            nums.append(right.pop(0))
    # take care of any excess
    nums.extend(left)
    nums.extend(right)



nums = [randint(0, 100) for _ in range(10)]
print(nums)
selection(nums)
print(nums)

sleep(5)