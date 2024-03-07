import time
import waypoint

'''
assuming we are looking at a sqaure
starting at the top left
facing right
using a regular cartesian plane

53.381629, -112.754504
-112.754504 = left and right
53.381629 = up and down
0.00001 = 1.11m

'''

def coor_input():
    # still need to validate that the coordinates are not too far apart
    # also need to check to see that the coordinates are valid, for examples top left is above bottom left and to the right to top left

    # #tp_left=input("What is the top left coordinte? No spaces, and x and y seperated by a comma. Enter like 'x,y'> ")
    # tp_left=input("top left coordinte> ")
    # numbers = tp_left.split(",")
    # tp_left = [int(num) for num in numbers]
   
    # #tp_right=input("What is the top right coordinte? No spaces, and x and y seperated by a comma. Enter like 'x,y'> ")
    # tp_right=input("top right coordinte> ")
    # numbers = tp_right.split(",")
    # tp_right = [int(num) for num in numbers]
    
    # # btm_left=input("What is the bottom left coordinte? No spaces, and x and y seperated by a comma. Enter like 'x,y'> ")
    # btm_left=input("bottom left coordinte> ")
    # numbers = btm_left.split(",")
    # btm_left = [int(num) for num in numbers]
    
    # # btm_right=input("What is the bottom right coordinte? No spaces, and x and y seperated by a comma. Enter like 'x,y'> ")
    # btm_right=input("bottom right coordinte> ")
    # numbers = btm_right.split(",")
    # btm_right = [int(num) for num in numbers]
    

    # tp_left = [53.381629, -112.754504] 
    # tp_right = [53.381629,-112.742207] 
    # btm_left = [53.374379,-112.754504] 
    # btm_right = [53.374379, -112.742207] 

    # Parshva's test number
    tp_left = [53.199693, -113.610326] 
    tp_right = [53.199620, -113.598547] 
    btm_left = [53.192517, -113.610150] 
    btm_right = [53.192490, -113.599008] 
    
    tp_left.reverse()
    tp_right.reverse()
    btm_left.reverse() 
    btm_right.reverse()

    # all retuns are a array
    return tp_left,tp_right,btm_left,btm_right
def flight_creation(tp_left,tp_right,btm_left,btm_right):
    # # Find the x-coordinate range between left and right
    # x_range = []
    # x = tp_left[0]
    # while x <= tp_right[0]:
    #     x_range.append(x)
    #     x += 1

    # y_range = []0
    # y = tp_left[1]
    # while y >= btm_left[1]:
    #     y_range.append(y)
    #     y = y-1
    # print("\nx range")
    # print(x_range)  
    # print("\ny range")  
    # print(y_range)

    # total_paris = len(x_range)*len(y_range)
    
    # for i in range(total_paris):

    # Find the x and y ranges of the rectangle

    x_displament_fct=0.00001
    y_displament_fct=0.00002


    x_range = []
    x = tp_left[0]
    while x <= tp_right[0]:
        x_range.append(x)
        x += x_displament_fct

    y_range = []
    y = btm_left[1]
    while y <= tp_left[1]:
        y_range.append(y)
        y += y_displament_fct
    y_range.reverse()

    y_travel=0
    
    # Create a list of all the coordinates in the middle, including corners
    coordinates = []
    for y in y_range:
        for x in x_range:
            coordinates.append([y, x])
        x_range.reverse()
        y_travel+=1

    # Print the resulting list of coordinates
    return coordinates,y_travel
    
    
    # x_range = list(range(tp_left[0],tp_right[0]+1))
    # y_range = list(range(btm_left[1],tp_left[1]+1))
    # # print(x_range)
    # # print(y_range)
    # # coordinates = []
    # # for i in y_range:
    # #     x=tp_left[0]
    # #     for j in x_range:
    # #         coordinates.append([x,y])
    # # return coordinates
    # coordinates = []
    # x = tp_left[0]
    # y = tp_left[1]
    # while y >= btm_left[1]:
    #     if x == tp_left[0]:
    #         while x <= tp_right[0]:
    #             coordinates.append([x,y])
    #             x = x + 1
    #     else:
    #         while x >= tp_left[0]:
    #             coordinates.append([x,y])
    #             x = x-1
    #     y = y-1

    # return coordinates

def results(coordinates,tp_left,tp_right,btm_left,btm_right,y_travel):

    span_x=tp_right[0]-tp_left[0]
    span_y=tp_left[1]-btm_left[1]
    return_dis=(span_x**2 + span_y**2)**0.5
    distance_x=tp_right[0]-tp_left[0]

    total_x=distance_x*y_travel

    distance_y=tp_left[1]-btm_left[1]

    total_travel=total_x+distance_y+return_dis

    print()
    print("the coordinates are:")
    print("tp_left")
    print(tp_left)
    print("tp_right")
    print(tp_right)
    print("btm_left")
    print(btm_left)
    print("btm_right")
    print(btm_right)
    print()
    print("please wait...")
    for i in coordinates:
        print(i)
    print("coordinates list has "+str(len(coordinates))+" pairs")
    print("The coordinates horizontally span from "+str(tp_left[0])+" to "+str(tp_right[0])+" with a net of " + str(span_x))
    print("The coordinates vertically span from "+str(tp_left[1])+" to "+str(btm_left[1])+" with a net of " + str(span_y))
    print()
    print("the total travel distance in km is "+str(total_travel*111.11))

        
    
def main():
    tp_left = [53.199693, -113.610326] 
    tp_right = [53.199620, -113.598547] 
    btm_left = [53.192517, -113.610150] 
    btm_right = [53.192490, -113.599008] 

    # start_time = time.time()
    # #list of list
    # flight_path=[]
    # print('\npassed line 166')
    # tp_left,tp_right,btm_left,btm_right=coor_input()
    # print('\npassed line 168')
    # print("please wait...")
    # coordinates,y_travel=flight_creation(tp_left,tp_right,btm_left,btm_right)
    # print('\npassed line 170')
    # results(coordinates,tp_left,tp_right,btm_left,btm_right,y_travel)
    # end_time = time.time()
    # elapsed_time = end_time - start_time
    # print(f"Elapsed time: {elapsed_time} seconds")

    path = waypoint.WaypointCont()
    path.setTopLeft(53.199693, -113.610326)
    path.setTopRight(53.199620, -113.598547)
    path.setBottomLeft(53.192517, -113.610150)
    path.setBottomRight(53.192490, -113.599008)

    path.createFlightPath()
    path.printPathway()
    
if __name__ == "__main__":
    main()    
