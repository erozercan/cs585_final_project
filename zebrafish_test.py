import cv2 as cv

def read_txt_file(filepath):
    with open(filepath, 'r') as file:
        data = file.readlines()
    data_list = []
    for line in data:
        data_list.append(line.split(","))
    return data_list

def get_two_fish_locations(frame_num,fish_data):
    return fish_data[(frame_num-1)*2],fish_data[(frame_num-1)*2+1]

def get_five_fish_locations(frame_num,fish_data):
    return fish_data[(frame_num-1)*5],fish_data[(frame_num-1)*5+1],fish_data[(frame_num-1)*5+2],fish_data[(frame_num-1)*5+3],fish_data[(frame_num-1)*5+4]

def divide_video(videopath):
    cap = cv.VideoCapture(videopath)  # Replace 'original_video.mp4' with the path to your video file

    # Get the original video resolution
    original_width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    original_height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))

    # Define the width of each half
    half_width = original_width // 2

    # Create VideoWriter objects for each half
    out1 = cv.VideoWriter('first_half.mp4', cv.VideoWriter_fourcc(*'mp4v'), 30, (half_width, original_height))
    out2 = cv.VideoWriter('second_half.mp4', cv.VideoWriter_fourcc(*'mp4v'), 30, (half_width, original_height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Split the frame into two halves
        first_half = frame[:, :half_width, :]
        second_half = frame[:, half_width:, :]
        
        # Write the halves to the corresponding output videos
        out1.write(first_half)
        out2.write(second_half)

    # Release VideoCapture and VideoWriter objects
    cap.release()
    out1.release()
    out2.release()
# [[1,2],[3,4],[5,6],[7,8]]

def two_fish_tracking(videopath, coord_path, output_path):
    cap = cv.VideoCapture(videopath)

    data = read_txt_file(coord_path)
    frame_width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
    print (frame_width,frame_height)

    fps = int(cap.get(cv.CAP_PROP_FPS))
    fourcc = cv.VideoWriter_fourcc(*'mp4v')

        # left right // top bottom
    new_width = frame_width - 320 - 355
    new_height = frame_height - 40 - 55

    # Define the region of interest (ROI) for cropping
    x_start, y_start = 320, 40
    x_end, y_end = frame_width - 355, frame_height - 55

    out = cv.VideoWriter(output_path, fourcc, fps, (new_width, new_height))
    frame_index = 1

    while cap.isOpened():
    # Capture frame-by-frame
        ret, frame = cap.read()
        #print (ret)
        if not ret:
            break
        if frame_index < 2000:
            fish1,fish2 = get_two_fish_locations(frame_index,data)
            fish1X, fish1Y, fish1width, fish1height = int(fish1[2]),int(fish1[3]),int(fish1[4]),int(fish1[5])
            fish2X, fish2Y, fish2width, fish2height = int(fish2[2]),int(fish2[3]),int(fish2[4]),int(fish2[5])
            cv.rectangle(frame, (fish1X, fish1Y), (fish1X + fish1width, fish1Y + fish1height), (0,0,255), thickness=2)
            cv.rectangle(frame, (fish2X, fish2Y), (fish2X + fish2width, fish2Y + fish2height), (0,0,255), thickness=2)
            # Write the modified frame to the output video
            cropped_frame = frame[y_start:y_end, x_start:x_end]

            # Write the modified cropped frame to the output video
            out.write(cropped_frame)

            # Move to the next frame
            frame_index += 1

    # Release the VideoCapture and VideoWriter objects
    cap.release()
    out.release()

def five_fish_tracking(videopath, coord_path, output_path):
    cap = cv.VideoCapture(videopath)

    data = read_txt_file(coord_path)
    frame_width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))

    fps = int(cap.get(cv.CAP_PROP_FPS))
    fourcc = cv.VideoWriter_fourcc(*'mp4v')

        # Calculate new dimensions after cropping
    new_width = frame_width - 320 - 355
    new_height = frame_height - 40 - 30

    # Define the region of interest (ROI) for cropping
    x_start, y_start = 320, 40
    x_end, y_end = frame_width - 355, frame_height - 30

    out = cv.VideoWriter(output_path, fourcc, fps, (new_width, new_height))
    frame_index = 1

    while cap.isOpened():
    # Capture frame-by-frame
        ret, frame = cap.read()
        #print (ret)
        if not ret:
            break
        if frame_index < 2000:
            fish1,fish2,fish3,fish4,fish5 = get_five_fish_locations(frame_index,data)

            fish1X, fish1Y, fish1width, fish1height = int(fish1[2]),int(fish1[3]),int(fish1[4]),int(fish1[5])
            fish2X, fish2Y, fish2width, fish2height = int(fish2[2]),int(fish2[3]),int(fish2[4]),int(fish2[5])
            fish3X, fish3Y, fish3width, fish3height = int(fish3[2]),int(fish3[3]),int(fish3[4]),int(fish3[5])
            fish4X, fish4Y, fish4width, fish4height = int(fish4[2]),int(fish4[3]),int(fish4[4]),int(fish4[5])
            fish5X, fish5Y, fish5width, fish5height = int(fish5[2]),int(fish5[3]),int(fish5[4]),int(fish5[5])

            cv.rectangle(frame, (fish1X, fish1Y), (fish1X + fish1width, fish1Y + fish1height), (0,0,255), thickness=2)
            cv.rectangle(frame, (fish2X, fish2Y), (fish2X + fish2width, fish2Y + fish2height), (0,0,255), thickness=2)
            cv.rectangle(frame, (fish3X, fish3Y), (fish3X + fish3width, fish3Y + fish3height), (0,0,255), thickness=2)
            cv.rectangle(frame, (fish4X, fish4Y), (fish4X + fish4width, fish4Y + fish4height), (0,0,255), thickness=2)
            cv.rectangle(frame, (fish5X, fish5Y), (fish5X + fish5width, fish5Y + fish5height), (0,0,255), thickness=2)
            # Write the modified frame to the output video
            cropped_frame = frame[y_start:y_end, x_start:x_end]

            # Write the modified cropped frame to the output video
            out.write(cropped_frame)

            # Move to the next frame
            frame_index += 1

    # Release the VideoCapture and VideoWriter objects
    cap.release()
    out.release()

def scale_fish(data):
    txt_data = []
    for row in data:
        frame,id,preX,preY = row[0],row[1],row[5],row[6]
        txt_data.append((frame,id,(int(preX)//2)-320,(int(preY)//2)-40))
    with open("output.txt", "w") as file:
        for entry in txt_data:
            file.write(",".join(map(str, entry)) + "\n")


def scale_fish_box(data):
    txt_data = []
    for row in data:
        frame,id,boundingX,boundingY, boundingWidth, boundingHeight = row[0],row[1],row[7],row[8],row[9],row[10]
        txt_data.append((frame,id,(int(boundingX)//2),(int(boundingY)//2), int(boundingWidth)//2, int(boundingHeight)//2))
    with open("output.txt", "w") as file:
        for entry in txt_data:
            file.write(",".join(map(str, entry)) + "\n")

        
def test_scaled_data(videopath, coord_path,output_path):
    cap = cv.VideoCapture(videopath)
    data = read_txt_file(coord_path)
    frame_width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv.CAP_PROP_FPS))
    fourcc = cv.VideoWriter_fourcc(*'mp4v')

    out = cv.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))
    frame_index = 1

    while cap.isOpened():
    # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            break
        if frame_index < 2000:
            fish1,fish2 = get_two_fish_locations(frame_index,data)
            fish1X, fish1Y, fish1width, fish1height = int(fish1[2]),int(fish1[3]),int(fish1[4]),int(fish1[5])
            fish2X, fish2Y, fish2width, fish2height = int(fish2[2]),int(fish2[3]),int(fish1[4]),int(fish1[5])

            #cv.circle(frame, (fish1X, fish1X), 5, (255, 0, 0), -1)
            #cv.circle(frame, (fish2X, fish2Y), 5, (255, 0, 0), -1)
            cv.rectangle(frame, (fish1X, fish1Y), (fish1X + fish1width, fish1Y + fish1height), (0,0,255), thickness=2)
            cv.rectangle(frame, (fish2X, fish2Y), (fish2X + fish2width, fish2Y + fish2height), (0,0,255), thickness=2)

            # Write the modified frame to the output video

            # Write the modified cropped frame to the output video
            out.write(frame)

            # Move to the next frame
            frame_index += 1

    # Release the VideoCapture and VideoWriter objects
    cap.release()
    out.release()

def five_test_scaled_data(videopath, coord_path,output_path):
    cap = cv.VideoCapture(videopath)
    data = read_txt_file(coord_path)
    frame_width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv.CAP_PROP_FPS))
    fourcc = cv.VideoWriter_fourcc(*'mp4v')

    out = cv.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))
    frame_index = 1

    while cap.isOpened():
    # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            break
        if frame_index < 2000:
            fish1,fish2,fish3,fish4,fish5 = get_five_fish_locations(frame_index,data)
            fish1X, fish1Y = int(fish1[2]),int(fish1[3])
            fish2X, fish2Y = int(fish2[2]),int(fish2[3])
            fish3X, fish3Y = int(fish3[2]),int(fish3[3])
            fish4X, fish4Y = int(fish4[2]),int(fish4[3])
            fish5X, fish5Y = int(fish5[2]),int(fish5[3])

            cv.circle(frame, (fish1X, fish1Y), 5, (255, 0, 0), -1)
            cv.circle(frame, (fish2X, fish2Y), 5, (255, 0, 0), -1)
            cv.circle(frame, (fish3X, fish3Y), 5, (255, 0, 0), -1)
            cv.circle(frame, (fish4X, fish4Y), 5, (255, 0, 0), -1)
            cv.circle(frame, (fish5X, fish5Y), 5, (255, 0, 0), -1)

            # Write the modified frame to the output video

            # Write the modified cropped frame to the output video
            out.write(frame)

            # Move to the next frame
            frame_index += 1

    # Release the VideoCapture and VideoWriter objects
    cap.release()
    out.release()




# Example usage
video_path = 'data/ZebraFish-01/ZebraFish-01-raw.mp4'
first_half = 'first_half.mp4'
second_half = 'z3_second_half.mp4'
cropped = 'z4_cropped.mp4'
fish_locations_file = 'fish_locations.txt'
output_video_path = 'modified_fish_video.mp4'
coord_path = "data/ZebraFish-01/gt/gt.txt"
output_coords = "output.txt"

fish_locations = read_txt_file("/Users/jacksonfisk/Desktop/CS/cs585/a5/data/ZebraFish-04/gt/gt.txt")

scale_fish(fish_locations)

#test_scaled_data(second_half,output_coords,output_video_path)
#five_test_scaled_data(cropped,output_coords,output_video_path)

#divide_video(video_path)
#five_fish_tracking(second_half, output_coords, output_video_path)



#data = read_txt_file("/Users/jacksonfisk/Desktop/CS/cs585/a5/data/ZebraFish-01/gt/gt.txt")
#print (get_fish_locations(3,data))